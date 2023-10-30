import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Header

st.markdown("<h1 style='color: gray;'> CONVENIO CENACE 2023-2025 </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: orange;'> Diseño  e  implementación de una metodología para pronóstico de demanda de energía \
            a corto plazo con manejo de datos bajo incertidumbre  </h2>", unsafe_allow_html=True)

st.caption('''
           En esta sección se incluyen puntos importantes del EDA realizado sobre los datos fuente.\
           
           ''')

st.caption('''
    Del conjunto de datos tomado de Cenace~ Conagua, archivo fuente en formato yyy-mm-dd hh:00:00, desde\
    2007-01-01 a 2023-09-05.  Contiene 24 variables de demanda de energía, datos reales-medidos  de la \
    demanda de carga de energía eléctrica en la Zona de Gerencia del  Noroeste por cada hora del día \
    compuesta por zonas de carga, a saber, Caborca, Nogales, Hermosillo, Guaymas, Cd. Obregón, Navojoa, \
    Los Mochis, Guasave, Culiacán y Mazatlán, cargas fuera del consumo de las zonas de carga descritas \
    anteriormente,  el consumo de las centrales y las pérdidas de energía que existen en la red.
    10 variables de calendario: lunes festivo, lunes después de festivo, Semana Santa, 1 de mayo, 10 de mayo, \
    16 de septiembre, 2 de noviembre, día antes de Navidad o Año Nuevo, Navidad o Año Nuevo, \
    día después de Navidad o Año Nuevo.
    Fuente Comisión Nacional del Agua (CONAGUA):
    Fecha en formato yyyy-mm-dd, desde 2007-01-01 a 2023-01-18. 14  variables meteorológicas\
           C and mm/h), datos reales-medidos de la  temperatura máxima y mínima diaria en Caborca, \
           Hermosillo, Ciudad Obregón, Los Mochis y Culiacán. Precipitación diaria en Hermosillo, \
           Ciudad Obregón, Los Mochis y Culiacán.           
           ''')


st.title ("Análisis Exploratorio de Datos")

df_GCRNO_complete = pd.read_csv('./GCRNO_complete_silver_2023-10-03.csv' , parse_dates=True)
df_GCRNO_complete['Date_time'] =  pd.to_datetime(df_GCRNO_complete['Date_time'],format="%Y-%m-%d %H:%M:%S")
df_GCRNO_complete['Year'] = df_GCRNO_complete['Date_time'].dt.year
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

#chart 2 Month
# Month chart

month_labels = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                8:'Agosto', 9:'Septiembre', 10:'Octubre',11:'Noviembre',12:'Diciembre'}

filtered_df = df_GCRNO_complete[(df_GCRNO_complete['Year'] >= 2015) & (df_GCRNO_complete['Year'] <= 2022)]

fig = px.box(filtered_df, x='Month', y='Energy_Demand',  points='outliers',
                color='Month',
                category_orders={'Month': [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ,10, 11,12]},
                labels={'Month': 'Mes'},
                title='Demanda de energía por Mes')
fig.update_xaxes(type='category', tickmode='array', tickvals=[1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11,12],
                 ticktext=[month_labels[Month] for Month in range(1,13  )])
st.plotly_chart(fig)

#chart 3
day_labels = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}
filtered_df = df_GCRNO_complete[(df_GCRNO_complete['Year'] >= 2018) & (df_GCRNO_complete['Year'] <= 2023)]

fig = px.box(filtered_df, x='Day', y='Energy_Demand',  points='outliers',
                color='Day',
                category_orders={'DayOfWeek': [0, 1, 2, 3, 4, 5, 6]},
                labels={'Day': 'Día de la semana'},
                title='Demanda de Energía por día de la semana')
fig.update_xaxes(type='category', tickmode='array', tickvals=[0, 1, 2, 3, 4, 5, 6],
                 ticktext=[day_labels[day] for day in range(7)])
st.plotly_chart(fig)
