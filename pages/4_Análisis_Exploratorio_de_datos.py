import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Header

st.markdown("<h1 style='color: gray;'> CONVENIO CENACE-UNISON </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: orange;'> Desarrollo de prototipo: metodología \
            con aprendizaje profundo para el pronóstico a corto plazo de demanda \
            de energía con datos en adelanto.</h2>", unsafe_allow_html=True)
st.caption('''
           En esta sección se incluyen puntos importantes del EDA realizado sobre los datos fuente.\
           
           ''')

st.caption('''
    Del conjunto de datos tomado de Cenace~ Conagua, archivo fuente en formato yyy-mm-dd hh:00:00, desde\
    2007-01-01 a 2023-09-05.  Contiene variables de energía y de calendario, así como 14  variables meteorológicas\
        de  temperatura máxima y mínima diaria de las ciudades de la zona de carga, que incluye  Caborca, \
           Hermosillo, Ciudad Obregón, Los Mochis y Culiacán. Precipitación diaria en Hermosillo, \
           Ciudad Obregón, Los Mochis y Culiacán.           
           ''')


st.title ("Análisis exploratorio de datos")
#hourly  chart 
df_GCRNO_complete = pd.read_csv('./GCRNO_complete_silver_2023-10-03.csv' , parse_dates=True)
df_GCRNO_complete['Date_time'] =  pd.to_datetime(df_GCRNO_complete['Date_time'],format="%Y-%m-%d %H:%M:%S")
df_GCRNO_complete['Year'] = df_GCRNO_complete['Date_time'].dt.year
df_GCRNO_complete.set_index("Date_time", inplace=True)
df_GCRNO_complete = df_GCRNO_complete.asfreq('h')

x = df_GCRNO_complete['Hour']
y = df_GCRNO_complete['Energy_Demand']

fig = px.box(df_GCRNO_complete, x, y, 
            color=x,
            color_discrete_sequence=px.colors.qualitative.Vivid
            )

fig.update_layout(title_text="Demanda de energia por hora", height=1000)
fig.update(layout_showlegend=False)

# Display the figure in Streamlit
st.write("Highlights de datos origen")
st.plotly_chart(fig)

#chart 2 Month
month_labels = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio',
                8:'Agosto', 9:'Septiembre', 10:'Octubre',11:'Noviembre',12:'Diciembre'}

filtered_df = df_GCRNO_complete[(df_GCRNO_complete['Year'] >= 2015) & (df_GCRNO_complete['Year'] <= 2022)]

boxes = []

for month in range(1, 13):
    month_data = filtered_df[filtered_df['Month'] == month]
    box = go.Box(
        x=month_data['Month'],
        y=month_data['Energy_Demand'],
        name=month_labels[month],  
        marker=dict(
            color=px.colors.qualitative.Vivid[month % len(px.colors.qualitative.Vivid)],  
            opacity=0.7
        ),
        boxpoints='outliers',
        jitter=0.3,  
        pointpos=-1.8  # Position of the outliers
    )
    boxes.append(box)

# Create figure and add the box traces
fig = go.Figure(data=boxes)

# Update layout
fig.update_layout(
    xaxis=dict(
        type='category', 
        tickmode='array', 
        tickvals=list(range(1, 13)),
        ticktext=[month_labels[Month] for Month in range(1, 13)]
    ),
    yaxis=dict(title='Energy_Demand'),
    title='Demanda de energía por mes'
)

st.plotly_chart(fig)

#chart 3
day_labels = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'}

filtered_df = df_GCRNO_complete[(df_GCRNO_complete['Year'] >= 2018) & (df_GCRNO_complete['Year'] <= 2023)]

boxes = []

for day in range(7):
    day_data = filtered_df[filtered_df['Day'] == day]
    box = go.Box(
        x=day_data['Day'],
        y=day_data['Energy_Demand'],
        name=day_labels[day],  # Using day_labels dictionary
        marker=dict(
            color=px.colors.qualitative.Vivid[day % len(px.colors.qualitative.Vivid)],  
            opacity=0.7
        ),
        boxpoints='outliers',
        jitter=0.3,  
        pointpos=-1.8  # Position of the outliers
    )
    boxes.append(box)


fig = go.Figure(data=boxes)

fig.update_layout(
    xaxis=dict(
        type='category', 
        tickmode='array', 
        tickvals=list(range(7)),
        ticktext=[day_labels[day] for day in range(7)]
    ),
    yaxis=dict(title='Energy_Demand'),
    title='Demanda de energía por día de la semana'
)

st.plotly_chart(fig)
