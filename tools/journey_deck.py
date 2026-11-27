"""Whitepaper (magazine edition): Reimagining the customer journey -> files/docs/NPS-Survey-Customer-Journey-Mapping.pdf
Loop brand, Plex type, real photos (brand/photos), product screens with a soft brand glow, QR + AppExchange + website on the back
cover, and every page footer links to npssurveys.com and the AppExchange listing."""
import os, sys, base64, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont, segno

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read()
LOCKK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-klein.svg")).read()
MARK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-mark-klein.svg")).read()
MARKW = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-mark-white.svg")).read()
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&utm_source=journey_whitepaper"
SITE = "https://www.npssurveys.com/?utm_source=journey_whitepaper"

def uri(path):
    mime = "image/webp" if path.endswith(".webp") else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode()

def qr(url, px):
    b = io.BytesIO(); segno.make(url, error="h").save(b, kind="svg", scale=10, border=0, dark="#002FA7", xmldecl=False, svgns=True)
    src = "data:image/svg+xml;base64," + base64.b64encode(b.getvalue()).decode(); m = int(px * .24)
    return (f'<div style="position:relative;width:{px}px;height:{px}px;margin:0 auto"><img src="{src}" style="width:100%;height:100%">'
            f'<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{m}px;height:{m}px;background:#fff;border-radius:18%;padding:5%">{MARK}</div></div>')

I = {
 "aware": '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1zM15 9a3 3 0 0 1 0 6M18 6a7 7 0 0 1 0 12"/>',
 "compare": '<path d="M12 3v18M5 7h14M5 7l-3 6a3 3 0 0 0 6 0zM19 7l-3 6a3 3 0 0 0 6 0z"/>',
 "decide": '<path d="M4 12l5 5L20 6"/>',
 "service": '<path d="M4 14v-2a8 8 0 0 1 16 0v2M4 14a2 2 0 0 0 2 2h1v-5H6a2 2 0 0 0-2 2zM20 14a2 2 0 0 1-2 2h-1v-5h1a2 2 0 0 1 2 2zM17 16v1a3 3 0 0 1-3 3h-2"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
 "loyal": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
 "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.3 11l7.4-3.8M8.3 13l7.4 3.8"/>',
 "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0zM8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M8 20h8"/>',
 "case": '<rect x="4" y="7" width="16" height="12" rx="2"/><path d="M9 7V5h6v2M4 12h16"/>',
 "rocket": '<path d="M12 3c4 2 6 6 5 11l-3 3h-4l-3-3C6 9 8 5 12 3zM9 17l-2 4M15 17l2 4"/><circle cx="12" cy="10" r="1.6"/>',
 "renew": '<path d="M20 11a8 8 0 0 0-14-4.5L4 9M4 4v5h5M4 13a8 8 0 0 0 14 4.5L20 15M20 20v-5h-5"/>',
 "smile": '<circle cx="12" cy="12" r="9"/><path d="M8 14a5 5 0 0 0 8 0M9 9.5h.01M15 9.5h.01"/>',
 "alert": '<path d="M12 3l10 18H2zM12 10v5M12 18h.01"/>',
 "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 "spark": '<path d="M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2z"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "chart": '<path d="M4 20V4M4 20h16M8 16v-5M12 16V8M16 16v-3"/>',
 "cal": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
}
def ic(name, size=26):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I[name]}</svg>'

# Brand type scale (npssurveys.com/brand), in CSS px on a 1280 x 720 page. No other sizes are used.
CSS = plexfont.css() + """@page{size:13.333in 7.5in;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"IBM Plex Sans";font-weight:400;font-size:18px;line-height:1.55;color:#0F1A3D;-webkit-print-color-adjust:exact}
a{color:inherit;text-decoration:none}
.s{width:13.333in;height:7.5in;position:relative;overflow:hidden;page-break-after:always}
.pad{position:absolute;inset:0;padding:60px 76px}
.deep{background:#001A66;color:#fff}.blue{background:#002FA7;color:#fff}
.shade{background:linear-gradient(160deg,#F4F7FF 0%,#E3EBFF 100%)}
.display{font-family:"IBM Plex Serif";font-weight:600;font-size:66px;line-height:1.05;letter-spacing:-.01em}
h1{font-family:"IBM Plex Serif";font-weight:600;font-size:60px;line-height:1.05;letter-spacing:-.01em}
h2,.quote,.num{font-family:"IBM Plex Serif";font-weight:600;font-size:40px;line-height:1.15;letter-spacing:-.01em}
h2{margin:10px 0 12px}
h3{font-family:"IBM Plex Serif";font-weight:600;font-size:22px;line-height:1.25}
.lead{font-size:20px;line-height:1.5;color:#4A5779}.dk .lead,.onph .lead{color:#D6E2FF}
.body{font-size:18px;line-height:1.55}.mut{color:#4A5779}.dk .mut,.onph .mut,.glass .mut{color:#D6E2FF}
.btn{font-size:15px;font-weight:600}
.small{font-size:14px;line-height:1.45}
.k{font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;line-height:1.3;color:#002FA7}.dk .k,.onph .k,.glass .k{color:#9DB4F5}
.lk svg{height:44px;width:auto;display:block}
.ft{position:absolute;left:76px;right:76px;bottom:26px;display:flex;justify-content:space-between;align-items:center;font-size:14px;color:#5A6787;z-index:5}
.dk .ft{color:#9DB4F5}.ft .l{display:flex;align-items:center;gap:14px}
.pill{display:flex;align-items:center;background:#fff;color:#002FA7;border-radius:99px;padding:7px 16px;box-shadow:0 4px 12px rgba(0,26,102,.18)}
.ft .r{display:flex;gap:8px}.ft .lk svg{height:26px}
.photo{position:absolute;background-size:cover;background-position:center}
.glow{position:absolute;border-radius:50%;filter:blur(70px)}
.hero{position:absolute;opacity:.10}.hero svg{width:100%;height:100%;display:block}
.glass{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:16px;color:#fff}
.card{background:#fff;border-radius:16px;box-shadow:0 18px 40px rgba(0,26,102,.12)}
.icb,.icl{display:grid;place-items:center;flex:none;width:44px;height:44px;border-radius:12px;background:#002FA7;color:#fff}
.icl{background:rgba(255,255,255,.14)}
.shot{position:absolute;border-radius:14px;box-shadow:0 30px 70px rgba(0,10,60,.45);border:1px solid rgba(255,255,255,.25)}"""

def ft(n):
    return (f'<div class="ft"><span class="l"><a class="pill lk" href="{SITE}">{LOCKK}</a><span>Reimagining the customer journey &nbsp; {n}</span></span>'
            f'<span class="r"><a class="pill btn" href="{SITE}">npssurveys.com</a><a class="pill btn" href="{LIST}">Try it free on AppExchange</a></span></div>')

P = {k: uri(f"brand/photos/{k}.jpg") for k in ["team-meeting", "agent-headset", "review-tablet", "team-huddle"]}
DIAL = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "brand/dials/dial-nps-2048.png"), "rb").read()).decode()
INBOX, ACT = uri("assets/product/inbox-focus.webp"), uri("assets/product/act-focus.webp")

STAGES = [("aware", "Awareness", "They notice your brand.", "Campaign survey"), ("compare", "Consideration", "They compare options.", "Pre-purchase form"),
          ("decide", "Decision", "They choose and buy.", "Post-sale CSAT"), ("service", "Service", "They use it and ask for help.", "Case-closed CSAT"),
          ("chat", "Adoption", "They settle in and use it.", "Follow-up NPS"), ("loyal", "Loyalty", "They stay and refer others.", "Relationship NPS")]

def p1():
    return f"""<div class="s blue dk"><div class="glow" style="width:7in;height:7in;right:-2in;top:-2in;background:#3D6BFF;opacity:.55"></div>
<div class="glow" style="width:5in;height:5in;left:-1.5in;bottom:-2.5in;background:#001A66;opacity:.9"></div>
<div class="glow" style="width:5.4in;height:5.4in;right:.2in;top:.7in;background:#6F8FFF;opacity:.75"></div>
<div style="position:absolute;right:.85in;top:1.05in;width:4.3in;background:#fff;border-radius:28px;padding:26px 26px 18px;box-shadow:0 40px 90px rgba(0,10,60,.5),0 0 0 10px rgba(255,255,255,.12)">
<img src="{DIAL}" style="width:100%;display:block"></div>
<div class="pad" style="display:flex;flex-direction:column"><div class="lk">{LOCK}</div><div style="margin-top:auto">
<div class="k">Whitepaper</div><div class="display" style="margin-top:14px;max-width:7.2in">Reimagining the customer journey</div>
<p class="lead" style="margin-top:20px;max-width:6.9in">From awareness to loyalty: what to ask at each moment, and how to act on every answer inside Salesforce.</p></div><div style="height:.5in"></div></div>{ft(1)}</div>"""

def p2():
    cards = "".join(f'<div class="glass" style="flex:1;padding:18px 16px"><div class="icl">{ic(i)}</div>'
                    f'<h3 style="margin-top:14px">{t}</h3><div class="body mut" style="margin-top:4px">{d}</div>'
                    f'<div class="k" style="margin-top:12px;padding-top:10px;border-top:1px solid rgba(255,255,255,.25)">{q}</div></div>' for i, t, d, q in STAGES)
    return f"""<div class="s deep dk"><div class="photo" style="inset:0;background-image:url({P['team-meeting']})"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,26,102,.96) 0%,rgba(0,47,167,.86) 48%,rgba(0,47,167,.55) 100%)"></div>
<div class="pad onph"><div class="k">01 &nbsp; Understanding the journey</div><h2 style="max-width:8in">Six stages. Six moments to listen.</h2>
<p class="lead" style="max-width:7.4in">Customers move through the same stages in every industry. One short question at each stage shows exactly where the journey breaks.</p>
<div style="display:flex;gap:12px;position:absolute;left:76px;right:76px;bottom:84px">{cards}</div></div>{ft(2)}</div>"""

def p3():
    rows = [("web", "Website visit", "Short web survey or embedded widget"), ("share", "Campaign or social post", "Campaign survey with a QR code or link"),
            ("trophy", "Opportunity won or lost", "Win/loss survey on the Opportunity"), ("case", "Case closed", "CSAT on the Case, follow-up on a low score"),
            ("rocket", "Onboarding complete", "Onboarding check-in on the Account"), ("renew", "Renewal in 60 days", "Relationship NPS to every contact")]
    tr = "".join(f'<div style="display:flex;align-items:center;gap:16px;padding:6px 0;border-bottom:1px solid #D3DDF7"><div class="icb" style="width:36px;height:36px">{ic(i,20)}</div>'
                 f'<div class="body" style="width:2.6in;font-weight:600">{a}</div><div class="body mut">{b}</div></div>' for i, a, b in rows)
    return f"""<div class="s shade"><div class="photo" style="right:0;top:0;bottom:0;width:4.4in;background-image:url({P['agent-headset']})"></div>
<div style="position:absolute;right:0;top:0;bottom:0;width:4.4in;background:linear-gradient(180deg,rgba(0,47,167,0) 40%,rgba(0,26,102,.92) 100%)"></div>
<div style="position:absolute;right:.45in;bottom:84px;width:3.5in;color:#fff" class="quote">"Every touchpoint is a chance to listen."</div>
<div class="pad" style="right:4.4in"><div class="k">02 &nbsp; Touchpoints</div><h2>Ask where the moment already lives</h2>
<p class="lead" style="max-width:7.6in">Tie each survey to the Salesforce event that marks the moment. It sends itself, and the answer lands on the right record.</p>
<div style="margin-top:10px">{tr}</div></div>{ft(3)}</div>"""

def p4():
    sig = [("smile", "Emotions", "How customers feel at each stage."), ("alert", "Pain points", "Where people get stuck, and why."),
           ("bulb", "Opportunities", "Where an extra touch lifts the score."), ("target", "Goals", "What customers are trying to get done.")]
    cards = "".join(f'<div class="glass" style="padding:14px 18px;display:flex;gap:14px;align-items:center"><div class="icl">{ic(i)}</div><div>'
                    f'<h3>{t}</h3><div class="body mut">{d}</div></div></div>' for i, t, d in sig)
    return f"""<div class="s deep dk"><div class="glow" style="width:7.5in;height:6in;right:-.5in;top:.8in;background:#2F6BFF;opacity:.65"></div>
<img class="shot" src="{INBOX}" style="right:-.7in;top:1.2in;width:7.1in">
<div class="small" style="position:absolute;right:.6in;top:.55in;display:flex;gap:8px;align-items:center;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);border-radius:99px;padding:7px 14px;font-weight:600">{ic('spark',16)} AI sorts every answer</div>
<div class="pad onph" style="right:7in"><div class="k">03 &nbsp; What to watch</div><h2>Four signals that tell you where to act</h2>
<div style="display:grid;gap:10px;margin-top:16px">{cards}</div></div>{ft(4)}</div>"""

def p5():
    steps = [("chat", "Collect", "Surveys send themselves at each moment."), ("spark", "Understand", "AI sorts answers by score and topic."),
             ("user", "Act", "A low score opens a follow-up with an owner."), ("chart", "Measure again", "The next score shows if the fix worked.")]
    cards = "".join(f'<div class="card" style="padding:12px 18px;display:flex;gap:14px;align-items:center"><div class="icb">{ic(i)}</div><div>'
                    f'<h3><span class="k" style="margin-right:8px">Step {n+1}</span>{t}</h3><div class="body mut">{d}</div></div></div>' for n, (i, t, d) in enumerate(steps))
    return f"""<div class="s shade"><div style="position:absolute;right:0;top:0;bottom:0;width:6.7in;background:linear-gradient(150deg,#002FA7,#001A66)"></div>
<div class="glow" style="width:6in;height:5in;right:.2in;top:1.6in;background:#3D6BFF;opacity:.7"></div>
<div style="position:absolute;right:.45in;top:60px;color:#fff;width:5.9in" class="quote">Every unhappy answer gets an owner.</div>
<img class="shot" src="{ACT}" style="right:.45in;top:2.05in;width:5.9in">
<div class="pad" style="right:6.7in"><div class="k">04 &nbsp; The feedback loop</div><h2>Use every answer to improve the next journey</h2>
<div style="display:grid;gap:8px;margin-top:14px">{cards}</div></div>{ft(5)}</div>"""

def p6():
    q = [("Quarter 1", "Awareness", "Campaign surveys on new audiences."), ("Quarter 2", "Comparison", "Feedback from prospects while they decide."),
         ("Quarter 3", "Purchase", "How buying and onboarding went."), ("Quarter 4", "Loyalty", "Relationship health before renewal.")]
    tl = "".join(f'<div style="position:relative;padding-left:44px;padding-bottom:10px"><div style="position:absolute;left:0;top:2px;width:26px;height:26px;border-radius:50%;background:#002FA7;border:5px solid #C9D7FF"></div>'
                 f'<div class="k">{a}</div><h3>{b}</h3><div class="body mut">{c}</div></div>' for a, b, c in q)
    return f"""<div class="s"><div class="photo" style="right:0;top:0;bottom:0;width:5in;background-image:url({P['review-tablet']})"></div>
<div style="position:absolute;right:0;top:0;bottom:0;width:5in;background:linear-gradient(90deg,#fff 0%,rgba(255,255,255,0) 22%)"></div>
<div style="position:absolute;right:.5in;bottom:84px;width:3.9in;color:#fff;padding:20px 22px;border-radius:16px;background:rgba(0,47,167,.92)">
<h3 style="display:flex;gap:10px;align-items:center">{ic('cal',22)} Reminders included</h3>
<div class="body" style="color:#D6E2FF;margin-top:6px">Anyone who misses the first invite gets a reminder on your schedule.</div></div>
<div class="pad" style="right:5in"><div class="k">05 &nbsp; Over a year</div><h2>A survey calendar that follows the customer</h2>
<p class="lead" style="max-width:7in;margin-bottom:16px">Schedule recurring surveys around the lifecycle so the score never goes stale.</p>
<div style="position:relative"><div style="position:absolute;left:12px;top:10px;bottom:30px;width:2px;background:#C9D7FF"></div>{tl}</div></div>{ft(6)}</div>"""

def p7():
    w = [("target", "Start with one moment", "Pick the moment that matters most, often a closed Case or a renewal, and switch on its ready-made survey."),
         ("user", "Agree who acts", "Name the owner and the follow-up time for every low score, so no unhappy customer waits."),
         ("chart", "Read one dashboard", "Review NPS, CSAT and follow-up rate together each month, then add the next moment.")]
    cards = "".join(f'<div class="card" style="flex:1;padding:22px"><div style="display:flex;justify-content:space-between;align-items:center"><div class="icb">{ic(i)}</div><div class="num" style="color:#C9D7FF">0{n+1}</div></div>'
                    f'<h3 style="margin-top:12px">{t}</h3><div class="body mut" style="margin-top:6px">{d}</div></div>' for n, (i, t, d) in enumerate(w))
    return f"""<div class="s shade"><div class="photo" style="left:0;right:0;top:0;height:3.1in;background-image:url({P['team-huddle']});background-position:center 25%"></div>
<div style="position:absolute;left:0;right:0;top:0;height:3.1in;background:linear-gradient(90deg,rgba(0,26,102,.95) 0%,rgba(0,47,167,.78) 45%,rgba(0,47,167,.15) 100%)"></div>
<div class="pad onph" style="color:#fff"><div class="k">06 &nbsp; Getting started</div><h2 style="max-width:7in">Three quick wins for your first month</h2></div>
<div style="position:absolute;left:76px;right:76px;top:2.55in;display:flex;gap:18px">{cards}</div>{ft(7)}</div>"""

def p8():
    return f"""<div class="s blue dk"><div class="glow" style="width:7in;height:7in;left:-2in;top:-2.5in;background:#3D6BFF;opacity:.5"></div>
<div class="hero" style="width:7.5in;height:7.5in;left:-2.6in;bottom:-3.2in">{MARKW}</div>
<div class="pad" style="display:flex;flex-direction:column"><div class="lk">{LOCK}</div><div style="margin-top:auto;display:flex;gap:.6in;align-items:flex-end">
<div style="flex:1"><h1 style="max-width:8.2in">Map the journey. Then close the loop on every answer.</h1>
<p class="lead" style="margin-top:16px">NPS Survey CX OS runs inside Salesforce. One price per company, with a 15-day free trial.</p>
<div style="margin-top:24px;display:flex;gap:12px"><a class="btn" href="{LIST}" style="background:#FFD60A;color:#0F1A3D;border-radius:99px;padding:14px 28px">Start your free trial on AppExchange</a>
<a class="btn" href="{SITE}" style="background:#fff;color:#002FA7;border-radius:99px;padding:14px 26px">npssurveys.com</a></div>
<p class="small" style="margin-top:16px;color:#D6E2FF">support@saleshub.info &nbsp; 1 (833) 733-2468</p></div>
<a href="{LIST}" style="display:block;background:#fff;border-radius:22px;padding:20px 20px 14px;text-align:center;color:#0F1A3D">{qr(LIST, 190)}<div class="btn" style="margin-top:10px">Scan to try it free</div><div class="small" style="color:#5A6787">Salesforce AppExchange</div></a></div>
<div style="height:.45in"></div></div>{ft(8)}</div>"""

CHECK = """() => { const out=[]; document.querySelectorAll('.s').forEach((s,i)=>{ const sr=s.getBoundingClientRect(); const f=s.querySelector('.ft').getBoundingClientRect();
 s.querySelectorAll('h1,h2,h3,p,.body,.lead,.k,.quote,.card,.glass,.display,.small').forEach(e=>{ if(e.closest('.ft')) return; const r=e.getBoundingClientRect();
  if(r.width===0) return; if(r.bottom>f.top-8 && r.top<f.bottom && r.right>f.left && r.left<f.right) out.push(`p${i+1} hits footer: ${e.textContent.trim().slice(0,40)}`);
  if(r.right>sr.right+1||r.bottom>sr.bottom+1) out.push(`p${i+1} off page: ${e.textContent.trim().slice(0,40)}`); });
 s.querySelectorAll('.card,.glass,.quote').forEach(a=>{ s.querySelectorAll('.card,.glass,.quote,.shot').forEach(b=>{ if(a===b||a.contains(b)||b.contains(a)) return;
  const r=a.getBoundingClientRect(), q=b.getBoundingClientRect(); if(r.left<q.right-2&&q.left<r.right-2&&r.top<q.bottom-2&&q.top<r.bottom-2) out.push(`p${i+1} overlap: ${a.textContent.trim().slice(0,30)} / ${b.textContent.trim().slice(0,30)||b.tagName}`);});}); });
 const sizes=new Set(); document.querySelectorAll('body *').forEach(e=>{ if(e.closest('svg')) return; if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())) sizes.add(getComputedStyle(e).fontSize); });
 return {issues:out, sizes:[...sizes]}; }"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/docs/NPS-Survey-Customer-Journey-Mapping.pdf")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{p1()}{p2()}{p3()}{p4()}{p5()}{p6()}{p7()}{p8()}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        print(pg.evaluate(CHECK))
        pg.pdf(path=out, width="13.333in", height="7.5in", print_background=True); b.close()
    print(out, os.path.getsize(out) // 1024, "KB")
