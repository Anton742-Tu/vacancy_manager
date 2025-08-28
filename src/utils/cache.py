import logging
import time
from functools import lru_cache
from typing import Any, Dict, List, Optional

from config.settings import CACHE_TTL, MAX_CACHE_SIZE

logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, max_size: Optional[int] = None, ttl: Optional[int] = None):
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


@lru_cache(maxsize=100)
def get_cached_vacancies(filters_hash: str, all_vacancies: tuple) -> List[Any]:
    """
    Кэширование результатов фильтрации

    Args:
        filters_hash: хэш фильтров для идентификации
        all_vacancies: кортеж вакансий (tuple для хэширования)
    """
    # Эта функция требует реализации логики фильтрации
    # Пока возвращаем пустой список
    return []


def generate_filters_hash(filters: Dict[str, Any]) -> str:
    """Генерация хэша для фильтров"""
    import hashlib
    import json

    filters_str = json.dumps(filters, sort_keys=True)
    return hashlib.md5(filters_str.encode()).hexdigest()
