"""Brand SVG figures for Insights posts. Run: python3 tools/figures.py  (writes content/figures/*.svg)
Embed in a post with {{FIG:name|Caption text}}."""
import os, math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(ROOT,"content/figures"); os.makedirs(OUT,exist_ok=True)
NAVY="#0C184A"; BLUE="#1E54E8"; DEEP="#052CA0"; SKY="#DCE7FF"; TINT="#F4F7FF"; LINE="#DCE4F7"; MUTE="#5E6B98"; SOFT="#3B4877"
RED="#EB5757"; AMB="#E9A52B"; GRN="#23A96A"; YEL="#FFE443"; W="#FFFFFF"
F='font-family="Inter, Arial, sans-serif"'
def t(x,y,s,size=16,fill=NAVY,w=600,a="start"): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{a}" {F}>{s}</text>'
def r(x,y,w,h,rx=12,fill=W,stroke=LINE,sw=1.5): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def arrow(x1,y1,x2,y2,c=BLUE,dash=False,small=False):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{2.5 if small else 3}" marker-end="url(#{'ahs' if small else MK.get(c,'ah')})"{" stroke-dasharray=\"7 7\"" if dash else ""}/>'
DEFS=f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker><marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker><marker id="aha" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{AMB}"/></marker>'+''.join(f'<marker id="ah{k}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{v}"/></marker>' for k,v in (("r",RED),("g",GRN)))+'</defs>'
MK={AMB:"aha",RED:"ahr",GRN:"ahg"}
def svg(w,h,body,label): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{DEFS}<rect width="{w}" height="{h}" rx="18" fill="{TINT}"/>{body}</svg>'

def timeline():
    W_,H=1000,300; b=t(40,50,"Your switch timeline to December 31, 2026",22,NAVY,800)
    ms=[("Oct 31","Inventory done","first export taken"),("Nov 14","Tool chosen","installed in sandbox"),("Nov 26","Top 2 surveys","rebuilt and tested"),("Dec 8","First survey","live in production"),("Dec 15","All surveys live","old tool read-only"),("Dec 22","Final export","old tool retired")]
    x0,x1,y=70,880,150; b+=f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{SKY}" stroke-width="10" stroke-linecap="round"/>'
    for i,(d,a,c) in enumerate(ms):
        x=x0+i*(x1-x0-40)/(len(ms)-1)
        b+=f'<circle cx="{x}" cy="{y}" r="15" fill="{BLUE}" stroke="{W}" stroke-width="4"/>'+t(x,y+5,str(i+1),13,W,800,"middle")
        b+=t(x,y-32,d,16,BLUE,800,"middle")+t(x,y+46,a,15,NAVY,700,"middle")+t(x,y+68,c,13,MUTE,500,"middle")
    xe=950; b+=f'<circle cx="{xe}" cy="{y}" r="20" fill="{RED}"/>'+t(xe,y+6,"!",20,W,800,"middle")+t(xe,y-36,"Dec 31",16,RED,800,"middle")+t(xe,y+108,"GetFeedback",13,RED,700,"middle")+t(xe,y+126,"Direct sunsets",13,RED,700,"middle")
    return svg(W_+20,H,b,"Timeline: six milestones from October 31 to December 22, before GetFeedback Direct sunsets on December 31, 2026")

def architecture():
    Wd,H=1000,420; b=t(40,50,"Bolt-on survey tool vs. native app",22,NAVY,800)
    # left
    b+=r(40,80,450,310,16,W)+t(64,114,"BOLT-ON",13,RED,800)+t(64,138,"Data lives in two places",16,NAVY,700)
    b+=r(70,170,170,80,12,TINT)+t(155,205,"Salesforce",16,NAVY,800,"middle")+t(155,228,"records",13,MUTE,500,"middle")
    b+=r(300,170,160,80,12,"#FFF4DB",AMB)+t(380,205,"Vendor cloud",16,NAVY,800,"middle")+t(380,228,"responses",13,MUTE,500,"middle")
    b+=arrow(244,195,296,195,AMB,True)+arrow(296,225,244,225,AMB,True)+t(270,272,"connector + field mapping",13,AMB,700,"middle")
    for i,s in enumerate(["New vendor security review","Sync errors and duplicates","Low scores noticed late"]): b+=t(74,316+i*24,"✕  "+s,14,SOFT,600)
    # right
    b+=r(510,80,450,310,16,W,BLUE,2.5)+t(534,114,"NATIVE (NPS SURVEY CX OS)",13,BLUE,800)+t(534,138,"Everything on the record",16,NAVY,700)
    b+=r(524,160,422,120,14,"#EAF1FF",BLUE)+t(540,182,"Inside your Salesforce org",12,BLUE,800)
    steps=[("Event","sends survey"),("Answer","on record"),("Low score","opens case"),("Dashboard","CX360")]
    for i,(a,c) in enumerate(steps):
        x=536+i*108; b+=r(x,196,78,68,10,W,LINE)+t(x+39,224,a,12.5,NAVY,800,"middle")+t(x+39,244,c,11,MUTE,600,"middle")
        if i<3: b+=arrow(x+82,230,x+104,230,small=True)
    for i,s in enumerate(["Data never leaves Salesforce","No connector to maintain","Every detractor gets an owner"]): b+=t(544,316+i*24,"✓  "+s,14,GRN,700)
    return svg(Wd,H,b,"Comparison: a bolt-on survey tool keeps responses in a vendor cloud synced by a connector; a native app keeps the whole loop inside Salesforce")

def loop():
    Wd,H=1000,520; b=t(40,50,"The service measurement loop",22,NAVY,800)+t(40,78,"Measure every redesign at the moment of service, then fix what the scores show.",15,MUTE,500)
    cx,cy,R=500,295,170; nodes=[("1","Service happens","application, call, visit"),("2","Short survey","CSAT or effort, 1–3 questions"),("3","Answer on record","case and contact in Salesforce"),("4","Low score routed","owner and due date"),("5","Monthly review","theme comments by cause"),("6","Redesign","then measure again")]
    b+=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{SKY}" stroke-width="12"/>'
    for i in range(6):
        a=math.radians(-90+i*60+30); a2=math.radians(-90+(i+1)*60-8)
        b+=f'<path d="M{cx+R*math.cos(a):.1f} {cy+R*math.sin(a):.1f} A{R} {R} 0 0 1 {cx+R*math.cos(a2):.1f} {cy+R*math.sin(a2):.1f}" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#ah)"/>' if False else ""
    for i,(n,a,c) in enumerate(nodes):
        ang=math.radians(-90+i*60); x=cx+R*math.cos(ang); y=cy+R*math.sin(ang)
        bw=250; bx=x-bw/2 + (70 if math.cos(ang)>0.3 else -70 if math.cos(ang)<-0.3 else 0); by=y-34
        b+=r(bx,by,bw,68,14,W,BLUE if i in (3,) else LINE,2)+f'<circle cx="{bx+24}" cy="{by+34}" r="14" fill="{NAVY}"/>'+t(bx+24,by+39,n,13,W,800,"middle")+t(bx+46,by+30,a,15,NAVY,800)+t(bx+46,by+51,c,12,MUTE,500)
    b+=f'<circle cx="{cx}" cy="{cy}" r="92" fill="{NAVY}"/>'+t(cx,cy-12,"Did it work",15,W,600,"middle")+t(cx,cy+8,"for the people",15,YEL,800,"middle")+t(cx,cy+28,"we serve?",15,YEL,800,"middle")
    return svg(Wd,H,b,"A six-step loop: service happens, a short survey, the answer on the record, low scores routed, monthly review, redesign and measure again")

def routing():
    Wd,H=1000,380; b=t(40,50,"How every score is routed in Salesforce",22,NAVY,800)
    x0,y0,cw=80,90,76
    for n in range(11):
        c=RED if n<=6 else AMB if n<=8 else GRN; b+=r(x0+n*cw,y0,cw-8,56,10,c,c)+t(x0+n*cw+(cw-8)/2,y0+36,str(n),20,W,800,"middle")
    groups=[(0,6,RED,"Detractor (0–6)","P1 case opens","Owner + due date, same-day call"),(7,8,AMB,"Passive (7–8)","30-day nurture","Check-in task or helpful email"),(9,10,GRN,"Promoter (9–10)","Thank-you + ask","Review, referral or case study")]
    for i,(a,z,c,h,act,d) in enumerate(groups):
        mid=x0+((a+z+1)/2)*cw-4; bx=60+i*300; by=220
        b+=arrow(mid,y0+62,bx+130,by-6,c)
        b+=r(bx,by,260,120,14,W,c,2.5)+t(bx+20,by+32,h,14,c,800)+t(bx+20,by+64,act,20,NAVY,800)+t(bx+20,by+92,d,13,MUTE,500)
    return svg(Wd,H,b,"Score routing: 0 to 6 opens a P1 case with an owner, 7 to 8 starts a 30-day nurture, 9 to 10 gets a thank-you and a review request")

def dashboard():
    Wd,H=1000,500; b=t(40,50,"What a closed-loop dashboard should show",22,NAVY,800)+t(960,50,"SAMPLE DATA",12,MUTE,800,"end")
    kp=[("NPS","+42","▲ 9 this quarter",GRN),("Detractors contacted","96%","target 95%",BLUE),("Median time to contact","1.4 days","target 2 days",NAVY),("Responses","4,812","31% response rate",NAVY)]
    for i,(a,v,c,col) in enumerate(kp):
        x=40+i*232; b+=r(x,80,216,104,14,W)+t(x+18,108,a,13,MUTE,700)+t(x+18,148,v,30,col,800)+t(x+18,172,c,12,MUTE,500)
    b+=r(40,200,440,270,14,W)+t(58,228,"NPS trend, last 8 weeks",14,NAVY,800)
    pts=[38,36,40,39,44,43,47,50]; xs=[70+i*55 for i in range(8)]; ys=[430-(p-30)*8 for p in pts]
    b+=f'<polyline points="{" ".join(f"{x},{y}" for x,y in zip(xs,ys))}" fill="none" stroke="{BLUE}" stroke-width="4" stroke-linejoin="round"/>'
    for x,y in zip(xs,ys): b+=f'<circle cx="{x}" cy="{y}" r="5" fill="{W}" stroke="{BLUE}" stroke-width="3"/>'
    b+=f'<line x1="60" y1="440" x2="460" y2="440" stroke="{LINE}" stroke-width="2"/>'
    b+=r(500,200,460,270,14,W)+t(518,228,"Open detractor cases",14,NAVY,800)
    rows=[("Acme Corp","3","A. Rivera","Today",RED),("Northwind","5","J. Chen","Tomorrow",AMB),("Harbor Health","4","M. Patel","Tomorrow",AMB),("Summit Freight","6","K. Osei","In 2 days",NAVY)]
    b+=t(518,258,"Account",12,MUTE,700)+t(690,258,"Score",12,MUTE,700)+t(760,258,"Owner",12,MUTE,700)+t(880,258,"Due",12,MUTE,700)
    for i,(a,s,o,d,c) in enumerate(rows):
        y=292+i*42; b+=f'<line x1="518" y1="{y-24}" x2="942" y2="{y-24}" stroke="{LINE}"/>'+t(518,y,a,14,NAVY,700)+r(690,y-17,30,24,6,RED,RED)+t(705,y,s,13,W,800,"middle")+t(760,y,o,14,SOFT,600)+t(880,y,d,14,c,700)
    return svg(Wd,H,b,"Sample dashboard with NPS, share of detractors contacted, median time to contact, responses, an 8-week NPS trend and open detractor cases with owners and due dates")

def flow(title,sub,steps,label,accent_last=True):
    Wd,H=1000,330; b=t(40,50,title,22,NAVY,800)+(t(40,78,sub,15,MUTE,500) if sub else "")
    n=len(steps); gap=40; bw=(920-gap*(n-1))/n
    for i,(a,c,d) in enumerate(steps):
        x=40+i*(bw+gap); last=accent_last and i==n-1
        b+=r(x,110,bw,180,16,"#EAF1FF" if last else W,BLUE if last else LINE,2.5 if last else 1.5)
        b+=f'<circle cx="{x+30}" cy="{142}" r="16" fill="{BLUE if last else NAVY}"/>'+t(x+30,147,str(i+1),14,W,800,"middle")
        b+=t(x+20,196,a,18,NAVY,800)
        for j,line in enumerate(c.split("|")): b+=t(x+20,224+j*21,line,13.5,MUTE,500)
        if d: b+=t(x+bw-18,147,d,14,BLUE,800,"end")
        if i<n-1: b+=arrow(x+bw+6,200,x+bw+gap-4,200,small=True)
    return svg(Wd,H,b,label)

def business_case():
    return flow("From four numbers to a CFO-ready business case","The free ROI calculator at npssurveys.com/roi",
        [("Enter 4 inputs","Accounts, revenue per|account, churn rate,|hours of manual work",""),("See the risk","Revenue at risk each|year and hours spent|on manual follow-up",""),("See payback","How many saved|accounts cover the|plan you pick",""),("Send to your CFO","A one-page business|case, ready to print|or save as PDF","~60 seconds")],
        "Four steps: enter four inputs, see revenue at risk, see payback by plan, send a one-page business case to your CFO")

def partner_tracks():
    Wd,H=1000,416; b=t(40,50,"SalesHub partner program for Salesforce SIs",22,NAVY,800)
    rows=[("REFERRAL PARTNER",[("Register","the opportunity"),("We sell","demo, close, onboard"),("You earn","20% of first year")],LINE,1.5),
          ("IMPLEMENTATION PARTNER",[("Register","deal registration"),("You deliver","keep 100% of services"),("You earn","25% yr 1 + 10% renewals")],BLUE,2.5)]
    for k,(h,st,sc,sw) in enumerate(rows):
        y=80+k*150; b+=r(40,y,920,130,16,"#EAF1FF" if k else W,sc,sw)+t(64,y+30,h,13,BLUE if k else MUTE,800)
        for i,(a,c) in enumerate(st):
            x=64+i*300; last=i==2
            b+=r(x,y+46,250,66,12,BLUE if last else W,BLUE if last else LINE)+t(x+18,y+74,a,16,W if last else NAVY,800)+t(x+18,y+97,c,13.5,"#DCE7FF" if last else MUTE,600)
            if i<2: b+=arrow(x+256,y+79,x+294,y+79,small=True)
    b+=t(40,392,"Example on CX Pro ($8,500/yr): referral $1,700 · implementation $2,125 in year one + $850 per renewal",14,SOFT,600)
    return svg(Wd,H,b,"Partner tracks: referral partners register, SalesHub sells, partner earns 20% of first year; implementation partners register, deliver and keep services revenue, and earn 25% of first year plus 10% of renewals")


def case_close_flow():
    return flow("CSAT on case close: the whole loop in Salesforce","One trigger, one survey per case, every answer on the record",
        [("Case closes","Status moves to a|closed value you|chose",""),("Survey sends","Once, to the case|contact, after a|short delay",""),("They rate it","One CSAT question|and one optional|\"why\" question",""),("Answer saved","On the Case and|Contact, ready for|reports",""),("Owner acts","A low score goes|to an owner who|follows up","")],
        "Five steps: a case closes, the survey sends once to the case contact, the customer rates the interaction, the answer is saved on the Case and Contact, and a low score goes to an owner for follow-up")

def case_close_checklist():
    Wd,H=1000,470; b=t(40,50,"Go-live checklist: CSAT on case close",22,NAVY,800)+t(40,78,"Run it in a sandbox first, then repeat in production",15,MUTE,500)
    cols=[("BEFORE YOU BUILD",["List every status that means closed","Pick the record types and queues in scope","Exclude spam, duplicates and internal cases","Agree who owns a low score, and how fast"]),
          ("TEST IN A SANDBOX",["Close a test case: one survey arrives","Edit the closed case: no second survey","Answer it: the score shows on the Case","Give a low score: the owner is notified"])]
    for k,(h,items) in enumerate(cols):
        x=40+k*470; b+=r(x,104,450,330,16,"#EAF1FF" if k else W,BLUE if k else LINE,2.5 if k else 1.5)+t(x+24,140,h,13,BLUE if k else MUTE,800)
        for i,it in enumerate(items):
            y=176+i*64; b+=r(x+24,y,30,30,7,W,BLUE,2.5)+f'<path d="M{x+31} {y+15} l7 7 l12 -14" fill="none" stroke="{GRN}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'+t(x+70,y+21,it,15.5,NAVY,600)
    return svg(Wd,H,b,"Go-live checklist. Before you build: list closed statuses, pick record types and queues, exclude spam and internal cases, agree who owns a low score. Test in a sandbox: one survey per closed case, no second survey on edit, score shows on the Case, low score notifies the owner")


def detractor_case():
    return flow("Working a detractor (P1) case","The daily routine for service managers and case owners",
        [("Pick it up","Open the P1 case|from your queue|or list view",""),("Read first","Score, comment|and history on|the record",""),("Reach out","Call or email|within one|business day",""),("Fix it","Solve or explain,|and agree the|next step",""),("Close loop","Record what you|did, then close|the case","")],
        "Five steps to work a detractor case: pick it up, read the score and comment on the record, reach out within one business day, fix or explain, record what you did and close the case")

FIGS={"detractor-case":detractor_case,"case-close-flow":case_close_flow,"case-close-checklist":case_close_checklist,"business-case-flow":business_case,"partner-tracks":partner_tracks,"switch-timeline":timeline,"native-vs-boltOn":architecture,"service-loop":loop,"score-routing":routing,"closed-loop-dashboard":dashboard}
if __name__=="__main__":
    for k,f in FIGS.items(): open(os.path.join(OUT,k+".svg"),"w").write(f()); print(k)
