import streamlit as st
import requests
from datetime import datetime
import json

def get_data_from_flask(url_path):
    URL = "http://127.0.0.1:8080/" + url_path
    response = requests.get(URL)
    return response.json()

last_record = get_data_from_flask('last_record')

string_data = last_record['data']
data = json.loads(string_data)


adate = data['date']['0'] / 1000
date_obj = datetime.utcfromtimestamp(adate)

date = date_obj.strftime("%d-%m-%Y")
time = data['time']['0']
indoor_temp = data['indoor_temp']['0']
indoor_humidity = data['indoor_humidity']['0']
indoor_co2 = data['indoor_co2']['0']

st.title("Indoor Conditions Monitoring")

st.header("Date and Time")
st.write(f"**Date:** {date}")
st.write(f"**Time:** {time}")

st.header("Indoor Temperature")
st.metric(label="Temperature (°C)", value=f"{indoor_temp}°C")

st.header("Indoor Humidity")
st.metric(label="Humidity (%)", value=f"{indoor_humidity}%")

st.header("Indoor CO2 Levels")
st.metric(label="CO2 (ppm)", value=f"{indoor_co2} ppm")

st.markdown("""
    <style>
    .stMetric { 
        text-align: center; 
        font-size: 24px; 
        font-weight: bold; 
    }
    .stHeader, .stTitle { 
        text-align: center; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("***")
st.write("Data provided by indoor monitoring system.")
