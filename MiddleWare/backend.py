from flask import Flask, request, jsonify
from google.cloud import bigquery
import os
from google.cloud.exceptions import GoogleCloudError
import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv('PROJECT_NAME')
key_path = os.getenv('KEY_PATH')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

client = bigquery.Client(project=PROJECT_NAME)
API_KEY = os.getenv('API_KEY')
LOCATION = os.getenv('LOCATION') # 'Lausanne,CH'

def get_weather_forecast(api_key, location):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

app = Flask(__name__)


@app.route('/')
def index():
    endpoints = '''
    <h1>Endpoints</h1>
    <ul>
        <li>/post/&lt;date&gt;/&lt;time&gt;/&lt;indoor_temp&gt;/&lt;indoor_humidity&gt;/&lt;outdoor_temp&gt;/&lt;outdoor_humidity&gt;/&lt;outdoor_wheather&gt;/&lt;outdoor_windspeed&gt;/&lt;detector_status&gt;/&lt;indoor_co2&gt;</li>
        <li>/forecast</li>
        <li>/outdoor_temp</li>
        <li>/outdoor_humidity</li>
        <li>/outdoor_windspeed</li>
        <li>/outdoor_weather</li>
        <li>/last_record</li>
        <li>/time</li>
        <li>/date</li>
    </ul>
    '''
    return endpoints


@app.route('/post/<date>/<time>/<indoor_temp>/<indoor_humidity>/<outdoor_temp>/<outdoor_humidity>/<outdoor_wheather>/<outdoor_windspeed>/<detector_status>/<indoor_co2>')
def post(date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_wheather, outdoor_windspeed, detector_status, indoor_co2):
    try:
        print("Received data")
        # Convert data types as needed
        indoor_temp = float(indoor_temp)
        indoor_humidity = float(indoor_humidity)
        outdoor_temp = float(outdoor_temp)
        outdoor_humidity = float(outdoor_humidity)
        outdoor_windspeed = float(outdoor_windspeed)
        indoor_co2 = float(indoor_co2)

        query = f"""
            INSERT INTO `{PROJECT_NAME}.WheatherData.weather-records` 
            (date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_wheather, outdoor_windspeed, detector_status, indoor_co2)
            VALUES('{date}', '{time}', {indoor_temp}, {indoor_humidity}, {outdoor_temp}, {outdoor_humidity}, '{outdoor_wheather}', {outdoor_windspeed}, '{detector_status}', {indoor_co2})
        """
        query_job = client.query(query)
        query_job.result()

        return jsonify('Data added successfully'), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

@app.route('/forecast')
def forecast():
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    return jsonify(forecast_data)

@app.route('/outdoor_temp')
def outdoor_temp():
    print("got request")
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    current_weather = forecast_data['list'][0]
    current_temp = current_weather['main']['temp']
    return jsonify(current_temp)

@app.route('/outdoor_humidity')
def outdoor_humidity():
    print("got request")
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    current_weather = forecast_data['list'][0]
    current_humidity = current_weather['main']['humidity']
    return jsonify(current_humidity)

@app.route('/outdoor_windspeed')
def outdoor_windspeed():
    print("got request")
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    current_weather = forecast_data['list'][0]
    current_wind_speed = current_weather['wind']['speed']
    return jsonify(current_wind_speed)

@app.route('/outdoor_weather') 
def outdoor_weather():
    print("got request")
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    current_weather = forecast_data['list'][0]
    current_weather = current_weather['weather'][0]['description']
    return jsonify(current_weather)                           

@app.route('/get_icon/<forecast>')
def get_icon(forecast):
    base_url = "https://openweathermap.org/img/wn"
    icon_url = f"{forecast}"
    end_url = '@2x.png'
    print(f"{base_url}/{icon_url}{end_url}")
    return jsonify(f"{base_url}/{icon_url}{end_url}")

    

@app.route('/time')
def time_date():
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return jsonify(current_time)

@app.route('/date')
def date(): 
    from datetime import datetime
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    return jsonify(current_date)

@app.route('/last_record')
def last_record():
    try:
        query = f"""
                SELECT *
                FROM `{PROJECT_NAME}.WheatherData.weather-records`
                ORDER BY date DESC, time DESC
                LIMIT 1
                """
        query_job = client.query(query)
        results = query_job.to_dataframe()
        return jsonify({
            "status": "success",
            "data": results.to_json()
        }), 200
    except GoogleCloudError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
