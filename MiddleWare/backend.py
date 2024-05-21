from flask import Flask
from google.cloud import bigquery
import os
from flask import jsonify
from google.cloud.exceptions import GoogleCloudError
import requests


PROJECT_NAME = "cloud-project-423208"
key_path = 'MiddleWare/cloud-project-423208-7825c93be1d3.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

client = bigquery.Client(project=PROJECT_NAME)
API_KEY = '8980b87bb33cc5c550a8cae48557b6af'

def get_weather_forecast(api_key):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': 'Lausanne,CH',
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

# http://127.0.0.1:8080/post/2024-04-20/16:02:23/25/25/25/25/sunny/25

@app.route('/post/<date>/<time>/<indoor_temp>/<indoor_humidity>/<outdoor_temp>/<outdoor_humidity>/<outdoor_weather>/<outdoor_windspeed>')
def post(date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_weather, outdoor_windspeed):
    try:
        indoor_temp = float(indoor_temp)
        indoor_humidity = float(indoor_humidity)
        outdoor_temp = float(outdoor_temp)
        outdoor_humidity = float(outdoor_humidity)
        outdoor_windspeed = float(outdoor_windspeed)

        query = """
                INSERT INTO `{0}.WheatherData.weather-records` (date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_wheather, outdoor_windspeed)
                VALUES(@date, @time, @indoor_temp, @indoor_humidity, @outdoor_temp, @outdoor_humidity, @outdoor_wheather, @outdoor_windspeed)
                """.format(PROJECT_NAME)
        query_params = [
            bigquery.ScalarQueryParameter('date', 'DATE', date),
            bigquery.ScalarQueryParameter('time', 'TIME', time),
            bigquery.ScalarQueryParameter('indoor_temp', 'FLOAT', indoor_temp),
            bigquery.ScalarQueryParameter('indoor_humidity', 'FLOAT', indoor_humidity),
            bigquery.ScalarQueryParameter('outdoor_temp', 'FLOAT', outdoor_temp),
            bigquery.ScalarQueryParameter('outdoor_humidity', 'FLOAT', outdoor_humidity),
            bigquery.ScalarQueryParameter('outdoor_wheather', 'STRING', outdoor_weather),
            bigquery.ScalarQueryParameter('outdoor_windspeed', 'FLOAT', outdoor_windspeed)
        ]
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        query_job = client.query(query, job_config=job_config)
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
    forecast_data = get_weather_forecast(API_KEY)
    return jsonify(forecast_data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
