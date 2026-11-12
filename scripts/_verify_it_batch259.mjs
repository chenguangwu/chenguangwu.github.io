// 第259批 JSDOM 验证：IT-N2 AST 离线提示/导出、IT-N20 历史回填清勾、IT-N26 Markdown 压缩与下拉框
// 用法: node scripts/_verify_it_batch259.mjs [OLD_DIR]
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
  const toasts = [];
  const dom = new JSDOM(read(file), {
    runScripts: 'dangerously', url: 'https://x.com/tool.html',
    beforeParse(w) {
      w.alert = () => {};
      w.i18nText = k => ({
        'toast.msg029': 'acorn 解析器加载失败，请检查网络',
        'toast.msg684': '请先输入 JavaScript 代码',
        'toast.msg671': '请先解析代码生成 AST',
      }[k] || k);
      w.ToolBox = {
        showToast: m => toasts.push(String(m)),
        copyText() {}, toggleToolTheme() {},
        setResult(id, v) { const e = w.document.getElementById(id); if (e) e.innerHTML = v; },
      };
      w.TBKit = {
        util: { isEn: () => false, exportTable() {}, diffBox() {} },
        chart: { bar() {}, line() {} }, matrix: { table() {} }, preset: { bar() {} },
        history: { list: () => [], last: () => null, record() {}, mount() {}, clear() {} },
      };
      if (extra) extra(w, toasts);
    },
  });
  return { dom, toasts };
}

// ---------------- IT-N2：AST 查看器 ----------------
const astHtml = read('ast-viewer.html');
check('N2 acorn 本地锁版本托管', /\/vendor\/acorn\/8\.19\.0\/acorn\.min\.js/.test(astHtml) && /integrity="sha384-/.test(astHtml), 'vendor');
check('N2 加载失败有明确提示分支', /typeof window\.acorn === 'undefined'/.test(astHtml) && /toast\.msg029/.test(astHtml), 'guard');
check('N2 保留 JSON 复制导出', /btnCopyJson/.test(astHtml) && /JSON\.stringify\(currentAst/.test(astHtml), 'export');
{
  const { dom, toasts } = makeDom('ast-viewer.html');
  const w = dom.window, d = w.document;
  const ci = d.getElementById('codeInput');
  if (ci) ci.value = 'const a = 1;';
  toasts.length = 0;
  const btn = d.getElementById('btnParse');
  if (btn) btn.click();
  check('N2 真机未加载 acorn 时报错', toasts.some(m => /acorn 解析器加载失败/.test(m)), JSON.stringify(toasts));
  check('N2 提示要求检查网络而非静默', toasts.some(m => /请检查网络/.test(m)), JSON.stringify(toasts));
}

// ---------------- IT-N20：文本清理器历史回填 ----------------
{
  let mountCb = null;
  const { dom } = makeDom('text-cleaner.html', (w) => {
    // 页面另有 mount(sel, 配置对象) 调用，只捕获函数型回填回调
    w.TBKit.history.mount = (sel, cb) => { if (typeof cb === 'function') mountCb = cb; };
  });
  const w = dom.window, d = w.document;
  if (typeof mountCb !== 'function') {
    // 通过页面真实「执行清理」按钮触发 extras → render → history.mount
    const btn = Array.from(d.querySelectorAll('button')).find(b => /executeClean\(\)/.test(b.getAttribute('onclick') || ''));
    if (btn) btn.click();
  }
  if (typeof mountCb !== 'function' && typeof w.__text_cleanerRender === 'function') {
    // 兜底：直接调用页面渲染器挂载回填回调（真实函数，非复制实现）
    w.__text_cleanerRender(['opt-trim'], '结果', false);
  }
  check('N20 历史回填回调已挂载', typeof mountCb === 'function', 'mount');
  if (typeof mountCb === 'function') {
    const trim = d.getElementById('opt-trim');
    trim.checked = true;
    // mount 回调收到的是扁平数据对象（含 __tbScore），不是 {t,d} 包装
    // 稀疏历史记录：当时未勾选 opt-trim，rec 中不含该字段
    mountCb({ 'output-text': 'A', __tbScore: '1' });
    check('N20 稀疏记录清除当前多勾选项', trim.checked === false, 'checked=' + trim.checked);
    // 全量记录：opt-trim='1' 应恢复勾选
    mountCb({ 'output-text': 'A', 'opt-trim': '1', __tbScore: '1' });
    check('N20 全量记录恢复已勾选项', trim.checked === true, 'checked=' + trim.checked);
    // 全量记录：opt-trim='0' 应清除勾选
    mountCb({ 'output-text': 'A', 'opt-trim': '0', __tbScore: '1' });
    check('N20 全量记录清除未勾选项', trim.checked === false, 'checked=' + trim.checked);
  }
}

// ---------------- IT-N26：Markdown 下拉框与压缩 ----------------
{
  const { dom } = makeDom('markdown-to-html.html');
  const w = dom.window, d = w.document;
  const sc = d.getElementById('showcode'), cp = d.getElementById('compact');
  check('N26 显示代码下拉框有选项', !!sc && sc.options.length >= 2 && sc.querySelector('option[value="1"]') !== null, 'opts=' + (sc ? sc.options.length : -1));
  check('N26 输出模式下拉框有选项', !!cp && cp.options.length >= 2 && cp.querySelector('option[value="compact"]') !== null, 'opts=' + (cp ? cp.options.length : -1));
  const md = d.getElementById('md');
  md.value = '# 标题\n\n- 甲\n- 乙\n\n段落一\n\n段落二';
  const preOf = s => { const m = s.match(/<pre[^>]*>([\s\S]*?)<\/pre>/); return m ? m[1] : ''; };
  sc.value = '1'; cp.value = 'pretty'; w.calcTool();
  const codePretty = d.getElementById('result').innerHTML;
  cp.value = 'compact'; w.calcTool();
  const codeCompact = d.getElementById('result').innerHTML;
  check('N26 显示代码时输出 HTML 代码面板', /<b>HTML 代码<\/b>/i.test(codeCompact), 'panel');
  check('N26 美化模式代码面板带换行', preOf(codePretty).includes('\n'), 'pretty pre');
  check('N26 压缩模式代码面板为单行', preOf(codeCompact).length > 0 && !preOf(codeCompact).includes('\n'), 'compact pre');
  // 生成器输出本就不含标签间空白，预览在两种模式下渲染一致（据实记录，不作判别点）
  sc.value = '0'; cp.value = 'pretty'; w.calcTool();
  const previewPretty = d.getElementById('result').innerHTML.split('<div class="tip-mini"')[0];
  cp.value = 'compact'; w.calcTool();
  const previewCompact = d.getElementById('result').innerHTML.split('<div class="tip-mini"')[0];
  console.log('DIAG 预览长度 pretty=' + previewPretty.length + ' compact=' + previewCompact.length +
    ' 含标签间空白=' + />\s+</.test(previewPretty));
}

// ---------------- IT-N29：空格清理器逐行对照预览 ----------------
{
  const { dom } = makeDom('whitespace.html');
  const w = dom.window, d = w.document;
  d.getElementById('source').value = 'a\n   \nb';
  ['top_trim', 'top_blank', 'top_collapse', 'top_trail', 'top_onespace'].forEach(id => {
    d.getElementById(id).checked = (id === 'top_blank');
  });
  w.calcTool();
  const res = d.getElementById('result').innerHTML;
  const preview = (res.split('逐行对照预览')[1] || '').split('</table>')[0];
  const rows = Array.from(preview.matchAll(/<tr><td>(\d+)<\/td><td><code>([\s\S]*?)<\/code><\/td><td><code>([\s\S]*?)<\/code><\/td><\/tr>/g))
    .map(m => ({ n: m[1], raw: m[2], after: m[3] }));
  console.log('DIAG N29 rows=' + JSON.stringify(rows));
  check('N29 表头改为原始行/处理后内容', /<th>原始行<\/th>/.test(preview) && /<th>处理后内容<\/th>/.test(preview), 'head');
  check('N29 三行均按原始行号展示', rows.length === 3 && rows[0].n === '1' && rows[1].n === '2' && rows[2].n === '3', 'n=' + rows.length);
  check('N29 被删空行标注已删除', /已删除/.test(rows[1] ? rows[1].after : ''), 'row2=' + (rows[1] ? rows[1].after : 'NA'));
  check('N29 第三行处理后内容不错位', rows[2] && rows[2].after === 'b', 'row3=' + (rows[2] ? rows[2].after : 'NA'));
  check('N29 第二行不再错配下一行内容', rows[1] && !/^b$/.test(rows[1].after), 'row2=' + (rows[1] ? rows[1].after : 'NA'));
}

console.log(`\n${OLD ? 'OLD' : 'NEW'} RESULT ${pass}/${pass + fail}`);
process.exit(0);
