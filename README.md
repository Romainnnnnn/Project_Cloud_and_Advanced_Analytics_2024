# Indoor Environment Monitoring with M5Stack Core2

### Overview

This project aims to monitor indoor temperature, humidity, and CO2 levels using the M5Stack Core2 IoT device. The data collected by the sensors is displayed on the device's screen and can be sent to a remote server for further analysis and monitoring.

### Features
- **Real-time Monitoring:** Continuously measures temperature, humidity, and CO2 levels.
- **Data Display:** Shows the sensor data on the M5Stack Core2's touchscreen display and on a streamlit dashboard app
- **Data Storing:** Stores the data onto a google cloud database
- **Alerts:** Set thresholds for each parameter to trigger alerts when values go out of the desired range.
- **Presence Detector:** When presence is detected the M5Stack speakers play information about today's weather
- **Forecast:** Weather forecast available on the streamlit dashboard app.
- **Historical Data Analysis:** Diplay of historical data on the streamlit dashboard app

### Requirements
- M5Stack Core2 IoT device
- Humidity sensor
- Temperature sensor
- CO2 sensor

### SetUp Instructions
1. Open a terminal window and run the following command
```
git clone https://github.com/Romainnnnnn/Project_Cloud_and_Advanced_Analytics_2024/
```
2. Navigate to the project directory:
```
cd Project_Cloud_and_Advanced_Analytics_2024
```
3. Set Up a Python Virtual Environment:
```
python -m venv venv
```
4. Activate the virtual environment:
- On windows ```venv\Scripts\activate```
- On MacOs and Linux ```source venv/bin/activate```


5. Install the Required Libraries:
```
pip install -r requirements.txt
```
6. Run the following command:
```
cd Tutorial
```
```
streamlit run tuto.py
```









