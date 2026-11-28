"""LinkedIn newsletter / article covers, 1920x1080, Loop brand (one hero, no yellow words)."""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont
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
.lk{position:absolute;left:120px;bottom:96px}
.url{position:absolute;right:120px;bottom:104px;background:#fff;color:#002FA7;font-weight:600;font-size:26px;border-radius:99px;padding:14px 30px}
.shot{position:absolute;right:-60px;top:170px;width:900px;border-radius:22px;box-shadow:0 50px 120px rgba(0,10,60,.55);border:2px solid rgba(255,255,255,.3)}
.ph{position:absolute;right:0;top:0;bottom:0;width:820px;background-size:cover;background-position:center}
.phf{position:absolute;right:0;top:0;bottom:0;width:820px;background:linear-gradient(90deg,#001A66 0%,rgba(0,26,102,.35) 45%,rgba(0,47,167,.15) 100%)}"""
def cover(kicker, title, sub, shot=None, photo=None):
    right = (f'<div class="glow" style="width:900px;height:700px;right:-100px;top:200px;background:#4A78FF;opacity:.7"></div><img class="shot" src="{uri(shot)}">' if shot
             else f'<div class="ph" style="background-image:url({uri(photo)})"></div><div class="phf"></div>')
    return f"""<html><head><style>{CSS}</style></head><body><div class="c">
<div class="hero" style="width:1100px;height:1100px;left:-420px;bottom:-560px">{MARKW}</div>{right}
<div class="t"><div class="k">{kicker}</div><h1>{title}</h1><p class="s">{sub}</p></div>
<div class="lk">{LOCK}</div><div class="url">npssurveys.com</div></div></body></html>"""
JOBS = [
 ("issue-01-cfo", cover("Close the Loop, issue 01", "The CFO business case for closing the loop", "The revenue model, the platform choice and a one-page case you can copy.", shot="assets/product/inbox-focus.webp")),
 ("archive-hybrid-cloud", cover("Close the Loop, from the archive", "Embracing a hybrid cloud approach", "Keep customer data where your team already works, and still use the best of the cloud.", photo="brand/photos/team-meeting.jpg")),
 ("archive-building-on-salesforce", cover("Close the Loop, from the archive", "Building an app on Salesforce", "What it takes to build native: security review, AppExchange and keeping data in the org.", shot="assets/product/dash-focus.webp")),
]
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/newsletter/covers"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for name, html in JOBS:
            pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(out, name + ".png"))
        b.close()
    print("ok")
