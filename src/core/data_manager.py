import json
import logging
import time
from pathlib import Path
from typing import List, Optional, Set

from config.settings import VACANCIES_FILE

from .models import Vacancy

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, data_file: Optional[Path] = None):
        self.data_file = data_file or VACANCIES_FILE
        self.vacancies: List[Vacancy] = []
        self._vacancy_ids: Set[str] = set()
        self._load_vacancies()

    def _load_vacancies(self) -> None:
        """Быстрая загрузка вакансий"""
        if not self.data_file.exists():
            logger.info("Файл вакансий не существует, создаем новый")
            return

        logger.info(f"Загрузка вакансий из {self.data_file}")
        start_time = time.time()  # Теперь правильно!

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.vacancies = []
            self._vacancy_ids.clear()

            for item in data:
                try:
                    vacancy = Vacancy.from_dict(item)
                    self.vacancies.append(vacancy)
                    self._vacancy_ids.add(vacancy.id)
                except Exception as e:
                    logger.warning(f"Ошибка загрузки вакансии: {e}")
                    continue

            elapsed = time.time() - start_time
            logger.info(f"Загружено {len(self.vacancies)} вакансий за {elapsed:.2f} сек")

        except json.JSONDecodeError:
            logger.error("Файл вакансий поврежден, создаем новый")
            self.vacancies = []
            self._vacancy_ids.clear()
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла: {e}")
            self.vacancies = []
            self._vacancy_ids.clear()

    def save_vacancies(self) -> None:
        """Оптимизированное сохранение"""
        if not self.vacancies:
            logger.info("Нет вакансий для сохранения")
            return

        logger.info(f"Сохранение {len(self.vacancies)} вакансий")
        start_time = time.time()

        try:
            # Создаем директорию если не существует
            self.data_file.parent.mkdir(parents=True, exist_ok=True)

            data = [vacancy.to_dict() for vacancy in self.vacancies]
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            elapsed = time.time() - start_time
            logger.info(f"Сохранено за {elapsed:.2f} сек")

        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")

    def add_vacancies(self, new_vacancies: List[Vacancy]) -> int:
        """Быстрое добавление с проверкой дубликатов"""
        if not new_vacancies:
            return 0

        vacancies_to_add = [vacancy for vacancy in new_vacancies if vacancy.id not in self._vacancy_ids]

        if not vacancies_to_add:
            logger.info("Все вакансии уже существуют, новых не добавлено")
            return 0

        logger.info(f"Добавление {len(vacancies_to_add)} новых вакансий")

        # Добавляем в память
        for vacancy in vacancies_to_add:
            self.vacancies.append(vacancy)
            self._vacancy_ids.add(vacancy.id)

        # Сохраняем
        self.save_vacancies()

        return len(vacancies_to_add)

    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаление вакансии по ID"""
        if vacancy_id not in self._vacancy_ids:
            return False

        self.vacancies = [v for v in self.vacancies if v.id != vacancy_id]
        self._vacancy_ids.remove(vacancy_id)
        self.save_vacancies()
        return True

    def clear_all_vacancies(self) -> None:
        """Очистка всех вакансий"""
        self.vacancies = []
        self._vacancy_ids.clear()

        if self.data_file.exists():
            try:
                self.data_file.unlink()
                logger.info("Файл вакансий удален")
            except Exception as e:
                logger.error(f"Ошибка удаления файла: {e}")
        else:
            logger.info("Файл вакансий не существует")

    def get_vacancy_by_id(self, vacancy_id: str) -> Optional[Vacancy]:
        """Получение вакансии по ID"""
        for vacancy in self.vacancies:
            if vacancy.id == vacancy_id:
                return vacancy
        return None

    def get_all_vacancies(self) -> List[Vacancy]:
        """Получение всех вакансий"""
        return self.vacancies.copy()
