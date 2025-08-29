# src/core/data_manager.py
import json
import logging
import time
from pathlib import Path
from typing import List, Optional, Set

from config.settings import VACANCIES_FILE

from .abc_storage import BaseStorage
from .models import Vacancy

logger = logging.getLogger(__name__)


class DataManager(BaseStorage):
    def __init__(self, data_file: Optional[Path] = None):
        self._data_file = data_file or VACANCIES_FILE
        self.vacancies: List[Vacancy] = []
        self._vacancy_ids: Set[str] = set()
        self._load_vacancies()

    def _load_vacancies(self) -> None:
        """Приватный метод загрузки вакансий"""
        if not self._data_file.exists():
            logger.info("Файл вакансий не существует, создаем новый")
            return

        logger.info(f"Загрузка вакансий из {self._data_file}")
        start_time = time.time()

        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
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

    def load_data(self) -> List[Vacancy]:
        """Загрузка данных из хранилища"""
        return self.vacancies.copy()

    def save_data(self, data: Optional[List[Vacancy]] = None) -> None:
        """Сохранение данных в хранилище"""
        vacancies_to_save = data if data is not None else self.vacancies

        if not vacancies_to_save:
            logger.info("Нет вакансий для сохранения")
            return

        logger.info(f"Сохранение {len(vacancies_to_save)} вакансий")
        start_time = time.time()

        try:
            # Создаем директорию если не существует
            self._data_file.parent.mkdir(parents=True, exist_ok=True)

            data_to_save = [vacancy.to_dict() for vacancy in vacancies_to_save]
            with open(self._data_file, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)

            elapsed = time.time() - start_time
            logger.info(f"Сохранено за {elapsed:.2f} сек")

        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> bool:
        """Добавление одной вакансии"""
        if vacancy.id in self._vacancy_ids:
            logger.info(f"Вакансия {vacancy.id} уже существует")
            return False

        try:
            self.vacancies.append(vacancy)
            self._vacancy_ids.add(vacancy.id)
            self.save_data()  # Сохраняем текущее состояние
            logger.info(f"Добавлена вакансия: {vacancy.id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка добавления вакансии: {e}")
            return False

    def get_all_vacancies(self) -> List[Vacancy]:
        """Получение всех вакансий"""
        return self.vacancies.copy()

    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаление вакансии по ID"""
        if vacancy_id not in self._vacancy_ids:
            return False

        try:
            self.vacancies = [v for v in self.vacancies if v.id != vacancy_id]
            self._vacancy_ids.remove(vacancy_id)
            self.save_data()  # Сохраняем текущее состояние
            logger.info(f"Удалена вакансия: {vacancy_id}")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления вакансии: {e}")
            return False

    # Старые методы для обратной совместимости
    def add_vacancies(self, new_vacancies: List[Vacancy]) -> int:
        """Добавление списка вакансий (для обратной совместимости)"""
        added_count = 0
        for vacancy in new_vacancies:
            if self.add_vacancy(vacancy):
                added_count += 1
        return added_count

    def clear_all_vacancies(self) -> None:
        """Очистка всех вакансий (для обратной совместимости)"""
        self.vacancies = []
        self._vacancy_ids.clear()
        self.save_data()  # Сохраняем пустое состояние

        if self._data_file.exists():
            try:
                self._data_file.unlink()
                logger.info("Файл вакансий удален")
            except Exception as e:
                logger.error(f"Ошибка удаления файла: {e}")
        else:
            logger.info("Файл вакансий не существует")
