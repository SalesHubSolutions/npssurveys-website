#!/usr/bin/env python3
"""Make /public-sector/ a real, linkable page (for Carahsoft and search) from the site app.

It is the homepage app opened on the public sector view, with its own title,
description and canonical URL. Re-run after any change to index.html.
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
title = 'NPS Survey CX OS for Government | State, Local, Federal and Defense on Salesforce'
desc = ('Resident and employee experience inside Salesforce for state and local government, federal civilian agencies '
        'and defense. Buy through Carahsoft on the CoreTrust cooperative contract (24COR-018GR) or start on AppExchange.')
s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1, flags=re.S)
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s, count=1)
s = s.replace('<link rel="canonical" href="https://www.npssurveys.com/">',
              '<link rel="canonical" href="https://www.npssurveys.com/public-sector/">', 1)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + title, s, count=1)
s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + desc, s, count=1)
s = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>https://www.npssurveys.com/public-sector/', s, count=1)
boot = ('<base href="/"><script>if(!location.hash)history.replaceState(null,"",location.pathname+location.search+"#public-sector")</script>')
s = s.replace('<head>', '<head>' + boot, 1)
os.makedirs(os.path.join(ROOT, 'public-sector'), exist_ok=True)
open(os.path.join(ROOT, 'public-sector', 'index.html'), 'w', encoding='utf-8').write(s)
print('public-sector/index.html written', len(s))
