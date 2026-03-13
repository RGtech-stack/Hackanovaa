from fastapi import FastAPI
from orchestrator import run_agents
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()


@app.post("/sos")
def sos(data: dict):

    message = data.get("message")
    lat = data.get("lat")
    lon = data.get("lon")

    result = run_agents(message, lat, lon)

    return result