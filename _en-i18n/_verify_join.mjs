// 一次性校验：EN 态下打印深度解析区块的真实拼接文本（校验 term-link 拼接句的空格/语序）
// 用法：node _en-i18n/_verify_join.mjs <slug> [selector]
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { JSDOM } from 'jsdom';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(ROOT, 'js', 'tool-i18n-en.js'), 'utf8'), ctx);
const EN = ctx.window.__TI18N_EN || {};

function render(rel, lang) {
  const dom = new JSDOM(fs.readFileSync(path.join(ROOT, rel), 'utf8'), {
    url: 'https://toolbox.local/' + rel + '?lang=' + lang,
    runScripts: 'outside-only',
    pretendToBeVisual: true,
  });
  const w = dom.window;
  let pending = 0;
  w.__TI18N_EN = EN;
  w.fetch = (u) => {
    const clean = decodeURIComponent(String(u).split('?')[0].split('#')[0]).replace(/^\/+/, '');
    const fp = path.join(ROOT, clean);
    pending++;
    return new Promise((resolve) => {
      fs.readFile(fp, 'utf8', (err, data) => {
        pending--;
        if (err) return resolve({ ok: false, json: async () => null, text: async () => '' });
        resolve({ ok: true, json: async () => JSON.parse(data), text: async () => data });
      });
    });
  };
  w.eval(fs.readFileSync(path.join(ROOT, 'js', 'i18n.js'), 'utf8'));
  w.eval(fs.readFileSync(path.join(ROOT, 'js', 'tool-i18n.js'), 'utf8'));
  return { w, getPending: () => pending };
}
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
async function settle(g) {
  for (let i = 0; i < 60; i++) {
    await wait(4);
    if (g() === 0) { await wait(4); if (g() === 0) return; }
  }
}

const slug = process.argv[2];
const sel = process.argv[3] || '.deep-dive li, .deep-dive dd, .deep-dive .dd-ex-body, .deep-dive .dd-sum, .deep-dive .dd-lead, .tool-notes li';
const { w, getPending } = render('tools/sports/' + slug + '.html', 'en-US');
await settle(getPending);
let n = 0;
for (const el of w.document.querySelectorAll(sel)) {
  const s = (el.textContent || '').replace(/\s+/g, ' ').trim();
  if (s) { console.log('· ' + s); n++; }
}
console.log('[' + slug + '] ' + n + ' 条');
w.close();
