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
