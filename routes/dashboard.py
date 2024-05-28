from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import pandas as pd
import numpy as np
import pickle as pkl, os
from werkzeug.utils import secure_filename


import numpy as np
import pandas as pd
import pickle as pkl
from tensorflow.keras.models import load_model
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

class Model():
    def __init__(self, VAEmodel, Classifier, label_encoder, input_dim=400):
        self.VAEmodel = VAEmodel
        self.Classifier = Classifier
        self.input_dim = input_dim
        self.label_encoder = label_encoder

    # Auxiliary functions
    def treat_data(self, data, desired_length=400):
        # Check if 'Qd' is in the DataFrame
        if 'Qd' in data:
            # Convert the pandas Series to a list
            data_list = data['Qd'].tolist()
            current_length = len(data_list)

            if current_length < desired_length:
                # Pad with zeros if shorter than desired length
                data_list.extend([0] * (desired_length - current_length))
            elif current_length > desired_length:
                # Truncate if longer than desired length
                data_list = data_list[:desired_length]

        return data_list

    def prepareData(self, data):

        # Assume data_list_of_lists is your list of lists representing input data points
        data_list_of_lists = data

        # Convert data to NumPy array and normalize to [0, 1]
        data_array = np.array(data_list_of_lists)
        max_value = 1.0974227
        data_array_normalized = data_array.astype(float) / max_value  # Normalize to [0, 1]

        # Convert NumPy array to PyTorch tensor
        data_tensor = torch.FloatTensor(data_array_normalized)
        return data_tensor

    def getEmbeddings(self, data_tensor):
        with torch.no_grad():
            mean, logvar = self.VAEmodel.encode(data_tensor)
        embeddings = torch.cat((mean, logvar), dim=1)  # Concatenate mean and logvar along dimension 1
        embeddings = embeddings.numpy()  # Convert embeddings tensor to NumPy array
        return embeddings

    def format_input(self, data_or_path):
        if isinstance(data_or_path, str):
            input_data = pd.read_csv(data_or_path)
        else:
            input_data = data_or_path
        treated_data = np.array([self.treat_data(input_data, self.input_dim)])
        data_tensor = self.prepareData(treated_data)
        data_embeddings = self.getEmbeddings(data_tensor)
        return pd.DataFrame(data_embeddings)

    # Methods
    def predict(self, data_or_path):
        formatted_data = self.format_input(data_or_path)
        class_probabilities = self.Classifier.predict(formatted_data)
        prediction = np.argmax(class_probabilities, axis=1)
        return self.label_encoder.inverse_transform(prediction)[0]

    def predict_multiple(self, path_to_data):
        df = pd.read_csv(path_to_data)
        battery_ids = df['Battery_ID'].unique()
        # List to store separated DataFrames
        separated_dfs = []
        # Iterate over unique battery IDs
        for battery_id in battery_ids:
            # Filter the DataFrame for the current battery ID
            filtered_df = df[df['Battery_ID'] == battery_id]
            # Append the filtered DataFrame to the list
            separated_dfs.append(filtered_df)
        # Generate the prediction for each
        predictions = {}
        for battery_data in separated_dfs:
            prediction = self.predict(battery_data)
            predictions[battery_data["Battery_ID"].values[0]] = prediction
            print(prediction)
        return predictions, separated_dfs


class VAE(nn.Module):
    def __init__(self, input_size, latent_size):
        super(VAE, self).__init__()

        # Encoder layers
        self.encoder_fc1 = nn.Linear(input_size, 256)
        self.encoder_fc2_mean = nn.Linear(256, latent_size)
        self.encoder_fc2_logvar = nn.Linear(256, latent_size)

        # Decoder layers
        self.decoder_fc1 = nn.Linear(latent_size, 256)
        self.decoder_fc2 = nn.Linear(256, input_size)

    def encode(self, x):
        x = F.relu(self.encoder_fc1(x))
        mean = self.encoder_fc2_mean(x)
        logvar = self.encoder_fc2_logvar(x)
        return mean, logvar

    def reparameterize(self, mean, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return eps * std + mean

    def decode(self, z):
        z = F.relu(self.decoder_fc1(z))
        return torch.sigmoid(self.decoder_fc2(z))

    def forward(self, x):
        mean, logvar = self.encode(x)
        z = self.reparameterize(mean, logvar)
        return self.decode(z), mean, logvar

# Define the loss function
def vae_loss(recon_x, x, mu, logvar):
    BCE = F.binary_cross_entropy(recon_x, x, reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return BCE + KLD



dashboard = Blueprint('dashboard', __name__)

#generamos una lista con 6 colores en hexadecimal que sean diferentes y vistosos que resalten sobre el fondo negro-gris
colores = ["#FF5733", "#33FF57", "#3357FF", "#FF33F6", "#F6FF33", "#FF8B33", "#33FF8B", "#8B33FF", "#FF338B", "#8BFF33", 
           "#FFC133", "#33FFC1", "#C133FF", "#FF338C", "#8CFF33", "#FF4D33", "#33FF4D", "#4D33FF", "#FF334D", "#4DFF33"]


def creating_true_false_thresholds(df:pd.DataFrame, column:str, i:int):
    dataset = {
        "label":column,
        "data": [round(x, 3) for x in df[column].values],
        "type": "line",
        "backgroundColor": colores[-1 -i]
    }



def formating_data_to_frontend(df:pd.DataFrame, column: str, i:int, df_apoyo:pd.DataFrame = None):
    data_formated = {"labels": [round(x,2) for x in df["t"].values],
                     "datasets": [{"label": column,
                                   "data": [round(x, 3) for x in df[column].values],
                                   "fill": True,
                                   "borderColor": "rgb(75, 192, 192)",
                                   "backgroundColor": colores[i]}]}
    
    if df_apoyo is not None:
        dataset = {
            "label":"Media baterias recicables",
            "data": [round(x, 3) for x in df_apoyo[column].values],
            "type": "line",
            "backgroundColor": "#709775",
            "borderColor": "#709775",
            "fill": False,
            "radius": 0
        }
        
        dataset2 = {
            "label":"Media baterias NO recicables",
            "data": [round(x, 3) for x in df_apoyo[column].values],
            "type": "line",
            "backgroundColor": "#D62246",
            "borderColor": "#D62246",
            "fill": False,
            "radius": 0
        }
        
        data_formated["datasets"].append(dataset)
        data_formated["datasets"].append(dataset2)
    
    return data_formated

def load_models()-> Model:
        # Load saved models
    
    model = load_model('./uploads/MODELO_NN.h5')

 
    VAEmodel = VAE(400, 5)
    VAEmodel.load_state_dict(torch.load('./uploads/MODELO_VAE.pth'))

        
    with open('./uploads/LABEL_ENCODER.pkl', 'rb') as file:
        label_encoder = pkl.load(file)
        
    modelo_final = Model(VAEmodel, model, label_encoder)
    
    return modelo_final


@dashboard.route('/upload', methods=['POST'])
def upload_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        
        print(filename)

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "last_file.csv")
        print(file_path)
        file.save(file_path)
    
        return {"message": "File uploaded successfully"}, 200
    
    return {"message": "Error uploading file"}, 500

@dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard_route():
    #tomamos el último csv subido
    
    #leemos el csv
    #df = pd.read_csv('uploads/output.csv', sep=',', encoding='utf-8')
    
    #hacemos la predicción
    #df['pred'] = model.predict(df)
    
    #formateamos los datos para el frontend
    
    model = load_models()
    
    predictions, df = model.predict_multiple('uploads/last_file.csv')
    df = pd.concat(df)
    columns = df.columns
    
    
    print(predictions)
    
    print(len(df["Battery_ID"].unique()))
    res = {"plots": {}}
    
    if "Battery_ID" in columns: 
        for id_uniq in df["Battery_ID"].unique():
            df_id = df[df["Battery_ID"] == id_uniq]
            id_uniq = str(id_uniq)[-4:]
            res["plots"][id_uniq] = {}
            i = 0
            for column in columns:
                if column != "Battery_ID" and column != "pred":
                    data_formated = formating_data_to_frontend(df_id, column, i)
                    res["plots"][id_uniq][column] = data_formated
                    i += 1
                    
    else:
        res["plots"]["1"] = {}
        i = 0
        for column in columns:
            if column != "pred":
                data_formated = formating_data_to_frontend(df, column, i)
                res["plots"]["1"][column] = data_formated
                i += 1
                
    res["ids"] = list(res["plots"].keys())
    res["resultados"] = {str(key)[-4:]: True if value == "NOT" else False for key,value in predictions.items()}
    
    totales = len(res["resultados"].keys())
    positivos = len([x for x in res["resultados"].values() if x])
    negativos = totales - positivos
    
    cantidades = [totales, positivos, negativos]
    res["cantidades_resultados"] = cantidades
    
    return jsonify(res)

@dashboard.route('/results', methods=['POST'])
def send_final():
    data = request.json    
    df = pd.DataFrame(data["baterias"])
    #lo volcamos a un csv
    df.to_csv('uploads/decision_final.csv', index=False)
    
    
    return {"message": "Decision final enviada correctamente"}, 200