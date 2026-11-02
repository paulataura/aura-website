"""Custom icons, diagrams and picture-led layouts for the site.

Icons are simple line drawings in the brand colours (currentColor), so a
rebrand only needs the colour tokens in styles.css changing.
"""
from template import e

_I = {
    "pump": '<circle cx="9" cy="13" r="5"/><path d="M14 13h4v-3h3v6h-3v-3"/><path d="M9 8V4h4"/><circle cx="9" cy="13" r="1.5"/>',
    "wetwell": '<path d="M5 3v15a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3V3"/><path d="M5 12c1.2 1 2.3 1 3.5 0s2.3-1 3.5 0 2.3 1 3.5 0 2.3-1 3.5 0"/>',
    "report": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1"/><path d="M8.5 10h7M8.5 14h7M8.5 18h4"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    "wrench": '<path d="M14.5 5.5a4 4 0 0 0 5 5L12 18a2.1 2.1 0 0 1-3-3l7.5-7.5"/><path d="M14.5 5.5 17 3l4 4-2.5 2.5"/>',
    "truck": '<path d="M2 7h11v9H2zM13 10h4l3 3v3h-7z"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>',
    "camera": '<rect x="2" y="7" width="14" height="10" rx="2"/><path d="m16 11 5-3v8l-5-3"/><circle cx="9" cy="12" r="2.2"/>',
    "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    "signal": '<path d="M12 20v-8"/><circle cx="12" cy="10" r="1.6"/><path d="M8 6.5a6 6 0 0 0 0 7M16 6.5a6 6 0 0 1 0 7M5 4a10 10 0 0 0 0 12M19 4a10 10 0 0 1 0 12"/>',
    "shield": '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19 13 11"/>',
}


def icon(name, size=28):
    return (f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')


def icon_cards(items, head=None, intro=None, alt=False):
    """items: (icon, title, text)."""
    cards = "".join(f'<div class="card icon-card"><span class="icon-badge">{icon(i)}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, t, d in items)
    hd = f'<div class="block-head"><h2>{e(head)}</h2>{f"<p>{e(intro)}</p>" if intro else ""}</div>' if head else ""
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap">{hd}<div class="card-grid">{cards}</div></div></section>'


def photo_cards(items, head=None, alt=False):
    """items: (image, title, text, href)."""
    cards = "".join(
        f'<a class="card photo-card" href="{h}"><div class="photo-card-img"><img src="{img}" alt="" loading="lazy" width="800" height="500"></div>'
        f'<div class="photo-card-body"><h3>{e(t)}</h3><p>{e(d)}</p><strong>Find out more ↗</strong></div></a>' for img, t, d, h in items)
    hd = f'<div class="block-head"><h2>{e(head)}</h2></div>' if head else ""
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap">{hd}<div class="card-grid">{cards}</div></div></section>'


def image_row(*, image=None, visual_html=None, alt_text="", eyebrow=None, head, paras, ticks=(), reverse=False, tint=False):
    """Text beside a large photo (or any visual), alternating sides down the page."""
    eb = f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ""
    p = "".join(f"<p>{e(x)}</p>" for x in paras)
    t = f'<ul class="tick-list">{"".join(f"<li>{e(x)}</li>" for x in ticks)}</ul>' if ticks else ""
    vis = visual_html or f'<div class="row-photo"><img src="{image}" alt="{e(alt_text)}" loading="lazy" width="1600" height="1067"></div>'
    return (f'<section class="block{" alt" if tint else ""}"><div class="wrap image-row{" reverse" if reverse else ""}">'
            f'<div class="image-row-text">{eb}<h2>{e(head)}</h2>{p}{t}</div><div class="image-row-visual">{vis}</div></div></section>')


def pump_station_diagram():
    """Cutaway of a typical package pump station with numbered points."""
    num = lambda n, x, y: (f'<g class="dg-num"><circle cx="{x}" cy="{y}" r="15"/><text x="{x}" y="{y + 5}" text-anchor="middle">{n}</text></g>')
    svg = f'''<svg class="diagram" viewBox="0 0 900 520" role="img" aria-labelledby="dgT dgD" xmlns="http://www.w3.org/2000/svg">
  <title id="dgT">Cutaway diagram of a pump station</title>
  <desc id="dgD">Sewage flows in through the inlet into the wet well. Level floats tell the control panel when to start the duty pump, which pushes the sewage out through the rising main. A standby pump takes over if the duty pump fails, and telemetry sends alarms and data.</desc>
  <defs>
    <pattern id="soil" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#e7eee4"/><circle cx="3" cy="4" r="1" fill="#cfdccb"/><circle cx="10" cy="10" r="1.2" fill="#cfdccb"/></pattern>
    <marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 10 5 0 10z" fill="#5c9c3f"/></marker>
  </defs>
  <rect x="0" y="0" width="900" height="170" fill="#f5f9f6"/>
  <rect x="0" y="170" width="900" height="350" fill="url(#soil)"/>
  <line x1="0" y1="170" x2="900" y2="170" stroke="#7a9a84" stroke-width="3"/>
  <!-- kiosk -->
  <rect x="610" y="70" width="120" height="100" rx="6" fill="#0b3425"/>
  <rect x="624" y="84" width="92" height="56" rx="3" fill="#123f2d" stroke="#3b6951"/>
  <circle cx="640" cy="98" r="5" fill="#8bd02d"/><circle cx="656" cy="98" r="5" fill="#8bd02d"/><circle cx="672" cy="98" r="5" fill="#e3a51d"/>
  <rect x="636" y="112" width="68" height="6" rx="3" fill="#3b6951"/><rect x="636" y="124" width="44" height="6" rx="3" fill="#3b6951"/>
  <line x1="715" y1="70" x2="715" y2="32" stroke="#0b3425" stroke-width="4"/>
  <path d="M703 30a16 16 0 0 1 24 0M697 22a26 26 0 0 1 36 0" fill="none" stroke="#8bd02d" stroke-width="3" stroke-linecap="round"/>
  <!-- cable to well -->
  <path d="M640 170 V188 H470 V205" fill="none" stroke="#0b3425" stroke-width="2" stroke-dasharray="6 5"/>
  <!-- wet well -->
  <rect x="240" y="166" width="280" height="324" rx="10" fill="#6f8579"/>
  <rect x="256" y="176" width="248" height="300" rx="6" fill="#f3f6f4"/>
  <rect x="256" y="330" width="248" height="146" fill="#cfe5ec"/>
  <path d="M256 330c20-6 40-6 62 0s42 6 62 0 42-6 62 0 42 6 62 0" fill="none" stroke="#7fb4c4" stroke-width="2"/>
  <rect x="320" y="158" width="120" height="12" rx="3" fill="#0b3425"/>
  <!-- inlet -->
  <rect x="0" y="246" width="256" height="28" fill="#9aa9a0"/>
  <line x1="40" y1="260" x2="200" y2="260" stroke="#5c9c3f" stroke-width="3" marker-end="url(#arr)"/>
  <path d="M256 270 q14 30 4 60" fill="none" stroke="#7fb4c4" stroke-width="5"/>
  <!-- pumps and pipework -->
  <g fill="#0b3425"><rect x="290" y="420" width="56" height="48" rx="8"/><rect x="400" y="420" width="56" height="48" rx="8"/></g>
  <g fill="#8bd02d"><rect x="298" y="428" width="40" height="8" rx="3"/><rect x="408" y="428" width="40" height="8" rx="3"/></g>
  <g fill="none" stroke="#3d5c4a" stroke-width="12" stroke-linejoin="round"><path d="M318 420 V214 H504"/><path d="M428 420 V214"/></g>
  <rect x="504" y="206" width="396" height="16" fill="#9aa9a0"/>
  <line x1="600" y1="214" x2="860" y2="214" stroke="#5c9c3f" stroke-width="3" marker-end="url(#arr)"/>
  <!-- floats -->
  <g stroke="#0b3425" stroke-width="1.5"><line x1="470" y1="205" x2="470" y2="296"/><line x1="484" y1="205" x2="484" y2="346"/><line x1="456" y1="205" x2="456" y2="406"/></g>
  <ellipse cx="470" cy="302" rx="11" ry="7" fill="#e05a3a"/><ellipse cx="484" cy="352" rx="11" ry="7" fill="#8bd02d"/><ellipse cx="456" cy="412" rx="11" ry="7" fill="#e3a51d"/>
  <text x="380" y="502" text-anchor="middle" class="dg-label">Wet well</text>
  <text x="60" y="236" class="dg-label">From the site</text>
  <text x="900" y="244" text-anchor="end" class="dg-label">To the sewer</text>
  {num(1, 670, 52)}{num(2, 752, 30)}{num(3, 128, 300)}{num(4, 300, 300)}{num(5, 372, 444)}{num(6, 520, 352)}{num(7, 760, 252)}
</svg>'''
    legend = [
        ("Control panel & kiosk", "Starts and stops the pumps and swaps duty and standby. We check settings, alarms and wiring."),
        ("Telemetry", "Sends alarms and performance data so problems are spotted between visits."),
        ("Inlet", "Where sewage arrives from the site. We look for blockages, debris and signs of ingress."),
        ("Wet well", "Holds the incoming flow. We clean out fat, silt and rags that cause pumps to block."),
        ("Duty & standby pumps", "Two pumps share the work so one can take over if the other fails. We check wear, blockages and running."),
        ("Level floats & high-level alarm", "Tell the panel when to start and stop, and raise the alarm if the level gets too high. We test every one."),
        ("Rising main", "Carries the flow away under pressure. We check valves and look for signs of restriction."),
    ]
    items = "".join(f'<li><span>{i}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(legend, 1))
    return f'''<section class="block alt" id="how-a-pump-station-works"><div class="wrap">
  <div class="block-head"><p class="eyebrow">How a pump station works</p><h2>What we check, and why it matters.</h2><p>Every point below can stop a station working. A proper service checks them all.</p></div>
  <div class="diagram-wrap"><div class="diagram-card">{svg}</div><ol class="diagram-legend">{items}</ol></div>
</div></section>'''


def monitor_widget():
    """The illustrative telemetry panel from the homepage, reused as a visual."""
    return '''<div class="monitor monitor-inline" aria-label="Illustrative pump station telemetry panel with sample information">
  <div class="monitor-top"><div><strong>Pump station overview</strong><small>Two-pump telemetry view</small></div><span class="illustrative"><span class="pulse"></span> Illustrative sample</span></div>
  <div class="monitor-main">
    <div class="monitor-box"><h2>Pump status</h2><div class="pump-row"><span class="status-dot green"></span><strong>P1</strong><span>Running</span><small>Duty</small></div><div class="pump-row"><span class="status-dot grey"></span><strong>P2</strong><span>Stopped</span><small>Ready</small></div></div>
    <div class="monitor-box"><h2>Signals &amp; safeguards</h2><div class="health-row"><span>P1 fault</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row"><span>P2 fault</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row"><span>Wet well float</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row"><span>Backup float</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row flow-reading"><span>Flowmeter</span><strong>6.8 <small>L/s</small></strong></div></div>
  </div>
</div>'''
