from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import AliasPath, BaseModel, Field, RootModel
from enum import StrEnum

from .fermentable import BatchFermentable
from .hop import BatchHop
from .misc import BatchMisc
from .recipe import RecipeDetail
from .yeast import BatchYeast

from .base import BoilStep, CarbonationType, Timestamp, VersionedModel
from .inventory import InventoryItem

class BatchMeasurement(BaseModel):
    """Measurement reading in a batch"""
    type: str
    value: float
    unit: str
    time: datetime
    comment: Optional[str] = None

class BatchNote(BaseModel):
    """Note entry in a batch"""
    note: str
    type: str | None = None
    timestamp: int

class BatchStatus(StrEnum):
    PLANNING = "Planning"
    BREWING = "Brewing"
    FERMENTING = "Fermenting"
    CONDITIONING = "Conditioning"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"

class Batch(BaseModel):
    name: str
    id: str = Field(alias="_id")
    batch_no: int = Field(alias="batchNo")
    brew_date: Optional[int] = Field(alias="brewDate", default=None)
    status: BatchStatus = Field(default=BatchStatus.PLANNING)
    brewer: Optional[str] = None
    # Recipe is an object containing a name.
    recipe_name: str = Field(validation_alias=AliasPath("recipe", "name"))

class BatchDetail(Batch, VersionedModel):
    """Represents a batch with fields from Brewfather API."""
    recipe_id: Optional[str] = Field(alias="recipeId", default=None)
    measurements: List[BatchMeasurement] = Field(default_factory=list)
    notes: List[BatchNote] = Field(default_factory=list)
    measurement_devices: List[Dict[str, Any]] = Field(alias="measurementDevices", default_factory=list)
    tags: List[str] = Field(default_factory=list)
    brewed: bool = False
    og: Optional[float] = None
    fg: Optional[float] = None
    abv: Optional[float] = None
    bottling_date: Optional[datetime] = Field(alias="bottlingDate", default=None)
    carbonation_type: CarbonationType | None = Field(alias="carbonationType", default=None)
    carbonation_level: Optional[float] = Field(alias="carbonationLevel", default=None)
    fermentation_start_date: Optional[datetime] = Field(alias="fermentationStartDate", default=None)
    fermentation_end_date: Optional[datetime] = Field(alias="fermentationEndDate", default=None)
    recipe: RecipeDetail
    
    # Process events and measurements
    events: List[Dict[str, Any]] = Field(default_factory=list)
    devices: Dict[str, Any] = Field(default_factory=dict)
    
    # Batch-specific measurements vs estimates
    measured_og: Optional[float] = Field(alias="measuredOg", default=None)
    measured_fg: Optional[float] = Field(alias="measuredFg", default=None)
    measured_abv: Optional[float] = Field(alias="measuredAbv", default=None)
    measured_attenuation: Optional[float] = Field(alias="measuredAttenuation", default=None)
    measured_efficiency: Optional[float] = Field(alias="measuredEfficiency", default=None)
    measured_mash_efficiency: Optional[float] = Field(alias="measuredMashEfficiency", default=None)
    measured_kettle_efficiency: Optional[float] = Field(alias="measuredKettleEfficiency", default=None)
    measured_conversion_efficiency: Optional[float] = Field(alias="measuredConversionEfficiency", default=None)
    measured_pre_boil_gravity: Optional[float] = Field(alias="measuredPreBoilGravity", default=None)
    measured_post_boil_gravity: Optional[float] = Field(alias="measuredPostBoilGravity", default=None)
    measured_first_wort_gravity: Optional[float] = Field(alias="measuredFirstWortGravity", default=None)
    measured_batch_size: Optional[float] = Field(alias="measuredBatchSize", default=None)
    measured_boil_size: Optional[float] = Field(alias="measuredBoilSize", default=None)
    measured_bottling_size: Optional[float] = Field(alias="measuredBottlingSize", default=None)
    measured_fermenter_top_up: Optional[float] = Field(alias="measuredFermenterTopUp", default=None)
    measured_kettle_size: Optional[float] = Field(alias="measuredKettleSize", default=None)
    measured_mash_ph: Optional[float] = Field(alias="measuredMashPh", default=None)
    
    # Estimates
    estimated_og: Optional[float] = Field(alias="estimatedOg", default=None)
    estimated_fg: Optional[float] = Field(alias="estimatedFg", default=None)
    estimated_ibu: Optional[float] = Field(alias="estimatedIbu", default=None)
    estimated_color: Optional[float] = Field(alias="estimatedColor", default=None)
    estimated_abv: Optional[float] = Field(alias="estimatedAbv", default=None)
    estimated_total_gravity: Optional[float] = Field(alias="estimatedTotalGravity", default=None)
    estimated_bu_gu_ratio: Optional[float] = Field(alias="estimatedBuGuRatio", default=None)
    estimated_rb_ratio: Optional[float] = Field(alias="estimatedRbRatio", default=None)
    
    # Batch-specific inventory tracking
    batch_fermentables: List[BatchFermentable] = Field(alias="batchFermentables", default_factory=list)
    batch_hops: List[BatchHop] = Field(alias="batchHops", default_factory=list)
    batch_yeasts: List[BatchYeast] = Field(alias="batchYeasts", default_factory=list)
    batch_miscs: List[BatchMisc] = Field(alias="batchMiscs", default_factory=list)
    
    # Local additions (not in recipe)
    batch_fermentables_local: List[BatchFermentable] = Field(alias="batchFermentablesLocal", default_factory=list)
    batch_hops_local: List[BatchHop] = Field(alias="batchHopsLocal", default_factory=list)
    batch_yeasts_local: List[BatchYeast] = Field(alias="batchYeastsLocal", default_factory=list)
    batch_miscs_local: List[BatchMisc] = Field(alias="batchMiscsLocal", default_factory=list)
    
    # Process control
    brew_controller_enabled: bool = Field(alias="brewControllerEnabled", default=False)
    fermentation_controller_enabled: bool = Field(alias="fermentationControllerEnabled", default=False)
    mash_steps_count: Optional[int] = Field(alias="mashStepsCount", default=None)
    boil_steps_count: Optional[int] = Field(alias="boilStepsCount", default=None)
    boil_steps: List[BoilStep] = Field(alias="boilSteps", default_factory=list)
    
    # Additional batch fields
    hidden: bool = False
    archived: bool = Field(alias="_archived", default=False)
    init: bool = Field(alias="_init", default=False)
    hide_batch_events: bool = Field(alias="hideBatchEvents", default=False)
    priming_sugar_equiv: Optional[float] = Field(alias="primingSugarEquiv", default=None)
    carbonation_force: Optional[float] = Field(alias="carbonationForce", default=None)
    bottling_date_set: bool = Field(alias="bottlingDateSet", default=False)
    fermentation_start_date_set: bool = Field(alias="fermentationStartDateSet", default=False)
    cost: Dict[str, Any] = Field(default_factory=dict)
    
    # Additional metadata fields
    shared: bool = Field(alias="_shared", default=False)
    share: str | None = Field(alias="_share", default=None)
    type_field: str = Field(alias="_type", default="batch")

    model_config = {
        "populate_by_name": True,
    }


class BatchList(RootModel[list[Batch]]):
    """A collection of batches from Brewfather API."""
    pass
