# UI использует BLL (бизнес-логику)
from bll import ContentService
import sys

# Уровень UI (представления) [cite: 11]
# Вся "грязная" работа с вводом/выводом здесь
def main():
    service = ContentService()

    while True:
        print("\n--- 📖 Библиотека Контента  ---")
        print("1. Добавить новый контент")
        print("2. Показать весь контент")
        print("3. Найти контент")
        print("4. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            add_content(service)
        elif choice == '2':
            list_all_content(service)
        elif choice == '3':
            search_content(service)
        elif choice == '4':
            print("Выход...")
            sys.exit()
        else:
            print("Неверный ввод.")

def add_content(service):
    title = input("Введите название: ")
    format_ = input("Введите формат (Книга, Видео, ...): ")
    location = input("Введите локацию (URL, Полка 5, ...): ")
    
    try:
        service.add_content(title, format_, location)
        print("Успешно добавлено!")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

def list_all_content(service):
    print("\n--- Весь контент ---")
    try:
        items = service.get_all_content()
        if not items:
            print("Библиотека пуста.")
        for item in items:
            print(f"[ID: {item.id}] {item.title} ({item.format}) - {item.location}")
    except Exception as e:
        print(f"Не удалось получить данные: {e}")

def search_content(service):
    query = input("Введите поисковый запрос (по названию или формату): ")
    try:
        items = service.search_content(query)
        print(f"\n--- Результаты поиска по '{query}' ---")
        if not items:
            print("Ничего не найдено.")
        for item in items:
            print(f"[ID: {item.id}] {item.title} ({item.format}) - {item.location}")
    except Exception as e:
        print(f"Ошибка поиска: {e}")

# Точка входа в программу
if __name__ == "__main__":
    main()