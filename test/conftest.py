import pytest
import requests
from unittest.mock import MagicMock

from src.hh_api_client import HHAPIClient


@pytest.fixture
def mock_requests(monkeypatch):
    """Mocking requests.get to return predefined responses."""
    def mock_get(url, *args, **kwargs):
        mock_response = MagicMock()
        if "employers" in url:
            if "12345" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'id': 12345,
                    'name': 'Test Employer'
                }
            elif "67890" in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'id': 67890,
                    'name': 'Another Test Employer'
                }
            else:
                mock_response.status_code = 404
        elif "vacancies" in url:
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'items': [{'id': 1, 'name': 'Test Vacancy'}],
                'pages': 1
            }
        return mock_response

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture
def hh_api_client():
    """Fixture to create an instance of HHAPIClient."""
    return HHAPIClient()
