from flask import Blueprint, request, jsonify, current_app
import pandas as pd

dashboard = Blueprint('dashboard', __name__)


def formating_data_to_frontend(df:pd.Dataframe, column: str):
    data_formated = {"labels": [x for x in df["t"].values],
                     "datasets": [{"label": column,
                                   "data": [x for x in df[column].values],
                                   "fill": False,
                                   "borderColor": "rgb(75, 192, 192)",
                                   "lineTension": 0.1}]}
    
    return data_formated
    
    
    

@dashboard.route('/dashboard', methods=['GET'])
def dashboard_route():
    
    #tomamos el último csv subido
    #leemos el csv
    df = pd.read_csv('uploads/ejemplo.csv', sep=',', encoding='utf-8')
    
    #hacemos la predicción
    #df['pred'] = model.predict(df)
    
    #formateamos los datos para el frontend
    columns = df.columns
    
    res = {"plots": {}}
    
    if "id" in columns: 
        for id_uniq in df["id"].unique():
            df_id = df[df["id"] == id_uniq]
            res["plots"][id_uniq] = {}
            for column in columns:
                if column != "id" and column != "pred":
                    data_formated = formating_data_to_frontend(df_id, column)
                    res["plots"][id_uniq][column] = data_formated

    
    else:
        res["plots"]["1"] = {}
        for column in columns:
            if column != "pred":
                data_formated = formating_data_to_frontend(df, column)
                res["plots"]["1"][column] = data_formated
    
    return jsonify(res)