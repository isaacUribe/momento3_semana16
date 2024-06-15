import requests as requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import io
import base64


app = Flask(__name__)

def get_data():

    #url de la api
    url = "https://jsonplaceholder.typicode.com/users"


    #Obtener datos mediante la libreria requests
    response = requests.get(url)


    #Validar si encuentra informacion 
    if response.status_code == 200:
        # Convierte la respuesta en formato JSON
        data = response.json()
        # Imprime los datos obtenidos
        print(type(data))
    else:
        print(f"Error en la solicitud: {response.status_code}")
        data = []
        
        
    #Convertir la data a un data frame
    df = pd.DataFrame(data)


    #Limpieza de datos
    df = df.dropna(subset=['name'])

    df = df.dropna(subset=['username'])

    df = df.dropna(subset=['phone'])

    df = df.dropna(subset=['website'])

    return df

@app.route('/')
def report():
    df = get_data()
    
    users_per_city = df['address'].apply(lambda x: x['city']).value_counts()

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    users_per_city.plot(kind='bar', color='skyblue')

    # Añadir título y etiquetas
    plt.title('Número de usuarios por ciudad')
    plt.xlabel('Ciudad')
    plt.ylabel('Número de usuarios')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return render_template('report.html', plot_url=plot_url, tables=[df.to_html(classes='data', header="true")])

if __name__ == '__main__':
    app.run(debug=True)
    
