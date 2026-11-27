"""Loop thumbnails (1280x720) for the live YouTube videos. Output: brand/youtube-thumbs/<videoId>.png"""
import os, sys, base64, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKUP = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read()
OUT = os.path.join(ROOT, "brand/youtube-thumbs")

# videoId: (headline with *one* yellow word, product shot or None for the dial)
T = {
    "uJHsCxF9Lb4": ("Every answer gets a *next step*", "01"),
    "wuMemtRED-A": ("Feedback on every *deal*", "09"),
    "uXIZmwdQTdQ": ("The CX OS in *75 seconds*", "05"),
    "lvgZfDSlG8Q": ("15+ question *types*", "06"),
    "RAXfmjeizKI": ("CX on every *account*", "04"),
    "Z718BdT7D3c": ("Surveys in your *brand*", "11"),
    "lSEr8I3yXQA": ("Account NPS for *manufacturers*", "05"),
    "EMHn3IOTTAM": ("Build a survey in *minutes*", "06"),
    "MQCpICocmBw": ("Win and loss, on every *deal*", "07"),
    "WOn2-yRUeqc": ("Surveys that *act*", "10"),
    "HJ6EvUrWmsM": ("From churn to *champions*", "03"),
    "aUua4Zancp0": ("Every unhappy customer gets a *call back*", "01"),
    "IYMiJXBxkQU": ("The full *demo*", "02"),
    "geDjsobcr28": ("Keep the customers you *heard*", "02"),
    "kJc8utk2-mU": ("Customer experience, inside *Salesforce*", "05"),
    "-rHzsvTPjb8": ("NPS feedback on *autopilot*", "08"),
    "Pa5i-A2WnNQ": ("NPS Survey *2.0*", None),
    "jEoJilXL3hU": ("Feedback on *escalated* cases", None),
    "HNSLDQcUDMg": ("Surveys for *high-priority* cases", None),
    "NbCuBef0KyM": ("Feedback after *onboarding*", None),
    "7Ek4YjYOyb8": ("Account *check&#8209;ins* on autopilot", None),
    "vYVtYpKusUY": ("NPS for every new *contact*", None),
    "52xdud2KbxU": ("Feedback after the *demo*", None),
    "yIAZY9b5d-k": ("CSAT after every *renewal*", None),
    "SNr9v-UOm6o": ("Learn why you *won*", None),
    "bM5E9EziLjE": ("Feedback at every *milestone*", None),
    "pDW6vcCorrs": ("Learn why you *lost*", None),
    "rSI6wHSHkhU": ("NPS, inside *Salesforce*", None),
}

def dial():
    """NPS dial in the brand dial palette: detractors coral, passives grey, promoters teal."""
    import math
    cx, cy, r, w = 260, 250, 200, 56
    def arc(a0, a1, col):
        p = lambda a: (cx + r * math.cos(math.radians(180 - a)), cy - r * math.sin(math.radians(180 - a)))
        (x0, y0), (x1, y1) = p(a0), p(a1)
        return f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="{w}" fill="none"/>'
    segs = arc(0, 180 * 6.5 / 10 - 1, "#EB6665") + arc(180 * 6.5 / 10 + 1, 180 * 8.5 / 10 - 1, "#E7E7E7") + arc(180 * 8.5 / 10 + 1, 180, "#267A72")
    a = math.radians(180 - 150)
    nx, ny = cx + (r - 40) * math.cos(a), cy - (r - 40) * math.sin(a)
    needle = f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#687385" stroke-width="14" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="20" fill="#687385"/>'
    return f'<svg viewBox="0 0 520 290" style="width:100%">{segs}{needle}</svg>'

CSS = plexfont.css() + """*{box-sizing:border-box;margin:0;padding:0}
body{width:1280px;height:720px;background:#002FA7;color:#fff;font-family:"IBM Plex Sans",Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden;position:relative}
.l{position:absolute;left:72px;top:64px;bottom:64px;width:560px;display:flex;flex-direction:column;justify-content:space-between}
.l svg{height:96px;width:auto;margin-left:-8px}
h1{font-family:"IBM Plex Serif",Georgia,serif;font-weight:600;letter-spacing:-.01em;line-height:1.04;font-size:86px}
h1 em{font-style:normal;color:#FFD60A}
.shot{position:absolute;left:680px;top:110px;height:500px;border-radius:22px;box-shadow:0 30px 80px rgba(0,8,50,.5);background:#fff}
.dial{position:absolute;left:690px;top:200px;width:520px;background:#fff;border-radius:28px;padding:44px 40px 30px;box-shadow:0 30px 80px rgba(0,8,50,.5)}"""

def html(head, shot):
    h = re.sub(r"\*(.+?)\*", r"<em>\1</em>", head)
    fs = 86 if len(head) <= 30 else 72
    if shot:
        b = base64.b64encode(open(os.path.join(ROOT, f"files/ads/tour/crops/{shot}.png"), "rb").read()).decode()
        right = f'<img class="shot" src="data:image/png;base64,{b}">'
    else:
        right = f'<div class="dial">{dial()}</div>'
    return f'<html><head><style>{CSS}</style></head><body><div class="l"><div>{LOCKUP}</div><h1 style="font-size:{fs}px">{h}</h1></div>{right}</body></html>'

def main(ids=None):
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 720})
        for vid, (head, shot) in T.items():
            if ids and vid not in ids: continue
            pg.set_content(html(head, shot)); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            pg.screenshot(path=os.path.join(OUT, vid + ".png"))
        b.close()

if __name__ == "__main__":
    main(sys.argv[1:] or None)
