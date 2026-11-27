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
CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'

CSS = """.pf{background:#0A1238;color:#fff;font-family:"IBM Plex Sans";border-radius:18px;padding:22px 26px;display:grid;gap:16px}
.pf .r{display:flex;flex-wrap:wrap;align-items:center;gap:14px 26px}
.pf .c{display:flex;align-items:center;gap:10px;font-weight:600;font-size:15px;line-height:1.2}
.pf .c small{display:block;font-weight:400;font-size:13px;color:#9DB4F5}
.pf b{font-family:"IBM Plex Serif";font-size:22px}
.pf .sf{width:44px;height:31px;background:url(%s) center/contain no-repeat}
.pf .ic{width:30px;height:30px;border-radius:8px;background:#002FA7;display:grid;place-items:center}
.st5{display:inline-flex;align-items:center;background:#002FA7;color:#fff;letter-spacing:1px;font-size:12px;line-height:1;padding:5px 9px;border-radius:999px;box-shadow:0 0 0 1px rgba(255,255,255,.25)}
.pints{display:inline-flex;gap:6px}.pint{display:inline-flex;align-items:center;gap:6px;background:#fff;color:#0F1A3D;border-radius:999px;padding:4px 10px 4px 6px;font-size:12.5px;font-weight:600;line-height:1}.pint svg{flex:none}""" % SF

def html():
    return f"""<div class="pf"><div class="r">
<div class="c"><span class="sf"></span><span><small>Available on</small>Salesforce AppExchange</span></div>
<div class="c"><b>5.0</b> on AppExchange <span class="st5">&#9733;&#9733;&#9733;&#9733;&#9733;</span></div>
<div class="c"><span class="ic">{CHECK}</span><span><small>Security reviewed</small>100% native to Salesforce</span></div></div>
<div class="r"><div class="c"><b>131</b> survey templates</div><div class="c"><b>67</b> question types</div><div class="c">Works with {PINTS}</div></div></div>"""

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
