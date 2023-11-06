#import libraries
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Streamlit App
st.markdown("<h1 style='color: gray;'> CONVENIO CENACE 2023-2025 </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: orange;'> Desarrollo de prototipo: metodología \
            con aprendizaje profundo para el pronóstico a corto plazo de demanda \
            de energía con datos en adelanto.</h2>", unsafe_allow_html=True)

st.caption('''
           En esta sección se incluyen los comparativos de  _MAPE_  en base a la hora que se\
           realizó el pronóstico. Se muestran primero las gráficas por estación, y por mes seleccionado.
           
           ''')

st.title ("Análisis de MAPE para pronósticos")


#Declare variables
models_info = 'MODELO ENCODER-DECODER CON VARIABLES EN ADELANTO' 

color_dict = {'Mape_M_1': px.colors.qualitative.Vivid[1],
              'Mape_M_2': px.colors.qualitative.Vivid[3],
              'Mape_M_3': px.colors.qualitative.Vivid[6],
              'Mape_M_4': px.colors.qualitative.Vivid[4],
              }
tipo_dict_1 = {'11:00 AM':'0',
               '12:00 PM':'1',
               '01:00 PM':'2',
               '02:00 PM':'3',
               '03:00 PM':'4',
               '04:00 PM':'5',
               '05:00 PM':'6',
               '06:00 PM':'7',
               '07:00 PM':'8',
               '08:00 PM':'9',
               '09:00 PM':'10',
               '10:00 PM':'11',
               '11:00 PM':'12',
              }
color_dict_e = {'Invierno': px.colors.qualitative.Pastel2[2],
               'Primavera': px.colors.qualitative.Pastel2[4],
               'Verano': px.colors.qualitative.Pastel2[5],
               'Otoño': px.colors.qualitative.Pastel2[6],
               }

option = st.select_slider(
        'Selecciona la hora de pronóstico', options=(
        '11:00 AM' , '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM',
        '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM'),
        )
tipo = tipo_dict_1[option]

df_compute = pd.read_csv("RESULTADOS_MAPE_HORA/Mape_["+tipo+"].csv")

st.write(f' Hora de cálculo de pronóstico {option}')

st.subheader("MAPE por estación")
# Plot by season
df_compute['Date'] = pd.to_datetime(df_compute['Date']) #
df = df_compute
df['Season'] = (df['Date'].dt.month%12 + 3)//3

seasons = {
             1: 'Invierno',
             2: 'Primavera',
             3: 'Verano',
             4: 'Otoño'}

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
        + '<sub>' + "Cálculo de MAPE por estación "+ '<br>' + '</sub>',
        legend_title='Variantes',
        font=dict(
            size=13,
            color='gray'))
fig.update_layout(
    title={
        'y':0.99,
        'xanchor': 'left',
        'yanchor': 'top'})

st.plotly_chart(fig)
st.subheader(' Gráfica de MAPE por mes ')
st.divider()

#MONTHLY
mes = st.select_slider(
    'Selecciona mes para pronóstico', options=(
    'Enero' , 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
               'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'),
              )

st.markdown(f"Se muestran resultados de {mes} ")

map_mes= {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
    }
df_compute['Date'] = pd.to_datetime(df_compute['Date']) #
df = df_compute
df['Month'] = (df['Date'].dt.month)
fig2 = go.Figure()

mes_sel =map_mes[mes] # month selection
Mape_Models = ['Mape_M_1', 'Mape_M_2', 'Mape_M_3', 'Mape_M_4']
fig2 = go.Figure()
newnames2 = { 
            'Mape_M_1':'SV: Sin variables por adelanto', 
            'Mape_M_2':'PC: Sólo primera componente por adelanto',
            'Mape_M_3':'CF: Clima y festivos por adelanto',
            'Mape_M_4':'CFD: Clima, festivos y día de la semana por adelanto'
           }

for mape in Mape_Models:
    fig2.add_trace(go.Violin(
    x=df[mape][df['Month'] == mes_sel].tolist(),
        legendgroup=mape, 
        scalegroup=mape, 
        name=mape ,  
        marker_color=color_dict[mape],
        line_color=color_dict[mape], 
        points='outliers',
        box_visible=True, 
        # showlegend=False,
        visible=True, 
        opacity=0.7
    ))

fig2.for_each_trace(lambda t: t.update(name=newnames2.get(t.name, t.name)))
fig2.update_layout(xaxis=dict(title='MAPE para pronóstico', zeroline=False),boxmode='group')
fig2.update_traces(orientation='h', side='positive', width=4) # horizontal orientation 
fig2.update_layout(
        title= models_info + '<br>' 
        + '<sub>' + "Cálculo de Mape por Mes  "+ '<br>' + '</sub>',
        legend_title='Variantes',
        font=dict(
            size=15,
            color='gray'),
        legend=dict(
            x=1,
            y=1,
            xanchor='right',
            yanchor='top'
        )
            )
fig2.update_layout(
    title={
        'y':0,
        'xanchor': 'left',
        'yanchor': 'top'})
    
fig2.update_layout(
    autosize=False,
    width=1200,
    height=600,
    yaxis=dict(
        title_text='Modelos',
        ticktext=['Modelo M1','Modelo M2','Modelo M3','Modelo M4'],
        tickmode="array",
        titlefont=dict(size=10),
    ))

st.plotly_chart(fig2)