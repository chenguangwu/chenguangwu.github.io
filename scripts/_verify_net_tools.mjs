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

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
