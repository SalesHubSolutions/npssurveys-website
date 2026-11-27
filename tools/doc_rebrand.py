"""Loop-brand the customer PDFs: new cover page in Plex, old product names updated in the text.
Writes in place under files/docs/ (originals stay in git history and in files/_originals/docs/)."""
import os, sys, shutil, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont, fitz
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "files/docs")
LOCK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read()

# file: (kicker, title, subtitle, edition line, drop original first page?)
JOBS = {
    "NPS-Survey-CX-OS-Getting-Started-Guide.pdf": ("Customer onboarding guide", "Getting started with NPS Survey CX OS",
        "Navigate the platform, build and send surveys, set up automation, read NPS and response analytics, and manage access.", "For Salesforce admins and CX owners", False),
    "NPS-Survey-CX-OS-Configuration-Resource-Pack.pdf": ("Configuration resource pack", "Configure NPS Survey CX OS for your org",
        "Installation, advanced configuration, administration, automation, reporting and go-live, in one reference.", "For admins and implementation teams", False),
    "NPS-Survey-Installation-and-Configuration-Guide.pdf": ("Installation and configuration guide", "Install NPS Survey CX OS in Salesforce",
        "Step-by-step setup with screenshots for administrators, business users and developers.", "For Salesforce admins &nbsp; Quick version: npssurveys.com/install", True),
    "NPS-Survey-CX-OS-Survey-Scheduler-and-Reminders.pdf": ("Business user guide", "Survey scheduler and reminders",
        "Send surveys from event records, then remind people who have not answered, on a schedule you set.", "Advanced automation", False),
}
# Interior text is left as written: install steps name the real package, site and guest-user artifacts.
SWAPS = []

CSS = plexfont.css() + """*{margin:0;padding:0;box-sizing:border-box}
body{background:#002FA7;color:#fff;font-family:"IBM Plex Sans";-webkit-print-color-adjust:exact}
.p{position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between}
.p svg.lk{width:auto;align-self:flex-start;display:block}
.k{font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#C9D5F2}
h1{font-family:"IBM Plex Serif";font-weight:600;letter-spacing:-.01em;line-height:1.06}
.s{color:#D6E2FF;line-height:1.45}
.ft{display:flex;justify-content:space-between;align-items:flex-end;color:#C9D5F2}
.ring{position:absolute;border-radius:50%;border:solid rgba(255,255,255,.07)}"""

def ttf(name):
    w = TTFont(os.path.join(ROOT, "tools/fonts", name)); w.flavor = None
    b = io.BytesIO(); w.save(b); return b.getvalue()

def cover_pdf(pw, ph, kick, title, sub, ed):
    from playwright.sync_api import sync_playwright
    u = pw / 612  # scale from Letter width
    if pw > ph: u = ph / 612
    html = f"""<html><head><style>{CSS}
.p{{width:{pw}pt;height:{ph}pt;padding:{56*u}pt {60*u}pt}} .p svg.lk{{height:{40*u}pt}} .k{{font-size:{9.5*u}pt}}
h1{{font-size:{40*u}pt;margin-top:{10*u}pt;max-width:{440*u}pt}} .s{{font-size:{13.5*u}pt;margin-top:{16*u}pt;max-width:{420*u}pt}}
.ft{{font-size:{9.5*u}pt}} .ring{{right:{-120*u}pt;bottom:{-120*u}pt;width:{420*u}pt;height:{420*u}pt;border-width:{48*u}pt}}</style></head>
<body><div class="p">{LOCK.replace('<svg', '<svg class="lk"', 1)}
<div><div class="k">{kick}</div><h1>{title}</h1><p class="s">{sub}</p></div>
<div class="ft"><span>{ed}</span><span>npssurveys.com &nbsp; support@saleshub.info</span></div></div></body></html>"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        data = pg.pdf(width=f"{round(pw*4/3,2)}px", height=f"{round(ph*4/3,2)}px", print_background=True, page_ranges="1"); b.close()
    return fitz.open("pdf", data)

def swap_text(doc, reg, bold):
    n = 0
    for page in doc:
        hits = []
        for old, new in SWAPS:
            for r in page.search_for(old):
                # sample the text's own size and colour, and the background under it
                info = None
                for blk in page.get_text("dict", clip=r)["blocks"]:
                    for ln in blk.get("lines", []):
                        for sp in ln["spans"]:
                            if old.split()[0] in sp["text"] or old[:6] in sp["text"]: info = sp
                if not info: continue
                pix = page.get_pixmap(clip=fitz.Rect(r.x0 - 3, r.y0, r.x0 - 1, r.y1), dpi=72)
                bg = tuple(c / 255 for c in pix.pixel(0, max(0, pix.height // 2))[:3]) if pix.width else (1, 1, 1)
                hits.append((r, new, info, bg))
        for r, new, info, bg in hits:
            page.add_redact_annot(r, fill=bg)
        if hits:
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
            for r, new, info, bg in hits:
                c = info["color"]; col = ((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255
                isb = "Bold" in info["font"] or info["flags"] & 16
                fs = info["size"]
                font = fitz.Font(fontbuffer=bold if isb else reg)
                while font.text_length(new, fs) > (r.width * 1.35) and fs > 5: fs -= .25
                page.insert_font(fontname="PlexB" if isb else "PlexR", fontbuffer=bold if isb else reg)
                page.insert_text((r.x0, r.y1 - (r.height - fs) / 2 - fs * .22), new, fontsize=fs, fontname="PlexB" if isb else "PlexR", color=col)
                n += 1
    return n

def main():
    reg, bold = ttf("IBMPlexSans-Regular.woff2"), ttf("IBMPlexSans-SemiBold.woff2")
    os.makedirs(os.path.join(ROOT, "files/_originals/docs"), exist_ok=True)
    for f, (k, t, s, e, drop) in JOBS.items():
        src = os.path.join(DOCS, f); keep = os.path.join(ROOT, "files/_originals/docs", f)
        if not os.path.exists(keep): shutil.copy(src, keep)
        doc = fitz.open(keep)
        n = swap_text(doc, reg, bold)
        if drop: doc.delete_page(0)
        r = doc[0].rect
        cov = cover_pdf(r.width, r.height, k, t, s, e)
        doc.insert_pdf(cov, start_at=0)
        doc.set_metadata({"title": t + " | NPS Survey CX OS", "author": "SalesHub, LLC", "subject": s, "creator": "SalesHub"})
        doc.save(src + ".tmp", garbage=3, deflate=True); os.replace(src + ".tmp", src)
        print(f, "swaps", n, "pages", doc.page_count, os.path.getsize(src) // 1024, "KB")

if __name__ == "__main__":
    main()
