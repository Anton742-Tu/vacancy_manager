from datetime import datetime
from typing import Dict, List, Optional

import requests

from config.settings import HH_API_AREA_RUSSIA, HH_API_BASE_URL, HH_API_TIMEOUT

from .models import Salary, Vacancy


class HHruAPIClient:
    def __init__(self):
        self.base_url = HH_API_BASE_URL
        self.timeout = HH_API_TIMEOUT

    def search_vacancies(
        self, query: str, area: int = HH_API_AREA_RUSSIA, per_page: int = 50, page: int = 0
    ) -> List[Vacancy]:
        """
        Поиск вакансий на hh.ru
        """
        params = {"text": query, "area": area, "per_page": per_page, "page": page}

        try:
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            return self._parse_vacancies(data.get("items", []))

        except requests.RequestException as e:
            raise Exception(f"Ошибка при запросе к API hh.ru: {e}")

    def _parse_vacancies(self, items: List[Dict]) -> List[Vacancy]:
        """Парсинг вакансий из ответа API"""
        vacancies = []

        for item in items:
            try:
                vacancy = self._parse_vacancy_item(item)
                vacancies.append(vacancy)
            except Exception as e:
                print(f"Ошибка при парсинге вакансии {item.get('id')}: {e}")

        return vacancies

    def _parse_vacancy_item(self, item: Dict) -> Vacancy:
        """Парсинг одной вакансии"""
        salary_data = item.get("salary")
        salary = None
        if salary_data:
            salary = Salary(
                from_amount=salary_data.get("from"),
                to_amount=salary_data.get("to"),
                currency=salary_data.get("currency", "RUB"),
                gross=salary_data.get("gross"),
            )

        return Vacancy(
            id=item["id"],
            name=item["name"],
            company=item["employer"]["name"],
            salary=salary,
            area=item["area"]["name"],
            url=item["alternate_url"],
            published_at=item["published_at"],
            snippet=item["snippet"].get("requirement", "") if item.get("snippet") else "",
            experience=item["experience"]["name"],
            employment=item["employment"]["name"],
            source="hh.ru",
        )
