from flask import Flask, make_response, jsonify
from datetime import datetime, timedelta

def get_days_in_range(start_date: datetime, end_date: datetime) -> list:
    '''Get all of the dates from start_date to end_date'''
    delta = end_date - start_date
    days_list = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        if day.date() < datetime.today().date():
            # Only add date if the date is before today
            days_list.append(day)
    return days_list

def create_response_object(detail: str, method: str, status: int, title: str):
    data = {
        "detail": detail,
        "method": method,
        "status": status,
        "title": title,
    }
    response = make_response(jsonify(data))
    response.status_code = status
    response.mimetype = 'application/json'
    
    return response