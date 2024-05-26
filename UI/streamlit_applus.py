import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time

# Page configuration
st.set_page_config(
    page_title="Home Monitoring App",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "[GitHub](https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024)"
    }
)

def get_data_from_flask(url_path):
    """
    Get data from the Flask backend server.
    
    Parameters:
    url_path (str): The path to the endpoint on the Flask server.
    
    Returns:
    dict: The JSON response from the Flask server.
    """
    URL = "https://backendproject-q7qdvoyxja-oa.a.run.app/" + url_path
    response = requests.get(URL)
    return response.json()

def display_current_time():
    """
    Display the current date and time in the Streamlit app.
    This function continuously updates the time every second.
    """
    st.markdown("<h2 style='text-align: center;'>Current Time</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        while True:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            st.markdown(f"<div style='text-align: center; font-size: 24px;'>{current_time}</div>", unsafe_allow_html=True)
            time.sleep(1)

# Page navigation setup
show_pages(
    [
        Page("streamlit_app.py", "Welcome", "🏠"),
        Page("pages/home_monitoring.py", "Home Monitoring", "🏠"),
        Page("pages/historical_data.py", "Historical Data", "🌎"),
        Page("pages/weather_forecast.py", "Forecast", "🌤️"),
    ]
)

# Centered title and welcome message
st.markdown("<h1 style='text-align: center;'>Welcome to Home Monitoring App</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'><img src='https://www.g4s.com/en-sa/-/media/g4s/saudiarabia/images/modules/newsandcontent/ess/s_home_monitoring_systems.ashx' width='300'></div>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center;'>
        <h3>Monitor your home's indoor conditions effortlessly.</h3>
        <ul style='list-style-position: inside;'>
            <li>Track temperature, humidity, and CO2 levels.</li>
            <li>Get real-time data and forecasts.</li>
            <li>Ensure a healthy living environment.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Display current time
display_current_time()

# Load data into session state
if 'last_record' not in st.session_state:
    st.session_state['last_record'] = get_data_from_flask('last_record')

if 'forecast' not in st.session_state:
    st.session_state['forecast'] = get_data_from_flask('forecast')

if 'last_record' not in st.session_state:
    st.session_state['last_record'] = get_data_from_flask('last_record')

st.markdown("***")

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
        st.experimental_set_query_params(page='historical_data')
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('View Forecast  🌤️', key='btn2'):
        st.experimental_set_query_params(page='weather_forecast')
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('Home Monitoring  🏠', key='btn3'):
        st.experimental_set_query_params(page='home_monitoring')
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("***")
st.markdown("<div style='text-align: center;'>For more information, visit our <a href='https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024'>GitHub repository</a>.</div>", unsafe_allow_html=True)
