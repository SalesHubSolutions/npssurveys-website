"""LinkedIn newsletter / article covers, 1920x1080, Loop brand (one hero, no yellow words).
RULE (Nov 27, 2026): covers stay clean (headline, one hero, logo + npssurveys.com). No QR on covers:
readers are on the screen they would scan with. The QR lives on the END CARD (files/newsletter/covers/endcard.png),
which is the last image of every issue, linked to the AppExchange trial."""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont, brandprint
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def uri(p):
    ext = p.rsplit(".", 1)[1]; mime = {"jpg": "jpeg", "webp": "webp", "png": "png"}[ext]
    return f"data:image/{mime};base64," + base64.b64encode(open(os.path.join(ROOT, p), "rb").read()).decode()
LOCK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read().replace("<svg", "<svg style='height:64px;width:auto;display:block'", 1)
MARKW = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-mark-white.svg")).read().replace("<svg", "<svg style='width:100%;height:100%;display:block'", 1)
CSS = plexfont.css() + """*{margin:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:"IBM Plex Sans";color:#fff;background:#002FA7}
.c{position:relative;width:1920px;height:1080px;overflow:hidden;background:linear-gradient(135deg,#002FA7 0%,#001A66 100%)}
.glow{position:absolute;border-radius:50%;filter:blur(110px)}
.hero{position:absolute;opacity:.10}
.t{position:absolute;left:120px;top:150px;width:900px}
.k{font-size:26px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#9DB4F5}
h1{font-family:"IBM Plex Serif";font-weight:600;font-size:92px;line-height:1.05;margin-top:26px;letter-spacing:-.01em}
.s{font-size:34px;line-height:1.4;color:#D6E2FF;margin-top:30px;max-width:820px}
.lk{position:absolute;left:120px;bottom:96px;display:flex;align-items:center;gap:28px}.site{font-size:26px;font-weight:600;color:#D6E2FF;padding-left:28px;border-left:2px solid rgba(255,255,255,.3);line-height:1.6}
.url{position:absolute;right:330px;bottom:112px;background:#fff;color:#002FA7;font-weight:600;font-size:26px;border-radius:99px;padding:14px 30px;box-shadow:0 10px 30px rgba(0,10,60,.35)}
.qr{position:absolute;right:110px;bottom:70px;width:190px;background:#fff;border-radius:22px;padding:16px 16px 10px;text-align:center;color:#0F1A3D;box-shadow:0 20px 50px rgba(0,10,60,.45)}.qr b{display:block;font-size:17px;font-weight:600;margin-top:6px}
.shot{position:absolute;right:-60px;top:170px;width:900px;border-radius:22px;box-shadow:0 50px 120px rgba(0,10,60,.55);border:2px solid rgba(255,255,255,.3)}
.ph{position:absolute;right:0;top:0;bottom:0;width:820px;background-size:cover;background-position:center}
.phf{position:absolute;right:0;top:0;bottom:0;width:820px;background:linear-gradient(90deg,#001A66 0%,rgba(0,26,102,.35) 45%,rgba(0,47,167,.15) 100%)}"""
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&utm_source=linkedin&utm_medium=newsletter&utm_campaign=ctl_qr"
def cover(kicker, title, sub, shot=None, photo=None):
    right = (f'<div class="glow" style="width:900px;height:700px;right:-100px;top:200px;background:#4A78FF;opacity:.7"></div><img class="shot" src="{uri(shot)}">' if shot
             else f'<div class="ph" style="background-image:url({uri(photo)})"></div><div class="phf"></div>')
    return f"""<html><head><style>{CSS}</style></head><body><div class="c">
<div class="hero" style="width:1100px;height:1100px;left:-420px;bottom:-560px">{MARKW}</div>{right}
<div class="t"><div class="k">{kicker}</div><h1>{title}</h1><p class="s">{sub}</p></div>
<div class="lk">{LOCK}<span class="site">npssurveys.com</span></div></div></body></html>"""
def endcard(issue):
    btn = "display:inline-block;border-radius:99px;font-weight:600;font-size:30px;padding:22px 42px;margin-right:18px"
    return f"""<html><head><style>{CSS}</style></head><body><div class="c">
<div class="glow" style="width:900px;height:900px;right:-150px;top:-200px;background:#4A78FF;opacity:.55"></div>
<div class="hero" style="width:1100px;height:1100px;left:-420px;bottom:-560px">{MARKW}</div>
<div class="t" style="top:200px;width:1050px"><div class="k">Close the Loop, {issue}</div><h1 style="font-size:84px">Close the loop on every customer, inside Salesforce.</h1>
<p class="s">Rated 5.0 on Salesforce AppExchange. Security reviewed, 100% native, and it works with Slack, Teams and Google reviews.</p>
<div style="margin-top:46px"><span style="{btn};background:#FFD60A;color:#0F1A3D">Start your 15-day free trial</span><span style="{btn};background:#fff;color:#002FA7">npssurveys.com</span></div></div>
<div style="position:absolute;right:150px;top:270px;width:440px;background:#fff;border-radius:30px;padding:34px 34px 24px;text-align:center;color:#0F1A3D;box-shadow:0 40px 90px rgba(0,10,60,.5)">{brandprint.qr(LIST, 372)}
<div style="font-size:28px;font-weight:600;margin-top:14px">Scan to try it free</div><div style="font-size:22px;color:#5A6787;margin-top:4px">Salesforce AppExchange</div></div>
<div class="lk">{LOCK}</div></div></body></html>"""

JOBS = [
 ("endcard", endcard("by SalesHub")),
 ("issue-01-cfo", cover("Close the Loop, issue 01", "The CFO business case for closing the loop", "The revenue model, the platform choice and a one-page case you can copy.", shot="assets/product/inbox-focus.webp")),
 ("archive-hybrid-cloud", cover("Close the Loop, from the archive", "Embracing a hybrid cloud approach", "Keep customer data where your team already works, and still use the best of the cloud.", photo="brand/photos/team-meeting.jpg")),
 ("archive-building-on-salesforce", cover("Close the Loop, from the archive", "The ROI of building an app on Salesforce", "What it costs, what it returns, and why native apps keep data in the org.", shot="assets/product/dash-focus.webp")),
]
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/newsletter/covers"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        for name, html in JOBS:
            pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(out, name + ".png"))
        b.close()
    print("ok")
