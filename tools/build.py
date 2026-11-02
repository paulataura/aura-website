"""Builds every page of aurasolutions.co.uk from tools/template.py.

Usage:  python3 tools/build.py [output_dir] [--preview]
  --preview  marks every page noindex (for the review copy)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from visuals import icon_cards, photo_cards, image_row, pump_station_diagram, monitor_widget
from template import (page, page_hero, cards, steps, split, reviews, faqs, faq_ld, nudge,
                      redirect, review_html, e, TEL, PHONE)

IMG_DRAIN = "assets/drainage-installation-final.webp"
IMG_PUMP = "assets/pump-station-final.webp"
IMG_TANKER = "assets/liquid-waste-collection-final.webp"
AREA = "Evesham & Worcestershire"

PAGES = {}


def add(path, **kw):
    PAGES[path] = kw


HERO_BY_MENU = {"installation-repairs.html": IMG_DRAIN, "site-services.html": IMG_TANKER, "waste-management.html": IMG_TANKER}


def other(img):
    return IMG_DRAIN if img == IMG_PUMP else IMG_PUMP


def service(path, *, menu, menu_href, title, description, eyebrow, h1, lead, image=None, image_alt="",
            intro_head, intro_paras, ticks, included_head, included, how, faq, review_keys=(), nudge_kw=None,
            related=None):
    crumbs = [(menu, menu_href), (h1.rstrip("."), path)] if menu else [(h1.rstrip("."), path)]
    image = image or HERO_BY_MENU.get(menu_href, IMG_TANKER)
    body = page_hero(eyebrow=eyebrow, h1=h1, lead=lead, crumbs=crumbs, image=image, image_alt=image_alt)
    body += split(intro_head, intro_paras, ticks)
    body += cards(included, head=included_head, alt=True)
    body += steps(how)
    if review_keys:
        body += reviews(list(review_keys), alt=True)
    if nudge_kw is not False:
        body += nudge(**{"image": other(image), **(nudge_kw or {})})
    if related:
        body += cards(related, head="Related services", cols=3, alt=not review_keys)
    body += faqs(faq, alt=bool(related) == bool(review_keys))
    add(path, title=title, description=description, body=body, crumbs=crumbs, extra_ld=[faq_ld(faq)], current=menu_href or path)


def overview(path, *, title, description, eyebrow, h1, lead, image=None, image_alt="", items, why_head, why_paras, why_ticks, review_keys=(), faq=None):
    crumbs = [(h1.rstrip("."), path)]
    image = image or IMG_TANKER
    body = page_hero(eyebrow=eyebrow, h1=h1, lead=lead, crumbs=crumbs, image=image, image_alt=image_alt)
    body += cards(items, head="What we can do for you", alt=True)
    body += split(why_head, why_paras, why_ticks)
    if review_keys:
        body += reviews(list(review_keys), alt=True)
    body += nudge(image=other(image))
    if faq:
        body += faqs(faq, alt=True)
    add(path, title=title, description=description, body=body, crumbs=crumbs, extra_ld=[faq_ld(faq)] if faq else None)


# =====================================================================
# HOME
# =====================================================================
home_body = f'''<section class="hero" id="top" aria-labelledby="hero-title">
      <div class="hero-photo hero-photo-v2" role="img" aria-label="Vacuum tanker collecting liquid waste at a treatment site"></div>
      <div class="hero-shade"></div>
      <div class="wrap hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">Asset management · Installation · Site services · Waste</p>
          <h1 id="hero-title">Solutions that keep<br>your site flowing.</h1>
          <p class="hero-intro">We're not just another contractor. We learn your site, solve the problem and take the stress away, from pump stations and drainage to tanks and liquid waste.</p>
          <div class="hero-actions"><a class="button button-lime" href="#enquire">Talk to an expert</a><a class="button button-dark" href="tel:{TEL}">Call {PHONE} <span aria-hidden="true">↗</span></a><a class="hero-secondary" href="#services">Explore our services</a></div>
        </div>
        <div class="monitor" aria-label="Illustrative pump station monitoring panel with sample information">
          <div class="monitor-top"><div><strong>Pump station overview</strong><small>Two-pump telemetry view</small></div><span class="illustrative"><span class="pulse"></span> Illustrative sample</span></div>
          <div class="monitor-main">
            <div class="monitor-box"><h2>Pump status</h2><div class="pump-row"><span class="status-dot green"></span><strong>P1</strong><span>Running</span><small>Duty</small></div><div class="pump-row"><span class="status-dot grey"></span><strong>P2</strong><span>Stopped</span><small>Ready</small></div></div>
            <div class="monitor-box"><h2>Signals &amp; safeguards</h2><div class="health-row"><span>P1 fault</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row"><span>P2 fault</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row"><span>Wet well float</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row"><span>Backup float</span><strong><i class="status-dot green"></i> OK</strong></div><div class="health-row flow-reading"><span>Flowmeter</span><strong>6.8 <small>L/s</small></strong></div></div>
          </div>
          <div class="monitor-charts"><div class="measure-box well-box"><div class="well-reading"><span class="measure-label">Wet well level</span><strong class="measure-value">8<span>%</span></strong><small>Level in the wet well</small></div><div class="well-visual" aria-hidden="true"><div class="tank-gauge"><div class="tank-shell"><div class="tank-water"></div><span class="tank-mark tank-mark-top"></span><span class="tank-mark tank-mark-mid"></span></div><span class="tank-base"></span></div><div class="tank-scale"><span>100%</span><span>50%</span><span>0%</span></div></div></div></div>
        </div>
      </div>
    </section>

    <section class="services" id="services" aria-label="Our services">
      <div class="wrap service-grid four">
        <a class="service-card" href="asset-management.html"><span class="service-number">01</span><div><h2>Asset Management</h2><p>We take ownership of your pump stations, tanks and drainage, planning and coordinating everything they need.</p><span class="card-link">Explore asset management <span aria-hidden="true">↗</span></span></div></a>
        <a class="service-card" href="installation-repairs.html"><span class="service-number">02</span><div><h2>Installation &amp; Repairs</h2><p>Drainage, septic tanks, treatment plants, pump stations, gullies and interceptors, designed and installed right first time.</p><span class="card-link">Explore installation <span aria-hidden="true">↗</span></span></div></a>
        <a class="service-card" href="site-services.html"><span class="service-number">03</span><div><h2>Site Services</h2><p>Pump station servicing, tank cleaning, jetting, CCTV surveys, interceptors, tankering and emergency response.</p><span class="card-link">Explore site services <span aria-hidden="true">↗</span></span></div></a>
        <a class="service-card" href="waste-management.html"><span class="service-number">04</span><div><h2>Waste Management</h2><p>Liquid, food and hazardous waste collected, handled and disposed of properly and compliantly.</p><span class="card-link">Explore waste management <span aria-hidden="true">↗</span></span></div></a>
      </div>
    </section>
    <div class="enquiry-strip"><div class="wrap enquiry-strip-inner"><p><strong>Got a problem on site?</strong> Tell us what's going on and we'll work out the right fix with you.</p><a href="#enquire">Send an enquiry <span aria-hidden="true">↗</span></a></div></div>

    <section class="why-section wrap" aria-labelledby="why-title">
      <div class="why-head"><div><p class="eyebrow">A partner, not a supplier</p><h2 id="why-title">We learn your site, not just the job.</h2></div><p>Most contractors turn up, do what they're asked and leave. We take time to understand how your site works and what it relies on, so we can solve the real problem and stop it coming back.</p></div>
      <div class="why-grid">
        <div class="why-card"><span>01</span><h3>We look at the bigger picture</h3><p>We find the cause, not just the symptom, and plan the work around how your site actually operates.</p></div>
        <div class="why-card"><span>02</span><h3>One partner for everything</h3><p>Installation, maintenance, cleaning, tankering and waste, all coordinated by one team that knows your site.</p></div>
        <div class="why-card"><span>03</span><h3>The right kit for every job</h3><p>Through our wide network we bring in exactly the equipment each job needs, when it's needed.</p></div>
      </div>
    </section>

    <section class="detail-section detail-light">
      <div class="wrap detail-grid"><div><p class="eyebrow">Asset management</p><h2>Start with one job. Hand us the whole system.</h2><p class="section-lede">Many customers first call us for a single job. Once we know the site, we take care of it all: planned servicing, emptying, cleaning, repairs and response, with one point of contact.</p><a class="text-link" href="asset-management.html">How asset management works <span aria-hidden="true">↗</span></a></div><div class="detail-list"><div><span>01</span><div><h3>Understand the site</h3><p>We map the assets, the waste streams and what could go wrong.</p></div></div><div><span>02</span><div><h3>Plan the work</h3><p>Servicing, inspections and collections are scheduled before they're needed.</p></div></div><div><span>03</span><div><h3>Respond and report</h3><p>When something changes we act fast, and you get clear reports on what we found and did.</p></div></div></div></div>
    </section>

    <section class="sectors" aria-labelledby="sectors-title">
      <div class="wrap">
        <p class="eyebrow">Who we help</p>
        <h2 id="sectors-title">Built around your kind of site.</h2>
        <p class="lede">Every site is different. Choose yours to see how we can help.</p>
        <div class="sector-grid">
          <a class="sector-card" href="food-drink.html"><h3>Food &amp; drink</h3><p>Food waste, tank cleaning and process liquid waste for food and drink producers.</p><strong>Food &amp; drink ↗</strong></a>
          <a class="sector-card" href="commercial-industrial.html"><h3>Commercial &amp; industrial</h3><p>Interceptors, gullies, tanks and site drainage kept compliant and working.</p><strong>Commercial ↗</strong></a>
          <a class="sector-card" href="homes.html"><h3>Homes</h3><p>Septic tanks, treatment plants and private pump stations, installed and looked after.</p><strong>Homes ↗</strong></a>
          <a class="sector-card" href="developers.html"><h3>Developers</h3><p>Adoptable pumping stations from design to commissioning and Section 104 adoption.</p><strong>Developers ↗</strong></a>
          <a class="sector-card" href="estates.html"><h3>Estates &amp; management</h3><p>Shared pump stations and private sewers managed for residents and managing agents.</p><strong>Estates ↗</strong></a>
        </div>
      </div>
    </section>

    <section class="reviews wrap" aria-labelledby="reviews-title">
      <div class="reviews-head"><div><p class="eyebrow">What customers say</p><h2 id="reviews-title">Honest, reliable, and easy to work with.</h2></div><a class="text-link" href="#enquire">Talk to us about your site <span aria-hidden="true">↗</span></a></div>
      <div class="review-grid">{review_html("developer")}{review_html("commercial")}{review_html("homeowner")}{review_html("sitemanager")}</div>
    </section>

    <section class="emergency-band" aria-labelledby="emergency-title">
      <div class="wrap emergency-grid">
        <div><p class="eyebrow">24/7 emergency response</p><h2 id="emergency-title">Something gone wrong? We'll get it sorted.</h2><p>Day or night, weekends included. Call and speak to someone who'll arrange the right response straight away.</p><a class="big-phone" href="tel:{TEL}">{PHONE}</a><br><a class="button button-lime" href="emergency-flood-response.html">Emergency &amp; flood response</a></div>
        <ul class="emergency-list"><li>Pump station failures and alarms</li><li>Flooding and flood response</li><li>Emergency tankers and overflows</li><li>Blocked drains and sewers</li><li>Oil, chemical and liquid spills</li></ul>
      </div>
    </section>'''

add("index.html",
    title="Drainage, Pump Station & Liquid Waste Services | Evesham, Worcestershire | ASG",
    description="Pump station maintenance, drainage asset management, septic tank installation, CCTV drain surveys, interceptor cleaning, tankering and 24/7 emergency response across Evesham and Worcestershire.",
    body=home_body)

# =====================================================================
# ASSET MANAGEMENT (single page)
# =====================================================================
am_faq = [
    ("What does asset management include?", "Whatever your site needs. We agree which assets we look after and what each needs, then plan and coordinate the servicing, emptying, cleaning, inspections, repairs and emergency response around them."),
    ("Do I need telemetry to have asset management?", "No. Telemetry is a tool we can add where it helps, to give you visibility of how an asset is performing and to collect data. Plenty of the sites we manage don't need it."),
    ("Can you take over a site from another contractor?", "Yes. We start by reviewing the assets, their history and anything that needs putting right, then agree a plan for looking after them from there."),
    ("How long does an agreement last?", "We agree the length with you at the start, based on the site and what's included. Ask us and we'll talk it through."),
    ("Can you look after just one asset?", "Yes. Some customers start with a single pump station or tank and add more once they see how it works."),
]
body = page_hero(eyebrow="Asset management", h1="Your assets, our responsibility.",
                 lead="Hand us your pump stations, tanks, interceptors and drainage. We get to know the site, plan what each asset needs and take care of it, so you don't have to.",
                 crumbs=[("Asset Management", "asset-management.html")], image=IMG_PUMP, image_alt="Wastewater treatment works with pumps and pipework")
body += split("One partner who knows your site.",
              ["Most problems with drainage and wastewater systems come from nobody owning them. Servicing gets missed, small faults grow and every call-out starts from scratch.",
               "With asset management, we take that ownership. We learn how your site works, plan the work before it's needed and coordinate every visit, so things keep running and you always know where you stand."],
              ["One point of contact for every asset", "Planned servicing, emptying and cleaning", "Repairs and remedial work arranged for you", "24/7 emergency response when it's needed", "Clear reports after every visit", "Reminders when services are due, no pushy sales"],
              eyebrow="Why asset management")
body += cards([
    ("Pump stations", "Duty and standby pumps, wet wells, floats, controls and kiosks, serviced and kept ready.", "pump-station-maintenance.html"),
    ("Septic tanks & treatment plants", "Emptying, servicing and repairs planned around how the system is used.", "septic-tanks-treatment-plants.html"),
    ("Interceptors & gullies", "Inspected, emptied and cleaned on a schedule that keeps the site compliant.", "interceptor-gully-cleaning.html"),
    ("Storage & process tanks", "Emptying, cleaning and waste collections coordinated with your operation.", "tank-cleaning.html"),
    ("Private drainage networks", "Sewers, chambers and drainage runs surveyed, jetted and repaired when needed.", "cctv-drain-surveys.html"),
    ("New & adoptable assets", "Pump stations and sewers looked after from commissioning through to adoption.", "developers.html"),
], head="What we can look after", intro="Any mix of assets, on one site or many.", alt=True)
body += steps([
    ("Understand the site", "We visit, map the assets, review their condition and history, and learn how your site operates."),
    ("Agree the plan", "We agree what we look after, how often, and how we respond when something goes wrong."),
    ("Look after it", "We coordinate every visit, deal with problems early and keep you updated with clear reports."),
], head="How it works")
body += f'''<section class="block alt"><div class="wrap split"><div><p class="eyebrow">Telemetry</p><h2>Visibility when you need it.</h2><p>Telemetry is a tool we can add to any asset we manage. It shows how the asset is performing, sends alerts when something changes and collects the data behind your reports.</p><p>We use it where it genuinely helps, typically pump stations, wet wells and tanks, and leave it out where it doesn't.</p></div><ul class="tick-list"><li>Live pump states, levels and alarms</li><li>Early warning before small faults become call-outs</li><li>Data to plan servicing and spot trends</li><li>Monthly reports on how your assets are performing</li><li>Works with many existing telemetry systems</li></ul></div></section>'''
body += reviews(["telemetry", "property"])
body += faqs(am_faq, alt=True)
add("asset-management.html", title=f"Drainage & Pump Station Asset Management | {AREA} | ASG",
    description="Drainage asset management across Worcestershire: pump stations, tanks, interceptors and private drainage looked after under one plan, with telemetry where it helps and 24/7 response.",
    body=body, crumbs=[("Asset Management", "asset-management.html")], extra_ld=[faq_ld(am_faq)], og_image=IMG_PUMP)

# =====================================================================
# INSTALLATION & REPAIRS
# =====================================================================
overview("installation-repairs.html",
         title=f"Drainage Installation & Repairs | {AREA} | ASG",
         description="Drainage installation, remedial works, septic tanks, sewage treatment plants, pump stations, gullies and interceptors installed across Evesham and Worcestershire.",
         eyebrow="Installation & repairs", h1="Built right. Built to last.",
         lead="From a new septic tank to a pump station on a housing site, we design and install systems that work for the site, then help keep them working.",
         image=IMG_DRAIN, image_alt="New drainage pipework and inspection chamber being installed",
         items=[
             ("Drainage installation & remedial works", "New drainage runs, connections and chambers, plus repairs to drainage that isn't working.", "drainage-installation.html"),
             ("Septic tanks & treatment plants", "New and replacement septic tanks and sewage treatment plants for homes and businesses.", "septic-tanks-treatment-plants.html"),
             ("Pump station installation", "Package and adoptable pumping stations, from design to commissioning.", "pump-station-installation.html"),
             ("Gully & interceptor installation", "Oil interceptors, separators and gullies specified and installed for compliance.", "gully-interceptor-installation.html"),
         ],
         why_head="We solve the problem, not just the brief.",
         why_paras=["We start by understanding the site: the ground, the flows, how it's used and what's gone wrong before. That's how we make sure the system we install is the right one.",
                    "Once it's in, we can look after it too, so the people who installed it are the people who maintain it."],
         why_ticks=["Domestic and commercial installations", "Remedial work on failing systems", "Small and medium projects, not major groundworks", "Commissioning and handover documents", "Ongoing care available after installation"],
         review_keys=("sitemanager", "warehouse"))

service("drainage-installation.html", menu="Installation & Repairs", menu_href="installation-repairs.html",
        title=f"Drainage Installation & Remedial Works | {AREA} | ASG",
        description="New drainage installation and drainage repairs for homes and businesses across Evesham and Worcestershire. Connections, chambers and remedial works done right first time.",
        eyebrow="Installation & repairs", h1="Drainage installation & remedial works.",
        lead="New drainage, connections and chambers, and repairs to drainage that keeps causing problems. Done properly, first time.",
        image=IMG_DRAIN, image_alt="New drainage pipework and inspection chamber",
        intro_head="Find the cause. Fix it properly.",
        intro_paras=["Recurring blockages, standing water and flooding usually point to a problem in the drainage itself. We find out what's really going on, often with a CCTV survey, then put it right.",
                     "For new work, we design around the site and how it will be used, so the drainage copes now and in the future."],
        ticks=["New drainage runs and connections", "Inspection chambers and manholes", "Repairs to collapsed or damaged pipes", "Fixing poor falls and standing water", "Surface water and soakaway problems", "Domestic and commercial sites"],
        included_head="What we do",
        included=[("New drainage", "Foul and surface water drainage for extensions, new buildings and site changes."),
                  ("Remedial works", "Repairs and replacements where existing drainage has failed or keeps blocking."),
                  ("Connections & chambers", "New connections to sewers and chambers, built to the right standard.")],
        how=[("Investigate", "We look at the site and, where needed, survey the drainage to find the real problem."),
             ("Scope and quote", "We explain what we found in plain English and agree the right fix."),
             ("Install and hand over", "We complete the work, test it and hand over with clear records.")],
        faq=[("Do you work on homes and businesses?", "Yes, we install and repair drainage on both domestic and commercial sites."),
             ("Do you do large groundworks?", "We focus on drainage installation and remedial works rather than major groundworks packages."),
             ("Will I need a CCTV survey first?", "Often, yes. A survey shows exactly what's wrong so the repair fixes the cause, not just the symptom."),
             ("Can you maintain the drainage afterwards?", "Yes. We can add it to an asset management plan so it's looked after from day one.")],
        review_keys=("warehouse",),
        related=[("CCTV drain surveys", "Find out exactly what's happening in your drains.", "cctv-drain-surveys.html"),
                 ("Jetting & drain cleaning", "Clear blockages and build-up quickly.", "jetting-drain-cleaning.html"),
                 ("Emergency & flood response", "Urgent help when drainage fails.", "emergency-flood-response.html")])

service("septic-tanks-treatment-plants.html", menu="Installation & Repairs", menu_href="installation-repairs.html",
        title=f"Septic Tank & Sewage Treatment Plant Installation | {AREA} | ASG",
        description="Septic tank and sewage treatment plant installation, replacement, servicing and emptying for homes and businesses across Evesham and Worcestershire.",
        eyebrow="Installation & repairs", h1="Septic tanks & treatment plants.",
        lead="New and replacement septic tanks and sewage treatment plants, installed to suit your property and kept working afterwards.",
        intro_head="The right system for your property.",
        intro_paras=["Not every property suits a septic tank. Where the system discharges, how many people it serves and the ground conditions all affect what's right, and what the rules allow.",
                     "We look at all of it first, recommend the right option, and take care of the installation from start to finish."],
        ticks=["New septic tanks and treatment plants", "Replacement of old or failing systems", "Upgrades where rules require it", "Drainage fields and connections", "Servicing and emptying after install", "Homes, farms and businesses"],
        included_head="What we do",
        included=[("New installations", "Septic tanks and sewage treatment plants for new builds and off-mains properties."),
                  ("Replacements & upgrades", "Replacing failing or non-compliant systems with the right modern equivalent."),
                  ("Servicing & emptying", "Planned servicing and emptying so the system keeps working as it should.")],
        how=[("Site review", "We look at the property, the existing system and where it discharges."),
             ("Recommend", "We explain the options and recommend the right one, with no hard sell."),
             ("Install and care", "We install, commission and can look after it from then on.")],
        faq=[("Is a septic tank always the right choice?", "No. Depending on where it discharges and the site, a sewage treatment plant may be needed instead. We'll tell you honestly which suits your property."),
             ("Can you replace my existing septic tank?", "Yes. We remove or decommission the old system and install the right replacement."),
             ("Do you include the drainage work?", "Yes. We can handle the connections and drainage field as part of the job."),
             ("Can you service and empty it afterwards?", "Yes. We can set up planned servicing and emptying so you don't have to remember.")],
        review_keys=("homeowner",),
        related=[("Tankering & emptying", "Septic tank and cesspit emptying.", "tankering.html"),
                 ("Homes", "How we help homeowners with private drainage.", "homes.html"),
                 ("Asset management", "Let us look after it long term.", "asset-management.html")])

service("pump-station-installation.html", menu="Installation & Repairs", menu_href="installation-repairs.html",
        title=f"Pump Station Installation | Adoptable Pumping Stations | {AREA} | ASG",
        description="Package and adoptable pumping station installation across Worcestershire, from design and installation to commissioning and Section 104 adoption.",
        eyebrow="Installation & repairs", h1="Pump station installation.",
        lead="Package and adoptable pumping stations designed, installed and commissioned properly, with a clear route to adoption where it's needed.",
        image=IMG_PUMP, image_alt="Wastewater treatment works with pumps and pipework",
        intro_head="From design to commissioning.",
        intro_paras=["A pump station has to suit the flows, the site and, on new developments, the water company's adoption standards. Getting that right at design stage saves months of problems later.",
                     "We keep projects moving from first drawings through installation and commissioning, then support the station until it's adopted or hand it into our care."],
        ticks=["Domestic and commercial package stations", "Adoptable pumping stations for developers", "Wet wells, controls and kiosks", "Commissioning and handover", "Telemetry where it helps", "Support through to adoption"],
        included_head="What we do",
        included=[("Design support", "Working with your designers to get a station that suits the site and adoption standards."),
                  ("Installation", "Installing the station, wet well, pipework, controls and kiosk."),
                  ("Commissioning & handover", "Testing, commissioning and the records needed for adoption or handover.")],
        how=[("Plan", "We review the design, flows and site constraints with you."),
             ("Install", "We install and commission the station, keeping you updated throughout."),
             ("Hand over or look after", "We support adoption, or look after the station from then on.")],
        faq=[("Do you install adoptable pumping stations?", "Yes. We install stations intended for adoption under a Section 104 agreement and support the process through to adoption."),
             ("Can you maintain the station before adoption?", "Yes. Most stations need maintaining between commissioning and adoption, and we can look after that for you."),
             ("Do you install pump stations for single homes?", "Yes, we install package pump stations for private properties as well as developments."),
             ("Can you add telemetry?", "Yes, where it helps. It gives early warning of faults and useful data during the maintenance period.")],
        review_keys=("developer",),
        related=[("Developers", "Adoptable assets from design to adoption.", "developers.html"),
                 ("Pump station maintenance", "Servicing and fault response.", "pump-station-maintenance.html"),
                 ("Asset management", "Long-term care for your station.", "asset-management.html")])

service("gully-interceptor-installation.html", menu="Installation & Repairs", menu_href="installation-repairs.html",
        title=f"Interceptor & Gully Installation | {AREA} | ASG",
        description="Oil interceptor, separator and gully installation for commercial sites, forecourts and yards across Evesham and Worcestershire.",
        eyebrow="Installation & repairs", h1="Gully & interceptor installation.",
        lead="Oil interceptors, separators and gullies specified and installed so your site drains properly and stays compliant.",
        intro_head="The right interceptor for your site.",
        intro_paras=["Car parks, yards, forecourts and workshops need the right interceptor to stop oil and silt reaching drains and watercourses. The wrong size or type causes compliance problems and constant call-outs.",
                     "We look at the area it drains, what's likely to go into it and how it will be maintained, then install a system that does the job."],
        ticks=["Oil interceptors and separators", "Road and yard gullies", "Replacement of failed units", "Alarms and access covers", "Maintenance plan from day one", "Commercial and industrial sites"],
        included_head="What we do",
        included=[("Specification", "Choosing the right class and size of interceptor for the area and use."),
                  ("Installation", "Installing interceptors, gullies, chambers and connections."),
                  ("Replacement", "Replacing damaged, undersized or failed units.")],
        how=[("Assess", "We look at the drainage area, use and any existing system."),
             ("Install", "We install and test the system and its alarms."),
             ("Maintain", "We set up emptying and inspection so it stays compliant.")],
        faq=[("Which interceptor do I need?", "It depends on the area drained, what's likely to enter the system and where it discharges. We'll recommend the right one."),
             ("Can you replace an old interceptor?", "Yes. We remove or decommission the old unit and install the right replacement."),
             ("Do you empty and maintain them too?", "Yes, through our interceptor and gully cleaning service.")],
        review_keys=(),
        related=[("Interceptor & gully cleaning", "Emptying and inspections to keep you compliant.", "interceptor-gully-cleaning.html"),
                 ("Commercial & industrial", "Site drainage for businesses.", "commercial-industrial.html"),
                 ("Asset management", "Let us look after it long term.", "asset-management.html")])

# =====================================================================
# SITE SERVICES
# =====================================================================
overview("site-services.html",
         title=f"Site Services: Tank Cleaning, Jetting, CCTV & Tankering | {AREA} | ASG",
         description="Pump station maintenance, tank cleaning, jetting, CCTV drain surveys, interceptor cleaning, tankering and 24/7 emergency response across Evesham and Worcestershire.",
         eyebrow="Site services", h1="The right service, the right kit.",
         lead="From a one-off tank clean to emergency tankers at 2am, we bring the right people and equipment for the job, and we get to know your site while we're there.",
         image=IMG_TANKER, image_alt="Vacuum tanker working at a treatment site",
         items=[
             ("Pump station maintenance", "Planned servicing, wet well cleans and fault response.", "pump-station-maintenance.html"),
             ("Tank cleaning", "Storage, process and septic tanks emptied and cleaned safely.", "tank-cleaning.html"),
             ("Jetting & drain cleaning", "High-pressure jetting to clear blockages and build-up.", "jetting-drain-cleaning.html"),
             ("CCTV drain surveys", "See exactly what's happening inside your drains.", "cctv-drain-surveys.html"),
             ("Interceptor & gully cleaning", "Emptying and inspections to keep your site compliant.", "interceptor-gully-cleaning.html"),
             ("Tankering & emergency tankers", "Planned and emergency tankers for liquids and sewage.", "tankering.html"),
             ("Emergency & flood response", "24/7 response to flooding, failures and spills.", "emergency-flood-response.html"),
         ],
         why_head="One job today. A partner for tomorrow.",
         why_paras=["Every job is a chance to understand your site better. While we're there, we look at the bigger picture and tell you honestly about anything that needs attention.",
                    "If it makes sense, we can schedule the work so you never have to chase it again."],
         why_ticks=["Access to a wide network of specialist kit", "Planned or same-day attendance", "Clear reports after every job", "Waste handled and documented properly", "24/7 emergency line"],
         review_keys=("commercial", "warehouse"))

# Pump station maintenance: picture-led layout with the cutaway diagram (approved 2 Nov)
_psm_crumbs = [("Site Services", "site-services.html"), ("Pump station maintenance", "pump-station-maintenance.html")]
_psm_faq = [("How often should a pump station be serviced?", "It depends on the station and how it's used. Most need servicing at least once or twice a year, and busier or adoptable stations more often."),
            ("Can you take over an existing pump station?", "Yes. We'll review its condition and history first and tell you honestly what needs doing."),
            ("Can you work with our current telemetry?", "Often, yes. Tell us what's installed and we'll check."),
            ("What if a pump stops at the weekend?", f"Call our 24/7 line on {PHONE}. We'll arrange attendance and emergency tankering if needed.")]
body = page_hero(eyebrow="Site services", h1="Pump station maintenance.",
                 lead="Planned servicing, wet well cleans and fast fault response, so your pump station keeps running and problems are caught early.",
                 crumbs=_psm_crumbs, image="assets/photo-wet-well.webp", image_alt="Looking down into a pump station wet well with float switch and pipework")
body += split("Keep the station ready, not just running.",
              ["Pump stations fail when small things go unnoticed: a sticking float, a worn impeller, fat building up in the wet well. Regular servicing catches them before they become an overflow or an emergency.",
               "We look after domestic, commercial and adoptable stations."],
              ["Planned servicing of pumps and controls", "Wet well cleaning and desilting", "Float and alarm checks", "Fault finding and repairs", "Emergency tankering if a station fails", "Clear service reports"],
              eyebrow="Why servicing matters")
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
body += photo_cards([(IMG_PUMP, "Pump station installation", "New and adoptable pumping stations.", "pump-station-installation.html"),
                     (IMG_TANKER, "Tankering & emergency tankers", "When a station needs pumping out.", "tankering.html"),
                     ("assets/stock-control-panel.webp", "Asset management", "Long-term care for your station.", "asset-management.html")], head="Related services")
body += faqs(_psm_faq, alt=True)
add("pump-station-maintenance.html", title="Pump Station Maintenance & Servicing | Worcestershire | ASG",
    description="Pump station maintenance, servicing, wet well cleaning and 24/7 fault response for domestic, commercial and adoptable pumping stations across Worcestershire.",
    body=body, crumbs=_psm_crumbs, extra_ld=[faq_ld(_psm_faq)], current="site-services.html", og_image="assets/photo-wet-well.webp")

service("tank-cleaning.html", menu="Site Services", menu_href="site-services.html",
        title=f"Tank Cleaning: Storage, Process & Septic Tanks | {AREA} | ASG",
        description="Industrial, food-site and storage tank cleaning across Evesham and Worcestershire. Tanks emptied, cleaned and the waste disposed of properly.",
        eyebrow="Site services", h1="Tank cleaning.",
        lead="Storage, process and septic tanks emptied and cleaned safely, with the waste taken away and disposed of properly.",
        image=IMG_TANKER, image_alt="Vacuum tanker emptying a tank",
        intro_head="Planned around your operation.",
        intro_paras=["On a food or industrial site, a tank clean has to fit around production, hygiene requirements and safe working. We plan the job with you so it's done safely and with minimal disruption.",
                     "We empty the tank, clean it, and handle the waste with the right paperwork."],
        ticks=["Process and storage tanks", "Food and drink site tanks", "Septic tanks and cesspits", "Rainwater and holding tanks", "Waste removal and disposal", "Planned or emergency"],
        included_head="What we do",
        included=[("Empty", "Removing the contents with the right tanker for the material."),
                  ("Clean", "Jetting and cleaning the tank so it's ready to use or inspect."),
                  ("Dispose", "Taking the waste to a licensed site with full documentation.")],
        how=[("Plan", "We agree access, timing, the material and safe working with you."),
             ("Clean", "We empty and clean the tank with the right equipment."),
             ("Report", "You get confirmation of the work and the waste paperwork.")],
        faq=[("Can you clean tanks on food production sites?", "Yes. We plan the work around your production schedule and site requirements."),
             ("What happens to the waste?", "It goes to a suitably licensed site, and you get the waste transfer paperwork."),
             ("Can this be scheduled regularly?", "Yes. Many customers have tanks cleaned on a schedule as part of asset management.")],
        related=[("Food & drink", "How we help food and drink producers.", "food-drink.html"),
                 ("Liquid waste collections", "Regular collections of liquid waste.", "liquid-waste.html"),
                 ("Jetting & drain cleaning", "Clearing drains and pipework.", "jetting-drain-cleaning.html")])

service("jetting-drain-cleaning.html", menu="Site Services", menu_href="site-services.html",
        title=f"Drain Jetting & Drain Cleaning | {AREA} | ASG",
        description="High-pressure drain jetting and drain cleaning for blockages, fat and silt build-up on domestic, commercial and industrial sites across Evesham and Worcestershire.",
        eyebrow="Site services", h1="Jetting & drain cleaning.",
        lead="High-pressure jetting to clear blockages, fat, silt and debris from drains, sewers and culverts.",
        intro_head="Clear it, then find out why.",
        intro_paras=["Jetting clears most blockages quickly. But if the same drain keeps blocking, there's usually a reason, so we'll tell you what we think is causing it and how to stop it happening again.",
                     "We can pair jetting with a CCTV survey to see the condition of the drain once it's clear."],
        ticks=["Blocked drains and sewers", "Fat, oil and grease build-up", "Silt and debris", "Culverts and larger pipes", "Planned cleaning programmes", "Emergency call-outs"],
        included_head="What we do",
        included=[("Unblocking", "Clearing blockages quickly to get things flowing again."),
                  ("Descaling & cleaning", "Removing fat, scale and build-up that narrows the pipe."),
                  ("Planned cleaning", "Regular jetting for drains that are prone to build-up.")],
        how=[("Attend", "We arrive with the right jetting equipment for the job."),
             ("Clear", "We clear the blockage and clean the line."),
             ("Advise", "We tell you what caused it and whether a survey or repair is needed.")],
        faq=[("Can you come out the same day?", f"Often, yes. For emergencies call {PHONE}."),
             ("Will jetting damage my drains?", "Jetting is safe for drains in reasonable condition. If we suspect damage, we'll suggest a CCTV survey first."),
             ("Can you set up regular cleaning?", "Yes, for drains prone to fat or silt build-up we can schedule regular jetting.")],
        review_keys=("commercial",),
        related=[("CCTV drain surveys", "See inside the drain after it's cleared.", "cctv-drain-surveys.html"),
                 ("Drainage remedial works", "Fix the cause of repeat blockages.", "drainage-installation.html"),
                 ("Emergency & flood response", "Urgent blockages and flooding.", "emergency-flood-response.html")])

service("cctv-drain-surveys.html", menu="Site Services", menu_href="site-services.html",
        title=f"CCTV Drain Surveys | {AREA} | ASG",
        description="CCTV drain surveys across Evesham and Worcestershire to find blockages, damage, root ingress and the cause of recurring drainage problems, with a clear report.",
        eyebrow="Site services", h1="CCTV drain surveys.",
        lead="A camera survey shows exactly what's happening inside your drains, so repairs fix the real problem first time.",
        intro_head="See the problem before you pay to fix it.",
        intro_paras=["Recurring blockages, bad smells, damp or flooding often come from damage you can't see: cracked or collapsed pipes, root ingress, displaced joints or poor falls.",
                     "A CCTV survey finds them. You get a clear report explaining what we found in plain English, and an honest recommendation for what to do next."],
        ticks=["Recurring blockages and flooding", "Pre-purchase and condition surveys", "Root ingress and collapsed pipes", "Drain mapping and tracing", "Pre-adoption surveys", "Clear written report"],
        included_head="What you get",
        included=[("The survey", "A camera survey of the drainage runs that matter."),
                  ("A clear report", "What we found, where, and how serious it is, in plain English."),
                  ("Honest advice", "What needs fixing now, what can wait, and what it involves.")],
        how=[("Book", "Tell us the problem and the site and we'll plan the survey."),
             ("Survey", "We clear the line if needed and survey the drains."),
             ("Report", "You get the report and our recommendations.")],
        faq=[("Do you need to clear the drain first?", "Sometimes. If a drain is blocked or full of debris, we'll jet it first so the camera can see."),
             ("Will I get a report?", "Yes, a clear report of what we found and what we recommend."),
             ("Can you do the repairs too?", "Yes. If repairs are needed we can scope and carry them out.")],
        review_keys=("warehouse",),
        related=[("Drainage remedial works", "Repairs based on what the survey finds.", "drainage-installation.html"),
                 ("Jetting & drain cleaning", "Clear the line before or after the survey.", "jetting-drain-cleaning.html"),
                 ("Developers", "Pre-adoption surveys for new sewers.", "developers.html")])

service("interceptor-gully-cleaning.html", menu="Site Services", menu_href="site-services.html",
        title=f"Interceptor Cleaning & Gully Emptying | {AREA} | ASG",
        description="Oil interceptor and separator emptying, gully cleaning and inspections for car parks, yards, forecourts and commercial sites across Evesham and Worcestershire.",
        eyebrow="Site services", h1="Interceptor & gully cleaning.",
        lead="Oil interceptors, separators and gullies emptied, cleaned and inspected so your site stays compliant and drains properly.",
        intro_head="Small assets. Big consequences.",
        intro_paras=["A full or neglected interceptor can let oil and silt into drains and watercourses, and blocked gullies flood car parks and yards. Both are easy to avoid with regular emptying.",
                     "We set the right schedule for your site, keep records of every visit and remind you when the next one is due."],
        ticks=["Oil interceptors and separators", "Road, yard and car park gullies", "Silt traps and catchpits", "Inspections and alarm checks", "Waste documented properly", "One-off or scheduled"],
        included_head="What we do",
        included=[("Empty & clean", "Removing oil, water and silt and cleaning the unit."),
                  ("Inspect", "Checking condition, alarms and covers, and reporting any issues."),
                  ("Records", "Waste paperwork and service records for your compliance file.")],
        how=[("Identify", "We list the interceptors and gullies on site and their condition."),
             ("Schedule", "We agree how often each needs attention."),
             ("Maintain", "We empty, clean and report, and remind you when the next visit is due.")],
        faq=[("How often should an interceptor be emptied?", "It depends on its size and how much oil and silt reaches it. We'll recommend a schedule after the first visit."),
             ("Do you provide waste paperwork?", "Yes, every collection comes with the right waste documentation."),
             ("Can you clean all the gullies on a site?", "Yes, from a few gullies to whole car parks and estates.")],
        review_keys=("commercial",),
        related=[("Gully & interceptor installation", "New and replacement units.", "gully-interceptor-installation.html"),
                 ("Commercial & industrial", "Site drainage for businesses.", "commercial-industrial.html"),
                 ("Asset management", "Never miss a service again.", "asset-management.html")])

service("tankering.html", menu="Site Services", menu_href="site-services.html",
        title=f"Tankering Services & Emergency Tankers | {AREA} | ASG",
        description="Vacuum tanker services across Evesham and Worcestershire: septic tank and cesspit emptying, liquid waste, overflows and 24/7 emergency tankers.",
        eyebrow="Site services", h1="Tankering & emergency tankers.",
        lead="The right tanker for the job, planned or in an emergency: septic tanks, cesspits, pump stations, overflows and liquid waste.",
        image=IMG_TANKER, image_alt="Vacuum tanker collecting liquid waste",
        intro_head="The right tanker, when you need it.",
        intro_paras=["Through our network we can bring in the right size and type of tanker for each job, from a small domestic septic tank to a large volume emergency on a commercial site.",
                     "Every load is handled and disposed of properly, with the paperwork to prove it."],
        ticks=["Septic tank and cesspit emptying", "Pump station and wet well pump-outs", "Overflows and floodwater", "Liquid waste collections", "Over-pumping support", "24/7 emergency tankers"],
        included_head="What we do",
        included=[("Planned emptying", "Regular emptying of septic tanks, cesspits and holding tanks."),
                  ("Emergency tankers", "Fast response to overflows, pump failures and flooding."),
                  ("Liquid waste", "Collection and disposal of liquid waste streams.")],
        how=[("Call or book", "Tell us what needs emptying, how much and how urgent."),
             ("Attend", "We send the right tanker for the job."),
             ("Dispose", "The waste goes to a licensed site, with full paperwork.")],
        faq=[("Do you offer emergency tankers?", f"Yes, 24/7. Call {PHONE}."),
             ("How often should my septic tank be emptied?", "Usually at least once a year, but it depends on the tank size and how many people use it. We can set up reminders."),
             ("Can you help when a pump station fails?", "Yes. We can pump out the wet well to prevent an overflow while the fault is fixed.")],
        review_keys=("homeowner",),
        related=[("Emergency & flood response", "Urgent help day or night.", "emergency-flood-response.html"),
                 ("Liquid waste collections", "Regular liquid waste collections.", "liquid-waste.html"),
                 ("Pump station maintenance", "Stop failures before they happen.", "pump-station-maintenance.html")])

emer_faq = [("Are you really available 24/7?", f"Yes. Call {PHONE} day or night, including weekends and bank holidays."),
            ("How quickly can you attend?", "We arrange the right response as quickly as possible. Call us and we'll tell you what to expect."),
            ("What should I do while I wait?", "If it's safe, keep people away from the affected area and stop water use where you can. We'll talk you through anything else when you call."),
            ("Do you deal with oil and chemical spills?", "Yes. Tell us what's been spilled and where, and we'll arrange the right response and disposal.")]
body = page_hero(eyebrow="24/7 emergency response", h1="Emergency & flood response.",
                 lead="Flooding, pump failures, overflows, blockages and spills, day or night. Call and we'll arrange the right response straight away.",
                 crumbs=[("Site Services", "site-services.html"), ("Emergency & flood response", "emergency-flood-response.html")],
                 primary=(f"Call {PHONE}", f"tel:{TEL}"), image=IMG_DRAIN)
body += split("Something gone wrong? We'll get it sorted.",
              ["When drainage fails, you need someone who answers the phone and takes charge. We arrange the right people and kit, deal with the immediate problem, then help you stop it happening again."],
              ["Pump station failures and alarms", "Flooding and floodwater removal", "Emergency tankers and overflows", "Blocked drains and sewers", "Oil, chemical and liquid spills", "Over-pumping and temporary measures"])
body += cards([("Flood response", "Removing floodwater, clearing drains and protecting the site."),
               ("Pump failures", "Pumping out the wet well and getting the station running again."),
               ("Overflows & blockages", "Emergency tankers and jetting to stop overflows quickly.")], head="How we can help", alt=True)
body += f'''<section class="block" id="spills"><div class="wrap split"><div><p class="eyebrow">Spill response</p><h2>Spills contained and cleared.</h2><p>Oil, fuel, chemical and other liquid spills need fast action to protect drains, watercourses and people. We arrange containment, recovery and proper disposal of the contaminated material.</p><p>Tell us what's been spilled, roughly how much and where, and we'll take it from there.</p></div><ul class="tick-list"><li>Oil and fuel spills</li><li>Chemical and process liquids</li><li>Contaminated water recovery</li><li>Drain protection and clean-up</li><li>Proper disposal with paperwork</li></ul></div></section>'''
body += reviews(["homeowner"], alt=True)
body += faqs(emer_faq)
add("emergency-flood-response.html", title=f"24/7 Emergency Drainage, Flood & Spill Response | {AREA} | ASG",
    description="24/7 emergency response across Evesham and Worcestershire: flooding, pump station failures, overflows, emergency tankers, blocked drains and spill response.",
    body=body, crumbs=[("Site Services", "site-services.html"), ("Emergency & flood response", "emergency-flood-response.html")],
    extra_ld=[faq_ld(emer_faq)], current="site-services.html", enquiry_heading="Not an emergency? Tell us what you need.")

# =====================================================================
# WASTE MANAGEMENT
# =====================================================================
overview("waste-management.html",
         title=f"Liquid, Food & Hazardous Waste Management | {AREA} | ASG",
         description="Liquid waste, food waste and hazardous waste collection and disposal across Evesham and Worcestershire. Registered waste carrier and broker.",
         eyebrow="Waste management", h1="Waste handled properly.",
         lead="Liquid, food and hazardous waste collected, handled and disposed of compliantly, with the experience to deal with the difficult streams.",
         image=IMG_TANKER, image_alt="Vacuum tanker collecting liquid waste",
         items=[
             ("Liquid waste collections", "Wastewater, sewage, process liquids and tank contents.", "liquid-waste.html"),
             ("Food waste", "Food and drink waste collected and handled properly.", "food-waste.html"),
             ("Hazardous waste", "Hazardous liquids assessed and handled case by case.", "hazardous-waste.html"),
             ("Spill response", "Oil, chemical and liquid spills contained and cleared.", "emergency-flood-response.html#spills"),
         ],
         why_head="Experience where it matters.",
         why_paras=["Some waste is simple. Some isn't. We're at our best with the specialist streams: food waste, hazardous liquids and spills, where knowing what you're doing protects your business.",
                    "As a registered waste carrier and broker, we make sure every load goes to the right place with the right paperwork."],
         why_ticks=["Registered waste carrier and broker (CBDU631384)", "Waste transfer notes for every load", "One-off or scheduled collections", "Specialist and hazardous streams", "Advice on handling difficult waste"],
         faq=[("Are you a registered waste carrier?", "Yes. We're a registered waste carrier and broker, registration CBDU631384."),
              ("Do you collect general waste or skips?", "No. We focus on liquid, food, hazardous and specialist waste streams."),
              ("Can you help with an unusual waste stream?", "Yes. Tell us what it is and we'll work out the right route for it.")])

service("liquid-waste.html", menu="Waste Management", menu_href="waste-management.html",
        title=f"Liquid Waste Collection & Disposal | {AREA} | ASG",
        description="Liquid waste collection and disposal across Evesham and Worcestershire: wastewater, sewage, process liquids, interceptor waste and tank contents, one-off or scheduled.",
        eyebrow="Waste management", h1="Liquid waste collections.",
        lead="Wastewater, sewage, process liquids and tank contents collected and disposed of properly, one-off or on a schedule.",
        image=IMG_TANKER, image_alt="Vacuum tanker collecting liquid waste",
        intro_head="A collection plan around your operation.",
        intro_paras=["Every site produces liquid waste differently. We look at what you produce, how much and how often, then set up collections that fit your operation rather than the other way round.",
                     "Every load is documented and goes to a suitably licensed site."],
        ticks=["Wastewater and sewage", "Process and wash-down water", "Interceptor and gully waste", "Tank and sump contents", "Scheduled or one-off", "Full waste paperwork"],
        included_head="What we collect",
        included=[("Wastewater & sewage", "From septic tanks, cesspits, holding tanks and pump stations."),
                  ("Process liquids", "Wash-down water and non-hazardous process liquids from commercial sites."),
                  ("Interceptor & tank waste", "Oily water, silt and tank contents.")],
        how=[("Tell us the stream", "What it is, how much and how it's stored."),
             ("Agree collections", "One-off or a schedule that suits your site."),
             ("Collect & document", "We collect, dispose and provide the paperwork.")],
        faq=[("Can I arrange regular collections?", "Yes. We'll set a schedule based on how much you produce."),
             ("Do you collect interceptor waste?", "Yes, as part of interceptor emptying or as a separate collection."),
             ("What about hazardous liquids?", "We assess hazardous liquids case by case. See our hazardous waste page.")],
        related=[("Tankering", "Tanker services and emergency tankers.", "tankering.html"),
                 ("Hazardous waste", "Hazardous liquids handled properly.", "hazardous-waste.html"),
                 ("Food waste", "Food and drink waste streams.", "food-waste.html")])

service("food-waste.html", menu="Waste Management", menu_href="waste-management.html",
        title=f"Food Waste Collection for Food & Drink Producers | {AREA} | ASG",
        description="Food waste and food-processing liquid waste collection across Evesham and Worcestershire for food and drink producers, with scheduled collections and full documentation.",
        eyebrow="Waste management", h1="Food waste.",
        lead="Food waste and food-processing liquids collected and handled properly, on a schedule that fits your production.",
        intro_head="Built around your production.",
        intro_paras=["Food and drink producers create waste that needs handling quickly and properly: packaged and unpackaged food, liquid by-products, wash-down water and tank residues.",
                     "We work out the right collection and disposal route for each stream and schedule it around your production."],
        ticks=["Liquid food waste and by-products", "Food-processing wash water", "Tank residues and sludges", "Out-of-date and rejected product", "Scheduled collections", "Full waste documentation"],
        included_head="What we do",
        included=[("Assess the streams", "Understanding what you produce, how much and how it's stored."),
                  ("Collect", "Scheduled or one-off collections that fit your production."),
                  ("Dispose properly", "The right disposal route for each stream, fully documented.")],
        how=[("Review", "We look at your waste streams and current arrangements."),
             ("Plan", "We recommend collections and routes for each stream."),
             ("Collect", "We collect on schedule and provide the paperwork.")],
        faq=[("What types of food waste do you collect?", "Liquid and solid food waste, by-products, rejected product and tank residues. Tell us what you produce and we'll advise."),
             ("Can collections fit around production?", "Yes. We schedule collections to suit your shifts and production."),
             ("Do you also clean food-site tanks?", "Yes, through our tank cleaning service.")],
        related=[("Food & drink", "Everything we do for food and drink producers.", "food-drink.html"),
                 ("Tank cleaning", "Process and storage tanks cleaned.", "tank-cleaning.html"),
                 ("Liquid waste", "Other liquid waste streams.", "liquid-waste.html")])

service("hazardous-waste.html", menu="Waste Management", menu_href="waste-management.html",
        title=f"Hazardous Liquid Waste Collection | {AREA} | ASG",
        description="Hazardous liquid waste assessed, collected and disposed of compliantly across Evesham and Worcestershire, including oils, chemicals and contaminated water.",
        eyebrow="Waste management", h1="Hazardous waste.",
        lead="Hazardous liquids assessed case by case, then collected and disposed of compliantly with the right paperwork.",
        intro_head="Start with the material.",
        intro_paras=["Hazardous waste needs the right handling, transport and disposal route, and that depends on exactly what it is. So we start by understanding the material rather than making blanket promises.",
                     "Share what you know, such as the source, composition and any safety data sheets, and we'll work out the right route."],
        ticks=["Oils and fuels", "Contaminated water", "Chemical and process liquids", "Interceptor and spill waste", "Consignment paperwork", "One-off or scheduled"],
        included_head="What we do",
        included=[("Assess", "Reviewing the material, its source and any data you have."),
                  ("Collect", "Arranging the right transport for the material."),
                  ("Dispose", "Disposal at a suitably permitted site, fully documented.")],
        how=[("Describe the stream", "Tell us what it is, how much and where it's stored."),
             ("Assess and quote", "We confirm the route and what's involved."),
             ("Collect", "We collect and provide the consignment paperwork.")],
        faq=[("Do you accept every hazardous liquid?", "We assess each one individually. Tell us what it is and we'll confirm whether and how we can handle it."),
             ("What if I don't know exactly what it is?", "Tell us what you do know. Sampling and analysis can be arranged if needed."),
             ("Is it urgent?", f"For spills or urgent situations, call {PHONE}.")],
        related=[("Spill response", "Spills contained and cleared.", "emergency-flood-response.html#spills"),
                 ("Liquid waste", "Non-hazardous liquid waste.", "liquid-waste.html"),
                 ("Commercial & industrial", "Waste and drainage for businesses.", "commercial-industrial.html")])

# =====================================================================
# SECTORS
# =====================================================================
body = page_hero(eyebrow="Who we help", h1="Built around your kind of site.",
                 lead="Every site is different. Choose yours to see how we can help.", crumbs=[("Sectors", "sectors.html")], image=IMG_DRAIN)
body += cards([("Food & drink", "Food waste, tank cleaning and process liquid waste for food and drink producers.", "food-drink.html"),
               ("Commercial & industrial", "Interceptors, gullies, tanks and site drainage kept compliant and working.", "commercial-industrial.html"),
               ("Homes", "Septic tanks, treatment plants and private pump stations, installed and looked after.", "homes.html"),
               ("Developers", "Adoptable pumping stations from design to commissioning and adoption.", "developers.html"),
               ("Estates & management companies", "Shared pump stations and private sewers managed for residents.", "estates.html")], alt=True)
add("sectors.html", title=f"Who We Help | {AREA} | ASG", description="Drainage, pump station and waste services for food and drink producers, businesses, homeowners, developers and estates across Evesham and Worcestershire.",
    body=body, crumbs=[("Sectors", "sectors.html")])


def sector(path, *, name, title, description, h1, lead, image=None, image_alt="", challenge_head, challenge_paras, challenges, services, review_keys, faq):
    crumbs = [("Sectors", "sectors.html"), (name, path)]
    image = image or IMG_DRAIN
    body = page_hero(eyebrow=name, h1=h1, lead=lead, crumbs=crumbs, image=image, image_alt=image_alt)
    body += split(challenge_head, challenge_paras, challenges)
    body += cards(services, head="How we can help", alt=True)
    body += reviews(list(review_keys))
    body += nudge(image=other(image))
    body += faqs(faq, alt=True)
    add(path, title=title, description=description, body=body, crumbs=crumbs, extra_ld=[faq_ld(faq)], current="sectors.html")


sector("food-drink.html", name="Food & drink",
       title=f"Food & Drink Site Services: Food Waste & Tank Cleaning | {AREA} | ASG",
       description="Food waste collection, tank cleaning, process liquid waste and site drainage for food and drink producers across Evesham and Worcestershire.",
       h1="Food & drink producers.", lead="Food waste, tank cleaning and process liquids handled properly and planned around your production.",
       image=IMG_TANKER, image_alt="Vacuum tanker at a food production site",
       challenge_head="We know production can't stop.",
       challenge_paras=["Food and drink sites produce waste that has to be dealt with quickly, safely and with the right paperwork, without getting in the way of production.",
                        "We get to know your site and your streams, then plan collections, cleans and maintenance around your shifts."],
       challenges=["Food waste and by-products", "Process liquids and wash water", "Tanks that need regular cleaning", "Site drainage under heavy load", "Audit-ready waste paperwork"],
       services=[("Food waste", "Collections and disposal routes for every stream.", "food-waste.html"),
                 ("Tank cleaning", "Process and storage tanks emptied and cleaned.", "tank-cleaning.html"),
                 ("Liquid waste", "Process liquids and wash water collected.", "liquid-waste.html"),
                 ("Jetting & drain cleaning", "Drains kept clear of fat and debris.", "jetting-drain-cleaning.html"),
                 ("Asset management", "Your whole site looked after under one plan.", "asset-management.html"),
                 ("Emergency response", "24/7 when something goes wrong.", "emergency-flood-response.html")],
       review_keys=("telemetry",),
       faq=[("Can you work around our production schedule?", "Yes. We plan collections and cleans around your shifts and downtime."),
            ("Do you provide waste documentation for audits?", "Yes. Every collection comes with the right paperwork."),
            ("Can you handle all our liquid waste streams?", "Tell us what you produce and we'll work out the right route for each one.")])

sector("commercial-industrial.html", name="Commercial & industrial",
       title=f"Commercial & Industrial Drainage and Waste Services | {AREA} | ASG",
       description="Interceptor cleaning, gully emptying, tank cleaning, drainage maintenance and liquid waste for commercial and industrial sites across Evesham and Worcestershire.",
       h1="Commercial & industrial sites.", lead="Interceptors, gullies, tanks and site drainage kept compliant, working and off your to-do list.",
       image=IMG_DRAIN, image_alt="Drainage works on a commercial site",
       challenge_head="Compliance without the chasing.",
       challenge_paras=["Commercial sites rely on drainage and liquid waste systems that only get noticed when they fail: a flooded car park, an overflowing interceptor or a blocked drain at the worst moment.",
                        "We take ownership of them, plan the work and keep records, so you're compliant and covered."],
       challenges=["Oil interceptors and gullies", "Storage and process tanks", "Site drainage and flooding", "Liquid and hazardous waste", "Multiple sites and properties"],
       services=[("Interceptor & gully cleaning", "Scheduled emptying and inspections.", "interceptor-gully-cleaning.html"),
                 ("Tank cleaning", "Storage and process tanks cleaned safely.", "tank-cleaning.html"),
                 ("CCTV drain surveys", "Find the cause of drainage problems.", "cctv-drain-surveys.html"),
                 ("Drainage remedial works", "Fix failing drainage properly.", "drainage-installation.html"),
                 ("Liquid & hazardous waste", "Collected and documented properly.", "waste-management.html"),
                 ("Asset management", "All your sites under one plan.", "asset-management.html")],
       review_keys=("commercial", "warehouse"),
       faq=[("Can you look after several sites?", "Yes. We can manage multiple sites and properties under one agreement."),
            ("Do you keep records for compliance?", "Yes. You get service reports and waste paperwork for every visit."),
            ("Can you remind us when services are due?", "Yes, without the pushy sales pitch.")])

sector("homes.html", name="Homes",
       title=f"Septic Tanks, Treatment Plants & Private Pump Stations for Homes | {AREA} | ASG",
       description="Septic tank and sewage treatment plant installation, emptying and servicing, private pump stations and emergency drainage for homeowners across Evesham and Worcestershire.",
       h1="Homes with private drainage.", lead="Septic tanks, treatment plants and private pump stations installed, serviced and looked after, with someone to call when it goes wrong.",
       challenge_head="Off-mains drainage, without the worry.",
       challenge_paras=["If your home isn't on mains drainage, you're responsible for the system that serves it. Most people only think about it when something goes wrong.",
                        "We can install the right system, keep it serviced and emptied, and be there 24/7 if it fails."],
       challenges=["Septic tanks and cesspits", "Sewage treatment plants", "Private pump stations", "Old or failing systems", "Emergencies at weekends"],
       services=[("Septic tanks & treatment plants", "New, replacement and upgraded systems.", "septic-tanks-treatment-plants.html"),
                 ("Emptying", "Septic tank and cesspit emptying.", "tankering.html"),
                 ("Pump station maintenance", "Private pump stations serviced.", "pump-station-maintenance.html"),
                 ("CCTV drain surveys", "Find out what's wrong with your drains.", "cctv-drain-surveys.html"),
                 ("Emergency response", "24/7 if your system fails.", "emergency-flood-response.html"),
                 ("Ongoing care", "Servicing and emptying on a schedule.", "asset-management.html")],
       review_keys=("homeowner",),
       faq=[("How often should my septic tank be emptied?", "Usually at least once a year, depending on the tank and how many people live there. We can remind you."),
            ("Do I need to replace my septic tank?", "Not always. It depends on its condition and where it discharges. We'll give you an honest answer."),
            ("What if my pump station fails at the weekend?", f"Call our 24/7 line on {PHONE}.")])

sector("developers.html", name="Developers",
       title=f"Adoptable Pumping Stations & Section 104 Support for Developers | {AREA} | ASG",
       description="Adoptable pumping station installation, maintenance, telemetry and Section 104 adoption support for housing developers across Worcestershire and surrounding counties.",
       h1="Developers & housebuilders.", lead="Adoptable pumping stations and sewers taken from design through commissioning, maintenance and adoption, with one partner keeping it moving.",
       image=IMG_PUMP, image_alt="Wastewater treatment works with pumps and pipework",
       challenge_head="A clear route to adoption.",
       challenge_paras=["Adoption delays cost developers time and money. Stations that don't meet the standard, missing records or problems during the maintenance period can hold up handover for months.",
                        "We work with you from design stage to get it right, look after the station until adoption, and use telemetry where it helps to catch issues early."],
       challenges=["Adoptable pumping stations", "Section 104 sewers", "Maintenance before adoption", "Pre-adoption surveys and records", "Water company liaison"],
       services=[("Pump station installation", "Adoptable stations designed and installed.", "pump-station-installation.html"),
                 ("Pump station maintenance", "Looked after until adoption.", "pump-station-maintenance.html"),
                 ("CCTV drain surveys", "Pre-adoption sewer surveys.", "cctv-drain-surveys.html"),
                 ("Asset management", "Telemetry, servicing and reports in one plan.", "asset-management.html"),
                 ("Tankering", "Pump-outs during construction and faults.", "tankering.html"),
                 ("Emergency response", "24/7 cover for your sites.", "emergency-flood-response.html")],
       review_keys=("developer", "property"),
       faq=[("Do you support Section 104 adoption?", "Yes. We install and maintain stations intended for adoption and support the process through to handover."),
            ("Can you maintain stations before adoption?", "Yes. We provide servicing, monitoring and response during the maintenance period."),
            ("Can you take on a station mid-project?", "Yes. We'll review where it is and what's needed to get it adopted.")])

sector("estates.html", name="Estates & management companies",
       title=f"Shared Pump Stations & Private Sewers for Estates | {AREA} | ASG",
       description="Management of shared pump stations, private sewers and treatment systems for estates, residents' management companies and managing agents across Worcestershire.",
       h1="Estates & management companies.", lead="Shared pump stations, private sewers and treatment systems looked after for residents and managing agents, under one agreement.",
       challenge_head="Shared assets need one owner.",
       challenge_paras=["On estates with private drainage, nobody wants to be the person dealing with the pump station. Responsibility gets passed around until something fails.",
                        "We take that responsibility: planned servicing, monitoring where it helps, emergency response and clear reports you can share with residents."],
       challenges=["Shared pump stations", "Private sewers and chambers", "Shared treatment plants", "Unadopted estate drainage", "Clear reporting for residents"],
       services=[("Asset management", "One agreement for the whole estate.", "asset-management.html"),
                 ("Pump station maintenance", "Shared stations serviced and monitored.", "pump-station-maintenance.html"),
                 ("CCTV drain surveys", "Condition surveys of estate drainage.", "cctv-drain-surveys.html"),
                 ("Jetting & drain cleaning", "Blockages cleared quickly.", "jetting-drain-cleaning.html"),
                 ("Emergency response", "24/7 for residents' peace of mind.", "emergency-flood-response.html"),
                 ("Adoption support", "Where adoption is still possible.", "developers.html")],
       review_keys=("property", "telemetry"),
       faq=[("Can you work with our managing agent?", "Yes. We can report to the managing agent, the management company or both."),
            ("Can you take over from another contractor?", "Yes. We start by reviewing the assets and their history."),
            ("Do residents get a 24/7 number?", f"Yes. Our emergency line is {PHONE}.")])

# =====================================================================
# ABOUT / CONTACT / PRIVACY
# =====================================================================
body = page_hero(eyebrow="About ASG", h1="Problem solvers, not just a contractor.",
                 lead="Aura Solutions Group looks after the systems beneath your site: pump stations, drainage, tanks and the waste they produce.", crumbs=[("About", "about.html")], image=IMG_PUMP)
body += split("We learn your site, not just the job.",
              ["We started ASG because too many sites were let down by contractors who turned up, did the minimum and left. We wanted to work differently.",
               "We take time to understand how each site operates and what it relies on. We look at the bigger picture, tell you honestly what we find, good or bad, and work with you to put it right.",
               "Through our wide network we bring in the right kit for every job, and our own telemetry and reporting give you visibility where it helps."],
              ["Consultative, honest advice", "One partner from installation to waste", "The right kit for every job", "Clear reports in plain English", "24/7 emergency response", "Registered waste carrier and broker"])
body += reviews(["sitemanager", "commercial"], alt=True)
add("about.html", title=f"About Aura Solutions Group | {AREA}", description="Aura Solutions Group (ASG) is a drainage, pump station and liquid waste partner for homes, businesses and developers across Evesham and Worcestershire.",
    body=body, crumbs=[("About", "about.html")])

body = page_hero(eyebrow="Contact", h1="Let's talk about your site.",
                 lead=f"Call us on {PHONE}, email info@aurasolutions.co.uk or send the form below. For emergencies, always call.", crumbs=[("Contact", "contact.html")], image=IMG_DRAIN)
add("contact.html", title=f"Contact Aura Solutions Group | {AREA}", description=f"Contact Aura Solutions Group for drainage, pump station and liquid waste services across Evesham and Worcestershire. 24/7 emergency line {PHONE}.",
    body=body, crumbs=[("Contact", "contact.html")])

privacy = f'''<section class="block"><div class="wrap prose">
<p>This notice explains how Aura Solutions Group Limited ("ASG", "we") uses personal information collected through this website.</p>
<h2>Who we are</h2><p>Aura Solutions Group Limited, company no. 15761350, registered office Main Street, Sedgeberrow, Evesham, England, WR11 7UH. Contact: <a href="mailto:info@aurasolutions.co.uk">info@aurasolutions.co.uk</a> or {PHONE}.</p>
<h2>What we collect</h2><p>When you send an enquiry we collect the details you give us: your name, phone number, email address, site postcode and a description of what you need.</p>
<h2>Why we use it</h2><p>We use your details to respond to your enquiry and, if you go ahead, to provide our services. Our lawful basis is our legitimate interest in responding to enquiries and taking steps at your request before entering into a contract.</p>
<h2>Who we share it with</h2><p>We don't sell your information. We share it only with service providers who help us run our business, such as our website and database hosting, and with contractors we arrange to carry out work you've asked for.</p>
<h2>How long we keep it</h2><p>We keep enquiry details for as long as needed to deal with your enquiry and for a reasonable period afterwards. If you become a customer, we keep records for as long as required for legal and accounting purposes.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete the information we hold about you, or object to how we use it, by contacting us at the details above. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
<h2>Cookies</h2><p>This website does not use tracking or advertising cookies.</p>
</div></section>'''
body = page_hero(eyebrow="Privacy", h1="Privacy notice.", lead="How we use the information you give us through this website.", crumbs=[("Privacy", "privacy.html")]) + privacy
add("privacy.html", title="Privacy Notice | Aura Solutions Group", description="How Aura Solutions Group uses personal information collected through aurasolutions.co.uk.",
    body=body, crumbs=[("Privacy", "privacy.html")], enquiry=False)


# Search titles (kept under ~65 characters so Google shows them in full)
TITLES = {
    "index.html": "Drainage, Pump Station & Liquid Waste Services | Evesham | ASG",
    "asset-management.html": "Drainage & Pump Station Asset Management | Worcestershire",
    "installation-repairs.html": "Drainage Installation & Repairs | Evesham | ASG",
    "drainage-installation.html": "Drainage Installation & Remedial Works | Evesham | ASG",
    "septic-tanks-treatment-plants.html": "Septic Tank & Treatment Plant Installation | Evesham | ASG",
    "pump-station-installation.html": "Pump Station Installation & Adoptable Stations | ASG",
    "gully-interceptor-installation.html": "Interceptor & Gully Installation | Evesham | ASG",
    "site-services.html": "Tank Cleaning, Jetting, CCTV & Tankering | Evesham | ASG",
    "pump-station-maintenance.html": "Pump Station Maintenance & Servicing | Worcestershire | ASG",
    "tank-cleaning.html": "Tank Cleaning Services | Evesham & Worcestershire | ASG",
    "jetting-drain-cleaning.html": "Drain Jetting & Drain Cleaning | Evesham | ASG",
    "cctv-drain-surveys.html": "CCTV Drain Surveys | Evesham & Worcestershire | ASG",
    "interceptor-gully-cleaning.html": "Interceptor Cleaning & Gully Emptying | Evesham | ASG",
    "tankering.html": "Tankering Services & Emergency Tankers | Evesham | ASG",
    "emergency-flood-response.html": "24/7 Emergency Drainage & Flood Response | Evesham | ASG",
    "waste-management.html": "Liquid, Food & Hazardous Waste Management | ASG",
    "liquid-waste.html": "Liquid Waste Collection & Disposal | Evesham | ASG",
    "food-waste.html": "Food Waste Collection for Food Producers | Evesham | ASG",
    "hazardous-waste.html": "Hazardous Liquid Waste Collection | Evesham | ASG",
    "sectors.html": "Who We Help | Aura Solutions Group",
    "food-drink.html": "Food & Drink Site Services & Food Waste | Evesham | ASG",
    "commercial-industrial.html": "Commercial Drainage & Waste Services | Evesham | ASG",
    "homes.html": "Septic Tanks & Private Pump Stations for Homes | ASG",
    "developers.html": "Adoptable Pumping Stations & Section 104 Support | ASG",
    "estates.html": "Shared Pump Stations & Private Sewers for Estates | ASG",
}
DESCRIPTIONS = {
    "index.html": "Pump station maintenance, drainage asset management, septic tanks, CCTV surveys, interceptor cleaning, tankering and 24/7 emergency response in Worcestershire.",
    "asset-management.html": "Pump stations, tanks, interceptors and private drainage looked after under one plan across Worcestershire, with telemetry where it helps and 24/7 response.",
    "developers.html": "Adoptable pumping station installation, maintenance and Section 104 adoption support for housing developers across Worcestershire.",
    "drainage-installation.html": "New drainage installation and drainage repairs for homes and businesses around Evesham and Worcestershire, done right first time.",
    "food-waste.html": "Food waste and food-processing liquid waste collection for food and drink producers around Evesham and Worcestershire, fully documented.",
    "homes.html": "Septic tank and treatment plant installation, emptying and servicing, private pump stations and 24/7 emergency drainage for homes in Worcestershire.",
    "liquid-waste.html": "Wastewater, sewage, process liquids, interceptor waste and tank contents collected and disposed of properly around Evesham and Worcestershire.",
}

# Service pre-selected in each page's enquiry form
SERVICE_DEFAULT = {
    "asset-management.html": "Asset management / ongoing care",
    "estates.html": "Asset management / ongoing care",
    "installation-repairs.html": "Installation or repair",
    "drainage-installation.html": "Installation or repair",
    "septic-tanks-treatment-plants.html": "Installation or repair",
    "pump-station-installation.html": "Installation or repair",
    "gully-interceptor-installation.html": "Installation or repair",
    "pump-station-maintenance.html": "Pump station maintenance",
    "tank-cleaning.html": "Tank cleaning or jetting",
    "jetting-drain-cleaning.html": "Tank cleaning or jetting",
    "cctv-drain-surveys.html": "CCTV drain survey",
    "interceptor-gully-cleaning.html": "Interceptor or gully cleaning",
    "tankering.html": "Tankering or liquid waste",
    "liquid-waste.html": "Tankering or liquid waste",
    "waste-management.html": "Food or hazardous waste",
    "food-waste.html": "Food or hazardous waste",
    "food-drink.html": "Food or hazardous waste",
    "hazardous-waste.html": "Food or hazardous waste",
    "emergency-flood-response.html": "Emergency or flooding",
}

# Old addresses that now live elsewhere
REDIRECTS = {
    "civils-installations.html": "installation-repairs.html",
    "septic-tank-installation.html": "septic-tanks-treatment-plants.html",
    "sewage-treatment-systems.html": "septic-tanks-treatment-plants.html",
    "gully-interceptor-maintenance.html": "interceptor-gully-cleaning.html",
    "industrial-services.html": "site-services.html",
    "liquid-waste-collection.html": "liquid-waste.html",
    "hazardous-liquid-waste.html": "hazardous-waste.html",
    "asset-service-agreements.html": "asset-management.html",
    "smart-telemetry-monitoring.html": "asset-management.html",
    "commercial-asset-management.html": "commercial-industrial.html",
    "domestic-asset-management.html": "homes.html",
    "developer-adoption-management.html": "developers.html",
    "estates-shared-site-management.html": "estates.html",
    "home-preview.html": "index.html",
}


def build(out, preview=False):
    os.makedirs(out, exist_ok=True)
    for path, kw in PAGES.items():
        kw = dict(kw)
        kw["title"] = TITLES.get(path, kw["title"])
        kw["description"] = DESCRIPTIONS.get(path, kw["description"])
        kw["service"] = SERVICE_DEFAULT.get(path)
        html = page(path=path, noindex=preview, **kw)
        with open(os.path.join(out, path), "w", encoding="utf-8") as f:
            f.write(html)
    for old, new in REDIRECTS.items():
        with open(os.path.join(out, old), "w", encoding="utf-8") as f:
            f.write(redirect(new))
    return sorted(PAGES)




def build_preview(out):
    """Preview copy in a sub-folder: shared files are loaded from the site root."""
    pages = build(out, preview=True)
    for name in os.listdir(out):
        p = os.path.join(out, name)
        s = open(p, encoding="utf-8").read()
        for a in ('href="styles.css"', 'href="home.css"', 'href="pages.css"', 'href="favicon-192.png"', 'src="script.js"'):
            s = s.replace(a, a.replace('="', '="../'))
        s = s.replace('src="assets/', 'src="../assets/')
        open(p, "w", encoding="utf-8").write(s)
    return pages


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = args[0] if args else os.path.join(os.path.dirname(__file__), "..")
    pages = build_preview(out) if "--preview" in sys.argv else build(out)
    print(len(pages), "pages,", len(REDIRECTS), "redirects ->", os.path.abspath(out))

