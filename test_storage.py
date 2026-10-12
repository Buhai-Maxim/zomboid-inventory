import pytest
from storage import InventoryManager, BaseDataReader

# Тестовий фейковий рідер, щоб не залежати від файлу на диску
class FakeDataReader(BaseDataReader):
    def read_data(self, file_path: str):
        return [
            {"ID": 1, "Name": "Hammer", "Type": "Tool", "Condition": "Mint", "Amount": 10},
            {"ID": 2, "Name": "Nails", "Type": "Fasteners", "Condition": "Good", "Amount": 450},
            {"ID": 3, "Name": "Axe", "Type": "Weapon", "Condition": "Bad", "Amount": 1}
        ]

@pytest.fixture
def manager():
    mgr = InventoryManager(FakeDataReader())
    mgr.load("dummy_path.csv")
    return mgr

def test_get_by_id(manager):
    item = manager.get_by_id(2)
    assert item is not None
    assert item["Name"] == "Nails"
    assert manager.get_by_id(999) is None

def test_search_by_name(manager):
    results = manager.search_by_name("hammer")
    assert len(results) == 1
    assert results[0]["ID"] == 1

def test_pagination(manager):
    page_1 = manager.get_page(page=1, page_size=2)
    page_2 = manager.get_page(page=2, page_size=2)
    assert len(page_1) == 2
    assert len(page_2) == 1
    assert page_1[0]["ID"] == 1
    assert page_2[0]["ID"] == 3