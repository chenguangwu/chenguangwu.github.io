// 第260批 JSDOM 验证：IT-N30 裸 CR 切分（补证据）、IT-N54 CRC 模型命名、IT-N109 MIME 映射
// 用法: node scripts/_verify_it_batch260.mjs [OLD_DIR]
import fs from 'fs';
import { JSDOM } from 'jsdom';

const OLD = process.argv[2] || null;
const path = f => OLD ? `${OLD}/tools/it/${f}` : `tools/it/${f}`;
const read = f => fs.readFileSync(path(f), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS ' + name + (detail ? ' | ' + detail : '')); }
  else { fail++; console.log('FAIL ' + name + (detail ? ' | ' + detail : '')); }
}
function makeDom(file, extra) {
  const dom = new JSDOM(read(file), {
    runScripts: 'dangerously', url: 'https://x.com/tool.html',
    beforeParse(w) {
      w.alert = () => {};
      w.i18nText = k => k;
      w.ToolBox = {
        showToast() {}, copyText() {}, toggleToolTheme() {},
        setResult(id, v) { const e = w.document.getElementById(id); if (e) e.innerHTML = v; },
      };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
      };
      if (extra) extra(w);
    },
  });
  return dom;
}

// ---------------- IT-N30：列表转换器裸 CR 切分（历史已修，取证） ----------------
{
  const dom = makeDom('list-converter.html');
  const w = dom.window, d = w.document;
  d.getElementById('mode').value = 'comma';
  d.getElementById('input').value = 'a\rb\nc';
  w.convert();
  check('N30 裸 CR 切分为多项', d.getElementById('output').value === 'a, b, c', 'out=' + d.getElementById('output').value);
  d.getElementById('input').value = 'a\r\nb\rc';
  w.convert();
  check('N30 CRLF/CR/LF 混合换行均切分', d.getElementById('output').value === 'a, b, c', 'out=' + d.getElementById('output').value);
  check('N30 源码正则含裸 CR 分支', /split\(\/\\r\\n\|\\r\|\\n\//.test(read('list-converter.html')), 'regex');
}

// ---------------- IT-N54：CRC-8 模型命名（真改） ----------------
const crcHtml = read('crc-calculator.html');
check('N54 采用 reveng 正式名 CRC-8/I-432-1', /CRC-8\/I-432-1 \(ITU\)/.test(crcHtml), 'src');
check('N54 不再误挂 CCITT 别名', !/CRC-8\/ITU \(CCITT\)/.test(crcHtml), 'src');
{
  const dom = makeDom('crc-calculator.html');
  const w = dom.window, d = w.document;
  const algos = w.eval('ALGOS');
  const m = algos.find(a => a.name === 'CRC-8/I-432-1 (ITU)');
  check('N54 参数保持 I-432-1 标准', !!m && m.poly === 0x07 && m.init === 0x00 && m.refin === false && m.refout === false && m.xorout === 0x55, 'params=' + JSON.stringify(m || null));
  d.getElementById('input').value = 'abc';
  d.getElementById('upper').checked = true;
  w.calc();
  const res = d.getElementById('results').textContent;
  check('N54 输出新名', /CRC-8\/I-432-1 \(ITU\)/.test(res), 'res');
  check('N54 校验值仍为 0x0A', /0x0A/.test(res), 'res');
  check('N54 结果区不含误挂的 CCITT 别名', !/CRC-8\/ITU \(CCITT\)/.test(res), 'res');
}

// ---------------- IT-N109：MIME 映射修订（真改） ----------------
{
  const dom = makeDom('mime-type.html');
  const w = dom.window;
  const MIME = w.eval('MIME');
  const find = ext => MIME.filter(m => m.ext === ext)[0];
  const exe = find('.exe'), ai = find('.ai'), m3u8 = find('.m3u8');
  check('N109 .exe 采用 IANA 注册值', !!exe && exe.mime === 'application/vnd.microsoft.portable-executable', 'mime=' + (exe ? exe.mime : 'NA'));
  check('N109 .exe 弃用过时 x-msdownload', !!exe && exe.mime !== 'application/x-msdownload', 'mime=' + (exe ? exe.mime : 'NA'));
  check('N109 .ai 改为 PDF 兼容值', !!ai && ai.mime === 'application/pdf', 'mime=' + (ai ? ai.mime : 'NA'));
  check('N109 .m3u8 移出视频分类', !!m3u8 && m3u8.cat === '其他', 'cat=' + (m3u8 ? m3u8.cat : 'NA'));
  check('N109 .m3u8 仍为 HLS 播放列表类型', !!m3u8 && m3u8.mime === 'application/vnd.apple.mpegurl', 'mime=' + (m3u8 ? m3u8.mime : 'NA'));
  check('N109 清单条目总数不变', MIME.length === 84, 'n=' + MIME.length);
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
