# GPS Integration for DURN Disaster Map

## Overview
The disaster map now includes **real-time GPS location tracking** and **vendor routing** to help users navigate to the nearest supply vendors during emergencies.

## Features

### 1. **Real-Time GPS Location**
- Requests browser geolocation permission
- Continuously tracks user position (watch mode)
- Displays user marker on map with pulsing animation
- Updates location panel with lat/lng coordinates

### 2. **Nearest Vendor Detection**
- Automatically finds the 3 nearest vendors based on GPS coordinates
- Calculates distance using Haversine formula
- Displays vendors in side panel sorted by distance
- Shows vendor stock/supply information

### 3. **Interactive Routing**
- Click "Route to Here" button to navigate to any vendor
- Uses Leaflet Routing Machine for turn-by-turn directions
- Shows visual route line on map
- Automatically centers map to show full route

### 4. **Status Display**
- GPS status indicator (🟢 Located / 🔴 Error)
- Real-time vendor count
- Automatic fallback to Mumbai center if GPS unavailable

---

## API Endpoints

### Get Nearest Vendors
```
GET /nearest-vendors?lat=19.076&lng=72.877&limit=3
```

**Response:**
```json
{
  "user_location": {"lat": 19.076, "lng": 72.877},
  "count": 3,
  "vendors": [
    {
      "id": "XYZ1",
      "type": "vendor",
      "lat": 19.072,
      "lng": 72.872,
      "label": "Khan Medical",
      "severity": "low",
      "distance_km": 0.52,
      "meta": {
        "stock": "ORS×200, Insulin×15",
        "open": true,
        "vtype": "Medical"
      }
    },
    ...
  ]
}
```

### Log User Location
```
POST /user-location?lat=19.076&lng=72.877&label=My%20Location
```

**Response:**
```json
{
  "id": "USER-ABC123",
  "type": "user_location",
  "lat": 19.076,
  "lng": 72.877,
  "label": "My Location",
  "created_at": "2026-03-13T10:30:45.123Z"
}
```

---

## How to Use

### 1. **Start the Backend Server**
```bash
cd e:\parth\Hackanovaa
pip install fastapi uvicorn httpx
uvicorn main:app --reload --port 8000
```

### 2. **Open the Map with GPS**
```
http://localhost:8000/map_gps.html
```

### 3. **Grant GPS Permission**
- Browser will ask for location permission
- Accept to enable real-time tracking

### 4. **View Nearest Vendors**
- Click "📍 Show Details" button to open side panel
- See your current coordinates
- View 3 nearest vendors with distances

### 5. **Navigate to a Vendor**
- Click "📍 Route to Here" on any vendor
- Map will show route from your location
- Route will include turn-by-turn directions (if available)

---

## Code Structure

### Frontend (map_gps.html)
- **GPS Tracking:** `requestGPSLocation()` - Watches position continuously
- **Vendor Search:** `findNearestVendors()` - Calls API to get nearest vendors
- **Routing:** `routeToVendor()` - Creates visual route on map
- **Display:** `displayMapEvents()` - Shows all markers (floods, vendors, etc.)

### Backend (events.py)
- **`/nearest-vendors`** - Finds vendors within distance range
- **`/user-location`** - Logs user GPS position
- **`haversine_distance()`** - Calculates distance between coordinates

---

## Key Technologies

| Technology | Purpose |
|-----------|---------|
| **Leaflet** | Map rendering & markers |
| **Leaflet Routing Machine** | Turn-by-turn directions |
| **Geolocation API** | Browser-based GPS |
| **FastAPI** | Backend API server |
| **Haversine Formula** | Distance calculation |

---

## Browser Requirements

✅ **Works in modern browsers with:**
- HTTPS or localhost
- Geolocation API support
- Cookies/Storage enabled

❌ **Won't work in:**
- HTTP (except localhost)
- Private/Incognito without permission
- Browsers with location disabled

---

## Troubleshooting

### GPS Not Working
1. Check if HTTPS or localhost
2. Check browser location permissions (Settings → Privacy)
3. Toggle geolocation in browser settings
4. Try incognito mode

### Vendors Not Showing
1. Ensure backend is running (`uvicorn main:app --reload`)
2. Check API base URL (default: `http://localhost:8000`)
3. Verify vendors exist in database
4. Open browser console (F12) for errors

### Route Not Displaying
1. Check if Leaflet Routing Machine is loaded
2. May need API key for some routing services
3. Try clicking same vendor twice
4. Check browser console for CORS errors

### Location Showing Wrong Coordinates
1. GPS accuracy varies by device
2. WiFi-based location less accurate than GPS
3. Try moving to open area for better signal
4. Refresh page and grant permission again

---

## Example Usage Flow

```
1. User opens map → Browser asks for GPS permission
2. User clicks "Allow" → GPS location tracked
3. Backend finds 3 nearest vendors → Displayed in panel
4. User clicks "Route to Here" on vendor → Route drawn on map
5. User navigates → Real-time location updates as they move
6. User reaches vendor → Marker shows vendor details
```

---

## Future Enhancements

📌 **Potential Improvements:**
- [ ] Offline map caching
- [ ] Multiple route options
- [ ] ETA calculation
- [ ] Push notifications for nearby vendors
- [ ] Vendor ratings/reviews
- [ ] Filter by supply type (Medical, Food, Water)
- [ ] Live vendor status updates
- [ ] Integration with Google Maps API
- [ ] Dark/Light theme toggle
- [ ] Voice-guided directions

---

## Support

For issues or feature requests, check:
- Browser console (F12 → Console tab)
- API documentation: http://localhost:8000/docs
- Backend logs in terminal

---

**Built with ❤️ for disaster relief coordination**
