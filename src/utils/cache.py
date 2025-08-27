import hashlib
import json
import logging
import time
from typing import Any, Dict, List, Optional

from config.settings import CACHE_TTL, MAX_CACHE_SIZE
from src.core.models import Vacancy

logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, max_size: int = None, ttl: int = None):
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, float] = {}
        self.max_size = max_size or MAX_CACHE_SIZE
        self.ttl = ttl or CACHE_TTL

    def get(self, key: str) -> Optional[Any]:
        """Получение из кэша"""
        if key in self.cache:
            if time.time() - self.timestamps[key] < self.ttl:
                return self.cache[key]
            else:
                self.delete(key)
        return None

    def set(self, key: str, value: Any) -> None:
        """Сохранение в кэш"""
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            self.delete(oldest_key)

        self.cache[key] = value
        self.timestamps[key] = time.time()

    def delete(self, key: str) -> None:
        """Удаление из кэша"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)


cache = CacheManager()


def get_cached_vacancies(vacancies: List[Vacancy], filters: Dict[str, Any]) -> List[Vacancy]:
    """
    Кэширование результатов фильтрации с автоматическим хэшированием
    """
    cache_key = _generate_cache_key(vacancies, filters)

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    from .filters import VacancyFilter

    filtered = VacancyFilter().apply_filters(vacancies, filters)

    cache.set(cache_key, filtered)

    return filtered


def _generate_cache_key(vacancies: List[Vacancy], filters: Dict[str, Any]) -> str:
    """Генерация ключа кэша"""
    vacancy_ids = "-".join(v.id for v in vacancies[:10])

    filters_str = json.dumps(filters, sort_keys=True)

    combined = f"{vacancy_ids}|{filters_str}"
    return hashlib.md5(combined.encode()).hexdigest()
