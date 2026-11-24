# npssurveys.com

Website for **NPS Survey CX OS by SalesHub**, the customer experience operating system for Salesforce.

- Hosted on GitHub Pages; domain `www.npssurveys.com` (registered at GoDaddy).
- `index.html` is the whole site (hash-routed sections: platform, industries, public sector, learn, resources, reviews, pricing, demo).
- `files/` holds downloads and videos; `pricing/`, `demo/`, `solutions/*` etc. redirect old Next.js URLs to the matching section.
- Every change is a commit, so any version can be restored.

## Website chat
- `assets/chat/chat.js` is the chat assistant, loaded on every page with one line before `</body>`:
  `<script src="/assets/chat/chat.js" defer></script>` (other sites use the full `https://www.npssurveys.com/assets/chat/chat.js`).
- It answers from its built-in knowledge base (keep prices and facts in step with the site), books demos with the Calendly calendar and sends "talk to a person" requests to Salesforce as web leads (source Web, description starts "Website chat lead").
- AI answers: deploy `worker/chat-worker.js` as a Cloudflare Worker with the secret `ANTHROPIC_API_KEY`, then add `data-api="https://<worker-url>"` to the script tag. If the Worker is down, the chat falls back to the knowledge base.
