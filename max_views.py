from flask import request, Blueprint, current_app
import requests
from datetime import datetime, timedelta
from utils import create_response_object
import calendar

max_views = Blueprint("max_views", __name__)

@max_views.route('/api/v1/max_views/day/<title>/<domain>', methods=['GET'])
def get_max_view_day(title: str, domain: str):
    # Get year and month params
    year = request.args.get('year')
    month = request.args.get('month')
    try:
        if year and month:
            start_date = datetime(int(year), int(month), 1)
            last_day_of_month = calendar.monthrange(int(year), int(month))[1]
            end_date = datetime(int(year), int(month), last_day_of_month)
            first_day_of_this_month = datetime.today().replace(day=1)
            if end_date >= first_day_of_this_month:
                return create_response_object("We do not yet have data for this month", "get", 404, "Not Found")
            request_url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{domain}/all-access/all-agents/{title}/daily/{start_date.year}{start_date:%m}{start_date:%d}00/{end_date.year}{end_date:%m}{end_date:%d}00'
            view_count_response = requests.get(request_url, headers=current_app.config['HEADERS'])
            response_obj_list = view_count_response.json()['items']
            data = {
                'date': None,
                'article': title,
                'domain': domain,
                'views': 0
            }


            for item in response_obj_list:
                if item['views'] >= data['views']:
                    data['date'] = datetime.strptime(item['timestamp'], '%Y%m%d00')
                    data['views'] = item['views']
            view_count_json = {'data': data}
        else:
            return create_response_object("Could not complete request. Please make sure your request is valid.", "get", 500, "Could not complete request")
        
        return view_count_json
    except ValueError:
        return create_response_object("Invalid date entered", "get", 400, "Bad Request")
    except Exception:
        return create_response_object("Could not complete request at this time. Please make sure your request is valid or try again later.", "get", 500, "Could not complete request at this time")