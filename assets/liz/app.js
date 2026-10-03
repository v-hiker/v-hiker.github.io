'use strict';

const menu = document.querySelector('.liz-menu');
const nav = document.querySelector('.liz-nav');
const header = document.querySelector('.liz-header');
const items = [...document.querySelectorAll('.gallery-item')];
const filters = [...document.querySelectorAll('[data-filter]')];
const dialog = document.querySelector('#lightbox');
const picture = document.querySelector('#lightbox-image');
let visibleItems = items;
let selectedIndex = 0;
let previousOverflow = '';

function closeMenu() {
  menu.setAttribute('aria-expanded', 'false');
  menu.setAttribute('aria-label', '打开导航');
  nav.classList.remove('is-open');
}
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  menu.setAttribute('aria-label', open ? '关闭导航' : '打开导航');
  nav.classList.toggle('is-open', open);
});
nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('click', event => { if (!event.target.closest('.liz-header')) closeMenu(); });
window.addEventListener('scroll', () => header.classList.toggle('is-scrolled', window.scrollY > 12), { passive: true });

filters.forEach(button => button.addEventListener('click', () => {
  const category = button.dataset.filter;
  for (const filter of filters) {
    const active = filter === button;
    filter.classList.toggle('is-active', active);
    filter.setAttribute('aria-pressed', String(active));
  }
  for (const item of items) item.hidden = category !== 'all' && item.dataset.category !== category;
  document.querySelector('#gallery-count').textContent = items.filter(item => !item.hidden).length + ' 幅画面';
}));

function showImage(index) {
  selectedIndex = (index + visibleItems.length) % visibleItems.length;
  const item = visibleItems[selectedIndex];
  const original = item.querySelector('img');
  picture.src = original.currentSrc || original.src;
  picture.alt = original.alt;
  document.querySelector('#lightbox-title').textContent = item.dataset.title;
  document.querySelector('#lightbox-caption').textContent = item.dataset.caption;
  document.querySelector('#lightbox-count').textContent = (selectedIndex + 1) + ' / ' + visibleItems.length;
  const credit = document.querySelector('#lightbox-credit');
  credit.replaceChildren(document.createTextNode(item.dataset.credit + ' · '));
  const source = document.createElement('a');
  source.href = item.dataset.source;
  source.target = '_blank';
  source.rel = 'noopener noreferrer';
  source.textContent = '查看出处 ↗';
  credit.append(source);
}
items.forEach(item => item.addEventListener('click', () => {
  visibleItems = items.filter(other => !other.hidden);
  showImage(visibleItems.indexOf(item));
  previousOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  dialog.showModal();
}));
document.querySelector('.lightbox-close').addEventListener('click', () => dialog.close());
document.querySelector('.lightbox-prev').addEventListener('click', () => showImage(selectedIndex - 1));
document.querySelector('.lightbox-next').addEventListener('click', () => showImage(selectedIndex + 1));
dialog.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
dialog.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const rect = dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeMenu();
  if (!dialog.open) return;
  if (event.key === 'ArrowLeft') { event.preventDefault(); showImage(selectedIndex - 1); }
  if (event.key === 'ArrowRight') { event.preventDefault(); showImage(selectedIndex + 1); }
});
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      for (const link of nav.querySelectorAll('a')) {
        if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      }
    }
  }, { rootMargin: '-15% 0px -60% 0px' });
  for (const id of ['about', 'duet', 'worlds', 'music', 'gallery']) observer.observe(document.querySelector('#' + id));
}
