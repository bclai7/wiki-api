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
    elif year and month and day:
        get_week_top_articles(year, month, day)
        return 'in weekly'
    
    return top_articles.json()

def get_week_top_articles(year: str, month: str, day: str):
    '''Get the top articles for a week. Takes in the year, month, and day as an argument and returns the top articles for the week starting
    on the Sunday before the given date throughout the Saturday after the given date'''
    days_list = get_weekdays(year, month, day)
    print(days_list)

def get_weekdays(year: str, month: str, day: str) -> list:
    '''Get all of the dates of the week for a given date, from Sunday to Saturday'''
    day = f'{month}/{day}/{year}'
    dt = datetime.strptime(day, '%m/%d/%Y')
    
    # Get the dates that start and end the week
    week_start_date = dt - timedelta(days=dt.weekday()+1)
    week_end_date = week_start_date + timedelta(days=6)

    # Get all of the dates for the week
    delta = week_end_date - week_start_date
    days_of_week = []
    for i in range(delta.days + 1):
        day = week_start_date + timedelta(days=i)
        days_of_week.append(day)
    
    return days_of_week