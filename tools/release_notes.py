"""Release notes 2.5.5 (Loop brand, US Letter) -> files/docs/NPS-Survey-CX-OS-Release-Notes-v2.5.5.pdf
Items are taken from the 2.5.5 package source (SalesHubSolutions/NPS-Survey, commit 41f2d7e) and checked
against the 2.4 notes so nothing already announced in 2.4 is called new."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plexfont, brandprint

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = open(os.path.join(ROOT, "brand/logo-kit/svg/nps-survey-logo-white.svg")).read()
SITE = "https://www.npssurveys.com/?utm_source=release_notes"
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&utm_source=release_notes"

NEW = [
 ("Guided survey sites setup", "One setup screen prepares the NPS, CSAT and Voice of the Customer survey sites. Site settings are stored as configuration records, and a dedicated guest-access permission set keeps respondents limited to what a survey needs."),
 ("Access by profile", "App Access Manager can now give access to everyone on a profile at once, as well as to individual users, so new hires get the right screens without extra steps."),
 ("A sturdier sending engine", "Immediate sends, scheduled sends, condition-based sends and reminders now run as background jobs with a distribution poller, so large sends and reminder waves finish reliably without holding up users."),
 ("Trigger toggles you can control", "Each automation trigger can be switched on or off per org, and only people with the Manage Trigger Toggles permission can change them."),
 ("Email template library", "Create, attach and edit survey email templates in one place. A guard asks for confirmation before you edit a template that live surveys already use."),
 ("Command Center filters", "Filter the CX Command Center by time period and account before you drill into analytics."),
]
CARRIED = ["CX Command Center with NPS, CSAT, response rate, loop closure and trends", "Guided Survey Builder, including the Matrix Grid question",
           "Automation Command Center with initial-send timing, reminders and conditions", "Trigger Control Panel", "Survey Response Analytics with flexible filters",
           "Email Library", "App Access Manager with license utilization", "Close the Loop follow-up on every low score"]

CSS = plexfont.css() + """@page{size:8.5in 11in;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"IBM Plex Sans";color:#0F1A3D;font-size:9.5pt;line-height:1.5;-webkit-print-color-adjust:exact}
.pg{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always}
.hd{background:#002FA7;color:#fff;padding:.5in .6in .4in}.hd svg{height:42px;width:auto;display:block}
.k{font-size:7.5pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#C9D5F2;margin-top:22px}
h1{font-family:"IBM Plex Serif";font-weight:600;font-size:30pt;line-height:1.08;letter-spacing:-.01em;margin-top:6px}
.dk{color:#D6E2FF;font-size:12pt;margin-top:10px;max-width:6.4in}
.bd{padding:.32in .6in}
h2{font-family:"IBM Plex Serif";font-weight:600;font-size:16pt;letter-spacing:-.01em;margin:4px 0 8px}
.k2{font-size:7.5pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#002FA7;margin-top:16px}
.it{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.bx{background:#F4F7FF;border-radius:10px;padding:12px 14px}.bx b{display:block;font-family:"IBM Plex Serif";font-weight:600;font-size:11pt;margin-bottom:3px}.bx p{font-size:9.5pt;color:#3B4770}
ul{padding-left:15px}li{margin:3px 0;font-size:9.5pt}
table{width:100%;border-collapse:collapse;font-size:9.5pt}td{padding:6px 0;border-bottom:1px solid #E7E7E7;vertical-align:top}td:first-child{width:1.8in;font-weight:600}
.ft{position:absolute;left:0;right:0;bottom:0;background:#002FA7;color:#fff;padding:.26in .6in;display:flex;justify-content:space-between;align-items:center}
.ft p{font-size:9.5pt;color:#D6E2FF}.ft b{color:#fff}
.cta{background:#FFD60A;color:#0F1A3D;font-weight:600;border-radius:99px;padding:9px 18px;font-size:10.5pt;text-decoration:none}
.tm{font-size:8pt;color:#8A94B3;margin-top:12px;line-height:1.4}"""

def page():
    new = "".join(f'<div class="bx"><b>{t}</b><p>{d}</p></div>' for t, d in NEW)
    car = "".join(f"<li>{x}</li>" for x in CARRIED)
    return f"""<div class="pg"><div class="hd">{LOCK}<div class="k">Release notes</div><h1>Version 2.5.5</h1>
<p class="dk">The version you install from Salesforce AppExchange today. It builds on 2.4 with a guided survey sites setup, access by profile and a sturdier sending engine for scheduled surveys and reminders.</p></div>
<div class="bd"><div class="k2">New and improved since 2.4</div><h2>What changed</h2><div class="it">{new}</div>
</div><div class="ft" style="align-items:flex-end;gap:.3in"><div style="flex:1"><p><b>SalesHub, LLC</b>, makers of NPS Survey &nbsp; support@saleshub.info</p>{brandprint.signoff(SITE, LIST)}</div><a class="cta" href="{LIST}">Get version 2.5.5</a></div></div>
<div class="pg"><div class="bd" style="padding-top:.55in"><div class="k2" style="margin-top:0">Still included</div><h2>Carried forward from 2.4</h2><ul style="columns:2;column-gap:24px">{car}</ul>
<div class="k2">Install and upgrade</div><h2>Before and after you install</h2>
<table><tr><td>New customers</td><td>Install from AppExchange into a sandbox first, then production. Every edition starts with a 15-day free trial.</td></tr>
<tr><td>Before you install</td><td>Turn on Digital Experiences in Setup. Builder surveys continue to use Experience Cloud survey sites in this version.</td></tr>
<tr><td>Upgrading</td><td>Existing surveys, responses and follow-ups stay in place. Run the guided survey sites setup once after the upgrade, then confirm access in App Access Manager.</td></tr>
<tr><td>Guides</td><td>Install and setup: npssurveys.com/install. Getting started guide, configuration resource pack and data sheet: npssurveys.com/#resources.</td></tr></table>
<p class="tm">Feature availability depends on your edition, org configuration and assigned access. Salesforce and AppExchange are trademarks of Salesforce, Inc.</p></div>
<div class="ft" style="align-items:flex-end;gap:.3in"><div style="flex:1"><p><b>SalesHub, LLC</b>, makers of NPS Survey<br>support@saleshub.info &nbsp; 1 (833) 733-2468</p>{brandprint.signoff(SITE, LIST)}</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:8px"><a class="cta" href="{LIST}">Get version 2.5.5</a></div><div style="width:1.05in">{brandprint.qr_card(LIST, 70)}</div></div></div>"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = os.path.join(ROOT, "files/docs/NPS-Survey-CX-OS-Release-Notes-v2.5.5.pdf")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{page()}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300); print(pg.evaluate(brandprint.CHECK))
        pg.pdf(path=out, width="8.5in", height="11in", print_background=True); b.close()
    print(out)
