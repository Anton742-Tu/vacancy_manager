import pandas as pd
import json
from typing import List, Any, cast
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from ..core.models import Vacancy
from config.settings import EXPORTS_DIR


class ExcelExporter:
    def __init__(self):
        pass

    def export_to_excel(self, vacancies: List[Vacancy], filename: str = "vacancies.xlsx") -> str:
        """Экспорт вакансий в Excel с правильной кодировкой"""
        data: List[Dict[str, Any]] = []

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
                'Источник': vacancy.source,
                'Дата публикации': vacancy.published_at[:10] if vacancy.published_at else ''
            })

        # Создаем DataFrame
        df = pd.DataFrame(data)

        # Убеждаемся, что все строковые колонки в UTF-8
        for column in df.select_dtypes(include=['object']).columns:
            df[column] = df[column].astype(str).str.encode('utf-8').str.decode('utf-8')

        filepath = EXPORTS_DIR / filename

        # Используем ExcelWriter с движком openpyxl и настройками
        with pd.ExcelWriter(
                filepath,
                engine='openpyxl',
                engine_kwargs={'options': {'strings_to_urls': False}}
        ) as writer:
            df.to_excel(writer, sheet_name='Вакансии', index=False)

            # Получаем worksheet для форматирования
            worksheet = writer.sheets['Вакансии']

            # Настраиваем ширину колонок
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except (ValueError, TypeError, AttributeError) as e:
                        print(f"Ошибка при обработке ячейки: {e}")
                        continue

                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

            # Жирный шрифт для заголовков
            for cell in worksheet[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')

        return str(filepath)


class CSVExporter:
    def __init__(self):
        pass

    def export_to_csv(self, vacancies: List[Vacancy], filename: str = "vacancies.csv") -> str:
        """Экспорт в CSV с правильной кодировкой"""
        data: List[Dict[str, Any]] = []

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

        # Сохраняем с явным указанием кодировки и разделителя
        df.to_csv(
            filepath,
            index=False,
            encoding='utf-8-sig',
            sep=';'
        )

        return str(filepath)


class JSONExporter:
    def __init__(self):
        pass

    def export_to_json(self, vacancies: List[Vacancy], filename: str = "vacancies_export.json") -> str:
        """Экспорт вакансий в JSON"""
        data = [vacancy.to_dict() for vacancy in vacancies]
        filepath = EXPORTS_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return str(filepath)
