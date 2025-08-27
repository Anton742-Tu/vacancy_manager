from typing import Any, Dict

from config.settings import DISPLAY_WIDTH, EMOJIS, MESSAGES
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

    print(f"\n{EMOJIS['vacancy']} {vacancy.name}")
    print(f"   {EMOJIS['company']} Компания: {vacancy.company}")
    print(f"   {EMOJIS['salary']} Зарплата: {salary_str}")
    print(f"   {EMOJIS['city']} Город: {vacancy.area}")
    print(f"   {EMOJIS['experience']} Опыт: {vacancy.experience}")
    print(f"   {EMOJIS['link']} Ссылка: {vacancy.url}")
    print(f"   {EMOJIS['date']} Опубликована: {vacancy.published_at[:10]}")
    print("-" * DISPLAY_WIDTH)


def display_vacancies(vacancies) -> None:
    """Отображение списка вакансий"""
    if not vacancies:
        print(MESSAGES["no_vacancies"])
        return

    print(f"\n📊 Найдено вакансий: {len(vacancies)}")
    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. ", end="")
        display_vacancy(vacancy)


def get_manual_vacancy_input():
    pass


def run_cli():
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
                print(f"✅ Добавлено {added_count} новых вакансий")

            except Exception as e:
                print(MESSAGES["error_api"].format(e))

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

            filtered_vacancies = manager.get_vacancies(filters)
            display_vacancies(filtered_vacancies)

        elif choice == "5":
            vacancies = manager.get_vacancies()
            if not vacancies:
                print("❌ Нет вакансий для удаления")
                continue

            display_vacancies(vacancies)
            try:
                idx_input = input("\nНомер вакансии для удаления: ").strip()
                if not idx_input.isdigit():
                    print("❌ Введите число!")
                    continue

                idx = int(idx_input) - 1
                if 0 <= idx < len(vacancies):
                    vacancy_id = vacancies[idx].id
                    if manager.delete_vacancy(vacancy_id):
                        print("✅ Вакансия удалена!")
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
                print(f"✅ Данные экспортированы в: {filepath}")
            except Exception as e:
                print(f"❌ Ошибка при экспорте: {e}")

        elif choice == "7":
            try:
                filename = input("Имя файла (по умолчанию vacancies.csv): ").strip()
                filename = filename if filename else "vacancies.csv"
                filepath = manager.export_to_csv(filename)
                print(f"✅ Данные экспортированы в CSV: {filepath}")
                print("💡 Совет: Откройте файл в Excel с указанием кодировки UTF-8")
            except Exception as e:
                print(f"❌ Ошибка при экспорте в CSV: {e}")

        elif choice == "8":
            try:
                filename = input("Имя файла (по умолчанию vacancies.json): ").strip()
                filename = filename if filename else "vacancies.json"
                filepath = manager.export_to_json(filename)
                print(f"✅ Данные экспортированы в JSON: {filepath}")
            except Exception as e:
                print(f"❌ Ошибка при экспорте в JSON: {e}")

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
                print("✅ Все вакансии удалены!")
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
