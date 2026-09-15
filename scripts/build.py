#!/usr/bin/env python3
"""Build static Pages output. Source HTML remains editable; _site is generated."""
from pathlib import Path
from html import escape, unescape
from urllib.parse import urljoin, urlsplit, urlunsplit
import json, re, shutil, posixpath, struct

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
CONFIG = json.loads((ROOT / 'seo.config.json').read_text())
BASE = CONFIG['base_url'].rstrip('/') + '/'
assert urlsplit(BASE).scheme == 'https' and not urlsplit(BASE).query and not urlsplit(BASE).fragment
# Canonical paths are relative to BASE, so GitHub project Pages and a future domain both work.
ROUTES = {
 'index.html': '',
 'leistungen/index.html': 'leistungen/',
 'leistungen/branding.html': 'branding/',
 'leistungen/social-media.html': 'social-media/',
 'leistungen/performance.html': 'performance-marketing/',
 'leistungen/email-marketing.html': 'email-marketing/',
 'webdesign/index.html': 'webdesign/',
 'ueber-uns.html': 'ueber-uns/',
 'arbeiten/index.html': 'projekte/',
 'blog/index.html': 'blog/',
 'wissen/index.html': 'wissen/',
 'wissen/website-kosten-schweiz/index.html': 'wissen/website-kosten-schweiz/',
 'recht/impressum.html': 'impressum/',
 'recht/datenschutz.html': 'datenschutz/',
}
for section, target in [('arbeiten', 'projekte'), ('blog', 'blog')]:
 for p in sorted((ROOT/section).glob('*.html')):
  if p.name != 'index.html': ROUTES[str(p.relative_to(ROOT))] = f'{target}/{p.stem}/'
for filename in ['marke.html', 'laune.html', 'takt.html']: ROUTES[filename] = filename
ALIASES = {'leistungen/websites.html': 'webdesign/'}
MAP = {**ROUTES, **ALIASES}
for target in list(MAP.values()):
 MAP[target] = target
 if not target.endswith('.html'): MAP[target+'index.html'] = target

META = {
 '': ('Marketing Agentur Schweiz für KMU | klartext.', 'Branding, Webdesign, Content, Social Media und Performance Marketing für Schweizer KMU. Entdeckt die Leistungen von klartext. und plant euren nächsten Schritt.'),
 'webdesign/': ('Webdesign Schweiz für KMU | klartext.', 'Webdesign für Schweizer KMU: Seitenstruktur, Gestaltung, technische SEO, Ladezeit und Pflege. Erfahrt, wie ihr euren neuen Webauftritt sinnvoll plant.'),
 'wissen/website-kosten-schweiz/': ('Was kostet eine Website in der Schweiz? | klartext.', 'Welche Faktoren bestimmen Website-Kosten? Ein Leitfaden für Schweizer KMU zu Konzept, Design, Inhalten, Technik, Betrieb und dem Vergleich von Offerten.'),
 'wissen/': ('Marketing-Wissen für Schweizer KMU | klartext.', 'Website, Budget und Marketing verständlich planen: Leitfäden und Antworten auf praktische Fragen von Schweizer KMU.'),
 'branding/': ('Branding und Markenstrategie für KMU | klartext.', 'Positionierung, Markenstrategie und Gestaltung: Erfahrt, wie ein Markensystem aus Logo, Farben, Schriften und Bildsprache entsteht.'),
 'social-media/': ('Social Media für Schweizer KMU | klartext.', 'Social Media mit Plan: Inhalte, Produktion, Veröffentlichung und Auswertung für Instagram, TikTok und LinkedIn. Leistungen im Überblick.'),
 'performance-marketing/': ('Performance Marketing für KMU | klartext.', 'Google Ads, Meta Ads, TikTok und LinkedIn: Ziele, Tracking, Kampagnen und Auswertung als Grundlage für nachvollziehbares Performance Marketing.'),
 'email-marketing/': ('E-Mail Marketing und Newsletter für KMU | klartext.', 'Newsletter, Segmentierung und automatisierte E-Mail-Strecken: Entdeckt die Leistungen rund um E-Mail Marketing und Kundenkommunikation.'),
 'leistungen/': ('Marketing-Leistungen für Schweizer KMU | klartext.', 'Branding, Social Media, Webdesign, Performance Marketing und E-Mail Marketing: die Leistungen von klartext. im Überblick.'),
 'ueber-uns/': ('Über klartext. | Marketing für Schweizer KMU', 'Einblick in die Arbeitsweise und den geplanten Auftritt von klartext. Team- und Unternehmensangaben dieser Entwurfsseite sind noch zu bestätigen.'),
 'projekte/': ('Projektentwürfe und Arbeitsbeispiele | klartext.', 'Arbeitsbeispiele aus Branding, Content und digitalem Marketing. Projektzuordnung, Referenzrechte und Ergebnisse sind vor Veröffentlichung zu prüfen.'),
 'blog/': ('Gedanken zu Marke und Marketing | klartext.', 'Artikel und Perspektiven zu Markenaufbau, Websites, Social Media und Strategie. Entdeckt den Blog von klartext.'),
 'impressum/': ('Impressum – Entwurf | klartext.', 'Impressumsentwurf von klartext. Verbindliche Betreiber- und Unternehmensangaben sind vor der Veröffentlichung zu vervollständigen.'),
 'datenschutz/': ('Datenschutzhinweise – Entwurf | klartext.', 'Datenschutzhinweise zum klartext.-Website-Entwurf. Die Angaben müssen vor dem Produktivstart mit den eingesetzten Diensten abgeglichen werden.')
}
LABELS={'':'Startseite','webdesign/':'Webdesign','wissen/':'Wissen','wissen/website-kosten-schweiz/':'Website-Kosten Schweiz','leistungen/':'Leistungen','branding/':'Branding','social-media/':'Social Media','performance-marketing/':'Performance Marketing','email-marketing/':'E-Mail Marketing','ueber-uns/':'Über uns','projekte/':'Projekte','blog/':'Blog','impressum/':'Impressum','datenschutz/':'Datenschutz'}

assert len(CONFIG['approved_paths']) == len(set(CONFIG['approved_paths'])), 'Duplicate approved paths'
assert set(CONFIG['approved_paths']) <= set(ROUTES.values()), 'Unknown approved path'
assert not set(CONFIG['approved_paths']) & {'marke.html','laune.html','takt.html'}, 'Design studies must remain noindex'

# Only generated output is replaced. Never delete source or user-authored files.
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
for directory in ['bilder','fonts','js','kopf','laune','logos','marke','video']:
 shutil.copytree(ROOT/directory, OUT/directory)
for p in ROOT.iterdir():
 if p.is_file() and p.suffix in {'.js','.css','.png'}: shutil.copy2(p,OUT/p.name)

sizes={}
def size_of(path):
 if path in sizes:return sizes[path]
 p=ROOT/path
 try:
  data=p.read_bytes()
  if data[:8]==b'\x89PNG\r\n\x1a\n': w,h=struct.unpack('>II',data[16:24])
  elif data[:2]==b'\xff\xd8':
   i=2
   while i<len(data):
    if data[i]!=255:i+=1;continue
    marker=data[i+1];i+=2
    length=int.from_bytes(data[i:i+2],'big')
    if marker in (0xc0,0xc1,0xc2,0xc3):h,w=struct.unpack('>HH',data[i+3:i+7]);break
    i+=length
   else:return None
  elif p.suffix=='.svg':
   m=re.search(r'viewBox=["\'][-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)',data.decode());w,h=map(float,m.groups())
  else:return None
  sizes[path]=(int(w),int(h));return sizes[path]
 except (OSError,ValueError,AttributeError,struct.error):return None

def resolved(value, source):
 u=urlsplit(unescape(value))
 if u.scheme or u.netloc or not u.path:return None
 return posixpath.normpath(posixpath.join(posixpath.dirname(source),u.path)).lstrip('/'),u

def rewrite_url(value, source, route):
 item=resolved(value,source)
 if not item:return value
 path,u=item
 if u.path.endswith('/'):path+='/'
 target=MAP.get(path,path)
 # Relative URLs make local preview and project subpath hosting identical.
 start=route if route.endswith('/') or route=='' else posixpath.dirname(route)
 rel=posixpath.relpath(target or '.',start or '.')
 if target.endswith('/') or target=='':rel=('./' if rel=='.' else rel+'/')
 return escape(urlunsplit(('', '',rel,u.query,u.fragment)),quote=True)

def breadcrumb(route,title):
 crumbs=[('', 'Startseite')]
 if route.startswith('wissen/') and route!='wissen/':crumbs.append(('wissen/','Wissen'))
 if route.startswith('blog/') and route!='blog/':crumbs.append(('blog/','Blog'))
 if route.startswith('projekte/') and route!='projekte/':crumbs.append(('projekte/','Projekte'))
 crumbs.append((route,LABELS.get(route,title.split('|')[0].strip())))
 graph={'@type':'BreadcrumbList','@id':BASE+route+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+path} for i,(path,name) in enumerate(crumbs)]}
 links=[]
 for i,(path,name) in enumerate(crumbs):
  rel=posixpath.relpath(path or '.',route or '.')
  links.append('<span aria-current="page">'+escape(name)+'</span>' if i==len(crumbs)-1 else '<a href="'+rel+'/">'+escape(name)+'</a>')
 return '<nav class="seo-breadcrumb" aria-label="Brotkrumennavigation">'+' <span aria-hidden="true">/</span> '.join(links)+'</nav>',graph

for source,route in ROUTES.items():
 s=(ROOT/source).read_text()
 if '</head>' not in s:
  s='<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'+s.replace('</style>','</style></head><body>',1)+'</body></html>'
 title_old=unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1))
 default_title=title_old.replace(' | KLARTEXT. Werbeagentur Zürich',' | klartext.').replace(' | KLARTEXT.',' | klartext.')
 if route.startswith('projekte/') and route!='projekte/':default_title=default_title.replace(' | klartext.',' – Arbeitsbeispiel | klartext.')
 desc_match=re.search(r'<meta name="description" content="([^"]*)"',s)
 desc=unescape(desc_match.group(1)) if desc_match else 'Gestaltungsstudie von klartext. Nicht zur Veröffentlichung in Suchmaschinen vorgesehen.'
 if route.startswith('blog/') and route!='blog/':desc=default_title.split('|')[0].strip()+'. Ein Beitrag über Marke und Marketing im klartext.-Blog.'
 if route.startswith('projekte/') and route!='projekte/':desc='Arbeitsbeispiel im klartext.-Entwurf. Zuordnung, Nutzungsrechte und Projektangaben sind noch nicht für die Veröffentlichung freigegeben.'
 title,desc=META.get(route,(default_title,desc))
 s=re.sub(r'<title>.*?</title>','<title>'+escape(title)+'</title>',s,flags=re.S)
 s=re.sub(r'<meta name="(?:description|robots)"[^>]*>\s*','',s)
 indexable=CONFIG['indexable'] and route in CONFIG['approved_paths']
 robots='index, follow, max-image-preview:large' if indexable else 'noindex, follow'
 canonical=BASE+route
 graph=[{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'inLanguage':'de-CH'}]
 if CONFIG['organization_verified']:
  graph.append({'@type':'Organization','@id':BASE+'#organization','name':'klartext.','url':BASE,'logo':BASE+'marke/wortmarke.svg'})
  graph[0]['publisher']={'@id':BASE+'#organization'}
 if route=='wissen/website-kosten-schweiz/':
  article={'@type':'Article','@id':canonical+'#article','headline':'Was kostet eine Website in der Schweiz?','description':desc,'mainEntityOfPage':{'@id':canonical+'#webpage'},'inLanguage':'de-CH'}
  if CONFIG['organization_verified']:article['publisher']={'@id':BASE+'#organization'}
  graph.append(article)
 person=CONFIG.get('person')
 if person and person.get('verified') and source=='ueber-uns.html':
  visible=unescape(re.sub('<[^>]+>',' ',re.sub(r'<(?:script|style)\b.*?</(?:script|style)>','',s,flags=re.S)))
  visible=' '.join(visible.split())
  assert person.get('name') and person['name'] in visible and person.get('visible_text') in visible, 'Person must match visible, verified profile.'
  graph.append({'@type':'Person','@id':BASE+'#person','name':person['name'],'url':canonical})
 # Defer external scripts in document order. They still run before DOMContentLoaded.
 s=re.sub(r'<script src="([^"]+)"',r'<script defer src="\1"',s)
 # Preserve optional intro implementation, but do not gate normal visits on all assets.
 s=s.replace('(function(){var n=0,s=null;', '(function(){if(!document.documentElement.hasAttribute("data-intro"))return;var n=0,s=null;')
 # Rebase asset and anchor links into clean route output.
 def tagfix(m):
  tag=m.group(0)
  img=re.match(r'<img\b',tag)
  src=re.search(r'\bsrc="([^"]+)"',tag)
  if img and src:
   item=resolved(src.group(1),source);dim=size_of(item[0]) if item else None
   if dim:
    tag=re.sub(r'\s(?:width|height)="[^"]*"','',tag)
    tag=tag[:-1]+f' width="{dim[0]}" height="{dim[1]}">'
   if 'decoding=' not in tag:tag=tag[:-1]+' decoding="async">'
   if 'dienst-' in src.group(1) and 'loading=' not in tag:tag=tag[:-1]+' loading="lazy">'
  return re.sub(r'\b(href|src|poster)="([^"]*)"',lambda x:x.group(1)+'="'+rewrite_url(x.group(2),source,route)+'"',tag)
 s=re.sub(r'<(?:a|link|img|script|video|source)\b[^>]*>',tagfix,s)
 if route and route not in ['marke.html','laune.html','takt.html']:
  markup,bc=breadcrumb(route,title);graph.append(bc)
  # Breadcrumb sits inside existing page intro, beneath floating nav.
  s=re.sub(r'(<section class="unter[^"\n]*">)',lambda m:m.group(1)+markup,s,count=1)
  if markup not in s:s=s.replace('<main>','<main>'+markup,1)
 # All standard footers expose the new knowledge hub.
 s=s.replace('<p class="fuss__kopf">Seite</p>','<p class="fuss__kopf">Seite</p><a href="'+posixpath.relpath('wissen',route or '.')+'/">Wissen</a>')
 # Existing trust claims remain as requested; contextual markers prevent treating them as verified.
 s=s.replace('Vertrauen uns</p>','Referenzen im Entwurf</p><p class="seo-pruefhinweis">Kundenbeziehungen und Nutzungsrechte sind noch zu bestätigen. Teile der Arbeiten stammen aus früheren beruflichen Stationen.</p>')
 s=s.replace('<h2 class="mitte">Die Mannschaft</h2>','<h2 class="mitte">Die Mannschaft</h2><p class="seo-pruefhinweis">Teamdarstellung im Entwurf: Namen, Rollen und Zugehörigkeit sind noch zu bestätigen.</p>')
 s=s.replace('<section class="vref">','<section class="vref"><p class="seo-pruefhinweis">Kundenstimmen im Entwurf: Zitate und Zuordnung sind noch nicht bestätigt.</p>')
 s=s.replace('<section class="preise" id="preise">','<section class="preise" id="preise"><p class="seo-pruefhinweis">Preise und Leistungsversprechen sind Entwurfswerte und noch nicht als Angebot freigegeben.</p>')
 s=s.replace('<p>2026 Klartext Digital GmbH · Alle Rechte vorbehalten</p>','<div><p>2026 Klartext Digital GmbH · Alle Rechte vorbehalten</p><p>Firmierung, Kontaktangaben und Geschäftszeiten: noch zu bestätigen.</p></div>')
 s=s.replace('<h2 data-rein-zeilen><span>Die Mannschaft</span></h2>','<h2 data-rein-zeilen><span>Die Mannschaft</span></h2><p class="seo-pruefhinweis">Teamdarstellung im Entwurf. Namen, Rollen und Zugehörigkeit sind noch nicht bestätigt.</p>')
 s=s.replace('Werbeagentur mit Sitz in Zürich, tätig in der ganzen Deutschschweiz','Marketing für Schweizer KMU · Standortangaben noch zu bestätigen')
 if route.startswith('projekte/') or route=='ueber-uns/':
  s=s.replace('<main>','<main><p class="seo-pruefhinweis seo-freigabe">Entwurf: Team, Projektzuordnung, Referenzrechte und Aussagen sind noch zu bestätigen.</p>',1)
 prefix=posixpath.relpath('.',route or '.')+'/'
 schema_json=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')
 head=f'''\n<meta name="description" content="{escape(desc,quote=True)}">\n<meta name="robots" content="{robots}">\n<link rel="canonical" href="{canonical}">\n<meta property="og:title" content="{escape(title,quote=True)}">\n<meta property="og:description" content="{escape(desc,quote=True)}">\n<meta property="og:url" content="{canonical}">\n<meta property="og:type" content="website">\n<meta property="og:locale" content="de_CH">\n<meta property="og:image" content="{BASE}marke/favicon-180.png">\n<link rel="stylesheet" href="{prefix}seo.css">\n<script type="application/ld+json">{schema_json}</script>\n'''
 if route=='':head+='<link rel="preload" as="image" href="kopf/grund.jpg" fetchpriority="high">\n'
 head+=f'<link rel="preload" href="{prefix}fonts/figtree-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
 s=s.replace('</head>',head+'</head>')
 dest=OUT/(route if route.endswith('.html') else route+'index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(s)

for old,target in {**ROUTES,**ALIASES}.items():
 dest=OUT/old
 canonical_file=target if target.endswith('.html') else target+'index.html'
 if old==canonical_file:continue
 dest.parent.mkdir(parents=True,exist_ok=True)
 rel=posixpath.relpath(target or '.',posixpath.dirname(old) or '.')+'/'
 dest.write_text(f'<!doctype html>\n<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Seite verschoben | klartext.</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="{BASE+target}"><meta http-equiv="refresh" content="0;url={rel}"></head><body><p>Diese Seite hat eine neue Adresse: <a href="{rel}">Weiter zur Seite</a>.</p></body></html>')
paths=[p for p in ROUTES.values() if CONFIG['indexable'] and p in CONFIG['approved_paths']]
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+escape(BASE+p)+'</loc></url>\n' for p in paths)+'</urlset>\n'
(OUT/'sitemap.xml').write_text(xml)
(OUT/'robots.txt').write_text('# Effective only when served at the host root. Draft noindex is in HTML.\nUser-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
(OUT/'.nojekyll').touch()
(ROOT/'docs/URL-MAP.json').write_text(json.dumps({k:BASE+v for k,v in {**ROUTES,**ALIASES}.items()},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(ROUTES)} pages and legacy redirects. Indexable sitemap entries: {len(paths)}. Output: {OUT}')
