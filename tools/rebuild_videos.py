"""Rebuild the two YouTube Shorts and the brand film in the Loop identity from current brand stills.
Writes <name>-v2.mp4 next to each hosted video (originals kept); same length and soundtrack as the original."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read()
TMP = "/tmp/vidbuild"; os.makedirs(TMP, exist_ok=True)
ORIG = os.path.join(ROOT, "files/_originals")
CSS = plexfont.css() + """*{margin:0;padding:0;box-sizing:border-box}body{background:#002FA7;color:#fff;font-family:"IBM Plex Sans";overflow:hidden}
h1{font-family:"IBM Plex Serif";font-weight:600;letter-spacing:-.01em;line-height:1.06}h1 em{font-style:normal;color:inherit}
.k{font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#C9D5F2}.sub{color:#D6E2FF;line-height:1.4}
.lk svg{width:auto;display:block}"""

def hook_916(kick, head, sub):
    return f"""<body style="width:1080px;height:1920px;padding:300px 90px 360px;display:flex;flex-direction:column">
<div class="lk">{LOCK.replace('<svg','<svg style="height:110px"',1)}</div><div style="margin-top:auto">
<div class="k" style="font-size:30px">{kick}</div><h1 style="font-size:112px;margin-top:22px">{head}</h1><p class="sub" style="font-size:42px;margin-top:30px">{sub}</p></div></body>"""

def hook_169(kick, head):
    return f"""<body style="width:1920px;height:1080px;padding:110px 140px;display:flex;flex-direction:column">
<div class="lk">{LOCK.replace('<svg','<svg style="height:96px"',1)}</div><div style="margin-top:auto">
<div class="k" style="font-size:26px">{kick}</div><h1 style="font-size:104px;margin-top:20px;max-width:1500px">{head}</h1></div><div style="height:60px"></div></body>"""

def screen_169(path):
    return f"""<body style="width:1920px;height:1080px;display:flex;align-items:center;justify-content:center">
<img src="data:image/png;base64,{__import__("base64").b64encode(open(path,"rb").read()).decode()}" style="height:1000px;width:1500px;border-radius:18px;box-shadow:0 30px 80px rgba(0,8,50,.5)"></body>"""

def pricing_169():
    pl = [("CX Lite", "$3,500", "NPS and CSAT, close the loop on every low score"), ("CX Pro", "$8,500", "CES, branching, review requests, AI summaries"),
          ("CX OS Insights", "$16,000", "Revenue CX, CX panels, AI digital workers")]
    cards = "".join(f'<div style="flex:1;background:{"#fff" if i == 2 else "rgba(255,255,255,.1)"};color:{"#0F1A3D" if i == 2 else "#fff"};border-radius:24px;padding:40px 36px">'
                     f'<div style="font-size:30px;font-weight:600">{n}</div><div style="font-family:IBM Plex Serif;font-weight:600;font-size:76px;margin:10px 0">{"<span style=font-size:30px;font-family:IBM\\ Plex\\ Sans>from </span>" if i == 2 else ""}{p}<span style="font-size:28px;font-family:IBM Plex Sans;font-weight:500"> /year</span></div>'
                     f'<div style="font-size:26px;opacity:.8;line-height:1.35">{d}</div></div>' for i, (n, p, d) in enumerate(pl))
    return f"""<body style="width:1920px;height:1080px;padding:120px 140px;display:flex;flex-direction:column">
<div class="k" style="font-size:26px">Pricing</div><h1 style="font-size:88px;margin-top:16px">One price per company. Not per user.</h1>
<div style="display:flex;gap:28px;margin-top:auto">{cards}</div>
<p class="sub" style="font-size:28px;margin-top:34px">Every plan starts with a 15-day free trial on Salesforce AppExchange.</p></body>"""

def render(jobs):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, (w, h, html) in jobs.items():
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.set_content(f"<html><head><style>{CSS}</style></head>{html}</html>"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
            pg.screenshot(path=f"{TMP}/{name}.png"); pg.close()
        b.close()

def build(stills, out, audio_src, xf=0.5):
    """stills: list of (png, seconds). Cross-fades between stills; total length = sum(seconds)."""
    ins, fc = [], []
    for i, (png, d) in enumerate(stills):
        ins += ["-framerate", "30", "-loop", "1", "-t", f"{d + xf}", "-i", png]
        fc.append(f"[{i}:v]format=yuv420p,fps=30,setpts=PTS-STARTPTS[v{i}]")
    prev, t = "v0", stills[0][1]
    for i in range(1, len(stills)):
        fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={xf}:offset={t:.3f}[x{i}]"); prev = f"x{i}"; t += stills[i][1]
    total = sum(d for _, d in stills)
    n = len(stills)
    tmp = out[:-4] + ".part.mp4"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *ins, "-i", audio_src, "-filter_complex", ";".join(fc),
                           "-map", f"[{prev}]", "-map", f"{n}:a", "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.3f}", "-movflags", "+faststart", tmp])
    os.replace(tmp, out); print(out, round(total, 2))

if __name__ == "__main__":
    T = os.path.join(ROOT, "files/ads/tour"); E = os.path.join(ROOT, "files/video/endcards"); A = os.path.join(ROOT, "brand/appexchange")
    scr = ["01-dash", "02-inbox", "03-act", "04-account", "05-csat", "07-case", "09-resp", "11-contact", "12-desk", "13-auto"]
    jobs = {
        "hook-3of10": (1080, 1920, hook_916("60 seconds with NPS Survey CX OS", "A customer just scored you <em>3</em>/10.", "What happens next decides if they stay.")),
        "hook-gov": (1080, 1920, hook_916("For government and defense teams on Salesforce", "Mission feedback can't wait a <em>whole</em> year.", "Annual surveys arrive after the problem has grown.")),
        "hook-film": (1920, 1080, hook_169("NPS Survey CX OS", "Most unhappy customers don't complain. They just <em>leave</em>.")),
        "pricing": (1920, 1080, pricing_169()),
    }
    for s in scr: jobs["scr-" + s] = (1920, 1080, screen_169(f"{A}/nps-survey-cx-os-{s}.png"))
    render(jobs)
    P = lambda n: f"{TMP}/{n}.png"
    build([(P("hook-3of10"), 4), (f"{T}/close-the-loop-9x16.png", 5.5), (f"{T}/ai-feedback-inbox-9x16.png", 5.5), (f"{T}/loop-board-9x16.png", 5.5),
           (f"{T}/executive-dashboard-9x16.png", 5.5), (f"{E}/NPS-CXOS-Short-3outof10.png", 7.3)],
          os.path.join(ROOT, "files/NPS-CXOS-Short-3outof10-v2.mp4"), f"{ORIG}/NPS-CXOS-Short-3outof10-pre-loop.mp4")
    build([(P("hook-gov"), 4), (f"{T}/executive-dashboard-9x16.png", 5.5), (f"{T}/close-the-loop-9x16.png", 5.5), (f"{T}/service-desk-9x16.png", 5.5),
           (f"{T}/translations-9x16.png", 5.5), (f"{E}/NPS-CXOS-Short-Government-Defense.png", 9.2)],
          os.path.join(ROOT, "files/NPS-CXOS-Short-Government-Defense-v2.mp4"), f"{ORIG}/NPS-CXOS-Short-Government-Defense-pre-loop.mp4")
    build([(P("hook-film"), 5)] + [(P("scr-" + s), 5.5) for s in scr] + [(P("pricing"), 5), (f"{E}/NPS-CXOS-Film-1080p.png", 9.5)],
          os.path.join(ROOT, "files/NPS-CXOS-Film-1080p-v2.mp4"), f"{ORIG}/NPS-CXOS-Film-1080p-pre-loop.mp4")
