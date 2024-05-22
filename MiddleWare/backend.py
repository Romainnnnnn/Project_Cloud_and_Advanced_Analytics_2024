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
    <html>
    <head>
        <style>
            .endpoint {
                font-family: Arial, sans-serif;
                font-size: 16px;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="endpoint">Available endpoints:</div>
        <ul>
            <li><a href="/movie_title">/movie_title</a></li>
        </ul>
    </body>
    </html>
    '''
    return endpoints



@app.route('/dates')
def get_dates():
    try:
        query = f"""
                SELECT *
                FROM `{PROJECT_NAME}.WheatherData.weather-records`
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

# http://127.0.0.1:8080/post/2024-04-20/16:02:23/25/25/25/25/sunny/25/25/25

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

        # Construct the BigQuery SQL query
        query = f"""
            INSERT INTO `{PROJECT_NAME}.WheatherData.weather-records` 
            (date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_wheather, outdoor_windspeed, detector_status, indoor_co2)
            VALUES('{date}', '{time}', {indoor_temp}, {indoor_humidity}, {outdoor_temp}, {outdoor_humidity}, '{outdoor_wheather}', {outdoor_windspeed}, '{detector_status}', {indoor_co2})
        """

        # Run the BigQuery query
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
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    current_weather = forecast_data['list'][0]
    current_temp = current_weather['main']['temp']
    return jsonify(current_temp)

@app.route('/outdoor_humidity')
def outdoor_humidity():
    forecast_data = get_weather_forecast(API_KEY, LOCATION)
    current_weather = forecast_data['list'][0]
    current_humidity = current_weather['main']['humidity']
    return jsonify(current_humidity)


@app.route('/get_icon/<forecast>')
def get_icon(forecast):
    base_url = "https://openweathermap.org/img/wn"
    icon_url = f"{forecast}"
    end_url = '@2x.png'
    return jsonify(f"{base_url}/{icon_url}{end_url}")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
