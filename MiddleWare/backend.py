from flask import Flask
from google.cloud import bigquery
import os
from flask import jsonify
import pandas as pd

PROJECT_NAME = "cloud-project-423208"
key_path = 'MiddleWare/cloud-project-423208-7825c93be1d3.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

client = bigquery.Client(project=PROJECT_NAME)


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
            <li><a href="/movie_id">/movie_id</a></li>
            <li>/movie_id/&lt;movie_title&gt;</li>
            <li>/title_from_id/&lt;movie_id&gt;</li>
            <li><a href="/rating_df">/rating_df</a></li>
            <li>/reco/&lt;user_id1&gt;/&lt;user_id2&gt;/&lt;user_id3&gt;</li>
            <li>/elastic_search/&lt;movie&gt;</li>
        </ul>
    </body>
    </html>
    '''
    return endpoints

@app.route('/movie_title')
def movie_title():
    query = f"""
            SELECT w.date
            FROM `{PROJECT_NAME}.WheatherData.weather-records` w
            """
    query_job = client.query(query)
    results = query_job.to_dataframe()
    return results.to_json()

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
                INSERT INTO `{0}.WeatherData.weather-records` (date, time, indoor_temp, indoor_humidity, outdoor_temp, outdoor_humidity, outdoor_weather, outdoor_windspeed)
                VALUES(@date, @time, @indoor_temp, @indoor_humidity, @outdoor_temp, @outdoor_humidity, @outdoor_weather, @outdoor_windspeed)
                """.format(PROJECT_NAME)
        query_params = [
            bigquery.ScalarQueryParameter('date', 'STRING', date),
            bigquery.ScalarQueryParameter('time', 'STRING', time),
            bigquery.ScalarQueryParameter('indoor_temp', 'FLOAT', indoor_temp),
            bigquery.ScalarQueryParameter('indoor_humidity', 'FLOAT', indoor_humidity),
            bigquery.ScalarQueryParameter('outdoor_temp', 'FLOAT', outdoor_temp),
            bigquery.ScalarQueryParameter('outdoor_humidity', 'FLOAT', outdoor_humidity),
            bigquery.ScalarQueryParameter('outdoor_weather', 'STRING', outdoor_weather),
            bigquery.ScalarQueryParameter('outdoor_windspeed', 'FLOAT', outdoor_windspeed)
        ]
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        query_job = client.query(query, job_config=job_config)
        query_job.result() 

        return jsonify('Data added successfully'), 200
    except Exception as e:
        print(e)
        return jsonify('Failed to add data'), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
