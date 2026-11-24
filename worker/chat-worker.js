/**
 * NPS Survey CX OS website assistant: AI backend (Cloudflare Worker).
 *
 * The website chat (assets/chat/chat.js) works on its own with a built-in knowledge base.
 * This Worker adds real AI answers. It keeps the AI key on the server, only accepts requests
 * from our own websites, limits each visitor, and caps answer length to keep cost low.
 *
 * Secrets / variables (set in Cloudflare, never in the website code):
 *   ANTHROPIC_API_KEY  secret, required
 *   ALLOWED_ORIGINS    optional, comma-separated; defaults below
 *   MODEL              optional, defaults to claude-haiku-5-5 (fast and inexpensive)
 */

const DEFAULT_ORIGINS = [
  "https://www.npssurveys.com", "https://npssurveys.com",
  "https://saleshub.info", "https://www.saleshub.info",
  "https://app.npssurveys.com"
];

const KNOWLEDGE = `
PRODUCT: NPS Survey CX OS by SalesHub, a 100% native Salesforce app on AppExchange. Sends NPS, CSAT and CES surveys and custom forms; every low score becomes a follow-up with an owner and a due date (close the loop). AI drafts surveys from one sentence, reads every comment (themes, sentiment, churn risk), drafts replies in the Feedback Inbox; AI digital workers keep follow-ups going. Dashboards by team, account and touchpoint; Revenue CX shows renewals at risk; account CX panels; CX Command Center; review requests for happy customers; translations; event registration and QR check-in; kiosks and QR codes; automatic reminders and over-survey protection; surveys can send when a case closes, a deal is won or any record changes. Rated 5.0 on AppExchange. Passed the Salesforce AppExchange security review. Survey answers stay in the customer's Salesforce org.
EDITIONS: Salesforce Essentials, Professional, Enterprise, Unlimited, in Lightning Experience. Respondents need no Salesforce login.
PRICING (per Salesforce org, per year, not per user):
- CX Lite $3,500: NPS and CSAT by email and link, close the loop on every low score, standard dashboards, 3 active surveys.
- CX Pro $8,500: everything in Lite plus CES, voice of customer and custom forms, review requests and nurture, translations, events and QR, AI comment summaries, 15 surveys.
- CX OS Insights $16,000 (recommended): everything in Pro plus Revenue CX, account CX panels and Command Center, AI digital workers and Programs, unlimited surveys.
YEAR-END OFFER: new customers who sign an annual plan by December 31, 2026 get 20% off year one ($2,800 / $6,800 / $12,800), no price increase in year two, done-for-you setup of first surveys and follow-up rules, and a free move of survey history from one previous tool. One per org, not combined with other discounts.
TRIAL: every install starts with a 15-day free trial, every feature on, no credit card. "Get It Now" on the AppExchange listing installs it (sandbox or production). "Try It" opens a read-only demo org with nothing installed. A Trialforce trial org with sample data is coming soon. Nothing to reinstall when buying.
INSTALL: turn on Feed Tracking for Case in Setup first (otherwise the install fails with "feedLayout is not supported for this layout"). Install sandbox first, then production, with a System Administrator login; "Install for Admins Only" is the safe default. Takes a few minutes. Then open the App Launcher, search NPS Survey; a guided setup walks through the rest. Current release 2.5.5. Free 30-minute guided setup call available. Guide: https://www.npssurveys.com/install/
BUYING: pay by card (Stripe), license switched from trial to paid within one business day; invoice and order form, nonprofit or multi-year pricing by emailing support@saleshub.info. Government buyers can purchase through Carahsoft.
SWITCHING: built-in import wizard brings past responses; team helps move them. GetFeedback retires December 31, 2026.
NOT ON SALESFORCE: CX360 Standalone works with any CRM or none: https://app.npssurveys.com/
CONTACT: support@saleshub.info (reply within one business day), phone 1 (833) 733-2468 (US business hours). Demo booking: https://calendly.com/npssurvey/demo (30 minutes). Recorded 3.5-minute demo: https://www.npssurveys.com/demo/ . Free live session Thursday, December 3, 2026, 12:00 PM ET: https://www.npssurveys.com/webinar/ . AppExchange listing: https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3 . ROI calculator: https://www.npssurveys.com/roi/ . Government: https://www.npssurveys.com/public-sector/ .
COMPANY: SalesHub, LLC, 1853 Piedmont Rd NE, Suite 301, Marietta, GA 30066.
`;

const SYSTEM = `You are Iris, the AI CX agent of NPS Survey CX OS by SalesHub, chatting with visitors on our website. If asked, say plainly that you are an AI.
Goal: answer questions helpfully and accurately, and help interested visitors take the next step (free trial, demo, or talking to our team).
Rules:
- Use only the facts below. If you don't know, say so plainly and offer to connect them with the team. Never invent features, prices, customers, integrations, certifications or dates.
- Be warm, clear and brief: 1 to 4 short sentences, or a short list. Plain text; **bold** and "- " lists are allowed. No emoji. Never use long dashes. Say "AI", never name AI vendors or models.
- Speak as "we" (the SalesHub team). Don't mention any individual by name.
- Don't discuss competitors negatively. Stay on topic: politely steer unrelated requests back to how we can help.
- Never ask for passwords, card numbers or other sensitive data. For pricing exceptions, contracts or security questionnaires, offer the team.
- When the visitor wants a demo or a meeting, set action "book". When they want a person to contact them, or you can't answer, set action "lead". When they want to start the trial, set action "trial". Otherwise action is null.
Reply ONLY with JSON: {"reply": "...", "action": null | "book" | "lead" | "trial", "chips": ["up to 3 short follow-up suggestions"]}
FACTS:
${KNOWLEDGE}`;

const hits = new Map(); // per-instance soft rate limit: 20 messages per visitor per 10 minutes

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const allowed = (env.ALLOWED_ORIGINS ? env.ALLOWED_ORIGINS.split(",").map(s => s.trim()) : DEFAULT_ORIGINS);
    const cors = {
      "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin"
    };
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (request.method !== "POST") return json({ error: "method" }, 405, cors);
    if (!allowed.includes(origin)) return json({ error: "origin" }, 403, cors);

    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const now = Date.now(), w = (hits.get(ip) || []).filter(t => now - t < 600000);
    if (w.length >= 20) return json({ reply: "You've sent a lot of messages in a short time. Please email support@saleshub.info and our team will help.", action: "lead" }, 200, cors);
    w.push(now); hits.set(ip, w);

    let body;
    try { body = await request.json(); } catch { return json({ error: "bad json" }, 400, cors); }
    const messages = (Array.isArray(body.messages) ? body.messages : [])
      .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
      .slice(-12).map(m => ({ role: m.role, content: m.content.slice(0, 1500) }));
    while (messages.length && messages[0].role !== "user") messages.shift();
    if (!messages.length || messages[messages.length - 1].role !== "user") return json({ error: "no question" }, 400, cors);

    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({
        model: env.MODEL || "claude-haiku-5-5",
        max_tokens: 450,
        system: SYSTEM + "\nVisitor is on: " + String(body.page || "").slice(0, 200),
        messages
      })
    });
    if (!r.ok) return json({ error: "upstream " + r.status }, 502, cors);
    const data = await r.json();
    const text = (data.content || []).map(c => c.text || "").join("").trim();
    let out;
    try { out = JSON.parse(text.slice(text.indexOf("{"), text.lastIndexOf("}") + 1)); } catch { out = { reply: text, action: null }; }
    const action = ["book", "lead", "trial"].includes(out.action) ? out.action : null;
    const reply = String(out.reply || "").replace(/[–—]/g, ", ").slice(0, 1800);
    const chips = Array.isArray(out.chips) ? out.chips.slice(0, 3).map(c => String(c).slice(0, 40)) : undefined;
    return json({ reply, action, chips }, 200, cors);
  }
};

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers: { ...headers, "Content-Type": "application/json" } });
}
