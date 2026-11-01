const menuButton = document.querySelector('.menu-button');
const nav = document.querySelector('.primary-nav');
const groups = [...document.querySelectorAll('.nav-group')];
const hoverNavigation = window.matchMedia('(min-width: 1181px) and (hover: hover)');
function setGroup(group, open) {
  group.classList.toggle('is-open', open);
  const button = group.querySelector('.dropdown-toggle');
  button.setAttribute('aria-expanded', String(open));
  const label = group.querySelector('.nav-group-heading > a').textContent;
  button.setAttribute('aria-label', `${open ? 'Hide' : 'Show'} ${label} services`);
}
function closeGroups(except) {
  groups.forEach(group => { if (group !== except) setGroup(group, false); });
}
menuButton?.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!open));
  menuButton.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
  nav.classList.toggle('open', !open);
  if (open) closeGroups();
});
groups.forEach(group => {
  const button = group.querySelector('.dropdown-toggle');
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') === 'true';
    closeGroups(group);
    setGroup(group, !open);
  });
  group.addEventListener('pointerenter', () => {
    if (hoverNavigation.matches) { closeGroups(group); setGroup(group, true); }
  });
  group.addEventListener('pointerleave', () => {
    if (hoverNavigation.matches && !group.contains(document.activeElement)) setGroup(group, false);
  });
  group.addEventListener('focusin', event => {
    if (event.target.matches('.nav-group-heading > a')) {
      closeGroups(group);
      if (window.matchMedia('(min-width: 1181px)').matches) setGroup(group, true);
    }
  });
  group.addEventListener('focusout', event => {
    if (!group.contains(event.relatedTarget)) setGroup(group, false);
  });
  group.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault(); event.stopPropagation(); setGroup(group, false); button.focus();
    }
  });
});
document.addEventListener('click', event => { if (!nav?.contains(event.target)) closeGroups(); });
nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  closeGroups();
  nav.classList.remove('open');
  menuButton?.setAttribute('aria-expanded', 'false');
  menuButton?.setAttribute('aria-label', 'Open menu');
}));
