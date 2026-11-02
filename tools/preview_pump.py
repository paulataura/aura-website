"""Builds the picture-led preview of the Pump station maintenance page into preview/."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from template import page, page_hero, steps, reviews, faqs, faq_ld, nudge, PHONE
from visuals import icon_cards, photo_cards, image_row, pump_station_diagram, monitor_widget

crumbs = [("Site Services", "site-services.html"), ("Pump station maintenance", "pump-station-maintenance.html")]
faq = [("How often should a pump station be serviced?", "It depends on the station and how it's used. Most need servicing at least once or twice a year, and busier or adoptable stations more often."),
       ("Can you take over an existing pump station?", "Yes. We'll review its condition and history first and tell you honestly what needs doing."),
       ("Can you work with our current telemetry?", "Often, yes. Tell us what's installed and we'll check."),
       ("What if a pump stops at the weekend?", f"Call our 24/7 line on {PHONE}. We'll arrange attendance and emergency tankering if needed.")]

body = page_hero(eyebrow="Site services", h1="Pump station maintenance.",
                 lead="Planned servicing, wet well cleans and fast fault response, so your pump station keeps running and problems are caught early.",
                 crumbs=crumbs, image="assets/stock-pumps-closeup.webp", image_alt="Pumps and pipework in a pumping station")
body += image_row(image="assets/stock-pump-set.webp", alt_text="Duty and standby pumps with valves and pipework",
                  eyebrow="Why servicing matters", head="Keep the station ready, not just running.",
                  paras=["Pump stations fail when small things go unnoticed: a sticking float, a worn impeller, fat building up in the wet well. Regular servicing catches them before they become an overflow or an emergency.",
                         "We look after domestic, commercial and adoptable stations."],
                  ticks=["Planned servicing of pumps and controls", "Wet well cleaning and desilting", "Fault finding, repairs and emergency tankering"])
body += pump_station_diagram()
body += icon_cards([("pump", "Pumps & controls", "Checking pump operation, duty and standby, control panels and kiosks."),
                    ("wetwell", "Wet well", "Inspecting and cleaning the wet well, floats and level controls."),
                    ("report", "Report & advise", "A clear report of what we found, did and recommend next.")],
                   head="What a service covers")
body += steps([("Review", "We look at the station, its equipment and service history."),
               ("Service", "We service on a schedule that suits the station and its use."),
               ("Respond", "If something fails, we arrange the right response quickly.")])
body += image_row(visual_html=monitor_widget(), eyebrow="Telemetry", head="See what's happening between visits.",
                  paras=["Telemetry is a tool we can add to any station we look after. It shows pump states and levels, sends an alert when something changes, and collects the data behind your reports."],
                  ticks=["Alarms before small faults become call-outs", "Monthly performance reports", "Works with many existing systems"], reverse=True)
body += reviews(["homeowner", "telemetry"], alt=True)
body += nudge(image="assets/stock-control-panel.webp")
body += photo_cards([("assets/pump-station-final.webp", "Pump station installation", "New and adoptable pumping stations.", "pump-station-installation.html"),
                     ("assets/liquid-waste-collection-final.webp", "Tankering & emergency tankers", "When a station needs pumping out.", "tankering.html"),
                     ("assets/stock-control-panel.webp", "Asset management", "Long-term care for your station.", "asset-management.html")], head="Related services")
body += faqs(faq, alt=True)

html = page(path="pump-station-maintenance.html", title="Pump Station Maintenance & Servicing | Worcestershire | ASG",
            description="Pump station maintenance, servicing, wet well cleaning and 24/7 fault response across Worcestershire.",
            body=body, crumbs=crumbs, extra_ld=[faq_ld(faq)], current="site-services.html", noindex=True,
            service="Pump station maintenance", og_image="assets/stock-pumps-closeup.webp")
for a in ('href="styles.css"', 'href="home.css"', 'href="pages.css"', 'href="favicon-192.png"', 'src="script.js"'):
    html = html.replace(a, a.replace('="', '="../'))
html = html.replace('src="assets/', 'src="../assets/').replace("url('assets/", "url('../assets/")
# keep site links pointing at the live pages
import re
html = re.sub(r'href="(?!https?:|tel:|mailto:|#|\.\./)([a-z0-9-]+\.html(?:#[^"]*)?)"', r'href="../\1"', html)
os.makedirs("preview", exist_ok=True)
open("preview/pump-station-maintenance.html", "w", encoding="utf-8").write(html)
print("built preview/pump-station-maintenance.html")
