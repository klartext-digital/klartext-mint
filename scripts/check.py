#!/usr/bin/env python3
"""Validate rendered metadata, schema, links, fragments and HTTP responses."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from urllib.request import urlopen
import json,re,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_site'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
errors=[];pages={};http=sys.argv[1] if len(sys.argv)>1 else None
for p in sorted(OUT.rglob('*.html')):
 text=p.read_text();pages[p]=Page(text)
for p,page in pages.items():
 rel=p.relative_to(OUT);text=p.read_text();tags=page.tags
 canonical=[a.get('href') for t,a in tags if t=='link' and a.get('rel')=='canonical']
 if len(canonical)!=1:errors.append(f'{rel}: expected one canonical')
 robots=[a.get('content','') for t,a in tags if t=='meta' and a.get('name')=='robots']
 if len(robots)!=1:errors.append(f'{rel}: expected one robots tag')
 redirect=any(t=='meta' and a.get('http-equiv')=='refresh' for t,a in tags)
 if not redirect and str(rel)!='takt.html':
  if sum(t=='h1' for t,a in tags)!=1:errors.append(f'{rel}: expected one h1')
  if not any(t=='meta' and a.get('name')=='description' and a.get('content') for t,a in tags):errors.append(f'{rel}: missing description')
  schema=re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)
  if not schema:errors.append(f'{rel}: missing schema')
  for block in schema:
   try:
    data=json.loads(block)
    for entity in data['@graph']:
     if entity['@type'] in ['Organization','Person'] and not json.loads((ROOT/'seo.config.json').read_text()).get('organization_verified'):errors.append(f'{rel}: unverified entity')
     if entity['@type']=='BreadcrumbList':
      assert [x['position'] for x in entity['itemListElement']]==list(range(1,len(entity['itemListElement'])+1))
   except Exception as e:errors.append(f'{rel}: invalid schema {e}')
 ids=[a['id'] for t,a in tags if 'id' in a]
 if len(ids)!=len(set(ids)):errors.append(f'{rel}: duplicate IDs')
 for tag,a in tags:
  for attr in ['href','src','poster']:
   if attr not in a:continue
   value=urlsplit(a[attr])
   if value.scheme or value.netloc:continue
   dest=(p.parent/unquote(value.path)).resolve() if value.path else p
   if dest.is_dir():dest=dest/'index.html'
   if not dest.exists():errors.append(f'{rel}: broken {attr} {a[attr]}');continue
   if attr=='href' and value.fragment and dest in pages and not any(x.get('id')==unquote(value.fragment) for t,x in pages[dest].tags):errors.append(f'{rel}: missing anchor {a[attr]}')
 if http:
  path=str(rel)
  if path.endswith('index.html'):path=path[:-10]
  try:
   response=urlopen(http.rstrip('/')+'/'+path)
   if response.status!=200:errors.append(f'{rel}: HTTP {response.status}')
  except Exception as e:errors.append(f'{rel}: HTTP {e}')
sitemap=ET.parse(OUT/'sitemap.xml')
config=json.loads((ROOT/'seo.config.json').read_text())
locs=[n.text for n in sitemap.iter() if n.tag.endswith('}loc')]
expected=[config['base_url'].rstrip('/')+'/'+p for p in config['approved_paths']] if config['indexable'] else []
if sorted(locs)!=sorted(expected):errors.append('Sitemap and indexing approval mismatch')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} HTML pages/redirects; metadata, JSON-LD, all local links/assets/fragments, sitemap'+('; HTTP 200' if http else ''))
