import streamlit as st
import requests
from datetime import datetime, time, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set up the page configuration
st.set_page_config(
    page_title="Forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "[GitHub](https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024)"
    }
)

def get_data_from_flask(url_path):
    URL = "https://backendproject-q7qdvoyxja-oa.a.run.app/" + url_path
    response = requests.get(URL)
    return response.json()

def get_noon_forecast(forecasts):
    target_time = time(12, 0)
    closest_forecast = min(forecasts, key=lambda x: abs((datetime.fromtimestamp(x['dt']).time().hour * 60 + datetime.fromtimestamp(x['dt']).time().minute) - (target_time.hour * 60 + target_time.minute)))
    return closest_forecast

# Set the page title
st.title('Detailed Weather Forecast')

# Load forecast data into session state if not already loaded
if 'forecast' not in st.session_state:
    st.session_state['forecast'] = get_data_from_flask('forecast') 

# Check if forecast data is valid
if st.session_state['forecast'].get('cod') == '200':
    st.subheader(f"Weather Forecast for {st.session_state['forecast']['city']['name']}")

    # Organize the forecast data by date
    daily_forecasts = {}
    for entry in st.session_state['forecast']['list']:
        date = datetime.fromtimestamp(entry['dt']).date()
        if date not in daily_forecasts:
            daily_forecasts[date] = []
        daily_forecasts[date].append(entry)
    
    # Display the header with weather icons and titles
    col_count = 0
    cols = st.columns(6)
    for date, forecasts in list(daily_forecasts.items())[:6]:
        forecast = get_noon_forecast(forecasts)
        icon_url = get_data_from_flask(f'get_icon/{forecast["weather"][0]["icon"]}')
        day_title = date.strftime('%A')

        with cols[col_count]:
            st.image(icon_url, width=50)
            st.write(f"**{day_title}**")
        
        col_count += 1

    st.markdown("***")

    all_temps = []
    all_dates = []
    # Display the forecast for each day
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

            # Plot the temperature variation throughout the day
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(times, temps, marker='o', linestyle='-', color='blue', alpha=0.6, markerfacecolor='red')
            ax.set_xlabel('Time')
            ax.set_ylabel('Temperature (°C)')
            ax.set_title(f'Temperature Variation on {date.strftime("%A, %Y-%m-%d")}')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)

    # Plot the overall temperature variation for all dates
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

# Footer with improved buttons
st.markdown("""
    <style>
    .nav-button {
        display: inline-block;
        padding: 10px 20px;
        margin: 10px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        color: white;
        background-color: #007BFF;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .nav-button:hover {
        background-color: #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('View Historical Data  🌎', key='btn1'):
        st.switch_page('pages/historical_data.py')
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('View Forecast  🌤️', key='btn2'):
        st.switch_page('pages/weather_forecast.py')
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('Home Monitoring  🏠', key='btn3'):
        st.switch_page('pages/home_monitoring.py')
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("***")
st.markdown("<div style='text-align: center;'>For more information, visit our <a href='https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024'>GitHub repository</a>.</div>", unsafe_allow_html=True)
