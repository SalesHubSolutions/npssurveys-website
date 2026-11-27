"""NPS Survey CX OS data sheet (2 pages, US Letter) -> files/docs/NPS-Survey-CX-OS-Data-Sheet.pdf"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read()
SHOT = base64.b64encode(open(sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/Downloads/NPS-Survey-Loop-kit/appexchange/nps-survey-cx-os-01-dash.png", "rb").read()).decode()
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&utm_source=datasheet"

CSS = plexfont.css() + """
@page{size:8.5in 11in;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"IBM Plex Sans";color:#0F1A3D;font-size:10.5pt;line-height:1.5;-webkit-print-color-adjust:exact}
.pg{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always}
.hd{background:#002FA7;color:#fff;padding:.5in .6in .42in}
.hd svg{height:44px;width:auto;margin-left:-4px}
.k{font-size:8pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#C9D5F2;margin-top:22px}
h1{font-family:"IBM Plex Serif";font-weight:600;font-size:30pt;line-height:1.08;letter-spacing:-.01em;margin-top:6px}
.dk{color:#D6E2FF;font-size:12pt;margin-top:10px;max-width:6.2in}
.bd{padding:.35in .6in}
h2{font-family:"IBM Plex Serif";font-weight:600;font-size:15pt;letter-spacing:-.01em;margin:0 0 8px}
.k2{font-size:7.5pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#002FA7;margin-bottom:4px}
.shot{width:100%;height:2.75in;object-fit:cover;object-position:top left;border-radius:8px;border:1px solid #DCE4F7;display:block;margin:4px 0 14px}
.c3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.c2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.bx{background:#F4F7FF;border-radius:10px;padding:12px 14px}
.bx b{display:block;font-size:10.5pt;margin-bottom:3px}
.bx p,.bx li{font-size:9pt;color:#3B4770;line-height:1.45}
ul{padding-left:14px}li{margin:2px 0}
.stat{display:flex;gap:16px;margin:14px 0 4px}.stat div{flex:1;border-top:2px solid #002FA7;padding-top:6px}
.stat b{font-family:"IBM Plex Serif";font-size:18pt;font-weight:600;display:block;line-height:1.1}.stat span{font-size:8.5pt;color:#5A6787}
.ed{border:1px solid #DCE4F7;border-radius:10px;padding:12px 14px;position:relative}
.ed.rec{border:2px solid #002FA7;background:#F4F7FF}
.ed .tag{position:absolute;top:-9px;left:12px;background:#002FA7;color:#fff;font-size:7pt;font-weight:600;letter-spacing:.06em;text-transform:uppercase;border-radius:99px;padding:2px 8px}
.ed h3{font-size:11.5pt;font-weight:600}.ed .pr{font-family:"IBM Plex Serif";font-size:17pt;font-weight:600;margin:2px 0 4px}.ed .pr small{font-family:"IBM Plex Sans";font-size:8.5pt;font-weight:500;color:#5A6787}
.ed li{font-size:8.8pt;color:#3B4770}
table{width:100%;border-collapse:collapse;font-size:9pt}td{padding:5px 0;border-bottom:1px solid #E7E7E7;vertical-align:top}td:first-child{width:1.7in;font-weight:600}
.ft{position:absolute;left:0;right:0;bottom:0;background:#002FA7;color:#fff;padding:.28in .6in;display:flex;justify-content:space-between;align-items:center}
.cta{background:#FFD60A;color:#0F1A3D;font-weight:600;border-radius:99px;padding:9px 18px;font-size:10.5pt;text-decoration:none}
.ft p{font-size:9pt;color:#D6E2FF;line-height:1.5}.ft b{color:#fff}
.tm{margin-top:10px;font-size:6.8pt;color:#8A94B3;line-height:1.4}
"""

P1 = f"""<div class="pg"><div class="hd">{LOCK}
<div class="k">Data sheet</div>
<h1>Every unhappy customer gets a call back, inside Salesforce.</h1>
<p class="dk">NPS Survey CX OS turns every NPS, CSAT and CES answer into an owned next step on the Account, Contact, Case or Opportunity it belongs to. No exports, no second system, no detractor left waiting.</p></div>
<div class="bd">
<div class="k2">The Salesforce challenge</div>
<div class="c2" style="margin-bottom:14px"><p>Most survey tools sit outside Salesforce. Answers arrive in a separate inbox, get exported to a spreadsheet, and the unhappy customer never hears back. Service, success and sales teams can't see the score on the record they already work in.</p>
<p>NPS Survey CX OS is a managed package that runs natively in your org. Responses are Salesforce records, follow-ups are owned work with a due date, and leaders read one dashboard for NPS, CSAT and follow-up rate across every team.</p></div>
<img class="shot" src="data:image/png;base64,{SHOT}">
<div class="c3">
<div class="bx"><b>Listen</b><p>Survey Studio with AI drafts, 70+ templates, 15+ question types, branching, translations and your brand. Send by email, SMS, link or QR when a Case closes, a deal is won or a renewal nears.</p></div>
<div class="bx"><b>Understand</b><p>NPS, CSAT and CES dashboards by region, team, product and agent. AI sorts every comment by sentiment, churn risk and topic, and summarizes what moved the score.</p></div>
<div class="bx"><b>Act</b><p>Close the Loop gives every low score an owner, a due date and a playbook. Follow-ups, reminders, review requests and nurture run on their own, and every closed loop is tracked.</p></div>
</div></div>
<div class="ft"><p><b>Try it free for 15 days</b><br>Install from Salesforce AppExchange in about 10 minutes.</p><a class="cta" href="{LIST}">Start your free trial</a></div></div>"""

P2 = f"""<div class="pg"><div class="bd" style="padding-top:.5in">
<div class="k2">What teams get</div><h2>One program for service, success and sales</h2>
<div class="c2">
<ul><li><b>Answers on the record.</b> Every response maps to the Account, Contact, Case or Opportunity.</li>
<li><b>Follow-up on every low score.</b> A P1 Case or task with an owner and due date, created automatically.</li>
<li><b>Feedback Inbox.</b> AI sorts answers by sentiment, churn risk and topic so the team works the right ones first.</li>
<li><b>Account and Contact CX panels.</b> Score history, open follow-ups and next best actions on the page layout.</li></ul>
<ul><li><b>Journeys and automation.</b> Onboarding, renewal, closed-won, closed-lost and case-closed surveys run on their own.</li>
<li><b>Brand Kit.</b> Type your website and get surveys in your colors, logo and voice.</li>
<li><b>Review requests.</b> Promoters are invited to leave a Google review at the right moment.</li>
<li><b>Revenue CX and AI digital workers</b> in CX OS Insights: renewals at risk and always-on CX tasks.</li></ul></div>

<div class="k2" style="margin-top:20px">Editions</div><h2>Priced per company, not per user</h2>
<div class="c3" style="margin-top:12px">
<div class="ed"><h3>CX Lite</h3><div class="pr">$3,500 <small>/year</small></div><ul><li>NPS and CSAT by email and link</li><li>Close the loop on every low score</li><li>Standard dashboards</li><li>3 active surveys</li></ul></div>
<div class="ed"><h3>CX Pro</h3><div class="pr">$8,500 <small>/year</small></div><ul><li>Everything in CX Lite</li><li>CES, custom forms and branching</li><li>Review requests and nurture</li><li>Translations, events and QR</li><li>AI comment summaries</li><li>15 active surveys</li></ul></div>
<div class="ed rec"><span class="tag">Recommended</span><h3>CX OS Insights</h3><div class="pr"><small>from </small>$16,000 <small>/year</small></div><ul><li>Everything in CX Pro</li><li>Revenue CX: renewals at risk</li><li>Account CX panels and Command Center</li><li>AI digital workers and Programs</li><li>Unlimited active surveys</li></ul></div></div>
<p style="font-size:8.5pt;color:#5A6787;margin-top:8px">Nonprofit discounts available. Public-sector buyers can purchase through Carahsoft. Current pricing is on the AppExchange listing.</p>

<div class="k2" style="margin-top:20px">Technical details</div>
<table>
<tr><td>Delivery</td><td>Salesforce managed package from AppExchange. Lightning Experience and Salesforce Mobile.</td></tr>
<tr><td>Salesforce editions</td><td>Professional, Enterprise, Unlimited, Performance, Developer and Essentials.</td></tr>
<tr><td>Works with</td><td>Sales Cloud, Service Cloud and Marketing Cloud Engagement.</td></tr>
<tr><td>Data residency</td><td>Surveys, responses and follow-ups are stored as records in your org. No third-party data transfer.</td></tr>
<tr><td>Security</td><td>Respects your profiles, permission sets and sharing rules. Passed Salesforce AppExchange security review.</td></tr>
<tr><td>Setup</td><td>Install in a sandbox, prove one moment, then production. Most teams send a first live survey in a day.</td></tr>
</table>
<div class="stat"><div><b>5.0</b><span>rated on AppExchange</span></div><div><b>10 min</b><span>to install</span></div><div><b>15 days</b><span>free trial, every edition</span></div></div>
<p class="tm">Net Promoter&reg;, NPS&reg; and the NPS-related emoticons are registered trademarks of Bain &amp; Company, Inc., NICE Systems, Inc., and Fred Reichheld. Salesforce and AppExchange are trademarks of Salesforce, Inc.</p></div>
<div class="ft"><p><b>SalesHub, LLC</b>, makers of NPS Survey &nbsp; npssurveys.com<br>support@saleshub.info &nbsp; 1 (833) 733-2468</p><a class="cta" href="{LIST}">Start your free trial</a></div></div>"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/docs/NPS-Survey-CX-OS-Data-Sheet.pdf")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{P1}{P2}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.pdf(path=out, width="8.5in", height="11in", print_background=True)
        b.close()
    print(out)
