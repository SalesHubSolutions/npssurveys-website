"""Shared brand pieces for Letter PDFs (data sheet, release notes, guides).
Document type scale (pt), same roles as the web scale on npssurveys.com/brand:
  title 30 Serif 600 | section 16 Serif 600 | card title 11 Serif 600 | big number 18 Serif 600
  lead 12 | body 9.5 | button 10.5 Sans 600 | small 8 | kicker 7.5 Sans 600 caps +8%
Fixed elements: QR (Klein, Loop centre, white card) and the sign-off bar (logo pill, npssurveys.com, AppExchange)."""
import os, io, base64, segno
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-mark-klein.svg")).read().replace("<svg", "<svg style='width:100%;height:100%;display:block'", 1)
LOCKK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-klein.svg")).read()
SIZES = {"30pt", "16pt", "11pt", "18pt", "12pt", "9.5pt", "10.5pt", "8pt", "7.5pt"}

def qr(url, px):
    b = io.BytesIO(); segno.make(url, error="h").save(b, kind="svg", scale=10, border=0, dark="#002FA7", xmldecl=False, svgns=True)
    src = "data:image/svg+xml;base64," + base64.b64encode(b.getvalue()).decode(); m = int(px * .24)
    return (f'<div style="position:relative;width:{px}px;height:{px}px;margin:0 auto"><img src="{src}" style="width:100%;height:100%">'
            f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{m}px;height:{m}px;background:#fff;border-radius:18%;padding:5%">{MARK}</div></div>')

def qr_card(url, px=70):
    return (f'<a href="{url}" style="display:block;background:#fff;border-radius:14px;padding:10px 10px 7px;text-align:center;color:#0F1A3D;text-decoration:none">'
            f'{qr(url, px)}<div style="font-size:8pt;font-weight:600;margin-top:5px">Scan to try it free</div></a>')

def signoff(site, listing):
    pill = "display:inline-flex;align-items:center;background:#fff;color:#002FA7;border-radius:99px;padding:4px 11px;font-size:8pt;font-weight:600;text-decoration:none"
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">'
            f'<a href="{site}" style="{pill};padding:4px 12px">{LOCKK.replace("<svg", "<svg style='height:22px;width:auto;display:block'", 1)}</a>'
            f'<span style="display:flex;gap:6px"><a href="{site}" style="{pill}">npssurveys.com</a><a href="{listing}" style="{pill}">Try it free on AppExchange</a></span></div>')

CHECK = """() => { const s=new Set(); document.querySelectorAll('body *').forEach(e=>{ if(e.closest('svg')) return;
  if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())) s.add(Math.round(parseFloat(getComputedStyle(e).fontSize)*0.75*10)/10+'pt'); });
  const o=[]; document.querySelectorAll('.pg').forEach((p,i)=>{ const r=p.getBoundingClientRect(); const f=p.querySelector('.ft'); const ft=f?f.getBoundingClientRect().top:r.bottom; p.querySelectorAll('*').forEach(e=>{ if(f&&f.contains(e)) return; if(!(['IMG','TR','LI'].includes(e.tagName)||[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))) return; const q=e.getBoundingClientRect(); if(q.height&&q.width&&(q.bottom>r.bottom+1||(q.bottom>ft-4&&q.top<ft+200))) o.push('p'+(i+1)+' hits footer: '+(e.textContent||'').trim().slice(0,30)); }); });
  return {sizes:[...s], overflow:o.slice(0,5)}; }"""
