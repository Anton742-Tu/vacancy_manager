import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.settings import DEFAULT_VACANCIES_FILE

from .models import Vacancy


class DataManager:
    def __init__(self, data_file: Optional[Path] = None):
        self.data_file = data_file or DEFAULT_VACANCIES_FILE
        self.vacancies: List[Vacancy] = self._load_vacancies()

    def _load_vacancies(self) -> List[Vacancy]:
        """Загрузка вакансий из файла"""
        if not self.data_file.exists():
            return []

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Vacancy.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_vacancies(self) -> None:
        """Сохранение вакансий в файл"""
        data = [vacancy.to_dict() for vacancy in self.vacancies]

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancies(self, new_vacancies: List[Vacancy]) -> int:
        """Добавление новых вакансий с проверкой дубликатов"""
        existing_ids = {vacancy.id for vacancy in self.vacancies}
        vacancies_to_add = [vacancy for vacancy in new_vacancies if vacancy.id not in existing_ids]

        self.vacancies.extend(vacancies_to_add)
        self.save_vacancies()
        return len(vacancies_to_add)

    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаление вакансии по ID"""
        initial_count = len(self.vacancies)
        self.vacancies = [v for v in self.vacancies if v.id != vacancy_id]

        if len(self.vacancies) < initial_count:
            self.save_vacancies()
            return True
        return False

    def clear_all_vacancies(self) -> None:
        """Очистка всех вакансий"""
        self.vacancies = []
        self.save_vacancies()

    def get_vacancy_by_id(self, vacancy_id: str) -> Optional[Vacancy]:
        """Получение вакансии по ID"""
        for vacancy in self.vacancies:
            if vacancy.id == vacancy_id:
                return vacancy
        return None

    def get_all_vacancies(self) -> List[Vacancy]:
        """Получение всех вакансий"""
        return self.vacancies.copy()
