// 两态锁：第 32 批 年金净单保费「NSP ÷ 12」不再标成月缴保费
// 用法：node scripts/_verify_insurance_batch_anp32.mjs [--head]
import { JSDOM } from 'jsdom';
import { execSync } from 'child_process';
import fs from 'fs';

const head = process.argv.includes('--head');
let failures = 0;
const assert = (cond, msg) => { if (!cond) { console.log('  ✗ ' + msg); failures++; } else { console.log('  ✓ ' + msg); } };
const norm = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
const CJK = /[一-鿿　-〿＀-￯]/;
const rd = (f) => head
  ? execSync(`git show HEAD:${f}`, { maxBuffer: 64 * 1024 * 1024 }).toString()
  : fs.readFileSync(f, 'utf8');
const json = (f) => JSON.parse(rd(f));

const NEW_LABEL = '12 期无息均摊 (元)';
const OLD_LABEL = '月均摊保费';
const NEW_NOTE = '「12 期无息均摊」只是把 NSP 按 12 等分，未计利息、费用、缴费期限与生存概率，不等于实际月缴保费。';

console.log('— 年金净单保费：12 期无息均摊表述 —');
const raw = rd('tools/insurance/annuity-nsp.html');
const ctx = { table: [], hist: [] };
const dom = new JSDOM(raw, {
  runScripts: 'dangerously',
  url: 'https://example.test/',
  beforeParse(w) {
    w.ToolBox = {
      setResult(id, h) { const e = w.document.getElementById(id); if (e) e.innerHTML = String(h); },
      showToast() {}, showError() {}, downloadText() {}, copyText() {},
      formatNumber(n, d) { const v = Number(n); if (!isFinite(v)) return String(n); return v.toFixed(typeof d === 'number' ? d : 2); }
    };
    w.i18nText = (k) => String(k);
    w.TBKit = {
      util: { isEn: () => false, diffBox() {}, exportTable() {}, exportCsv() { return true; } },
      history: { record(r) { ctx.hist.push(r || {}); }, list: () => [], last: () => null, mount() {}, clear() {} },
      matrix: {
        table(host, opt) {
          const el = w.document.querySelector(host);
          const rows = (opt && opt.rows) || [];
          ctx.table = rows.map(r => (r || []).map(c => String(c == null ? '' : c)));
          if (el) el.innerHTML = '<table><tbody>' + rows.map(r =>
            '<tr>' + r.map(c => '<td>' + c + '</td>').join('') + '</tr>'
          ).join('') + '</tbody></table>';
        }
      },
      chart: { line() {}, bar() {} },
      preset: { bar() {} }
    };
  }
});
const w = dom.window;
await new Promise(r => { if (w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
await new Promise(r => setTimeout(r, 50));

const fq = norm(w.document.querySelector('.formula-eq') && w.document.querySelector('.formula-eq').textContent);
assert(/12 期无息均摊参考值 = NSP ÷ 12/.test(fq), `公式框应改写为 12 期无息均摊参考值；实际=「${fq.slice(0, 200)}」`);
assert(/不等于实际月缴保费/.test(fq) && /不含利息、费用、缴费期限与生存概率/.test(fq),
  `公式框应明确「不等于实际月缴保费」及缺失假设；实际=「${fq.slice(0, 200)}」`);
assert(!/月均摊保费 = NSP ÷ 12|月均摊值用于缴费节奏参考/.test(fq), '公式框不得再称「月均摊保费 / 缴费节奏参考」');

const lis = Array.from(w.document.querySelectorAll('.tool-notes ul li')).map(e => norm(e.textContent));
assert(lis.includes(NEW_NOTE), `计算说明应补第 3 条澄清；实际=${JSON.stringify(lis)}`);
assert(!lis.some(x => x.includes(OLD_LABEL)), `计算说明不得再含「${OLD_LABEL}」；实际=${JSON.stringify(lis)}`);

const out = () => norm(w.document.getElementById('result') && w.document.getElementById('result').textContent);
w.resetForm();
assert(out().includes(NEW_LABEL) && !out().includes(OLD_LABEL), `结果区标签应改为「${NEW_LABEL}」；实际=「${out().slice(0, 180)}」`);
assert(/1250\.00/.test(out()), `默认 NSP=15000 时 12 期均摊应为 1250.00（数值不变）；实际=「${out().slice(0, 180)}」`);
const flat = (ctx.table || []).map(r => r.join(' | ')).join(' || ');
assert(flat.includes(NEW_LABEL) && !flat.includes(OLD_LABEL), `明细表标签应同步；实际=${flat.slice(0, 200)}`);

// 图表系列名（静态脚本串）不得再写 Monthly equivalent / 月均摊保费
assert(raw.includes("'12-period interest-free split (¥)'") && !raw.includes("'Monthly equivalent (¥)'"),
  '图表英文系列名应改为 12-period interest-free split');
assert(!raw.includes("'月均摊保费 (元)'") && raw.includes("'" + NEW_LABEL + "'"),
  '图表中文系列名应改为 12 期无息均摊 (元)');

// 运行期数值不变：注入 b=42 / ax=42 → 147.00
const set = (id, v) => { const e = w.document.getElementById(id); if (e) e.value = String(v); };
set('b', 42); set('ax', 42); w.calcTool();
assert(/147\.00/.test(out()), `注入 42/42 时 12 期均摊应为 147.00；实际=「${out().slice(0, 180)}」`);

// 英文 map：键 = 中文源串，值无 CJK；旧键已删
const m = json('i18n/tools/en/insurance/annuity-nsp.json').map;
assert(!!m[fq] && !CJK.test(m[fq]), '英文 map 应含与 HTML 逐字一致的新 formula-eq 键且值无 CJK');
assert(!!m[NEW_LABEL] && !CJK.test(m[NEW_LABEL]), `英文 map 应含新标签键；实际=${m[NEW_LABEL]}`);
assert(!!m[NEW_NOTE] && !CJK.test(m[NEW_NOTE]), `英文 map 应含新计算说明键；实际=${String(m[NEW_NOTE]).slice(0, 80)}`);
assert(!Object.keys(m).some(k => k.includes('月均摊保费')), '英文 map 不得残留旧「月均摊保费」键');
assert(/NOT the actual monthly premium/.test(m[fq]), '英文公式框应明确不是实际月缴保费');

// 行业元数据 note 两处同步
const ind = json('i18n/tools/insurance.json')['annuity-nsp'];
assert(ind.note.includes(NEW_NOTE) && ind['zh-CN'].note.includes(NEW_NOTE),
  'i18n/tools/insurance.json 的 note 两处副本应同步新说明');

// 用例同步：auto 锚点不得再锚定旧标签
const vc = rd('scripts/verify_insurance_calc.js');
assert(vc.includes('147.00 12 期无息均摊 (元)') && !vc.includes('147.00 月均摊保费'),
  'verify_insurance_calc.js 的 auto 用例锚点应随标签同步');

dom.window.close();
console.log(head ? `[HEAD] ${failures} FAIL` : `[当前] 年金净单保费表述锁 ${failures === 0 ? 'PASS' : 'FAIL (' + failures + ')'}`);
process.exit(failures ? 1 : 0);
