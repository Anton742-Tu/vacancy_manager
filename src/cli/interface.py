import logging
from datetime import datetime
from typing import Any, Dict, List

from config.settings import MESSAGES, EMOJIS, DISPLAY_WIDTH
from src.main import VacancyManager
from src.core.models import Vacancy


# Добавляем логгер
logger = logging.getLogger(__name__)

def display_vacancy(vacancy: Vacancy) -> None:
    """Отображение одной вакансии"""
    salary = vacancy.salary
    salary_str = "Не указана"
    if salary:
        if salary.from_amount and salary.to_amount:
            salary_str = f"{salary.from_amount} - {salary.to_amount} {salary.currency}"
        elif salary.from_amount:
            salary_str = f"от {salary.from_amount} {salary.currency}"
        elif salary.to_amount:
            salary_str = f"до {salary.to_amount} {salary.currency}"

    print(f"\n{EMOJIS['vacancy']} {vacancy.name}")
    print(f"   {EMOJIS['company']} Компания: {vacancy.company}")
    print(f"   {EMOJIS['salary']} Зарплата: {salary_str}")
    print(f"   {EMOJIS['city']} Город: {vacancy.area}")
    print(f"   {EMOJIS['experience']} Опыт: {vacancy.experience}")
    print(f"   {EMOJIS['link']} Ссылка: {vacancy.url}")
    print(f"   {EMOJIS['date']} Опубликована: {vacancy.published_at[:10]}")
    print("-" * DISPLAY_WIDTH)


def display_vacancies(vacancies: List[Vacancy]) -> None:
    """Отображение списка вакансий"""
    if not vacancies:
        print(MESSAGES["no_vacancies"])
        return

    print(f"\n📊 Найдено вакансий: {len(vacancies)}")
    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. ", end="")
        display_vacancy(vacancy)


def get_manual_vacancy_input() -> Dict[str, Any]:
    """Получение данных для ручного добавления вакансии"""
    print("\n📝 Добавление вакансии вручную")
    print("=" * 50)

    vacancy_data: Dict[str, Any] = {
        "name": input("Название вакансии: ").strip(),
        "company": input("Компания: ").strip(),
        "area": input("Город: ").strip(),
        "url": input("Ссылка на вакансию: ").strip(),
        "experience": input("Требуемый опыт: ").strip(),
        "employment": input("Тип занятости: ").strip(),
        "snippet": input("Описание: ").strip(),
        "published_at": datetime.now().isoformat(),
        "salary": {},
    }

    # Данные о зарплате
    salary_from = input("Зарплата от (или Enter чтобы пропустить): ").strip()
    salary_to = input("Зарплата до (или Enter чтобы пропустить): ").strip()
    currency = input("Валюта (RUB/USD/EUR, по умолчанию RUB): ").strip() or "RUB"

    if salary_from:
        vacancy_data["salary"]["from"] = int(salary_from)
    if salary_to:
        vacancy_data["salary"]["to"] = int(salary_to)
    vacancy_data["salary"]["currency"] = currency

    return vacancy_data


def run_cli() -> None:
    """Запуск CLI интерфейса"""
    print(MESSAGES["welcome"])
    print("=" * DISPLAY_WIDTH)

    manager = VacancyManager()

    while True:
        print("\n" + "=" * DISPLAY_WIDTH)
        print("🎯 МЕНЕДЖЕР ВАКАНСИЙ HH.RU")
        print("=" * DISPLAY_WIDTH)
        print(f"1. {EMOJIS['search']} Поиск и добавление вакансий с hh.ru")
        print(f"2. {EMOJIS['add']} Добавить вакансию вручную")
        print(f"3. {EMOJIS['view']} Показать все вакансии")
        print(f"4. {EMOJIS['filter']} Фильтровать вакансии")
        print(f"5. {EMOJIS['delete']} Удалить вакансию")
        print(f"6. {EMOJIS['export']} Экспорт в Excel")
        print(f"7. {EMOJIS['export']} Экспорт в CSV")
        print(f"8. {EMOJIS['export']} Экспорт в JSON")
        print(f"9. {EMOJIS['stats']} Статистика")
        print(f"10. {EMOJIS['clear']} Очистить все вакансии")
        print(f"11. {EMOJIS['exit']} Выход")
        print("=" * DISPLAY_WIDTH)

        choice = input("Выберите действие (1-11): ").strip()

        if choice == "1":
            try:
                query = input("Введите поисковый запрос (например 'Python developer'): ").strip()
                if not query:
                    print("❌ Запрос не может быть пустым!")
                    continue

                count_input = input("Количество вакансий (по умолчанию 20, макс 100): ").strip()
                count = min(int(count_input) if count_input.isdigit() else 20, 100)

                print(f"{EMOJIS['search']} Поиск вакансий '{query}'...")
                added_count = manager.search_and_add_vacancies(query, count)

                if added_count == 0:
                    print("⚠️  Не найдено новых вакансий. Попробуйте другой запрос.")
                else:
                    print(f"✅ Добавлено {added_count} новых вакансий")

            except Exception as e:
                # Исправляем здесь: используем logger вместо input.error
                logger.error(f"Ошибка при поиске вакансий: {e}")
                print(MESSAGES["error_api"].format(e))
                print("💡 Попробуйте другой поисковый запрос или проверьте соединение с интернетом")

        elif choice == "2":
            try:
                vacancy_data = get_manual_vacancy_input()
                success = manager.add_manual_vacancy(vacancy_data)
                if success:
                    print(MESSAGES["vacancy_added"])
                else:
                    print("❌ Ошибка при добавлении вакансии")
            except Exception as e:
                logger.error(f"Ошибка при добавлении вакансии: {e}")
                print(MESSAGES["error_general"].format(e))

        elif choice == "3":
            vacancies: List[Vacancy] = manager.get_vacancies()
            display_vacancies(vacancies)

        elif choice == "4":
            print("\n🎛️  Фильтрация вакансий (оставьте поле пустым чтобы пропустить)")
            filters: Dict[str, Any] = {}

            company = input("Компания: ").strip()
            if company:
                filters["company"] = company

            area = input("Город: ").strip()
            if area:
                filters["area"] = area

            min_salary = input("Минимальная зарплата: ").strip()
            if min_salary and min_salary.isdigit():
                filters["min_salary"] = int(min_salary)

            experience = input("Опыт работы: ").strip()
            if experience:
                filters["experience"] = experience

            employment = input("Тип занятости: ").strip()
            if employment:
                filters["employment"] = employment

            filtered_results: List[Vacancy] = manager.get_vacancies(filters)
            display_vacancies(filtered_results)

        elif choice == "5":
            all_vacancies: List[Vacancy] = manager.get_vacancies()  # Меняем имя переменной
            if not all_vacancies:
                print("❌ Нет вакансий для удаления")
                continue

            display_vacancies(all_vacancies)
            try:
                idx_input = input("\nНомер вакансии для удаления: ").strip()
                if not idx_input.isdigit():
                    print("❌ Введите число!")
                    continue

                idx = int(idx_input) - 1
                if 0 <= idx < len(all_vacancies):
                    vacancy_id = all_vacancies[idx].id
                    if manager.delete_vacancy(vacancy_id):
                        print(MESSAGES["vacancy_deleted"])
                    else:
                        print("❌ Вакансия не найдена!")
                else:
                    print("❌ Неверный номер!")
            except ValueError:
                print("❌ Введите корректное число!")

        elif choice == "6":
            try:
                filename = input("Имя файла (по умолчанию vacancies.xlsx): ").strip()
                filename = filename if filename else "vacancies.xlsx"

                if not filename.endswith(".xlsx"):
                    filename += ".xlsx"

                filepath = manager.export_to_excel(filename)
                print(MESSAGES["export_success"].format(filepath))
            except Exception as e:
                print(MESSAGES["error_export"].format(e))

        elif choice == "7":
            try:
                filename = input("Имя файла (по умолчанию vacancies.csv): ").strip()
                filename = filename if filename else "vacancies.csv"
                filepath = manager.export_to_csv(filename)
                print(MESSAGES["export_success"].format(filepath))
                print("💡 Совет: Откройте файл в Excel с указанием кодировки UTF-8")
            except Exception as e:
                print(MESSAGES["error_export"].format(e))

        elif choice == "8":
            try:
                filename = input("Имя файла (по умолчанию vacancies.json): ").strip()
                filename = filename if filename else "vacancies.json"
                filepath = manager.export_to_json(filename)
                print(MESSAGES["export_success"].format(filepath))
            except Exception as e:
                print(MESSAGES["error_export"].format(e))

        elif choice == "9":
            stats = manager.get_statistics()
            if not stats:
                print("❌ Нет данных для статистики")
                continue

            print("\n📊 СТАТИСТИКА ВАКАНСИЙ")
            print("=" * 40)
            print(f"Всего вакансий: {stats['total']}")
            print(f"С указанной зарплата: {stats['with_salary']}")
            print(f"Источники: {dict(stats['sources'])}")

            print("\n🏢 Топ компаний:")
            for company, count in stats["by_company"].most_common(5):
                print(f"  {company}: {count}")

            print("\n📍 Топ городов:")
            for area, count in stats["by_area"].most_common(5):
                print(f"  {area}: {count}")

        elif choice == "10":
            confirm = input("❌ Вы уверены? Это удалит ВСЕ вакансии! (y/n): ").strip().lower()
            if confirm == "y":
                manager.clear_all_vacancies()
                print(MESSAGES["all_cleared"])
            else:
                print("Отменено")

        elif choice == "11":
            print("👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор! Попробуйте снова.")

        # Пауза перед следующим шагом
        input("\nНажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    run_cli()
