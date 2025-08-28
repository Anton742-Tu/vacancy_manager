import logging
import time
from typing import Any, Dict, List, Optional

import requests

from config.settings import HH_API_BASE_URL, HH_API_TIMEOUT, HH_API_USER_AGENT, HH_API_AREA_RUSSIA
from .models import Vacancy

logger = logging.getLogger(__name__)


class Salary:
    pass


class HHruAPIClient:
    def __init__(self):
        self.base_url = HH_API_BASE_URL
        self.timeout = HH_API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": HH_API_USER_AGENT,
            "Accept": "application/json",
        })

    def search_vacancies(
            self, query: str, area: int = HH_API_AREA_RUSSIA, per_page: int = 50, page: int = 0
    ) -> List[Vacancy]:
        """Поиск вакансий на hh.ru"""
        params: Dict[str, Any] = {
            "text": query,
            "area": area,
            "per_page": per_page,
            "page": page
        }

        logger.info(f"Поиск вакансий: '{query}', страница {page}")
        start_time = time.time()

        try:
            response = self.session.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            found = data.get("found", 0)
            items = data.get("items", [])

            logger.info(f"API вернуло: found={found}, items={len(items)}")

            vacancies = self._parse_vacancies(items)

            elapsed = time.time() - start_time
            logger.info(f"Успешно распаршено {len(vacancies)} вакансий за {elapsed:.2f} сек")

            # Логируем первую вакансию для отладки
            if vacancies and logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Первая вакансия: {vacancies[0]}")

            return vacancies

        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к API hh.ru: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Статус код: {e.response.status_code}")
                logger.error(f"Ответ сервера: {e.response.text[:500]}...")
            return []
        except Exception as e:
            logger.error(f"Неожиданная ошибка при парсинге: {e}")
            return []

    def _parse_vacancies(self, items: List[Dict[str, Any]]) -> List[Vacancy]:
        """Парсинг вакансий с улучшенной обработкой ошибок"""
        vacancies = []

        for item in items:
            try:
                vacancy = self._parse_vacancy_item(item)
                if vacancy:
                    vacancies.append(vacancy)
            except Exception as e:
                logger.warning(f"Ошибка парсинга вакансии {item.get('id')}: {e}")
                # Логируем проблемные данные для отладки
                logger.debug(f"Проблемные данные: {item}")
                continue

        return vacancies

    def _parse_vacancy_item(self, item: Dict[str, Any]) -> Optional[Vacancy]:
        """Парсинг одной вакансии с проверкой обязательных полей"""
        try:
            # Проверяем обязательные поля
            if not all(key in item for key in ["id", "name", "employer", "area"]):
                logger.warning(f"Пропускаем вакансию {item.get('id')}: отсутствуют обязательные поля")
                return None

            # Обработка зарплаты
            salary_data = item.get("salary")
            salary = None
            if salary_data:
                salary = self._parse_salary(salary_data)

            # Обработка snippet
            snippet = ""
            snippet_data = item.get("snippet", {})
            if snippet_data and "requirement" in snippet_data:
                snippet = str(snippet_data["requirement"] or "")

            # Создаем вакансию
            return Vacancy(
                id=str(item["id"]),
                name=str(item["name"]),
                company=str(item["employer"]["name"]),
                salary=salary,
                area=str(item["area"]["name"]),
                url=str(item.get("alternate_url", "")),
                published_at=str(item.get("published_at", "")),
                snippet=snippet,
                experience=str(item.get("experience", {}).get("name", "")),
                employment=str(item.get("employment", {}).get("name", "")),
                source="hh.ru",
            )

        except (KeyError, TypeError, ValueError) as e:
            logger.warning(f"Ошибка парсинга вакансии {item.get('id')}: {e}")
            logger.debug(f"Данные вакансии: {item}")
            return None

    def _parse_salary(self, salary_data: Dict[str, Any]) -> Optional[Salary]:
        """Парсинг данных о зарплате"""
        from .models import Salary

        if not salary_data:
            return None

        try:
            return Salary(
                from_amount=salary_data.get("from"),
                to_amount=salary_data.get("to"),
                currency=salary_data.get("currency", "RUB"),
                gross=salary_data.get("gross"),
            )
        except Exception as e:
            logger.warning(f"Ошибка парсинга зарплаты: {e}")
            return None
