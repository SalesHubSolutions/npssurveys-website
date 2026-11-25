"""Generate branded drip email HTML (same design as g2.html). Output: files/email/<key>.html"""
import pathlib, html
D = pathlib.Path(__file__).parent
SITE = "https://www.npssurveys.com"
F = "font-family:Arial,Helvetica,sans-serif;"
CAL = "https://calendly.com/npssurvey/demo"
APPX = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3"

def u(url, camp, key, part):
    sep = "&amp;" if "?" in url else "?"
    return f"{url}{sep}utm_source=drip&amp;utm_medium=email&amp;utm_campaign={camp}&amp;utm_content={key}_{part}"

def W(inner, pad="0 32px"):
    return f'<tr><td style="background:#ffffff;padding:{pad};">{inner}</td></tr>\n'

def checks(items, color="#267A72"):
    rows = "".join(f'<tr><td width="34" valign="top" style="padding:0 0 14px 0;"><div style="width:24px;height:24px;line-height:24px;border-radius:12px;background:{color};color:#fff;{F}font-size:13px;font-weight:bold;text-align:center;">&#10003;</div></td><td valign="top" style="padding:0 0 14px 0;{F}font-size:16px;line-height:24px;color:#3A4664;">{t}</td></tr>' for t in items)
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>'

def steps(items):
    cols = ["#002FA7", "#2F58C4", "#5C7FD6", "#267A72"]
    out = ""
    for i, (t, d) in enumerate(items):
        last = i == len(items) - 1
        c = "#267A72" if last else cols[min(i, 2)]
        n = "&#10003;" if last else str(i + 1)
        out += f'<tr><td width="52" valign="top" style="padding:0 0 16px 0;"><div style="width:38px;height:38px;line-height:38px;border-radius:19px;background:{c};color:#fff;{F}font-size:16px;font-weight:bold;text-align:center;">{n}</div></td><td valign="top" style="padding:0 0 16px 0;{F}"><div style="font-size:17px;font-weight:bold;color:{"#267A72" if last else "#0F1A3D"};">{t}</div><div style="font-size:15px;line-height:22px;color:#5A6787;">{d}</div></td></tr>'
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{out}</table>'

def paras(ps):
    return "".join(f'<p style="margin:0 0 14px 0;">{p}</p>' for p in ps)

def img(src, href, alt, cap=None):
    c = f'<div style="{F}font-size:13px;color:#5A6787;padding:10px 2px 0 2px;">{cap}</div>' if cap else ""
    return f'<a href="{href}"><img src="{src}" width="536" alt="{alt}" style="display:block;width:100%;max-width:536px;height:auto;border:1px solid #DCE3F5;border-radius:12px;"></a>{c}'

def cta(label, href, second=None):
    s = f'<div style="{F}font-size:14px;padding-top:14px;"><a href="{second[1]}" style="color:#002FA7;font-weight:bold;text-decoration:none;">{second[0]}</a></div>' if second else ""
    return f'<tr><td align="center" style="background:#ffffff;padding:26px 32px 6px 32px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:#FFD60A;border-radius:10px;"><a href="{href}" style="display:inline-block;padding:16px 30px;{F}font-size:16px;font-weight:bold;color:#0F1A3D;text-decoration:none;">{label} &rarr;</a></td></tr></table>{s}</td></tr>\n'

def trust(gov):
    cells = ([("Carahsoft", "CoreTrust contract<br>24COR-018GR")] if gov else [("Security reviewed", "by Salesforce for<br>AppExchange")]) + [("100% Salesforce", "Data never leaves<br>your org"), ('<span style="color:#FFB800;">&#9733;&#9733;&#9733;&#9733;&#9733;</span>', "Rated 5.0 on<br>AppExchange")]
    tds = ""
    for i, (b, s) in enumerate(cells):
        mid = "border-left:1px solid #E3E8F4;border-right:1px solid #E3E8F4;" if i == 1 else ""
        tds += f'<td width="33%" align="center" style="padding:16px 6px;{F}font-size:12px;line-height:17px;color:#5A6787;{mid}"><b style="display:block;font-size:14px;color:#0F1A3D;">{b}</b>{s}</td>'
    return W(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #E3E8F4;border-bottom:1px solid #E3E8F4;"><tr>{tds}</tr></table>', "28px 32px 0 32px")

def build(key, camp, label, preheader, kicker, head, hl, greet, body_html, hero=None, gov=False, light=False):
    home = f"{SITE}/public-sector/" if gov else f"{SITE}/"
    hero_row = f'<tr><td style="padding:0;background:#002FA7;line-height:0;font-size:0;"><a href="{u(home,camp,key,"hero")}"><img src="{hero[0]}" width="600" alt="{hero[1]}" style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a></td></tr>\n' if hero else ""
    hl_html = f' <span style="background:#FFD60A;padding:0 4px;">{hl}</span>' if hl else ""
    foot_extra = f'<a href="{u(SITE+"/webinar/",camp,key,"footer")}" style="color:#ffffff;text-decoration:none;font-weight:bold;">Live demo Dec 3</a>'
    out = f'''<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"></head>
<body style="margin:0;padding:0;background:#EEF2FB;">
<span style="display:none;max-height:0;overflow:hidden;opacity:0;">{preheader}</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#EEF2FB;"><tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#002FA7;border-radius:16px;">
<tr><td style="background:#002FA7;padding:22px 32px;border-radius:16px 16px 0 0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td><a href="{u(home,camp,key,"logo")}"><img src="{SITE}/files/email/logo-white.png" width="146" height="44" alt="NPS Survey CX OS by SalesHub" style="display:block;border:0;"></a></td>
<td align="right" style="{F}font-size:12px;letter-spacing:1.5px;color:#C7D5FF;font-weight:bold;">{label}</td></tr></table></td></tr>
{hero_row}<tr><td style="background:#ffffff;padding:{"34px" if hero else "30px"} 32px 6px 32px;{F}">
<div style="font-size:12px;letter-spacing:1.6px;font-weight:bold;color:#002FA7;">{kicker}</div>
<h1 style="margin:10px 0 0 0;font-family:'IBM Plex Serif',Georgia,'Times New Roman',serif;font-size:{"28px;line-height:34px" if light else "32px;line-height:38px"};font-weight:600;color:#0F1A3D;">{head}{hl_html}</h1></td></tr>
<tr><td style="background:#ffffff;padding:14px 32px 4px 32px;{F}font-size:16px;line-height:25px;color:#3A4664;"><p style="margin:0 0 12px 0;">{greet}</p></td></tr>
{body_html}{"" if light else trust(gov)}<tr><td style="background:#ffffff;padding:24px 32px 30px 32px;{F}font-size:15px;line-height:23px;color:#3A4664;">Best regards,<br><b style="color:#0F1A3D;">SalesHub Support Team</b><br><a href="mailto:support@saleshub.info" style="color:#002FA7;text-decoration:none;">support@saleshub.info</a> &middot; 1 (833) 733-2468</td></tr>
<tr><td style="background:#0F1A3D;padding:24px 32px;border-radius:0 0 16px 16px;{F}font-size:12px;line-height:19px;color:#AFC0E8;">
<a href="{u(APPX,camp,key,"footer")}" style="color:#ffffff;text-decoration:none;font-weight:bold;">AppExchange</a> &nbsp;&middot;&nbsp; <a href="https://www.youtube.com/@saleshubllc" style="color:#ffffff;text-decoration:none;font-weight:bold;">YouTube</a> &nbsp;&middot;&nbsp; <a href="https://www.linkedin.com/company/12673581" style="color:#ffffff;text-decoration:none;font-weight:bold;">LinkedIn</a> &nbsp;&middot;&nbsp; {foot_extra}<br><br>
SalesHub, LLC &middot; Georgia-certified small business &middot; 1853 Piedmont Rd NE, Suite 301, Marietta, GA 30066<br>Not the right fit? Reply &ldquo;unsubscribe&rdquo; and we won&rsquo;t email you again.</td></tr>
</table></td></tr></table></body></html>
'''
    (D / f"{key}.html").write_text(out)

C, G = "CUSTOMER EXPERIENCE IN SALESFORCE", "FOR STATE &amp; LOCAL GOVERNMENT"
E = f"{SITE}/files/email"
YT = lambda vid, camp, key: u(f"https://www.youtube.com/watch?v={vid}", camp, key, "video")
TRIAL = f"{SITE}/go/?s=drip"
txt = lambda ps: W(f'<div style="{F}font-size:16px;line-height:25px;color:#3A4664;">{paras(ps)}</div>', "0 32px")

k, c = "ncx01", "ncx_nurture"
build(k, c, C, "Thanks for your interest. Here is the whole idea in 75 seconds.", "WELCOME", "Your 75-second tour of", "NPS Survey CX OS.", "Hi {!Lead.FirstName},",
  txt(["Thanks for your interest in NPS Survey CX OS, the customer experience platform that runs 100% inside Salesforce. Here is the whole idea in 75 seconds:"])
  + W(img(f"{E}/video-tour.jpg", YT("uXIZmwdQTdQ", c, k), "Watch: NPS Survey CX OS in 75 seconds", "&#9654; Watch: NPS Survey CX OS in 75 seconds"), "4px 32px 22px 32px")
  + W(checks(["<b>NPS, CSAT and effort surveys</b> sent right from Salesforce", "<b>Close the Loop:</b> every unhappy customer gets an owner and a follow-up", "<b>Dashboards</b> for NPS trends, sentiment and churn risk on every account"]), "0 32px")
  + cta("Book a 30-minute demo", u(CAL, c, k, "cta"), ("Or start a free 15-day trial on AppExchange", u(TRIAL, c, k, "trial"))))

k = "ncx02"
build(k, c, C, "Detractors who told you what was wrong quietly churn. Here is how to stop that.", "CLOSE THE LOOP", "Stop losing customers", "you already heard from.", "Hi {!Lead.FirstName},",
  txt(["Most teams collect NPS, then the feedback sits in a spreadsheet. Detractors who told you exactly what was wrong quietly churn. NPS Survey CX OS closes that gap inside Salesforce:"])
  + W(checks(["A score of 0 to 6 <b>opens a follow-up</b> for the right owner, with a due date", "Answers appear on the <b>Account, Contact, Case and Opportunity</b> your team already works in", "Managers see which customers were <b>won back</b>, and which are still at risk"]), "4px 32px 8px 32px")
  + W(img(f"{E}/close-the-loop.jpg", u(SITE + "/close-the-loop/", c, k, "shot"), "Close the Loop in Salesforce", "Close the Loop: every unhappy answer gets an owner and a due date."), "6px 32px 0 32px")
  + cta("See it on your data", u(CAL, c, k, "cta"), ("&#9654; Watch: From churn to champions", YT("HJ6EvUrWmsM", c, k))))

k = "ncx03"
build(k, c, C, "Build a survey, send it, read the results and act, in one short video.", "WATCH THE DEMO", "Design, send, analyze and act,", "in 2.5 minutes.", "Hi {!Lead.FirstName},",
  txt(["If you'd like to see the whole flow before talking to anyone, this is the one to watch: building a survey, sending it from Salesforce, reading the results and acting on them."])
  + W(img(f"{E}/video-demo.jpg", YT("IYMiJXBxkQU", c, k), "Watch the full demo", "&#9654; Full demo: design, send, analyze and act"), "4px 32px 18px 32px")
  + txt(["Want a quicker look at one piece? Eight short clips, about 25 seconds each, cover survey building, question types, win/loss surveys, account-level NPS and analytics."])
  + cta("Book a 30-minute demo", u(CAL, c, k, "cta"), ("Browse the 25-second feature clips", "https://www.youtube.com/@saleshubllc")))

k = "ncx04"
build(k, c, C, "Where does the feedback data go? Nowhere. It stays in Salesforce.", "SECURITY &amp; TRUST", "Your feedback data", "never leaves Salesforce.", "Hi {!Lead.FirstName},",
  txt(["A quick note on what IT and security teams usually ask first: where does the data go? With NPS Survey CX OS, it doesn't go anywhere. Unlike bolt-on survey tools that sync data in and out of Salesforce, it is built natively on the platform."])
  + W(checks(["<b>Passed the Salesforce security review</b> for AppExchange", "<b>Rated 5.0</b> on AppExchange", "Uses your <b>existing security, sharing rules and reporting</b>, with no connectors to maintain", "Covered by the controls Salesforce is audited for: <b>SOC 2, ISO 27001</b> and more"]), "4px 32px 8px 32px")
  + W(img(f"{E}/account-cx.jpg", u(SITE + "/", c, k, "shot"), "Account CX inside Salesforce", "Scores, AI summary and next steps on the Account record, inside your org."), "6px 32px 0 32px")
  + cta("View the AppExchange listing", u(APPX, c, k, "cta"), ("Or book a 30-minute demo", u(CAL, c, k, "demo"))))

k = "ncx05"
build(k, c, C, "GetFeedback retires on December 31, 2026. Here is the easy way off.", "GETFEEDBACK RETIRES DEC 31", "Moving off GetFeedback?", "Read this first.", "Hi {!Lead.FirstName},",
  txt(["If your team runs surveys with GetFeedback, it is being retired on December 31, 2026. And if you use another bolt-on tool, the same question applies: is the feedback actually driving action inside Salesforce?", "Teams that move to NPS Survey CX OS:"])
  + W(checks(["<b>Rebuild their NPS, CSAT and effort surveys</b> in minutes, or we move them for you", "See every answer on the <b>Account and Contact</b> records they already use", "Add <b>Close the Loop</b> follow-up their old tool never had"]), "0 32px 4px 32px")
  + W(steps([("Week 1: map your surveys", "We list every survey, trigger and report you run today."), ("Week 2: rebuild and test", "Surveys rebuilt natively, tested in a sandbox."), ("Live before Dec 31", "Your first survey goes out from Salesforce, with follow-ups on.")]), "10px 32px 0 32px")
  + cta("Plan my migration", u(CAL, c, k, "cta"), ("See the switch guide", u(SITE + "/switch/", c, k, "switch"))))

k = "ncx06"
build(k, c, C, "One last note from the NPS Survey team.", "ONE LAST NOTE", "Should we", "close your file?", "Hi {!Lead.FirstName},",
  txt(["We've sent a few notes about NPS Survey CX OS and haven't heard back, which usually means one of three things:"])
  + W(steps([("The timing isn't right", "Reply \"later\" and we'll check back in a few months."), ("Someone else owns customer experience", "Reply with their name and we'll reach out to them instead."), ("You're all set", "Reply \"unsubscribe\" and this is the last email you'll get from us.")]), "4px 32px 0 32px")
  + cta("Book a 30-minute demo", u(CAL, c, k, "cta")), light=True)

k = "ncx10"
build(k, "ncx_customer", "WELCOME ABOARD", "Welcome aboard. Here is what happens in your first 30 days.", "WELCOME ABOARD", "Welcome to NPS Survey CX OS.", "Here's what's next.", "Hi {!Contact.FirstName},",
  txt(["Thank you for choosing NPS Survey CX OS. We're excited to help your team turn every answer into action. Here is your first 30 days:"])
  + W(steps([("Kickoff call", "We'll reach out within 2 business days to schedule onboarding."), ("Install", "We'll walk you through installing from AppExchange, sandbox first, then production."), ("First survey live", "Most teams send their first NPS survey within two weeks."), ("30-day check-in", "We review results and switch on Close the Loop with you.")]), "4px 32px 8px 32px")
  + W(img(f"{E}/video-demo.jpg", YT("IYMiJXBxkQU", "ncx_customer", k), "Watch the full demo", "&#9654; A good primer for your admins: the full demo"), "6px 32px 0 32px")
  + cta("Watch the full demo", YT("IYMiJXBxkQU", "ncx_customer", k), ("Questions? Just reply, or write to support@saleshub.info", "mailto:support@saleshub.info")))

c = "gov"
k = "g1"
build(k, c, G, "Hear from residents after every pothole, permit and 311 call.", "RESIDENT FEEDBACK", "Hear from residents", "after every service.", "Hi {!Lead.FirstName},",
  txt(["When a resident reports a pothole, renews a permit or calls 311, the request is closed in your system. What is often missing is the resident's view of how it went.", "NPS Survey CX OS runs inside Salesforce:"])
  + W(checks(["A short survey goes out <b>when a case or request closes</b>, in the resident's language", "The answer lands on <b>the same record</b> your team already works", "An unhappy answer <b>opens a follow-up</b> for the right person, so no low score sits unread"]), "0 32px 4px 32px")
  + txt(["Is resident feedback something {!Lead.Company} is looking at this year?"])
  + cta("Book a 20-minute walkthrough", u(CAL, c, k, "cta"), ("See the public-sector overview", u(SITE + "/public-sector/", c, k, "link"))),
  hero=("https://images.pexels.com/photos/34520606/pexels-photo-34520606.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=1200&amp;h=540&amp;fit=crop", "A county staff member helping a resident"), gov=True)

k = "g3"
build(k, c, G, "No new solicitation needed: Carahsoft and CoreTrust 24COR-018GR.", "SIMPLE TO BUY", "Buy it through", "Carahsoft or CoreTrust.", "Hi {!Lead.FirstName},",
  txt(["Buying software is often the slowest part, so we made it simple:"])
  + W(checks(["<b>Carahsoft:</b> available through the public-sector distributor many agencies already use", "<b>CoreTrust cooperative contract 24COR-018GR:</b> eligible agencies buy without a new solicitation", "<b>Georgia-certified small business:</b> may help with your small-business goals", "<b>No new platform to approve:</b> it installs from AppExchange into your existing Salesforce org"]), "0 32px 4px 32px")
  + txt(["Should I send the contract details to you or to a colleague?"])
  + cta("Send me the contract details", "mailto:support@saleshub.info?subject=Contract%20details%20for%20NPS%20Survey%20CX%20OS", ("See the public-sector overview", u(SITE + "/public-sector/", c, k, "link"))), gov=True)

k = "g4"
build(k, c, G, "Twenty minutes, one real request, start to finish.", "20-MINUTE WALKTHROUGH", "See it on", "a real request.", "Hi {!Lead.FirstName},",
  txt(["Would 20 minutes help? Here is what we would show you:"])
  + W(steps([("A request closes", "A survey goes out to the resident by text or email."), ("A low score comes in", "A follow-up opens for the owning department, with a due date."), ("Leaders see it", "The dashboard your directors would use, by service and district.")]), "4px 32px 8px 32px")
  + W(img(f"{E}/close-the-loop.jpg", u(SITE + "/public-sector/", c, k, "shot"), "Close the Loop in Salesforce"), "6px 32px 0 32px")
  + cta("Pick a time", u(CAL, c, k, "cta"), ("Or reply with a time that suits you", "mailto:support@saleshub.info?subject=Walkthrough%20time")), gov=True)

k = "g5"
build(k, c, G, "A short last note from the NPS Survey team.", "THANK YOU", "Closing the loop", "on my notes.", "Hi {!Lead.FirstName},",
  txt(["I have not heard back, so I will stop here. If resident feedback becomes a priority for {!Lead.Company}, reply to this email and we will pick it up from there.", "Thank you for the work you do for your residents."])
  + cta("Book a walkthrough anytime", u(CAL, c, k, "cta")), gov=True, light=True)

k = "g6"
build(k, c, G, "Our last note for now.", "ONE LAST NOTE", "Should we", "close your file?", "Hi {!Lead.FirstName},",
  txt(["We have sent a few notes about resident feedback inside Salesforce and have not heard back, so this will be our last one for now.", "If improving resident or employee experience becomes a priority, reply to this email or book a time below, and we will tailor a short walkthrough to your agency's services."])
  + cta("Book a 20-minute walkthrough", u(CAL, c, k, "cta")), gov=True, light=True)
print("generated")
