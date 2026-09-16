#!/usr/bin/env python3
"""Vorsichtiges Verkleinern von CSS und JS beim Bauen.

Die Quelldateien bleiben unveraendert und lesbar. Nur die Ausgabe in _site
wird verkleinert. Beide Verfahren sind bewusst zurueckhaltend gewaehlt:
lieber ein paar Bytes weniger sparen als ein kaputtes Layout riskieren.

CSS: kennt Zeichenketten, damit content:"/" nicht als Kommentar gilt.
     Abstaende werden nur um { } ; und , entfernt. Um : + - ~ > bleibt
     alles stehen, sonst zerbricht calc(100% + 10px) oder ein Selektor.

JS:  entfernt nur Zeilen, die vollstaendig Kommentar sind, sowie die
     Einrueckung. Zeilenenden bleiben erhalten, damit die automatische
     Semikolon-Ergaenzung von JavaScript sich nicht anders verhaelt.
     Kein Eingriff in Zeichenketten, regulaere Ausdruecke oder Code.
"""


def css(text):
    out = []
    i = 0
    n = len(text)
    quote = None
    while i < n:
        c = text[i]
        if quote:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in '"\'':
            quote = c
            out.append(c)
            i += 1
            continue
        if c == '/' and i + 1 < n and text[i + 1] == '*':
            ende = text.find('*/', i + 2)
            i = n if ende < 0 else ende + 2
            continue
        if c in ' \t\r\n\f':
            j = i
            while j < n and text[j] in ' \t\r\n\f':
                j += 1
            naechstes = text[j] if j < n else ''
            if out and out[-1] not in '{};,' and naechstes not in '{};,' and naechstes != '':
                out.append(' ')
            i = j
            continue
        out.append(c)
        i += 1
    s = ''.join(out)
    s = s.replace(';}', '}')
    return s.strip()


def js(text):
    zeilen = []
    im_block = False
    for roh in text.split('\n'):
        zeile = roh.strip()
        if im_block:
            if '*/' in zeile:
                rest = zeile.split('*/', 1)[1].strip()
                im_block = False
                if rest:
                    zeilen.append(rest)
            continue
        if zeile.startswith('/*'):
            if '*/' in zeile[2:]:
                rest = zeile[2:].split('*/', 1)[1].strip()
                if rest:
                    zeilen.append(rest)
            else:
                im_block = True
            continue
        if zeile.startswith('//'):
            continue
        if zeile:
            zeilen.append(zeile)
    return '\n'.join(zeilen) + '\n'
