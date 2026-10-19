"""Render 1080x1350 branded social images from a JSON spec.
Usage: python3 tools/social_images.py spec.json
spec.json = {"outdir": "social/2026-11", "images": {"file-name": "<HTML body snippet>"}}
Body snippet building blocks (see social/2026-10 for examples):
  <div class="kick">Label</div> <h1>Headline <em>yellow part</em></h1> <p class="lead">Text</p>
  <ol><li><div>Step<span>detail</span></div></li></ol> <div class="big">1</div>
  <div class="foot"><div class="url">npssurveys.com/xyz</div><div class="fine">fine print</div></div>
  {FLAG} inserts the U.S. flag.
"""
import json, sys, os
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK=open(os.path.join(ROOT,"brand/logo/nps-survey-cx-os-mark-white.svg")).read()
FLAG=open(os.path.join(ROOT,"brand/flag/us-flag.svg")).read().replace("<svg ",'<svg style="width:285px;height:auto;border-radius:6px;box-shadow:0 10px 30px rgba(0,0,0,.35)" ',1)
base="""<html><head><link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&display=swap"><style>
*{box-sizing:border-box}body{margin:0;width:1080px;height:1350px;font-family:Inter,Arial,sans-serif;color:#fff;
background:radial-gradient(120% 90% at 15% 0%,#2B64F2 0%,#1E54E8 40%,#052CA0 100%);padding:84px 80px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:18px;font-weight:800;font-size:34px}.top svg{width:78px;height:auto}.top small{display:block;font-size:22px;font-weight:600;opacity:.85}
.kick{margin-top:70px;display:inline-block;background:#FFE443;color:#0C184A;font-weight:800;font-size:26px;letter-spacing:.06em;text-transform:uppercase;padding:12px 22px;border-radius:999px;align-self:flex-start}
h1{font-size:84px;line-height:1.04;font-weight:800;margin:34px 0 0;letter-spacing:-.01em}h1 em{font-style:normal;color:#FFE443}
p.lead{font-size:34px;line-height:1.35;color:#D6E2FF;margin:30px 0 0}
ol{margin:40px 0 0;padding:0;list-style:none;counter-reset:n}ol li{counter-increment:n;font-size:34px;line-height:1.3;font-weight:700;margin:0 0 22px;display:flex;gap:20px;align-items:flex-start}
ol li:before{content:counter(n);flex:none;width:52px;height:52px;border-radius:50%;background:#FFE443;color:#0C184A;display:grid;place-items:center;font-weight:800;font-size:28px}
ol li span{font-weight:500;color:#D6E2FF;display:block;font-size:27px}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;gap:20px}
.url{background:#fff;color:#0C184A;font-weight:800;font-size:32px;padding:20px 30px;border-radius:999px}
.fine{font-size:19px;color:#B9C8F5;max-width:470px;line-height:1.35}
.big{font-size:150px;font-weight:800;line-height:1;color:#FFE443}
</style></head><body><div class="top">"""+MARK+"""<div>NPS Survey CX OS<small>by SalesHub</small></div></div>{BODY}</body></html>"""

spec=json.load(open(sys.argv[1])); out=os.path.join(ROOT,spec["outdir"]); os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1350})
    for k,body in spec["images"].items():
        pg.set_content(base.replace("{BODY}",body.replace("{FLAG}",'<div style="margin-top:56px">'+FLAG+'</div>'))); pg.wait_for_timeout(600)
        pg.screenshot(path=os.path.join(out,k+".png")); print(os.path.join(spec["outdir"],k+".png"))
    b.close()
