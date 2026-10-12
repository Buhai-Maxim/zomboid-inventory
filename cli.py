import argparse
from storage import CSVDataReader, InventoryManager

def main():
    parser = argparse.ArgumentParser(description="Zomboid Inventory Management CLI")
    parser.add_argument("--file", default="items.csv", help="Шлях до файлу даних")
    
    subparsers = parser.add_subparsers(dest="command", help="Доступні команди")

    # Команда перегляду з пагінацією
    page_parser = subparsers.add_parser("list", help="Посторінковий перегляд предметів")
    page_parser.add_argument("--page", type=int, default=1, help="Номер сторінки")
    page_parser.add_argument("--size", type=int, default=5, help="Кількість на сторінці")

    # Пошук по ID
    id_parser = subparsers.add_parser("get-id", help="Знайти предмет за ID")
    id_parser.add_argument("id", type=int, help="ID предмета")

    # Пошук за назвою
    search_parser = subparsers.add_parser("search", help="Пошук предметів за назвою")
    search_parser.add_argument("name", type=str, help="Назва або частина назви")

    # Статистика відсотків
    stats_parser = subparsers.add_parser("stats", help="Відсоткове відношення стану предметів")
    stats_parser.add_argument("--name", type=str, default=None, help="Назва конкретного предмета")

    args = parser.parse_args()

    manager = InventoryManager(CSVDataReader())
    try:
        manager.load(args.file)
    except FileNotFoundError:
        print(f"Помилка: Файл '{args.file}' не знайдено.")
        return

    if args.command == "list":
        items = manager.get_page(args.page, args.size)
        print(f"--- Предмети (Сторінка {args.page}) ---")
        for item in items:
            print(f"ID: {item['ID']} | {item['Name']} ({item['Type']}) | Стан: {item['Condition']} | Кількість: {item['Amount']}")

    elif args.command == "get-id":
        item = manager.get_by_id(args.id)
        if item:
            print(f"Знайдено: {item}")
        else:
            print(f"Предмет з ID {args.id} не знайдено.")

    elif args.command == "search":
        items = manager.search_by_name(args.name)
        print(f"--- Результати пошуку для '{args.name}' ---")
        for item in items:
            print(item)

    elif args.command == "stats":
        stats = manager.get_condition_stats(args.name)
        target = f"для '{args.name}'" if args.name else "для всіх предметів"
        print(f"--- Статистика стану {target} ---")
        for cond, pct in stats.items():
            print(f"{cond}: {pct}%")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()