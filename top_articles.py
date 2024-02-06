from flask import request, Blueprint, current_app
import requests
from datetime import datetime
from utils import get_days_in_range, create_response_object, get_week_start_and_end_dates

top_articles = Blueprint("top_articles", __name__)

@top_articles.route('/api/v1/articles/most_viewed/<domain>', methods=['GET'])
def get_top_articles(domain: str):
    # Get year, month, and day params
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')

    try:
        # Check if monthly or weekly
        if year and month and day is None:
            # Month
            date = datetime(int(year), int(month), 1)
            first_day_of_this_month = datetime.today().replace(day=1)
            if date >= first_day_of_this_month:
                return create_response_object("We do not yet have data for this month", "get", 404, "Not Found")
            request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{domain}/all-access/{date.year}/{date:%m}/all-days'
            top_articles_response = requests.get(request_url, headers=current_app.config['HEADERS'])
            top_articles_json = {'data': {'type': 'month', 'dates': [date.strftime("%B %Y")], 'articles': top_articles_response.json()['items'][0]['articles']}}
        elif year and month and day:
            # Week
            date = datetime(int(year), int(month), int(day))
            top_articles_list, dates_list = get_week_top_articles(date, domain)
            if(len(top_articles_list) == 0):
                return create_response_object("We do not yet have data for this week", "get", 404, "Not Found")
            top_articles_json = {'data': {'type': 'week', 'dates': dates_list, 'articles': top_articles_list}}
        else:
            return create_response_object("Could not complete request. Please make sure your request is valid.", "get", 500, "Could not complete request")
        
        return top_articles_json
    except ValueError:
        return create_response_object("Invalid date entered", "get", 400, "Bad Request")
    except Exception:
        return create_response_object("Could not complete request at this time. Please make sure your request is valid or try again later.", "get", 500, "Could not complete request at this time")

def get_week_top_articles(date: datetime, domain: str):
    '''Get the top articles for a week. Takes in the date as an argument and returns the top articles for the week starting
    on the Monday before the given date throughout the Sunday after the given date'''
    # Get list of days in the week for the given date
    days_list = get_weekdays(date)
    if len(days_list) == 0:
        # If there are no valid dates for the week of the given date, return empty lists
        return [], []

    # For each day of the week, check the top articles and update dict with count
    article_views_dict = {}
    for day in days_list:
        # Get list of articles for this day
        request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{domain}/all-access/{day.year}/{day:%m}/{day:%d}'
        day_top_articles_response = requests.get(request_url, headers=current_app.config['HEADERS'])
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
        
    return ranked_articles_list, days_list

def get_weekdays(date: datetime) -> list:
    '''Get all of the dates of the week for a given date, from Monday to Sunday'''
    # Get the dates that start and end the week
    week_start_date, week_end_date = get_week_start_and_end_dates(date)

    # Get all of the dates for the week
    days_of_week = get_days_in_range(week_start_date, week_end_date)
    
    return days_of_week


