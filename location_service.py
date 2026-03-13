import requests

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()

        location = data.get("city", "Unknown")
        coords = data.get("loc", "0,0")

        lat, lon = coords.split(",")

        return {
            "city": location,
            "lat": float(lat),
            "lon": float(lon)
        }

    except:
        return {
            "city": "Unknown",
            "lat": 0,
            "lon": 0
        }