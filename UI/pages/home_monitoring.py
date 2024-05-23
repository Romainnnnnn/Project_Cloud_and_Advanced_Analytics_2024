import streamlit as st
import requests
from datetime import datetime

def get_data_from_flask(url_path):
    URL = "http://127.0.0.1:8080/" + url_path
    response = requests.get(URL)
    return response.json()

st.title('Home Monitoring')

forecast_data = get_data_from_flask('forecast')
current_weather = forecast_data['list'][0]
current_temp = current_weather['main']['temp']
current_desc = current_weather['weather'][0]['description']
current_humidity = current_weather['main']['humidity']
current_wind_speed = current_weather['wind']['speed']
icon_url = get_data_from_flask(f'get_icon/{current_weather["weather"][0]["icon"]}')

col1, col2 = st.columns(2)
with col1:
    st.markdown("## Live")
    col3, col4 = st.columns(2)
    with col3:
        st.image(icon_url, width=120)
    with col4:
        st.subheader(f"{round(current_temp, 1)} C°")
    col5, col6 = st.columns([1, 3])
    with col5:
        st.image("https://cdn-icons-png.flaticon.com/512/4148/4148460.png", width=70)
    with col6:
        st.markdown(f"## {current_humidity} %")
    col7, col8 = st.columns([1, 3])
    with col7:
        st.image("https://p7.hiclipart.com/preview/917/595/765/weather-forecasting-wind-computer-icons-clip-art-wind.jpg", width=70)
    with col8:
        st.markdown(f"## {current_wind_speed} %")

days = forecast_data['list'][::8]
with col2:
    st.markdown("### Forecast")
    columns = st.columns(2)
    for idx, day in enumerate(days[1:]):
        date = datetime.utcfromtimestamp(day['dt']).strftime('%A')
        temp_min = day['main']['temp_min']
        temp_max = day['main']['temp_max']
        desc = day['weather'][0]['description']
        icon_url = get_data_from_flask(f'get_icon/{day["weather"][0]["icon"]}')

        col = columns[idx % 2]
        with col:
            st.write(f"### {date}")
            st.image(icon_url, width=70)
            st.write(f"{temp_min}°C - {temp_max}°C")
