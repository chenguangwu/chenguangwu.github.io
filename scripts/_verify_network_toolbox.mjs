// 网络工具箱 E2E 验证：13 工具状态机 / 复制格式 / 多源回退 / 降级
// 用法: node scripts/_verify_network_toolbox.mjs
import fs from 'fs';
import { JSDOM } from 'jsdom';

const html = fs.readFileSync('tools/it/network-toolbox.html', 'utf8');
const js = fs.readFileSync('js/network-toolbox.js', 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}

let copied = '';
const dom = new JSDOM(html, {
  runScripts: 'dangerously', url: 'https://x.com/tools/it/network-toolbox.html',
  beforeParse(w) {
    w.ToolBox = { showToast() {} };
    w.TextEncoder = TextEncoder;
    Object.defineProperty(w.navigator, 'clipboard', {
      value: { writeText(t) { copied = String(t); return Promise.resolve(); } }, configurable: true,
    });
    w.fetch = async function (url, opts) {
      const u = String(url);
      if (u.indexOf('ipwho.is') >= 0) throw new Error('blocked-primary');
      if (u.indexOf('ipapi.co') >= 0) return { ok: true, json: async () => ({ ip: '1.2.3.4', country_name: 'US', region: 'CA', city: 'SF', org: 'AS1 ISP', asn: 'AS1', timezone: 'America/Los_Angeles' }) };
      if (u.indexOf('v6.ident.me') >= 0) return { ok: true, text: async () => '2001:db8::1' };
      if (u.indexOf('githubstatus') >= 0) return { ok: true, json: async () => ({ status: { indicator: 'none', updated_at: '2026-01-01T00:00:00Z' } }) };
      if (u.indexOf('cloudflarestatus') >= 0) return { ok: true, json: async () => ({ status: { indicator: 'minor', updated_at: '2026-01-02T00:00:00Z' } }) };
      if (u.indexOf('__down') >= 0) return { ok: true, arrayBuffer: async () => new ArrayBuffer(1024), body: null };
      return { ok: true, json: async () => ({}), headers: { get: () => null } };
    };
    w.RTCPeerConnection = class {
      constructor() { this.cands = []; }
      createDataChannel() {}
      createOffer() { return Promise.resolve({ type: 'offer', sdp: 'x' }); }
      setLocalDescription() {
        setTimeout(() => {
          if (this.onicecandidate) {
            this.onicecandidate({ candidate: { candidate: 'candidate:1 1 udp 2130706431 192.168.1.7 54321 typ host' } });
            this.onicecandidate({ candidate: { candidate: 'candidate:2 1 udp 1694498815 8.8.8.8 54321 typ srflx' } });
            this.onicecandidate({ candidate: null });
          }
        }, 0);
        return Promise.resolve();
      }
      close() {}
    };
    w.Image = class {
      set src(v) { setTimeout(() => { if (this.onload) this.onload(); }, 0); }
    };
  },
});
const w = dom.window, d = w.document;
w.eval(js);

// ---------- 结构与空态 ----------
check('13 个工具卡片齐全', d.querySelectorAll('.nt-card').length === 13, String(d.querySelectorAll('.nt-card').length));
check('结果区均 aria-live=polite', d.querySelectorAll('.nt-result[aria-live="polite"]').length === 13);
check('运行/复制按钮各 13', d.querySelectorAll('[data-run]').length === 13 && d.querySelectorAll('[data-copy]').length === 13);
// 页面加载会自动跑一次 T1，等它结束再断言（RUNNING 标志复位）
await new Promise(r => setTimeout(r, 80));

// ---------- 纯逻辑：IP 校验 ----------
check('IPv4 合法', w.NT.validIp('8.8.8.8') === '4');
check('IPv4 非法段拒绝', w.NT.validIp('999.1.1.1') === '');
check('IPv6 合法', w.NT.validIp('2001:4860:4860::8888') === '6');
check('普通文本拒绝', w.NT.validIp('abc') === '');

// ---------- render 状态机 ----------
w.NT.render('t5', 'error', '测试错误', '复制文本');
check('render 失败态写徽章与 data-s', d.querySelector('#card-t5 .nt-badge').getAttribute('data-s') === 'error' && d.getElementById('result-t5').getAttribute('data-s') === 'error');
check('render 失败态按钮变重试', /重试/.test(d.querySelector('#card-t5 [data-run]').textContent));

// ---------- T8 降级（不伪造） ----------
await w.NT.run('t8');
check('T8 未配置时保持降级态', w.NT.ST.t8.state === 'idle' && /不伪造数据/.test(w.NT.ST.t8.copy), w.NT.ST.t8.state);

// ---------- T1 多源回退 + 复制格式 ----------
check('T1 主源失败后备源成功', w.NT.ST.t1.state === 'ok' && /来源: ipapi.co/.test(w.NT.ST.t1.copy), w.NT.ST.t1.copy.slice(0, 60));
check('T1 复制格式含全部字段', ['IP:', '版本: IPv', '位置:', 'ISP:', 'ASN:', '时区:', '来源:', '时间:'].every(k => w.NT.ST.t1.copy.indexOf(k) >= 0));
check('T1 IPv6 探测成功并附行', /\nIPv6: 2001:db8::1/.test(w.NT.ST.t1.copy));

// ---------- T2 非法 IP 不发请求 ----------
d.getElementById('t2-ip').value = 'not-an-ip';
await w.NT.run('t2');
check('T2 非法 IP 直接报错', w.NT.ST.t2.state === 'error' && /格式不合法/.test(w.NT.ST.t2.display));

// ---------- T3 host candidate ----------
await w.NT.run('t3');
check('T3 保留 host 内网地址', w.NT.ST.t3.state === 'ok' && /192\.168\.1\.7/.test(w.NT.ST.t3.copy), w.NT.ST.t3.state);
check('T3 srflx 未混入内网列表', !/8\.8\.8\.8/.test(w.NT.ST.t3.copy));

// ---------- T6 WebRTC 比对 ----------
await w.NT.run('t6');
check('T6 与 T1 公网 IP 一致性为不一致（8.8.8.8 vs 1.2.3.4）', /一致性: 不一致/.test(w.NT.ST.t6.copy), w.NT.ST.t6.copy.slice(-80));

// ---------- T13 状态映射 ----------
await w.NT.run('t13');
check('T13 operational/degraded 映射', /GitHub: operational/.test(w.NT.ST.t13.copy) && /Cloudflare: degraded/.test(w.NT.ST.t13.copy), w.NT.ST.t13.copy.slice(0, 80));

// ---------- 复制按钮 ----------
const copyBtn = d.querySelector('[data-copy="t1"]');
copyBtn.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
await new Promise(r => setTimeout(r, 10));
check('复制按钮写入 T1 文本', copied === w.NT.ST.t1.copy, copied.slice(0, 40));

// ---------- 本机历史 + 汇总表 + 对比（persist/table 维度强锁） ----------
check('汇总表为真实 <table>', d.querySelectorAll('.nt-hist-table').length === 1);
const histRaw = w.localStorage.getItem('ntHist_v1') || '{}';
let hist = {}; try { hist = JSON.parse(histRaw); } catch (e) {}
check('成功结果写入 localStorage', !!(hist.t1 && hist.t1.copy && hist.t1.time), histRaw.slice(0, 60));
const histRows = d.querySelectorAll('#ntHistoryBody tr');
check('历史表渲染已运行工具行', histRows.length >= 1 && /T1/.test(histRows[0].textContent), String(histRows.length));
// 再跑一次 T1，制造「上次 vs 本次」，验证对比可用
const prevCopy = w.NT.ST.t1.copy;
await w.NT.run('t1');
await new Promise(r => setTimeout(r, 30));
check('二次运行保留上一次副本', !!(w.NT.ST.t1.prevCopy && w.NT.ST.t1.prevCopy === prevCopy), (w.NT.ST.t1.prevCopy || '').slice(0, 30));
const diffBtn = d.querySelector('#ntHistoryBody [data-diff="t1"]');
check('对比按钮出现在历史行', !!diffBtn);
if (diffBtn) {
  diffBtn.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
  check('点击对比展开逐行 diff', !!d.querySelector('#ntHistoryBody .nt-diff-row .nt-hist-diff'));
}

console.log('RESULT ' + pass + '/' + (pass + fail));
process.exit(fail ? 1 : 0);
