```mermaid
classDiagram
    class BaseDataReader {
        <<interface>>
        +read_data(file_path: str) List~Dict~
    }

    class CSVDataReader {
        +read_data(file_path: str) List~Dict~
    }

    class InventoryManager {
        -reader: BaseDataReader
        -items: List~Dict~
        +load(file_path: str) void
        +get_page(page: int, page_size: int) List~Dict~
        +get_by_id(item_id: int) Optional~Dict~
        +search_by_name(name: str) List~Dict~
        +get_condition_stats(item_name: Optional~str~) Dict~str, float~
    }

    BaseDataReader <|.. CSVDataReader : implements
    InventoryManager o-- BaseDataReader : uses