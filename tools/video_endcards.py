"""Loop end cards for the hosted videos (Plex type, logo-kit lockup, 15-day trial).

Renders one PNG per card into files/video/endcards/, then splices each card onto
its video as <name>-loop.mp4 next to the original. Originals are never touched.
"""
import os, sys, base64, subprocess, io
import segno
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = lambda n: open(os.path.join(ROOT, "brand/logo-kit/svg", n)).read()
LOCKUP, STACK, MARK_K = SVG("nps-survey-logo-white.svg"), SVG("nps-survey-logo-stacked-white.svg"), SVG("nps-survey-mark-klein.svg")
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&tab=e"
TM = ("Net Promoter&reg;, NPS&reg; and the NPS-related emoticons are registered trademarks of Bain &amp; Company, Inc., "
      "NICE Systems, Inc., and Fred Reichheld. Salesforce and AppExchange are trademarks of Salesforce, Inc.")

def qr(url, px):
    """Klein Blue QR with the Loop in the centre (high error correction)."""
    q = segno.make(url, error="h")
    b = io.BytesIO(); q.save(b, kind="svg", scale=10, border=0, dark="#002FA7", xmldecl=False, svgns=True)
    src = "data:image/svg+xml;base64," + base64.b64encode(b.getvalue()).decode()
    m = int(px * .24)
    return (f'<div class="qrw" style="width:{px}px;height:{px}px"><img src="{src}" style="width:100%;height:100%;image-rendering:pixelated">'
            f'<div class="qm" style="width:{m}px;height:{m}px">{MARK_K}</div></div>')

CSS = plexfont.css() + """*{box-sizing:border-box;margin:0;padding:0}
body{background:#002FA7;color:#fff;font-family:"IBM Plex Sans",Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}
h1{font-family:"IBM Plex Serif",Georgia,serif;font-weight:600;letter-spacing:-.01em;line-height:1.08}
.cta{display:inline-block;background:#FFD60A;color:#0F1A3D;font-weight:600;border-radius:999px;white-space:nowrap}
.pill{display:inline-block;background:#fff;color:#002FA7;font-weight:600;border-radius:999px}
.card{background:#fff;color:#0F1A3D;border-radius:28px;text-align:center;box-shadow:0 26px 70px rgba(0,8,50,.4)}
.card p{font-weight:600}.card span{display:block;color:#5A6787;font-weight:500}
.qrw{position:relative;margin:0 auto}.qm{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#fff;border-radius:18%;padding:5%;display:grid;place-items:center}
.qm svg{width:100%;height:100%}
.sub{color:#D6E2FF;font-weight:500}.fine{color:#AFC0EA;line-height:1.4}
svg{display:block}"""

def film(w=1920, h=1080, utm="&utm_source=film&utm_medium=video&utm_campaign=cxos_film"):
    return f"""<body style="width:{w}px;height:{h}px;padding:110px 130px;display:flex;align-items:center;justify-content:space-between;gap:90px">
<div style="flex:1;display:flex;flex-direction:column;gap:46px">
<div style="height:120px">{LOCKUP.replace('<svg', '<svg style="height:120px;width:auto"', 1)}</div>
<h1 style="font-size:84px">Start your 15-day free trial on Salesforce AppExchange.</h1>
<div><span class="cta" style="font-size:36px;padding:22px 40px">Try it free at npssurveys.com</span></div></div>
<div class="card" style="padding:34px 34px 26px">{qr(LIST+utm, 380)}<p style="font-size:26px;margin-top:20px">Scan for the free trial</p></div>
<p class="fine" style="position:absolute;left:130px;right:130px;bottom:40px;font-size:15px">{TM}</p></body>"""

def short(line, utm, gov=False, w=1080, h=1920):
    foot = '<p class="fine" style="font-size:28px;text-align:center">Government buyers: available through Carahsoft</p>' if gov else '<p class="fine" style="font-size:28px;text-align:center">Link in the description</p>'
    return f"""<body style="width:{w}px;height:{h}px;padding:250px 110px 300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:56px;text-align:center">
<div style="width:520px">{STACK.replace('<svg', '<svg style="width:100%;height:auto"', 1)}</div>
<p class="sub" style="font-size:40px;margin-top:-20px">{line}</p>
<span class="cta" style="font-size:44px;padding:26px 50px">Start your 15-day free trial</span>
<div class="card" style="padding:36px 36px 28px">{qr(LIST+utm, 430)}<p style="font-size:32px;margin-top:22px">Scan to try it free</p><span style="font-size:24px;margin-top:4px">Salesforce AppExchange</span></div>
{foot}</body>"""

def meta(w=1080, h=1920):
    return f"""<body style="width:{w}px;height:{h}px;padding:260px 70px 320px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:54px;text-align:center">
<div style="height:150px">{LOCKUP.replace('<svg', '<svg style="height:150px;width:auto"', 1)}</div>
<p class="sub" style="font-size:42px;margin-top:40px">Year-end launch offer</p>
<h1 style="font-size:88px;margin-top:-24px;white-space:nowrap">20% off your first year</h1>
<p class="sub" style="font-size:40px;margin-top:-14px">Free setup, free switch, 15-day trial</p>
<span class="cta" style="font-size:48px;padding:30px 60px;margin-top:60px">Start your free trial</span>
<p style="font-size:40px;font-weight:600">npssurveys.com/start</p>
<p class="fine" style="font-size:24px;margin-top:30px">Installs from Salesforce AppExchange. Offer ends Dec 31, 2026.</p></body>"""

def insights(w, h):
    s = w / 1080
    return f"""<body style="width:{w}px;height:{h}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{40*s}px;text-align:center">
<div style="width:{440*s}px">{STACK.replace('<svg', '<svg style="width:100%;height:auto"', 1)}</div>
<span class="pill" style="font-size:{40*s}px;padding:{20*s}px {44*s}px">npssurveys.com/insights</span>
<p class="sub" style="font-size:{26*s}px">15-day free trial on Salesforce AppExchange</p></body>"""

# name: (source, cut_seconds, html)
JOBS = {
    "NPS-CXOS-Film-1080p": ("files/NPS-CXOS-Film-1080p.mp4", 64.75, film()),
    "NPS-CXOS-Short-3outof10": ("files/NPS-CXOS-Short-3outof10.mp4", 25.8, short("The CX OS for Salesforce", "&utm_source=yt_short_qr")),
    "NPS-CXOS-Short-Government-Defense": ("files/NPS-CXOS-Short-Government-Defense.mp4", 27.75, short("Mission-ready CX on Salesforce", "&utm_source=yt_qr_gov", gov=True)),
    "meta_offer_9x16": ("files/meta/meta_offer_9x16.mp4", 11.9, meta()),
    "nps-cxos-4k-3840x2160": ("files/video/nps-cxos-4k-3840x2160.mp4", 18.0, insights(3840, 2160)),
    "nps-cxos-linkedin-1080x1350": ("files/video/nps-cxos-linkedin-1080x1350.mp4", 18.0, insights(1080, 1350)),
}

# Static strips inside the body of a video that still say 7-day: drawn again and laid over the old strip.
PATCHES = {
    "meta_offer_9x16": ("meta_offer_9x16-footer", 1080, 150, 0, 1770, 0.3,
        '<body style="width:1080px;height:150px;background:#fff;color:#0F1A3D;padding:44px 72px 0">'
        '<p style="font-size:34px;font-weight:600;line-height:1.2">Free setup, free switch, 15-day trial</p>'
        '<p style="font-size:27px;color:#5A6787;margin-top:6px">Installs from Salesforce AppExchange. Offer ends Dec 31.</p></body>'),
}

def probe(f, q):
    return subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", q, "-of", "csv=p=0", f]).decode().strip()

def render_cards(names):
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/video/endcards"); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for n in names:
            src = os.path.join(ROOT, JOBS[n][0]); w, h = map(int, probe(src, "stream=width,height").split(","))
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.set_content(f"<html><head><style>{CSS}</style></head>{JOBS[n][2]}</html>")
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            pg.screenshot(path=os.path.join(out, n + ".png")); pg.close()
            if n in PATCHES:
                pn, pw, ph, *_r, html = PATCHES[n]
                pg = b.new_page(viewport={"width": pw, "height": ph})
                pg.set_content(f"<html><head><style>{CSS}</style></head>{html}</html>")
                pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
                pg.screenshot(path=os.path.join(out, pn + ".png")); pg.close()
        b.close()

def splice(n, xf=0.5):
    src, cut, _ = JOBS[n]; src = os.path.join(ROOT, src)
    card = os.path.join(ROOT, "files/video/endcards", n + ".png")
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]))
    hold = dur - cut  # card fills the same time the old one did, so length and audio stay identical
    dst = src[:-4] + "-loop.mp4"; tmp = dst[:-4] + ".part.mp4"
    ins, pre = ["-i", src, "-framerate", "30", "-i", card], "[0:v]"
    if n in PATCHES:
        pn, pw, ph, px, py, fin, _h = PATCHES[n]
        ins += ["-framerate", "30", "-loop", "1", "-t", f"{cut+xf}", "-i", os.path.join(ROOT, "files/video/endcards", pn + ".png")]
        pre = f"[2:v]format=rgb24,fade=in:st=0:d={fin}[p];[0:v][p]overlay={px}:{py}:eof_action=pass[o];[o]"
    fc = (f"{pre}trim=0:{cut+xf},setpts=PTS-STARTPTS,format=yuv420p,fps=30[a];"
          f"[1:v]format=yuv420p,loop=-1:1,trim=duration={hold+xf},fps=30,setpts=PTS-STARTPTS[b];"
          f"[a][b]xfade=transition=fade:duration={xf}:offset={cut}[v]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc,
                           "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                           "-c:a", "copy", "-movflags", "+faststart", "-t", f"{dur}", tmp])
    os.replace(tmp, dst); return dst

if __name__ == "__main__":
    names = sys.argv[2:] or list(JOBS)
    if sys.argv[1] in ("cards", "all"): render_cards(names)
    if sys.argv[1] in ("video", "all"):
        for n in names: print(splice(n))
