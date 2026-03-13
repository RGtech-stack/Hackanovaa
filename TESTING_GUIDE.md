# GPS & Route Highlighting — Complete Testing Guide

## ✅ Setup Status
✓ Backend server: **Running on port 8000**
✓ All Python files: **Complete**
✓ map_gps.html: **Fixed with route highlighting**
✓ API endpoints: **All configured**

---

## 🚀 How to Run Everything

### Step 1: Start the Backend Server
```powershell
cd e:\parth\Hackanovaa
python -m uvicorn main:app --reload --port 8000
```
**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Open the Map in Browser
Navigate to:
```
http://localhost:8000/map_gps.html
```

### Step 3: Grant GPS Permission
- Browser will request location permission
- Click **"Allow"** to enable GPS tracking
- GPS status will change from 🔴 to 🟢

---

## 🗺️ Testing GPS Features

### 1. GPS Status Indicator
**Location:** Bottom-left corner
- 🔴 **Red** = Waiting for GPS signal
- 🟢 **Green** = GPS located successfully
- Shows: Latitude, Longitude, Vendor count

### 2. Location Panel
**Location:** Top-right "Show Details" button
- Click button to toggle side panel
- Shows: Your GPS coordinates (updates in real-time)
- Shows: Nearest 3 vendors with distance

### 3. Vendor List Updates
- Updates automatically every time GPS location changes
- Shows: Vendor name, Distance in km, Available supplies
- Vendors sorted by nearest distance

---

## 📍 Testing Route Highlighting

### Step 1: Wait for Vendors to Load
- Side panel shows "NEAREST VENDORS" section
- Should display 3 vendors with "Route to Here" buttons

### Step 2: Click "Route to Here"
- On any vendor item in side panel
- Two things happen:

#### Route Line Display (IMMEDIATE):
- **Dashed cyan line** (━ ━ ━) appears instantly
- This is the fallback/direct path
- This line is ALWAYS visible (even if API fails)

#### Optimal Route (WITHIN 2-3 seconds):
- **Solid cyan line** (━━━━) replaces dashed line
- Shows actual road-based route
- Calculated by OpenRouteService API

### Step 3: Visual Confirmation
- Route line should be highlighted in **bright cyan** (#00E5FF)
- Line should clearly connect your location to vendor
- Map automatically zooms to fit full route
- **Alert message:** "Route to [Vendor Name] activated! 🗺️"

### Step 4: Switch Routes
- Click "Route to Here" on different vendor
- Previous route clears automatically
- New route displays instantly (dashed)
- Solid route appears once API responds

---

## 🔧 Troubleshooting

### GPS Not Working
**Problem:** GPS status shows 🔴 and "Waiting for location..."

**Solution:**
1. Check browser permissions: Settings → Privacy → Location
2. Ensure you **allowed** location access for localhost:8000
3. Wait 5-10 seconds (geolocation can be slow)
4. Check browser console: `F12` → Console tab
5. Look for errors starting with "GPS Error"

**Fallback:** If GPS unavailable, map defaults to Mumbai center (19.076°, 72.877°)

---

### Route Not Showing
**Problem:** Click "Route to Here" but no line appears

**Solution:**

#### If dashed line should appear but doesn't:
- Check browser console for JavaScript errors: `F12` → Console
- Verify `simpleLine.addTo(map)` is being called

#### If dashed line appears but solid line doesn't:
- This is OK! Dashed line is fallback route
- Solid line requires OpenRouteService API response
- Give it 2-3 seconds to respond
- Check console for "Routing error" messages

#### If both missing:
- Verify Leaflet Routing Machine is loaded:
  - Open DevTools → Network tab
  - Should see: `leaflet-routing-machine.umd.js` ✓ (green)
  - Should see: `leaflet-routing-machine.css` ✓ (green)
- If red (404): CDN issue, try refreshing page

---

### No Vendors Showing
**Problem:** Vendor count shows 0, no vendors in list

**Solution:**
1. Ensure GPS is working (🟢 indicator)
2. Backend should have seed data:
   ```
   GET http://localhost:8000/map-events?type=vendor
   ```
   Should return 4 vendors (Khan Medical, Shree Kirana, etc.)
3. If empty, check events.py line 27 - seed_events() should run

---

## 🧪 Manual API Testing (Advanced)

### Test Nearest Vendors Endpoint
```powershell
curl "http://localhost:8000/nearest-vendors?lat=19.076&lng=72.877&limit=3"
```

**Expected response:**
```json
{
  "user_location": {"lat": 19.076, "lng": 72.877},
  "count": 3,
  "vendors": [
    {
      "id": "ABC1",
      "type": "vendor",
      "label": "Khan Medical",
      "distance_km": 0.52,
      "lat": 19.0720,
      "lng": 72.8720,
      "meta": {"stock": "ORS×200, Insulin×15", "open": true}
    },
    ...
  ]
}
```

### Test Map Events
```powershell
curl "http://localhost:8000/map-events"
```
Should return all events (floods, dangers, SOS, vendors, drones)

---

## 📋 Final Checklist

- [ ] Backend running (port 8000)
- [ ] Page loads at http://localhost:8000/map_gps.html
- [ ] GPS permission requested & granted
- [ ] GPS indicator shows 🟢 (green)
- [ ] Location panel updates with coordinates
- [ ] Vendor count shows 3
- [ ] Vendor list displays in side panel
- [ ] "Route to Here" buttons visible
- [ ] Click button → dashed route appears
- [ ] 2-3 seconds later → solid route appears (if API works)
- [ ] Map zooms to fit route
- [ ] Route is highlighted in bright cyan
- [ ] Map legend visible (bottom-right)
- [ ] Can toggle details panel on/off

**If all ✓: GPS & Route Highlighting = Perfect! 🎉**

---

## 📞 Debug Info to Include if Issues

1. Browser console output: `F12` → Console
2. Network errors: `F12` → Network → filter by "Error"
3. API response: Test endpoint in separate tab
4. Backend logs: Check terminal running uvicorn
5. Approximate GPS location: Share in error report

---

**Last Updated:** March 13, 2026
**DURN Disaster Map v1.0**
