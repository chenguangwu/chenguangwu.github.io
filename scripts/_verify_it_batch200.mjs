// 第200批 · IT-N253 regex 分享链接 base64url 对称修复（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/regex.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 160) : '')); }

// 经典 payload：中文 + 换行 —— 标准 base64 中段含 '+'（清单复现样本）
const payload = { p: '\\d+', f: 'g', t: '联系我 张三 13800138000' };
const standardB64 = Buffer.from(JSON.stringify(payload), 'utf8').toString('base64');

function makeDom(hash) {
  const copied = [];
  const warns = [];
  const url = 'https://example.com/tools/it/regex.html' + (hash || '');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    url,
    beforeParse(w) {
      w.alert = () => {};
      w.i18nText = (k, fb) => (fb != null ? fb : '');
      w.ToolBox = {
        copyText(t) { copied.push(String(t)); },
        downloadText() {}, showToast() {}, toggleToolTheme() {}
      };
      w.console = { warn(...a) { warns.push(a.join(' ')); }, log() {}, error() {} };
      w.TBKit = { util: { isEn: () => false, exportTable() {} } };
    }
  });
  return { dom, w: dom.window, d: dom.window.document, copied, warns };
}

// ── 场景1：copyShareLink 生成的链接应不含 + / / / = 且经 Params 往返能还原 ──
{
  const { dom, w, d, copied } = makeDom('');
  try { d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true })); } catch (e) {}
  d.getElementById('pattern').value = payload.p;
  d.getElementById('flags').value = payload.f;
  d.getElementById('testText').value = payload.t;
  w.copyShareLink();
  check('copyShareLink 调用了 copyText', copied.length >= 1, 'n=' + copied.length);
  const url = copied[0] || '';
  const m = url.match(/#regex=([^&]*)/);
  check('分享链接含 #regex= 片段', !!m);
  const enc = m ? m[1] : '';
  check('base64url 无 + / = 字符', !/[+/=]/.test(enc), enc.slice(0, 40));
  // 经 URLSearchParams（模拟浏览器 hash 解析）后字节不变
  const viaParams = new URLSearchParams('regex=' + enc).get('regex');
  check('base64url 经 URLSearchParams 不变', viaParams === enc);
}

// ── 场景2：用新格式链接加载页面，restoreSharedRegex 还原三字段 ──
{
  const urlEnc = standardB64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  const { dom, w, d } = makeDom('#regex=' + urlEnc);
  check('新链接还原 pattern', d.getElementById('pattern').value === payload.p, JSON.stringify(d.getElementById('pattern').value));
  check('新链接还原 flags', d.getElementById('flags').value === payload.f);
  check('新链接还原中文 testText', d.getElementById('testText').value === payload.t, JSON.stringify(d.getElementById('testText').value));
}

// ── 场景3：旧标准 base64 链接（+ 被解成空格）兼容 ──
{
  check('样本标准 base64 确实含 +', standardB64.indexOf('+') >= 0, standardB64.slice(0, 40));
  const { dom, w, d } = makeDom('#regex=' + standardB64);
  check('旧链接还原 pattern', d.getElementById('pattern').value === payload.p);
  check('旧链接还原中文 testText', d.getElementById('testText').value === payload.t, JSON.stringify(d.getElementById('testText').value));
}

// ── 场景4：无效片段不崩溃、有 warn ──
{
  const { dom, w, d, warns } = makeDom('#regex=!!!invalid!!!');
  check('无效片段不抛异常且保持默认', /d\+/.test(d.getElementById('pattern').value) && d.getElementById('testText').value.indexOf('Hello') >= 0, JSON.stringify(d.getElementById('pattern').value));
  check('无效片段有 console.warn', warns.length >= 1, 'n=' + warns.length);
}

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
