"""Build the Insights blog: content/insights/*.html -> insights/<slug>/index.html + insights/index.html + sitemap.
Each content file starts with a JSON front-matter block between <!--META and META--> :
  {"slug","title","description","date":"YYYY-MM-DD","author","tags":[...],"read":"6 min","cta":"switch|roi|trial"}
Run: python3 tools/build_insights.py
"""
import json, re, glob, os, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&tab=e&utm_source=npssurveys.com&utm_medium=blog&utm_campaign=cxos_insights"
SITE = "https://www.npssurveys.com"
CAL = "https://calendly.com/npssurvey/demo?utm_source=npssurveys.com&utm_medium=blog&utm_campaign=cxos_insights"

CSS = """:root{--blue:#002FA7;--blue-deep:#002FA7;--yellow:#FFFFFF;--navy:#0F1A3D;--bg:#fff;--bg-tint:#F4F7FF;--surface:#fff;--line:#DCE4F7;--fg:#0F1A3D;--fg-soft:#3B4877;--fg-mute:#5E6B98;--link:#002FA7;--font:"IBM Plex Sans",system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
h1,h2,.h2{font-family:"IBM Plex Serif",Georgia,"Times New Roman",serif!important;font-weight:600!important;letter-spacing:-.012em!important}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0A1230;--bg-tint:#111C45;--surface:#111C45;--line:#24326A;--fg:#EEF2FF;--fg-soft:#C5D0F2;--fg-mute:#97A5D6;--link:#8FB0FF}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--font);font-size:17px;line-height:1.65}
a{color:var(--link)}img{max-width:100%}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}.narrow{max-width:760px;margin:0 auto;padding:0 20px}
.annc{background:#EDF1FB;color:#002FA7;font-weight:600;font-size:.9rem;text-align:center;padding:9px 16px}.annc a{color:#002FA7}
header{background:var(--blue-deep);color:#fff}header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:14px}
.logo{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:800}.logo img{width:36px;height:36px}.logo small{display:block;font-weight:600;font-size:.72rem;opacity:.8}
nav a{color:#fff;text-decoration:none;font-weight:600;margin-left:18px;font-size:.95rem}nav a.btn{background:#fff;color:#002FA7;padding:9px 16px;border-radius:999px}
@media (max-width:720px){nav a:not(.btn){display:none}}
.hero{background:#002FA7;color:#fff;padding:52px 0 56px}
.hero h1{font-size:clamp(1.9rem,4.2vw,2.9rem);line-height:1.1;margin:10px 0 12px;font-weight:800}.hero p{color:#D6E2FF;font-size:1.1rem;margin:0}
.crumb{font-size:.88rem;color:#D6E2FF}.crumb a{color:#fff}.meta{margin-top:16px;font-size:.88rem;color:#D6E2FF}
article{padding:44px 0 20px}article h2{font-size:1.6rem;line-height:1.2;margin:40px 0 10px}article h3{font-size:1.2rem;margin:28px 0 8px}
article p,article li{color:var(--fg-soft)}article strong{color:var(--fg)}
article table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.95rem}article th,article td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}article th{background:var(--bg-tint)}
.tw{overflow-x:auto}
.cta{background:var(--bg-tint);border:1px solid var(--line);border-radius:18px;padding:24px;margin:36px 0}.cta h3{margin:0 0 6px}.cta .call{margin:16px 0 0;font-size:.95rem;border-top:1px solid var(--line);padding-top:14px}.cta .call a{font-weight:700}
.b{display:inline-flex;align-items:center;font-weight:700;border-radius:999px;padding:12px 20px;text-decoration:none;margin:10px 10px 0 0}.b.p{background:#002FA7;color:#fff}.b.d{background:#fff;color:#002FA7;border:2px solid #002FA7}
figure.fig{margin:28px 0;}figure.fig svg{width:100%;height:auto;display:block;border-radius:18px;box-shadow:0 10px 30px rgba(12,24,74,.08)}@media (max-width:640px){figure.fig{overflow-x:auto}figure.fig svg{min-width:620px}}figure.fig figcaption{font-size:.85rem;color:var(--fg-mute);margin-top:8px;text-align:center}
.src{font-size:.88rem;color:var(--fg-mute);border-top:1px solid var(--line);margin-top:36px;padding-top:16px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;padding:40px 0 60px}
.card{border:1px solid var(--line);border-radius:18px;padding:22px;text-decoration:none;color:var(--fg);background:var(--surface);display:flex;flex-direction:column;gap:8px}
.card h2{font-size:1.2rem;margin:0;line-height:1.3}.card p{color:var(--fg-soft);margin:0;font-size:.95rem}.tag{font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--link)}
.card .more{margin-top:auto;font-weight:700;color:var(--link);font-size:.9rem}
footer{border-top:1px solid var(--line);padding:28px 0;font-size:.85rem;color:var(--fg-mute)}
"""

def head(title, desc, url, extra=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#002FA7">
<meta property="og:type" content="article"><meta property="og:site_name" content="NPS Survey CX OS"><meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}/share.png"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Serif:wght@500;600&display=swap">
<style>{CSS}</style>{extra}</head><body>
<div class="annc">GetFeedback retires December 31, 2026. <a href="/#switch">Move your surveys to native Salesforce &rarr;</a></div>
<header><div class="wrap"><a class="logo" href="/"><img src="/brand/logo/nps-survey-cx-os-mark-white.svg" alt=""><span>NPS Survey<small>CX OS by SalesHub</small></span></a>
<nav><a href="/#platform">Product</a><a href="/#industries">Solutions</a><a href="/insights/">Insights</a><a href="/#partners">Partners</a><a href="/#pricing">Pricing</a><a class="btn" href="{LIST}&utm_content=blog_nav" target="_blank" rel="noopener">Free trial</a></nav></div></header>"""

FOOT = """<footer><div class="wrap">&copy; 2026 SalesHub, LLC &middot; 1853 Piedmont Rd, Suite 301, Marietta, GA 30066 &middot; <a href="mailto:support@saleshub.info">support@saleshub.info</a> &middot; 1 (833) 733-2468<br>
Salesforce and AppExchange are trademarks of Salesforce, Inc. Net Promoter&reg;, NPS&reg; and the NPS-related emoticons are registered trademarks of Bain &amp; Company, Inc., NICE Systems, Inc. and Fred Reichheld.</div></footer></body></html>"""

CTAS = {
 "switch": ("Moving off GetFeedback or Delighted?", "Keep your surveys, follow-up and dashboards inside Salesforce. Start the 15-day free trial, or book a 30-minute switch call.", [("Start the free trial", "p", "trial"), ("See the switch plan", "d", "/#switch")]),
 "roi": ("Build the business case in 60 seconds", "Put in your accounts, revenue and churn and get a one-page case you can send to finance.", [("Open the ROI calculator", "d", "/#roi"), ("Start the free trial", "p", "trial")]),
 "public": ("Measure service where it happens", "NPS Survey CX OS runs inside the Salesforce org your agency already uses. Buy through Carahsoft or start on AppExchange.", [("Public sector solutions", "d", "/#public-sector"), ("Start the free trial", "p", "trial")]),
 "partner": ("Deliver the migration, keep the services", "Implementation partners keep 100% of their services revenue and earn 25% of the first-year subscription plus 10% of every renewal.", [("See the partner program", "p", "/#partners"), ("See the switch plan", "d", "/#switch")]),
 "trial": ("Close the loop on every score", "NPS, CSAT and CES surveys that send themselves, land on the record and give every unhappy customer an owner, 100% inside Salesforce.", [("Start the free trial", "p", "trial"), ("Book a demo", "d", "/#demo")]),
}

def cta_html(kind, slug):
    t, p, bs = CTAS[kind]
    links = "".join(f'<a class="b {c}" href="{(LIST+"&utm_content=blog_"+slug) if h=="trial" else h}"{" target=_blank rel=noopener" if h=="trial" else ""}>{l} &rarr;</a>' for l, c, h in bs)
    call = f'<p class="call">Prefer to talk it through? <a href="{CAL}&utm_content=blog_call_{slug}" target="_blank" rel="noopener">Book a 30-minute call</a> with our team. We will look at your org and your surveys with you.</p>'
    return f'<div class="cta"><h3>{t}</h3><p>{p}</p>{links}{call}</div>'

def load():
    posts = []
    for f in glob.glob(os.path.join(ROOT, "content/insights/*.html")):
        raw = open(f).read()
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*META-->(.*)", raw, re.S)
        meta = json.loads(m.group(1)); meta["body"] = m.group(2); posts.append(meta)
    return sorted(posts, key=lambda p: (p["date"], p["slug"]), reverse=True)

def figs(body):
    def rep(m):
        name, _, cap = m.group(1).partition("|")
        svg = open(os.path.join(ROOT, "content/figures", name.strip() + ".svg")).read()
        return f'<figure class="fig">{svg}<figcaption>{html.escape(cap.strip())}</figcaption></figure>'
    return re.sub(r"\{\{FIG:([^}]+)\}\}", rep, body)

def fmt(d): return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")

def build():
    posts = load()
    for p in posts:
        url = f"{SITE}/insights/{p['slug']}/"
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"], "datePublished": p["date"],
              "author": {"@type": "Organization", "name": p.get("author", "SalesHub")}, "publisher": {"@type": "Organization", "name": "SalesHub, LLC"}, "mainEntityOfPage": url, "image": f"{SITE}/share.png"}
        body = figs(p["body"]).replace("{{CTA}}", cta_html(p.get("cta", "trial"), p["slug"])).replace("{{TRIAL}}", LIST + "&utm_content=blog_" + p["slug"])
        page = head(p["title"] + " | NPS Survey CX OS", p["description"], url, f'<script type="application/ld+json">{json.dumps(ld)}</script>') + f"""
<section class="hero"><div class="narrow"><div class="crumb"><a href="/insights/">Insights</a> &middot; {html.escape(" · ".join(p.get("tags", [])))}</div>
<h1>{html.escape(p["title"])}</h1><p>{html.escape(p["description"])}</p><div class="meta">{html.escape(p.get("author","SalesHub"))} &middot; {fmt(p["date"])} &middot; {p.get("read","")} read</div></div></section>
<main class="narrow"><article>{body}{cta_html(p.get("cta","trial"), p["slug"]) if "{{CTA}}" not in p["body"] else ""}</article></main>""" + FOOT
        os.makedirs(os.path.join(ROOT, "insights", p["slug"]), exist_ok=True)
        open(os.path.join(ROOT, "insights", p["slug"], "index.html"), "w").write(page)
    cards = "".join(f'<a class="card" href="/insights/{p["slug"]}/"><span class="tag">{html.escape((p.get("tags") or [""])[0])}</span><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["description"])}</p><span class="more">{fmt(p["date"])} &middot; {p.get("read","")} read &rarr;</span></a>' for p in posts)
    idx = head("Insights: customer experience inside Salesforce | NPS Survey CX OS", "Practical guides on NPS, CSAT and closed-loop feedback in Salesforce, for CX leaders, Salesforce admins and public sector teams.", f"{SITE}/insights/") + f"""
<section class="hero"><div class="wrap"><div class="crumb"><a href="/">Home</a> &middot; Insights</div><h1>Insights</h1><p>Practical guides on running feedback programs inside Salesforce, for CX leaders, admins and public sector teams. New posts every week.</p></div></section>
<main class="wrap"><div class="cards">{cards}</div></main>""" + FOOT
    open(os.path.join(ROOT, "insights", "index.html"), "w").write(idx)
    # sitemap
    sm = os.path.join(ROOT, "sitemap.xml"); s = open(sm).read()
    s = re.sub(r"\s*<url><loc>https://www\.npssurveys\.com/insights/[^<]*</loc>.*?</url>", "", s, flags=re.S)
    today = datetime.date.today().isoformat()
    add = f"\n  <url><loc>{SITE}/insights/</loc><lastmod>{today}</lastmod></url>" + "".join(f"\n  <url><loc>{SITE}/insights/{p['slug']}/</loc><lastmod>{p['date']}</lastmod></url>" for p in posts)
    s = s.replace("</urlset>", add + "\n</urlset>"); open(sm, "w").write(s)
    print("built", len(posts), "posts")

if __name__ == "__main__":
    build()
