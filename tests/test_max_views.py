from datetime import datetime
import unittest
from app import app
    
class TestMaxViews():
    MAX_VIEWS_URL = '/api/v1/max_views/day/Barack_Obama/en.wikipedia'
    def test_monthly_max_views_200_response(self):
        # Valid date entered
        response = app.test_client().get(self.MAX_VIEWS_URL, query_string={'year': '2021', 'month': '1'})
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert b'article' in response.data
        assert b'views' in response.data

    def test_monthly_max_views_400_response(self):
        # Invalid month entered
        response = app.test_client().get(self.MAX_VIEWS_URL, query_string={'year': '2021', 'month': '100'})
        assert response.status_code == 400
        # Invalid year entered
        response = app.test_client().get(self.MAX_VIEWS_URL, query_string={'year': '20211', 'month': '1'})
        assert response.status_code == 400
        # Letters entered
        response = app.test_client().get(self.MAX_VIEWS_URL, query_string={'year': 'f', 'month': 'a'})
        assert response.status_code == 400

    def test_monthly_max_views_404_response(self):
        # Future date entered
        response = app.test_client().get(self.MAX_VIEWS_URL, query_string={'year': str(datetime.today().year + 1), 'month': '1'})
        assert response.status_code == 404

    def test_monthly_max_views_500_response(self):
        # No date entered
        response = app.test_client().get(self.MAX_VIEWS_URL)
        assert response.status_code == 500

if __name__ == '__main__':
    unittest.main()

