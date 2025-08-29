import unittest

from src.core.models import Salary, Vacancy
from src.utils.filters import VacancyFilter


class TestFilters(unittest.TestCase):

    def setUp(self):
        """Создание тестовых вакансий"""
        self.vacancies = [
            Vacancy(
                id="1",
                name="Python Developer",
                company="Yandex",
                salary=Salary(from_amount=100000, to_amount=150000),
                area="Moscow",
                experience="1-3 года",
                employment="полная занятость",
            ),
            Vacancy(
                id="2",
                name="Java Developer",
                company="Sber",
                salary=Salary(from_amount=120000, to_amount=180000),
                area="Saint Petersburg",
                experience="3-6 лет",
                employment="полная занятость",
            ),
            Vacancy(
                id="3",
                name="Data Scientist",
                company="Yandex",
                salary=Salary(from_amount=150000, to_amount=250000),
                area="Moscow",
                experience="более 6 лет",
                employment="удаленная работа",
            ),
        ]

        self.filter = VacancyFilter()

    def test_filter_by_company(self):
        """Тест фильтрации по компании"""
        filtered = self.filter.filter_by_company(self.vacancies, "Yandex")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(v.company == "Yandex" for v in filtered))

    def test_filter_by_area(self):
        """Тест фильтрации по городу"""
        filtered = self.filter.filter_by_area(self.vacancies, "Moscow")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(v.area == "Moscow" for v in filtered))

    def test_filter_by_experience(self):
        """Тест фильтрации по опыту"""
        filtered = self.filter.filter_by_experience(self.vacancies, "3-6 лет")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, "2")

    def test_filter_by_employment(self):
        """Тест фильтрации по типу занятости"""
        filtered = self.filter.filter_by_employment(self.vacancies, "удаленная работа")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, "3")

    def test_empty_filter(self):
        """Тест пустой фильтрации"""
        filtered = self.filter.filter_by_company(self.vacancies, "NonExistentCompany")
        self.assertEqual(len(filtered), 0)
