import unittest

from src.core.models import Salary, Vacancy


class TestModels(unittest.TestCase):

    def test_salary_creation(self):
        """Тест создания объекта Salary"""
        salary = Salary(from_amount=100000, to_amount=150000, currency="RUB", gross=True)
        self.assertEqual(salary.from_amount, 100000)
        self.assertEqual(salary.to_amount, 150000)
        self.assertEqual(salary.currency, "RUB")
        self.assertTrue(salary.gross)

    def test_salary_to_dict(self):
        """Тест преобразования Salary в словарь"""
        salary = Salary(from_amount=100000, to_amount=150000, currency="RUB")
        salary_dict = salary.to_dict()

        expected = {"from": 100000, "to": 150000, "currency": "RUB", "gross": None}
        self.assertEqual(salary_dict, expected)

    def test_salary_from_dict(self):
        """Тест создания Salary из словаря"""
        data = {"from": 100000, "to": 150000, "currency": "USD", "gross": True}
        salary = Salary.from_dict(data)

        self.assertEqual(salary.from_amount, 100000)
        self.assertEqual(salary.to_amount, 150000)
        self.assertEqual(salary.currency, "USD")
        self.assertTrue(salary.gross)

    def test_vacancy_creation(self):
        """Тест создания объекта Vacancy"""
        salary = Salary(from_amount=100000, to_amount=150000)
        vacancy = Vacancy(
            id="123",
            name="Python Developer",
            company="Test Company",
            salary=salary,
            area="Moscow",
            url="https://hh.ru/vacancy/123",
        )

        self.assertEqual(vacancy.id, "123")
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.company, "Test Company")
        self.assertEqual(vacancy.area, "Moscow")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123")

    def test_vacancy_to_dict(self):
        """Тест преобразования Vacancy в словарь"""
        salary = Salary(from_amount=100000, to_amount=150000)
        vacancy = Vacancy(id="123", name="Python Developer", company="Test Company", salary=salary)

        vacancy_dict = vacancy.to_dict()

        self.assertEqual(vacancy_dict["id"], "123")
        self.assertEqual(vacancy_dict["name"], "Python Developer")
        self.assertEqual(vacancy_dict["company"], "Test Company")
        self.assertIsNotNone(vacancy_dict["salary"])

    def test_vacancy_from_dict(self):
        """Тест создания Vacancy из словаря"""
        data = {
            "id": "123",
            "name": "Python Developer",
            "company": "Test Company",
            "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
            "area": "Moscow",
            "url": "https://hh.ru/vacancy/123",
        }

        vacancy = Vacancy.from_dict(data)

        self.assertEqual(vacancy.id, "123")
        self.assertEqual(vacancy.name, "Python Developer")
        self.assertEqual(vacancy.company, "Test Company")
        self.assertEqual(vacancy.area, "Moscow")
        self.assertIsNotNone(vacancy.salary)
        self.assertEqual(vacancy.salary.from_amount, 100000)
