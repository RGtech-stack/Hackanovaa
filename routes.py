# routes.py
# Safe/danger route endpoints + OpenRouteService integration

from fastapi import APIRouter, HTTPException
from models import RouteModel
import uuid
import httpx   # pip install httpx

router = APIRouter()

# ── In-memory route store ──
db_routes: dict = {}

# ── OpenRouteService API key ──
# Get free key at https://openrouteservice.org/dev/#/signup
ORS_API_KEY = "YOUR_ORS_API_KEY"
ORS_BASE    = "https://api.openrouteservice.org/v2"


def _id():
    return str(uuid.uuid4())[:8].upper()


# ─────────────────────────────────────────────
# SEED ROUTES
# ─────────────────────────────────────────────

def seed_routes():
    demo = [
        {
            "name": "SV Road — Mahim Causeway",
            "coords": [[19.060, 72.840], [19.068, 72.858], [19.075, 72.878]],
            "status": "clear",
            "note": "Water < 20cm — fully passable"
        },
        {
            "name": "Eastern Express Highway",
            "coords": [[19.080, 72.895], [19.120, 72.920], [19.160, 72.948]],
            "status": "clear",
            "note": "Elevated road — completely safe"
        },
        {
            "name": "LBS Marg — Kurla",
            "coords": [[19.120, 72.900], [19.140, 72.920], [19.165, 72.942]],
            "status": "caution",
            "note": "1ft water — slow vehicles only"
        },
        {
            "name": "Cadell Road",
            "coords": [[19.055, 72.850], [19.048, 72.857], [19.045, 72.865]],
            "status": "blocked",
            "note": "3.2ft water — car blocked, boat only"
        },
        {
            "name": "Ghatkopar Corridor",
            "coords": [[19.155, 72.940], [19.163, 72.948], [19.170, 72.955]],
            "status": "blocked",
            "note": "Fully submerged — drone-only zone"
        },
    ]
    for r in demo:
        rid = _id()
        db_routes[rid] = {**r, "id": rid}


seed_routes()


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@router.get("/routes")
def get_routes(status: str = None):
    """
    Return all routes.
    Optional filter: ?status=clear|caution|blocked
    """
    routes = list(db_routes.values())
    if status:
        routes = [r for r in routes if r["status"] == status]
    return {"count": len(routes), "routes": routes}


@router.post("/routes")
def add_route(route: RouteModel):
    """Add a manual route with known coords."""
    rid = _id()
    record = {**route.model_dump(), "id": rid}
    db_routes[rid] = record
    return record


@router.delete("/routes/{route_id}")
def delete_route(route_id: str):
    if route_id not in db_routes:
        raise HTTPException(404, "Route not found")
    del db_routes[route_id]
    return {"deleted": route_id}


@router.patch("/routes/{route_id}/status")
def update_route_status(route_id: str, status: str):
    """Update a route's passability status."""
    if route_id not in db_routes:
        raise HTTPException(404, "Route not found")
    if status not in ("clear", "caution", "blocked"):
        raise HTTPException(400, "status must be clear | caution | blocked")
    db_routes[route_id]["status"] = status
    return db_routes[route_id]


# ─────────────────────────────────────────────
# OPENROUTESERVICE — real road routing
# ─────────────────────────────────────────────

@router.get("/routing/directions")
async def get_directions(
    start_lat: float, start_lng: float,
    end_lat:   float, end_lng:   float,
    profile: str = "driving-car"
):
    """
    Get real turn-by-turn route via OpenRouteService.

    Profiles available:
      driving-car | cycling-regular | foot-walking

    Example:
      GET /routing/directions?start_lat=19.076&start_lng=72.877&end_lat=19.120&end_lng=72.900

    Returns GeoJSON route + distance + duration.
    """
    if ORS_API_KEY == "YOUR_ORS_API_KEY":
        # Return mock when key not set
        return {
            "source": "mock",
            "message": "Set ORS_API_KEY in routes.py to get real directions",
            "mock_route": {
                "distance_km": round(
                    ((end_lat - start_lat)**2 + (end_lng - start_lng)**2)**0.5 * 111, 2
                ),
                "coords": [
                    [start_lat, start_lng],
                    [(start_lat + end_lat) / 2, (start_lng + end_lng) / 2],
                    [end_lat, end_lng],
                ]
            }
        }

    url = f"{ORS_BASE}/directions/{profile}"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [
            [start_lng, start_lat],   # ORS uses [lng, lat] order
            [end_lng,   end_lat],
        ]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=body, headers=headers, timeout=10)

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"ORS error: {resp.text}")

    data = resp.json()
    route = data["routes"][0]

    # Decode ORS encoded polyline to [[lat,lng], ...]
    coords = _decode_polyline(route["geometry"])

    return {
        "source": "openrouteservice",
        "distance_km": round(route["summary"]["distance"] / 1000, 2),
        "duration_min": round(route["summary"]["duration"] / 60, 1),
        "coords": coords,
    }


def _decode_polyline(encoded: str) -> list:
    """Decode Google/ORS encoded polyline to [[lat,lng], ...]"""
    coords, index, lat, lng = [], 0, 0, 0
    while index < len(encoded):
        for is_lat in (True, False):
            shift, result = 0, 0
            while True:
                b = ord(encoded[index]) - 63
                index += 1
                result |= (b & 0x1F) << shift
                shift += 5
                if b < 0x20:
                    break
            delta = ~(result >> 1) if result & 1 else result >> 1
            if is_lat:
                lat += delta
            else:
                lng += delta
        coords.append([lat / 1e5, lng / 1e5])
    return coords