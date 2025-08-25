import pandas as pd
from typing import List
from pathlib import Path

from ..core.models import Vacancy
from config.settings import EXPORTS_DIR


class ExcelExporter:
    @staticmethod
    def export_to_excel(vacancies: List[Vacancy], filename: str = "vacancies.xlsx") -> str:
        """Экспорт вакансий в Excel"""
        data = []

        for vacancy in vacancies:
            salary_from = vacancy.salary.from_amount if vacancy.salary else None
            salary_to = vacancy.salary.to_amount if vacancy.salary else None
            currency = vacancy.salary.currency if vacancy.salary else None

            data.append({
                'ID': vacancy.id,
                'Название': vacancy.name,
                'Компания': vacancy.company,
                'Зарплата от': salary_from,
                'Зарплата до': salary_to,
                'Валюта': currency,
                'Город': vacancy.area,
                'Опыт': vacancy.experience,
                'Тип занятости': vacancy.employment,
                'Ссылка': vacancy.url,
                'Источник': vacancy.source
            })

        df = pd.DataFrame(data)
        filepath = EXPORTS_DIR / filename
        df.to_excel(filepath, index=False)
        return str(filepath)


class JSONExporter:
    @staticmethod
    def export_to_json(vacancies: List[Vacancy], filename: str = "vacancies_export.json") -> str:
        """Экспорт вакансий в JSON"""
        data = [vacancy.to_dict() for vacancy in vacancies]
        filepath = EXPORTS_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(filepath)
