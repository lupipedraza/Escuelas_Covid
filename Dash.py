#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:07:15 2021

@author: lucia
"""

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import math


archivo_escuelas = "escuelas.geojson"
escuelas = gpd.read_file(archivo_escuelas)
escuelas = escuelas.assign(positivos=0, sospechosos=0, burbujas_aisladas=0, escuela_cerrada=False)

def suma_sin_nulls(valores):
  res = 0
  for valor in valores:
    if not math.isnan(valor):
      res += valor
  return res

def valor_a_booleano(valor):
  return valor == "Sí"

datos_denuncias_archivo = "denuncias_covid.csv"
datos_denuncias = pd.read_csv(datos_denuncias_archivo)

for indice, denuncia in datos_denuncias.iterrows():
  cui_escuela = denuncia[2]
  if math.isnan(cui_escuela):
    continue
  
  cui_escuela = int(cui_escuela)

  filtro = (escuelas['cui'] == cui_escuela) # Ojo acá hay que filtrar los anexos. TODO
  fila_con_cui_escuela = escuelas[filtro]

  escuelas.loc[filtro, 'positivos'] = suma_sin_nulls(denuncia[3:7])
  escuelas.loc[filtro, 'sospechosos'] = suma_sin_nulls(denuncia[7:11])
  escuelas.loc[filtro, 'escuela_cerrada'] = valor_a_booleano(denuncia[11])
  escuelas.loc[filtro, 'burbujas_aisladas'] = suma_sin_nulls(denuncia[12:13])

escuelas_infectadas=escuelas[escuelas['burbujas_aisladas']>0]
coordenada_x=[a[0].x for a in escuelas_infectadas.geometry]
coordenada_y=[a[0].y for a in escuelas_infectadas.geometry]

escuelas_infectadas['lon']=coordenada_x
escuelas_infectadas['lat']=coordenada_y

#%%
'''
#Ploteo estático
#Cargamos los barrios

archivo_barrios = "barrios.geojson"
barrios = gpd.read_file(archivo_barrios)





#fig=plt.figure(figsize=(150,150))
base = barrios.plot(color='white', edgecolor='black',linewidth=0.5)


escuelas_infectadas=escuelas[escuelas['burbujas_aisladas']>0]
escuelas_infectadas.plot(ax=base,column='burbujas_aisladas', cmap='BuGn',s=30,vmax=1,vmin=0,alpha=0.5)
plt.title('Cantidad de burbujas aisladas por escuela')



escuelas_infectadas=escuelas[escuelas['positivos']>0]
escuelas_infectadas.plot(ax=base,column='positivos', cmap='RdPu',s=30,vmax=1,vmin=0,alpha=0.5)
plt.title('Cantidad de positivos por escuela')



plt.xticks([])
plt.yticks([])
plt.savefig('mapa.png')

'''
#%%
import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.io as pio

pio.renderers.default='browser'



#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)




app.layout = html.Div( children=[
    html.H1(children='Probando'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Label('Opciones'),
    
    dcc.Dropdown( id="lista",
        options=[
            {'label': 'Infectadxs', 'value': 'positivos'},
            {'label': u'Burbujas', 'value': 'burbujas_aisladas'},
            {'label': 'Escuelas cerradas', 'value': 'escuela_cerrada'}
        ],
        value='positivos'
    ),

    dcc.Graph(
        id='mapa',
        figure={}
    ),
    #html.Br(),
    #html.Div(id='output_container', children=[])
    

])

# Connect the Plotly graphs with Dash Components
@app.callback(
   [Output(component_id='mapa', component_property='figure')],
    [Input(component_id='lista', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    #container = "Escuelas por {}".format(option_slctd)

    dff = escuelas_infectadas.copy()
    dff["escuela_cerrada"]=[int(a) for a in dff["escuela_cerrada"]]
    #fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    
    fig = px.scatter_mapbox(dff, lat="lat", lon="lon", hover_name="cui", hover_data=["escuela_cerrada", "sospechosos"],
                                color_discrete_sequence=["fuchsia"], zoom=10, height=300,size=option_slctd)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    

    return ([fig])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
