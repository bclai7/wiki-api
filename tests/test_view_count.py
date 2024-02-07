from datetime import datetime
import unittest
from app import app
    
class TestViewCount():
    VIEW_COUNT_URL = '/api/v1/view_count/article/Barack_Obama/en.wikipedia'
    def test_monthly_view_count_200_response(self):
        # Valid date entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '2021', 'month': '1'})
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert b'article' in response.data
        assert b'views' in response.data

    def test_monthly_view_count_400_response(self):
        # Invalid month entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '2021', 'month': '100'})
        assert response.status_code == 400
        # Invalid year entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '20211', 'month': '1'})
        assert response.status_code == 400
        # Letters entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': 'f', 'month': 'a'})
        assert response.status_code == 400

    def test_monthly_view_count_404_response(self):
        # Future date entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': str(datetime.today().year + 1), 'month': '1'})
        assert response.status_code == 404

    def test_monthly_view_count_500_response(self):
        # No date entered
        response = app.test_client().get(self.VIEW_COUNT_URL)
        assert response.status_code == 500
    
    def test_weekly_view_count_200_response(self):
        # Valid date entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '2021', 'month': '1', 'day': '1'})
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert b'article' in response.data
        assert b'views' in response.data

    def test_weekly_view_count_400_response(self):
        # Invalid day entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '2021', 'month': '1', 'day': '100'})
        assert response.status_code == 400
        # Invalid month entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '2021', 'month': '100', 'day': '10'})
        assert response.status_code == 400
        # Invalid year entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': '20211', 'month': '1', 'day': '10'})
        assert response.status_code == 400
        # Letters entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': 'f', 'month': 'a', 'day': 'v'})
        assert response.status_code == 400

    def test_weekly_view_count_404_response(self):
        # Future date entered
        response = app.test_client().get(self.VIEW_COUNT_URL, query_string={'year': str(datetime.today().year + 1), 'month': '1', 'day': '10'})
        assert response.status_code == 404

    def test_weekly_view_count_500_response(self):
        # No date entered
        response = app.test_client().get(self.VIEW_COUNT_URL)
        assert response.status_code == 500

if __name__ == '__main__':
    unittest.main()

