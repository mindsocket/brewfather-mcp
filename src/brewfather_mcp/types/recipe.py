from typing import Any, Dict
from pydantic import BaseModel, Field, RootModel, field_validator
from enum import StrEnum

from .base import BoilStep, EquipmentProfile, EquipmentProfileDetail, FermentationSchedule, FgFormula, IbuFormula, MashSchedule, Timestamp, WaterSettings
from .fermentable import RecipeFermentable
from .hop import RecipeHop
from .misc import RecipeMisc
from .yeast import RecipeYeast

class RecipeType(StrEnum):
    ALL_GRAIN = "All Grain"
    EXTRACT = "Extract"
    PARTIAL_MASH = "Partial Mash"


class RecipeStyle(BaseModel):
    """Style information for a recipe"""
    name: str

class RecipeStyleDetail(RecipeStyle):
    category: str
    type: str
    ibu_min: float = Field(alias="ibuMin")
    ibu_max: float = Field(alias="ibuMax")
    abv_min: float = Field(alias="abvMin")
    abv_max: float = Field(alias="abvMax")
    og_min: float = Field(alias="ogMin")
    og_max: float = Field(alias="ogMax")
    fg_min: float = Field(alias="fgMin")
    fg_max: float = Field(alias="fgMax")
    color_min: float = Field(alias="colorMin")
    color_max: float = Field(alias="colorMax")
    style_guide: str | None = Field(alias="styleGuide", default=None)
    notes: str | None = None
    profile: str | None = None
    ingredients: str | None = None
    examples: str | None = None

class RecipeName(BaseModel):
    name: str

class Recipe(RecipeName):
    """Base recipe model with fields from list view"""
    id: str = Field(alias="_id")
    author: str | None = None
    type: RecipeType | None = Field(alias="type", default=None)
    equipment: EquipmentProfile | None = None
    style: RecipeStyle | None = None

    model_config = {
        "populate_by_name": True,
    }

class RecipeDetail(Recipe):
    """Detailed recipe model with all properties"""
    # Basic properties
    batch_size: float | None = Field(alias="batchSize", default=None)
    boil_size: float | None = Field(alias="boilSize", default=None)
    boil_time: int | None = Field(alias="boilTime", default=None)
    efficiency: float | None = None
    mash_efficiency: float | None = Field(alias="mashEfficiency", default=None)

    # Calculations
    og: float | None = None
    fg: float | None = None
    ibu: float | None = None
    color: float | None = None
    abv: float | None = None
    og_plato: float | None = Field(alias="ogPlato", default=None)
    post_boil_gravity: float | None = Field(alias="postBoilGravity", default=None)
    pre_boil_gravity: float | None = Field(alias="preBoilGravity", default=None)
    attenuation: float | None = None

    # Recipe components
    style: RecipeStyle | RecipeStyleDetail | None = None
    fermentables: list[RecipeFermentable] = Field(default_factory=list)
    hops: list[RecipeHop] = Field(default_factory=list)
    yeasts: list[RecipeYeast] = Field(default_factory=list)
    miscs: list[RecipeMisc] = Field(default_factory=list)
    mash: MashSchedule | None = None
    water: WaterSettings | None = None
    fermentation: FermentationSchedule | None = None
    equipment: EquipmentProfile | EquipmentProfileDetail | None = None
    
    # Process details
    boil_steps: list[BoilStep] = Field(alias="boilSteps", default_factory=list)
    mash_steps_count: int | None = Field(alias="mashStepsCount", default=None)
    boil_steps_count: int | None = Field(alias="boilStepsCount", default=None)
    
    # Metadata
    notes: str | None = None
    tags: list[str] | None = None
    public: bool | None = None
    hidden: bool = Field(default=False)
    search_tags: list[str] = Field(alias="searchTags", default_factory=list)
    version: str | None = Field(alias="_version", default=None)
    created: Timestamp | None = Field(alias="_created", default=None)
    timestamp: Timestamp | None = Field(alias="_timestamp", default=None)
    timestamp_ms: int | None = Field(alias="_timestamp_ms", default=None)
    rev: str | None = Field(alias="_rev", default=None)
    uid: str | None = Field(alias="_uid", default=None)
    ev: float | None = Field(alias="_ev", default=None)
    type_field: str = Field(alias="_type", default="recipe")
    init: bool = Field(alias="_init", default=False)
    share: str | None = Field(alias="_share", default=None)
    public_flag: bool | None = Field(alias="_public", default=None)
    
    # Additional recipe fields from API
    defaults: Dict[str, Any] | None = None
    nutrition: Dict[str, Any] | None = None
    total_gravity: float | None = Field(alias="totalGravity", default=None)
    og_plato: float | None = Field(alias="ogPlato", default=None)
    first_wort_gravity: float | None = Field(alias="firstWortGravity", default=None)
    data: Dict[str, Any] | None = None
    
    # Additional calculations
    fermentables_total_amount: float | None = Field(alias="fermentablesTotalAmount", default=None)
    hops_total_amount: float | None = Field(alias="hopsTotalAmount", default=None)
    ibu_formula: IbuFormula | None = Field(alias="ibuFormula", default=None)
    fg_formula: FgFormula | None = Field(alias="fgFormula", default=None)
    carbonation: float | None = None
    style_conformity: bool | None = Field(alias="styleConformity", default=None)
    bu_gu_ratio: float | None = Field(alias="buGuRatio", default=None)
    rb_ratio: float | None = Field(alias="rbRatio", default=None)
    sum_dry_hop_per_liter: float | None = Field(alias="sumDryHopPerLiter", default=None)
    avg_weighted_hopstand_temp: float | None = Field(alias="avgWeightedHopstandTemp", default=None)
    diasmatic_power: float | None = Field(alias="diastaticPower", default=None)
    primary_temp: float | None = Field(alias="primaryTemp", default=None)
    first_wort_gravity: float | None = Field(alias="firstWortGravity", default=None)
    fermentable_ibu: float | None = Field(alias="fermentableIbu", default=None)
    extra_gravity: float | None = Field(alias="extraGravity", default=None)
    path: str | None = None
    yeast_tolerance_exceeded_by: float | None = Field(alias="yeastToleranceExceededBy", default=None)
    manual_fg: bool | None = Field(alias="manualFg", default=None)
    hop_stand_minutes: int | None = Field(alias="hopStandMinutes", default=None)
    carbonation_style: Dict[str, Any] | None = Field(alias="carbonationStyle", default=None)

    model_config = {
        "populate_by_name": True,
    }


class RecipeList(RootModel[list[Recipe]]):
    """A collection of recipes."""
    pass
