/* aditi gargeshwari — sage desktop theme */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- scroll reveals --------------------------------------------------- */
  var targets = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window) || reduceMotion) {
    targets.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -6% 0px' });
    targets.forEach(function (el) { io.observe(el); });
  }

  /* ---- portfolio grid, rendered from assets/js/projects.js ------------- */
  var grid = document.getElementById('projectGrid');

  if (grid && Array.isArray(window.PROJECTS)) {
    var LABEL = { live: 'visit site', writeup: 'read more', repo: 'view code' };

    var el = function (tag, cls, text) {
      var n = document.createElement(tag);
      if (cls) n.className = cls;
      if (text != null) n.textContent = text;
      return n;
    };

    window.PROJECTS.forEach(function (p) {
      var links = p.links || {};
      var kind = links.live ? 'live' : links.writeup ? 'writeup' : links.repo ? 'repo' : null;
      var href = kind ? links[kind] : null;

      // keep-case so everything authored in projects.js renders verbatim
      var card = el(href ? 'a' : 'div', 'card keep-case');
      if (href) {
        card.href = href;
        if (/^https?:/i.test(href)) { card.target = '_blank'; card.rel = 'noopener'; }
      } else {
        // no link, but keyboard users still need a way to reveal the description
        card.tabIndex = 0;
      }

      var bar = el('span', 'card__bar');
      var icon = el('img');
      icon.src = p.icon; icon.alt = ''; icon.width = 16; icon.height = 16;
      bar.append(icon, el('span', null, p.file || p.slug + '.exe'));
      var close = el('span', 'win__btn win__btn--close');
      close.setAttribute('aria-hidden', 'true');
      close.appendChild(el('i'));
      bar.appendChild(close);

      var art = el('span', 'card__thumb');
      var cover = el('img', 'shot');
      cover.src = p.cover; cover.alt = ''; cover.loading = 'lazy';
      art.appendChild(cover);

      var overlay = el('span', 'card__overlay');
      overlay.appendChild(el('span', 'card__overlay-text', p.description));
      if (kind) overlay.appendChild(el('span', 'card__more', LABEL[kind] + ' \u2192'));
      art.appendChild(overlay);

      var body = el('span', 'card__body');
      body.appendChild(el('span', 'card__title', p.name));
      body.appendChild(el('span', 'card__meta', p.tagline));

      var status = el('span', 'card__status', p.status);
      if (links.live) status.classList.add('card__status--live');
      body.appendChild(status);

      if (p.tags && p.tags.length) {
        var tags = el('span', 'card__tags');
        p.tags.forEach(function (t) { tags.appendChild(el('span', null, t)); });
        body.appendChild(tags);
      }

      // touch devices get the description inline; css hides this where hover exists
      body.appendChild(el('span', 'card__desc', p.description));

      card.append(bar, art, body);
      grid.appendChild(card);
    });

    var count = document.querySelector('[data-project-count]');
    if (count) {
      var n = window.PROJECTS.length;
      count.textContent = n + (n === 1 ? ' item' : ' items');
    }
  }

  /* ---- taskbar clock ---------------------------------------------------- */
  var clock = document.querySelector('[data-clock]');
  if (clock) {
    var tick = function () {
      var d = new Date();
      var h = d.getHours();
      var m = String(d.getMinutes()).padStart(2, '0');
      var ampm = h < 12 ? 'am' : 'pm';
      h = h % 12 || 12;
      clock.textContent = h + ':' + m + ' ' + ampm + ' local';
    };
    tick();
    setInterval(tick, 30000);
  }
})();
