from enum import StrEnum, auto
from pydantic import BaseModel, Field

class InventoryCategory(StrEnum):
    FERMENTABLES = auto()
    HOPS = auto()
    MISCS = auto()
    YEASTS = auto()

class InventoryItem(BaseModel):
    id: str | None = Field(alias="_id")
    inventory: float | None = None
