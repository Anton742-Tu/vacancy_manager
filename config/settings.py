from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

# Пути к файлам
DATA_DIR = BASE_DIR / 'data'
EXPORTS_DIR = DATA_DIR / 'exports'

# Создаем директории если их нет
DATA_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# Настройки API
HH_API_BASE_URL = "https://api.hh.ru/vacancies"
HH_API_TIMEOUT = 10
HH_API_AREA_RUSSIA = 113

# Настройки приложения
DEFAULT_VACANCIES_FILE = DATA_DIR / "vacancies.json"
DEFAULT_EXPORT_FILE = EXPORTS_DIR / "vacancies.xlsx"
MAX_VACANCIES_PER_REQUEST = 100

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOG_LEVEL = logging.INFO
LOG_FILE = LOG_DIR / 'vacancy_manager.log'

# Настройка логирования
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
