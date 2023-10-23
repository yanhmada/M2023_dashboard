import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime


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
