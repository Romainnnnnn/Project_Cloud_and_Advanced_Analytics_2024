import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_data_from_flask(url_path):
    URL = "http://127.0.0.1:8080/" + url_path
    response = requests.get(URL)
    return response.json()

st.title('Detailed Weather Forecast')

forecast_data = get_data_from_flask('forecast')

if st.button('Show More Detailed Weather Forecast'):
    if forecast_data.get('cod') == '200':
        st.subheader(f"Weather Forecast for Lausanne")

        daily_forecasts = {}
        for entry in forecast_data['list']:
            date = datetime.fromtimestamp(entry['dt']).date()
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(entry)

        all_temps = []
        all_dates = []
        for date, forecasts in daily_forecasts.items():
            with st.expander(f"**Date: {date.strftime('%A, %Y-%m-%d')}**"):
                times = []
                temps = []
                icons = []
                num_forecasts = len(forecasts)
                cols = st.columns(num_forecasts)
                for i, forecast in enumerate(forecasts):
                    with cols[i]:
                        time = datetime.fromtimestamp(forecast['dt'])
                        temp = forecast['main']['temp']
                        description = forecast['weather'][0]['description'].capitalize()
                        icon_url = get_data_from_flask(f'get_icon/{forecast["weather"][0]["icon"]}')

                        times.append(time)
                        temps.append(temp)
                        icons.append(icon_url)
                        all_dates.append(time)
                        all_temps.append(temp)

                        st.write(f"**Time:** {time.strftime('%H:%M')}")
                        st.write(f"**Temp:** {temp}°C")
                        st.write(f"**Weather:** {description}")

                        st.image(icon_url, width=70)

                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(times, temps, marker='o', linestyle='-', color='blue', alpha=0.6, markerfacecolor='red')
                ax.set_xlabel('Time')
                ax.set_ylabel('Temperature (°C)')
                ax.set_title(f'Temperature Variation on {date.strftime("%A, %Y-%m-%d")}')
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                plt.xticks(rotation=45)
                plt.tight_layout()

                st.pyplot(fig)

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(all_dates, all_temps, linestyle='-', color='blue', alpha=0.6, markerfacecolor='red')
        ax2.set_ylabel('Temperature (°C)')
        ax2.set_title('Temperature Variation')
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%A'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig2)
    else:
        st.error("API error. Please check the API key or try again later.")

