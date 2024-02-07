from datetime import datetime
import unittest
from app import app
    
class TestTopArticles():
    MOST_VIEWED_URL = '/api/v1/articles/most_viewed/en.wikipedia'
    def test_monthly_top_articles_200_response(self):
        # Valid date entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '2021', 'month': '1'})
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert b'articles' in response.data

    def test_monthly_top_articles_400_response(self):
        # Invalid month entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '2021', 'month': '100'})
        assert response.status_code == 400
        # Invalid year entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '20211', 'month': '1'})
        assert response.status_code == 400
        # Letters entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': 'f', 'month': 'a'})
        assert response.status_code == 400

    def test_monthly_top_articles_404_response(self):
        # Future date entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': str(datetime.today().year + 1), 'month': '1'})
        assert response.status_code == 404

    def test_monthly_top_articles_500_response(self):
        # No date entered
        response = app.test_client().get(self.MOST_VIEWED_URL)
        assert response.status_code == 500
    
    def test_weekly_top_articles_200_response(self):
        # Valid date entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '2021', 'month': '1', 'day': '1'})
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert b'articles' in response.data

    def test_weekly_top_articles_400_response(self):
        # Invalid day entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '2021', 'month': '1', 'day': '100'})
        assert response.status_code == 400
        # Invalid month entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '2021', 'month': '100', 'day': '10'})
        assert response.status_code == 400
        # Invalid year entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': '20211', 'month': '1', 'day': '10'})
        assert response.status_code == 400
        # Letters entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': 'f', 'month': 'a', 'day': 'v'})
        assert response.status_code == 400

    def test_weekly_top_articles_404_response(self):
        # Future date entered
        response = app.test_client().get(self.MOST_VIEWED_URL, query_string={'year': str(datetime.today().year + 1), 'month': '1', 'day': '10'})
        assert response.status_code == 404

    def test_weekly_top_articles_500_response(self):
        # No date entered
        response = app.test_client().get(self.MOST_VIEWED_URL)
        assert response.status_code == 500

if __name__ == '__main__':
    unittest.main()

