// 第273批 JSDOM 验证：IT-N318 八进制非法段拒绝（状态校正+英文提示）/ IT-N319 随机字符串重置与预设默认
// 用法: node scripts/_verify_it_batch273.mjs [OLD_DIR]
import fs from 'fs';
import { webcrypto } from 'node:crypto';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const page = (rel) => OLD ? `${OLD}/tools/it/${rel}` : `tools/it/${rel}`;
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
const baseStubs = (w, extra = {}) => {
  w.ToolBox = { showToast() {}, copyText() {}, exportCsv() {} };
  w.TBKit = Object.assign({
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {} }, matrix: { table() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {} },
    preset: { bar() {} },
  }, extra);
  w.i18nText = (z) => z;
  if (extra.crypto) Object.defineProperty(w, 'crypto', { value: extra.crypto, configurable: true });
};

// ---------- IT-N318：octal-encode ----------
{
  const alerts = [];
  const dom = new JSDOM(fs.readFileSync(page('octal-encode.html'), 'utf8'), {
    runScripts: 'dangerously', url: 'https://x.com/octal-encode.html',
    beforeParse(w) {
      baseStubs(w);
      w.alert = (m) => alerts.push(String(m));
    },
  });
  const w = dom.window, d = w.document;
  d.getElementById('input').value = '078';
  w.dec();
  check('N318 078 被整段拒绝（回归锚）', alerts.length === 1 && alerts[0].indexOf('非法八进制数') >= 0 && d.getElementById('output').value === '', 'alert=' + alerts.join('|'));
  alerts.length = 0;
  d.getElementById('input').value = '378';
  w.dec();
  check('N318 378 被整段拒绝（回归锚）', alerts.length === 1 && alerts[0].indexOf('378') >= 0 && d.getElementById('output').value === '', 'alert=' + alerts.join('|'));
  alerts.length = 0;
  d.getElementById('input').value = '101 102';
  w.dec();
  check('N318 合法八进制仍正常解码（回归锚）', d.getElementById('output').value === 'AB', 'out=' + d.getElementById('output').value);
  alerts.length = 0;
  w.TBKit.util.isEn = () => true;
  d.getElementById('input').value = '078';
  w.dec();
  check('N318 英文态非法输入提示无 CJK', alerts.length === 1 && /^Invalid octal number: 078$/.test(alerts[0]), 'alert=' + alerts.join('|'));
  check('N318 源码保留整段正则守卫', /\[0-7\]\{1,3\}/.test(fs.readFileSync(page('octal-encode.html'), 'utf8')));
}

// ---------- IT-N319：random-string ----------
{
  let presetList = null;
  const dom = new JSDOM(fs.readFileSync(page('random-string.html'), 'utf8'), {
    runScripts: 'dangerously', url: 'https://x.com/random-string.html',
    beforeParse(w) {
      baseStubs(w, {
        crypto: webcrypto,
        preset: { bar: (host, list, after) => { presetList = list; } },
      });
    },
  });
  const w = dom.window, d = w.document;
  await new Promise(r => setTimeout(r, 50)); // DOMContentLoaded boot 渲染预设
  const IDS = ['top_upper', 'top_lower', 'top_digit', 'top_sym'];
  const ids = () => IDS.filter(id => d.getElementById(id) && d.getElementById(id).checked);
  const result = () => String(d.getElementById('result').textContent || '');

  // 人为破坏状态后点重置：应恢复出厂默认并立即生成
  IDS.forEach(id => { d.getElementById(id).checked = false; });
  d.getElementById('len').value = '7';
  d.getElementById('cnt').value = '2';
  w.resetForm();
  check('N319 重置恢复 upper+lower+digit 三项', ids().join(',') === 'top_upper,top_lower,top_digit', 'ids=' + ids().join(','));
  check('N319 重置恢复 len=16/cnt=5', d.getElementById('len').value === '16' && d.getElementById('cnt').value === '5');
  check('N319 重置后立即生成示例（不再空字符集报错）', result().indexOf('生成 5 个随机字符串') >= 0 && result().indexOf('请至少选择一种字符集') < 0, 'head=' + result().slice(0, 30));

  check('N319 预设条已渲染（4 个预设）', !!presetList && presetList.length === 4, 'n=' + (presetList && presetList.length));
  if (presetList) {
    const groups = [['top_upper', 'top_lower', 'top_digit'], ['top_upper', 'top_lower'], ['top_upper', 'top_lower', 'top_digit', 'top_sym'], ['top_digit', 'top_sym']];
    let full = true, binary = true, groupOK = true;
    presetList.forEach((p, i) => {
      const v = p.values || {};
      if (!IDS.every(id => Object.prototype.hasOwnProperty.call(v, id))) full = false;
      IDS.forEach(id => { if (!['0', '1'].includes(String(v[id]))) binary = false; });
      IDS.forEach(id => { if (String(v[id]) !== (groups[i].includes(id) ? '1' : '0')) groupOK = false; });
    });
    check('N319 每个预设显式列出 4 个 checkbox', full);
    check('N319 预设值严格 0/1（无裸布尔）', binary);
    check('N319 默认参数预设只勾 upper+lower+digit', groupOK);
    // 从全勾选态切到 8 位大小写，验证旧勾选被清
    IDS.forEach(id => { d.getElementById(id).checked = true; });
    const p = presetList[1];
    IDS.forEach(id => { d.getElementById(id).checked = String(p.values[id]) === '1'; });
    check('N319 从全勾选切到 8 位大小写只留两项', ids().join(',') === 'top_upper,top_lower', 'ids=' + ids().join(','));
  }
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
