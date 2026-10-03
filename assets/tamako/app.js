'use strict';
const nav = document.querySelector('#site-nav');
const menu = document.querySelector('.menu-toggle');
const header = document.querySelector('.site-header');
const filters = [...document.querySelectorAll('[data-filter]')];
const galleryItems = [...document.querySelectorAll('.gallery-item')];
const lightbox = document.querySelector('#lightbox');
const lightboxImage = document.querySelector('#lightbox-image');
let activeIndex = 0;
let activeItems = galleryItems;
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
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
window.addEventListener('scroll', () => header.classList.toggle('is-scrolled', window.scrollY > 15), { passive: true });

function setFilter(category) {
  filters.forEach(button => {
    const selected = button.dataset.filter === category;
    button.classList.toggle('is-active', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
  galleryItems.forEach(item => { item.hidden = category !== 'all' && item.dataset.category !== category; });
  document.querySelector('#gallery-count').textContent = galleryItems.filter(item => !item.hidden).length + ' 幅画面';
}
filters.forEach(button => button.addEventListener('click', () => setFilter(button.dataset.filter)));
document.querySelectorAll('[data-gallery-filter]').forEach(link => {
  link.addEventListener('click', () => setFilter(link.dataset.galleryFilter));
});

function displayImage(index) {
  activeIndex = (index + activeItems.length) % activeItems.length;
  const item = activeItems[activeIndex];
  const sourceImage = item.querySelector('img');
  lightboxImage.src = sourceImage.currentSrc || sourceImage.src;
  lightboxImage.alt = sourceImage.alt;
  document.querySelector('#lightbox-title').textContent = item.dataset.title;
  document.querySelector('#lightbox-caption').textContent = item.dataset.caption;
  const credit = document.querySelector('#lightbox-credit');
  credit.replaceChildren(document.createTextNode(item.dataset.credit + ' · '));
  const sourceLink = document.createElement('a');
  sourceLink.href = item.dataset.source;
  sourceLink.target = '_blank';
  sourceLink.rel = 'noopener noreferrer';
  sourceLink.textContent = '查看出处 ↗';
  credit.append(sourceLink);
  document.querySelector('#lightbox-counter').textContent = (activeIndex + 1) + ' / ' + activeItems.length;
}
galleryItems.forEach(item => item.addEventListener('click', () => {
  activeItems = galleryItems.filter(element => !element.hidden);
  displayImage(activeItems.indexOf(item));
  previousOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  lightbox.showModal();
}));
document.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
document.querySelector('.lightbox-prev').addEventListener('click', () => displayImage(activeIndex - 1));
document.querySelector('.lightbox-next').addEventListener('click', () => displayImage(activeIndex + 1));
lightbox.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
lightbox.addEventListener('click', event => {
  if (event.target === lightbox) {
    const bounds = lightbox.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) lightbox.close();
  }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeMenu();
  if (!lightbox.open) return;
  if (event.key === 'ArrowLeft') { event.preventDefault(); displayImage(activeIndex - 1); }
  if (event.key === 'ArrowRight') { event.preventDefault(); displayImage(activeIndex + 1); }
});
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      nav.querySelectorAll('a').forEach(link => {
        const current = link.hash === '#' + entry.target.id;
        link.classList.toggle('is-current', current);
        if (current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }, { rootMargin: '-12% 0px -58% 0px', threshold: 0 });
  ['about', 'friends', 'street', 'stories', 'gallery'].forEach(id => observer.observe(document.getElementById(id)));
}
