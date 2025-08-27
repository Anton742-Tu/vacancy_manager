import logging
import time
from typing import Any, Dict, List, Optional

import requests

from config.settings import HH_API_AREA_RUSSIA, HH_API_BASE_URL, HH_API_TIMEOUT, HH_API_USER_AGENT

from .models import Salary, Vacancy

logger = logging.getLogger(__name__)


class HHruAPIClient:
    def __init__(self):
        self.base_url = HH_API_BASE_URL
        self.timeout = HH_API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": HH_API_USER_AGENT})

    def search_vacancies(
        self, query: str, area: int = HH_API_AREA_RUSSIA, per_page: int = 50, page: int = 0
    ) -> List[Vacancy]:
        """Поиск вакансий на hh.ru"""
        params: Dict[str, Any] = {"text": query, "area": area, "per_page": per_page, "page": page}

        logger.info(f"Поиск вакансий: '{query}', страница {page}")
        start_time = time.time()

        try:
            response = self.session.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            vacancies = self._parse_vacancies(data.get("items", []))

            elapsed = time.time() - start_time
            logger.info(f"Найдено {len(vacancies)} вакансий за {elapsed:.2f} сек")

            return vacancies

        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к API hh.ru: {e}")
            return []
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return []

    def _parse_vacancies(self, items: List[Dict[str, Any]]) -> List[Vacancy]:
        """Быстрый парсинг вакансий"""
        vacancies = []

        for item in items:
            try:
                vacancy = self._parse_vacancy_item_fast(item)
                if vacancy:  # Проверяем, что вакансия корректна
                    vacancies.append(vacancy)
            except Exception as e:
                logger.warning(f"Ошибка парсинга вакансии {item.get('id')}: {e}")
                continue

        return vacancies

    def _parse_vacancy_item_fast(self, item: Dict[str, Any]) -> Optional[Vacancy]:
        """Быстрый парсинг одной вакансии"""
        try:
            # Быстрая проверка обязательных полей
            if not all(key in item for key in ["id", "name", "employer", "area"]):
                return None

            salary_data = item.get("salary")
            salary = None
            if salary_data and any(key in salary_data for key in ["from", "to"]):
                salary = Salary(
                    from_amount=salary_data.get("from"),
                    to_amount=salary_data.get("to"),
                    currency=salary_data.get("currency", "RUB"),
                    gross=salary_data.get("gross"),
                )

            # Минимальная обработка snippet
            snippet = ""
            snippet_data = item.get("snippet")
            if snippet_data and "requirement" in snippet_data:
                snippet = str(snippet_data["requirement"])[:200]  # Ограничиваем длину

            return Vacancy(
                id=str(item["id"]),
                name=str(item["name"]),
                company=str(item["employer"]["name"]),
                salary=salary,
                area=str(item["area"]["name"]),
                url=str(item.get("alternate_url", "")),
                published_at=str(item.get("published_at", "")),
                snippet=snippet,  # Укороченное описание
                experience=str(item.get("experience", {}).get("name", "")),
                employment=str(item.get("employment", {}).get("name", "")),
                source="hh.ru",
            )

        except (KeyError, TypeError, ValueError) as e:
            logger.warning(f"Ошибка быстрого парсинга: {e}")
            return None
