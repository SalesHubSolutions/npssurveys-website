"""Brand SVG figures for Insights posts. Run: python3 tools/figures.py  (writes content/figures/*.svg)
Embed in a post with {{FIG:name|Caption text}}."""
import os, math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(ROOT,"content/figures"); os.makedirs(OUT,exist_ok=True)
NAVY="#0C184A"; BLUE="#1E54E8"; DEEP="#052CA0"; SKY="#DCE7FF"; TINT="#F4F7FF"; LINE="#DCE4F7"; MUTE="#5E6B98"; SOFT="#3B4877"
RED="#EB5757"; AMB="#E9A52B"; GRN="#23A96A"; YEL="#FFE443"; W="#FFFFFF"
F='font-family="Inter, Arial, sans-serif"'
def t(x,y,s,size=16,fill=NAVY,w=600,a="start"): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{a}" {F}>{s}</text>'
def r(x,y,w,h,rx=12,fill=W,stroke=LINE,sw=1.5): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def arrow(x1,y1,x2,y2,c=BLUE,dash=False): 
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="3" marker-end="url(#ah)"{" stroke-dasharray=\"7 7\"" if dash else ""}/>'
DEFS=f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{BLUE}"/></marker></defs>'
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
    b+=r(530,160,410,120,14,"#EAF1FF",BLUE)+t(546,182,"Inside your Salesforce org",12,BLUE,800)
    steps=[("Event","sends survey"),("Answer","on record"),("Low score","opens case"),("Dashboard","CX360")]
    for i,(a,c) in enumerate(steps):
        x=546+i*98; b+=r(x,196,86,68,10,W,LINE)+t(x+43,224,a,13,NAVY,800,"middle")+t(x+43,244,c,11,MUTE,600,"middle")
        if i<3: b+=arrow(x+86,230,x+96,230)
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

FIGS={"switch-timeline":timeline,"native-vs-boltOn":architecture,"service-loop":loop,"score-routing":routing,"closed-loop-dashboard":dashboard}
if __name__=="__main__":
    for k,f in FIGS.items(): open(os.path.join(OUT,k+".svg"),"w").write(f()); print(k)
