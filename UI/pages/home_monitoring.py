import streamlit as st
import requests
from datetime import datetime
import json

# Set up the page configuration
st.set_page_config(
    page_title="Home Monitoring",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
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

# Load the last record into session state if not already loaded
if 'last_record' not in st.session_state:
    st.session_state['last_record'] = get_data_from_flask('last_record')

# Retrieve the last record from the session state
last_record = st.session_state['last_record']

# Extract the data from the JSON string
string_data = last_record['data']
data = json.loads(string_data)

# Convert the timestamp to a readable date format
adate = data['date']['0'] / 1000
date_obj = datetime.utcfromtimestamp(adate)

# Format the date and extract other data points
date = date_obj.strftime("%d-%m-%Y")
time = data['time']['0']
indoor_temp = data['indoor_temp']['0']
indoor_humidity = data['indoor_humidity']['0']
indoor_co2 = data['indoor_co2']['0']

# Set the page title
st.title("Indoor Conditions Monitoring")

# Separator
st.markdown("***")

# Display the time and date of the last record
st.write(f"**Recorded at:** {time} on {date}")

# Separator
st.markdown("***")

# Create columns for displaying metrics
col1, col2, col3 = st.columns(3)

# Display the indoor temperature metric
with col1:
    st.header("Indoor Temperature")
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfED-3BLG4QiOVM3kueDC9eYhUTI9aN7XM9A&s", width=70)
    st.metric(label="Temperature (°C)", value=f"{indoor_temp}°C")

# Display the indoor humidity metric
with col2:
    st.header("Indoor Humidity")
    st.image("https://cdn-icons-png.flaticon.com/512/4148/4148460.png", width=70)
    st.metric(label="Humidity (%)", value=f"{indoor_humidity}%")

# Display the indoor CO2 levels metric
with col3:
    st.header("Indoor CO2 Levels")
    st.image("https://icons.veryicon.com/png/o/education-technology/agricultural-facilities/co2.png", width=70)
    st.metric(label="CO2 (ppm)", value=f"{indoor_co2} ppm")

# Add custom CSS for styling the metrics
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

# Separator
st.markdown("***")

# Additional information about the data
st.write("Data provided by indoor monitoring system.")

# FOOTER with navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])

# Button to navigate to the Historical Data page
with col1:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('View Historical Data'):
        st.switch_page('pages/historical_data.py') 
    st.markdown("</div>", unsafe_allow_html=True)

# Button to navigate to the Forecast page
with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('View Forecast'):
        st.switch_page('pages/weather_forecast.py')
    st.markdown("</div>", unsafe_allow_html=True)

# Button to refresh the Home Monitoring page
with col3:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button('Home Monitoring'):
        st.switch_page('pages/home_monitoring.py')
    st.markdown("</div>", unsafe_allow_html=True)

# Separator
st.markdown("***")

# Link to the GitHub repository for more information
st.markdown("<div style='text-align: center;'>For more information, visit our <a href='https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024'>GitHub repository</a>.</div>", unsafe_allow_html=True)
