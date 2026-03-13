# models.py
# All data models for DURN disaster map

from pydantic import BaseModel
from typing import Literal, Optional


class MapEvent(BaseModel):
    type: Literal["flood", "danger", "sos", "volunteer", "drone", "vendor"]
    lat: float
    lng: float
    severity: Literal["critical", "high", "medium", "low"] = "medium"
    label: Optional[str] = None
    meta: Optional[dict] = None
    # meta examples:
    #   flood   → {"depth_cm": 120}
    #   sos     → {"need": "Insulin", "floor": 3}
    #   vendor  → {"stock": "ORS x200", "open": True, "vtype": "Medical"}
    #   drone   → {"battery": 78, "status": "Delivering"}
    #   volunteer → {"vehicle": "boat", "status": "available"}


class SOSRequest(BaseModel):
    lat: float
    lng: float
    label: Optional[str] = "SOS Request"
    need: Optional[str] = "Help needed"
    floor: Optional[int] = None


class RouteModel(BaseModel):
    name: str
    coords: list[list[float]]   # [[lat, lng], [lat, lng], ...]
    status: Literal["clear", "caution", "blocked"] = "clear"
    note: Optional[str] = None


class FloodZone(BaseModel):
    """Polygon zone — used for shaded flood area on map"""
    name: str
    severity: Literal["critical", "high", "medium", "low"]
    coordinates: list[list[float]]  # [[lat,lng], [lat,lng], ...]  — min 3 points
    depth_cm: Optional[int] = None