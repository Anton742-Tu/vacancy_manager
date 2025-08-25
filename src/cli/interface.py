import json
from datetime import datetime
from typing import Any, Dict

from config.settings import DEFAULT_VACANCIES_FILE
from src.main import VacancyManager


def display_vacancy(vacancy) -> None:
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

    print(f"\n📋 {vacancy.name}")
    print(f"   🏢 Компания: {vacancy.company}")
    print(f"   💰 Зарплата: {salary_str}")
    print(f"   📍 Город: {vacancy.area}")
    print(f"   🎯 Опыт: {vacancy.experience}")
    print(f"   🔗 Ссылка: {vacancy.url}")
    print(f"   📅 Опубликована: {vacancy.published_at[:10]}")
    print("-" * 60)


def display_vacancies(vacancies) -> None:
    """Отображение списка вакансий"""
    if not vacancies:
        print("❌ Нет вакансий для отображения")
        return

    print(f"\n📊 Найдено вакансий: {len(vacancies)}")
    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. ", end="")
        display_vacancy(vacancy)


def get_manual_vacancy_input() -> Dict[str, Any]:
    """Получение данных для ручного добавления вакансии"""
    print("\n📝 Добавление вакансии вручную")
    print("=" * 50)

    vacancy_data = {
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


def run_cli():
    """Запуск CLI интерфейса"""
    print("🚀 Запуск менеджера вакансий HH.ru")
    print("=" * 50)

    manager = VacancyManager()

    while True:
        print("\n" + "=" * 60)
        print("🎯 МЕНЕДЖЕР ВАКАНСИЙ HH.RU")
        print("=" * 60)
        print("1. 🔍 Поиск и добавление вакансий с hh.ru")
        print("2. 📝 Добавить вакансию вручную")
        print("3. 👀 Показать все вакансии")
        print("4. 🎛️  Фильтровать вакансии")
        print("5. ❌ Удалить вакансию")
        print("6. 💾 Экспорт в Excel")
        print("7. 📊 Статистика")
        print("8. 🗑️  Очистить все вакансии")
        print("9. 🚪 Выход")
        print("=" * 60)

        choice = input("Выберите действие (1-9): ").strip()

        if choice == "1":
            try:
                query = input("Введите поисковый запрос (например 'Python developer'): ").strip()
                if not query:
                    print("❌ Запрос не может быть пустым!")
                    continue

                count_input = input("Количество вакансий (по умолчанию 20, макс 100): ").strip()
                count = min(int(count_input) if count_input.isdigit() else 20, 100)

                print(f"🔍 Поиск вакансий '{query}'...")
                added_count = manager.search_and_add_vacancies(query, count)
                print(f"✅ Добавлено {added_count} новых вакансий")

            except Exception as e:
                print(f"❌ Ошибка при поиске вакансий: {e}")

        elif choice == "2":
            try:
                vacancy_data = get_manual_vacancy_input()
                success = manager.add_manual_vacancy(vacancy_data)
                if success:
                    print("✅ Вакансия успешно добавлена!")
                else:
                    print("❌ Ошибка при добавлении вакансии")
            except Exception as e:
                print(f"❌ Ошибка: {e}")

        elif choice == "3":
            vacancies = manager.get_vacancies()
            display_vacancies(vacancies)

        elif choice == "4":
            print("\n🎛️  Фильтрация вакансий (оставьте поле пустым чтобы пропустить)")
            filters = {}

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

            filtered_vacancies = manager.get_vacancies(filters)
            display_vacancies(filtered_vacancies)

        elif choice == "5":
            vacancies = manager.get_vacancies()
            if not vacancies:
                print("❌ Нет вакансий для удаления")
                continue

            display_vacancies(vacancies)
            try:
                idx = int(input("\nНомер вакансии для удаления: ")) - 1
                if 0 <= idx < len(vacancies):
                    vacancy_id = vacancies[idx].id
                    if manager.delete_vacancy(vacancy_id):
                        print("✅ Вакансия удалена!")
                    else:
                        print("❌ Вакансия не найдена!")
                else:
                    print("❌ Неверный номер!")
            except ValueError:
                print("❌ Введите число!")

        elif choice == "6":
            try:
                filename = input("Имя файла (по умолчанию vacancies.xlsx): ").strip()
                filename = filename if filename else "vacancies.xlsx"

                if not filename.endswith(".xlsx"):
                    filename += ".xlsx"

                filepath = manager.export_to_excel(filename)
                print(f"✅ Данные экспортированы в: {filepath}")
            except Exception as e:
                print(f"❌ Ошибка при экспорте: {e}")

        elif choice == "7":
            stats = manager.get_statistics()
            if not stats:
                print("❌ Нет данных для статистики")
                continue

            print("\n📊 СТАТИСТИКА ВАКАНСИЙ")
            print("=" * 40)
            print(f"Всего вакансий: {stats['total']}")
            print(f"С указанной зарплатой: {stats['with_salary']}")
            print(f"Источники: {dict(stats['sources'])}")

            print("\n🏢 Топ компаний:")
            for company, count in stats["by_company"].most_common(5):
                print(f"  {company}: {count}")

            print("\n📍 Топ городов:")
            for area, count in stats["by_area"].most_common(5):
                print(f"  {area}: {count}")

        elif choice == "8":
            confirm = input("❌ Вы уверены? Это удалит ВСЕ вакансии! (y/n): ").strip().lower()
            if confirm == "y":
                manager.clear_all_vacancies()
                print("✅ Все вакансии удалены!")
            else:
                print("Отменено")

        elif choice == "9":
            print("👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор! Попробуйте снова.")

        # Пауза перед следующим шагом
        input("\nНажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    run_cli()
