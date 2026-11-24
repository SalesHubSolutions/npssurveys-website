/*!
 * NPS Survey CX OS website assistant
 * One script tag on any page or any website:
 *   <script src="https://www.npssurveys.com/assets/chat/chat.js" defer></script>
 * Optional AI backend (Cloudflare Worker in /worker): set data-api on the tag, or window.NPSCHAT_API.
 * Without a backend, or if it fails, answers come from the built-in knowledge base below.
 */
(function () {
  "use strict";
  if (window.__npsChat) return;
  window.__npsChat = true;

  var TAG = document.currentScript;
  var API = (TAG && TAG.getAttribute("data-api")) || window.NPSCHAT_API || "";
  var SITE = "https://www.npssurveys.com";
  var DEMO = "https://calendly.com/npssurvey/demo";
  var LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&tab=e&utm_source=" +
    encodeURIComponent(location.hostname || "website") + "&utm_medium=chat&utm_campaign=site_chat";
  var W2L = { oid: "00D6g000001VQio", action: "https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8" };
  var STORE = "npschat.v1";
  var FREEMAIL = /^(gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|aol|icloud|me|mac|proton|protonmail|pm|gmx|mail|yandex|zoho|qq|163|126|fastmail|tutanota|duck|inbox|comcast|att|verizon|mailinator|guerrillamail|10minutemail|tempmail|yopmail)\.[a-z]{2,3}(\.[a-z]{2})?$/i;

  function track(name, params) { try { window.gtag && window.gtag("event", name, params || {}); } catch (_) {} }
  function load() { try { return JSON.parse(sessionStorage.getItem(STORE)) || null; } catch (_) { return null; } }
  function save() { try { sessionStorage.setItem(STORE, JSON.stringify(state)); } catch (_) {} }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function link(href, text) { return '<a href="' + href + '" target="_blank" rel="noopener">' + text + "</a>"; }
  function site(path, text) { return link(SITE + path, text); }

  // ---------- Knowledge base (facts from npssurveys.com; keep in step with the site) ----------
  var KB = [
    { id: "pricing", k: "price pricing cost costs how much plan plans license licence per user seat seats annual year quote budget expensive cheap",
      a: "Pricing is one annual price per Salesforce org, not per user:<ul><li><b>CX Lite</b> $3,500 a year: NPS and CSAT by email and link, close the loop on every low score, standard dashboards, 3 active surveys.</li><li><b>CX Pro</b> $8,500 a year: everything in Lite plus CES, voice of customer and custom forms, review requests, translations, events and QR codes, AI comment summaries, 15 surveys.</li><li><b>CX OS Insights</b> $16,000 a year (recommended): everything in Pro plus Revenue CX, account CX panels, the Command Center, AI digital workers and unlimited surveys.</li></ul>Sign an annual plan by December 31, 2026 and your first year is 20% off. Every plan starts with a 15-day free trial.",
      chips: ["Which plan fits me?", "Start free trial", "Book a demo"] },
    { id: "plans", k: "which plan fit difference differences compare lite pro insights recommended right edition choose",
      a: "A quick guide: <b>CX Lite</b> suits a team starting with NPS or CSAT and follow-up on low scores. <b>CX Pro</b> adds CES, custom forms, translations, QR codes and AI comment summaries. <b>CX OS Insights</b> is for companies tying feedback to renewals and revenue, with account panels, the Command Center and AI digital workers. Not sure? A 30-minute call with our team will point you to the right one.",
      chips: ["Pricing", "Book a demo", "Start free trial"] },
    { id: "offer", k: "discount offer deal promotion year-end 20% sale coupon nonprofit non-profit multi-year",
      a: "Year-end offer for new customers: sign any annual plan by December 31, 2026 and get 20% off year one, no price increase in year two, a done-for-you launch of your first surveys and follow-up rules, and a free move of your survey history from one previous tool. Nonprofit or multi-year pricing? Email " + link("mailto:support@saleshub.info", "support@saleshub.info") + ". " + site("/start/", "See the offer"),
      chips: ["Pricing", "Book a demo"] },
    { id: "trial", k: "trial free try test evaluate evaluation credit card get it now sandbox demo org play",
      a: "Yes. Every install starts with a <b>15-day free trial</b> with every feature on, in your own Salesforce org. No credit card. Choose <b>Get It Now</b> on our AppExchange listing (sandbox or production). Want a look first with nothing installed? <b>Try It</b> on the listing opens a ready-made demo org in your browser. When you pick a plan there is nothing to reinstall.",
      chips: ["How do I install it?", "Start free trial", "Book a demo"] },
    { id: "install", k: "install installation setup set up configure configuration get started onboarding feed tracking error sandbox production package appexchange how long",
      a: "Install takes about 10 minutes: <ol><li>In Setup, turn on <b>Feed Tracking for Case</b> first (the install fails without it).</li><li>Install from AppExchange, sandbox first, then production, with a System Administrator login.</li><li>Open the App Launcher and search for NPS Survey. A guided setup walks you through the rest.</li></ol>We also do a free 30-minute guided setup call with you. Full steps: " + site("/install/", "Install and setup guide"),
      chips: ["Book a guided setup", "Start free trial"] },
    { id: "editions", k: "edition editions essentials professional enterprise unlimited lightning classic requirements require compatible work with license login respondents",
      a: "It works with Salesforce <b>Essentials, Professional, Enterprise and Unlimited</b> editions, in Lightning Experience. People answering your surveys don't need a Salesforce login.",
      chips: ["Start free trial", "Is our data safe?"] },
    { id: "security", k: "security secure safe data privacy where data live store stored leave gdpr hipaa compliance compliant review security review native",
      a: "NPS Survey CX OS is 100% native to Salesforce, so survey answers stay in your own Salesforce org and never leave it. The app has passed Salesforce's AppExchange security review. For a security questionnaire or specific compliance needs, our team can help: " + link("mailto:support@saleshub.info", "support@saleshub.info") + ".",
      chips: ["Talk to a person", "Book a demo"] },
    { id: "what", k: "what is it does do product overview about explain how works work platform cx os features capabilities",
      a: "NPS Survey CX OS runs your customer feedback inside Salesforce. You send NPS, CSAT and CES surveys, and every low score turns into a follow-up with an owner and a due date, so every unhappy customer gets a call back. AI reads every comment, dashboards show your scores by team, account and touchpoint, and happy customers get asked for a review. " + site("/tour/", "Take the product tour"),
      chips: ["Close the loop", "AI features", "Watch the demo"] },
    { id: "loop", k: "close the loop closed loop detractor detractors follow up follow-up unhappy low score case owner callback call back alert escalate",
      a: "When a customer gives a low score, four things happen at once: a follow-up is opened with an owner and a due time, the team is alerted, the customer's record shows the score, and the follow-up stays on the close-the-loop board until someone logs the call and the outcome. Nothing gets lost on page 4 of a report. " + site("/close-the-loop/", "How close the loop works"),
      chips: ["Watch the demo", "Book a demo"] },
    { id: "ai", k: "ai artificial intelligence gpt agent agents digital worker workers summarize summary sentiment themes draft drafts churn triage automation",
      a: "AI is built in: it drafts a survey from one sentence, reads every comment for themes, sentiment and churn risk, drafts a reply in the Feedback Inbox, and AI digital workers keep the follow-up going after your team goes home. AI comment summaries come with CX Pro; digital workers with CX OS Insights.",
      chips: ["Watch the demo", "Pricing"] },
    { id: "channels", k: "channel channels email link qr code kiosk translations translation language languages multilingual spanish event events check-in registration send sending reminders reminder",
      a: "Surveys go out by email and link, QR codes and kiosks, with automatic reminders and rules so customers aren't over-surveyed. Surveys can be translated so each region answers in its own language, and there is event registration and QR check-in too. Translations, events and QR are in CX Pro and above.",
      chips: ["Pricing", "Book a demo"] },
    { id: "triggers", k: "trigger triggers automate automatic case close closed opportunity won deal record change flow when send csat after case",
      a: "Surveys can send themselves when something happens in Salesforce: a case closes, a deal is won, or any record changes. For example, a CSAT survey after every closed case. We set up your first one with you on a 30-minute call.",
      chips: ["Book a guided setup", "Start free trial"] },
    { id: "switch", k: "switch switching migrate migration move import getfeedback delighted qualtrics medallia surveymonkey feedback management replace replacing retire retires history",
      a: "Yes, you can switch. The built-in import wizard brings over your past responses, and we help you move them during setup (free with the year-end offer). GetFeedback retires on December 31, 2026, so many teams are moving now. " + site("/insights/replace-getfeedback-salesforce/", "Replacing GetFeedback in Salesforce"),
      chips: ["Book a demo", "Talk to a person"] },
    { id: "cx360", k: "without salesforce no salesforce hubspot dynamics zoho other crm standalone cx360 not on salesforce",
      a: "Not on Salesforce? <b>CX360 Standalone</b> is our version that works with any CRM, or none, from the same team. " + link("https://app.npssurveys.com/?utm_source=" + encodeURIComponent(location.hostname || "website") + "&utm_medium=chat&utm_campaign=site_chat", "Explore CX360 Standalone"),
      chips: ["Talk to a person"] },
    { id: "gov", k: "government public sector state local federal agency agencies defense city county carahsoft procurement contract vehicle",
      a: "We work with state, local, federal and defense teams on Salesforce, and government buyers can purchase through Carahsoft. " + site("/public-sector/", "NPS Survey CX OS for government"),
      chips: ["Talk to a person", "Book a demo"] },
    { id: "pay", k: "pay payment invoice purchase order po buy card credit stripe billing order form procurement",
      a: "You can buy by card (processed securely by Stripe) and we switch your license from trial to paid within one business day. Prefer an invoice and order form? Email " + link("mailto:support@saleshub.info", "support@saleshub.info") + ". " + site("/install/#buy", "Buy a plan"),
      chips: ["Pricing", "Talk to a person"] },
    { id: "support", k: "support help contact phone call email reach person human talk someone sales team speak",
      a: "You can reach the SalesHub team by email at " + link("mailto:support@saleshub.info", "support@saleshub.info") + " (answered within one business day) or by phone at " + link("tel:+18337332468", "1 (833) 733-2468") + " in US business hours. Or leave your details here and we'll reply.",
      chips: ["Talk to a person", "Book a demo"] },
    { id: "demo", k: "demo demonstration see it show me watch video walkthrough meeting webinar recording",
      a: "Two ways to see it: watch the 3½-minute recorded demo (" + site("/demo/", "watch now") + "), or book a 30-minute live demo with our team, shown on your own use case. There is also a free live session on Thursday, December 3, 2026 at 12:00 PM ET: " + site("/webinar/", "save a seat") + ".",
      chips: ["Book a demo", "Watch the demo"] },
    { id: "reviews", k: "reviews rating rated customers who uses references case study trust",
      a: "NPS Survey CX OS is rated 5.0 on Salesforce AppExchange, and it is made by SalesHub, LLC in Marietta, Georgia. You can read the reviews on our " + link(LIST, "AppExchange listing") + ".",
      chips: ["Start free trial", "Book a demo"] },
    { id: "roi", k: "roi return value business case cfo justify savings churn revenue worth",
      a: "Build your business case in about a minute with the " + site("/roi/", "ROI calculator") + ", or grab the free CFO business case PDF from our resources.",
      chips: ["Book a demo", "Pricing"] },
    { id: "sites", k: "experience cloud community site sites guest public page survey page link where answered",
      a: "Customers answer surveys on a secure page served from your own Salesforce org, so they don't need a login. The guided setup creates and connects it for you, or we do it with you on a free 30-minute setup call.",
      chips: ["Book a guided setup", "How do I install it?"] }
  ];

  var SYN = { cost: "price", costs: "price", pricey: "price", much: "price", charge: "price", subscription: "price",
    setup: "install", onboard: "install", installing: "install", trialing: "trial", free: "trial",
    detractors: "detractor", followup: "follow", agents: "ai", bots: "ai", migrate: "switch", import: "switch",
    meeting: "demo", call: "support", human: "support", person: "support" };

  function words(t) { return (t.toLowerCase().match(/[a-z0-9%-]+/g) || []).map(function (w) { return SYN[w] || w; }); }
  var STOP = /^(the|a|an|is|are|do|does|i|we|you|it|to|of|for|and|or|in|on|with|can|my|our|me|how|what|about|this|that|be|have|has|any|your|there)$/;

  function answer(text) {
    var t = text.toLowerCase();
    if (/\b(book|schedule|set up a call|meeting|calendly)\b.*\b(demo|call|meeting|time)\b|^book a demo$|^book a guided setup$/.test(t)) return { action: "book" };
    if (/talk to a person|speak to (a|someone)|human|real person|contact me|call me|email me|sales rep/.test(t)) return { action: "lead" };
    if (/^start free trial$/.test(t)) return { action: "trial" };
    if (/^watch the demo$/.test(t)) return { html: KB.filter(function (e) { return e.id === "demo"; })[0].a, chips: ["Book a demo"] };
    var ws = words(text).filter(function (w) { return !STOP.test(w); });
    var best = null, bestScore = 0;
    KB.forEach(function (e) {
      var keys = " " + e.k + " ", s = 0;
      ws.forEach(function (w) { if (keys.indexOf(" " + w + " ") >= 0) s += 2; else if (w.length > 4 && keys.indexOf(w.slice(0, 5)) >= 0) s += 1; });
      if (e.k.indexOf(t.trim()) >= 0 && t.trim().length > 3) s += 3;
      if (s > bestScore) { best = e; bestScore = s; }
    });
    if (best && bestScore >= 2) return { html: best.a, chips: best.chips, topic: best.id };
    return { html: "I don't have a sure answer to that one, and I'd rather not guess. Our team can answer it properly: leave your details and we'll reply within one business day, or book a 30-minute call.", chips: ["Talk to a person", "Book a demo", "Pricing"], unknown: true };
  }

  // ---------- State ----------
  var state = load() || { open: false, msgs: [], lead: null, greeted: false };

  // ---------- Styles ----------
  var css = "" +
    ".npc,.npc *{box-sizing:border-box}" +
    ".npc{--b:#002FA7;--bd:#00227A;--ink:#0F1A3D;--mute:#5A6787;--line:#DCE3F5;--tint:#F4F7FF;font:15px/1.5 'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:var(--ink);position:fixed;right:20px;bottom:20px;z-index:2147483000}" +
    ".npc-l{width:60px;height:60px;border-radius:50%;border:0;background:var(--b);color:#fff;cursor:pointer;display:grid;place-items:center;box-shadow:0 8px 24px rgba(0,47,167,.35);transition:transform .15s}" +
    ".npc-l:hover{transform:scale(1.05)}.npc-l:focus-visible,.npc button:focus-visible,.npc a:focus-visible,.npc input:focus-visible,.npc textarea:focus-visible{outline:3px solid #8FB0FF;outline-offset:2px}" +
    ".npc-l svg{width:30px;height:30px}" +
    ".npc-tip{position:absolute;right:72px;bottom:10px;background:#fff;color:var(--ink);border:1px solid var(--line);border-radius:12px;padding:9px 12px;white-space:nowrap;box-shadow:0 6px 18px rgba(15,26,61,.12);font-size:14px;cursor:pointer}" +
    ".npc-tip b{color:var(--b)}" +
    ".npc-p{position:absolute;right:0;bottom:76px;width:380px;max-width:calc(100vw - 32px);height:600px;max-height:calc(100vh - 110px);background:#fff;border-radius:16px;box-shadow:0 18px 50px rgba(15,26,61,.25);display:flex;flex-direction:column;overflow:hidden;border:1px solid var(--line)}" +
    ".npc-p[hidden],.npc-tip[hidden]{display:none}" +
    ".npc-h{background:#071338;color:#fff;padding:12px 14px 12px 18px;display:flex;align-items:center;gap:10px}" +
    ".npc-hero{display:flex;align-items:center;gap:14px;padding:18px 18px 20px;color:#fff;background:radial-gradient(90% 120% at 15% 50%,rgba(61,107,240,.55),transparent 60%),linear-gradient(180deg,#071338,#0A1F66)}" +
    ".npc-hero b{display:block;font:600 18px/1.2 'IBM Plex Serif',Georgia,serif}.npc-hero span{display:block;font-size:13px;line-height:1.45;color:rgba(255,255,255,.8);margin-top:4px}" +
    ".npc-orb{position:relative;flex:none;width:62px;height:62px;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 35% 30%,#3D6BF0,#002FA7 60%,#00227A);box-shadow:0 0 0 6px rgba(61,107,240,.2),0 0 40px 8px rgba(61,107,240,.55)}" +
    ".npc-orb svg{width:30px;height:30px}.npc-orb::after{content:'';position:absolute;inset:-12px;border-radius:50%;border:1px solid rgba(143,176,255,.45);animation:npcp 3.6s ease-out infinite}" +
    "@keyframes npcp{0%{transform:scale(.85);opacity:.9}100%{transform:scale(1.3);opacity:0}}@media (prefers-reduced-motion:reduce){.npc-orb::after{animation:none}}" +
    ".npc.talked .npc-hero{display:none}" +
    ".npc-h svg{width:28px;height:28px;flex:none}.npc-h .npc-t{flex:1;min-width:0}.npc-h b{display:block;font-size:15px;font-weight:600}.npc-h span{font-size:12.5px;opacity:.85}" +
    ".npc-x{background:transparent;border:0;color:#fff;width:34px;height:34px;border-radius:8px;cursor:pointer;font-size:22px;line-height:1}.npc-x:hover{background:rgba(255,255,255,.15)}" +
    ".npc-m{flex:1;overflow-y:auto;padding:16px;background:var(--tint);display:flex;flex-direction:column;gap:10px}" +
    ".npc-b{max-width:88%;padding:10px 13px;border-radius:14px;background:#fff;border:1px solid var(--line);word-wrap:break-word}" +
    ".npc-b.u{align-self:flex-end;background:var(--b);color:#fff;border-color:var(--b)}" +
    ".npc-b a{color:var(--b);font-weight:600}.npc-b.u a{color:#fff}.npc-b ul,.npc-b ol{margin:6px 0 2px;padding-left:20px}.npc-b li{margin:3px 0}" +
    ".npc-c{display:flex;flex-wrap:wrap;gap:6px}" +
    ".npc-c button{border:1px solid var(--b);background:#fff;color:var(--b);border-radius:999px;padding:6px 12px;font:inherit;font-size:13.5px;font-weight:600;cursor:pointer}.npc-c button:hover{background:var(--b);color:#fff}" +
    ".npc-typing{display:inline-flex;gap:4px;padding:12px 14px}.npc-typing i{width:6px;height:6px;border-radius:50%;background:var(--mute);opacity:.5;animation:npcd 1s infinite}.npc-typing i:nth-child(2){animation-delay:.15s}.npc-typing i:nth-child(3){animation-delay:.3s}" +
    "@keyframes npcd{50%{opacity:1;transform:translateY(-2px)}}" +
    "@media (prefers-reduced-motion:reduce){.npc-typing i{animation:none}.npc-l{transition:none}}" +
    ".npc-f{display:flex;gap:8px;padding:10px;border-top:1px solid var(--line);background:#fff}" +
    ".npc-f textarea{flex:1;resize:none;border:1px solid var(--line);border-radius:10px;padding:10px 12px;font:inherit;max-height:96px;color:var(--ink)}" +
    ".npc-f button{border:0;background:var(--b);color:#fff;border-radius:10px;padding:0 14px;font:inherit;font-weight:600;cursor:pointer}" +
    ".npc-foot{font-size:11.5px;color:var(--mute);text-align:center;padding:0 10px 8px;background:#fff}" +
    ".npc-foot a{color:var(--mute)}" +
    ".npc-form{display:grid;gap:8px}.npc-form label{font-size:12.5px;font-weight:600;color:var(--mute)}" +
    ".npc-form input,.npc-form textarea{width:100%;border:1px solid var(--line);border-radius:8px;padding:8px 10px;font:inherit;font-size:14px;color:var(--ink)}" +
    ".npc-form .bad{border-color:#D92D20}.npc-form .er{color:#B42318;font-size:12.5px}" +
    ".npc-form button{border:0;background:var(--b);color:#fff;border-radius:999px;padding:9px 14px;font:inherit;font-weight:600;cursor:pointer}" +
    ".npc-cal{width:100%;height:520px;border:0;border-radius:10px;background:#fff}" +
    ".npc-b.wide{max-width:100%;width:100%;padding:6px}" +
    ".nx-help{display:none!important}" +
    "@media (max-width:720px){body:has(.mcta) .npc:not(.open){bottom:calc(84px + env(safe-area-inset-bottom))}}" +
    "@media (max-width:480px){.npc{right:12px;bottom:12px}.npc-p{position:fixed;inset:0;width:100%;max-width:none;height:100%;max-height:none;border-radius:0;border:0}.npc-tip{display:none}}";

  var LOOP = '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M31.07 77.03 A33 33 0 1 1 68.93 77.03" fill="none" stroke="currentColor" stroke-width="14" stroke-linecap="round"/><circle cx="50" cy="83" r="7.5" fill="currentColor"/></svg>';

  // ---------- DOM ----------
  var root, panel, list, input, tip;
  function build() {
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    root = document.createElement("div"); root.className = "npc";
    root.innerHTML =
      '<div class="npc-tip" hidden role="button" tabindex="0">Questions? <b>Ask Iris</b>, our AI agent</div>' +
      '<section class="npc-p" hidden role="dialog" aria-label="Chat with Iris, the NPS Survey CX OS AI agent">' +
      '<div class="npc-h"><div class="npc-t"><b>Iris</b><span>AI CX Agent · NPS Survey CX OS</span></div><button class="npc-x" type="button" aria-label="Close chat">&times;</button></div>' +
      '<div class="npc-hero" aria-hidden="true"><div class="npc-orb">' + LOOP + '</div><div><b>Hi, I\'m Iris.</b><span>The AI agent inside NPS Survey CX OS. Ask me anything, or let me book you time with our team.</span></div></div>' +
      '<div class="npc-m" aria-live="polite"></div>' +
      '<form class="npc-f"><label for="npc-in" style="position:absolute;left:-9999px">Type your question</label><textarea id="npc-in" rows="1" placeholder="Ask Iris a question" maxlength="600"></textarea><button type="submit">Send</button></form>' +
      '<div class="npc-foot">Iris is an AI and can make mistakes. By continuing, you agree to our ' + link("https://saleshub.info/privacy-policy", "privacy policy") + '. Conversations may be saved to help us follow up.</div>' +
      '</section>' +
      '<button class="npc-l" type="button" aria-label="Open chat" aria-expanded="false">' + LOOP + '</button>';
    document.body.appendChild(root);
    panel = root.querySelector(".npc-p"); list = root.querySelector(".npc-m"); input = root.querySelector("textarea"); tip = root.querySelector(".npc-tip");
    var launcher = root.querySelector(".npc-l");
    launcher.addEventListener("click", function () { toggle(); });
    tip.addEventListener("click", function () { toggle(true); });
    tip.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(true); } });
    root.querySelector(".npc-x").addEventListener("click", function () { toggle(false); });
    root.querySelector(".npc-f").addEventListener("submit", function (e) { e.preventDefault(); send(input.value); });
    input.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(input.value); } });
    input.addEventListener("input", function () { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 96) + "px"; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) toggle(false); });
    list.addEventListener("click", function (e) {
      var c = e.target.closest("button[data-chip]"); if (c) { send(c.getAttribute("data-chip")); }
    });
    state.msgs.forEach(function (m) { render(m, true); });
    if (state.msgs.some(function (m) { return m.who === "u"; })) root.classList.add("talked");
    if (state.open) toggle(true, true);
    var seen = false; try { seen = sessionStorage.getItem(STORE + ".tip") === "1"; } catch (_) {}
    if (!seen && !state.open) setTimeout(function () { if (panel.hidden) { tip.hidden = false; try { sessionStorage.setItem(STORE + ".tip", "1"); } catch (_) {} } }, 9000);
    // Any element with data-open-chat opens the assistant (e.g. a "Chat with us" button on the page).
    document.addEventListener("click", function (e) { var t = e.target.closest && e.target.closest("[data-open-chat]"); if (t) { e.preventDefault(); toggle(true); } });
  }

  function toggle(force, quiet) {
    var open = typeof force === "boolean" ? force : panel.hidden;
    panel.hidden = !open; tip.hidden = true;
    root.querySelector(".npc-l").setAttribute("aria-expanded", String(open));
    state.open = open; save();
    if (open) {
      if (!state.greeted) {
        state.greeted = true;
        bot({ html: "Hi, I'm Iris, the AI agent inside NPS Survey CX OS. I can answer questions about the platform, pricing and setup, or connect you with our team. What would you like to know?", chips: ["How does it work?", "Pricing", "Book a demo", "Talk to a person"] });
      }
      if (!quiet) { track("chat_open", { page: location.pathname }); setTimeout(function () { input.focus(); }, 50); }
      list.scrollTop = list.scrollHeight;
    }
  }

  function render(m, restoring) {
    var b = document.createElement("div");
    if (m.kind === "form") { b.className = "npc-b"; b.appendChild(leadForm(m)); }
    else if (m.kind === "cal") { b.className = "npc-b wide"; b.innerHTML = calendar(); }
    else { b.className = "npc-b" + (m.who === "u" ? " u" : ""); b.innerHTML = m.who === "u" ? esc(m.text) : m.html; }
    list.appendChild(b);
    if (m.chips && m.chips.length && !restoring) {
      var c = document.createElement("div"); c.className = "npc-c";
      c.innerHTML = m.chips.map(function (x) { return '<button type="button" data-chip="' + esc(x) + '">' + esc(x) + "</button>"; }).join("");
      list.appendChild(c);
    }
    list.scrollTop = list.scrollHeight;
  }
  function push(m) { state.msgs.push(m); if (state.msgs.length > 60) state.msgs = state.msgs.slice(-60); save(); render(m); }
  function bot(m) { m.who = "b"; push(m); }

  function typing(on) {
    var t = list.querySelector(".npc-typing");
    if (on && !t) { t = document.createElement("div"); t.className = "npc-b npc-typing"; t.innerHTML = "<i></i><i></i><i></i>"; t.setAttribute("aria-label", "Typing"); list.appendChild(t); list.scrollTop = list.scrollHeight; }
    if (!on && t) t.remove();
  }

  // ---------- Conversation ----------
  var busy = false;
  function send(text) {
    text = String(text || "").trim(); if (!text || busy) return;
    input.value = ""; input.style.height = "auto";
    list.querySelectorAll(".npc-c").forEach(function (c) { c.remove(); });
    root.classList.add("talked");
    push({ who: "u", text: text });
    var local = answer(text);
    if (local.action) return act(local.action);
    if (!API) { busy = true; typing(true); setTimeout(function () { typing(false); busy = false; reply(local); }, 450); return; }
    busy = true; typing(true);
    var hist = state.msgs.filter(function (m) { return m.who === "u" || (m.who === "b" && m.html); }).slice(-12).map(function (m) {
      return { role: m.who === "u" ? "user" : "assistant", content: m.who === "u" ? m.text : m.html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() };
    });
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { ctl && ctl.abort(); }, 20000);
    fetch(API, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist, page: location.href }), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        clearTimeout(timer); typing(false); busy = false;
        if (!d || !d.reply) throw new Error("empty");
        bot({ html: format(d.reply), chips: d.chips || defaultChips(d.action) });
        if (d.action) act(d.action, true);
      })
      .catch(function () { clearTimeout(timer); typing(false); busy = false; reply(local); });
  }

  function defaultChips(action) { return action ? [] : ["Book a demo", "Pricing", "Talk to a person"]; }

  // Turns the AI's plain text (with **bold**, - lists and bare links) into safe HTML.
  function format(t) {
    var s = esc(t);
    s = s.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    s = s.replace(/(https?:\/\/[^\s<)]+[^\s<).,;:!?])/g, function (u) { return '<a href="' + u + '" target="_blank" rel="noopener">' + u.replace(/^https?:\/\/(www\.)?/, "").replace(/\?.*$/, "") + "</a>"; });
    s = s.replace(/([\w.+-]+@[\w-]+\.[\w.]+)/g, '<a href="mailto:$1">$1</a>');
    var lines = s.split(/\n/), out = [], inList = false;
    lines.forEach(function (l) {
      var m = l.match(/^\s*(?:[-*]|\d+\.)\s+(.*)/);
      if (m) { if (!inList) { out.push("<ul>"); inList = true; } out.push("<li>" + m[1] + "</li>"); }
      else { if (inList) { out.push("</ul>"); inList = false; } if (l.trim()) out.push(l + "<br>"); }
    });
    if (inList) out.push("</ul>");
    return out.join("").replace(/(<br>)+$/, "");
  }

  function reply(r) {
    if (r.unknown) track("chat_unanswered", { q: (state.msgs[state.msgs.length - 1] || {}).text || "" });
    else if (r.topic) track("chat_answer", { topic: r.topic });
    bot({ html: r.html, chips: r.chips });
  }

  function act(action, fromAi) {
    if (action === "book") {
      if (!fromAi) bot({ html: "Here's our calendar. Pick a time that suits you for a 30-minute demo with the SalesHub team. You'll get a calendar invite with a video link." });
      push({ kind: "cal", who: "b" });
      track("chat_book_open", { page: location.pathname });
    } else if (action === "lead") {
      if (!fromAi) bot({ html: "Happy to connect you with our team. Leave your details and we'll reply within one business day." });
      push({ kind: "form", who: "b" });
    } else if (action === "trial") {
      bot({ html: "Start your 15-day free trial from Salesforce AppExchange: choose <b>Get It Now</b> on " + link(LIST + "&utm_content=chat_trial", "our listing") + ". Every feature is on, no credit card. Turn on Feed Tracking for Case in Setup first. " + site("/install/", "Install guide"), chips: ["How do I install it?", "Book a guided setup"] });
      track("chat_trial_click", {});
    }
  }

  function calendar() {
    var q = "hide_gdpr_banner=1&primary_color=002FA7";
    if (state.lead) q += "&name=" + encodeURIComponent(state.lead.name) + "&email=" + encodeURIComponent(state.lead.email);
    return '<iframe class="npc-cal" title="Book a demo with SalesHub" src="' + DEMO + "?" + q + '" loading="lazy"></iframe>' +
      '<div style="padding:6px 6px 2px;font-size:13px">Calendar not loading? ' + link(DEMO, "Open it in a new tab") + "</div>";
  }

  // ---------- Lead capture (sent to Salesforce as a web lead, source Web) ----------
  function leadForm(m) {
    var f = document.createElement("form"); f.className = "npc-form"; f.noValidate = true;
    if (m.sent) { f.innerHTML = "<div><b>Thanks, we've got it.</b> We'll reply within one business day.</div>"; return f; }
    var id = "npcf" + Math.random().toString(36).slice(2, 7);
    f.innerHTML =
      '<label for="' + id + 'n">Your name</label><input id="' + id + 'n" name="name" autocomplete="name" required>' +
      '<label for="' + id + 'e">Work email</label><input id="' + id + 'e" name="email" type="email" autocomplete="email" required>' +
      '<label for="' + id + 'c">Company</label><input id="' + id + 'c" name="company" autocomplete="organization" required>' +
      '<label for="' + id + 'q">How can we help? (optional)</label><textarea id="' + id + 'q" name="q" rows="2"></textarea>' +
      '<div class="er" hidden></div><button type="submit">Send to the team</button>' +
      '<div style="font-size:12px;color:#5A6787">We only use this to reply about NPS Survey CX OS.</div>';
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var g = function (n) { return (f.querySelector('[name="' + n + '"]').value || "").trim(); };
      var name = g("name"), email = g("email"), company = g("company"), er = f.querySelector(".er"), bad = [];
      f.querySelectorAll("input").forEach(function (i) { i.classList.remove("bad"); });
      if (name.length < 2) bad.push("name");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || FREEMAIL.test(email.split("@").pop())) bad.push("email");
      if (company.length < 2) bad.push("company");
      if (bad.length) {
        bad.forEach(function (n) { f.querySelector('[name="' + n + '"]').classList.add("bad"); });
        er.hidden = false; er.textContent = bad.indexOf("email") >= 0 ? "Please use your work email (not Gmail, Yahoo, Outlook or similar)." : "Please fill in your name and company.";
        return;
      }
      var parts = name.split(/\s+/), first = parts.length > 1 ? parts.slice(0, -1).join(" ") : "", last = parts[parts.length - 1];
      var convo = state.msgs.filter(function (x) { return x.who === "u" && x.text; }).slice(-8).map(function (x) { return "- " + x.text; }).join("\n");
      var desc = ["Website chat lead", "Question: " + (g("q") || "n/a"), "Page: " + location.href, "Visitor asked:", convo || "n/a"].join("\n").slice(0, 3900);
      postLead({ first_name: first, last_name: last, email: email, company: company, description: desc });
      state.lead = { name: name, email: email };
      m.sent = true; save();
      f.innerHTML = "<div><b>Thanks, " + esc(first || last) + ".</b> We've got it and will reply within one business day.</div>";
      track("generate_lead", { form: "chat" });
      try { window.gtag && window.gtag("event", "ads_conversion_Contact_Us_1"); } catch (_) {}
      bot({ html: "Want to talk sooner? You can pick a time for a 30-minute call now.", chips: ["Book a demo"] });
    });
    return f;
  }

  function postLead(fields) {
    var name = "npcw" + Date.now();
    var ifr = document.createElement("iframe"); ifr.name = name; ifr.hidden = true; ifr.title = "";
    var form = document.createElement("form"); form.method = "POST"; form.action = W2L.action; form.target = name; form.hidden = true;
    var all = { oid: W2L.oid, retURL: SITE + "/thanks.html", lead_source: "Web" };
    Object.keys(fields).forEach(function (k) { all[k] = fields[k]; });
    Object.keys(all).forEach(function (k) { var i = document.createElement("input"); i.type = "hidden"; i.name = k; i.value = all[k]; form.appendChild(i); });
    document.body.appendChild(ifr); document.body.appendChild(form); form.submit();
    setTimeout(function () { form.remove(); ifr.remove(); }, 15000);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build); else build();
})();
