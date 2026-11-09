import fs from 'fs';
import { execSync } from 'child_process';
import { JSDOM, VirtualConsole } from 'jsdom';
const file = 'tools/music/bpm-converter.html';
const html = process.argv.includes('--head') ? execSync(`git show HEAD:${file}`).toString() : fs.readFileSync(file, 'utf8');
const vc = new VirtualConsole();
vc.on('jsdomError', () => {});
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://example.test/' + file, virtualConsole: vc,
  beforeParse(w) {
    w.ToolBox = { showToast() {}, showError() {}, copyText() {}, formatNumber: n => String(n) };
    w.i18nText = k => String(k);
  }
});
const w = dom.window, doc = w.document, input = doc.getElementById('bpmInput'), slider = doc.getElementById('bpmSlider');
let failures = 0;
function assert(ok, msg) { console.log(`${ok ? 'PASS' : 'FAIL'}: ${msg}`); if (!ok) failures++; }
function type(v) { input.value = v; input.dispatchEvent(new w.Event('input', { bubbles: true })); }
function change() { input.dispatchEvent(new w.Event('change', { bubbles: true })); }
type(''); assert(input.value === '', '清空保留空输入');
assert(['noteGrid','delayTable','lfoGrid','sampleGrid'].every(id => !/\d+(?:\.\d+)?\s*(?:ms|Hz|samples)/i.test(doc.getElementById(id).textContent)), '空态不保留此前计算结果');
w.calcAll(); assert(['noteGrid','delayTable','lfoGrid','sampleGrid'].every(id => !doc.getElementById(id).textContent.trim()), '空态下其他控件重算不得产生旧结果');
for (const c of '120') type(input.value + c);
assert(input.value === '120' && slider.value === '120', '逐键输入 120 并同步滑块');
type('1'); assert(input.value === '1', '输入中的暂时越界值不被回写');
change(); assert(input.value === '40' && slider.value === '40', '完成输入时低值钳制至 40');
type('999'); change(); assert(input.value === '300' && slider.value === '300', '完成输入时高值钳制至 300');
type(''); change(); assert(input.value === '', '空值提交保持空态');
w.setBpm(90); assert(input.value === '90' && slider.value === '90', '预设同步输入和滑块');
dom.window.close();
process.exit(failures ? 1 : 0);
