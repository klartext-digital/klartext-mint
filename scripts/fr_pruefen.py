#!/usr/bin/env python3
"""Vergleicht deutsche Quelle und franzoesische Fassung.

Aufruf (im Ordner klartext-mint):  python3 fr_pruefen.py fr/seo/index.html [weitere ...]
Ohne Argumente: alle Dateien unter fr/.

1. GERUEST: Folge aller Tags mit allen nicht uebersetzbaren Attributen muss identisch sein.
2. RESTDEUTSCH: sichtbare Texte, die noch nach Deutsch aussehen.
3. GEDANKENSTRICHE: ' – ' oder '—' im franzoesischen Text sind verboten.
"""
import re, sys
from pathlib import Path
from html.parser import HTMLParser

FREI = {'alt', 'title', 'aria-label', 'placeholder', 'data-text', 'data-wort'}

class Geruest(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []; self.texte = []; self.stapel = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        meta_text = tag == 'meta' and any(k in (a.get('name', '') + a.get('property', '')) for k in ('description', 'title'))
        # Google-Hilfelinks duerfen die Sprache wechseln (hl=de zu hl=fr).
        attrs = [(k, re.sub(r'([?&]hl=)fr\b', r'\1de', v) if k == 'href' and v else v) for k, v in attrs]
        fest = tuple(sorted((k, v) for k, v in attrs if k not in FREI and not (meta_text and k == 'content')))
        self.tags.append((tag, fest, self.getpos()[0]))
        for k in FREI & a.keys():
            self.texte.append(a[k] or '')
        if meta_text: self.texte.append(a.get('content') or '')
        if tag in ('script', 'style'): self.stapel.append(tag)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        self.tags.append(('/' + tag, (), self.getpos()[0]))
        if self.stapel and self.stapel[-1] == tag: self.stapel.pop()
    def handle_data(self, d):
        if not self.stapel and d.strip(): self.texte.append(d)

DEUTSCH = re.compile(r'\b(und|oder|nicht|euch|euer|eure|eurem|euren|eurer|ihr|wir|uns|unser|unsere|ist|sind|wird|werden|der|die|das|den|dem|ein|eine|einen|einem|mit|für|auf|von|zu|bei|nach|wie|was|wer|auch|noch|schon|dass|kein|keine|sich|Sie|Ihr|Ihre|über|vor|zum|zur|im|am|es|so|nur|aber)\b')

def lies(p):
    g = Geruest(); g.feed(Path(p).read_text()); return g

def pruefe(fr):
    de = Path(str(fr)[3:])
    a, b = lies(de), lies(fr)
    fehler = []
    for i, (x, y) in enumerate(zip(a.tags, b.tags)):
        if x[0] == 'html': continue
        if x[:2] != y[:2]:
            fehler.append(f'GERUEST weicht ab ab Zeile DE {x[2]} / FR {y[2]}: DE {x[0]} {dict(x[1])} | FR {y[0]} {dict(y[1])}')
            break
    if len(a.tags) != len(b.tags) and not fehler:
        fehler.append(f'GERUEST: Anzahl Tags DE {len(a.tags)} / FR {len(b.tags)}')
    rest = []
    for t in b.texte:
        t = ' '.join(t.split())
        treffer = DEUTSCH.findall(t)
        if len(treffer) >= 2 or (len(t.split()) <= 4 and treffer and t not in ('Klartext Digital GmbH',)):
            rest.append(t[:110])
    for t in rest[:25]:
        fehler.append('RESTDEUTSCH? ' + t)
    for t in b.texte:
        if ' – ' in t or '—' in t or ' - ' in t:
            fehler.append('GEDANKENSTRICH: ' + ' '.join(t.split())[:110])
    if not re.search(r'<html lang="fr"', Path(fr).read_text()): fehler.append('html lang ist nicht "fr"')
    return fehler

dateien = sys.argv[1:] or [str(p) for p in sorted(Path('fr').rglob('*.html'))]
alles_gut = True
for f in dateien:
    f = f if f.startswith('fr/') else 'fr/' + f
    e = pruefe(f)
    print(('OK   ' if not e else 'FEHLT') + ' ' + f)
    for z in e: print('     ' + z)
    alles_gut &= not e
sys.exit(0 if alles_gut else 1)
