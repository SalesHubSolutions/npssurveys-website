"""One light trust row for every branded email (replaces the old 3-cell row and the dark proof strip).
Cells: Salesforce AppExchange + 5.0 | Security reviewed, 100% native | Works with Slack, Teams, Google (gov: Carahsoft / CoreTrust)."""
SITE = "https://www.npssurveys.com"
LIST = "https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000FtRTKUA3&amp;utm_source=drip&amp;utm_medium=email&amp;utm_campaign=trust_row"
F = "font-family:Arial,Helvetica,sans-serif;"
def ic(name, w, h, alt):
    return f'<img src="{SITE}/brand/proof/icon-{name}.png" width="{w}" height="{h}" alt="{alt}" style="display:inline-block;border:0;vertical-align:middle;">'
def trust_row(gov=False):
    c1 = (ic("salesforce", 40, 28, "Salesforce"), "Salesforce AppExchange", '<span style="color:#002FA7;letter-spacing:1px;">&#9733;&#9733;&#9733;&#9733;&#9733;</span> Rated 5.0')
    c2 = (ic("check", 28, 28, ""), "Security reviewed", "100% native to Salesforce,<br>data stays in your org")
    if gov:
        c3 = (ic("contract", 28, 28, ""), "Buy through Carahsoft", "CoreTrust contract<br>24COR-018GR")
    else:
        c3 = (ic("slack", 18, 18, "Slack") + "&nbsp;" + ic("teams", 18, 18, "Microsoft Teams") + "&nbsp;" + ic("google", 18, 18, "Google"), "Works with", "Slack, Teams and<br>Google reviews")
    tds = ""
    for i, (icon, b, s) in enumerate([c1, c2, c3]):
        mid = "border-left:1px solid #E3E8F4;border-right:1px solid #E3E8F4;" if i == 1 else ""
        tds += (f'<td width="33%" align="center" valign="top" style="padding:16px 6px;{F}font-size:12px;line-height:17px;color:#5A6787;{mid}">'
                f'<a href="{LIST}" style="text-decoration:none;color:#5A6787;"><div style="height:28px;line-height:28px;">{icon}</div>'
                f'<b style="display:block;font-size:14px;line-height:19px;color:#0F1A3D;padding-top:8px;">{b}</b>{s}</a></td>')
    return (f'<tr><td style="background:#ffffff;padding:28px 32px 0 32px;" class="trust-row"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-top:1px solid #E3E8F4;border-bottom:1px solid #E3E8F4;"><tr>{tds}</tr></table></td></tr>\n')
