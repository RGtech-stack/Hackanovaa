# 🗺️ Map GPS v2.0 — Visual Guide & Quick Reference

## Screen Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│ DUR N  ⚠ FLOOD ALERT  📍GPS: Located  🏪Vendors: 4        │ ← Top Bar
├────────────────────────────────┬──────────────────────────┤
│                                │  YOUR LOCATION           │
│                                │  ┌──────────────────┐    │
│                                │  │ Lat: 19.0760     │    │
│      🗺️ MAP AREA              │  │ Lng: 72.8777     │    │
│                                │  └──────────────────┘    │
│   🌊 Flood Zones (polygons)   │                          │
│   🟢 Vendor ✨ (glowing)       │  NEAREST VENDOR          │
│   🆘 SOS Signals (pulsing)     │  ┌──────────────────┐    │
│   ⚠️ Danger Zones             │  │🏪 Khan Medical   │    │
│   🚁 Drones                    │  │📍 0.52 km away   │    │
│   👤 Volunteers                │  │✓ Open            │    │
│   🛣️ Routes (colored lines)    │  └──────────────────┘    │
│                                │                          │
│                                │  MAP LAYERS              │
│                                │  □ 🌊 Flood Zones       │
│                                │  □ ⚠️ Danger Zones      │
│                                │  □ 🆘 SOS Signals       │
│                                │  □ 🏪 Vendors          │
│                                │  □ 🛣️ Routes           │
│                                │  □ 🚁 Drones           │
│                                │  □ 👤 Volunteers        │
├┤ GPS STATUS                    └──────────────────────────┤
│ 🟢 Located                                                 │
│ Vendors: 4                     LEGEND (bottom-right)      │
│                                ┌──────────────────────┐  │
└────────────────────────────────┤ 📍 Your Location     │──┘
                                 │ 🌊 Flood Zone        │
                                 │ ⚠️ Danger Zone       │
                                 │ 🆘 SOS Signal        │
                                 │ 🏪 Vendor Supply     │
                                 │ 🚁 Drone             │
                                 │ 👤 Volunteer         │
                                 │                      │
                                 │ 🟢 Safe Route        │
                                 │ 🟡 Caution Route     │
                                 │ 🔴 Blocked Route     │
                                 └──────────────────────┘
```

---

## Icon Guide

### Your Location
```
    🔴 Red (Waiting)
    🟢 Green (Located) ← Shows when GPS is active
```
- **Size:** 40×40 pixels
- **Effect:** Pulsing circle with glow
- **Update:** Real-time

### Danger Zones
```
    ⚠️ 
    Size: 36×36 px
    Color: Red glow (#FF1744)
    Examples: Collapsed bridge, live wire, wall collapse
```

### SOS Signals
```
    🆘 (Pulsing)
    Size: 36×36 px
    Color: Red glow, pulses up/down
    Examples: Rashida Bi (Medicine floor 3), Family of 4 (Rescue floor 4)
```

### Vendors
```
    🏪
    Size: 36×36 px
    Color: Green glow (#00E676)
    Nearest: ✨ Green glowing circle (radius 150m)
    Examples: Khan Medical, Shree Kirana, City Pharmacy
```

### Drones
```
    🚁
    Size: 36×36 px
    Color: Cyan glow (#00E5FF)
    Examples: Drone Alpha (Delivering, 78% battery), Drone Beta (Idle, 100%)
```

### Volunteers
```
    👤
    Size: 36×36 px
    Color: Yellow glow (#FFD600)
    Examples: Suresh (Boat, delivering), Priya (Bike, available)
```

### Flood Zones
```
    🌊 (Polygon + Circle)
    Polygon: Actual flood area
    Circle: Radius based on water depth
    
    Colors by severity:
    🔴 Critical: Red (#FF1744)
    🟠 High:     Orange (#FF6D00)
    🟡 Medium:   Yellow (#FFD600)
    
    Calculation: Radius (m) = Depth (cm) × 2.5
    Example: 128 cm flood → 320 m radius circle
```

### Routes
```
    🟢 Safe Route:     ━━━━━━━ Green solid line
    🟡 Caution Route:  ━ ━ ━ ━ Yellow dashed line
    🔴 Blocked Route:  ┆ ┆ ┆ ┆ Red dotted line
    
    Colors: Green (#00E676), Yellow (#FFD600), Red (#FF1744)
    Width: 4px, Opacity: 80%
```

---

## User Interactions

### 1️⃣ Loading the Map
```
Step 1: Open browser to http://localhost:8000/map_gps.html
Step 2: Browser asks "Allow location access?"
Step 3: Click "Allow"
Step 4: Wait 5-10 seconds
Result: 🟢 GPS indicator appears, your location marked
```

### 2️⃣ Viewing Your Location
```
Side Panel:
┌──────────────────────┐
│ YOUR LOCATION        │
│ Lat: 19.0760        │
│ Lng: 72.8777        │
│ Updated: Real-time   │
└──────────────────────┘

Map:
📍 Your location marker (pulsing)
🔵 Zoom automatically centers on you
```

### 3️⃣ Finding Nearest Vendor
```
Automatic: Happens every time GPS updates (as you move)

Side Panel:
┌──────────────────────┐
│ NEAREST VENDOR       │
│ 🏪 Khan Medical     │
│ 📍 0.52 km away     │
│ ORS×200, Insulin×15 │
│ ✓ Open              │
└──────────────────────┘

Map:
🏪 Vendor marker (green glow)
✨ Green pulsing circle (150m radius around vendor)
```

### 4️⃣ Toggling Map Layers
```
Side Panel MAP LAYERS section:

Click checkbox to hide/show:
☑ 🌊 Flood Zones    ← Click to toggle flood areas
☑ ⚠️ Danger Zones   ← Click to toggle dangers
☑ 🆘 SOS Signals    ← Click to toggle rescue requests
☑ 🏪 Vendors        ← Click to toggle supply stores
☑ 🛣️ Routes         ← Click to toggle travel routes
☑ 🚁 Drones        ← Click to toggle rescue drones
☑ 👤 Volunteers     ← Click to toggle ground volunteers

Map updates INSTANTLY when toggled
```

### 5️⃣ Clicking on Map Features
```
Click on Flood Zone:
┌─────────────────────────────┐
│ 🌊 FLOOD ZONE               │
│ Dharavi                     │
│ Depth: 128 cm               │
│ Radius: 0.32 km             │
│ Severity: CRITICAL          │
└─────────────────────────────┘

Click on Vendor:
┌─────────────────────────────┐
│ 🏪 VENDOR                   │
│ Khan Medical                │
│ Severity: LOW               │
│ {"stock": "ORS×200..."}     │
└─────────────────────────────┘

Click on Route:
┌─────────────────────────────┐
│ 🛣️ ROUTE                     │
│ SV Road (CLEAR)             │
│ Status: CLEAR               │
│ Passable — water < 20cm     │
└─────────────────────────────┘
```

---

## Color Legend Reference

### Flood Severity
| Severity | Color | Example |
|----------|-------|---------|
| 🔴 Critical | Red (#FF1744) | Ghatkopar (152 cm) |
| 🟠 High | Orange (#FF6D00) | Mahim (85 cm) |
| 🟡 Medium | Yellow (#FFD600) | Kurla (37 cm) |

### Route Status
| Status | Style | Color |
|--------|-------|-------|
| 🟢 Safe | Solid line | Green (#00E676) |
| 🟡 Caution | Dashed | Yellow (#FFD600) |
| 🔴 Blocked | Dotted | Red (#FF1744) |

### Event Priority
| Priority | Icon | Color |
|----------|------|-------|
| 🆘 Critical | SOS (pulsing) | Red (#FF1744) |
| ⚠️ High | Danger | Orange/Red |
| ℹ️ Info | Vendor/Drone | Green/Cyan |

---

## Keyboard & Navigation Tips

```
Mouse Controls:
- Drag to pan map
- Scroll wheel to zoom
- Double-click to zoom in
- Ctrl + Scroll to zoom out

Map Buttons:
- Zoom in/out buttons  (top-left)
- Reset view           (auto on location update)
- Fullscreen            (available on some browsers)

Side Panel:
- Scroll if content overflows
- Checkboxes toggle layers instantly
- Auto-hides on side of screen
- Always visible (no closing)
```

---

## Expected Data on Map

### Vendors (🏪)
1. Khan Medical (19.0720, 72.8720) ← 0.52 km
2. Shree Kirana (19.0600, 72.8500) ← 1.75 km
3. City Pharmacy (19.1300, 72.9100) ← 4.2 km
4. Ghatkopar Hub (19.1600, 72.9400) ← 8.5 km

### Flood Zones (🌊)
1. Dharavi (128 cm, Critical, Red)
2. Mahim Creek (85 cm, High, Orange)
3. Ghatkopar (152 cm, Critical, Red)

### SOS Signals (🆘)
1. Rashida Bi (Medicine, floor 3)
2. Family of 4 (Rescue, floor 4)
3. Elderly Man (Insulin, floor 2)
4. 3 Children (Food + Water, floor 1)

### Safe Routes (🟢)
- SV Road to Mahim Causeway (Clear)
- Eastern Express Highway (Clear)

### Caution Routes (🟡)
- LBS Marg to Kurla (Caution)

### Blocked Routes (🔴)
- Cadell Road (Blocked)
- Ghatkopar Corridor (Drone-only)

---

## Troubleshooting Visual

### Problem: GPS shows 🔴 red (not responding)
```
Checklist:
□ Phone/browser has location enabled
□ Website has location permission (check: Settings > Privacy > Location)
□ GPS takes 5-10 seconds, wait longer
□ Try moving around to help signal lock
□ Fallback: Map defaults to Mumbai center (19.076, 72.877)
```

### Problem: Map is blank/loading
```
Checklist:
□ Backend server running (port 8000)
□ Check browser console for errors (F12)
□ Refresh page (Ctrl + R or Cmd + R)
□ Check network (F12 > Network) for failed requests
□ Try different browser
```

### Problem: Vendor circle not glowing
```
Checklist:
□ Check "🏪 Vendors" toggle is ON
□ Zoom in to see 150m circle better
□ Click vendor marker to confirm it exists
□ Check side panel for "NEAREST VENDOR" info
```

### Problem: Flood zones not showing
```
Checklist:
□ Check "🌊 Flood Zones" toggle is ON
□ Zoom to Mumbai area (19.0-19.2 latitude)
□ Click on polygon/circle for details
□ Check backend has flood zones: http://localhost:8000/flood-zones
```

---

## Performance Notes

| Action | Speed | Expected |
|--------|-------|----------|
| Page Load | <2s | ✅ Fast |
| GPS Signal | 3-10s | ✅ Normal |
| Layer Toggle | <100ms | ✅ Instant |
| Vendor Update | Real-time | ✅ Live |
| Zoom/Pan | Smooth | ✅ 60fps |
| Popup Display | <100ms | ✅ Instant |

---

## Important Notes

✔️ **Always-Visible Panel:** No button to toggle, panel always on right
✔️ **Real-Time Updates:** Vendor location updates as GPS updates
✔️ **Graceful Fallback:** GPS fails → defaults to Mumbai center
✔️ **All Layers On:** Except toggles hide specific types
✔️ **Dark Theme:** Automatically adapts to different backgrounds
✔️ **Mobile Ready:** Works on phones, tablets, desktop

---

**Version:** 2.0 (Complete Redesign)
**Last Updated:** March 13, 2026
**Status:** 🟢 Ready to Use
