"""Build the product tour and its ad kit from tools/tour_data.py.
Run: python3 tools/product_tour.py            (page + figures + copy)
     python3 tools/product_tour.py --ads      (also render the ad images, needs Playwright)
Outputs:
  tour/index.html                    public deep-dive tour, one section per feature
  tour/kit/index.html                noindex gallery of ad creatives and copy for the team
  content/figures/tour-<id>.svg      workflow figure for features without a listing screen
  files/ads/tour/<id>-4x5.png, -1x1.png, -9x16.png   ad creatives (1080 wide)
  files/ads/tour/ad-copy.json and ad-copy.csv        ad copy, length-checked
Screens are the AppExchange listing images in files/appx/ (sample data)."""
import os, sys, json, csv, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_insights as bi, figures as fg
from tour_data import F, GROUPS
ROOT = bi.ROOT; SITE = bi.SITE
LISTB = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&tab=e"
DEMO = "https://calendly.com/npssurvey/demo"
E = html.escape

def land(f, src, med):  # landing URL for ads: UTMs before the hash
    return f"{SITE}/tour/?utm_source={src}&utm_medium={med}&utm_campaign=tour_{f['id'].replace('-','_')}#{f['id']}"

def check_copy():
    errs = []
    for f in F:
        if len(f["mh"]) > 40: errs.append((f["id"], "meta headline", len(f["mh"])))
        if len(f["lh"]) > 70: errs.append((f["id"], "linkedin headline", len(f["lh"])))
        for h in f["gh"]:
            if len(h) > 30: errs.append((f["id"], "google headline", h, len(h)))
        for d in f["gd"]:
            if len(d) > 90: errs.append((f["id"], "google desc", d, len(d)))
        if "—" in json.dumps(f, ensure_ascii=False): errs.append((f["id"], "long dash"))
    return errs

def copy_rows():
    rows = []
    for f in F:
        primary = f"{f['hook']} {f['outcome']} NPS Survey CX OS runs 100% inside Salesforce. Try it free for 15 days."
        rows.append(dict(id=f["id"], feature=f["name"], group=GROUPS[f["group"]], hook=f["hook"],
            meta_primary_text=primary, meta_headline=f["mh"], meta_description="Free 15-day trial on AppExchange",
            meta_url=land(f, "meta", "paid_social"),
            linkedin_intro=f"{f['hook']} {f['outcome']}", linkedin_headline=f["lh"], linkedin_url=land(f, "linkedin", "paid_social"),
            google_headline_1=f["gh"][0], google_headline_2=f["gh"][1], google_headline_3=f["gh"][2],
            google_description_1=f["gd"][0], google_description_2=f["gd"][1], google_url=land(f, "google", "cpc"),
            image_4x5=f"{SITE}/files/ads/tour/{f['id']}-4x5.png", image_1x1=f"{SITE}/files/ads/tour/{f['id']}-1x1.png", image_9x16=f"{SITE}/files/ads/tour/{f['id']}-9x16.png"))
    return rows

def visual(f):
    if f["shot"]:
        return f'<img src="/files/appx/nps-cx-os-{f["shot"]}.jpg" alt="{E(f["name"])}: {E(f["title"])}" loading="lazy" width="1500" height="1000">'
    return open(os.path.join(ROOT, "content/figures", f"tour-{f['id']}.svg")).read()

CSS = """
.thero{background:#002FA7;color:#fff;padding:56px 0 48px}.thero h1{font-size:clamp(2rem,4.6vw,3.2rem);line-height:1.08;margin:10px 0 14px;font-weight:800;max-width:900px}.thero p{color:#D6E2FF;font-size:1.12rem;max-width:760px;margin:0}
.jump{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px;margin:28px 0 0}.jump a{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:14px;padding:12px 14px;color:#fff;text-decoration:none;font-weight:700;font-size:.95rem}.jump a span{display:block;font-weight:500;font-size:.8rem;color:#C9D5F2;margin-top:2px}
.grp{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:800;color:var(--link);margin:56px 0 0}
.feat{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:36px;align-items:start;padding:36px 0;border-bottom:1px solid var(--line);scroll-margin-top:20px}
.feat h2{font-size:1.75rem;line-height:1.15;margin:4px 0 10px}.feat .k{font-weight:800;color:var(--link);font-size:.9rem}
.feat h3{font-size:.8rem;letter-spacing:.07em;text-transform:uppercase;color:var(--fg-mute);margin:18px 0 6px}
.feat p,.feat li{color:var(--fg-soft)}.feat ol{padding-left:20px;margin:0}.feat li{margin:4px 0}
.feat .out{background:var(--bg-tint);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin-top:16px;color:var(--fg)}
.feat .vis img,.feat .vis svg{width:100%;height:auto;display:block;border-radius:16px;box-shadow:0 12px 34px rgba(12,24,74,.14)}
.feat .who{font-size:.88rem;color:var(--fg-mute)}
@media (max-width:860px){.feat{grid-template-columns:minmax(0,1fr)}.feat .vis{order:-1}}
.note{font-size:.85rem;color:var(--fg-mute)}
.kit{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:12px 0}.kit img{width:100%;border-radius:10px;border:1px solid var(--line)}
.kitrow{padding:28px 0;border-bottom:1px solid var(--line)}.kitrow table{font-size:.88rem}.kitrow td:first-child{width:180px;font-weight:700;color:var(--fg)}
"""

def page():
    jump = "".join(f'<a href="#{f["id"]}">{E(f["name"])}<span>{E(f["hook"])}</span></a>' for f in F)
    body = ""
    for g, gname in enumerate(GROUPS):
        fs = [f for f in F if f["group"] == g]
        if not fs: continue
        body += f'<div class="grp">{E(gname)}</div>'
        for f in fs:
            trial = f"{LISTB}&utm_source=npssurveys.com&utm_medium=website&utm_campaign=tour&utm_content={f['id']}"
            body += f"""<section class="feat" id="{f['id']}"><div><div class="k">{E(f['name'])}</div><h2>{E(f['title'])}</h2><div class="who">Best for: {E(f["who"])}</div>
<h3>The business problem</h3><p>{E(f['problem'])}</p>
<h3>How it works</h3><ol>{''.join(f'<li>{E(s)}</li>' for s in f['how'])}</ol>
<div class="out"><b>What changes:</b> {E(f['outcome'])}</div>
<a class="b p" href="{trial}" target="_blank" rel="noopener">Try it free for 15 days &rarr;</a><a class="b d" href="{DEMO}" target="_blank" rel="noopener">See it in a demo</a></div>
<div class="vis">{visual(f)}</div></section>"""
    ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "NPS Survey CX OS", "applicationCategory": "BusinessApplication", "operatingSystem": "Salesforce",
          "offers": {"@type": "Offer", "price": "3500", "priceCurrency": "USD"}, "featureList": [f["name"] for f in F], "url": f"{SITE}/tour/"}
    title = "Product tour: every feature and the problem it solves | NPS Survey CX OS"
    desc = f"A deep-dive tour of NPS Survey CX OS for Salesforce: {len(F)} features, the business problem each one solves, how it works and what changes."
    out = bi.head(title, desc, f"{SITE}/tour/", f"<style>{CSS}</style><script type=\"application/ld+json\">{json.dumps(ld)}</script>") + f"""
<section class="thero"><div class="wrap"><div class="crumb"><a href="/">Home</a> &middot; Product tour</div>
<h1>Every feature, and the business problem it solves.</h1>
<p>NPS Survey CX OS runs 100% inside Salesforce. Here is what each part does, who it is for, how it works and what changes for your team. Pick the problem you have today.</p>
<div class="jump">{jump}</div></div></section>
<main class="wrap">{body}
<p class="note" style="margin:28px 0">Product screens are from the NPS Survey CX OS listing on Salesforce AppExchange; names and numbers in them are sample data. Pricing: one price per Salesforce org per year, from $3,500, with a 15-day free trial.</p>
{bi.cta_html("trial", "tour")}</main>""" + bi.FOOT
    os.makedirs(os.path.join(ROOT, "tour"), exist_ok=True)
    open(os.path.join(ROOT, "tour", "index.html"), "w").write(out)

def kit(rows):
    items = ""
    for r in rows:
        tbl = "".join(f"<tr><td>{E(k.replace('_',' '))}</td><td>{E(v)}</td></tr>" for k, v in r.items() if k not in ("id", "image_4x5", "image_1x1", "image_9x16"))
        items += f"""<div class="kitrow" id="{r['id']}"><h2 style="margin:0 0 6px">{E(r['feature'])}</h2>
<div class="kit"><a href="/files/ads/tour/{r['id']}-4x5.png"><img src="/files/ads/tour/{r['id']}-4x5.png" alt="4:5" loading="lazy"></a><a href="/files/ads/tour/{r['id']}-1x1.png"><img src="/files/ads/tour/{r['id']}-1x1.png" alt="1:1" loading="lazy"></a><a href="/files/ads/tour/{r['id']}-9x16.png"><img src="/files/ads/tour/{r['id']}-9x16.png" alt="9:16" loading="lazy"></a></div>
<div class="tw"><table>{tbl}</table></div></div>"""
    out = bi.head("Ad kit: product tour creatives | NPS Survey CX OS", "Internal ad kit.", f"{SITE}/tour/kit/", f'<meta name="robots" content="noindex"><style>{CSS}</style>') + f"""
<section class="thero"><div class="wrap"><h1>Product tour ad kit</h1><p>{len(rows)} features &times; 3 sizes (4:5 feed, 1:1 square, 9:16 stories and reels) with ready copy for Meta, LinkedIn and Google. Download all copy as <a style="color:#fff" href="/files/ads/tour/ad-copy.csv">CSV</a> or <a style="color:#fff" href="/files/ads/tour/ad-copy.json">JSON</a>. Each ad lands on its section of the <a style="color:#fff" href="/tour/">product tour</a>.</p></div></section>
<main class="wrap">{items}</main>""" + bi.FOOT
    os.makedirs(os.path.join(ROOT, "tour", "kit"), exist_ok=True)
    open(os.path.join(ROOT, "tour", "kit", "index.html"), "w").write(out)

LOOP = open(os.path.join(ROOT, "brand/logo/nps-survey-cx-os-mark-white.svg")).read()
AD_CSS = """*{box-sizing:border-box;margin:0;padding:0}body{background:#002FA7;color:#fff;font-family:"IBM Plex Sans",Arial,sans-serif;-webkit-font-smoothing:antialiased;display:flex;flex-direction:column;overflow:hidden}
.top{display:flex;align-items:center;gap:16px}.top svg{width:60px;height:60px}.top b{display:block;font-size:32px;font-weight:800}.top small{display:block;font-size:20px;font-weight:600;color:#C9D5F2}
.kick{display:inline-block;align-self:flex-start;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.28);border-radius:999px;padding:9px 20px;font-size:24px;font-weight:700;color:#fff}
h1{font-weight:800;letter-spacing:-.02em;line-height:1.06}
.vis{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.shot{max-width:100%;max-height:100%;border-radius:22px;box-shadow:0 26px 70px rgba(0,8,50,.45);background:#fff;display:block}
.steps{background:#fff;border-radius:26px;padding:22px;width:100%;box-shadow:0 26px 70px rgba(0,8,50,.45)}
.st{display:flex;gap:20px;align-items:center;background:#F4F7FF;border:2px solid #DCE4F7;border-radius:18px;padding:16px 22px}.st+.st{margin-top:12px}
.st i{flex:none;width:56px;height:56px;border-radius:50%;background:#0C184A;color:#fff;display:grid;place-items:center;font-style:normal;font-weight:800;font-size:27px}
.st b{display:block;font-size:30px;font-weight:800;color:#0C184A}.st span{display:block;font-size:24px;font-weight:600;color:#5E6B98;margin-top:2px}
.foot{display:flex;align-items:center;justify-content:space-between;gap:20px}
.pill{background:#fff;color:#002FA7;font-weight:800;font-size:31px;padding:20px 32px;border-radius:999px;white-space:nowrap}
.out{font-size:34px;line-height:1.35;color:#D6E2FF;font-weight:500}.out b{color:#fff}
.fine{font-size:21px;color:#C9D5F2;line-height:1.35;text-align:right}"""

SIZES = {"4x5": (1080, 1350, 72, 60, 40), "1x1": (1080, 1080, 64, 52, 30), "9x16": (1080, 1920, 84, 72, 56)}

def ad_html(f, size):
    w, h, pad, fs, gap = SIZES[size]
    if f["shot"]:
        vis = f'<img class="shot" src="file://{ROOT}/files/ads/tour/crops/{f["shot"]}.png">'
    else:
        n = 4 if size != "1x1" else 3
        vis = '<div class="steps">' + "".join(f'<div class="st"><i>{i+1}</i><div><b>{E(a)}</b><span>{E(b.replace("|"," "))}</span></div></div>' for i, (a, b) in enumerate(f["fig"][:n])) + "</div>"
    outtxt = f'<p class="out"><b>What changes:</b> {E(f["outcome"])}</p>' if size == "9x16" else ""
    top_safe = 120 if size == "9x16" else 0; bot_safe = 200 if size == "9x16" else 0
    return f"""<html><head><style>{AD_CSS} body{{width:{w}px;height:{h}px;padding:{pad+top_safe}px {pad}px {pad+bot_safe}px;gap:{gap}px}} h1{{font-size:{fs}px}}</style></head><body>
<div class="top">{LOOP}<div><b>NPS Survey</b><small>CX OS by SalesHub</small></div></div>
<div class="kick">{E(f['name'])}</div><h1>{E(f['hook'])}</h1>
<div class="vis">{vis}</div>{outtxt}
<div class="foot"><div class="pill">Try it free for 15 days</div><div class="fine">Native to Salesforce<br>npssurveys.com/tour</div></div></body></html>"""

def render_ads(only=None):
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/ads/tour")
    with sync_playwright() as p:
        b = p.chromium.launch()
        for size, (w, h, *_ ) in SIZES.items():
            pg = b.new_page(viewport={"width": w, "height": h})
            for f in F:
                if only and f["id"] not in only: continue
                tmp = os.path.join(out, "_tmp.html"); open(tmp, "w").write(ad_html(f, size))
                pg.goto("file://" + tmp); pg.wait_for_timeout(150)
                pg.screenshot(path=os.path.join(out, f"{f['id']}-{size}.png"))
            pg.close()
        b.close()
    os.remove(os.path.join(out, "_tmp.html"))

def main():
    errs = check_copy()
    if errs: print("COPY ERRORS:", *errs, sep="\n  "); sys.exit(1)
    for f in F:
        if not f["shot"]:
            svg = fg.flow(f["title"], f["name"] + " in NPS Survey CX OS", [(a, b, "") for a, b in f["fig"]], f"{f['name']}: " + "; ".join(f["how"]))
            open(os.path.join(ROOT, "content/figures", f"tour-{f['id']}.svg"), "w").write(svg)
    rows = copy_rows(); out = os.path.join(ROOT, "files/ads/tour"); os.makedirs(out, exist_ok=True)
    json.dump(rows, open(os.path.join(out, "ad-copy.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out, "ad-copy.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    page(); kit(rows)
    if "--ads" in sys.argv: render_ads([a for a in sys.argv[2:] if not a.startswith("--")] or None)
    print("tour built:", len(F), "features")

if __name__ == "__main__":
    main()
