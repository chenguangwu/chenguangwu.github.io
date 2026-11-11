// 第210批 · IT-N267/N268/N269 json-schema-generator required口径/描述注释/混合类型（JSDOM 真机）
import fs from 'fs';
import { JSDOM } from 'jsdom';

const PAGE = process.env.TB_PAGE || 'tools/it/json-schema-generator.html';
const html = fs.readFileSync(PAGE, 'utf8');
const checks = [];
function check(n, ok, x) { checks.push([n, ok]); console.log((ok ? 'PASS ' : 'FAIL ') + n + (x ? ' | ' + String(x).slice(0, 200) : '')); }

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'https://example.com/tools/it/json-schema-generator.html',
  beforeParse(w) {
    w.alert = () => {};
    w.ToolBox = { showToast() {}, toggleToolTheme() {}, copyText() {}, downloadText() {} };
    w.TBKit = {
      util: { isEn: () => false, exportTable() {}, diffBox() {} },
      chart: { line() {}, bar() {} },
      matrix: { table() {} },
      preset: { bar() {} },
      history: { list() { return []; }, record() {}, last() { return null; }, mount() {}, clear() {} }
    };
  }
});
const w = dom.window, d = w.document;
d.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true }));

const DEFAULTS = { optRequired: true, optExamples: true, optDescriptions: false, optTitle: true, optMinMax: false };
function gen(json, opts) {
  const o = Object.assign({}, DEFAULTS, opts || {});
  for (const k of Object.keys(o)) d.getElementById(k).checked = o[k];
  d.getElementById('input').value = json;
  w.eval('generateSchema()');
  return w.eval('lastSchema');
}

// ── IT-N267 null 字段不进 required ──
const sNull = gen('{"a":null,"b":"x"}');
check('N267 null 字段不进 required', sNull.required.indexOf('a') < 0 && sNull.required.indexOf('b') >= 0, JSON.stringify(sNull.required));
check('N267 null 字段本身仍推断为 null 类型', sNull.properties.a.type === 'null');
const sample = w.eval('SAMPLE');
const sSample = gen(sample);
check('N267 默认示例的 metadata:null 不再进 required', !sSample.required || sSample.required.indexOf('metadata') < 0, JSON.stringify(sSample.required));

// ── IT-N267 数组内多对象取共有键 ──
const sArr = gen('{"items":[{"a":1,"b":2},{"a":3}]}');
const arrItems = sArr.properties.items.items;
check('N267 数组对象保留全部属性', !!arrItems.properties.a && !!arrItems.properties.b, JSON.stringify(Object.keys(arrItems.properties)));
check('N267 数组对象 required 只取共有键', (arrItems.required || []).join(',') === 'a', JSON.stringify(arrItems.required));

// ── IT-N268 描述注释从死控件变成真输出 ──
const sNoDesc = gen('{"name":"Tom","score":80}', { optDescriptions: false });
const sDesc = gen('{"name":"Tom","score":80}', { optDescriptions: true });
check('N268 未勾选时无 description', !sNoDesc.properties.name.description, JSON.stringify(sNoDesc.properties.name));
check('N268 勾选后输出 description', sDesc.properties.name.description === 'The name field.', JSON.stringify(sDesc.properties.name));
check('N268 每个属性都有 description', !!sDesc.properties.name.description && !!sDesc.properties.score.description);
check('N268 勾选与不勾选产物确实不同', JSON.stringify(sNoDesc) !== JSON.stringify(sDesc));

// ── IT-N269 混合类型 anyOf ──
const m = w.eval("mergeSchemas([{type:'integer'},{type:'string'}])");
check('N269 混合类型不再返回空 schema', Object.keys(m).length > 0 && !!(m.anyOf || m.type), JSON.stringify(m));
check('N269 混合类型输出 anyOf 两项', !!m.anyOf && m.anyOf.length === 2, JSON.stringify(m));
const sMixed = gen('{"tags":[1,"a"]}');
check('N269 混合数组 items.anyOf 保留元素类型', !!sMixed.properties.tags.items.anyOf && sMixed.properties.tags.items.anyOf.length === 2, JSON.stringify(sMixed.properties.tags.items));
const mDup = w.eval("mergeSchemas([{type:'integer'},{type:'integer'}])");
check('N269 同类型合并不产 anyOf', !mDup.anyOf && mDup.type === 'integer', JSON.stringify(mDup));
const tv = w.eval('buildTreeView(lastSchema)');
check('N269 树视图也展示 anyOf', !!(tv.properties && tv.properties.tags && tv.properties.tags.items && tv.properties.tags.items.anyOf), JSON.stringify(tv).slice(0, 180));

// ── 顺带：isIPv4 范围与前导零 ──
check('IPv4 合法地址通过', w.eval("isIPv4('192.168.1.1')") === true);
check('IPv4 拒绝 999 段', w.eval("isIPv4('999.999.999.999')") === false);
check('IPv4 拒绝 256 段', w.eval("isIPv4('256.0.0.1')") === false);
check('IPv4 拒绝前导零', w.eval("isIPv4('01.2.3.4')") === false);
const sIp = gen('{"ip":"999.999.999.999","valid":"10.0.0.1"}');
check('非法 IP 不标 ipv4 format', !sIp.properties.ip.format && sIp.properties.valid.format === 'ipv4', JSON.stringify(sIp.properties));

// ── 双语口径 ──
const en = JSON.parse(fs.readFileSync('i18n/tools/en/it/json-schema-generator.json', 'utf8'));
const key = '：本工具按单个样本推断，对象中的非 null 键均列入必填；null 字段不列入（避免「必填且只能为 null」），数组元素的多个对象只取共有键。多份样本需人工合并后再调整。';
check('en JSON 含更新后的 required 说明键', Object.prototype.hasOwnProperty.call(en.map || {}, key));
check('页面含更新后的 required 说明', html.indexOf('本工具按单个样本推断') >= 0);

const pass = checks.filter(c => c[1]).length;
console.log('==== ' + pass + '/' + checks.length + ' 通过 ====');
process.exit(pass === checks.length ? 0 : 1);
