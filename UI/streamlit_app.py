import requests
import streamlit as st
import time
import ntplib
from datetime import datetime
import requests


def get_ntp_time():
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    return datetime.fromtimestamp(response.tx_time)


def get_weather_forecast(api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': 'Lausanne,CH',  # Fixed to Lausanne, Switzerland
        'appid': api_key,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }
    response = requests.get(base_url, params=params)
    return response.json()


API_KEY = '8980b87bb33cc5c550a8cae48557b6af'


st.title('Live Date and Time with NTP')
'''
# Live update of time
while True:
    try:
        current_time = get_ntp_time()
        st.write(f"**Current Date and Time (NTP):** {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1)
        st.experimental_rerun()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        break
'''

forecast_data = get_weather_forecast(API_KEY)
if forecast_data.get('cod') == '200':
    st.subheader(f"Weather Forecast for Lausanne")

    # Group forecast data by date
    daily_forecasts = {}
    for entry in forecast_data['list']:
        date = datetime.fromtimestamp(entry['dt']).date()
        if date not in daily_forecasts:
            daily_forecasts[date] = []
        daily_forecasts[date].append(entry)

    # Display forecast for each day with plot
    for date, forecasts in daily_forecasts.items():
        with st.expander(f"**Date: {date.strftime('%A, %Y-%m-%d')}**"):
            times = []
            temps = []
            icons = []

            # Collect data for plotting and displaying
            for forecast in forecasts:
                time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                temp = forecast['main']['temp']
                description = forecast['weather'][0]['description'].capitalize()
                icon_url = f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"

                times.append(time)
                temps.append(temp)
                icons.append(icon_url)

            # Create columns for each forecast
            num_forecasts = len(forecasts)
            cols = st.columns(num_forecasts)

            for i, forecast in enumerate(forecasts):
                with cols[i]:
                    time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                    temp = forecast['main']['temp']
                    description = forecast['weather'][0]['description'].capitalize()
                    icon_url = f"http://openweathermap.org/img/wn/{forecast['weather'][0]['icon']}@2x.png"

                    st.write(f"{time}")
                    st.write(f"{temp}°C")
                    st.write(f"{description}")
                    st.image(icon_url, width=50)

else:
    st.error("API error. Please check the API key or try again later.")



