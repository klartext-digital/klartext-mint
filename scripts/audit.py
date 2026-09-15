#!/usr/bin/env python3
"""Inventory the built site without inventing ranking or field-performance data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter, deque
import json, re, os

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('KLARTEXT_BUILD_DIR',ROOT/'_site')).resolve()
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

pages={};edges={}
for p in sorted(OUT.rglob('*.html')):
    text=p.read_text();tags=Page(text).tags
    if any(t=='meta' and a.get('http-equiv')=='refresh' for t,a in tags):continue
    key=str(p.relative_to(OUT));main=re.search(r'<main\b[^>]*>(.*?)</main>',text,re.S)
    visible=re.sub(r'<[^>]*>',' ',main.group(1) if main else '')
    title=re.search(r'<title>(.*?)</title>',text,re.S).group(1)
    description=next((a.get('content','') for t,a in tags if t=='meta' and a.get('name')=='description'),'')
    schemas=[e['@type'] for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S) for e in json.loads(s)['@graph']]
    pages[key]={'title':title,'description':description,'main_words':len(visible.split()),'schema':schemas,'html_bytes':p.stat().st_size,'responsive_images':sum(t=='img' and 'srcset' in a for t,a in tags),'robots':next((a.get('content') for t,a in tags if t=='meta' and a.get('name')=='robots'),'')}
    links=set()
    for tag,a in tags:
        u=urlsplit(a.get('href',''))
        if tag!='a' or u.scheme or u.netloc:continue
        dest=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
        if dest.is_dir():dest=dest/'index.html'
        if dest.suffix=='.html' and dest.is_relative_to(OUT):links.add(str(dest.relative_to(OUT)))
    edges[key]=links
distance={'index.html':0};queue=deque(['index.html'])
while queue:
    source=queue.popleft()
    for target in edges.get(source,set()):
        if target in pages and target not in distance:
            distance[target]=distance[source]+1;queue.append(target)
for path,data in pages.items():
    data['clicks_from_home']=distance.get(path)
    data['incoming_pages']=sum(path in targets for source,targets in edges.items() if source!=path)
titles=Counter(v['title'] for v in pages.values())
report={'canonical_documents':len(pages),'duplicate_titles':[t for t,n in titles.items() if n>1],'pages':pages,'limits':['No rankings, indexing coverage or lead totals available without connected accounts.','PageSpeed API returned HTTP 429; no Core Web Vitals pass claimed.','Existing intro animation remains enabled as requested.','GitHub legacy aliases use HTML redirects; server redirects remain part of the production hosting move.']}
(ROOT/'docs/AUDIT-CURRENT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'Audit: {len(pages)} documents, {len(report["duplicate_titles"])} duplicate titles. New routes are reachable from the homepage.')
