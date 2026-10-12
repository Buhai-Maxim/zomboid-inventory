import csv
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from collections import Counter

class BaseDataReader(ABC):
    @abstractmethod
    def read_data(self, file_path: str) -> List[Dict]:
        pass

class CSVDataReader(BaseDataReader):
    def read_data(self, file_path: str) -> List[Dict]:
        items = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item_id = row.get("id") or row.get("ID")
                name = row.get("name") or row.get("Name")
                item_type = row.get("type") or row.get("Type")
                condition = row.get("condition") or row.get("Condition")
                amount = row.get("amount") or row.get("Amount")

                items.append({
                    "ID": int(item_id),
                    "Name": name,
                    "Type": item_type,
                    "Condition": condition,
                    "Amount": int(amount)
                })
        return items

class InventoryManager:
    def __init__(self, reader: BaseDataReader):
        self.reader = reader
        self.items: List[Dict] = []

    def load(self, file_path: str):
        self.items = self.reader.read_data(file_path)

    def get_page(self, page: int = 1, page_size: int = 10) -> List[Dict]:
        start = (page - 1) * page_size
        end = start + page_size
        return self.items[start:end]

    def get_by_id(self, item_id: int) -> Optional[Dict]:
        for item in self.items:
            if item["ID"] == item_id:
                return item
        return None

    def search_by_name(self, name: str) -> List[Dict]:
        name_lower = name.lower()
        return [item for item in self.items if name_lower in item["Name"].lower()]

    def get_condition_stats(self, item_name: Optional[str] = None) -> Dict[str, float]:
        target_items = self.items
        if item_name:
            target_items = [i for i in self.items if i["Name"].lower() == item_name.lower()]

        total_amount = sum(item["Amount"] for item in target_items)
        if total_amount == 0:
            return {}

        counts = Counter()
        for item in target_items:
            counts[item["Condition"]] += item["Amount"]

        return {cond: round((count / total_amount) * 100, 2) for cond, count in counts.items()}