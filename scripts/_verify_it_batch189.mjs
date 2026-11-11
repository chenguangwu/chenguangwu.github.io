// 第189批 · IT-N458 og-meta 空值不输出 + 必填告警
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/og-meta-tag-generator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 110) : '')); }

let isEn = false;
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/og-meta-tag-generator.html',
  beforeParse(w) {
    w.i18nText = k => k;
    w.ToolBox = { showToast() {}, copyText() {}, downloadText() {}, toggleToolTheme() {}, escHtml(s) { return String(s); } };
    w.TBKit = {
      util: { isEn: () => isEn, exportTable() {}, diffBox() {} },
      chart: { line() {} }, matrix: { table() {} }, preset: { bar() {} },
      history: { add() {}, list() { return []; }, last() { return null; }, record() {}, clear() {}, mount() {} }
    };
  }
});
const w = dom.window;
const d = w.document;
function gen(o) {
  for (const k of ['f_title','f_desc','f_img','f_url','f_site','f_locale','f_type']) {
    const e = d.getElementById(k); if (e && o[k] !== undefined) e.value = o[k];
  }
  w.build();
  return { out: d.getElementById('output').value, res: d.getElementById('result').textContent, resHtml: d.getElementById('result').innerHTML };
}

// 判别1：清单复现——清空标题描述、只填图片，不得出现 content=""
const r1 = gen({ f_title:'', f_desc:'', f_img:'https://x.com/a.jpg', f_url:'', f_type:'website' });
check('空标题不输出 og:title', r1.out.indexOf('og:title') < 0, r1.out.slice(0, 90));
check('空描述不输出 og:description', r1.out.indexOf('og:description') < 0, r1.out.slice(0, 90));
check('无 content=""', r1.out.indexOf('content=""') < 0, r1.out.slice(0, 90));
check('缺字段告警含 og:title/url', r1.res.indexOf('og:title') >= 0 && r1.res.indexOf('og:url') >= 0, r1.res.slice(0, 110));

// 判别2：全填时正常输出、无告警
const r2 = gen({ f_title:'T', f_desc:'D', f_img:'https://x.com/a.jpg', f_url:'https://x.com/', f_site:'S', f_type:'article' });
check('全填含 og:title', r2.out.indexOf('<meta property="og:title" content="T">') >= 0, r2.out.slice(0, 90));
check('全填无缺失告警', r2.res.indexOf('缺少建议填写') < 0 && r2.res.indexOf('Missing') < 0, r2.res.slice(0, 90));

// 判别3：只填标题无图——twitter:card=summary、告警含 image/url
const r3 = gen({ f_title:'OnlyTitle', f_desc:'', f_img:'', f_url:'', f_type:'website' });
check('无图走 summary', r3.out.indexOf('twitter:card" content="summary"') >= 0, r3.out.slice(0, 90));
check('告警含 image/url', r3.res.indexOf('og:image') >= 0 && r3.res.indexOf('og:url') >= 0, r3.res.slice(0, 90));

// 判别4：英文态告警走英译
isEn = true;
const r4 = gen({ f_title:'', f_desc:'D', f_img:'', f_url:'https://x.com/', f_type:'website' });
check('英文告警无中文', r4.res.indexOf('缺少') < 0 && r4.res.indexOf('Missing') >= 0, r4.res.slice(0, 100));
isEn = false;

// 判别5：状态链 空→全→空
gen({ f_title:'T', f_desc:'D', f_img:'https://x/a.jpg', f_url:'https://x/', f_type:'website' });
const r5 = gen({ f_title:'', f_desc:'', f_img:'', f_url:'', f_type:'website' });
check('状态链回到空仍无 content=""', r5.out.indexOf('content=""') < 0, r5.out.slice(0, 80));

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
