// 第275批 JSDOM 验证：IT-N322 .env 唯一键与真实随机密钥 / IT-N323 昵称复制逐行分隔
// 用法: node scripts/_verify_it_batch275.mjs [OLD_DIR]
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
function stubs(w) {
  w.ToolBox = { showToast() {}, copyText() {}, exportCsv() {}, createTable() { return ''; } };
  w.TBKit = {
    util: { isEn: () => false, exportTable() {}, diffBox() {} },
    chart: { line() {} }, matrix: { table() {} },
    history: { list: () => [], last: () => null, record() {}, mount() {} },
    preset: { bar() {} },
  };
  w.i18nText = () => '';
  Object.defineProperty(w, 'crypto', { value: webcrypto, configurable: true });
}

// ---------- IT-N322：generator-16 ----------
{
  const dom = new JSDOM(fs.readFileSync(page('generator-16.html'), 'utf8'), {
    runScripts: 'dangerously', url: 'https://x.com/generator-16.html',
    beforeParse: stubs,
  });
  const w = dom.window, d = w.document;
  d.getElementById('cnt').value = '20';
  w.gen();
  const lines = (d.getElementById('res').textContent || '').split('\n').map(s => s.trim()).filter(Boolean);
  const keys = lines.map(s => s.split('=')[0]);
  const uniq = new Set(keys);
  check('N322 生成 20 行（回归锚）', lines.length === 20, 'n=' + lines.length);
  check('N322 20 个键全部唯一', uniq.size === 20, 'uniq=' + uniq.size);
  check('N322 超过 15 条用 _2 后缀消歧', keys.some(k => /_[2-9]$/.test(k)), 'keys=' + keys.slice(0, 6).join(','));
  const secrets = lines.filter(s => /^(JWT_SECRET|SESSION_SECRET|OPENAI_API_KEY|STRIPE_SECRET_KEY)/.test(s));
  check('N322 密钥类字段不再使用固定占位符', secrets.length > 0 && secrets.every(s => !/change-me-in-production|random-secret-string|sk-xxxxxxxx|sk_test_xxxxxxxx/.test(s)), 'sample=' + secrets[0]);
  check('N322 密钥类字段为安全随机 hex', secrets.length > 0 && secrets.every(s => /=(sk_test_|sk-)?[0-9a-f]{48,}$/.test(s)), 'sample=' + secrets[0]);
  w.gen();
  const lines2 = (d.getElementById('res').textContent || '').split('\n').map(s => s.trim()).filter(Boolean);
  const secrets2 = lines2.filter(s => /^(JWT_SECRET|SESSION_SECRET|OPENAI_API_KEY|STRIPE_SECRET_KEY)/.test(s));
  check('N322 连续两次生成密钥不同', secrets.join('|') !== secrets2.join('|'));
  check('N322 公式文案已同步唯一键/随机密钥', /唯一后缀/.test(fs.readFileSync(page('generator-16.html'), 'utf8')));
}

// ---------- IT-N323：gamertag-generator 复制逐行 ----------
{
  let copied = '';
  const dom = new JSDOM(fs.readFileSync(page('gamertag-generator.html'), 'utf8'), {
    runScripts: 'dangerously', url: 'https://x.com/gamertag-generator.html',
    beforeParse(w) {
      stubs(w);
      w.alert = () => {};
      Object.defineProperty(w.navigator, 'clipboard', {
        value: { writeText(t) { copied = String(t); return Promise.resolve(); } }, configurable: true,
      });
    },
  });
  const w = dom.window, d = w.document;
  d.getElementById('count').value = '3';
  w.generate();
  const rows = Array.from(d.getElementById('output').querySelectorAll('.code-row')).map(r => r.textContent || '');
  w.copyResult();
  check('N323 复制得到 3 行（回归锚）', rows.length === 3 && copied.split('\n').length === 3, 'copied=' + JSON.stringify(copied));
  check('N323 复制内容与每条 code-row 逐行一致', copied === rows.join('\n'), 'rows=' + JSON.stringify(rows));
  check('N323 复制串含换行分隔且无空行', copied.indexOf('\n') > 0 && copied.split('\n').every(line => line.length > 0), 'first=' + copied.split('\n')[0]);
  check('N323 源码逐行收集而非直接 textContent', /map\.call\(rows/.test(fs.readFileSync(page('gamertag-generator.html'), 'utf8')));
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
