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


def load_models()-> Model:
        # Load saved models
    
    model = load_model('./uploads/MODELO_NN.h5')

 
    VAEmodel = VAE(400, 5)
    VAEmodel.load_state_dict(torch.load('./uploads/MODELO_VAE.pth'))

        
    with open('./uploads/LABEL_ENCODER.pkl', 'rb') as file:
        label_encoder = pkl.load(file)
        
    modelo_final = Model(VAEmodel, model, label_encoder)
    
    return modelo_final


model = load_models()

predictons, separated_dfs = model.predict_multiple('./APPmedias.csv')

general = pd.concat(separated_dfs)

general['Predictions'] = general['Battery_ID'].map(predictons)

general.to_csv('predictions.csv', encoding='utf-8')