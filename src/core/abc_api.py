from abc import ABC, abstractmethod
from typing import List

from .models import Vacancy


class BaseAPIClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, query: str, **kwargs) -> List[Vacancy]:
        """Получение вакансий по запросу"""
        pass
