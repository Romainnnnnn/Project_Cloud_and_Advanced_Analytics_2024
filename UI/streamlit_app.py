import streamlit as st
import time
import ntplib
from datetime import datetime


def get_ntp_time():
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    return datetime.fromtimestamp(response.tx_time)


st.title('Live Date and Time with NTP')

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
