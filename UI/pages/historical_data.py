import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_data_from_flask(url_path):
    URL = "http://127.0.0.1:8080/" + url_path
    response = requests.get(URL)
    return response.json()

st.title('Historical Data')

data = get_data_from_flask('historical_data')
df = pd.DataFrame(data)

st.subheader("Indoor Conditions Over Time")
fig, ax = plt.subplots()
ax.plot(pd.to_datetime(df['timestamp']), df['indoor_temp'], label='Indoor Temp (°C)', color='blue')
ax.plot(pd.to_datetime(df['timestamp']), df['indoor_humidity'], label='Indoor Humidity (%)', color='green')
ax.plot(pd.to_datetime(df['timestamp']), df['air_quality'], label='Air Quality', color='red')
ax.set_xlabel('Time')
ax.set_ylabel('Values')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

st.subheader("Outdoor Conditions Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(pd.to_datetime(df['timestamp']), df['outdoor_temp'], label='Outdoor Temp (°C)', color='orange')
ax2.set_xlabel('Time')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig2)
