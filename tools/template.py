"""Shared page template for aurasolutions.co.uk.

Every page is built from this one file, so the header, menu, emergency strip,
enquiry form and footer stay identical everywhere. Branding (logo, colours)
lives in styles.css, so a rebrand is a single change.
"""
import html as _html
import json

SITE = "https://aurasolutions.co.uk"
PHONE = "01386 571556"
TEL = "+441386571556"
EMAIL = "info@aurasolutions.co.uk"
ENQUIRY_ENDPOINT = "https://tatuejkauahqsgzwalid.supabase.co/functions/v1/website-enquiry"

MENU = [
    ("Asset Management", "asset-management.html", []),
    ("Installation & Repairs", "installation-repairs.html", [
        ("Drainage installation & remedial works", "drainage-installation.html"),
        ("Septic tanks & treatment plants", "septic-tanks-treatment-plants.html"),
        ("Pump station installation", "pump-station-installation.html"),
        ("Gully & interceptor installation", "gully-interceptor-installation.html"),
    ]),
    ("Site Services", "site-services.html", [
        ("Pump station maintenance", "pump-station-maintenance.html"),
        ("Tank cleaning", "tank-cleaning.html"),
        ("Jetting & drain cleaning", "jetting-drain-cleaning.html"),
        ("CCTV drain surveys", "cctv-drain-surveys.html"),
        ("Interceptor & gully cleaning", "interceptor-gully-cleaning.html"),
        ("Tankering & emergency tankers", "tankering.html"),
        ("Emergency & flood response", "emergency-flood-response.html"),
    ]),
    ("Waste Management", "waste-management.html", [
        ("Liquid waste collections", "liquid-waste.html"),
        ("Food waste", "food-waste.html"),
        ("Hazardous waste", "hazardous-waste.html"),
        ("Spill response", "emergency-flood-response.html#spills"),
    ]),
    ("Sectors", "sectors.html", [
        ("Food & drink", "food-drink.html"),
        ("Commercial & industrial", "commercial-industrial.html"),
        ("Homes", "homes.html"),
        ("Developers", "developers.html"),
        ("Estates & management companies", "estates.html"),
    ]),
]

SERVICES_SELECT = [
    "Asset management / ongoing care", "Installation or repair", "Pump station maintenance",
    "Tank cleaning or jetting", "CCTV drain survey", "Interceptor or gully cleaning",
    "Tankering or liquid waste", "Food or hazardous waste", "Emergency or flooding", "Something else",
]

REVIEWS = {
    "developer": ("We dealt with Paul throughout a pumping station project on one of our housing sites. He kept things moving from design stage right through to commissioning and was always available when we needed an answer. We had some blockage and ingress issues along the way, but the Aura telemetry meant we could deal with these before they became an issue. The station was adopted without any issues.", "Residential developer", "Stratford-upon-Avon"),
    "commercial": ("We've used ASG for several years now across multiple commercial properties. The service is always reliable whether it's a blocked drain, interceptor cleaning or a planned maintenance visit. The engineers are knowledgeable and the reports are far more detailed than we've received from previous contractors. They remind us when services are due without a pushy sales pitch and just make things easy.", "Facilities manager", "Multiple commercial units"),
    "warehouse": ("Adam and the team helped us investigate recurring flooding around our warehouse. The CCTV survey identified several issues that had been missed by other contractors. The remedial works were completed quickly and we've had no further problems.", "Operations manager", "Warehouse"),
    "property": ("We initially brought Aura Solutions in to install a pumping station, but they've since taken over the ongoing maintenance and monitoring as well. Having one company responsible for everything makes life much easier.", "Property management company", ""),
    "homeowner": ("Steph was brilliant from start to finish. We had an emergency with our private sewage pumping station over a weekend and she arranged attendance almost immediately. The engineer diagnosed the fault and got everything back up and running within hours.", "Homeowner", "Private pumping station"),
    "telemetry": ("The Aura telemetry system has been a game changer. We receive alerts before minor issues become major ones and can see exactly how our assets are performing through the monthly reports. Since ASG started managing the site we've seen a noticeable reduction in emergency call-outs and cost!", "Facilities manager", ""),
    "sitemanager": ("Not often you can say a contractor exceeds expectations these days, but these guys did. Good communication, realistic timescales and no surprises. They simply got on with the job. They didn't always tell us what we wanted to hear but were honest and explained everything, good or bad, in language we could understand.", "Site manager", ""),
}


def e(s):
    return _html.escape(s, quote=True)


def review_html(key):
    text, who, where = REVIEWS[key]
    cap = e(who) + (f"<span>{e(where)}</span>" if where else "")
    return (f'<figure class="review"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div>'
            f'<blockquote>"{e(text)}"</blockquote><figcaption>{cap}</figcaption></figure>')


def nav_html(current):
    parts = []
    for i, (label, href, kids) in enumerate(MENU):
        if not kids:
            parts.append(f'<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{e(label)}</a>')
            continue
        sid = f"sub{i}"
        links = "".join(f'<a href="{h}">{e(t)}</a>' for t, h in kids)
        parts.append(
            f'<div class="nav-group"><div class="nav-group-heading"><a href="{href}">{e(label)}</a>'
            f'<button class="dropdown-toggle" type="button" aria-expanded="false" aria-controls="{sid}" aria-label="Show {e(label)}"><span aria-hidden="true">⌄</span></button></div>'
            f'<div class="nav-dropdown" id="{sid}">{links}</div></div>')
    parts.append('<a href="about.html">About</a><a href="contact.html">Contact</a><a class="nav-login" href="https://app.aurasolutions.co.uk/">Log in</a>')
    return "".join(parts)


def enquiry_html(source, heading="Tell us what needs attention.", intro=None, service=None):
    intro = intro or "A quick description is all we need to get started. We'll come back to you to talk it through. No pushy sales pitch, just honest advice."
    opts = '<option value="">Choose a service</option>' + "".join(
        f'<option{" selected" if o == service else ""}>{e(o)}</option>' for o in SERVICES_SELECT)
    return f'''<section class="enquiry" id="enquire" aria-labelledby="enquire-title">
      <div class="wrap enquiry-grid">
        <div class="enquiry-intro"><p class="eyebrow">Get in touch</p><h2 id="enquire-title">{e(heading)}</h2><p>{e(intro)}</p><p class="contact-phone"><a href="tel:{TEL}">{PHONE}</a></p><p class="contact-email"><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
        <form class="form" data-enquiry data-source="{e(source)}" novalidate>
          <label>Name<input name="name" autocomplete="name" required></label>
          <label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
          <label>Email<input name="email" type="email" autocomplete="email"></label>
          <label>Site postcode<input name="postcode" autocomplete="postal-code"></label>
          <label>What do you need?<select name="service">{opts}</select></label>
          <label>How urgent?<select name="urgency"><option>Planning ahead</option><option>Within a week</option><option>As soon as possible</option><option>Emergency (please also call us)</option></select></label>
          <label class="full">Tell us about it<textarea name="message" placeholder="What's happening on site, and anything we should know"></textarea></label>
          <label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
          <button class="button button-dark" type="submit">Send enquiry <span aria-hidden="true">↗</span></button>
          <p class="form-note">We use your details only to respond to your enquiry. See our <a href="privacy.html">privacy notice</a>.</p>
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>'''


FORM_JS = """<script>
(function(){const t0=Date.now();document.querySelectorAll('form[data-enquiry]').forEach(function(f){f.addEventListener('submit',async function(ev){ev.preventDefault();const s=f.querySelector('.form-status'),b=f.querySelector('button[type=submit]');const d=Object.fromEntries(new FormData(f));if(!d.name||!d.phone){s.className='form-status err';s.textContent='Please add your name and phone number.';return}b.disabled=true;s.className='form-status';s.textContent='Sending...';d.source_page=f.dataset.source+' page ('+location.pathname+')';d.elapsed_ms=Date.now()-t0;try{const r=await fetch('%s',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const j=await r.json();if(r.ok&&j.ok){f.reset();s.className='form-status ok';s.textContent='Thanks, we have your enquiry and will be in touch shortly. For emergencies please call %s.'}else throw 0}catch(_){s.className='form-status err';s.innerHTML='Sorry, that didn\\'t send. Please call %s or email <a href="mailto:%s">%s</a>.'}b.disabled=false})})})();
</script>""" % (ENQUIRY_ENDPOINT, PHONE, PHONE, EMAIL, EMAIL)


def page(*, path, title, description, body, current=None, crumbs=None, noindex=False, extra_ld=None, og_image="assets/liquid-waste-collection-final.webp", source=None, enquiry=True, enquiry_heading=None, service=None):
    url = f"{SITE}/" + ("" if path == "index.html" else path)
    ld = [{"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Aura Solutions Group", "legalName": "Aura Solutions Group Limited", "alternateName": "ASG", "url": f"{SITE}/", "telephone": TEL, "email": EMAIL,
           "address": {"@type": "PostalAddress", "streetAddress": "Main Street", "addressLocality": "Sedgeberrow, Evesham", "addressRegion": "Worcestershire", "postalCode": "WR11 7UH", "addressCountry": "GB"},
           "areaServed": {"@type": "GeoCircle", "geoMidpoint": {"@type": "GeoCoordinates", "latitude": 52.044282, "longitude": -1.974488}, "geoRadius": 32187, "name": "Evesham, Worcestershire and surrounding areas"}}]
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}]
        for i, (name, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": i, "name": name, "item": f"{SITE}/{href}"})
        ld.append({"@type": "BreadcrumbList", "itemListElement": items})
    if extra_ld:
        ld.extend(extra_ld)
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": ld}, separators=(",", ":"))
    robots = '<meta name="robots" content="noindex, nofollow">\n  ' if noindex else ""
    if not source:
        source = crumbs[-1][0] if crumbs else ("Home" if path == "index.html" else path)
    enq = enquiry_html(source, enquiry_heading or "Tell us what needs attention.", service=service) if enquiry else ""
    return f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {robots}<meta name="theme-color" content="#0b3324">
  <link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png">
  <link rel="canonical" href="{url}">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta property="og:site_name" content="Aura Solutions Group">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{og_image}">
  <script type="application/ld+json">{ld_json}</script>
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="home.css">
  <link rel="stylesheet" href="pages.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner wrap">
      <a class="brand" href="index.html" aria-label="ASG Aura Solutions Group, home"><span class="brand-art" aria-hidden="true"></span></a>
      <button class="menu-button" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
      <nav id="primary-nav" class="primary-nav" aria-label="Primary navigation">{nav_html(current or path)}</nav>
      <a class="header-login" href="https://app.aurasolutions.co.uk/" aria-label="Log in to the Aura job system"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>Log in</a>
      <a class="header-cta" href="#enquire">Talk to an expert</a>
    </div>
  </header>
  <div class="emergency-strip"><div class="wrap emergency-strip-inner"><p><strong>24/7 emergency response</strong><span>Pump failure, flooding, blockage or spill?</span></p><a href="tel:{TEL}" aria-label="Call the 24/7 emergency line on {PHONE}">Call now <strong>{PHONE}</strong></a></div></div>
  <main id="main">
{body}
{enq}
  </main>
  <footer class="site-footer"><div class="wrap footer-inner">
    <div><div class="footer-name">ASG <span>Aura Solutions Group</span></div><p class="footer-legal">Aura Solutions Group Limited · Registered in England and Wales, company no. 15761350<br>Registered office: Main Street, Sedgeberrow, Evesham, England, WR11 7UH<br>VAT no. GB 471 3179 91 · Registered waste carrier and broker CBDU631384</p></div>
    <div><a class="footer-phone" href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><div class="footer-links"><a href="asset-management.html">Asset Management</a><a href="installation-repairs.html">Installation &amp; Repairs</a><a href="site-services.html">Site Services</a><a href="waste-management.html">Waste Management</a><a href="sectors.html">Sectors</a><a href="privacy.html">Privacy</a><a href="https://app.aurasolutions.co.uk">Customer login</a></div></div>
  </div></footer>
  <script src="script.js" defer></script>
  {FORM_JS if enquiry else ""}
</body>
</html>
'''


# ---------- building blocks used by the content file ----------

DEFAULT_HERO = "assets/liquid-waste-collection-final.webp"


def page_hero(*, eyebrow, h1, lead, crumbs=None, image=None, image_alt="", primary=("Talk to an expert", "#enquire")):
    """Full-width heading with a faded photo behind it (like the homepage)."""
    crumb = ""
    if crumbs:
        trail = '<a href="index.html">Home</a>' + "".join(
            f'<span aria-hidden="true">/</span>' + (f'<a href="{h}">{e(n)}</a>' if i < len(crumbs) - 1 else f'{e(n)}')
            for i, (n, h) in enumerate(crumbs))
        crumb = f'<nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>'
    img = image or DEFAULT_HERO
    alt = f' role="img" aria-label="{e(image_alt)}"' if image_alt else ' aria-hidden="true"'
    pos = ";background-position:center 92%" if img.endswith(".svg") else (";background-position:center 68%" if "wet-well" in img else "")
    return f'''<section class="page-hero"><div class="page-hero-bg" style="background-image:url('{img}'){pos}"{alt}></div><div class="page-hero-shade"></div><div class="wrap page-hero-inner"><div class="page-hero-copy">{crumb}<p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p>
      <div class="hero-actions"><a class="button button-lime" href="{primary[1]}">{e(primary[0])}</a><a class="button button-dark" href="tel:{TEL}">Call {PHONE} <span aria-hidden="true">↗</span></a></div></div></div></section>'''


def cards(items, head=None, intro=None, alt=False, cols=3, eyebrow=None):
    """items: (title, text) or (title, text, href)."""
    out = []
    for it in items:
        if len(it) == 3:
            out.append(f'<a class="card" href="{it[2]}"><h3>{e(it[0])}</h3><p>{e(it[1])}</p><strong>Find out more ↗</strong></a>')
        else:
            out.append(f'<div class="card"><h3>{e(it[0])}</h3><p>{e(it[1])}</p></div>')
    hd = ""
    if head:
        hd = f'<div class="block-head">{f"<p class=eyebrow>{e(eyebrow)}</p>" if eyebrow else ""}<h2>{e(head)}</h2>{f"<p>{e(intro)}</p>" if intro else ""}</div>'
    grid = "card-grid" + (" two" if cols == 2 else "")
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap">{hd}<div class="{grid}">{"".join(out)}</div></div></section>'


def steps(items, head="How it works", alt=False, eyebrow=None):
    s = "".join(f'<div class="step"><span>0{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(items, 1))
    eb = f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ""
    return f'<section class="block dark"><div class="wrap"><div class="block-head">{eb}<h2>{e(head)}</h2></div><div class="steps">{s}</div></div></section>'


def split(head, paras, ticks, eyebrow=None, alt=False):
    p = "".join(f"<p>{e(x)}</p>" for x in paras)
    t = "".join(f"<li>{e(x)}</li>" for x in ticks)
    eb = f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ""
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap split"><div>{eb}<h2>{e(head)}</h2>{p}</div><ul class="tick-list">{t}</ul></div></section>'


def reviews(keys, head="What customers say", alt=False):
    grid = "review-grid" if len(keys) > 1 else "single-review"
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap"><div class="block-head"><p class="eyebrow">Customer feedback</p><h2>{e(head)}</h2></div><div class="{grid}">{"".join(review_html(k) for k in keys)}</div></div></section>'


def faqs(items, head="Common questions", alt=False):
    d = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    return f'<section class="block{" alt" if alt else ""}"><div class="wrap"><div class="block-head"><h2>{e(head)}</h2></div><div class="faq">{d}</div></div></section>'


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def nudge(head="Want us to look after it for you?", text="Many customers start with one job. Once we know your site, we can take care of all of it under one asset management agreement.", link=("How asset management works", "asset-management.html"), image="assets/pump-station-final.webp"):
    """Full-width photo band with a dark green overlay."""
    return (f'<section class="band" style="background-image:url(\'{image}\')"><div class="band-shade"></div><div class="wrap band-inner"><div><p class="eyebrow">One partner for the whole site</p><h2>{e(head)}</h2><p>{e(text)}</p></div>'
            f'<div class="band-actions"><a class="button button-lime" href="{link[1]}">{e(link[0])} <span aria-hidden="true">↗</span></a><a class="button button-outline-light" href="#enquire">Talk to an expert</a></div></div></section>')


def redirect(to):
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><title>Moved</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="{SITE}/{to}"><meta http-equiv="refresh" content="0; url={to}"></head>
<body><p>This page has moved to <a href="{to}">{SITE}/{to}</a>.</p></body></html>
'''
