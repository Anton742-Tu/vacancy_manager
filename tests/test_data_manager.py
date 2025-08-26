import tempfile
import unittest
from pathlib import Path

from src.core.data_manager import DataManager
from src.core.models import Salary, Vacancy


class TestDataManager(unittest.TestCase):

    def setUp(self):
        """Создание временного файла для тестов"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test_vacancies.json"
        self.manager = DataManager(self.test_file)

    def tearDown(self):
        """Очистка после тестов"""
        self.temp_dir.cleanup()

    def test_add_and_get_vacancies(self):
        """Тест добавления и получения вакансий"""
        vacancy = Vacancy(
            id="test_1",
            name="Test Developer",
            company="Test Company",
            salary=Salary(from_amount=100000),
            area="Test City",
        )

        added_count = self.manager.add_vacancies([vacancy])
        self.assertEqual(added_count, 1)

        vacancies = self.manager.get_all_vacancies()
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].id, "test_1")

    def test_duplicate_vacancies(self):
        """Тест обработки дубликатов"""
        vacancy = Vacancy(id="duplicate_id", name="Test Developer", company="Test Company")

        first_add = self.manager.add_vacancies([vacancy])
        second_add = self.manager.add_vacancies([vacancy])

        self.assertEqual(first_add, 1)
        self.assertEqual(second_add, 0)

        vacancies = self.manager.get_all_vacancies()
        self.assertEqual(len(vacancies), 1)

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        vacancy = Vacancy(id="to_delete", name="To Delete", company="Test Company")

        self.manager.add_vacancies([vacancy])

        result = self.manager.delete_vacancy("to_delete")
        self.assertTrue(result)

        vacancies = self.manager.get_all_vacancies()
        self.assertEqual(len(vacancies), 0)

    def test_nonexistent_delete(self):
        """Тест удаления несуществующей вакансии"""
        result = self.manager.delete_vacancy("nonexistent")
        self.assertFalse(result)

    def test_save_and_load(self):
        """Тест сохранения и загрузки из файла"""
        vacancy = Vacancy(id="save_test", name="Save Test", company="Test Company")

        self.manager.add_vacancies([vacancy])

        new_manager = DataManager(self.test_file)
        vacancies = new_manager.get_all_vacancies()

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].id, "save_test")

    def test_corrupted_file(self):
        """Тест обработки поврежденного файла"""
        with open(self.test_file, "w") as f:
            f.write('{"corrupted": "data"')

        manager = DataManager(self.test_file)
        vacancies = manager.get_all_vacancies()

        self.assertEqual(len(vacancies), 0)
