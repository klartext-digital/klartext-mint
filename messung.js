/* Local event contract for a future consent-aware analytics adapter.
   No cookies, storage, third-party tags, requests, form values or query strings.
   An interaction is not a received lead. Only a delivery-confirming backend may
   emit a future lead_received event. */
(() => {
  const allowed = new Set(['abo_explore', 'project_explore', 'abo_inquiry', 'project_inquiry', 'strategy_inquiry', 'content_inquiry', 'webdesign_inquiry', 'mail_open']);
  document.addEventListener('click', event => {
    const element = event.target.closest?.('[data-event]');
    if (!element || !allowed.has(element.dataset.event)) return;
    window.dispatchEvent(new CustomEvent('klartext:interaction', {detail: {event: element.dataset.event, path: location.pathname}}));
  });
})();
