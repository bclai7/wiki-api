from flask import request, Blueprint, current_app
import requests
from datetime import datetime, timedelta
from utils import create_response_object, get_week_start_and_end_dates
import calendar

view_count = Blueprint("view_count", __name__)

@view_count.route('/api/v1/view_count/article/<title>/<domain>', methods=['GET'])
def get_view_count(title: str, domain: str):
    # Get year, month, and day params
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    try:
        # Check if monthly or weekly
        if year and month and day is None:
            # Month
            start_date = datetime(int(year), int(month), 1)
            last_day_of_month = calendar.monthrange(int(year), int(month))[1]
            end_date = datetime(int(year), int(month), last_day_of_month)
            first_day_of_this_month = datetime.today().replace(day=1)
            if start_date >= end_date:
                return create_response_object("Start date must be before end date", "get", 400, "Bad Request")
            if end_date >= first_day_of_this_month:
                return create_response_object("We do not yet have data for this month", "get", 404, "Not Found")
            request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{domain}/all-access/all-agents/{title}/monthly/{start_date.year}{start_date:%m}{start_date:%d}00/{end_date.year}{end_date:%m}{end_date:%d}00'
            view_count_response = requests.get(request_url, headers=current_app.config['HEADERS'])
            response_obj = view_count_response.json()['items'][0]
            view_count_json = {'data': {'type': 'month', 'dates': [start_date.strftime("%B %Y")], 'article': response_obj['article']}, 'domain': response_obj['project'], 'views': response_obj['views']}
        elif year and month and day:
            # Week
            date = datetime(int(year), int(month), int(day))
            week_start_date, week_end_date = get_week_start_and_end_dates(date)
            if week_end_date >= datetime.today():
                return create_response_object("We do not yet have data for this week", "get", 404, "Not Found")
            
            view_count_json = {'data': get_week_view_count(week_start_date, week_end_date, domain, title)}
        else:
            return create_response_object("Could not complete request. Please make sure your request is valid.", "get", 500, "Could not complete request")
        
        return view_count_json
    except ValueError:
        return create_response_object("Invalid date entered", "get", 400, "Bad Request")
    except Exception:
        return create_response_object("Could not complete request at this time. Please make sure your request is valid or try again later.", "get", 500, "Could not complete request at this time")
    
def get_week_view_count(start_date: datetime, end_date: datetime, domain: str, title: str):
    request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{domain}/all-access/all-agents/{title}/daily/{start_date.year}{start_date:%m}{start_date:%d}00/{end_date.year}{end_date:%m}{end_date:%d}00'
    view_count_response = requests.get(request_url, headers=current_app.config['HEADERS'])
    response_obj_list = view_count_response.json()['items']
    view_count = 0
    for item in response_obj_list:
        view_count = view_count + item['views']
    
    data = {
        'type': 'week',
        'dates': [start_date, end_date],
        'article': title,
        'domain': domain,
        'views': view_count
    }

    return data