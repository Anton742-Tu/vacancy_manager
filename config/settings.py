from pathlib import Path
from typing import Dict


# Пути и директории
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = DATA_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"

# Файлы
VACANCIES_FILE = DATA_DIR / "vacancies.json"
LOG_FILE = LOGS_DIR / "vacancy_manager.log"

# API настройки
HH_API_BASE_URL = "https://api.hh.ru/vacancies"
HH_API_TIMEOUT = 30
HH_API_AREA_RUSSIA = 113  # Код России в HH API
HH_API_USER_AGENT = "VacancyManager/1.0 (Tumashovster@Gmail.com)"

# Настройки логирования
LOG_LEVEL = "INFO"  # Можете изменить на "DEBUG" для детального логирования
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Лимиты
MAX_VACANCIES_PER_REQUEST = 100
MAX_CACHE_SIZE = 1000
CACHE_TTL = 300  # 5 минут в секундах

# Настройки экспорта
DEFAULT_EXCEL_FILENAME = "vacancies.xlsx"
DEFAULT_CSV_FILENAME = "vacancies.csv"
DEFAULT_JSON_FILENAME = "vacancies_export.json"
CSV_SEPARATOR = ";"
CSV_ENCODING = "utf-8-sig"

# Настройки отображения
DISPLAY_WIDTH = 60
TRUNCATE_TEXT_LENGTH = 200

# Сообщения и тексты
MESSAGES: Dict[str, str] = {
    "welcome": "🚀 Запуск менеджера вакансий HH.ru",
    "no_vacancies": "❌ Нет вакансий для отображения",
    "vacancy_added": "✅ Вакансия успешно добавлена!",
    "vacancy_deleted": "✅ Вакансия удалена!",
    "all_cleared": "✅ Все вакансии удалены!",
    "export_success": "✅ Данные экспортированы в: {}",
    "error_general": "❌ Ошибка: {}",
    "error_api": "❌ Ошибка при запросе к API: {}",
    "error_export": "❌ Ошибка при экспорте: {}",
}

# Эмодзи и символы для CLI
EMOJIS: Dict[str, str] = {
    "vacancy": "📋",
    "company": "🏢",
    "salary": "💰",
    "city": "📍",
    "experience": "🎯",
    "link": "🔗",
    "date": "📅",
    "search": "🔍",
    "add": "📝",
    "view": "👀",
    "filter": "🎛️",
    "delete": "❌",
    "export": "💾",
    "stats": "📊",
    "clear": "🗑️",
    "exit": "🚪",
}

# Создание необходимых директорий
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
