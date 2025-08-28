# src/utils/exporters.py
import json
import logging
import time
from typing import Any, Dict, List, Optional

import pandas as pd

from config.settings import (
    CSV_ENCODING,
    CSV_SEPARATOR,
    DEFAULT_CSV_FILENAME,
    DEFAULT_EXCEL_FILENAME,
    DEFAULT_JSON_FILENAME,
    EXPORTS_DIR,
)

from ..core.models import Vacancy

logger = logging.getLogger(__name__)


class ExcelExporter:
    def export_to_excel(self, vacancies: List[Vacancy], filename: Optional[str] = None) -> str:
        """Экспорт вакансий в Excel"""
        if not vacancies:
            return "Нет данных для экспорта"

        filename = filename or DEFAULT_EXCEL_FILENAME
        logger.info(f"Экспорт {len(vacancies)} вакансий в Excel")
        start_time = time.time()

        try:
            chunk_size = 1000
            filepath = EXPORTS_DIR / filename

            with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
                for i in range(0, len(vacancies), chunk_size):
                    chunk = vacancies[i : i + chunk_size]
                    data = self._prepare_chunk_data(chunk)

                    df = pd.DataFrame(data)
                    sheet_name = f"Вакансии_{i // chunk_size + 1}"
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            elapsed = time.time() - start_time
            logger.info(f"Excel экспорт завершен за {elapsed:.2f} сек")
            return str(filepath)

        except Exception as e:
            logger.error(f"Ошибка Excel экспорта: {e}")
            return f"Ошибка: {e}"

    def _prepare_chunk_data(self, vacancies: List[Vacancy]) -> List[Dict[str, Any]]:
        """Подготовка данных порциями"""
        data = []
        for vacancy in vacancies:
            salary_from = vacancy.salary.from_amount if vacancy.salary else None
            salary_to = vacancy.salary.to_amount if vacancy.salary else None

            data.append(
                {
                    "ID": vacancy.id,
                    "Название": vacancy.name,
                    "Компания": vacancy.company,
                    "Зарплата от": salary_from,
                    "Зарплата до": salary_to,
                    "Город": vacancy.area,
                    "Опыт": vacancy.experience,
                    "Тип занятости": vacancy.employment,
                    "Ссылка": vacancy.url,
                }
            )
        return data


class CSVExporter:
    def export_to_csv(self, vacancies: List[Vacancy], filename: Optional[str] = None) -> str:
        """Экспорт в CSV с правильной кодировкой"""
        if not vacancies:
            return "Нет данных для экспорта"

        filename = filename or DEFAULT_CSV_FILENAME
        logger.info(f"Экспорт {len(vacancies)} вакансий в CSV")
        start_time = time.time()

        try:
            data = []
            for vacancy in vacancies:
                salary_from = vacancy.salary.from_amount if vacancy.salary else None
                salary_to = vacancy.salary.to_amount if vacancy.salary else None
                currency = vacancy.salary.currency if vacancy.salary else None

                data.append(
                    {
                        "ID": vacancy.id,
                        "Название": vacancy.name,
                        "Компания": vacancy.company,
                        "Зарплата от": salary_from,
                        "Зарплата до": salary_to,
                        "Валюта": currency,
                        "Город": vacancy.area,
                        "Опыт": vacancy.experience,
                        "Тип занятости": vacancy.employment,
                        "Ссылка": vacancy.url,
                        "Источник": vacancy.source,
                    }
                )

            df = pd.DataFrame(data)
            filepath = EXPORTS_DIR / filename
            df.to_csv(filepath, index=False, encoding=CSV_ENCODING, sep=CSV_SEPARATOR)

            elapsed = time.time() - start_time
            logger.info(f"CSV экспорт завершен за {elapsed:.2f} сек")
            return str(filepath)

        except Exception as e:
            logger.error(f"Ошибка CSV экспорта: {e}")
            return f"Ошибка: {e}"


class JSONExporter:
    def export_to_json(self, vacancies: List[Vacancy], filename: Optional[str] = None) -> str:
        """Экспорт вакансий в JSON"""
        if not vacancies:
            return "Нет данных для экспорта"

        filename = filename or DEFAULT_JSON_FILENAME
        logger.info(f"Экспорт {len(vacancies)} вакансий в JSON")
        start_time = time.time()

        try:
            data = [vacancy.to_dict() for vacancy in vacancies]
            filepath = EXPORTS_DIR / filename

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            elapsed = time.time() - start_time
            logger.info(f"JSON экспорт завершен за {elapsed:.2f} сек")
            return str(filepath)

        except Exception as e:
            logger.error(f"Ошибка JSON экспорта: {e}")
            return f"Ошибка: {e}"
