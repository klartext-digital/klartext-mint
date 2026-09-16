function calculateBudget(project, monthly, months) {
if (![project, monthly, months].every(Number.isFinite) || project < 0 || monthly < 0 || !Number.isInteger(months) || months < 1 || months > 120 || project > 100000000 || monthly > 1000000) {
throw new RangeError('Ungültige Budgetangaben');
}
return (Math.round(project * 100) + Math.round(monthly * 100) * months) / 100;
}
if (typeof module !== 'undefined') module.exports = {calculateBudget};
if (typeof document !== 'undefined') {
const form = document.getElementById('budget-form');
form?.addEventListener('submit', event => {
event.preventDefault();
if (!form.reportValidity()) return;
const total = calculateBudget(Number(form.elements.projekt.value), Number(form.elements.betrieb.value), Number(form.elements.monate.value));
const money = new Intl.NumberFormat('de-CH', {style: 'currency', currency: 'CHF'}).format(total);
document.getElementById('budget-ergebnis').textContent = money + ' Gesamtkosten über ' + form.elements.monate.value + ' Monate auf Basis eurer Eingaben.';
window.dispatchEvent(new CustomEvent('klartext:interaction', {detail: {event: 'budget_calculated', path: location.pathname}}));
});
form?.addEventListener('input', () => { document.getElementById('budget-ergebnis').textContent = 'Eingaben geändert. Bitte neu berechnen.'; });
}
