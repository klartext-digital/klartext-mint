(() => {
const form = document.getElementById('anfrage');
if (!form) return;
const types = {abo: 'Laufendes Marketing im Abo', projekt: 'Ein einzelnes Projekt', team: 'Unser Marketingteam ergänzen'};
const requested = new URLSearchParams(location.search).get('anliegen');
if (Object.hasOwn(types, requested)) form.elements.anliegen.value = requested;
const result = document.getElementById('anfrage-ergebnis');
form.addEventListener('input', () => { result.hidden = true; });
form.addEventListener('submit', (event) => {
event.preventDefault();
if (!form.reportValidity()) return;
const value = name => form.elements[name].value.trim();
for (const name of ['vorhaben', 'ziel']) {
if (!value(name)) {
form.elements[name].setCustomValidity('Bitte beschreibt diesen Punkt kurz.');
form.elements[name].reportValidity();
return;
}
}
const selected = types[value('anliegen')];
const text = ['Anliegen: ' + selected, '', 'Vorhaben:', value('vorhaben'), '', 'Gewünschtes Ergebnis:', value('ziel'), '', 'Vorhandene Grundlagen / Rahmen:', value('rahmen') || 'Noch offen'].join('\n');
document.getElementById('briefing-text').value = text;
document.getElementById('briefing-mail').href = 'mailto:hallo@klartext-digital.ch?subject=' + encodeURIComponent('Anfrage: ' + selected) + '&body=' + encodeURIComponent(text);
document.getElementById('briefing-status').textContent = 'Briefing vorbereitet. Es wurde noch nichts gesendet.';
result.hidden = false;
document.getElementById('briefing-titel').focus();
window.dispatchEvent(new CustomEvent('klartext:interaction', {detail: {event: 'briefing_prepared', path: location.pathname, offer: value('anliegen')}}));
});
form.addEventListener('input', event => event.target.setCustomValidity?.(''));
document.getElementById('briefing-kopieren').addEventListener('click', async () => {
const text = document.getElementById('briefing-text');
try {
await navigator.clipboard.writeText(text.value);
document.getElementById('briefing-status').textContent = 'Briefing kopiert. Es wurde noch nichts gesendet.';
} catch {
text.focus(); text.select();
document.getElementById('briefing-status').textContent = 'Bitte kopiert den markierten Text mit der Kopierfunktion eures Geräts.';
}
});
})();
