import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Set up the page configuration
st.set_page_config(
    page_title="Historical Data",
    page_icon="🌎",
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

def format_date(date):
    """
    Format the date from timestamp to a readable format.
    
    Parameters:
    date (int): The timestamp date.
    
    Returns:
    str: The formatted date string.
    """
    adate = date / 1000
    date_obj = datetime.utcfromtimestamp(adate)
    date = date_obj.strftime("%d-%m-%Y")
    return date

# Set the page title
st.title('Historical Data')

# Load data into session state if not already loaded
if 'all_records' not in st.session_state:
    st.session_state['all_records'] = get_data_from_flask('all_records')

# Create a DataFrame from the loaded data
df = pd.DataFrame(st.session_state['all_records'])

# Format the date column
df['date'] = df['date'].apply(format_date)

# Combine date and time into a single column
df['date_time'] = df['date'] + ' ,' + df['time']

# Subheader for indoor conditions over time
st.subheader("Indoor Conditions Over Time")

# Display metrics and plots for indoor temperature, humidity, and CO2 levels
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Average Temperature (°C)", value=round(df['indoor_temp'].mean(), 2))
    fig, ax = plt.subplots()
    ax.plot(df['date_time'], df['indoor_temp'], label='Indoor Temp (°C)', color='blue')
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    interval = len(df) // 7
    ax.set_xticks(df['date_time'][::interval])
    ax.set_xticklabels(df['date_time'][::interval], rotation=45)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.metric(label="Average Indoor Humidity (%)", value=round(df['indoor_humidity'].mean(), 2))
    fig, ax = plt.subplots()
    ax.plot(df['date_time'], df['indoor_humidity'], label='Indoor Humidity (%)', color='green')
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    interval = len(df) // 7
    ax.set_xticks(df['date_time'][::interval])
    ax.set_xticklabels(df['date_time'][::interval], rotation=45)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col3:
    st.metric(label="Average Indoor CO2 (ppm)", value=round(df['indoor_co2'].mean(), 2))
    fig, ax = plt.subplots()
    ax.plot(df['date_time'], df['indoor_co2'], label='Indoor CO2 (ppm)', color='red')
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    interval = len(df) // 7
    ax.set_xticks(df['date_time'][::interval])
    ax.set_xticklabels(df['date_time'][::interval], rotation=45)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Separator
st.markdown("***")

# Subheader for outdoor conditions over time
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.subheader("Outdoor Conditions Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(df['date_time'], df['outdoor_temp'], label='Outdoor Temp (°C)', color='orange')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Temperature (°C)')
    interval = len(df) // 7
    ax2.set_xticks(df['date_time'][::interval])
    ax2.set_xticklabels(df['date_time'][::interval], rotation=45)
    ax2.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

# Separator
st.markdown("***")

# Display the dataframe
col1, col2, col3 = st.columns([1, 7, 1])
with col2:
    st.dataframe(df)

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