// 13 个 telecom 独立网络工具页验证：结构 / 状态机 / [object Object] 防护 / timezone 对象修复
// 用法: node scripts/_verify_net_tools.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const js = fs.readFileSync('js/network-toolbox.js', 'utf8');
const pages = [
  ['public-ip-lookup','t1'],['ip-geolocation','t2'],['local-ip-address','t3'],
  ['site-reachability','t4'],['url-reachability','t5'],['webrtc-leak-test','t6'],
  ['nat-type-test','t7'],['dns-egress-lookup','t8'],['cdn-edge-check','t9'],
  ['proxy-routing-test','t10'],['network-speed-test','t11'],['browser-fingerprint','t12'],
  ['service-status','t13'],
];
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

for (const [slug, id] of pages) {
  const html = fs.readFileSync('tools/telecom/' + slug + '.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.com/tools/telecom/' + slug + '.html',
    beforeParse(w) {
      w.ToolBox = { showToast() {} };
      w.TextEncoder = TextEncoder;
      Object.defineProperty(w.navigator, 'clipboard', {
        value: { writeText(t) { w.__copied = String(t); return Promise.resolve(); } }, configurable: true,
      });
      w.fetch = async (u) => {
        if (/ipwho\.is/.test(u)) return { ok: true, json: async () => ({
          ip: '8.8.8.8', type: 'IPv4', country: 'US', region: 'CA', city: 'Mountain View',
          connection: { isp: 'Google LLC', asn: 'AS15169' },
          timezone: { id: 'America/Los_Angeles', abbr: 'PDT', offset: -25200, name: 'Pacific Daylight Time', utc: '-07:00' },
        }) };
        if (/v6\.ident\.me/.test(u)) return { ok: true, text: async () => '' };
        return { ok: false, status: 500 };
      };
    },
  });
  const w = dom.window, d = w.document;
  w.eval(js);
  await new Promise(r => setTimeout(r, 60));
  check(slug + ' 页面标识', d.body.getAttribute('data-tool') === id);
  check(slug + ' 结果容器', !!d.getElementById('result-' + id));
  check(slug + ' 执行/复制按钮', !!d.querySelector('[data-run="' + id + '"]') && !!d.querySelector('[data-copy="' + id + '"]'));
  check(slug + ' 字段表/FAQ', d.querySelectorAll('.nt-table tr').length >= 2 && d.querySelectorAll('.nt-faq details').length >= 2);
  const txt = d.getElementById('result-' + id).textContent;
  check(slug + ' 无 [object Object]', !/\[object Object\]/.test(txt));
  // A 级升级：每页须有本工具专属的结果解读器 + 解读容器
  check(slug + ' 解读器函数', typeof w.__ntAnalyze === 'function');
  check(slug + ' 解读容器', !!d.getElementById('analysis-' + id));
}

// T1 结果速读强验证：成功结果须生成解读项，且判断与数据一致（8.8.8.8 = 公网 IPv4）
{
  const html = fs.readFileSync('tools/telecom/public-ip-lookup.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.com/tools/telecom/public-ip-lookup.html',
    beforeParse(w) {
      w.ToolBox = { showToast() {} };
      w.fetch = async (u) => {
        if (/ipwho\.is/.test(u)) return { ok: true, json: async () => ({
          ip: '8.8.8.8', type: 'IPv4', country: 'US', connection: {},
          timezone: { id: 'America/Los_Angeles' },
        }) };
        if (/v6/.test(u)) return { ok: true, text: async () => '' };
        return { ok: false, status: 500 };
      };
    },
  });
  const w = dom.window, d = w.document;
  w.eval(js);
  await new Promise(r => setTimeout(r, 80));
  const az = d.getElementById('analysis-t1');
  const atext = az ? az.textContent : '';
  check('T1 结果速读已生成', az && az.querySelectorAll('.nt-an-item').length >= 3,
    '解读项数=' + (az ? az.querySelectorAll('.nt-an-item').length : 0));
  check('T1 解读判定公网 IPv4', /公网地址|Public/.test(atext) && /IPv4/.test(atext), atext.slice(0, 80));
  check('T1 解读无 [object Object]', !/\[object Object\]/.test(atext));
}

// 专项：T1 timezone 对象必须取 id，不是 [object Object]
{
  const html = fs.readFileSync('tools/telecom/public-ip-lookup.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.com/tools/telecom/public-ip-lookup.html',
    beforeParse(w) {
      w.ToolBox = { showToast() {} }; w.TextEncoder = TextEncoder;
      w.fetch = async (u) => {
        if (/ipwho\.is/.test(u)) return { ok: true, json: async () => ({
          ip: '1.2.3.4', type: 'IPv4', country: 'CN', connection: {},
          timezone: { id: 'Asia/Shanghai', abbr: '+08', name: 'China Standard Time', utc: '+08:00' },
        }) };
        if (/v6/.test(u)) return { ok: true, text: async () => '' };
        return { ok: false, status: 500 };
      };
    },
  });
  const w = dom.window;
  w.eval(js);
  await new Promise(r => setTimeout(r, 80));
  const t1 = w.NT.ST.t1.copy || '';
  check('T1 timezone 取 id 文本', /Asia\/Shanghai/.test(t1) && !/\[object Object\]/.test(t1),
    (t1.split('\n').find(l => /时区|Timezone/.test(l)) || '').slice(0, 60));
}

// 解读器判别力：同一工具不同输入须给出不同判断（防固定文案 / 零逃生）
{
  const html = fs.readFileSync('tools/telecom/site-reachability.html', 'utf8');
  const dom = new JSDOM(html, {
    runScripts: 'dangerously', url: 'https://x.com/tools/telecom/site-reachability.html',
    beforeParse(w) { w.ToolBox = { showToast() {} }; },
  });
  const w = dom.window;
  w.eval(js);
  const good = w.__ntAnalyze('t4', 'A: ✅ 可达 10ms\nB: ✅ 可达 10ms\n汇总: 2/2 可达', false);
  const bad = w.__ntAnalyze('t4', 'A: ❌ 不可达\nB: ❌ 不可达\n汇总: 0/2 可达', false);
  check('解读器判别力（不同输入不同判断）', good !== bad && /全部可达/.test(good) && /全部不可达/.test(bad));
  const empty = w.__ntAnalyze('t4', '', false);
  check('解读器空输入不臆测', empty === '');
  // 英文态：英文结果文本不得输出中文
  const enOut = w.__ntAnalyze('t4', 'A: Reachable 10ms\nB: Reachable 10ms\nSummary: 2/2 reachable', true);
  check('解读器英文态零 CJK', !/[\u4e00-\u9fff]/.test(enOut));
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
