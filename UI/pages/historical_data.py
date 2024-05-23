import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def get_data_from_flask(url_path):
    URL = "http://127.0.0.1:8080/" + url_path
    response = requests.get(URL)
    return response.json()


def format_date(date):
    adate = date / 1000
    date_obj = datetime.utcfromtimestamp(adate)
    date = date_obj.strftime("%d-%m-%Y")
    return date

st.title('Historical Data')

if 'all_records' not in st.session_state:
    st.session_state['all_records'] = get_data_from_flask('all_records')
    
df = pd.DataFrame(st.session_state['all_records'])


df['date'] = df['date'].apply(format_date)


st.subheader("Indoor Conditions Over Time")
fig, ax = plt.subplots()
ax.plot(df['time'], df['indoor_temp'], label='Indoor Temp (°C)', color='blue')
ax.plot(df['time'], df['indoor_humidity'], label='Indoor Humidity (%)', color='green')
ax.plot(df['time'], df['indoor_co2'], label='Air Quality', color='red')
ax.set_xlabel('Time')
ax.set_ylabel('Values')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.subheader("Outdoor Conditions Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(df['time'], df['outdoor_temp'], label='Outdoor Temp (°C)', color='orange')
ax2.set_xlabel('Time')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig2)
