from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.settings import MAX_VACANCIES_PER_REQUEST

from .core.api_client import HHruAPIClient
from .core.data_manager import DataManager
from .core.models import Salary, Vacancy
from .utils.exporters import CSVExporter, ExcelExporter, JSONExporter
from .utils.filters import VacancyFilter


class VacancyManager:
    def __init__(self, data_file: Optional[Path] = None):
        self.api_client = HHruAPIClient()
        self.data_manager = DataManager(data_file)
        self.filter = VacancyFilter()
        self.excel_exporter = ExcelExporter()
        self.csv_exporter = CSVExporter()
        self.json_exporter = JSONExporter()

    def search_and_add_vacancies(self, query: str, count: int = 20) -> int:
        """Поиск и добавление вакансий с hh.ru"""
        if count > MAX_VACANCIES_PER_REQUEST:
            count = MAX_VACANCIES_PER_REQUEST

        vacancies = self.api_client.search_vacancies(query, per_page=count)
        return self.data_manager.add_vacancies(vacancies)

    def add_manual_vacancy(self, vacancy_data: Dict[str, Any]) -> bool:
        """Добавление ручной вакансии"""
        try:
            salary_data = vacancy_data.get("salary", {})
            salary = Salary(
                from_amount=salary_data.get("from"),
                to_amount=salary_data.get("to"),
                currency=salary_data.get("currency", "RUB"),
            )

            vacancy = Vacancy(
                id=f"manual_{datetime.now().timestamp()}",
                name=vacancy_data["name"],
                company=vacancy_data["company"],
                salary=salary,
                area=vacancy_data.get("area", ""),
                url=vacancy_data.get("url", ""),
                published_at=vacancy_data.get("published_at", datetime.now().isoformat()),
                snippet=vacancy_data.get("snippet", ""),
                experience=vacancy_data.get("experience", ""),
                employment=vacancy_data.get("employment", ""),
                source="manual",
            )

            self.data_manager.add_vacancies([vacancy])
            return True

        except Exception as e:
            print(f"Ошибка при добавлении вакансии: {e}")
            return False

    def get_vacancies(self, filters: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получение вакансий с фильтрацией"""
        vacancies = self.data_manager.get_all_vacancies()

        if not filters:
            return vacancies

        filtered_vacancies = vacancies

        if "company" in filters:
            filtered_vacancies = self.filter.filter_by_company(filtered_vacancies, filters["company"])

        if "area" in filters:
            filtered_vacancies = self.filter.filter_by_area(filtered_vacancies, filters["area"])

        if "min_salary" in filters:
            filtered_vacancies = self.filter.filter_by_min_salary(filtered_vacancies, filters["min_salary"])

        if "experience" in filters:
            filtered_vacancies = self.filter.filter_by_experience(filtered_vacancies, filters["experience"])

        if "employment" in filters:
            filtered_vacancies = self.filter.filter_by_employment(filtered_vacancies, filters["employment"])

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаление вакансии"""
        return self.data_manager.delete_vacancy(vacancy_id)

    def clear_all_vacancies(self) -> None:
        """Очистка всех вакансий"""
        self.data_manager.clear_all_vacancies()

    def export_to_excel(self, filename: str = "vacancies.xlsx") -> str:
        """Экспорт в Excel - возвращает путь к файлу или сообщение об ошибке"""
        vacancies = self.data_manager.get_all_vacancies()
        if not vacancies:
            return "Нет данных для экспорта"
        return self.excel_exporter.export_to_excel(vacancies, filename)

    def export_to_csv(self, filename: str = "vacancies.csv") -> str:
        """Экспорт в CSV - возвращает путь к файлу или сообщение об ошибке"""
        vacancies = self.data_manager.get_all_vacancies()
        if not vacancies:
            return "Нет данных для экспорта"
        return self.csv_exporter.export_to_csv(vacancies, filename)

    def export_to_json(self, filename: str = "vacancies_export.json") -> str:
        """Экспорт в JSON - возвращает путь к файлу или сообщение об ошибке"""
        vacancies = self.data_manager.get_all_vacancies()
        if not vacancies:
            return "Нет данных для экспорта"
        return self.json_exporter.export_to_json(vacancies, filename)

    def get_statistics(self) -> Dict[str, Any]:
        """Получение статистики"""
        vacancies = self.data_manager.get_all_vacancies()

        if not vacancies:
            return {}

        from collections import Counter

        stats = {
            "total": len(vacancies),
            "by_company": Counter(v.company for v in vacancies),
            "by_area": Counter(v.area for v in vacancies),
            "by_experience": Counter(v.experience for v in vacancies),
            "by_employment": Counter(v.employment for v in vacancies),
            "with_salary": sum(1 for v in vacancies if v.salary),
            "sources": Counter(v.source for v in vacancies),
        }

        return stats
