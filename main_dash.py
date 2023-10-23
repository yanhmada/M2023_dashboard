# dashboard.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

st.title ("Reporte técnico complementario  de metodología para pronóstico de demanda de \
          energía a corto plazo")
st.subheader("")

# Streamlit App

df_GCRNO_complete = pd.read_csv('./GCRNO_complete_silver_2023-10-03.csv' , parse_dates=True)
df_GCRNO_complete['Date_time'] =  pd.to_datetime(df_GCRNO_complete['Date_time'],format="%Y-%m-%d %H:%M:%S")
df_GCRNO_complete['Year'] = df_GCRNO_complete['Date_time'].dt.year
#"%Y-%m-%d %H:%M:%S"
df_GCRNO_complete.set_index("Date_time", inplace=True)
df_GCRNO_complete = df_GCRNO_complete.asfreq('h')


x = df_GCRNO_complete['Hour']
y = df_GCRNO_complete['Energy_Demand']

fig = px.box(df_GCRNO_complete, x, y, color=x)

fig.update_layout(title_text="Demanda de Energia por Hora", height=1000)
fig.update(layout_showlegend=False)

# Display the figure in Streamlit
st.write("Highlights de datos origen")

st.plotly_chart(fig)
#chart 3
day_labels = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

filtered_df = df_GCRNO_complete[(df_GCRNO_complete['Year'] >= 2018) & (df_GCRNO_complete['Year'] <= 2023)]

fig = px.box(filtered_df, x='Day', y='Energy_Demand',  points='outliers',
                color='Day',
                category_orders={'DayOfWeek': [0, 1, 2, 3, 4, 5, 6]},
                labels={'Day': 'Day of the Week'},
                title='Energy Demand by Day of the Week')
fig.update_xaxes(type='category', tickmode='array', tickvals=[0, 1, 2, 3, 4, 5, 6],
                 ticktext=[day_labels[day] for day in range(7)])
st.plotly_chart(fig)
# Month chart

month_labels = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
                8:'August', 9:'September', 10:'October',11:'November',12:'December'}

filtered_df = df_GCRNO_complete[(df_GCRNO_complete['Year'] >= 2015) & (df_GCRNO_complete['Year'] <= 2022)]

fig = px.box(filtered_df, x='Month', y='Energy_Demand',  points='outliers',
                color='Month',
                category_orders={'Month': [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10, 11,12]},
                labels={'Month': 'Month'},
                title='Energy Demand by Month')
fig.update_xaxes(type='category', tickmode='array', tickvals=[1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11,12],
                 ticktext=[month_labels[Month] for Month in range(1,13  )])
st.plotly_chart(fig)
# PART 3

color_dict_f = {'Forecast_M_1': px.colors.qualitative.Vivid[1],
              'Forecast_M_2': px.colors.qualitative.Vivid[3],
              'Forecast_M_3': px.colors.qualitative.Vivid[6],
              'Forecast_M_4': px.colors.qualitative.Vivid[4],
              'Actual': px.colors.qualitative.Vivid[10]
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

training_set = 'Conjunto de entrenamiento:  2007-01-01 00:00:00 – 2022-02-05 23:00:00' 
val_set = 'Conjunto de validación:  2022-02-06 00:00:00 – 2022-06-05 23:00:00' 
test_set = 'Conjunto de prueba:   2022-06-06 00:00:00 – 2023-06-05 23:00:00'
holiday_dates =['2023-05-01','2023-04-07','2023-02-06','2023-03-20','2023-01-01','2022-12-25','2022-11-20','2022-09-16']
#date1 ='2022-09-14'
min_date = datetime.strptime("2022/09/14", "%Y/%m/%d").date()
max_date = datetime.strptime("2023/09/04", "%Y/%m/%d").date()
selectdate = datetime.strptime("2023/09/04", "%Y/%m/%d").date()
st.write("Revisión de los resultados en conjunto de Prueba")
st.write(test_set)
date1 = st.date_input("Selecciona la fecha a revisar ", value = selectdate, min_value =min_date,

                       max_value=max_date, key=None, help=None, on_change=None, 
                       format="YYYY/MM/DD", disabled=False, label_visibility="visible")
#date1 = st.date_input("Selecciona la fecha a revisar",min_value="2022-09-14",
#                       max_value="2023-09-04", key=None, help=None, on_change=None, 
#                       format="YYYY/MM/DD", disabled=False, label_visibility="visible")

#
Date = holiday_dates[2]
datepath = str(date1)
tipo = str(0)          ## choose corresponding index '0': 11:00 AM, '1': 12:00 AM, ..., '12': 23:00 AM
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
           + 'Hora de cálculo de pronóstico ' + tipo_dict_t[tipo] + '<br>'
           + '<sub>' + training_set + '<br>' + '</sub>'
           + '<sub>' + test_set + '<br>' + '</sub>',
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