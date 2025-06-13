
from pydantic import BaseModel, RootModel, Field, field_validator

from brewfather_mcp import utils

from .base import VersionedModel
from .inventory import InventoryItem

class FermentableBase(InventoryItem):
    """
    Core fermentable fields present in all contexts.
    """
    name: str
    type: str
    supplier: str
    attenuation: float | None = None

    model_config = {
        "populate_by_name": True,
    }

class FermentableDetail(FermentableBase, VersionedModel):
    color: float
    potential: float
    potential_percentage: float = Field(alias="potentialPercentage")

    grain_category: str | None = Field(alias="grainCategory", default=None)
    origin: str | None = None
    notes: str | None = None
    ibu_per_amount: float | None = Field(alias="ibuPerAmount", default=None)
    max_in_batch: float | None = Field(alias="maxInBatch", default=None)
    not_fermentable: bool | None = Field(alias="notFermentable", default=None)
    
    # Technical brewing properties
    acid: float | None = None
    cgdb: float | None = None
    coarse_fine_diff: float | None = Field(alias="coarseFineDiff", default=None)
    fan: float | None = None
    fgdb: float | None = None
    friability: float | None = None
    moisture: float | None = None
    protein: float | None = None
    diastatic_power: float | None = Field(alias="diastaticPower", default=None)

    # Additional fields for recipe context
    substitutes: str = ""
    used_in: str = Field(alias="usedIn", default="")
    user_notes: str = Field(alias="userNotes", default="")
    best_before_date: str | None = Field(alias="bestBeforeDate", default=None)
    manufacturing_date: str | None = Field(alias="manufacturingDate", default=None)
    
    hidden: bool = False
    
    # Additional color representation sometimes present
    lovibond: float | None = None
    cost_per_amount: float | None = Field(alias="costPerAmount", default=None)

    @field_validator("manufacturing_date", "best_before_date", mode="before")
    @classmethod
    def convert_timestamp_to_isodate(cls, value):
        return utils.convert_timestamp_to_iso8601(value)

class FermentableList(RootModel[list[FermentableBase]]):
    pass

class RecipeFermentable(FermentableDetail):
    """Fermentable ingredient in a recipe context"""
    # Recipe-specific required fields
    amount: float
    percentage: float | None = None
    add_after_boil: bool = Field(alias="addAfterBoil", default=False)
    
    model_config = {
        "populate_by_name": True,
    }


class BatchFermentable(RecipeFermentable):
    """Fermentable ingredient in a batch context with batch-specific tracking fields"""

    # Batch-specific tracking fields (always present)
    checked: bool = False
    not_in_recipe: bool = Field(alias="notInRecipe", default=False)
    removed_from_inventory: bool = Field(alias="removedFromInventory", default=False)
    removed_amount: float = Field(alias="removedAmount", default=0.0)
    total_cost: float = Field(alias="totalCost", default=0.0)
    display_amount: float = Field(alias="displayAmount", default=0.0)
    
    model_config = {
        "populate_by_name": True,
    }
