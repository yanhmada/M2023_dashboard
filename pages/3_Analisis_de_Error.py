#import libraries
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

models_info = 'MODELO ENCODER-DECODER CON VARIABLES EN ADELANTO' 

df_compute_11_AM = pd.read_csv("RESULTADOS_MAPE_HORA/Mape_[0].csv")

color_dict = {'Mape_M_1': px.colors.qualitative.Vivid[1],
              'Mape_M_2': px.colors.qualitative.Vivid[3],
              'Mape_M_3': px.colors.qualitative.Vivid[6],
              'Mape_M_4': px.colors.qualitative.Vivid[4],
              }
# Plot by season. Example for forecast computed at 11:00 AM 
color_dict_e = {'Invierno': px.colors.qualitative.Pastel2[2],
               'Primavera': px.colors.qualitative.Pastel2[4],
               'Verano': px.colors.qualitative.Pastel2[5],
               'Otoño': px.colors.qualitative.Pastel2[6],
               }
df_compute_11_AM['Date'] = pd.to_datetime(df_compute_11_AM['Date']) #
df = df_compute_11_AM
df['Season'] = (df['Date'].dt.month%12 + 3)//3
seasons = {
             1: 'Invierno',
             2: 'Primavera',
             3: 'Verano',
             4: 'Otoño'
}
df['Season_name'] = df['Season'].map(seasons)
Mape_Models = ['Mape_M_1', 'Mape_M_2', 'Mape_M_3', 'Mape_M_4']

Estaciones = ['Invierno','Primavera','Verano','Otoño']
fig = go.Figure()
fig.update_layout(
    autosize=False,
    width=1000,
    height=1400,
    yaxis=dict(
        title_text='Estaciones del año',
        ticktext=['Invierno','Primavera','Verano','Otoño'],
        tickvals=[2,6,10,14],
        tickmode="array",
        titlefont=dict(size=20),
    ))
for estacion in Estaciones:
    for mape in Mape_Models:
        fig.add_trace(go.Violin(
        x=df[mape][ df['Season_name'] == estacion ].tolist(),
        legendgroup=mape, scalegroup=mape, 
        name= mape + estacion,
        marker_color=color_dict[mape],
        line_color=color_dict[mape], 
        fillcolor=color_dict_e[estacion],
        points='outliers',
        box_visible=True, 
      #  showlegend=False,
        visible=True, 
        opacity=0.7
        ))
newnames = {'Mape_M_1Invierno':'SV ❄', 
            'Mape_M_2Invierno':'PC ❄',
            'Mape_M_3Invierno':'CF ❄',
            'Mape_M_4Invierno':'CFD ❄',
            'Mape_M_5Invierno':'CFT ❄',
            'Mape_M_1Primavera':'SV ❀', 
            'Mape_M_2Primavera':'PC ❀',
            'Mape_M_3Primavera':'CF ❀',
            'Mape_M_4Primavera':'CFD ❀',
            'Mape_M_5Primavera':'CFT ❀',
            'Mape_M_1Verano':'SV ☼', 
            'Mape_M_2Verano':'PC ☼',
            'Mape_M_3Verano':'CF ☼',
            'Mape_M_4Verano':'CFD ☼',
            'Mape_M_5Verano':'CFT ☼',
            'Mape_M_1Otoño':'SV 𖥸', 
            'Mape_M_2Otoño':'PC 𖥸',
            'Mape_M_3Otoño':'CF 𖥸',
            'Mape_M_4Otoño':'CFD 𖥸',
            'Mape_M_5Otoño':'CFT 𖥸'

           }
fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
fig.update_layout(xaxis=dict(title='MAPE (24 h)', zeroline=False),boxmode='group')
fig.update_traces(orientation='h', side='positive', width=4) # horizontal box plots 
fig.update_layout(
        title= models_info + '<br>' 
        'Hora de cálculo de pronóstico: 11:00 AM' + '<br>'
        + '<sub>' + "Cálculo de Mape por Estación "+ '<br>' + '</sub>',
        legend_title='Variantes',
        font=dict(
            size=13,
            color='gray'))
fig.update_layout(
    title={
        'y':0.99,
        'xanchor': 'left',
        'yanchor': 'top'})
fig.show()

st.plotly_chart(fig)