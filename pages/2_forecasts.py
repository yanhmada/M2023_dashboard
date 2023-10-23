import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime


# PART 3

color_dict_f = {'Forecast_M_1': px.colors.qualitative.Vivid[1],
              'Forecast_M_2': px.colors.qualitative.Vivid[3],
              'Forecast_M_3': px.colors.qualitative.Vivid[6],
              'Forecast_M_4': px.colors.qualitative.Vivid[4],
              'Actual': px.colors.qualitative.Vivid[10]
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
tipo_dict_t = {'0': '11:00 AM',
               '1': '12:00 PM',
               '2': '01:00 PM',
               '3': '02:00 PM',
               '4': '03:00 PM',
               '5': '04:00 PM',
               '6': '05:00 PM',
               '7': '06:00 PM',
               '8': '07:00 PM',
               '9': '08:00 PM',
               '10': '09:00 PM',
               '11': '10:00 PM',
               '12': '11:00 PM',
              }
models_info = 'Modelo Encoder Decoder para pronóstico, con variables en Adelanto' 

training_set = 'Conjunto de entrenamiento:  2007-01-01 00:00:00 – 2022-03-12 23:00:00' 
val_set = 'Conjunto de validación:  2022-03-13 00:00:00 – 2022-04-12 23:00:00' 
test_set = 'Conjunto de prueba:   2022-04-13 00:00:00 – 2023-09-04 23:00:00'


holiday_dates =['2023-05-01','2023-04-07','2023-02-06','2023-03-20','2023-01-01','2022-12-25','2022-11-20','2022-09-16']
#date1 ='2022-09-14'
min_date = datetime.strptime("2022/09/14", "%Y/%m/%d").date()
max_date = datetime.strptime("2023/09/04", "%Y/%m/%d").date()
selectdate = datetime.strptime("2023/09/04", "%Y/%m/%d").date()
st.write("Revisión de los resultados en conjunto de Prueba")
st.write("Selecciona del conjunto de prueba 2022/09/14 a 2023/09/04")
date1 = st.date_input("Selecciona la fecha a revisar ", value = selectdate, min_value =min_date,

                       max_value=max_date, key=None, help=None, on_change=None, 
                       format="YYYY/MM/DD", disabled=False, label_visibility="visible")

Date = holiday_dates[2]
datepath = str(date1)
#tipo = str(0)          ## choose corresponding index '0': 11:00 AM, '1': 12:00 AM, ..., '12': 23:00 AM
option = st.select_slider(
    'Selecciona la hora de pronostico', options=(
    '11:00 AM' , '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM',
               '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM', '10:00 PM', '11:00 PM'),
              )
tipo = tipo_dict_1[option]
path = 'RESULTADOS_MES/' + datepath + '/forecast_all_models_' + datepath + '_[' + tipo + ']_.csv'
df = pd.read_csv(path)
All = ['Actual', 'Forecast_M_1', 'Forecast_M_2', 'Forecast_M_3', 'Forecast_M_4']
fig = go.Figure()
fig.update_layout(
    autosize=False,
    width=1200,
    height=600,
    )
for curve in All:
    fig.add_trace(go.Scatter(
    x=df['Date_time'].tolist(),
    y=df[curve].tolist(),
    line_color=color_dict_f[curve], 
    name = curve
        ))
newnames = {'Actual':'Demanda real de Gerencia', 
            'Forecast_M_1':'SV: Sin variables por adelanto', 
            'Forecast_M_2':'PC: Sólo primera componente por adelanto',
            'Forecast_M_3':'CF: Clima y festivos por adelanto',
            'Forecast_M_4':'CFD: Clima, festivos y día de la semana por adelanto'
           }
fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

fig.update_layout(
    title= models_info + '<br>' 
           + 'Hora de cálculo de pronóstico ' + tipo_dict_t[tipo] + '<br>',
        #   + '<sub>' + training_set + '<br>' + '</sub>'
        #   + '<sub>' + test_set + '<br>' + '</sub>',
    legend_title='Variantes:',
    font=dict(
        size=10,
        color='gray'
    ))
fig.update_layout(
    title={
        'y':0.97,
        'xanchor': 'left',
        'yanchor': 'top'})
st.plotly_chart(fig)