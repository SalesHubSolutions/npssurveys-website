"""Proof strip: the name-recognition trust bar (AppExchange, 5.0, security reviewed, Slack/Teams/Google reviews).
Renders brand/proof/proof-strip-600.png (email, 1200x? @2x) and proof-strip-1600.png (docs/social).
HTML snippet PROOF_HTML(dark) is reused in PDFs."""
import os, re, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = open(os.path.join(ROOT, "index.html")).read(); _i = _s.find("Slack</span>")
SEC = _s[_s.rfind("<section", 0, _i):_s.find("</section>", _i)]
PINTS = re.search(r'<span class="pints">.*?</span></span>', SEC, re.S).group(0)
SF = "data:image/svg+xml;base64," + base64.b64encode(open(os.path.join(ROOT, "brand/partners/salesforce.svg"), "rb").read()).decode()
CHECK = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#002FA7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'

CSS = """.pf{background:#fff;color:#071338;font-family:"IBM Plex Sans";border:1px solid #E4EAF6;border-radius:14px;padding:12px 16px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 12px;box-shadow:0 1px 2px rgba(7,19,56,.04)}
.pf .c{display:flex;align-items:center;gap:8px;font-weight:600;font-size:13px;line-height:1.25;color:#071338}
.pf .c small{display:block;font-weight:400;font-size:11.5px;color:#687385}
.pf b{font-family:"IBM Plex Serif";font-size:17px;color:#002FA7}
.pf .sf{width:34px;height:24px;background:url(%s) center/contain no-repeat}
.pf .ic{width:24px;height:24px;border-radius:50%%;background:#EAF0FF;display:grid;place-items:center}
.pf .dv{width:1px;height:28px;background:#E4EAF6}
.pf .st5{color:#002FA7;letter-spacing:0;font-size:12px;line-height:1}
.pf .pints{display:inline-flex;gap:8px;align-items:center}.pf .pint{display:inline-flex;font-size:0;line-height:0}.pf .pint svg{flex:none}""" % SF

def html():
    return f"""<div class="pf">
<div class="c"><span class="sf"></span><span><small>Available on</small>Salesforce AppExchange</span></div><span class="dv"></span>
<div class="c"><b>5.0</b><span class="st5">&#9733;&#9733;&#9733;&#9733;&#9733;</span></div><span class="dv"></span>
<div class="c"><span class="ic">{CHECK}</span><span><small>Security reviewed</small>100% native</span></div><span class="dv"></span>
<div class="c">{PINTS}</div></div>"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(ROOT, "brand/proof"), exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, name in [(600, "proof-strip-600.png"), (820, "proof-strip-820.png")]:
            pg = b.new_page(viewport={"width": w, "height": 300}, device_scale_factor=2)
            pg.set_content(f"<html><head><style>{plexfont.css()}*{{margin:0;box-sizing:border-box}}body{{background:transparent}}{CSS}</style></head><body>{html()}</body></html>")
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.locator(".pf").screenshot(path=os.path.join(ROOT, "brand/proof", name), omit_background=True)
        b.close()
    print("ok")
