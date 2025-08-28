from abc import ABC, abstractmethod
from typing import List, Optional

from .models import Vacancy


class BaseStorage(ABC):
    """Абстрактный базовый класс для хранения данных вакансий"""

    @abstractmethod
    def load_data(self) -> List[Vacancy]:
        """Загрузка данных из хранилища"""
        pass

    @abstractmethod
    def save_data(self, data: Optional[List[Vacancy]] = None) -> None:
        """Сохранение данных в хранилище"""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """Добавление одной вакансии"""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Vacancy]:
        """Получение всех вакансий"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаление вакансии по ID"""
        pass
