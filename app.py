from flask import Flask
from datetime import datetime, timedelta
from top_articles import top_articles
from view_count import view_count
from max_views import max_views

app = Flask(__name__)
app.register_blueprint(top_articles)
app.register_blueprint(view_count)
app.register_blueprint(max_views)
app.debug = True

app.config['HEADERS'] = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

@app.route('/')
def home():
    return 'This is the Wiki API'

