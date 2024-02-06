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
        request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{year}/{month}/all-days'
        top_articles_response = requests.get(request_url, headers=HEADERS)
        top_articles_json = {'data': {'type': 'month', 'articles': top_articles_response.json()['items'][0]['articles']}}
    elif year and month and day:
        top_articles_list = get_week_top_articles(year, month, day)
        top_articles_json = {'data': {'type': 'week', 'articles': top_articles_list}}
    
    return top_articles_json

def get_week_top_articles(year: str, month: str, day: str):
    '''Get the top articles for a week. Takes in the year, month, and day as an argument and returns the top articles for the week starting
    on the Sunday before the given date throughout the Saturday after the given date'''
    # Get list of days in the week for the given date
    days_list = get_weekdays(year, month, day)

    # For each day of the week, check the top articles and update dict with count
    article_views_dict = {}
    for day in days_list:
        # Get list of articles for this day
        request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{day.year}/{day.month}/{day.day}'
        day_top_articles_response = requests.get(request_url, headers=HEADERS)
        day_top_articles_json = day_top_articles_response.json()
        day_top_articles_list = day_top_articles_json['items'][0]['articles']
        
        # Update total week view count of each article on this day
        for article in day_top_articles_list:
            article_views_dict[article['article']] = article_views_dict.setdefault(article['article'], 0) + int(article['views'])
        
    # Sort list by views in descending order
    sorted_article_views_list = sorted(article_views_dict.items(), key=lambda x:x[1], reverse=True)
    
    # Populate output list of objects to be returned
    ranked_articles_list = []
    rank = 1
    for key, value in sorted_article_views_list:
        ranked_articles_list.append({'article': key, 'rank': rank, 'views': value})
        rank += 1
        
    return ranked_articles_list


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