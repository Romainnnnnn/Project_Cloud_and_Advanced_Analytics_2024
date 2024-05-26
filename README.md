# Indoor Environment Monitoring with M5Stack Core2

### Overview

This project aims to monitor indoor temperature, humidity, and CO2 levels using the M5Stack Core2 IoT device. The data collected by the sensors is displayed on the device's screen and can be sent to a remote server for further analysis and monitoring.

### Features
- **Real-time Monitoring:** Continuously measures temperature, humidity, and CO2 levels.
- **Data Display:** Shows the sensor data on the M5Stack Core2's touchscreen display and on a streamlit dashboard app
- **Data Storing:** Stores the data onto a google cloud database
- **Alerts:** Set thresholds for each parameter to trigger alerts when values go out of the desired range.
- **Presence Detector:** When presence is detected the M5Stack speakers play information about today's weather using Google Text-2-Speech API
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
The local streamlit app will guide you through the final configuration steps.

### Further Implementations
- Forecast available on the m5 Stack device
- Using OpenAI to generate text for the Google Text-2-Speech API
- Better error handling in case of lost connection


### Streamlit Dashboard
You can see the dashboard [here](https://homemonitoring-q7qdvoyxja-oa.a.run.app)

### Youtube video
You can see a youtube video showcasing the project [here]()

### Contributors

- **Romain Hovius:** Backend, m5stack code
- **Youssouf Chaïb:** UI, m5stack code








