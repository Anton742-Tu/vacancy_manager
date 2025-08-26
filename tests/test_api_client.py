# tests/test_api_client.py
import unittest
from unittest.mock import Mock, patch
from src.core.api_client import HHruAPIClient


class TestAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = HHruAPIClient()

    @patch('src.core.api_client.requests.Session.get')
    def test_successful_search(self, mock_get):
        """Тест успешного поиска вакансий"""
        # Мокируем ответ API
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [
                {
                    'id': 'test_1',
                    'name': 'Python Developer',
                    'employer': {'name': 'Test Company'},
                    'area': {'name': 'Moscow'},
                    'salary': {'from': 100000, 'to': 150000, 'currency': 'RUB'},
                    'alternate_url': 'https://hh.ru/vacancy/test_1',
                    'published_at': '2024-01-01T10:00:00+0300',
                    'snippet': {'requirement': 'Python experience'},
                    'experience': {'name': '1-3 года'},
                    'employment': {'name': 'полная занятость'}
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем поиск
        vacancies = self.client.search_vacancies('Python')

        # Проверяем результаты
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].id, 'test_1')
        self.assertEqual(vacancies[0].name, 'Python Developer')
        self.assertEqual(vacancies[0].company, 'Test Company')
        self.assertIsNotNone(vacancies[0].salary)

    @patch('src.core.api_client.requests.Session.get')
    def test_api_error(self, mock_get):
        """Тест обработки ошибки API"""
        mock_get.side_effect = Exception('API error')

        vacancies = self.client.search_vacancies('Python')

        self.assertEqual(len(vacancies), 0)

    @patch('src.core.api_client.requests.Session.get')
    def test_empty_response(self, mock_get):
        """Тест пустого ответа от API"""
        mock_response = Mock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        vacancies = self.client.search_vacancies('NonexistentQuery')

        self.assertEqual(len(vacancies), 0)
