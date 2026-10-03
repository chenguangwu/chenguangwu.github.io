import { JSDOM } from 'jsdom';
import fs from 'fs';
import path from 'path';
import vm from 'vm';

const ROOT = path.dirname(path.dirname(new URL(import.meta.url).pathname));
function enData() {
  const ctx = { window: {} };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'js', 'tool-i18n-en.js'), 'utf8'), ctx);
  return ctx.window.__TI18N_EN || {};
}
function probePage(htmlPath, lang) {
  const rel = path.relative(ROOT, htmlPath).split(path.sep).join('/');
  const html = fs.readFileSync(htmlPath, 'utf8');
  const dom = new JSDOM(html, { url: 'https://toolbox.local/' + rel + '?lang=' + lang, runScripts: 'outside-only', pretendToBeVisual: true });
  const w = dom.window;
  let pending = 0;
  if (lang !== 'zh-CN') w.__TI18N_EN = enData();
  w.fetch = (u) => {
    const clean = decodeURIComponent(String(u).split('?')[0].split('#')[0]).replace(/^\/+/, '');
    const fp = path.join(ROOT, clean);
    pending++;
    return new Promise((resolve) => {
      fs.readFile(fp, 'utf8', (err, data) => {
        pending--;
        if (err) resolve({ ok: false, status: 404, json: async () => null, text: async () => '' });
        else resolve({ ok: true, status: 200, json: async () => JSON.parse(data), text: async () => data });
      });
    });
  };
  w.eval(fs.readFileSync(path.join(ROOT, 'js', 'i18n.js'), 'utf8'));
  w.eval(fs.readFileSync(path.join(ROOT, 'js', 'tool-i18n.js'), 'utf8'));
  return { w, getPending: () => pending };
}
const tick = (ms = 4) => new Promise((r) => setTimeout(r, ms));
async function settle(getPending, rounds = 60) {
  for (let i = 0; i < rounds; i++) { await tick(); if (getPending() === 0) { await tick(); if (getPending() === 0) return; } }
}

const targets = process.argv.slice(2);
for (const t of targets) {
  const [ind, slug] = t.split('/');
  const file = path.join(ROOT, 'tools', ind, slug + '.html');
  const { w, getPending } = probePage(file, 'en-US');
  await settle(getPending);
  console.log('==== ' + t + ' ====');
  for (const a of w.document.querySelectorAll('a.term-link')) {
    console.log('  TL: ' + a.textContent);
  }
  const el = w.document.querySelector('.dd-ex-body, .dd-faq dd, .info-box');
  if (el) console.log('  SAMPLE: ' + el.textContent.slice(0, 160));
  w.close();
}
