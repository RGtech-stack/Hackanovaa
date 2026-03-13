# events.py
# Map event endpoints: flood markers, danger zones, SOS, drones, volunteers, vendors

from fastapi import APIRouter, HTTPException
from models import MapEvent, SOSRequest, FloodZone
from datetime import datetime
import uuid

router = APIRouter()

# ── In-memory store (swap with PostGIS later) ──
db_events: dict = {}
db_zones:  dict = {}   # flood polygon zones


def _id():
    return str(uuid.uuid4())[:8].upper()


# ─────────────────────────────────────────────
# SEED — demo data so map works immediately
# ─────────────────────────────────────────────

def seed_events():
    demo = [
        # ── Flood markers ──
        {"type":"flood",     "lat":19.0760, "lng":72.8777, "severity":"critical", "label":"Dharavi",         "meta":{"depth_cm":128}},
        {"type":"flood",     "lat":19.0550, "lng":72.8350, "severity":"high",     "label":"Mahim Creek",     "meta":{"depth_cm":85}},
        {"type":"flood",     "lat":19.1200, "lng":72.9000, "severity":"medium",   "label":"Kurla East",      "meta":{"depth_cm":37}},
        {"type":"flood",     "lat":19.0330, "lng":72.8550, "severity":"high",     "label":"Sion",            "meta":{"depth_cm":94}},
        {"type":"flood",     "lat":19.1680, "lng":72.9480, "severity":"critical", "label":"Ghatkopar West",  "meta":{"depth_cm":152}},
        # ── Danger zones ──
        {"type":"danger",    "lat":19.0640, "lng":72.8620, "severity":"critical", "label":"Collapsed Bridge"},
        {"type":"danger",    "lat":19.1400, "lng":72.9300, "severity":"critical", "label":"Live Wire in Water"},
        {"type":"danger",    "lat":19.0480, "lng":72.8700, "severity":"high",     "label":"Wall Collapse Risk"},
        # ── SOS signals ──
        {"type":"sos",       "lat":19.0800, "lng":72.8800, "severity":"critical", "label":"Rashida Bi",      "meta":{"need":"Medicine","floor":3}},
        {"type":"sos",       "lat":19.0520, "lng":72.8380, "severity":"critical", "label":"Family of 4",     "meta":{"need":"Rescue","floor":4}},
        {"type":"sos",       "lat":19.1250, "lng":72.9050, "severity":"high",     "label":"Elderly Man",     "meta":{"need":"Insulin","floor":2}},
        {"type":"sos",       "lat":19.0360, "lng":72.8600, "severity":"high",     "label":"3 Children",      "meta":{"need":"Food + Water","floor":1}},
        # ── Vendors ──
        {"type":"vendor",    "lat":19.0720, "lng":72.8720, "severity":"low",      "label":"Khan Medical",    "meta":{"stock":"ORS×200, Insulin×15","open":True,"vtype":"Medical"}},
        {"type":"vendor",    "lat":19.0600, "lng":72.8500, "severity":"low",      "label":"Shree Kirana",    "meta":{"stock":"Rice 40kg, Water×300","open":True,"vtype":"Food"}},
        {"type":"vendor",    "lat":19.1300, "lng":72.9100, "severity":"low",      "label":"City Pharmacy",   "meta":{"stock":"ORS×80, Paracetamol×200","open":True,"vtype":"Medical"}},
        {"type":"vendor",    "lat":19.1600, "lng":72.9400, "severity":"low",      "label":"Ghatkopar Hub",   "meta":{"stock":"Kits×30","open":False,"vtype":"Mixed"}},
        # ── Drones ──
        {"type":"drone",     "lat":19.0850, "lng":72.8850, "severity":"low",      "label":"Drone Alpha",     "meta":{"battery":78, "status":"Delivering"}},
        {"type":"drone",     "lat":19.1100, "lng":72.9200, "severity":"low",      "label":"Drone Beta",      "meta":{"battery":100,"status":"Idle"}},
        {"type":"drone",     "lat":19.0450, "lng":72.8700, "severity":"low",      "label":"Drone Gamma",     "meta":{"battery":22, "status":"Returning"}},
        # ── Volunteers ──
        {"type":"volunteer", "lat":19.0680, "lng":72.8750, "severity":"low",      "label":"Suresh — Boat",   "meta":{"vehicle":"boat","status":"delivering"}},
        {"type":"volunteer", "lat":19.1150, "lng":72.9050, "severity":"low",      "label":"Priya — Bike",    "meta":{"vehicle":"bike","status":"available"}},
    ]
    for e in demo:
        eid = _id()
        db_events[eid] = {**e, "id": eid, "created_at": datetime.utcnow().isoformat() + "Z"}

    # Flood polygon zones (shaded areas on map)
    demo_zones = [
        {
            "name": "Dharavi Flood Zone",
            "severity": "critical",
            "depth_cm": 128,
            "coordinates": [
                [19.0740, 72.8750], [19.0780, 72.8750],
                [19.0785, 72.8810], [19.0745, 72.8815], [19.0740, 72.8750]
            ]
        },
        {
            "name": "Mahim Flood Zone",
            "severity": "high",
            "depth_cm": 85,
            "coordinates": [
                [19.0530, 72.8320], [19.0570, 72.8320],
                [19.0575, 72.8380], [19.0535, 72.8382], [19.0530, 72.8320]
            ]
        },
        {
            "name": "Ghatkopar Flood Zone",
            "severity": "critical",
            "depth_cm": 152,
            "coordinates": [
                [19.1660, 72.9460], [19.1700, 72.9460],
                [19.1705, 72.9510], [19.1665, 72.9512], [19.1660, 72.9460]
            ]
        },
    ]
    for z in demo_zones:
        zid = _id()
        db_zones[zid] = {**z, "id": zid}


seed_events()


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@router.get("/map-events")
def get_events(type: str = None):
    """Return all map events. Optional ?type=flood|sos|danger|..."""
    events = list(db_events.values())
    if type:
        events = [e for e in events if e["type"] == type]
    return {"count": len(events), "events": events}


@router.post("/map-events")
def add_event(event: MapEvent):
    """Add any map event."""
    eid = _id()
    record = {**event.model_dump(), "id": eid, "created_at": datetime.utcnow().isoformat() + "Z"}
    db_events[eid] = record
    return record


@router.delete("/map-events/{event_id}")
def delete_event(event_id: str):
    if event_id not in db_events:
        raise HTTPException(404, "Event not found")
    del db_events[event_id]
    return {"deleted": event_id}


@router.post("/sos")
def create_sos(payload: SOSRequest):
    """Shortcut to create a critical SOS from a citizen's GPS location."""
    eid = "SOS-" + _id()
    record = {
        "id": eid, "type": "sos",
        "lat": payload.lat, "lng": payload.lng,
        "severity": "critical",
        "label": payload.label,
        "meta": {"need": payload.need, "floor": payload.floor},
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    db_events[eid] = record
    return record


@router.get("/flood-zones")
def get_flood_zones():
    """Return flood polygon zones for shaded map overlay."""
    return {"count": len(db_zones), "zones": list(db_zones.values())}


@router.post("/flood-zones")
def add_flood_zone(zone: FloodZone):
    """Add a polygon flood zone."""
    zid = _id()
    record = {**zone.model_dump(), "id": zid}
    db_zones[zid] = record
    return record


# ─────────────────────────────────────────────
# GPS & NEAREST VENDOR
# ─────────────────────────────────────────────

def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance in km between two GPS points."""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth radius in km
    lat1_rad, lng1_rad = radians(lat1), radians(lng1)
    lat2_rad, lng2_rad = radians(lat2), radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c


@router.get("/nearest-vendors")
def get_nearest_vendors(lat: float, lng: float, limit: int = 3):
    """
    Find nearest vendors to user location (GPS coordinates).
    Returns top N closest vendors with distances.
    """
    vendors = [e for e in db_events.values() if e["type"] == "vendor"]
    
    if not vendors:
        return {"error": "No vendors found", "vendors": []}
    
    # Calculate distance for each vendor
    vendors_with_dist = []
    for v in vendors:
        distance = haversine_distance(lat, lng, v["lat"], v["lng"])
        vendors_with_dist.append({
            **v,
            "distance_km": round(distance, 2)
        })
    
    # Sort by distance and return top N
    vendors_with_dist.sort(key=lambda x: x["distance_km"])
    return {
        "user_location": {"lat": lat, "lng": lng},
        "count": len(vendors_with_dist[:limit]),
        "vendors": vendors_with_dist[:limit]
    }


@router.post("/user-location")
def log_user_location(lat: float, lng: float, label: str = "My Location"):
    """Log current user GPS location (for internal tracking)."""
    uid = "USER-" + _id()
    record = {
        "id": uid,
        "type": "user_location",
        "lat": lat,
        "lng": lng,
        "label": label,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    # Optional: Store in db_events or separate storage
    return record