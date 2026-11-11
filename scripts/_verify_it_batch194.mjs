// 第194批 · IT-N117/N118 base58 解码历史 + deep-dive 示例纠错（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/base58-encode.html';
const ENFILE = process.env.TB_EN || 'i18n/tools/en/it/base58-encode.json';
const DDFILE = process.env.TB_DD || 'i18n/tools/content_deepdive.json';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 130) : '')); }

let isEn = false;
let history = [];
let presetCfg = null;
const alerts = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/base58-encode.html',
  beforeParse(w) {
    w.alert = m => alerts.push(String(m));
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {} };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: { bar(sel, items, cb) { presetCfg = { sel, items, cb }; } },
      history: {
        list() { return history; },
        last() { return history.length ? history[history.length - 1].d : null; },
        record(r) { history.push({ t: Date.now(), d: r }); },
        mount() {},
        clear() { history = []; }
      }
    };
  }
});
const w = dom.window;
const d = w.document;
function fire(n) { d.dispatchEvent(new w.Event(n, { bubbles: true })); }
function enc(v, variant) {
  if (variant) d.getElementById('variant').value = variant;
  d.getElementById('input').value = v;
  d.getElementById('output').value = 'SENTINEL';
  w.eval('__base58_encode_last=0;enc()');
  return d.getElementById('output').value;
}
function dec(v, variant) {
  if (variant) d.getElementById('variant').value = variant;
  d.getElementById('input').value = v;
  d.getElementById('output').value = 'SENTINEL';
  w.eval('__base58_encode_last=0;dec()');
  return d.getElementById('output').value;
}

// 判别1：解码路径入历史并带方向/variant（IT-N117）
fire('DOMContentLoaded');
history = [];
const dOut = dec('9Ajdvzr', 'bitcoin');
check('解码真出 Hello', dOut === 'Hello', dOut);
check('解码产生历史', history.length === 1, 'n=' + history.length);
check('解码方向字段', history.length === 1 && history[0].d['方向'] === '解码', JSON.stringify(history[0] && history[0].d));
check('解码历史含 variant', history.length === 1 && history[0].d.variant === 'bitcoin', JSON.stringify(history[0] && history[0].d));
history = [];
const eOut = enc('Hello', 'bitcoin');
check('编码真出 9Ajdvzr', eOut === '9Ajdvzr', eOut);
check('编码方向字段', history.length === 1 && history[0].d['方向'] === '编码', JSON.stringify(history[0] && history[0].d));
history = [];
dec('9Ajdvzr', 'bitcoin');
dec('9Ajdvzr', 'bitcoin');
check('同输入同方向不重复', history.length === 1, 'n=' + history.length);

// 判别2：deep-dive 示例与页面算法一致（IT-N118）
const bytes = new Uint8Array([72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100]); // Hello World
const real = {};
for (const k of ['bitcoin', 'ripple', 'flickr']) {
  d.getElementById('variant').value = k;
  real[k] = w.eval('encodeBase58(new Uint8Array([72,101,108,108,111,32,87,111,114,108,100]))');
}
check('bitcoin 样例复算', real.bitcoin === 'JxF12TrwUP45BMd', real.bitcoin);
check('ripple 样例复算', real.ripple === 'JxErpTiA7PhnBMd', real.ripple);
check('flickr 样例复算', real.flickr === 'iXf12sRWto45bmC', real.flickr);
const exNode = d.querySelector ? d.querySelector('.dd-ex-body') : null;
const exText = exNode ? String(exNode.textContent) : '';
check('页面示例含 bitcoin 真值', exText.indexOf('JxF12TrwUP45BMd') >= 0, exText.slice(0, 130));
check('页面示例含 ripple 真值', exText.indexOf('JxErpTiA7PhnBMd') >= 0);
check('页面示例含 flickr 真值', exText.indexOf('iXf12sRWto45bmC') >= 0);
check('页面示例无旧错误值', exText.indexOf('2NEwd2UZ') < 0);

// 判别3：权威源与 en JSON 三源同步
const dd = JSON.parse(fs.readFileSync(DDFILE, 'utf8'));
const ddStr = JSON.stringify(dd);
check('权威源含正确样例', ddStr.indexOf('JxF12TrwUP45BMd') >= 0 && ddStr.indexOf('JxErpTiA7PhnBMd') >= 0 && ddStr.indexOf('iXf12sRWto45bmC') >= 0);
check('权威源无旧错误值', ddStr.indexOf('2NEwd2UZ') < 0);
const en = JSON.parse(fs.readFileSync(ENFILE, 'utf8'));
const enKey = Object.keys(en.map).find(k => k.indexOf('输入 `Hello World`') === 0);
check('en 映射键已更新', !!enKey && enKey.indexOf('2NEwd2UZ') < 0 && enKey.indexOf('JxF12TrwUP45BMd') >= 0, enKey ? enKey.slice(0, 100) : 'no key');
check('en 映射值已更新', !!enKey && en.map[enKey].indexOf('JxF12TrwUP45BMd') >= 0 && en.map[enKey].indexOf('2NEwd2UZ') < 0, enKey ? en.map[enKey].slice(0, 100) : 'no value');

// 判别4：英文态方向与预设仍正常
isEn = true;
history = [];
dec('9Ajdvzr', 'bitcoin');
check('英文态方向 Encode/Decode', history.length === 1 && history[0].d['方向'] === 'Decode', JSON.stringify(history[0] && history[0].d));
isEn = false;
check('预设仍为 4 条', presetCfg && presetCfg.items.length === 4, presetCfg && presetCfg.items.map(x => x.label).join('/'));

// 判别5：状态链 合法 → 非法 → 恢复
check('状态链合法', dec('9Ajdvzr', 'bitcoin') === 'Hello');
alerts.length = 0;
check('状态链非法', dec('0OIl', 'bitcoin') === 'SENTINEL' && alerts.length > 0, alerts.join('|'));
check('状态链恢复', dec('9Ajdvzr', 'bitcoin') === 'Hello');

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
