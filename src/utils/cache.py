import logging
import time
from functools import lru_cache
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, float] = {}
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds

    def get(self, key: str) -> Optional[Any]:
        """Получение из кэша"""
        if key in self.cache:
            if time.time() - self.timestamps[key] < self.ttl:
                return self.cache[key]
            else:
                # Удаляем просроченный кэш
                self.delete(key)
        return None

    def set(self, key: str, value: Any) -> None:
        """Сохранение в кэш"""
        if len(self.cache) >= self.max_size:
            # Удаляем самый старый элемент
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            self.delete(oldest_key)

        self.cache[key] = value
        self.timestamps[key] = time.time()

    def delete(self, key: str) -> None:
        """Удаление из кэша"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)


# Использование в main.py
cache = CacheManager()


@lru_cache(maxsize=100)
def get_cached_vacancies(filters_hash: str):
    """Кэширование результатов фильтрации"""
    # ... логика фильтрации ...
