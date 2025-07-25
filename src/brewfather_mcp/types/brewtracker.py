"""Brewtracker and readings type definitions based on actual API responses."""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, RootModel


class BrewTrackerStep(BaseModel):
    """Individual step in a brewing stage"""
    name: Optional[str] = None  # Some steps don't have names
    type: str  # e.g., "mash", "ramp", "event", "boil"
    time: int  # Time in seconds
    duration: Optional[int] = None
    priority: Optional[int] = None
    value: Optional[float] = None  # Temperature or other target value
    description: Optional[str] = None
    tooltip: Optional[str] = None
    pause_before: bool = Field(alias="pauseBefore", default=False)
    final: Optional[bool] = None

    model_config = {
        "populate_by_name": True,
    }


class BrewTrackerStage(BaseModel):
    """Brewing stage (e.g., Mash, Boil) with steps"""
    name: str
    type: str  # e.g., "tracker"
    duration: int  # Duration in seconds
    step: int  # Current step index
    position: int  # Current position in seconds
    paused: bool
    steps: List[BrewTrackerStep]

    model_config = {
        "populate_by_name": True,
    }


class BrewTrackerStatus(BaseModel):
    """Complete brewtracker status for a batch"""
    id: Optional[str] = Field(alias="_id", default=None)
    name: Optional[str] = None
    stage: int = 0  # Current stage index
    hidden: bool = False
    alarm: bool = False
    active: bool = False
    completed: bool = False
    enabled: bool = True
    notify: bool = True
    stages: List[BrewTrackerStage] = Field(default_factory=list)
    rev: Optional[str] = Field(alias="_rev", default=None)

    model_config = {
        "populate_by_name": True,
    }


class BatchReading(BaseModel):
    """Individual sensor reading from a batch"""
    # Core fields always present
    time: int  # Unix timestamp in milliseconds
    type: str  # Device type like "raptCloud", "stream"
    
    # Fields that may not be present in all device types
    id: Optional[str] = None  # Device ID like "RAPTPILL"
    name: Optional[str] = None  # Device name like "RAPT pill" 
    device_type: Optional[str] = Field(alias="deviceType", default=None)  # "Hydrometer", "TemperatureController"
    device_id: Optional[str] = Field(alias="deviceId", default=None)  # UUID of device
    
    # Sensor data (optional depending on device type)
    temp: Optional[float] = None  # Temperature in Celsius
    sg: Optional[float] = None  # Specific gravity
    battery: Optional[float] = None  # Battery percentage
    rssi: Optional[float] = None  # Signal strength
    target_temp: Optional[float] = Field(alias="target_temp", default=None)
    
    # Additional fields that might be present
    ph: Optional[float] = None
    pressure: Optional[float] = None
    angle: Optional[float] = None
    interval: Optional[int] = None
    
    # Fields for stream type devices
    room_temp: Optional[float] = Field(alias="roomTemp", default=None)
    fridge_temp: Optional[float] = Field(alias="fridgeTemp", default=None)
    beer: Optional[float] = None
    bpm: Optional[float] = None
    comment: Optional[str] = None
    status: Optional[str] = None

    model_config = {
        "populate_by_name": True,
    }


class BatchReadingsList(RootModel[List[BatchReading]]):
    """Collection of batch readings"""
    pass


class LastReading(BatchReading):
    """Most recent reading from batch sensors - same structure as BatchReading"""
    pass