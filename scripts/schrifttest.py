"""Testseite schrifttest.html: echte Startseite plus Umschalter fuer die
Grundschrift. Titel (Fields Display) und Pinselschrift (Klartext Hand)
bleiben fest. Nur Vorschau, noindex, nicht in Sitemap oder Navigation."""
import re
from pathlib import Path

SCHRIFTEN = [
 ('Aktuell', None),
 ('DM Sans', 'DM Sans'), ('Inter', 'Inter'), ('Manrope', 'Manrope'),
 ('Figtree', 'Figtree'), ('Plus Jakarta Sans', 'Plus Jakarta Sans'),
 ('Outfit', 'Outfit'), ('Work Sans', 'Work Sans'), ('Instrument Sans', 'Instrument Sans'),
 ('Geist', 'Geist'), ('Albert Sans', 'Albert Sans'),
]

def baue(out: Path):
 s = (out/'index.html').read_text(encoding='utf-8')
 fam = '&'.join('family='+n.replace(' ', '+')+':wght@300;400;500;600;700;800' for _, n in SCHRIFTEN if n and n != 'Figtree')
 kopf = ('<meta name="robots" content="noindex, nofollow">'
  '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
  f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">'
  '<style>'
  '.stest{position:fixed;z-index:2147483000;left:50%;bottom:16px;transform:translateX(-50%);'
  'display:flex;gap:6px;align-items:center;max-width:calc(100vw - 24px);overflow-x:auto;scrollbar-width:none;'
  'padding:8px;border-radius:999px;background:rgb(14 13 11 / .92);box-shadow:0 14px 40px -12px rgb(0 0 0 / .6);'
  'font:600 13px/1 system-ui,-apple-system,sans-serif!important;color:#F7F7F5}'
  '.stest::-webkit-scrollbar{display:none}'
  '.stest b{padding:0 8px 0 10px;white-space:nowrap;font:inherit!important;opacity:.7}'
  '.stest button{all:unset;cursor:pointer;white-space:nowrap;padding:9px 13px;border-radius:999px;'
  'font-size:13px!important;line-height:1!important;color:#F7F7F5;background:rgb(247 247 245 / .08)}'
  '.stest button:hover{background:rgb(247 247 245 / .2)}'
  '.stest button[aria-pressed="true"]{background:#F5A524;color:#0E0D0B}'
  '</style>')
 s = re.sub(r'<meta name="robots"[^>]*>', '', s)
 s = s.replace('</head>', kopf+'</head>', 1)
 def _knopf(l, n):
  stil = ("'" + n + "'," if n else '') + 'system-ui'
  return '<button type="button" data-f="' + (n or '') + '" style="font-family:' + stil + '!important">' + l + '</button>'
 knoepfe = ''.join(_knopf(l, n) for l, n in SCHRIFTEN)
 leiste = f'<div class="stest" role="toolbar" aria-label="Schrift wählen"><b>Schrift</b>{knoepfe}</div>'
 js = r'''<script>
(function(){
 var FIX=/fields-display|Klartext Hand|Rock Salt/i, st=document.createElement('style');
 document.head.appendChild(st);
 function markieren(){document.querySelectorAll('body *').forEach(function(e){
  if(e.closest('.stest'))return;
  if(FIX.test(getComputedStyle(e).fontFamily))e.setAttribute('data-fix','');});}
 function setze(f){
  st.textContent=f?'body *:not([data-fix]):not([data-fix] *):not(.stest):not(.stest *){font-family:"'+f+'",system-ui,sans-serif!important;font-synthesis-weight:auto!important}':'';
  document.querySelectorAll('.stest button').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.f===f))});
  try{localStorage.setItem('schrifttest',f)}catch(e){}
  try{var u=new URL(location.href);if(f)u.searchParams.set('schrift',f);else u.searchParams.delete('schrift');history.replaceState(null,'',u)}catch(e){}
 }
 function los(){
  markieren();
  var f='';try{f=new URL(location.href).searchParams.get('schrift')||localStorage.getItem('schrifttest')||''}catch(e){}
  setze(f);
  document.querySelector('.stest').addEventListener('click',function(ev){var b=ev.target.closest('button');if(b)setze(b.dataset.f)});
 }
 (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){setTimeout(los,50)});
})();
</script>'''
 s = s.replace('</body>', leiste+js+'</body>', 1)
 (out/'schrifttest.html').write_text(s, encoding='utf-8')
