from flask import request, Blueprint, current_app
import requests
from datetime import datetime, timedelta
from utils import get_days_in_range, create_response_object

max_views = Blueprint("max_views", __name__)