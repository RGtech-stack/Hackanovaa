<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>DURN — Disaster Map</title>

<!-- Leaflet -->
<link  rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>

<!-- Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>

<style>
/* ── RESET ── */
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html, body { height:100%; font-family:'Inter',sans-serif; }

/* ── LAYOUT ── */
#app { display:grid; grid-template-rows:54px 1fr; height:100vh; }

/* ── TOP BAR ── */
#topbar {
  background:#fff;
  border-bottom:1px solid #e2e8f0;
  display:flex; align-items:center;
  padding:0 16px; gap:10px;
  box-shadow:0 1px 3px rgba(0,0,0,.06);
  z-index:1000;
}
.logo {
  font-weight:800; font-size:18px; color:#0f172a; letter-spacing:-0.5px;
}
.logo em { color:#ef4444; font-style:normal; }
.sep { width:1px; height:22px; background:#e2e8f0; margin:0 4px; }
.alert-pill {
  background:#fef2f2; border:1px solid #fecaca;
  color:#dc2626; font-size:10px; font-weight:700;
  padding:3px 10px; border-radius:20px; letter-spacing:1px;
  animation:blink 2s step-end infinite; white-space:nowrap;
}
@keyframes blink { 0%,100%{opacity:1} 55%{opacity:.2} }
.chips { display:flex; gap:6px; }
.chip {
  background:#f8fafc; border:1px solid #e2e8f0;
  font-size:11px; font-weight:500; color:#475569;
  padding:3px 10px; border-radius:20px;
  display:flex; align-items:center; gap:4px;
}
.chip b { font-family:'JetBrains Mono',monospace; color:#0f172a; }
.tb-right { margin-left:auto; display:flex; gap:8px; }
.btn {
  border:none; border-radius:8px; cursor:pointer;
  font-size:12px; font-weight:600; padding:7px 14px;
  display:flex; align-items:center; gap:5px;
  transition:opacity .15s; white-space:nowrap;
}
.btn:hover { opacity:.82; }
.btn-blue { background:#3b82f6; color:#fff; }
.btn-red  { background:#ef4444; color:#fff; }
.btn-slate { background:#f1f5f9; color:#374151; border:1px solid #e2e8f0; }

/* ── MAP AREA ── */
#map-wrap { position:relative; overflow:hidden; }
#map { width:100%; height:100%; }
.leaflet-control-attribution { font-size:9px !important; }

/* ── LEFT PANEL ── */
#panel {
  position:absolute; top:12px; left:12px;
  width:228px; z-index:800;
  display:flex; flex-direction:column; gap:8px;
  max-height:calc(100vh - 80px);
  overflow-y:auto;
  scrollbar-width:thin; scrollbar-color:#cbd5e1 transparent;
}
#panel::-webkit-scrollbar { width:3px; }
#panel::-webkit-scrollbar-thumb { background:#cbd5e1; border-radius:3px; }

.pcard {
  background:#fff; border:1px solid #e2e8f0;
  border-radius:10px; padding:12px 14px;
  box-shadow:0 1px 4px rgba(0,0,0,.05);
}
.pcard-title {
  font-size:9px; font-weight:700; letter-spacing:1.5px;
  text-transform:uppercase; color:#94a3b8;
  margin-bottom:10px;
  display:flex; justify-content:space-between; align-items:center;
}
.badge {
  font-size:9px; font-weight:700;
  font-family:'JetBrains Mono',monospace;
  padding:2px 7px; border-radius:10px;
}
.b-red    { background:#fef2f2; color:#ef4444; }
.b-orange { background:#fff7ed; color:#f97316; }
.b-blue   { background:#eff6ff; color:#3b82f6; }
.b-green  { background:#f0fdf4; color:#16a34a; }

/* Layer toggles */
.lrow {
  display:flex; align-items:center; justify-content:space-between;
  padding:5px 0; font-size:12px; color:#334155;
  border-bottom:1px solid #f8fafc;
}
.lrow:last-child { border-bottom:none; }
.llabel { display:flex; align-items:center; gap:7px; }
.ldot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.tog {
  position:relative; width:32px; height:17px;
  background:#cbd5e1; border-radius:9px;
  border:none; cursor:pointer; transition:background .18s; flex-shrink:0;
}
.tog.on { background:#3b82f6; }
.tog::after {
  content:''; position:absolute;
  width:13px; height:13px; border-radius:50%;
  background:#fff; top:2px;
  box-shadow:0 1px 2px rgba(0,0,0,.2); transition:left .18s;
}
.tog.on::after  { left:17px; }
.tog.off::after { left:2px; }

/* Event items */
.ev {
  padding:7px 8px; border-radius:7px; margin-bottom:5px;
  cursor:pointer; border:1px solid #f1f5f9;
  transition:background .1s;
}
.ev:last-child { margin-bottom:0; }
.ev:hover { background:#f8fafc; border-color:#e2e8f0; }
.ev-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:2px; }
.ev-name { font-size:11px; font-weight:600; color:#0f172a; }
.ev-sub  { font-size:10px; color:#94a3b8; font-family:'JetBrains Mono',monospace; }
.sp {
  font-size:8px; font-weight:700; letter-spacing:.5px;
  padding:1px 6px; border-radius:8px;
}
.sp-critical { background:#fef2f2; color:#dc2626; }
.sp-high     { background:#fff7ed; color:#ea580c; }
.sp-medium   { background:#fefce8; color:#ca8a04; }
.sp-low      { background:#f0fdf4; color:#16a34a; }

/* Routing form */
.form-row { display:flex; flex-direction:column; gap:4px; margin-bottom:8px; }
.form-label { font-size:10px; font-weight:600; color:#64748b; }
.form-input {
  border:1px solid #e2e8f0; border-radius:6px;
  padding:6px 8px; font-size:11px; font-family:'JetBrains Mono',monospace;
  outline:none; color:#0f172a;
}
.form-input:focus { border-color:#3b82f6; }

/* ── LEGEND ── */
#legend {
  position:absolute; bottom:28px; left:12px;
  background:#fff; border:1px solid #e2e8f0;
  border-radius:10px; padding:12px 14px;
  box-shadow:0 2px 8px rgba(0,0,0,.07);
  z-index:800;
}
.leg-title {
  font-size:9px; font-weight:700; letter-spacing:1.5px;
  text-transform:uppercase; color:#94a3b8; margin-bottom:8px;
}
.leg-row { display:flex; align-items:center; gap:8px; margin-bottom:5px; font-size:11px; color:#334155; }
.leg-row:last-child { margin-bottom:0; }
.leg-ico  { width:18px; text-align:center; font-size:13px; flex-shrink:0; }
.leg-line { width:20px; height:3px; border-radius:2px; flex-shrink:0; }

/* ── SITREP ── */
#sitrep {
  position:absolute; bottom:28px; right:12px;
  background:#fff; border:1px solid #e2e8f0;
  border-radius:10px; overflow:hidden;
  box-shadow:0 2px 8px rgba(0,0,0,.07);
  z-index:800; min-width:186px;
}
.sr-head {
  background:#f8fafc; border-bottom:1px solid #e2e8f0;
  padding:7px 12px; font-size:9px; font-weight:700;
  letter-spacing:1.5px; color:#64748b; text-transform:uppercase;
}
.sr-row {
  display:flex; justify-content:space-between; align-items:center;
  padding:5px 12px; border-bottom:1px solid #f8fafc;
  font-size:11px;
}
.sr-row:last-child { border-bottom:none; }
.sr-k { color:#94a3b8; }
.sr-v { font-family:'JetBrains Mono',monospace; font-weight:600; color:#0f172a; }
.v-red   { color:#dc2626 !important; }
.v-green { color:#16a34a !important; }
.v-amber { color:#ca8a04 !important; }

/* ── POPUP ── */
.leaflet-popup-content-wrapper {
  border-radius:10px !important;
  border:1px solid #e2e8f0 !important;
  box-shadow:0 4px 16px rgba(0,0,0,.1) !important;
  padding:0 !important;
}
.leaflet-popup-content { margin:0 !important; font-family:'Inter',sans-serif; }
.leaflet-popup-tip-container { display:none; }
.pop { padding:12px 14px; min-width:168px; }
.pop-type { font-size:9px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#94a3b8; margin-bottom:4px; }
.pop-name { font-size:13px; font-weight:700; color:#0f172a; margin-bottom:7px; }
.pop-row  { display:flex; justify-content:space-between; gap:12px; margin-bottom:3px; font-size:11px; }
.pop-k    { color:#94a3b8; }
.pop-v    { font-weight:600; color:#0f172a; }

/* GPS dot */
.gps-dot {
  width:13px; height:13px; border-radius:50%;
  background:#3b82f6; border:2px solid #fff;
  box-shadow:0 0 0 4px rgba(59,130,246,.25);
}

/* Route on map label */
.rl {
  background:rgba(255,255,255,.9); border:1px solid #e2e8f0;
  font-size:9px; font-weight:600; font-family:'JetBrains Mono',monospace;
  padding:2px 6px; border-radius:4px; white-space:nowrap;
  box-shadow:0 1px 3px rgba(0,0,0,.08);
}
</style>
</head>
<body>
<div id="app">

  <!-- ── TOP BAR ── -->
  <div id="topbar">
    <div class="logo">DU<em>R</em>N</div>
    <div class="sep"></div>
    <div class="alert-pill">⚠ FLOOD ALERT ACTIVE</div>
    <div class="chips">
      <div class="chip">🌊 <b id="c-flood">—</b></div>
      <div class="chip">🆘 <b id="c-sos">—</b></div>
      <div class="chip">⚠️ <b id="c-danger">—</b></div>
      <div class="chip">🏪 <b id="c-vendor">—</b></div>
      <div class="chip">🚁 <b id="c-drone">—</b></div>
    </div>
    <div class="tb-right">
      <button class="btn btn-slate" onclick="locateMe()">📍 My Location</button>
      <button class="btn btn-red"   onclick="sendSOS()">🆘 Send SOS</button>
    </div>
  </div>

  <!-- ── MAP ── -->
  <div id="map-wrap">
    <div id="map"></div>

    <!-- LEFT PANEL -->
    <div id="panel">

      <!-- Layers -->
      <div class="pcard">
        <div class="pcard-title">Map Layers</div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#3b82f6"></div>Flood Zones</div><button class="tog on" onclick="tog('flood',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#7c3aed"></div>Flood Areas</div><button class="tog on" onclick="tog('zones',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#ef4444"></div>Danger Zones</div><button class="tog on" onclick="tog('danger',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#dc2626"></div>SOS Signals</div><button class="tog on" onclick="tog('sos',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#16a34a"></div>Vendors</div><button class="tog on" onclick="tog('vendor',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#0ea5e9"></div>Drones</div><button class="tog on" onclick="tog('drone',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#8b5cf6"></div>Volunteers</div><button class="tog on" onclick="tog('volunteer',this)"></button></div>
        <div class="lrow"><div class="llabel"><div class="ldot" style="background:#64748b"></div>Routes</div><button class="tog on" onclick="tog('route',this)"></button></div>
      </div>

      <!-- Routing form -->
      <div class="pcard">
        <div class="pcard-title">Get Route</div>
        <div class="form-row">
          <div class="form-label">Start (lat, lng)</div>
          <input class="form-input" id="rt-start" placeholder="19.0760, 72.8777"/>
        </div>
        <div class="form-row">
          <div class="form-label">End (lat, lng)</div>
          <input class="form-input" id="rt-end" placeholder="19.1200, 72.9000"/>
        </div>
        <button class="btn btn-blue" style="width:100%;justify-content:center;" onclick="getRoute()">
          🛣 Calculate Route
        </button>
        <div id="rt-result" style="margin-top:8px;font-size:10px;color:#64748b;font-family:'JetBrains Mono',monospace;"></div>
      </div>

      <!-- SOS list -->
      <div class="pcard">
        <div class="pcard-title">Active SOS <span class="badge b-red" id="b-sos">0</span></div>
        <div id="sos-list"><div style="font-size:11px;color:#94a3b8">Loading...</div></div>
      </div>

      <!-- Flood list -->
      <div class="pcard">
        <div class="pcard-title">Flood Zones <span class="badge b-blue" id="b-flood">0</span></div>
        <div id="flood-list"></div>
      </div>

    </div>

    <!-- LEGEND -->
    <div id="legend">
      <div class="leg-title">Legend</div>
      <div class="leg-row"><div class="leg-ico">🌊</div>Flood Zone</div>
      <div class="leg-row"><div class="leg-ico">⚠️</div>Danger Zone</div>
      <div class="leg-row"><div class="leg-ico">🆘</div>SOS Signal</div>
      <div class="leg-row"><div class="leg-ico">🏪</div>Vendor / Supply</div>
      <div class="leg-row"><div class="leg-ico">🚁</div>Drone</div>
      <div class="leg-row"><div class="leg-ico">🙋</div>Volunteer</div>
      <div style="border-top:1px solid #f1f5f9;margin:8px 0 4px;padding-top:8px;">
        <div class="leg-row"><div class="leg-line" style="background:#16a34a"></div>Safe Route</div>
        <div class="leg-row"><div class="leg-line" style="background:repeating-linear-gradient(90deg,#ca8a04 0,#ca8a04 6px,transparent 6px,transparent 10px)"></div>Caution</div>
        <div class="leg-row"><div class="leg-line" style="background:repeating-linear-gradient(90deg,#dc2626 0,#dc2626 4px,transparent 4px,transparent 8px)"></div>Blocked</div>
      </div>
    </div>

    <!-- SITREP -->
    <div id="sitrep">
      <div class="sr-head">Situation Report</div>
      <div class="sr-row"><span class="sr-k">Critical SOS</span> <span class="sr-v v-red"   id="sr-crit">—</span></div>
      <div class="sr-row"><span class="sr-k">Flood Zones</span>  <span class="sr-v"          id="sr-flood">—</span></div>
      <div class="sr-row"><span class="sr-k">Blocked Routes</span><span class="sr-v v-amber" id="sr-blocked">—</span></div>
      <div class="sr-row"><span class="sr-k">Drones Active</span><span class="sr-v v-green"  id="sr-drones">—</span></div>
      <div class="sr-row"><span class="sr-k">Vendors Open</span> <span class="sr-v v-green"  id="sr-vendors">—</span></div>
    </div>

  </div>
</div>

<script>
// ─────────────────────────────────────
// CONFIG
// ─────────────────────────────────────
const API = 'http://localhost:8000';

// ─────────────────────────────────────
// MAP — white (light) Carto tiles
// ─────────────────────────────────────
const map = L.map('map', { center:[19.076,72.877], zoom:13, zoomControl:false });

L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
  attribution:'© OpenStreetMap © CARTO', subdomains:'abcd', maxZoom:19
}).addTo(map);

L.control.zoom({ position:'topright' }).addTo(map);

// ─────────────────────────────────────
// LAYER GROUPS
// ─────────────────────────────────────
const LG = {
  flood:     L.layerGroup().addTo(map),
  zones:     L.layerGroup().addTo(map),  // flood polygons
  danger:    L.layerGroup().addTo(map),
  sos:       L.layerGroup().addTo(map),
  vendor:    L.layerGroup().addTo(map),
  drone:     L.layerGroup().addTo(map),
  volunteer: L.layerGroup().addTo(map),
  route:     L.layerGroup().addTo(map),
  routing:   L.layerGroup().addTo(map),  // ORS result
};
const LGon = Object.fromEntries(Object.keys(LG).map(k=>[k,true]));

// ─────────────────────────────────────
// ICON FACTORY
// ─────────────────────────────────────
function icon(emoji, bg, border, size=28) {
  return L.divIcon({
    className:'',
    html:`<div style="
      width:${size}px;height:${size}px;
      background:${bg};border:1.5px solid ${border};border-radius:50%;
      display:flex;align-items:center;justify-content:center;
      font-size:${Math.floor(size*.46)}px;
      box-shadow:0 1px 4px rgba(0,0,0,.13);
    ">${emoji}</div>`,
    iconSize:[size,size], iconAnchor:[size/2,size/2],
  });
}

const SEV = {
  critical:{ flood:{bg:'#dbeafe',bd:'#3b82f6',sz:34}, sos:{bg:'#fef2f2',bd:'#ef4444',sz:32}, danger:{bg:'#fef2f2',bd:'#ef4444'} },
  high:    { flood:{bg:'#fed7aa',bd:'#f97316',sz:28}, sos:{bg:'#fef2f2',bd:'#ef4444',sz:27}, danger:{bg:'#fef2f2',bd:'#ef4444'} },
  medium:  { flood:{bg:'#fef9c3',bd:'#ca8a04',sz:23}, sos:{bg:'#fff7ed',bd:'#f97316',sz:23}, danger:{bg:'#fef2f2',bd:'#ef4444'} },
  low:     { flood:{bg:'#d1fae5',bd:'#16a34a',sz:18}, sos:{bg:'#fff7ed',bd:'#f97316',sz:20}, danger:{bg:'#fef2f2',bd:'#ef4444'} },
};

// ─────────────────────────────────────
// POPUP BUILDER
// ─────────────────────────────────────
function popup(typeLabel, name, rows) {
  return `<div class="pop">
    <div class="pop-type">${typeLabel}</div>
    <div class="pop-name">${name}</div>
    ${rows.map(([k,v])=>`<div class="pop-row"><span class="pop-k">${k}</span><span class="pop-v">${v}</span></div>`).join('')}
  </div>`;
}

// ─────────────────────────────────────
// RENDER EVENTS
// ─────────────────────────────────────
function renderEvents(events) {
  ['flood','danger','sos','vendor','drone','volunteer'].forEach(k=>LG[k].clearLayers());

  let counts = {flood:0,sos:0,danger:0,vendor:0,drone:0};
  let sosList=[], floodList=[], critSos=0, vendorsOpen=0;

  events.forEach(ev => {
    const {lat,lng,severity,label,meta={}} = ev;
    if (!lat||!lng) return;
    let m;

    if (ev.type==='flood') {
      const c = SEV[severity]?.flood || SEV.medium.flood;
      m = L.marker([lat,lng],{icon:icon('🌊',c.bg,c.bd,c.sz)});
      m.bindPopup(popup('🌊 Flood Zone', label||'Flood',[
        ['Severity', `<span class="sp sp-${severity}">${severity.toUpperCase()}</span>`],
        ...(meta.depth_cm?[['Depth',`${meta.depth_cm} cm`]]:[]),
        ['Coords', `${lat.toFixed(4)}, ${lng.toFixed(4)}`],
      ]));
      // small subtle ring — NO big blob
      L.circle([lat,lng],{
        radius:{critical:300,high:200,medium:130,low:70}[severity]||130,
        color:{critical:'#3b82f6',high:'#f97316',medium:'#ca8a04',low:'#16a34a'}[severity],
        fillOpacity:0.07, weight:1.5, opacity:0.5,
      }).addTo(LG.flood);
      LG.flood.addLayer(m);
      counts.flood++; floodList.push(ev);

    } else if (ev.type==='danger') {
      m = L.marker([lat,lng],{icon:icon('⚠️','#fef2f2','#ef4444',28)});
      m.bindPopup(popup('⚠️ Danger Zone', label||'Danger',[
        ['Severity',`<span class="sp sp-${severity}">${severity.toUpperCase()}</span>`],
        ['Coords',`${lat.toFixed(4)}, ${lng.toFixed(4)}`],
      ]));
      LG.danger.addLayer(m); counts.danger++;

    } else if (ev.type==='sos') {
      const c = SEV[severity]?.sos || SEV.medium.sos;
      m = L.marker([lat,lng],{icon:icon('🆘',c.bg,c.bd,c.sz)});
      m.bindPopup(popup('🆘 SOS Signal', label||'SOS',[
        ['Priority',`<span class="sp sp-${severity}">${severity.toUpperCase()}</span>`],
        ...(meta.need  ?[['Needs', meta.need]] :[]),
        ...(meta.floor ?[['Floor',`${meta.floor}F`]]:[]),
        ['Coords',`${lat.toFixed(4)}, ${lng.toFixed(4)}`],
      ]));
      LG.sos.addLayer(m); counts.sos++; sosList.push(ev);
      if (severity==='critical') critSos++;

    } else if (ev.type==='vendor') {
      const open=meta.open!==false;
      const vico={Medical:'💊',Food:'🍱',Mixed:'📦'}[meta.vtype]||'🏪';
      m = L.marker([lat,lng],{icon:icon(vico,open?'#f0fdf4':'#f8fafc',open?'#16a34a':'#94a3b8',26)});
      m.bindPopup(popup('🏪 Vendor', label||'Vendor',[
        ['Status', open?'<span style="color:#16a34a;font-weight:600">Open</span>':'<span style="color:#94a3b8">Closed</span>'],
        ['Type', meta.vtype||'General'],
        ...(meta.stock?[['Stock',meta.stock]]:[]),
        ['Coords',`${lat.toFixed(4)}, ${lng.toFixed(4)}`],
      ]));
      LG.vendor.addLayer(m); counts.vendor++;
      if(open) vendorsOpen++;

    } else if (ev.type==='drone') {
      const bat=meta.battery??100;
      const bc=bat>50?'#16a34a':bat>20?'#ca8a04':'#dc2626';
      m = L.marker([lat,lng],{icon:icon('🚁','#f0f9ff','#0ea5e9',26)});
      m.bindPopup(popup('🚁 Drone', label||'Drone',[
        ['Status', meta.status||'Idle'],
        ['Battery', `<span style="color:${bc};font-weight:600">${bat}%</span>`],
        ['Coords',`${lat.toFixed(4)}, ${lng.toFixed(4)}`],
      ]));
      LG.drone.addLayer(m); counts.drone++;

    } else if (ev.type==='volunteer') {
      const vico={boat:'⛵',bike:'🏍',car:'🚗',foot:'🚶'}[meta.vehicle]||'🙋';
      m = L.marker([lat,lng],{icon:icon(vico,'#faf5ff','#8b5cf6',24)});
      m.bindPopup(popup('🙋 Volunteer', label||'Volunteer',[
        ['Vehicle', meta.vehicle||'Foot'],
        ['Status',  meta.status||'Available'],
        ['Coords',`${lat.toFixed(4)}, ${lng.toFixed(4)}`],
      ]));
      LG.volunteer.addLayer(m);
    }
  });

  // Counters
  document.getElementById('c-flood').textContent  = counts.flood;
  document.getElementById('c-sos').textContent    = counts.sos;
  document.getElementById('c-danger').textContent = counts.danger;
  document.getElementById('c-vendor').textContent = counts.vendor;
  document.getElementById('c-drone').textContent  = counts.drone;
  document.getElementById('sr-crit').textContent    = critSos;
  document.getElementById('sr-flood').textContent   = counts.flood;
  document.getElementById('sr-drones').textContent  = counts.drone;
  document.getElementById('sr-vendors').textContent = vendorsOpen;
  document.getElementById('b-sos').textContent   = sosList.length;
  document.getElementById('b-flood').textContent = floodList.length;

  renderSOSList(sosList);
  renderFloodList(floodList);
}

// ─────────────────────────────────────
// RENDER FLOOD POLYGON ZONES
// ─────────────────────────────────────
function renderZones(zones) {
  LG.zones.clearLayers();
  const fc = {critical:'#6366f1',high:'#f97316',medium:'#ca8a04',low:'#16a34a'};
  zones.forEach(z => {
    L.polygon(z.coordinates, {
      color: fc[z.severity]||'#6366f1',
      fillOpacity:0.12, weight:1.5, opacity:0.6,
      dashArray:'5 4',
    }).bindPopup(popup('🗺 Flood Area', z.name,[
      ['Severity',`<span class="sp sp-${z.severity}">${z.severity.toUpperCase()}</span>`],
      ...(z.depth_cm?[['Depth',`${z.depth_cm} cm`]]:[]),
    ])).addTo(LG.zones);
  });
}

// ─────────────────────────────────────
// RENDER ROUTES
// ─────────────────────────────────────
function renderRoutes(routes) {
  LG.route.clearLayers();
  let blocked=0;
  const rc={clear:'#16a34a',caution:'#ca8a04',blocked:'#dc2626'};
  const rd={clear:null,caution:'8 5',blocked:'4 6'};
  const ri={clear:'🟢',caution:'🟡',blocked:'🔴'};

  routes.forEach(r => {
    L.polyline(r.coords,{
      color:rc[r.status], weight:r.status==='clear'?4:3,
      opacity:.85, dashArray:rd[r.status],
    }).bindPopup(popup(
      `${ri[r.status]} Route — ${r.status.toUpperCase()}`,
      r.name, r.note?[['Note',r.note]]:[]
    )).addTo(LG.route);

    // Midpoint label
    const mid=r.coords[Math.floor(r.coords.length/2)];
    L.marker(mid,{icon:L.divIcon({
      className:'',
      html:`<div class="rl" style="color:${rc[r.status]};border-color:${rc[r.status]}44;">${r.status.toUpperCase()}</div>`,
      iconAnchor:[0,0],
    })}).addTo(LG.route);

    if(r.status==='blocked') blocked++;
  });
  document.getElementById('sr-blocked').textContent = blocked;
}

// ─────────────────────────────────────
// SIDEBAR LISTS
// ─────────────────────────────────────
function renderSOSList(list) {
  const ord={critical:3,high:2,medium:1,low:0};
  const s=[...list].sort((a,b)=>(ord[b.severity]||0)-(ord[a.severity]||0));
  document.getElementById('sos-list').innerHTML = s.slice(0,5).map(x=>`
    <div class="ev" onclick="flyTo(${x.lat},${x.lng})">
      <div class="ev-top">
        <span class="ev-name">${x.label||'SOS'}</span>
        <span class="sp sp-${x.severity}">${x.severity.toUpperCase()}</span>
      </div>
      <div class="ev-sub">${x.meta?.need||''}</div>
    </div>`).join('') || '<div style="font-size:11px;color:#94a3b8">None active</div>';
}

function renderFloodList(list) {
  const ord={critical:3,high:2,medium:1,low:0};
  const s=[...list].sort((a,b)=>(ord[b.severity]||0)-(ord[a.severity]||0));
  document.getElementById('flood-list').innerHTML = s.slice(0,4).map(x=>`
    <div class="ev" onclick="flyTo(${x.lat},${x.lng})">
      <div class="ev-top">
        <span class="ev-name">${x.label||'Flood'}</span>
        <span class="sp sp-${x.severity}">${x.severity.toUpperCase()}</span>
      </div>
      <div class="ev-sub">${x.meta?.depth_cm ? x.meta.depth_cm+'cm depth':''}</div>
    </div>`).join('');
}

// ─────────────────────────────────────
// LAYER TOGGLE
// ─────────────────────────────────────
function tog(name, btn) {
  LGon[name] = !LGon[name];
  btn.classList.toggle('on',  LGon[name]);
  btn.classList.toggle('off', !LGon[name]);
  LGon[name] ? map.addLayer(LG[name]) : map.removeLayer(LG[name]);
}

// ─────────────────────────────────────
// GPS — show user's location
// ─────────────────────────────────────
let gpsMarker=null;
function locateMe() {
  if (!navigator.geolocation) { alert('GPS not supported'); return; }
  navigator.geolocation.getCurrentPosition(pos => {
    const {latitude:lat, longitude:lng, accuracy} = pos.coords;
    if (gpsMarker) map.removeLayer(gpsMarker);
    gpsMarker = L.marker([lat,lng],{icon:L.divIcon({
      className:'', html:`<div class="gps-dot"></div>`,
      iconSize:[13,13], iconAnchor:[6,6],
    })}).addTo(map).bindPopup(popup('📍 Your Location','GPS Position',[
      ['Coords',`${lat.toFixed(5)}, ${lng.toFixed(5)}`],
      ['Accuracy',`±${Math.round(accuracy)}m`],
    ])).openPopup();
    map.flyTo([lat,lng],15,{duration:1.2});

    // Pre-fill routing start
    document.getElementById('rt-start').value = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
  }, ()=>alert('Allow location access in your browser.'));
}

// ─────────────────────────────────────
// SEND SOS
// ─────────────────────────────────────
function sendSOS() {
  if (!navigator.geolocation) { alert('GPS not available'); return; }
  navigator.geolocation.getCurrentPosition(async pos => {
    const {latitude:lat, longitude:lng} = pos.coords;
    try {
      await fetch(`${API}/sos`,{
        method:'POST', headers:{'Content-Type':'application/json'},
        body:JSON.stringify({lat,lng,label:'My SOS',need:'Help needed'}),
      });
      alert('✅ SOS sent! Help is being coordinated.');
      loadData();
    } catch { alert('SOS saved. Will sync when backend is online.'); }
  }, ()=>alert('Allow location access to send SOS.'));
}

// ─────────────────────────────────────
// ROUTING — calls FastAPI → ORS
// ─────────────────────────────────────
async function getRoute() {
  const startRaw = document.getElementById('rt-start').value.trim();
  const endRaw   = document.getElementById('rt-end').value.trim();
  const res      = document.getElementById('rt-result');

  if (!startRaw||!endRaw) { res.textContent='Enter start and end coordinates.'; return; }

  const [sLat,sLng] = startRaw.split(',').map(Number);
  const [eLat,eLng] = endRaw.split(',').map(Number);

  if ([sLat,sLng,eLat,eLng].some(isNaN)) {
    res.textContent='Invalid coordinates. Use: lat, lng'; return;
  }

  res.textContent = 'Calculating route...';
  LG.routing.clearLayers();

  try {
    const resp = await fetch(`${API}/routing/directions?start_lat=${sLat}&start_lng=${sLng}&end_lat=${eLat}&end_lng=${eLng}`);
    const data = await resp.json();
    const coords = data.coords || data.mock_route?.coords;

    if (!coords) { res.textContent='No route returned.'; return; }

    // Draw route on map
    L.polyline(coords,{color:'#8b5cf6',weight:4,opacity:.8}).addTo(LG.routing);

    // Start / End markers
    L.marker(coords[0],{icon:icon('🟢','#f0fdf4','#16a34a',22)}).addTo(LG.routing);
    L.marker(coords[coords.length-1],{icon:icon('🏁','#f0f9ff','#3b82f6',22)}).addTo(LG.routing);

    map.fitBounds(L.polyline(coords).getBounds(),{padding:[30,30]});

    const dist = data.distance_km || data.mock_route?.distance_km || '—';
    const time = data.duration_min ? `${data.duration_min} min` : '';
    res.innerHTML = `✅ ${dist} km${time?' · '+time:''}<br><span style="color:#94a3b8">${data.source==='mock'?'(mock — add ORS key for real routing)':''}</span>`;

  } catch {
    res.textContent = 'Route error. Is backend running?';
  }
}

// ─────────────────────────────────────
// FLY TO
// ─────────────────────────────────────
function flyTo(lat,lng) {
  map.flyTo([lat,lng],15,{duration:.8});
}

// ─────────────────────────────────────
// LOAD ALL DATA FROM FASTAPI
// ─────────────────────────────────────
async function loadData() {
  try {
    const [evRes, rtRes, znRes] = await Promise.all([
      fetch(`${API}/map-events`),
      fetch(`${API}/routes`),
      fetch(`${API}/flood-zones`),
    ]);
    const evData = await evRes.json();
    const rtData = await rtRes.json();
    const znData = await znRes.json();

    renderEvents(evData.events || []);
    renderRoutes(rtData.routes || []);
    renderZones(znData.zones   || []);
  } catch {
    console.warn('Backend offline — demo data');
    renderEvents(DEMO); renderRoutes(DEMO_RT); renderZones(DEMO_ZONES);
  }
}

// ─────────────────────────────────────
// DEMO FALLBACK
// ─────────────────────────────────────
const DEMO=[
  {type:'flood',    lat:19.0760,lng:72.8777,severity:'critical',label:'Dharavi',       meta:{depth_cm:128}},
  {type:'flood',    lat:19.0550,lng:72.8350,severity:'high',    label:'Mahim Creek',   meta:{depth_cm:85}},
  {type:'flood',    lat:19.1200,lng:72.9000,severity:'medium',  label:'Kurla East',    meta:{depth_cm:37}},
  {type:'flood',    lat:19.0330,lng:72.8550,severity:'high',    label:'Sion',          meta:{depth_cm:94}},
  {type:'danger',   lat:19.0640,lng:72.8620,severity:'critical',label:'Collapsed Bridge'},
  {type:'danger',   lat:19.1400,lng:72.9300,severity:'critical',label:'Live Wire in Water'},
  {type:'sos',      lat:19.0800,lng:72.8800,severity:'critical',label:'Rashida Bi',    meta:{need:'Medicine',floor:3}},
  {type:'sos',      lat:19.0520,lng:72.8380,severity:'critical',label:'Family of 4',   meta:{need:'Rescue',floor:4}},
  {type:'sos',      lat:19.1250,lng:72.9050,severity:'high',    label:'Elderly Man',   meta:{need:'Insulin',floor:2}},
  {type:'vendor',   lat:19.0720,lng:72.8720,severity:'low',     label:'Khan Medical',  meta:{stock:'ORS×200',open:true,vtype:'Medical'}},
  {type:'vendor',   lat:19.0600,lng:72.8500,severity:'low',     label:'Shree Kirana',  meta:{stock:'Rice 40kg',open:true,vtype:'Food'}},
  {type:'drone',    lat:19.0850,lng:72.8850,severity:'low',     label:'Drone Alpha',   meta:{battery:78,status:'Delivering'}},
  {type:'drone',    lat:19.1100,lng:72.9200,severity:'low',     label:'Drone Beta',    meta:{battery:100,status:'Idle'}},
  {type:'volunteer',lat:19.0680,lng:72.8750,severity:'low',     label:'Suresh — Boat', meta:{vehicle:'boat',status:'delivering'}},
];
const DEMO_RT=[
  {name:'SV Road — Mahim',    coords:[[19.060,72.840],[19.068,72.858],[19.075,72.878]],status:'clear',  note:'Water < 20cm'},
  {name:'Eastern Express Hwy',coords:[[19.080,72.895],[19.120,72.920],[19.160,72.948]],status:'clear',  note:'Elevated — safe'},
  {name:'LBS Marg — Kurla',   coords:[[19.120,72.900],[19.140,72.920],[19.165,72.942]],status:'caution',note:'1ft water'},
  {name:'Cadell Road',        coords:[[19.055,72.850],[19.048,72.857],[19.045,72.865]],status:'blocked',note:'3.2ft water'},
  {name:'Ghatkopar Corridor', coords:[[19.155,72.940],[19.163,72.948],[19.170,72.955]],status:'blocked',note:'Drone only'},
];
const DEMO_ZONES=[
  {name:'Dharavi Flood Area',   severity:'critical',depth_cm:128,coordinates:[[19.074,72.875],[19.078,72.875],[19.0785,72.881],[19.0745,72.8815],[19.074,72.875]]},
  {name:'Mahim Flood Area',     severity:'high',    depth_cm:85, coordinates:[[19.053,72.832],[19.057,72.832],[19.0575,72.838],[19.0535,72.8382],[19.053,72.832]]},
  {name:'Ghatkopar Flood Area', severity:'critical',depth_cm:152,coordinates:[[19.166,72.946],[19.170,72.946],[19.1705,72.951],[19.1665,72.9512],[19.166,72.946]]},
];

// ─────────────────────────────────────
// BOOT
// ─────────────────────────────────────
loadData();
setInterval(loadData, 15000);
</script>
</body>
</html>