from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from storage import CSVDataReader, InventoryManager

app = FastAPI(title="Zomboid Accounting API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = InventoryManager(CSVDataReader())
manager.load("items.csv")

@app.get("/items")
def get_items(page: int = 1, size: int = 50):
    return {
        "page": page,
        "size": size,
        "items": manager.get_page(page=page, page_size=size)
    }

@app.get("/items/search")
def search_items(name: str = Query(..., min_length=1)):
    return manager.search_by_name(name)

@app.get("/items/stats")
def get_stats(name: Optional[str] = None):
    return manager.get_condition_stats(name)

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    item = manager.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item