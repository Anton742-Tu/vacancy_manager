from typing import Any, Dict, List, Optional, Union, cast

import requests

from config.settings import HH_API_AREA_RUSSIA, HH_API_BASE_URL, HH_API_TIMEOUT

from .models import Salary, Vacancy

# Тип для параметров запроса
RequestParams = Dict[str, Union[str, int, float, None]]


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
        params: RequestParams = {"text": query, "area": area, "per_page": per_page, "page": page}

        try:
            # Явно указываем тип для response
            response: requests.Response = requests.get(
                self.base_url, params=params, timeout=self.timeout  # Теперь mypy будет доволен
            )
            response.raise_for_status()
            data: Dict[str, Any] = response.json()

            return self._parse_vacancies(data.get("items", []))

        except requests.RequestException as e:
            raise Exception(f"Ошибка при запросе к API hh.ru: {e}")

    def _parse_vacancies(self, items: List[Dict[str, Any]]) -> List[Vacancy]:
        """Парсинг вакансий из ответа API"""
        vacancies: List[Vacancy] = []

        for item in items:
            try:
                vacancy = self._parse_vacancy_item(item)
                vacancies.append(vacancy)
            except Exception as e:
                print(f"Ошибка при парсинге вакансии {item.get('id')}: {e}")

        return vacancies

    def _parse_vacancy_item(self, item: Dict[str, Any]) -> Vacancy:
        """Парсинг одной вакансии"""
        salary_data: Optional[Dict[str, Any]] = item.get("salary")
        salary: Optional[Salary] = None

        if salary_data:
            salary = Salary(
                from_amount=salary_data.get("from"),
                to_amount=salary_data.get("to"),
                currency=salary_data.get("currency", "RUB"),
                gross=salary_data.get("gross"),
            )

        # Получаем snippet с проверкой на None
        snippet_data: Optional[Dict[str, Any]] = item.get("snippet")
        snippet: str = ""
        if snippet_data:
            snippet = cast(str, snippet_data.get("requirement", ""))

        # Проверяем обязательные поля
        employer: Dict[str, Any] = item["employer"]
        area_data: Dict[str, Any] = item["area"]
        experience: Dict[str, Any] = item["experience"]
        employment: Dict[str, Any] = item["employment"]

        return Vacancy(
            id=str(item["id"]),  # Гарантируем строковый тип
            name=str(item["name"]),
            company=str(employer["name"]),
            salary=salary,
            area=str(area_data["name"]),
            url=str(item["alternate_url"]),
            published_at=str(item["published_at"]),
            snippet=snippet,
            experience=str(experience["name"]),
            employment=str(employment["name"]),
            source="hh.ru",
        )
