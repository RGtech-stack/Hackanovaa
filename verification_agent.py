import json
import math


def load_volunteers():
    """
    Load volunteer data from JSON file
    """
    try:
        with open("data/volunteers.json", "r") as f:
            volunteers = json.load(f)
        return volunteers
    except Exception as e:
        print("[VERIFICATION AGENT] Error loading volunteers:", e)
        return []


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates (km)
    """
    R = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def verify_emergency(location, severity, lat, lon):
    """
    Verification Agent

    Checks if an emergency is real by finding volunteers
    within a 15 km radius of the SOS location.
    """

    print("\n[VERIFICATION AGENT] Starting verification process...")

    volunteers = load_volunteers()

    sos_lat = lat
    sos_lon = lon

    # Skip verification for low severity
    if severity <= 4:
        print("[VERIFICATION AGENT] Low severity event. Skipping verification.")
        return True, "Low severity emergency"

    nearby_volunteers = []

    for v in volunteers:

        volunteer_lat = v.get("lat")
        volunteer_lon = v.get("lon")
        available = v.get("available", False)

        if volunteer_lat is None or volunteer_lon is None:
            continue

        distance = haversine_distance(sos_lat, sos_lon, volunteer_lat, volunteer_lon)

        print(f"[VERIFICATION AGENT] Distance to {v.get('name')} = {distance:.2f} km")

        if distance <= 15 and available:
            nearby_volunteers.append(v)

    if len(nearby_volunteers) == 0:
        print("[VERIFICATION AGENT] No volunteers within 15 km radius.")
        return False, "No nearby volunteers available"

    confirmations = 0

    for volunteer in nearby_volunteers:

        print(f"[VERIFICATION AGENT] Contacting volunteer {volunteer.get('name')}...")

        # simulate confirmation
        simulated_reply = True

        if simulated_reply:
            confirmations += 1

    if confirmations >= 1:
        print(f"[VERIFICATION AGENT] Emergency verified by {confirmations} volunteer(s).")
        return True, "Emergency verified"

    return False, "Emergency not verified"