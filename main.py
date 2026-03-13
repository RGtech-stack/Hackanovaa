# main.py
# DURN — Disaster Map Backend
# ─────────────────────────────────────────────
# Install : pip install fastapi uvicorn httpx
# Run     : uvicorn main:app --reload --port 8000
# Docs    : http://localhost:8000/docs
# ─────────────────────────────────────────────

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from events import router as events_router
from routes import router as routes_router

app = FastAPI(
    title="DURN Disaster Map API",
    description=(
        "Real-time disaster coordination backend.\n\n"
        "Manages: flood zones · danger zones · SOS signals · "
        "vendors · drones · volunteers · safe routes"
    ),
    version="1.0.0",
)

# Allow frontend (map.html) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(events_router, tags=["Events"])
app.include_router(routes_router, tags=["Routes"])


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "DURN API online ✓",
        "docs":   "http://localhost:8000/docs",
        "endpoints": {
            "events":      "GET  /map-events",
            "sos":         "POST /sos",
            "flood_zones": "GET  /flood-zones",
            "routes":      "GET  /routes",
            "directions":  "GET  /routing/directions",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)