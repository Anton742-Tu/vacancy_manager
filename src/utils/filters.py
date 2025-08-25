from typing import Callable, List, Optional

from ..core.models import Vacancy


class VacancyFilter:
    @staticmethod
    def filter_by_company(vacancies: List[Vacancy], company_name: str) -> List[Vacancy]:
        """Фильтрация по компании"""
        return [v for v in vacancies if company_name.lower() in v.company.lower()]

    @staticmethod
    def filter_by_area(vacancies: List[Vacancy], area: str) -> List[Vacancy]:
        """Фильтрация по городу"""
        return [v for v in vacancies if area.lower() in v.area.lower()]

    @staticmethod
    def filter_by_min_salary(vacancies: List[Vacancy], min_salary: int) -> List[Vacancy]:
        """Фильтрация по минимальной зарплате"""

        def has_min_salary(vacancy: Vacancy) -> bool:
            if not vacancy.salary:
                return False

            salary = vacancy.salary
            if salary.from_amount and salary.from_amount >= min_salary:
                return True
            if salary.to_amount and salary.to_amount >= min_salary:
                return True
            return False

        return list(filter(has_min_salary, vacancies))

    @staticmethod
    def filter_by_experience(vacancies: List[Vacancy], experience: str) -> List[Vacancy]:
        """Фильтрация по опыту"""
        return [v for v in vacancies if experience.lower() in v.experience.lower()]

    @staticmethod
    def filter_by_employment(vacancies: List[Vacancy], employment: str) -> List[Vacancy]:
        """Фильтрация по типу занятости"""
        return [v for v in vacancies if employment.lower() in v.employment.lower()]

    @staticmethod
    def filter_by_custom(vacancies: List[Vacancy], filter_func: Callable[[Vacancy], bool]) -> List[Vacancy]:
        """Пользовательская фильтрация"""
        return list(filter(filter_func, vacancies))
