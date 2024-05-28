import pandas as pd
import numpy as np


df = pd.read_csv('./predictions.csv', encoding='utf-8')

#agrupamos los valores de la bateria

df.drop(columns=["Battery_ID"], inplace=True)

df = df.groupby(['Predictions', "t"]).mean()

# ponemos tanto la prediccion como el tiempo como columnas
df = df.reset_index()

# guardamos el archivo

df.to_csv('./predictions_means.csv', index=False)