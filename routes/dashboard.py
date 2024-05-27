from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle, os
from werkzeug.utils import secure_filename

dashboard = Blueprint('dashboard', __name__)

#generamos una lista con 6 colores en hexadecimal que sean diferentes y vistosos que resalten sobre el fondo negro-gris
colores = ["#FF5733", "#33FF57", "#3357FF", "#FF33F6", "#F6FF33", "#FF8B33", "#33FF8B", "#8B33FF", "#FF338B", "#8BFF33", 
           "#FFC133", "#33FFC1", "#C133FF", "#FF338C", "#8CFF33", "#FF4D33", "#33FF4D", "#4D33FF", "#FF334D", "#4DFF33"]
def formating_data_to_frontend(df:pd.DataFrame, column: str, i:int):
    data_formated = {"labels": [round(x,2) for x in df["t"].values],
                     "datasets": [{"label": column,
                                   "data": [round(x, 3) for x in df[column].values],
                                   "fill": True,
                                   "borderColor": "rgb(75, 192, 192)",
                                   "backgroundColor": colores[i]}]}
    
    return data_formated


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

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(file_path)
        file.save(file_path)
    
        return {"message": "File uploaded successfully"}, 200
    
    return {"message": "Error uploading file"}, 500

@dashboard.route('/dashboard', methods=['GET', 'POST'])
def dashboard_route():
    #tomamos el último csv subido
    
    #leemos el csv
    df = pd.read_csv('uploads/output.csv', sep=',', encoding='utf-8')
    
    #hacemos la predicción
    #df['pred'] = model.predict(df)
    
    #formateamos los datos para el frontend
    columns = df.columns
    
    #model = pickle.load(open('model.pkl', 'rb'))
    
    print(len(df["Battery_ID"].unique()))
    res = {"plots": {}}
    
    if "Battery_ID" in columns: 
        for id_uniq in df["Battery_ID"].unique()[:6]:
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
    res["resultados"] = {str(id_uniq)[-4:]: True for id_uniq in res["ids"]}
    
    totales = len(res["resultados"].keys())
    positivos = len([x for x in res["resultados"].values() if x])
    negativos = totales - positivos
    
    cantidades = [totales, positivos, negativos]
    res["cantidades_resultados"] = cantidades
    
    return jsonify(res)