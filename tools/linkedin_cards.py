"""LinkedIn cards in the Klein Blue brand (flat #002FA7, Loop mark, white card), 1080x1350 rendered at 2x = 2160x2700.
Examples: social/2026-11/li-*.png. Edit CARDS (kicker, headline, card HTML, card top, footer url, note) and run: python3 tools/linkedin_cards.py
Output PNGs land in the current folder; move them to social/YYYY-MM/li-<name>.png.
Accent test: a CARDS key ending in -y renders the URL pill (the CTA) and one <em> headline word in Signal Yellow #FFD60A. Nothing else is ever yellow."""
import asyncio, sys
from playwright.async_api import async_playwright
LOOP = '<svg viewBox="0 0 100 100" width="64" height="64"><path d="M31.07 77.03 A33 33 0 1 1 68.93 77.03" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/><circle cx="50" cy="83" r="7.5" fill="#fff"/></svg>'
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;background:#002FA7;color:#fff;font-family:"IBM Plex Sans",sans-serif;-webkit-font-smoothing:antialiased;position:relative;overflow:hidden}
.top{position:absolute;left:84px;top:80px;display:flex;align-items:center;gap:18px}
.brand b{display:block;font-size:34px;font-weight:700;letter-spacing:-.01em}.brand span{display:block;font-size:20px;opacity:.78;margin-top:2px;font-weight:500}
.kick{position:absolute;left:84px;top:236px;font-size:26px;font-weight:600;color:#b9c8f2}
h1{position:absolute;left:84px;right:84px;top:282px;font-size:72px;line-height:1.04;font-weight:700;letter-spacing:-.025em}
.card{position:absolute;left:84px;right:84px;background:#fff;color:#0f1a3d;border-radius:28px;box-shadow:0 30px 80px rgba(0,10,50,.35);padding:40px 44px}
.foot{position:absolute;left:84px;right:84px;bottom:76px;display:flex;align-items:center;justify-content:space-between;gap:24px}
.pill{background:#fff;color:#002FA7;}body.y .pill{background:#FFD60A;}body.y h1 em{color:#FFD60A;font-style:normal}.pill{font-size:30px;font-weight:700;padding:20px 34px;border-radius:999px;letter-spacing:-.01em}
.note{font-size:21px;color:#c9d5f2;text-align:right;line-height:1.35;max-width:430px}
.lab{font-size:19px;color:#5c6784;font-weight:600}
.q{font-size:30px;font-weight:700;letter-spacing:-.01em;margin-top:8px;line-height:1.2}
.row{display:flex;align-items:center;gap:12px}
.chip{font-size:20px;font-weight:600;padding:9px 18px;border-radius:999px;background:#edf1fb;color:#002FA7}
.chip.on{background:#002FA7;color:#fff}
.scale{display:grid;grid-template-columns:repeat(11,1fr);gap:8px;margin-top:22px}
.scale div{height:58px;border:2px solid #dbe3f5;border-radius:12px;display:grid;place-items:center;font-size:22px;font-weight:600;color:#33405f}
.scale div.sel{background:#002FA7;border-color:#002FA7;color:#fff}
.sub{font-size:21px;color:#5c6784;margin-top:6px}
.hr{height:1px;background:#e6ebf5;margin:26px 0}
.btn{font-size:20px;font-weight:600;padding:12px 20px;border-radius:12px;border:2px solid #dbe3f5;color:#0f1a3d}
.btn.p{background:#002FA7;border-color:#002FA7;color:#fff}
.bar{height:12px;border-radius:6px;background:#e6ebf5;overflow:hidden;margin-top:12px}.bar i{display:block;height:100%;background:#002FA7;border-radius:6px}
.li{display:flex;align-items:center;justify-content:space-between;padding:20px 0;border-top:1px solid #e6ebf5}.li:first-of-type{border-top:0}
.n{font-size:26px;font-weight:700}.m{font-size:20px;color:#5c6784;margin-top:4px}
.red{background:#fdecec;color:#b42318}.amb{background:#fdf3e1;color:#9a5b00}.grn{background:#e7f6ee;color:#127a45}
.ck{width:36px;height:36px;border-radius:50%;background:#127a45;display:grid;place-items:center;flex:none}
.ic{width:52px;height:52px;border-radius:14px;background:#edf1fb;color:#002FA7;display:grid;place-items:center;font-size:24px;font-weight:800;flex:none}
"""
CHECK='<svg width="20" height="20" viewBox="0 0 20 20"><path d="M4 10.5l4 4 8-9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def page(kick, h1, card, top, url, note):
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top">{LOOP}<div class="brand"><b>NPS Survey</b><span>CX OS by SalesHub</span></div></div>
<div class="kick">{kick}</div><h1>{h1}</h1><div class="card" style="top:{top}px">{card}</div>
<div class="foot"><div class="pill">{url}</div><div class="note">{note}</div></div></body></html>"""
CARDS = {
"translations": page("New on the blog","Every customer gets the survey in their language.","""
<div class="row"><span class="lab">Survey languages</span></div>
<div class="row" style="margin-top:14px"><span class="chip">English</span><span class="chip on">Español</span><span class="chip">Français</span><span class="chip">Deutsch</span></div>
<div class="hr"></div><div class="lab">Relationship NPS · sent in Spanish</div>
<div class="q">¿Qué tan probable es que nos recomiende a un amigo o colega?</div>
<div class="scale">"""+"".join(f'<div class="{"sel" if i==9 else ""}">{i}</div>' for i in range(11))+"""</div>
<div class="row" style="justify-content:space-between;margin-top:12px"><span class="sub">Nada probable</span><span class="sub">Muy probable</span></div>""",500,"npssurveys.com/insights","One survey, many languages. Each contact's language picks the version."),
"events": page("New on the blog","Register. Check in. Ask how it went. All in Salesforce.","""
<div class="row" style="gap:24px"><div style="width:110px;height:118px;border-radius:18px;background:#002FA7;color:#fff;display:grid;place-items:center;text-align:center;flex:none"><div><div style="font-size:20px;font-weight:600;opacity:.8">DEC</div><div style="font-size:50px;font-weight:700;line-height:1">10</div></div></div>
<div><div class="q" style="margin:0">Customer Day</div><div class="sub">10:00 AM to 3:00 PM · Atlanta, GA</div><div class="row" style="margin-top:14px"><span class="btn p">Google Calendar</span><span class="btn">Outlook</span></div></div></div>
<div class="hr"></div>
<div class="row" style="justify-content:space-between"><span class="lab">At the door</span><span class="lab" style="color:#002FA7">QR self check-in</span></div>
<div class="row" style="justify-content:space-between;margin-top:10px"><span class="n">42 of 50 checked in</span><span class="sub" style="margin:0">84%</span></div>
<div class="bar"><i style="width:84%"></i></div>
<div class="hr"></div><div class="row" style="justify-content:space-between"><span class="n" style="font-size:24px">Thank-you survey to all 42</span><span class="chip on">Send</span></div>""",590,"npssurveys.com/insights","Registration page, calendar invite, door list and follow-up survey."),
"renewals": page("New on the blog","Your feedback already knows which renewals are at risk.","""
<div class="row" style="justify-content:space-between"><span class="lab">Needs you this week</span><span class="lab">Ranked by money and renewal date</span></div>
<div style="margin-top:8px">
<div class="li"><div><div class="n">Harbor Logistics</div><div class="m">Renews in 41 days · price and support comments</div></div><div style="text-align:right"><div class="n">$240K</div><span class="chip red" style="display:inline-block;margin-top:6px">Act now</span></div></div>
<div class="li"><div><div class="n">Brightline Health</div><div class="m">Renews in 56 days · reliability comments</div></div><div style="text-align:right"><div class="n">$180K</div><span class="chip red" style="display:inline-block;margin-top:6px">Act now</span></div></div>
<div class="li"><div><div class="n">Summit Foods</div><div class="m">Renews in 76 days · mixed feedback</div></div><div style="text-align:right"><div class="n">$150K</div><span class="chip amb" style="display:inline-block;margin-top:6px">Watch</span></div></div>
</div><div class="row" style="margin-top:16px"><span class="btn p">Plan the save</span><span class="sub" style="margin:0">One clear next step for each account</span></div>""",590,"npssurveys.com/insights","Feedback, renewal dates and contract value in one weekly list."),
"closeloop": page("Playbook","Every low score gets an owner. Same day.","""
<div class="row" style="justify-content:space-between"><span class="lab">New answer · Relationship NPS</span><span class="chip red">Score 3</span></div>
<div class="q">“Billing changed again and nobody told us.”</div><div class="sub">Dana Lee · Director of Operations</div>
<div class="hr"></div>
<div class="row" style="gap:18px"><div class="ic">1</div><div><div class="n" style="font-size:24px">Follow-up opened automatically</div><div class="m">High priority · on the Account and Contact</div></div></div>
<div class="row" style="gap:18px;margin-top:20px"><div class="ic">2</div><div><div class="n" style="font-size:24px">Owner: Account Manager</div><div class="m">Due tomorrow · call the customer</div></div></div>
<div class="row" style="gap:18px;margin-top:20px"><div class="ck">"""+CHECK+"""</div><div><div class="n" style="font-size:24px">Closed the loop</div><div class="m">Called, fixed the invoice, told them what changed</div></div></div>""",520,"npssurveys.com/insights","The 5-step playbook for closing the loop in Salesforce."),
"measures": page("Playbook","NPS, CSAT or CES? Ask the right one at the right moment.","""
<div class="li"><div class="row" style="gap:20px"><div class="ic">N</div><div><div class="n">NPS</div><div class="m">How the relationship is going</div></div></div><span class="chip">Quarterly, after onboarding</span></div>
<div class="li"><div class="row" style="gap:20px"><div class="ic">C</div><div><div class="n">CSAT</div><div class="m">How one interaction went</div></div></div><span class="chip">When a case closes</span></div>
<div class="li"><div class="row" style="gap:20px"><div class="ic">E</div><div><div class="n">CES</div><div class="m">How easy a task was</div></div></div><span class="chip">After a task is done</span></div>""",590,"npssurveys.com/insights","Which survey to send at each moment in Salesforce."),
"switch": page("GetFeedback retires December 31","Move your surveys into native Salesforce. Keep every answer.","""
<div class="lab">Switch checklist</div>
"""+"".join(f'<div class="row" style="gap:18px;margin-top:22px"><div class="ck">{CHECK}</div><div><div class="n" style="font-size:25px">{a}</div><div class="m">{b}</div></div></div>' for a,b in [("Export your surveys and history","Questions, answers and dates"),("Import into Salesforce","Matched to Contacts and Accounts by email"),("Rebuild triggers natively","Case close, onboarding, renewal"),("Turn on follow-up","Every low score gets an owner")]),560,"npssurveys.com/insights","A checklist for Salesforce teams. 7-day free trial on AppExchange."),
"partner-migration": page("For Salesforce partners","Your clients need a survey migration by December 31.","""
<div class="row" style="justify-content:space-between"><span class="lab">Migration project · fixed scope</span><span class="chip">5 phases</span></div>
"""+"".join(f'<div class="row" style="gap:18px;margin-top:20px"><div class="ic">{i+1}</div><div><div class="n" style="font-size:25px">{a}</div><div class="m">{b}</div></div></div>' for i,(a,b) in enumerate([("Discover","Inventory every survey, trigger and owner"),("Export","Definitions and response history"),("Rebuild in a sandbox","Same Salesforce events, same fields"),("Cut over","One survey live, then the rest"),("Hand over","Owners, follow-up rules, admin training")]))+"""
<div class="hr"></div><div class="row" style="justify-content:space-between"><span class="n" style="font-size:23px">Keep 100% of services</span><span class="chip on">25% yr 1 + 10% renewals</span></div>""",470,"npssurveys.com/insights","Implementation partner terms. Full terms in the SalesHub partner agreement."),
"reminders": page("Admin how-to","Remind only the people who haven't answered.","""
<div class="row" style="justify-content:space-between"><span class="lab">Onboarding survey · reminder limit 2</span><span class="chip">24 hours apart</span></div>
<div style="margin-top:8px">
<div class="li"><div class="row" style="gap:20px"><div class="ic">0</div><div><div class="n" style="font-size:25px">Survey sent</div><div class="m">Day 0 · when the record qualifies</div></div></div><span class="chip">Sent</span></div>
<div class="li"><div class="row" style="gap:20px"><div class="ic">1</div><div><div class="n" style="font-size:25px">Reminder 1</div><div class="m">Day 1 · only because there's no answer yet</div></div></div><span class="chip">Sent</span></div>
<div class="li"><div class="row" style="gap:20px"><div class="ck">"""+CHECK+"""</div><div><div class="n" style="font-size:25px">Answered</div><div class="m">Day 1 · reminders stop for this survey</div></div></div><span class="chip grn">Done</span></div>
</div><div class="hr"></div><div class="row" style="justify-content:space-between"><span class="n" style="font-size:23px">Reminder 2</span><span class="chip">Never sent</span></div>""",520,"npssurveys.com/insights","The 24-hour rule, reminder limits, and Live vs. Snapshot mode."),
"csat-case-close": page("Admin how-to","Ask about the case while it's fresh. Once.","""
<div class="row" style="justify-content:space-between"><span class="lab">Case 00012874 · Billing question</span><span class="chip grn">Closed</span></div>
<div class="hr"></div><div class="lab">CSAT survey · sent once, to the case contact</div>
<div class="q">How satisfied were you with how we handled your request?</div>
<div class="row" style="gap:10px;margin-top:20px">"""+"".join(f'<span class="btn{" p" if i==2 else ""}" style="flex:1;text-align:center;font-size:24px">{i}</span>' for i in range(1,6))+"""</div>
<div class="row" style="justify-content:space-between;margin-top:10px"><span class="sub">Very unsatisfied</span><span class="sub">Very satisfied</span></div>
<div class="hr"></div>
<div class="row" style="gap:18px"><div class="ic">!</div><div><div class="n" style="font-size:24px">Low score: owner notified</div><div class="m">Saved on the Case and Contact · follow up today</div></div></div>""",520,"npssurveys.com/insights","Trigger, audience, send once, save on the record, route low scores.")
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=2)
        for k,h in CARDS.items():
            await pg.set_content(h.replace("<body>",'<body class="y">',1) if k.endswith("-y") else h); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"{k}.png")
        await b.close()
asyncio.run(main())
