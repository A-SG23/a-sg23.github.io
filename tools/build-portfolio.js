#!/usr/bin/env node
/* Writes the portfolio cards into portfolio.html as static HTML.

     node tools/build-portfolio.js

   assets/js/projects.js stays the single source of truth for project content.
   This bakes it into the page so the grid can never be empty — no dependency
   on JavaScript running, on a script loading, or on a cache being fresh.
   Run it after editing projects.js. */

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
global.window = {};
require(path.join(ROOT, "assets/js/projects.js"));
const PROJECTS = global.window.PROJECTS;

const LABEL = { live: "visit site", writeup: "read more", repo: "view code" };
const esc = (s) =>
  String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
           .replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function card(p) {
  const links = p.links || {};
  const kind = links.live ? "live" : links.writeup ? "writeup" : links.repo ? "repo" : null;
  const href = kind ? links[kind] : null;
  const external = href && /^https?:/i.test(href);

  const open = href
    ? `<a class="card keep-case" href="${esc(href)}"` +
      (external ? ` target="_blank" rel="noopener"` : "") + `>`
    // no link, but keyboard users still need to reach the description
    : `<div class="card keep-case" tabindex="0">`;
  const close = href ? "</a>" : "</div>";

  const tags = (p.tags || []).map((t) => `<span>${esc(t)}</span>`).join("");
  const more = kind ? `<span class="card__more">${LABEL[kind]} &rarr;</span>` : "";
  const live = links.live ? " card__status--live" : "";

  return `        ${open}
          <span class="card__bar">
            <img src="${esc(p.icon)}" alt="" width="16" height="16">
            <span>${esc(p.file || p.slug + ".exe")}</span>
            <span class="win__btn win__btn--close" aria-hidden="true"><i></i></span>
          </span>
          <span class="card__thumb">
            <img class="shot" src="${esc(p.cover)}" alt="" loading="lazy">
            <span class="card__overlay">
              <span class="card__overlay-text">${esc(p.description)}</span>
              ${more}
            </span>
          </span>
          <span class="card__body">
            <span class="card__title">${esc(p.name)}</span>
            <span class="card__meta">${esc(p.tagline)}</span>
            <span class="card__status${live}">${esc(p.status)}</span>
            <span class="card__tags">${tags}</span>
            <span class="card__desc">${esc(p.description)}</span>
          </span>
        ${close}`;
}

const file = path.join(ROOT, "portfolio.html");
let html = fs.readFileSync(file, "utf8");

const START = /(<!-- PROJECTS:START[\s\S]*?-->)[\s\S]*?(<!-- PROJECTS:END -->)/;
if (!START.test(html)) throw new Error("PROJECTS markers not found in portfolio.html");

html = html.replace(START, (_, a, b) =>
  `${a}\n${PROJECTS.map(card).join("\n\n")}\n        ${b}`);

const n = PROJECTS.length;
html = html.replace(/(<span class="win__cell" data-project-count>)[^<]*(<\/span>)/,
                    `$1${n} item${n === 1 ? "" : "s"}$2`);

fs.writeFileSync(file, html);
console.log(`wrote ${n} project card${n === 1 ? "" : "s"} into portfolio.html`);
