from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
app.run(debug=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

@app.route('/')
def home():
    return 'This is the Wiki API'

@app.route('/api/v1/articles/most_viewed', methods=['GET'])
def get_top_articles():
    # Get year, month, and day params
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    # Check if monthly or weekly
    if year and month and day is None:
        request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikisource/all-access/{year}/{month}/all-days'
        top_articles = requests.get(request_url, headers=HEADERS)
    return top_articles.json()
