from storage import CSVDataReader, InventoryManager

manager = InventoryManager(CSVDataReader())
manager.load("items.csv")

print("--- Сторінка 1 (по 2 елементи) ---")
print(manager.get_page(page=1, page_size=2))

print("\n--- Пошук предмета по ID = 2 ---")
print(manager.get_by_id(2))

print("\n--- Пошук за назвою 'Hammer' ---")
print(manager.search_by_name("Hammer"))