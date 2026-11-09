#!/usr/bin/env node
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
for (const [slug, first, second] of [['color-converter','convert','palette'], ['ip-calculator','ipv4','ipv6'], ['cron','visual','manual']]) {
  const html = fs.readFileSync(path.join(__dirname, '../tools/it/' + slug + '.html'), 'utf8');
  const dom = new JSDOM(html, { url: 'https://toolbox.local/', runScripts: 'outside-only' });
  const w = dom.window;
  const start = html.indexOf('function switchTab('), end = html.indexOf('\nfunction ', start + 10);
  assert(start >= 0 && end > start, slug);
  w.updatePalette = w.calcContrast = w.renderCommonColors = w.renderHistory = w.buildMaskTable = w.updateNextTimes = () => {};
  w.eval(html.slice(start, end));
  for (const target of [second, first]) {
    w.switchTab(target); // no browser global event
    assert(w.document.querySelector('.tab[data-tab="' + target + '"]').classList.contains('active'), slug + ': tab ' + target);
    assert(w.document.getElementById('tab-' + target).classList.contains('active'), slug + ': pane ' + target);
    assert.strictEqual(w.document.querySelectorAll('.tab[data-tab].active').length, 1, slug + ': active tabs');
  }
  if (slug === 'ip-calculator') {
    const a = html.indexOf('function switchTabWithIndex('), b = html.indexOf('\nfunction ', a + 10);
    w.eval(html.slice(a, b));
    w.switchTabWithIndex('ipv6');
    assert(w.document.querySelector('.tab[data-tab="ipv6"]').classList.contains('active'));
    assert(w.document.getElementById('tab-ipv6').classList.contains('active'));
  }
  w.close();
}
console.log('IT tabs: explicit target and programmatic switches passed for all three tools');
