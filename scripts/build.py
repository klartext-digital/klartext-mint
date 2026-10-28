#!/usr/bin/env python3
"""Build static Pages output. Source HTML remains editable; _site is generated."""
from pathlib import Path
from html import escape, unescape
from urllib.parse import urljoin, urlsplit, urlunsplit
import json, re, shutil, posixpath, struct, os, hashlib
from release_policy import validate_preview
import verkleinern

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('KLARTEXT_BUILD_DIR', ROOT / '_site')).resolve()
assert OUT != ROOT and OUT not in ROOT.parents, 'Output must not replace source directories'
CONFIG = json.loads((ROOT / 'seo.config.json').read_text())
validate_preview(CONFIG)
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
 'recht/impressum.html': 'impressum/',
 'recht/datenschutz.html': 'datenschutz/',
}
for section, target in [('arbeiten', 'projekte'), ('blog', 'blog')]:
 for p in sorted((ROOT/section).glob('*.html')):
  if p.name != 'index.html': ROUTES[str(p.relative_to(ROOT))] = f'{target}/{p.stem}/'
for filename in ['marke.html', 'laune.html', 'takt.html']: ROUTES[filename] = filename
PAGE_META = json.loads((ROOT/'page-meta.json').read_text())
for route in PAGE_META:
 ROUTES[route+'index.html'] = route
IMAGE_VARIANTS = json.loads((ROOT/'bild-varianten.json').read_text())
IMAGE_SIZES = json.loads((ROOT/'bild-groessen.json').read_text()) if (ROOT/'bild-groessen.json').exists() else {}
# ── Blogübersicht: aus den Artikeln erzeugt, nicht von Hand gepflegt ──────────
# Die sechs Karten standen handgeschrieben in blog/index.html — samt Lesezeit,
# Datum, Anriss, Bild und Person. Jeder neue Beitrag hätte dort eine weitere
# Karte von Hand gebraucht; Anrisse und Daten wären mit der Zeit auseinander
# gelaufen. Fünf der sechs Angaben stehen ohnehin im Artikel. Sie werden von
# dort gelesen, die Personenzuordnung kommt aus blog-autoren.json.
BLOG_AUTOREN = json.loads((ROOT/'blog-autoren.json').read_text()) if (ROOT/'blog-autoren.json').exists() else {}
MONATE = {'Jan':1,'Feb':2,'Mär':3,'Maer':3,'Apr':4,'Mai':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Okt':10,'Nov':11,'Dez':12}

def blog_beitraege():
 """Liest jeden Blogartikel und gibt die Angaben für seine Karte zurück.

 Zwei Bauformen: die kurzen Standpunkte liegen flach als blog/<x>.html und
 tragen Datum, Einstiegsabsatz und Bild im Artikel selbst. Die Leitfaeden
 liegen als Ordner blog/<x>/index.html; sie haben kein Datum, oft keinen
 Einstiegsabsatz vor dem Inhaltsverzeichnis und kein figure-Bild. Fuer sie
 kommen Anriss und Bild aus page-meta.json. Gemessen am 17.09.2026: eine
 Karte ohne Datum und ohne Person haelt — die Hoehe kommt aus dem Raster.
 """
 aus=[]
 kandidaten=[(p,p.name,False) for p in sorted((ROOT/'blog').glob('*.html'))]
 kandidaten+=[(p,p.parent.name+'/',True) for p in sorted((ROOT/'blog').glob('*/index.html'))]
 for p,ziel,ordner in kandidaten:
  if not ordner and p.name=='index.html': continue
  if re.search(r' \d+$',p.stem) or ' ' in p.as_posix(): continue
  s=p.read_text()
  m=re.search(r'<main[\s\S]*?</main>',s)
  k=m.group(0) if m else s
  h1=re.search(r'<h1[^>]*>([\s\S]*?)</h1>',k)
  if not h1: continue
  stamm=p.parent.name if ordner else p.stem
  meta=PAGE_META.get('blog/'+ziel,{}) if ordner else {}
  chip=re.search(r'<span class="chip"[^>]*>([\s\S]*?)</span>',k)
  datum=re.sub(r'<[^>]*>','',chip.group(1)).strip() if chip else ''
  t=re.match(r'(\d{1,2})\.\s*([A-Za-zäöüÄÖÜ]+)\s*(\d{4})',datum) if datum else None
  bild=re.search(r'artikel__bild"[\s\S]*?src="(?:\.\./)+([^"]+)"',k)
  bildpfad=bild.group(1) if bild else meta.get('image','')
  absatz=re.search(r'<article class="artikel[^"]*"[^>]*>\s*<p>([\s\S]*?)</p>',k)
  anriss=absatz.group(1).strip() if absatz else escape(meta.get('description',''))
  if not (bildpfad and anriss): continue
  minuten=max(1,round(len(re.sub(r'<[^>]*>',' ',k).split())/200))
  aus.append({
   'datei':ziel,'stamm':stamm,
   'titel':re.sub(r'<[^>]*>','',h1.group(1)).strip(),
   'datum':datum,
   'sortierung':(1,int(t.group(3)),MONATE.get(t.group(2)[:3],0),int(t.group(1))) if t else (0,0,0,0),
   'bild':bildpfad,'anriss':anriss,'minuten':minuten,
   'person':BLOG_AUTOREN.get(stamm),
  })
 aus.sort(key=lambda b:b['sortierung'],reverse=True)
 return aus

def blog_karten_html(beitraege):
 teile=[]
 for b in beitraege:
  person=''
  if b['person']:
   person=('\n          <span class="lese__wer">'
           f'\n            <img src="../bilder/{b["person"]["bild"]}" alt="" loading="lazy">'
           f'\n            <span><b>{escape(b["person"]["name"])}</b><i>{escape(b["person"]["rolle"])}</i></span>'
           '\n          </span>')
  teile.append(
   f'\n      <a class="lese" href="{b["datei"]}" data-rein>'
   '\n        <div class="lese__oben">'
   f'\n          <p class="lese__meta"><span class="lese__zeit">*{b["minuten"]} Min Lesezeit</span>'
   + (f'<span class="lese__datum">{escape(b["datum"])}</span>' if b['datum'] else '')
   + '</p>'
   f'\n          <h3 class="lese__titel">{escape(b["titel"])}</h3>'
   f'\n          <p class="lese__anriss">{b["anriss"]}</p>'
   f'{person}'
   '\n        </div>'
   f'\n        <div class="lese__bild"><img src="../{b["bild"]}" alt="" loading="lazy"></div>'
   '\n      </a>')
 return ''.join(teile)

ALIASES = {'leistungen/websites.html': 'webdesign/',
           'content-creation/index.html': 'social-media/',
           'kommunikationsstrategie/index.html': 'branding/',
           'wissen/index.html': 'blog/',
           'wissen/branding-kosten/index.html': 'blog/branding-kosten/',
           'wissen/google-ads-budget/index.html': 'blog/google-ads-budget/',
           'wissen/marketingbudget-kmu/index.html': 'blog/marketingbudget-kmu/',
           'wissen/social-media-kosten/index.html': 'blog/social-media-kosten/',
           'wissen/website-erstellen-lassen/index.html': 'blog/website-erstellen-lassen/',
           'wissen/website-kosten-schweiz/index.html': 'blog/website-kosten-schweiz/',
           'wissen/website-pflege-checkliste/index.html': 'blog/website-pflege-checkliste/',
           'wissen/website-relaunch-checkliste/index.html': 'blog/website-relaunch-checkliste/'}
MAP = {**ROUTES, **ALIASES}
for target in list(MAP.values()):
 MAP[target] = target
 if not target.endswith('.html'): MAP[target+'index.html'] = target

META = {
 '': ('Marketingagentur Basel, Baselland & Aargau | Klartext Digital', 'Marketingagentur aus Pratteln, Schwerpunkt Region Basel und Aargau, tätig in der ganzen Deutschschweiz: SEO, Webdesign, Social Media, Google und Meta Ads.'),
 'webdesign/': ('Webdesign Basel & Aargau für KMU | Klartext Digital', 'Webdesign für KMU in Basel, Baselland und im Aargau: Struktur, Gestaltung, technische SEO, Ladezeit und Pflege aus einer Hand.'),

 'branding/': ('Branding & Markenstrategie Basel | Klartext Digital', 'Positionierung, Markensystem und Vorlagen für euren Alltag. Branding als Projekt oder spezialisierte Ergänzung eurer Marketingabteilung.'),
 'social-media/': ('Social-Media-Agentur Basel & Aargau | Klartext Digital', 'Social Media für Unternehmen in der Region Basel und im Aargau: Redaktionsplan, Reels und Auswertung. Laufend, als Kampagne oder für euer Team.'),
 'performance-marketing/': ('Google & Meta Ads Agentur Basel | Klartext Digital', 'Google und Meta Ads mit passenden Zielseiten, Messung und laufender Betreuung. Werbeetat und Umsetzung klar planen, Anfragen nach Qualität beurteilen.'),
 'email-marketing/': ('Newsletter & E-Mail-Marketing Basel | Klartext Digital', 'Newsletter-Kampagnen, Vorlagen und automatisierte Strecken. Konzeption, Umsetzung und Auswertung als laufende Betreuung oder Ergänzung eures Teams.'),
 'leistungen/': ('Marketing-Leistungen für KMU, Region Basel | klartext.', 'Branding, Social Media, Webdesign, Performance Marketing und E-Mail Marketing für Unternehmen in Basel, Baselland und im Aargau: die Leistungen im Überblick.'),
 'ueber-uns/': ('Über klartext. | Marketingagentur aus Pratteln', 'Marketingagentur aus Pratteln, Schwerpunkt Region Basel und Aargau, tätig in der ganzen Deutschschweiz: wer wir sind und wie wir arbeiten.'),
 "projekte/grand-casino-baden/": ("Grand Casino Baden: Social Media | Klartext Digital", "Laufende Social-Media-Betreuung und Content-Produktion für das Grand Casino Baden seit 2024: Präsenz am Markt, organisch gewachsen."),
 "projekte/red-bull/": ("Red Bull × Grand Casino Baden | Klartext Digital", "Content und Fotografie für zwei Drinks zur Winter Edition, umgesetzt in der Bar im Grand Casino Baden."),
 "projekte/aesthetics-medical/": ("Aesthetics Medical: Social Media | Klartext Digital", "Social Media und Reels für die Aesthetics Medical AG am Utoquai in Zürich: Behandlungen verständlich zeigen statt erklären müssen."),
 "projekte/nordlicht/": ("Nordlicht: Markenidentität & Website | Klartext Digital", "Branding und Website für eine junge Energieplattform: eine klare Markenidentität, entwickelt und umgesetzt in sechs Wochen (2025)."),
 "projekte/volta/": ("Volta: Auftritt für komplexe Technik | Klartext Digital", "Branding und 3D-Bildsprache für Volta: ein Auftritt, der komplexe Technik verständlich macht. Umgesetzt in neun Wochen (2024)."),
 "projekte/meridian/": ("Meridian: vom Nischenprodukt zur Marke | Klartext Digital", "Branding und Kampagne für Meridian: vom Nischenprodukt zur Marke mit Haltung, entwickelt in zwölf Wochen (2024)."),
 'projekte/': ('Projekte und Referenzen | Klartext Digital', 'Einblicke in die Referenzen von Klartext Digital: Projekte aus Branding, Content und digitalem Marketing.'),
 'blog/': ('Gedanken zu Marke und Marketing | klartext.', 'Artikel und Perspektiven zu Markenaufbau, Websites, Social Media und Strategie. Entdeckt den Blog von klartext.'),
 'impressum/': ('Impressum | Klartext Digital', 'Impressum der Klartext Digital GmbH (in Gründung), Lohagstrasse 15, 4133 Pratteln.'),
 'datenschutz/': ('Datenschutz | Klartext Digital', 'Datenschutzerklärung der Klartext Digital GmbH, Pratteln: Hosting, E-Mail, keine Cookies und keine Besuchermessung.')
}
# Unternehmensangaben: eine Quelle (seo.config.json → business), dieselben
# Daten wie im Google-Unternehmensprofil und in der Fusszeile. Google und
# KI-Suchen vergleichen Name, Adresse und Einzugsgebiet über alle Quellen;
# Abweichungen kosten Vertrauen. ProfessionalService ist ein LocalBusiness
# und damit auch eine Organization.
BUSINESS=CONFIG.get('business') or {}
ORGANISATION={'@type':'Organization','@id':BASE+'#organization','name':'Klartext Digital','alternateName':'klartext.','url':BASE,'logo':BASE+'marke/wortmarke.svg'}
if BUSINESS:
 ORGANISATION={'@type':BUSINESS['type'],'@id':BASE+'#organization','name':BUSINESS['name'],'alternateName':BUSINESS['alternateName'],
  'url':BASE,'logo':BASE+'marke/wortmarke.svg','image':BASE+'bilder/dienst-3.jpg','email':BUSINESS['email'],
  'address':{'@type':'PostalAddress','streetAddress':BUSINESS['street'],'postalCode':BUSINESS['postal_code'],'addressLocality':BUSINESS['locality'],'addressRegion':BUSINESS['region'],'addressCountry':BUSINESS['country']},
  'areaServed':[{'@type':'AdministrativeArea','name':n} for n in BUSINESS['area_served']],
  'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday'],'opens':BUSINESS['opens'],'closes':BUSINESS['closes']}] if BUSINESS.get('opens') else [],
  'knowsAbout':['Webdesign','Suchmaschinenoptimierung','Social Media Marketing','Google Ads','Meta Ads','E-Mail-Marketing','Branding']}
LEISTUNGEN={'webdesign/':'Webdesign','seo/':'Suchmaschinenoptimierung (SEO)','social-media/':'Social-Media-Betreuung','performance-marketing/':'Google Ads und Meta Ads','branding/':'Branding und Markenstrategie','email-marketing/':'E-Mail-Marketing und Newsletter','website-betreuung/':'Website-Betreuung','marketing-abo/':'Marketing im Abo','projektarbeit/':'Marketing-Projekte'}
LABELS={'':'Startseite','webdesign/':'Webdesign','leistungen/':'Leistungen','branding/':'Branding','social-media/':'Social Media','performance-marketing/':'Performance Marketing','email-marketing/':'E-Mail Marketing','ueber-uns/':'Über uns','projekte/':'Projekte','blog/':'Blog','impressum/':'Impressum','datenschutz/':'Datenschutz'}
for route, meta in PAGE_META.items():
 META[route] = (meta['title'], meta['description'])
 LABELS[route] = meta['label']

assert len(CONFIG['approved_paths']) == len(set(CONFIG['approved_paths'])), 'Duplicate approved paths'
assert set(CONFIG['approved_paths']) <= set(ROUTES.values()), 'Unknown approved path'
assert not set(CONFIG['approved_paths']) & {'marke.html','laune.html','takt.html'}, 'Design studies must remain noindex'

# Only generated output is replaced. Never delete source or user-authored files.
if OUT.exists():
 assert OUT == ROOT/'_site' or (OUT/'.klartext-generated').is_file(), 'Refuse to replace a directory not owned by this build'
 shutil.rmtree(OUT)
OUT.mkdir()
(OUT/'.klartext-generated').touch()
for directory in ['bilder','fonts','js','kopf','laune','logos','marke','video']:
 shutil.copytree(ROOT/directory, OUT/directory)
# Quelldateien bleiben lesbar; nur die Ausgabe wird verkleinert.
# Fremde Bibliotheken unter js/ sind bereits verkleinert und werden kopiert.
for p in ROOT.iterdir():
 if not p.is_file(): continue
 if p.suffix=='.css': (OUT/p.name).write_text(verkleinern.css(p.read_text()))
 elif p.suffix=='.js': (OUT/p.name).write_text(verkleinern.js(p.read_text()))
 elif p.suffix=='.png': shutil.copy2(p,OUT/p.name)

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

stempel_cache={}
def stempel(path):
 """Kurzer Fingerabdruck einer Datei fuer die Adresse.

 Browser halten Skripte und Stylesheets zehn Minuten fest. Nach einem
 Deploy sieht man deshalb den alten Stand und haelt eine Aenderung fuer
 wirkungslos — das ist uns mehrfach passiert. Haengt der Fingerabdruck
 an der Adresse, bekommt jeder sofort die neue Datei, ohne hart neu zu
 laden. Aendert sich die Datei nicht, bleibt die Adresse gleich und der
 Cache greift weiter."""
 if path in stempel_cache:return stempel_cache[path]
 try:h=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()[:8]
 except OSError:h=None
 stempel_cache[path]=h;return h

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


def faq_paare(text):
 """Frage-Antwort-Paare aus dem sichtbaren Seiteninhalt lesen.
 Zwei Bauformen: <details><summary> auf den neuen Seiten und das
 Akkordeon der Startseite. Nur was sichtbar auf der Seite steht,
 darf ausgezeichnet werden."""
 paare=[]
 for m in re.finditer(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>',text,re.S):
  paare.append((m.group(1),m.group(2)))
 for m in re.finditer(r'<span class="frage__text">(.*?)</span>[\s\S]*?<div class="frage__leib">(.*?)</div>',text,re.S):
  paare.append((m.group(1),m.group(2)))
 sauber=[]
 for frage,antwort in paare:
  f=' '.join(unescape(re.sub('<[^>]+>','',frage)).split())
  a=' '.join(unescape(re.sub('<[^>]+>',' ',antwort)).split())
  if f and a and len(a)>25: sauber.append((f,a))
 return sauber

def breadcrumb(route,title):
 crumbs=[('', 'Startseite')]
 
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
 route_dir=route if route.endswith('/') else posixpath.dirname(route)
 s=(ROOT/source).read_text()
 if '</head>' not in s:
  s='<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'+s.replace('</style>','</style></head><body>',1)+'</body></html>'
 title_old=unescape(re.search(r'<title>(.*?)</title>',s,re.S).group(1))
 default_title=title_old.replace(' | KLARTEXT. Werbeagentur Zürich',' | klartext.').replace(' | KLARTEXT.',' | klartext.')
 desc_match=re.search(r'<meta name="description" content="([^"]*)"',s)
 desc=unescape(desc_match.group(1)) if desc_match else 'Gestaltungsstudie von klartext. Nicht zur Veröffentlichung in Suchmaschinen vorgesehen.'
 if route.startswith('blog/') and route!='blog/':desc=default_title.split('|')[0].strip()+'. Ein Beitrag über Marke und Marketing im klartext.-Blog.'
 title,desc=META.get(route,(default_title,desc))
 s=re.sub(r'<html lang="de">','<html lang="de-CH">',s,count=1)
 s=re.sub(r'<title>.*?</title>','<title>'+escape(title)+'</title>',s,flags=re.S)
 s=re.sub(r'<meta name="(?:description|robots)"[^>]*>\s*','',s)
 indexable=CONFIG['indexable'] and route in CONFIG['approved_paths']
 robots='index, follow, max-image-preview:large' if indexable else 'noindex, follow'
 canonical=BASE+route
 graph=[{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'inLanguage':'de-CH'}]
 if CONFIG['organization_verified']:
  graph.append(ORGANISATION)
  graph[0]['publisher']={'@id':BASE+'#organization'}
 veroeffentlicht=re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"',s)
 is_article=PAGE_META.get(route,{}).get('article',False) or bool(veroeffentlicht)
 preview_image=BASE+PAGE_META.get(route,{}).get('image','bilder/dienst-3.jpg')
 if is_article:
  headline=unescape(re.sub('<[^>]+>','',re.search(r'<h1\b[^>]*>(.*?)</h1>',s,re.S).group(1)))
  article={'@type':'Article','@id':canonical+'#article','headline':headline,'description':desc,'mainEntityOfPage':{'@id':canonical+'#webpage'},'inLanguage':'de-CH','image':preview_image}
  if veroeffentlicht:article['datePublished']=veroeffentlicht.group(1)
  if CONFIG['organization_verified']:article['publisher']={'@id':BASE+'#organization'}
  graph.append(article)
 # Leistungsseiten: Service mit Anbieter und Einzugsgebiet. Hilft Google
 # und KI-Suchen, Leistung, Firma und Region zusammenzubringen.
 if route in LEISTUNGEN and BUSINESS:
  graph.append({'@type':'Service','@id':canonical+'#service','name':LEISTUNGEN[route],'serviceType':LEISTUNGEN[route],
   'provider':{'@id':BASE+'#organization'},'areaServed':ORGANISATION['areaServed'],'url':canonical,'description':desc})
 fragen=faq_paare(s)
 if len(fragen)>=2:
  graph.append({'@type':'FAQPage','@id':canonical+'#faq','inLanguage':'de-CH','mainEntity':[
   {'@type':'Question','name':f,'acceptedAnswer':{'@type':'Answer','text':a}} for f,a in fragen]})
 person=CONFIG.get('person')
 if person and person.get('verified') and source=='ueber-uns.html':
  visible=unescape(re.sub('<[^>]+>',' ',re.sub(r'<(?:script|style)\b.*?</(?:script|style)>','',s,flags=re.S)))
  visible=' '.join(visible.split())
  assert person.get('name') and person['name'] in visible and person.get('visible_text') in visible, 'Person must match visible, verified profile.'
  graph.append({'@type':'Person','@id':BASE+'#person','name':person['name'],'url':canonical})
 # Die Blogübersicht wird erzeugt, nicht gepflegt: ein neuer Beitrag ist eine
 # Datei, die Karte entsteht daraus.
 # WICHTIG: Das muss VOR tagfix laufen. tagfix ergaenzt Bildmasse, decoding und
 # WebP-Varianten und schreibt interne Verweise auf die sauberen Adressen um.
 # Stand der Block dahinter, verloren die erzeugten Karten beides: Portraets
 # luden als volles JPEG statt als 420er WebP, ohne Bildmasse sprang beim Laden
 # das Layout, und die Verweise zeigten auf die alten .html-Adressen.
 # Der assert ist Absicht — ein stiller Fehlschlag wuerde die Uebersicht
 # einfrieren, ohne dass es jemand merkt.
 if route=='blog/':
  raster=re.search(r'(<div class="lesegitter">)([\s\S]*?)(\n    </div>\n  </section>)',s)
  assert raster, 'Kartenraster in blog/index.html nicht gefunden — Aufbau geaendert?'
  karten=blog_karten_html(blog_beitraege())
  assert karten.count('<a class="lese"')>=1, 'Keine Blogbeitraege gelesen'
  s=s[:raster.start(2)]+karten+s[raster.end(2):]
 # Defer external scripts in document order. They still run before DOMContentLoaded.
 s=re.sub(r'<script src="([^"]+)"',r'<script defer src="\1"',s)
 # Ladeschirm: bleibt aktiv — beim ersten Besuch und danach jeden zehnten Aufruf.
 # Ausdrueckliche Vorgabe des Auftraggebers; nicht ueber den Build abschalten.
 # Rebase asset and anchor links into clean route output.
 def tagfix(m):
  tag=m.group(0)
  variants=None
  img=re.match(r'<img\b',tag)
  src=re.search(r'\bsrc="([^"]+)"',tag)
  if img and src:
   item=resolved(src.group(1),source);dim=size_of(item[0]) if item else None
   variants=IMAGE_VARIANTS.get(item[0]) if item else None
   if dim:
    tag=re.sub(r'\s(?:width|height)="[^"]*"','',tag)
    tag=tag[:-1]+f' width="{dim[0]}" height="{dim[1]}">'
   if 'decoding=' not in tag:tag=tag[:-1]+' decoding="async">'
   # Hero-Hintergruende tragen fetchpriority="high" und duerfen NICHT lazy laden —
   # sonst poppt das erste Bild der Seite verzoegert nach und widerspricht der Prioritaet.
   if 'dienst-' in src.group(1) and 'loading=' not in tag and 'fetchpriority="high"' not in tag:tag=tag[:-1]+' loading="lazy">'
  def _mit_stempel(x):
   attr,wert=x.group(1),x.group(2)
   # srcset mit EINER Adresse (z. B. <source> im Kopf-Logo) wie src
   # umschreiben; Listen mit Breitenangaben baut der Build selbst.
   if attr=='srcset' and (',' in wert or ' ' in wert.strip()):return x.group(0)
   neu=rewrite_url(wert,source,route)
   if attr in ('href','src'):
    item=resolved(wert,source)
    if item and item[0].endswith(('.js','.css')) and not item[1].query:
     h=stempel(item[0])
     if h:neu+=('&amp;' if '?' in neu else '?')+'v='+h
   return attr+'="'+neu+'"'
  tag=re.sub(r'\b(href|src|poster|srcset)="([^"]*)"',_mit_stempel,tag)
  if variants:
   candidates=', '.join(posixpath.relpath(v['path'],route_dir or '.')+' '+str(v['width'])+'w' for v in variants)
   # Ein im Markup gesetztes sizes bleibt stehen: dieselbe Bilddatei dient
   # sowohl als Umfang-Karte (30vw) als auch als Hero-Hintergrund (62vw),
   # und bild-groessen.json kennt nur EINEN Wert je Datei.
   hat_sizes='sizes="' in tag
   sizes=IMAGE_SIZES.get(item[0],'(max-width: 700px) 100vw, 50vw') if item else '(max-width: 700px) 100vw, 50vw'
   tag=tag[:-1]+' srcset="'+candidates+'"'+('' if hat_sizes else ' sizes="'+sizes+'"')+'>'
  return tag
 # Handschrift: der innere Traeger .brush__t steht immer im Markup (Strich
 # aussen, Schrift mit Pinselmaske innen), nicht erst, wenn das Skript laeuft.
 s=re.sub(r'(<(p|span|em|b|i)\b[^>]*class="[^"]*\b(?:brush|wort)\b[^"]*"[^>]*>)(?!<span class="brush__t">)(.*?)(</\2>)',
  r'\1<span class="brush__t">\3</span>\4',s,flags=re.S)
 s=re.sub(r'<(?:a|link|img|image|script|video|source)\b[^>]*>',tagfix,s)  # image: SVG-Bild in der Arbeitsweise-Grafik
 if route and route not in ['marke.html','laune.html','takt.html']:
  markup,bc=breadcrumb(route,title);graph.append(bc)
  # Breadcrumb sits inside existing page intro, beneath floating nav.
  s=re.sub(r'(<section class="unter[^"\n]*">)',lambda m:m.group(1)+markup,s,count=1)
  if markup not in s:s=s.replace('<main>','<main>'+markup,1)
 # All standard footers expose the new knowledge hub.
 spalte=re.search(r'<p class="fuss__kopf">Seite</p>[\s\S]*?</nav>',s)
 if spalte and 'mlink__t">Blog<' not in spalte.group(0):
  s=s.replace('<p class="fuss__kopf">Seite</p>','<p class="fuss__kopf">Seite</p><a href="'+posixpath.relpath('blog',route_dir or '.')+'/">Blog</a>')
 # Offer navigation is shared; keep the existing visual menu and interactions.
 def route_link(target):return posixpath.relpath(target,route_dir or '.')+'/'
 offer_nav='<nav class="seo-offer-nav" aria-label="Zusammenarbeit"><a href="'+route_link('marketing-abo')+'">Marketing im Abo</a><a href="'+route_link('projektarbeit')+'">Projektarbeit</a></nav>'
 # Entfernt 18.09.2026 (Dusan: "brauchen wir das" - nein). Die beiden Links
 # standen als schlichte unterstrichene Textlinks ueber den nummerierten
 # Leistungen derselben Menuespalte, also in fremder Formensprache, und die
 # Fusszeile fuehrt Marketing im Abo und Projektarbeit ohnehin schon.
 # Die 404-Seite behaelt ihre seo-offer-nav: dort ist sie neben "Zur
 # Startseite" die einzige Navigation, keine Dopplung.
 # References retain their source presentation per the confirmed project rules.
 # Preise sind vom Auftraggeber bestaetigt (16.09.2026): kein Entwurfshinweis mehr.
 # Die Angaben zur Mehrwertsteuer stehen sichtbar unter den Paketen.
 # Firmierung und Adresse bestätigt (14.10.2026). "in Gründung" entfällt mit dem
 # Handelsregistereintrag. Telefon bewusst leer (Dusan, 14.10.2026).
 s=s.replace('<p>2026 Klartext Digital GmbH · Alle Rechte vorbehalten</p>','<p>2026 Klartext Digital GmbH (in Gründung) · Alle Rechte vorbehalten</p>')
 # Entwurfs-Hinweis unten rechts entfernt (Dusan 15.10.2026: keine Hinweise
 # auf der Seite, die nicht hingehoeren). Steht noch in den Quelldateien.
 s=re.sub(r'<div class="demo">[^<]*</div>\s*','',s)
 prefix=posixpath.relpath('.',route_dir or '.')+'/'
 schema_json=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')
 head=f'''\n<meta name="description" content="{escape(desc,quote=True)}">\n<meta name="robots" content="{robots}">\n<link rel="canonical" href="{canonical}">\n<meta property="og:title" content="{escape(title,quote=True)}">\n<meta property="og:description" content="{escape(desc,quote=True)}">\n<meta property="og:url" content="{canonical}">\n<meta property="og:type" content="website">\n<meta property="og:locale" content="de_CH">\n<meta property="og:image" content="{BASE}marke/favicon-180.png">\n<link rel="stylesheet" href="{prefix}seo.css?v={stempel("seo.css") or ""}">\n<script type="application/ld+json">{schema_json}</script>\n'''
 if route=='':head+='<link rel="preload" as="image" href="kopf/portrait-unscharf.webp" type="image/webp" fetchpriority="high">\n'
 # A real landscape image replaces the tiny app icon in link previews.
 head=head.replace(BASE+'marke/favicon-180.png',preview_image)
 head=head.replace('property="og:type" content="website"','property="og:type" content="'+('article' if is_article else 'website')+'"')
 head+=f'<meta property="og:image:alt" content="Klartext Digital – Webdesign und Marketing">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{escape(title,quote=True)}">\n<meta name="twitter:description" content="{escape(desc,quote=True)}">\n<meta name="twitter:image" content="{preview_image}">\n<script defer src="{prefix}messung.js?v={stempel("messung.js") or ""}"></script>\n'
 for key,name in [('google','google-site-verification'),('bing','msvalidate.01')]:
  token=CONFIG.get('verification',{}).get(key)
  if token:head+=f'<meta name="{name}" content="{escape(token,quote=True)}">\n'
 head+=f'<link rel="preload" href="{prefix}fonts/figtree-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
 # Fliesstext: Trade Gothic Next Light/Regular aus dem Adobe-Fonts-Web-Projekt
 # "Klartext Website" (Kit ymt6jvd, Lizenz ueber Dusans Creative Cloud).
 head+='<link rel="preconnect" href="https://use.typekit.net" crossorigin>\n<link rel="stylesheet" href="https://use.typekit.net/ymt6jvd.css">\n'
 head+=f'<link rel="preload" href="{prefix}fonts/klartext-hand-11.woff2" as="font" type="font/woff2" crossorigin>\n'
 s=s.replace('</head>',head+'</head>')
 dest=OUT/(route if route.endswith('.html') else route+'index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(s)

for old,target in {**ROUTES,**ALIASES}.items():
 dest=OUT/old
 canonical_file=target if target.endswith('.html') else target+'index.html'
 if old==canonical_file:continue
 dest.parent.mkdir(parents=True,exist_ok=True)
 rel=posixpath.relpath(target or '.',posixpath.dirname(old) or '.')+'/'
 dest.write_text(f'<!doctype html>\n<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Seite verschoben | klartext.</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="{BASE+target}"><meta http-equiv="refresh" content="0;url={rel}"></head><body><p>Diese Seite hat eine neue Adresse: <a href="{rel}">Weiter zur Seite</a>.</p></body></html>')
paths=[p for p in ROUTES.values() if CONFIG['indexable'] and p in CONFIG['approved_paths']]
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+escape(BASE+p)+'</loc></url>\n' for p in paths)+'</urlset>\n'
(OUT/'sitemap.xml').write_text(xml)
# KI-Suchen ausdruecklich zulassen (Entscheid 15.10.2026, Sichtbarkeit in
# ChatGPT, Perplexity, Gemini, Claude, Copilot). Allow: / gilt zwar schon ueber
# den Stern; eigene Bloecke verhindern, dass ein Hoster- oder Vorlagen-Default
# einzelne Crawler sperrt, und machen die Absicht lesbar.
KI_CRAWLER=['GPTBot','OAI-SearchBot','ChatGPT-User','PerplexityBot','Perplexity-User','ClaudeBot','Claude-SearchBot','Claude-User','Google-Extended','Applebot-Extended','Bingbot']
robots='# Effective only when served at the host root. Draft noindex is in HTML.\nUser-agent: *\nAllow: /\n\n'
robots+=''.join('User-agent: '+c+'\nAllow: /\n\n' for c in KI_CRAWLER)
(OUT/'robots.txt').write_text(robots+'Sitemap: '+BASE+'sitemap.xml\n')
# llms.txt: Kurzsteckbrief für KI-Suchen (ChatGPT, Perplexity, Gemini), aus
# denselben Titeln und Beschreibungen erzeugt wie die Seiten selbst. Wirkt wie
# robots.txt erst an der Wurzel der Produktivdomain.
def llms_txt():
 b=BUSINESS
 zeilen=['# Klartext Digital','',
  '> Marketingagentur aus '+b.get('locality','Pratteln')+'. Schwerpunkt '+b.get('focus','Region Basel und Aargau')+', tätig in der ganzen Deutschschweiz: '
  'Webdesign, SEO, Social Media, Google und Meta Ads, Branding und Newsletter, im Abo oder als Projekt.','']
 if b:zeilen+=['Firma: '+b['name']+(' ('+b['legal_status']+')' if b.get('legal_status') else ''),'Adresse: '+b['street']+', '+b['postal_code']+' '+b['locality']+', Schweiz','E-Mail: '+b['email'],'Öffnungszeiten: Montag bis Freitag, '+b.get('opens','')+' bis '+b.get('closes','')+' Uhr','Schwerpunkt: '+b.get('focus',''),'Einzugsgebiet: ganze Deutschschweiz ('+', '.join(b['area_served'])+')','']
 gruppen=[('Leistungen',['marketing-abo/','projektarbeit/','webdesign/','seo/','social-media/','performance-marketing/','branding/','email-marketing/','website-betreuung/']),
  ('Leitfäden',sorted(r for r in META if r.startswith('blog/') and r!='blog/')),
  ('Über uns',['ueber-uns/','projekte/','impressum/'])]
 for name,routen in gruppen:
  zeilen.append('## '+name)
  for r in routen:
   if r in META:zeilen.append('- ['+META[r][0].split(' | ')[0]+']('+BASE+r+'): '+META[r][1])
  zeilen.append('')
 return '\n'.join(zeilen)
(OUT/'llms.txt').write_text(llms_txt())
(OUT/'.nojekyll').touch()
# GitHub Pages serves this document with HTTP 404 at any missing path.
# Absolute asset/navigation URLs also work when that path is deeply nested.
error_html=f'''<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Seite nicht gefunden | Klartext Digital</title><meta name="robots" content="noindex, follow"><meta name="description" content="Diese Seite wurde nicht gefunden. Zur Startseite oder zu den Leistungen von Klartext Digital."><link rel="canonical" href="{BASE}404.html"><link rel="stylesheet" href="{BASE}stil.css"><link rel="stylesheet" href="{BASE}seo.css"></head><body><main><section class="unter unter--eng"><p class="brush">404</p><h1 class="seo-h1">Hier geht es nicht weiter.</h1><p>Die Adresse stimmt nicht oder die Seite wurde verschoben.</p><p><a class="knopf knopf--akzent" href="{BASE}">Zur Startseite</a></p><nav class="seo-offer-nav" aria-label="Weitere Seiten"><a href="{BASE}marketing-abo/">Marketing im Abo</a><a href="{BASE}projektarbeit/">Projektarbeit</a><a href="{BASE}blog/">Blog</a></nav></section></main></body></html>'''
(OUT/'404.html').write_text(error_html)
(OUT/'build-manifest.json').write_text(json.dumps(sorted(str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()),indent=2)+'\n')
(ROOT/'docs/URL-MAP.json').write_text(json.dumps({k:BASE+v for k,v in {**ROUTES,**ALIASES}.items()},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(ROUTES)} pages and legacy redirects. Indexable sitemap entries: {len(paths)}. Output: {OUT}')
