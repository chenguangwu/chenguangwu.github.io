#!/usr/bin/env node
/**
 * it 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 与 scripts/verify_calc.js 的区别：
 *   - verify_calc.js 是「冒烟测试」：只跑 calcTool() 检查不报错
 *   - 本脚本是「正确性验证」：注入已知输入，用独立实现/权威测试向量断言输出
 *
 * 用法：
 *   node scripts/verify_it_calc.js            # 跑全部用例
 *   node scripts/verify_it_calc.js base64 md5 # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）
 *   expect  —— 期望子串，命中任意一个「输出元素」（value 或 innerHTML）即通过
 *   ref     —— 该期望值的来源说明（权威向量 / 独立实现 / 标准文档），必填，便于复核
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const TOOLS_DIR = path.join(ROOT, "tools");

// ---------------------------------------------------------------- 固定基准日（根治日期漂移）
// 门禁用例不得依赖真实「今天」：真实日期每推进一天，相对今天推算的绝对日期期望就会过期一天，
// 导致 CI 偶发/漂移失败（已发生 fire/livestock/cleaning/pediatrics/travel 五道门禁）。
// 这里把 new Date() / Date.now() 冻结到一个固定基准日，使所有日期型页面在 CI 永远算同一天、完全确定。
// 约定：用例断言应「与今天无关」（时长/计数/静态名称/状态标题）或「基于基准日的相对结果」。
const REAL_DATE = Date;
const FIXED_NOW = Date.parse("2024-06-15T00:00:00Z");
function FrozenDate(...args) {
  // 无参构造 → 固定基准日；带参构造（new Date(t) / new Date(y,m,d)）按真实 Date 透传
  if (args.length === 0) return new REAL_DATE(FIXED_NOW);
  return new REAL_DATE(...args);
}
FrozenDate.now = () => FIXED_NOW;
FrozenDate.parse = REAL_DATE.parse.bind(REAL_DATE);
FrozenDate.UTC = REAL_DATE.UTC.bind(REAL_DATE);
FrozenDate.prototype = REAL_DATE.prototype;

// 根治（续）：把 Math.random 也替换成「确定性种子 PRNG」，并在每个用例前重置种子。
// 原因：Math.random 类页面（随机推荐 / 随机生成器 / 随机抽题等）在本地与 CI 的随机序列不同，
// 且 Node 版本（ICU / V8）差异会让「断言随机输出值」的用例偶发落空（已发生 niche 等门禁）。
// 固定种子 + 每用例重置 → 任何页面在任意进程、任意环境下都得到完全一致的随机序列，门禁可重现。
let _rngState = 0;
function _rngReset() { _rngState = 0x9e3779b9 >>> 0; }
(function installSeededRandom() {
  _rngReset();
  const next = () => {
    _rngState = (_rngState + 0x6d2b79f5) | 0;
    let t = Math.imul(_rngState ^ (_rngState >>> 15), 1 | _rngState);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  Math.random = next;
})();


// ---------------------------------------------------------------- 用例
const CASES = [
  {
    // 原 it/base64 已在「跨分类重复工具治理（批次六）」合并进 base64-converter，
    // 旧 slug 不再存在。用例改指现存工具，避免死用例长期拖挂门禁。
    slug: "it/base64-converter",
    inputs: { input: "hello" },
    expect: ["aGVsbG8="],
    ref: "Base64('hello') = aGVsbG8=（RFC 4648 标准测试向量）",
  },
  {
    slug: "it/md5",
    inputs: { textInput: "hello" },
    expect: ["5d41402abc4b2a76b9719d911017c592"],
    ref: "MD5('hello') = 5d41402abc4b2a76b9719d911017c592（RFC 1321 常见向量）",
  },
  {
    slug: "it/sha",
    inputs: { textInput: "hello" },
    checks: ["sha-256"],
    expect: ["2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"],
    ref: "SHA-256('hello') = 2cf24dba…9824（NIST 标准向量）",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "123456789" },
    expect: ["CBF43926", "cbf43926"],
    ref: "标准 CRC-32/ISO-HDLC（多项式 0x04C11DB7）对 '123456789' 应为 CBF43926",
  },

  // —— 编码类（期望值由 python base64 / 自实现 base58 独立计算，非凭记忆）——
  {
    slug: "it/base32-encode",
    inputs: { input: "hello" },
    expect: ["NBSWY3DP", "nbswy3dp"],
    ref: "python base64.b32encode(b'hello') = NBSWY3DP（RFC 4648）",
  },
  {
    slug: "it/base58-encode",
    inputs: { input: "hello" },
    expect: ["Cn8eVZg"],
    ref: "自实现 Base58（BTC 字母表）编码 'hello' = Cn8eVZg",
  },
  {
    slug: "it/hex-encode",
    inputs: { input: "hello" },
    expect: ["68656c6c6f", "68656C6C6F"],
    ref: "b'hello'.hex() = 68656c6c6f",
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "68656c6c6f" },
    expect: ["hello"],
    ref: "bytes.fromhex('68656c6c6f') = b'hello'",
  },
  {
    slug: "it/binary-encode",
    inputs: { input: "hi" },
    expect: ["0110100001101001", "01101000 01101001"],
    ref: "''.join(format(c,'08b') for c in b'hi') = 0110100001101001",
  },
  {
    slug: "it/text-to-binary",
    inputs: { input: "hi" },
    expect: ["0110100001101001", "01101000 01101001"],
    ref: "同上，b'hi' 的 8 位二进制表示",
  },
  {
    slug: "it/text-to-hex",
    inputs: { input: "hello" },
    expect: ["68656c6c6f", "68656C6C6F", "68 65 6c 6c 6f", "68 65 6C 6C 6F"],
    ref: "b'hello'.hex() = 68656c6c6f",
  },
  {
    slug: "it/text-to-decimal",
    inputs: { input: "hi" },
    expect: ["104 105", "104,105", "104105"],
    ref: "'hi' 的十进制码点为 104 105",
  },
  {
    slug: "it/text-to-octal",
    inputs: { input: "hi" },
    expect: ["150 151", "150,151"],
    ref: "format(104,'o')=150、format(105,'o')=151",
  },
  {
    slug: "it/decimal-encode",
    inputs: { input: "hi" },
    expect: ["104 105", "104,105"],
    ref: "同 text-to-decimal：'hi' → 104 105",
  },
  {
    slug: "it/octal-encode",
    inputs: { input: "hi" },
    expect: ["150 151", "150,151"],
    ref: "同 text-to-octal：'hi' → 150 151",
  },
  {
    slug: "it/text-to-ascii",
    inputs: { txt: "z" },
    expect: ["122"],
    ref: "ord('z') = 122（ASCII 码表；默认正文 Hello, ToolBox! 不含码点 122，注入失败即不命中）",
  },
  {
    slug: "it/text-to-unicode",
    inputs: { txt: "A" },
    expect: ["U+0041", "0041", "65"],
    ref: "ord('A') = 65 → U+0041",
  },
  {
    slug: "it/url-encode",
    inputs: { input: "a b" },
    expect: ["a%20b", "a+b"],
    ref: "urllib.parse.quote('a b') = a%20b（plusSpace 开启时为 a+b，两者均属正确实现）",
  },
  {
    slug: "it/html-entities-encode",
    inputs: { input: "<" },
    expect: ["&lt;", "&#60;", "&#x3C;"],
    ref: "HTML 实体：'<' 转义为 &lt;（或数字实体 &#60;）",
  },

  // —— 进制与密码类 ——
  {
    slug: "it/integer-base-converter",
    inputs: { num: "255", fromBase: "10", toBase: "16" },
    expect: ["FF", "ff"],
    ref: "format(255,'X') = FF",
  },
  {
    slug: "it/number-base-converter",
    inputs: { inputValue: "1000", inputBase: "10" },
    expect: ["3E8"],
    ref: "inputValue=1000 按十进制解读 → 十六进制 3E8（formatNumber(1000,16).toUpperCase()）。"
       + "改用 1000 而非 255：页面含 0–255 静态参考表，255 的各进制表示恒在表中（原 expect「FF」撞表，逃生项）；"
       + "1000 超出静态表范围，其转换结果仅在输入框真正注入时出现，回退默认(空)无 3E8 → 失配。",
  },
  {
    slug: "it/calc-2",
    inputs: { numInput: "255", fromBase: "10" },
    expect: ["FF", "ff"],
    ref: "format(255,'X') = FF",
  },
  {
    slug: "it/caesar-cipher",
    inputs: { input: "abc", shift: "1" },
    expect: ["bcd"],
    ref: "凯撒位移 1：a→b、b→c、c→d",
  },
  {
    slug: "it/rot-cipher",
    inputs: { input: "hello", shift: "13" },
    expect: ["uryyb"],
    ref: "ROT13('hello') = uryyb（自互逆，经典向量）",
  },
  {
    slug: "it/morse",
    inputs: { input: "SOS" },
    expect: ["... --- ...", "...---..."],
    ref: "摩斯电码 S=...、O=---，SOS = ... --- ...（国际求救信号）",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "1987" },
    expect: ["MCMLXXXVII"],
    ref: "1987 = 1000+900+80+7 = MCMLXXXVII",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { timestampSec: "0" },
    expect: ["1970"],
    ref: "Unix 时间戳 0 = 1970-01-01T00:00:00Z（UTC 纪元）",
  },
  {
    slug: "it/standard-deviation",
    inputs: { data: "1,2,3,4" },
    expect: ["1.291", "1.118"],
    ref: "statistics.stdev([1,2,3,4])=1.2910（样本，n-1）；pstdev=1.1180（总体，n）",
  },
  {
    slug: "it/hypothesis-test",
    // 回归保护：原实现双侧 p 用 p=2*(1-|Φ(z)-0.5|)，z=2 时得 1.046（p 值 >1）且结论反转。
    // 此处取 z=1.5（非默认输入）→ 正确 p=0.134 且不拒绝 H₀；默认输入为 z=2/p=0.046/拒绝 H₀。
    inputs: { mean: "103", mu0: "100", sigma: "10", n: "25", tail: "two" },
    expect: ["Z = 1.5，p = 0.134", "p=0.134 ≥ α=0.05，不拒绝 H₀"],
    ref: "se=10/√25=2，z=(103−100)/2=1.5，双侧 p=2(1−Φ(1.5))=0.13361（Python math.erf 独立复算）→ 不拒绝 H₀",
  },
];

// ---------------------------------------------------------------- DOM stub
// canvas 2D 上下文桩（所有方法为空实现，measureText 返回零宽度以适配排版计算）
const CTX2D = new Proxy(
  { measureText: () => ({ width: 0 }), createLinearGradient: () => ({ addColorStop() {} }), canvas: { width: 0, height: 0, clientWidth: 300, clientHeight: 300 } },
  {
    get(t, k) {
      if (k in t) return t[k];
      return () => {};   // arc / fill / fillText / beginPath … 一律空实现
    },
    set() { return true; }, // ctx.fillStyle = … 等属性写入
  }
);

function makeEl(val) {
  const handlers = {};
  const el = {
    value: val === undefined ? "" : val,
    textContent: "",
    // 与真实 <select> 对齐：页面常读 el.selectedOptions[0].text 取选项标签，
    // 缺此属性会在 calc() 抛 "Cannot read properties of undefined" 使整页无法验证。
    selectedOptions: [
      { text: String(val === undefined ? "" : val), value: String(val === undefined ? "" : val), selected: true },
    ],
    checked: false,
    style: {},
    dataset: {},
    children: [],
    _handlers: handlers,
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener(ev, cb) { (handlers[ev] = handlers[ev] || []).push(cb); },
    removeEventListener() {},
    fire(ev) { for (const cb of handlers[ev] || []) cb({ target: el, preventDefault() {}, stopPropagation() {} }); },
    appendChild(c) {
      this.children.push(c);
      // 真实 DOM 会把子节点内容反映到父节点，结果采集依赖这一点
      const piece = (c && c.innerHTML) || (c && c.textContent) || "";
      if (piece) this.innerHTML = String(this.innerHTML || "") + piece;
      return c;
    },
    removeChild() {},
    insertAdjacentHTML() {},
    setAttribute() {},
    getAttribute() { return null; },
    removeAttribute() {},
    querySelector() { return makeEl(""); },
    querySelectorAll() { return []; },
    closest() { return null; },
    focus() {},
    click() {},
    remove() {},
    getBoundingClientRect() { return { width: 0, height: 0, top: 0, left: 0 }; },
    clientWidth: 300,
    clientHeight: 300,
    offsetWidth: 300,
    offsetHeight: 300,
    parentElement: { textContent: "", clientWidth: 300, clientHeight: 300, offsetWidth: 300, offsetHeight: 300, getBoundingClientRect: () => ({ width: 300, height: 300, top: 0, left: 0 }) },
    parentNode: null,
    // canvas 2D 上下文桩：含图表的页面（如 healthcare/tdee-calculator 的热量环形图）
    // 在 calc() 里直接 ctx.arc/fillText，缺了会抛 "getContext is not a function" 使整页无法验证。
    getContext() { return CTX2D; },
  };
  let _h = "";
  Object.defineProperty(el, "innerHTML", {
    set(v) { _h = String(v == null ? "" : v); },
    get() { return _h; },
  });
  return el;
}

function inlineScripts(html) {
  const out = [];
  for (const m of html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = m[1] || "";
    if (/\bsrc=/i.test(attrs)) continue;
    if (/type\s*=\s*["']?(application|text\/template|text\/tailwindcss)/i.test(attrs)) continue;
    out.push(m[2]);
  }
  return out.filter((c) => c.trim().length > 40).join("\n");
}

/**
 * 提取 HTML 内联事件属性（oninput / onclick / onchange …）。
 * 很多工具页不用 addEventListener，而是直接在标签上写 oninput="encode()"，
 * stub 若不解析这些属性，注入输入后永远触发不到转换逻辑。
 */
function inlineHandlers(html) {
  const map = {};
  for (const m of html.matchAll(/<[a-zA-Z][^>]*\bid="([^"]+)"[^>]*>/g)) {
    const tag = m[0];
    const id = m[1];
    for (const h of tag.matchAll(/\bon(input|change|click|keyup|blur|submit)\s*=\s*"([^"]*)"/gi)) {
      const code = h[2]
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, "&")
        .replace(/&#39;/g, "'")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">");
      if (!code.trim()) continue;
      (map[id] = map[id] || {})[h[1].toLowerCase()] = code;
    }
  }
  return map;
}

function collectStrings(elements) {
  // 收集所有「可能被写入结果」的字符串：value 与 innerHTML
  const seen = [];
  for (const [id, el] of Object.entries(elements)) {
    const v = el && el.value !== undefined && el.value !== "" ? String(el.value) : "";
    const h = el && el.innerHTML ? String(el.innerHTML) : "";
    const tc = el && el.textContent !== undefined && el.textContent !== "" ? String(el.textContent) : "";
    for (const s of [v, h, tc]) {
      if (s && s.trim()) seen.push(s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
    }
  }
  return seen.join("\n");
}

async function runCase(c) {
  // 每个用例都会往 globalThis（当作 window）挂函数，用后清理，避免污染下一个用例
  const before = new Set(Object.keys(globalThis));
  try {
    return await runCaseInner(c);
  } finally {
    for (const k of Object.keys(globalThis)) {
      if (!before.has(k)) { try { delete globalThis[k]; } catch (e) { /* 只读属性跳过 */ } }
    }
  }
}

async function runCaseInner(c) {
  _rngReset(); // 每个用例前重置随机种子，确保随机页输出与顺序/环境无关
  const file = path.join(TOOLS_DIR, c.slug + ".html");
  if (!fs.existsSync(file)) return { ok: false, why: "文件不存在" };
  const html = fs.readFileSync(file, "utf8");

  const defaults = {};
  for (const m of html.matchAll(/<input[^>]*id="([^"]+)"[^>]*value="([^"]*)"/g)) defaults[m[1]] = m[2];
  for (const m of html.matchAll(/<textarea[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/textarea>/g))
    defaults[m[1]] = m[2].replace(/&#10;/g, "\n").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
  const sel = {};
  for (const m of html.matchAll(/<select[^>]*id="([^"]+)"[\s\S]*?<\/select>/g))
    sel[m[1]] = [...m[0].matchAll(/<option[^>]*value="([^"]*)"/g)].map((x) => x[1]);

  const script = inlineScripts(html);
  if (!script.trim()) return { ok: false, why: "无内联脚本" };

  // 还原页面标题 / h1 / label 文本：很多工具用 document.querySelector('h1').textContent
  // （或 title）做「计算模式分支」选择，stub 若不提供真实文本会落入兜底零值分支，导致验证失真。
  const stripTags = (s) => s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const h1Text = stripTags((html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i) || [,""])[1]);
  const titleText = stripTags((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [,""])[1]);
  const labelTexts = [...html.matchAll(/<label[^>]*>([\s\S]*?)<\/label>/gi)].map((m) => stripTags(m[1]));

  const inline = inlineHandlers(html);
  const elements = {};
  const getEl = (id) => {
    if (!(id in elements)) {
      const v =
        c.inputs && id in c.inputs
          ? c.inputs[id]
          : defaults[id] !== undefined
          ? defaults[id]
          : sel[id]
          ? sel[id][0]
          : "";
      elements[id] = makeEl(v);
      // 把内联 on* 属性注册成事件处理器，使 fire() 能触发页面真实逻辑
      const ih = inline[id];
      if (ih) {
        for (const [ev, code] of Object.entries(ih)) {
          try {
            elements[id].addEventListener(ev, new Function("event", code));
          } catch (e) { /* 语法异常的内联代码忽略 */ }
        }
      }
    }
    return elements[id];
  };
  // 关键：页面普遍用 DOMContentLoaded 做初始化与事件绑定，stub 必须收集并执行这些回调，
  // 否则后续调用转换函数时内部状态（如 currentAlgo）根本没建立。
  const readyCbs = [];
  const document = {
    getElementById: getEl,
    getElementsByName: () => [],
    getElementsByClassName: () => [],
    querySelector(sel) {
      // 与真实 DOM 对齐：查询「已选中项」时，未选中应返回 null。
      // stub 原先恒返回空元素（truthy），会让 `el ? el.value : fallback` 拿到空串 ""
      // 从而误入非默认分支（如 down-payment 的还款方式掉进等额本金）。
      // 用例可用 checks 声明选中项，此处返回首个选中值。
      if (/:checked/.test(sel)) {
        // 补桩（parentElement）：大量「量表/选项评估」类页面（如中医 Naranjo 关联性评价）
        // 读到选中项后会立即读取 `checked.parentElement.textContent` 取选项标签，
        // 缺该属性会在首个已答项抛 "Cannot read properties of undefined"，使整例无法验证。
        // 这里补一个最小桩（textContent 为空串），仅补齐属性、不改变既有语义。
        if (c.checks && c.checks.length)
          return { value: c.checks[0], checked: true, parentElement: { textContent: "" } };
        return null;
      }
      // 提供真实 h1 / title 文本，供「按标题分支」的计算逻辑正确选模式
      if (/^h1$/i.test(sel)) { const e = makeEl(""); e.textContent = h1Text; e.value = h1Text; return e; }
      if (/^title$/i.test(sel)) { const e = makeEl(""); e.textContent = titleText; e.value = titleText; return e; }
      return makeEl("");
    },
    querySelectorAll(sel) {
      // 支持 ':checked' 类选择器：用例可用 checks 声明哪些复选框处于选中态
      if (/checked/.test(sel) && c.checks)
        return c.checks.map((v) => ({ value: v, checked: true, parentElement: { textContent: "" } }));
      // 提供真实 label 文本，部分工具据此命名输出字段
      if (/label/i.test(sel)) return labelTexts.map((t) => { const e = makeEl(""); e.textContent = t; e.value = t; return e; });
      return [];
    },
    createElement: () => makeEl(""),
    createTextNode: (t) => ({ textContent: t }),
    addEventListener(ev, cb) {
      if (/DOMContentLoaded|readystatechange|^load$/i.test(ev)) readyCbs.push(cb);
    },
    documentElement: { setAttribute() {}, getAttribute() { return null; }, style: {}, classList: { add() {}, remove() {}, toggle() {} } },
    body: makeEl(""),
  };
  const localStorage = { getItem() { return null; }, setItem() {}, removeItem() {} };
  const ToolBox = {
    setResult: (id, h) => { getEl(id).innerHTML = h; },
    toggleToolTheme() {},
    escHtml: (x) => String(x == null ? "" : x),
    escapeHtml: (x) => String(x == null ? "" : x),
    copy: () => {}, copyText: () => {}, toast: () => {}, showToast: () => {},
    t: (k, d) => d || k,
    // 与页面 TOOLBOX-API-STUB 保持一致：多数工具的 fmt() 直接转发到 formatNumber，
    // 缺了它依赖千分位格式化的页面会在 calc() 首行抛错，导致整页无法验证。
    formatNumber: (n, dec) => {
      if (typeof n !== "number" || isNaN(n)) return String(n);
      dec = dec != null ? dec : 0;
      return n.toLocaleString("zh-CN", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    },
    // 同 stub：明细表渲染。返回 HTML 字符串即可，collectStrings 会剥离标签后再断言。
    createTable: (headers, rows) => {
      let x = "<table><thead><tr>";
      (headers || []).forEach((t) => { x += "<th>" + (t == null ? "" : String(t)) + "</th>"; });
      x += "</tr></thead><tbody>";
      (rows || []).forEach((row) => {
        x += "<tr>";
        (row || []).forEach((c) => { x += "<td>" + (c != null ? String(c) : "") + "</td>"; });
        x += "</tr>";
      });
      return x + "</tbody></table>";
    },
  };
  const navigator = { userAgent: "node", clipboard: { writeText() {} } };
  // window 直接用 globalThis：内联 on* 属性编译出的函数在全局作用域执行，
  // 只能看到挂在 window（即全局）上的函数，用普通对象会导致「xxx is not defined」。
  const win = globalThis;
  const added = new Set(Object.keys(win));
  win.addEventListener = (ev, cb) => { if (/DOMContentLoaded|^load$/i.test(ev)) readyCbs.push(cb); };
  win.localStorage = localStorage;
  win.location = { href: "", search: "" };
  win.navigator = navigator;
  win.document = document;
  win.ToolBox = ToolBox;
  // 图表页会读 CSS 变量取色（如 healthcare/tdee-calculator 的 resolveCanvasColor），
  // 没有 getComputedStyle 会在 calc() 首行抛 "getComputedStyle is not defined"。
  win.getComputedStyle = () => ({ getPropertyValue: () => "" });

  const names = [...script.matchAll(/^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(/gm)].map((m) => m[1]);
  const PRIO = ["calcTool", "calc", "calculate", "compute", "convert", "run", "update", "render"];
  const ordered = [
    ...PRIO.filter((p) => names.includes(p)),
    ...names.filter(
      (n) => !PRIO.includes(n) && /^(calc|compute|convert|update|render|do|run|encode|decode|gen|handle|apply|build|format|to[A-Z])/.test(n)
    ),
    ...names.filter((n) => !PRIO.includes(n)),
  ];

  // 定时器桩：页面常用 requestAnimationFrame(loop) / setTimeout(loop, n) 做动画或渲染循环。
  // 原先传 (f)=>f() 会「立即同步」调用，循环变无限同步递归 → 几秒内吃光内存 OOM（image/gif-split
  // 等重型页因此拖垮整批还原）。这里改成「有限次立即执行」：预算耗尽即变 no-op，既允许合法的
  // 一次性延迟/几帧渲染，又掐断无限循环。
  let _timerBudget = 100;
  const safeTimer = (f) => {
    if (typeof f !== "function") return 0;
    if (_timerBudget-- <= 0) return 0;
    try { f(); } catch (e) { /* 定时器回调异常不影响主流程 */ }
    return 0;
  };
  const expose = ordered.map((n) => `try{__f[${JSON.stringify(n)}]=typeof ${n}==='function'?${n}:null;}catch(e){}`).join("\n");
  let fns;
  try {
    const compiled = new Function(
      "document", "window", "console", "navigator", "localStorage", "ToolBox", "alert", "setTimeout", "requestAnimationFrame", "setInterval", "requestIdleCallback", "Date",
      `var __f={};\n${script}\n${expose}\nreturn __f;`
    );
    fns = compiled(document, win, { log() {}, warn() {}, error() {} }, navigator, localStorage, ToolBox, () => {}, safeTimer, safeTimer, safeTimer, safeTimer, FrozenDate);
  } catch (e) {
    return { ok: false, why: "初始化失败: " + e.message.slice(0, 80) };
  }

  // 浏览器里传统 <script> 的顶层函数声明会成为 window 属性，内联 on* 才能调到；
  // 而 new Function 编译出的顶层函数只存在于函数作用域，必须先导出到 globalThis。
  for (const [n, f] of Object.entries(fns)) {
    if (typeof f === "function") { try { globalThis[n] = f; } catch (e) { /* 只读全局跳过 */ } }
  }

  const errs = [];

  // 1) 执行 DOMContentLoaded 回调（完成初始化与事件绑定）
  const pending = [];
  for (const cb of readyCbs) {
    try { const r = cb(); if (r && typeof r.then === "function") pending.push(r); }
    catch (e) { errs.push("ready: " + e.message.slice(0, 50)); }
  }
  // 2) 覆盖输入并触发真实的 input/change 事件（最贴近用户实际操作）
  if (c.inputs) {
    for (const [id, v] of Object.entries(c.inputs)) {
      const el = getEl(id);
      el.value = v;
      for (const ev of ["input", "change", "keyup"]) {
        try { const r = el.fire(ev); if (r && typeof r.then === "function") pending.push(r); }
        catch (e) { errs.push(id + "." + ev + ": " + e.message.slice(0, 40)); }
      }
    }
    await Promise.allSettled(pending);   // async 处理函数（如 crypto.subtle）需等其落盘
    const blob1 = collectStrings(elements);
    for (const want of c.expect) {
      if (blob1.includes(want)) return { ok: true, via: "input event" };
    }
  }
  // 3) 兜底：直接调用候选函数
  // 跳过「状态破坏性 / 辅助」类函数：resetAll / clearHistory / restoreHistory / saveHistory /
  // renderHistory / swapValues 等会改写输入或覆盖 res 输出，导致扰动态结果被默认值吞掉
  // （strength-1、carbon-5 等页因此假同态）。只跑真正的计算函数。
  const DESTRUCTIVE = /^(reset|clear|restore|save|swap)\b|history|reset|clear/i;
  for (const n of ordered) {
    if (DESTRUCTIVE.test(n)) continue;
    const f = fns[n];
    if (!f) continue;
    try {
      const r = f();
      if (r && typeof r.then === "function") { await r; }
    } catch (e) {
      errs.push(n + ": " + e.message.slice(0, 50));
      continue;
    }
    const blob = collectStrings(elements);
    for (const want of c.expect) {
      if (blob.includes(want)) return { ok: true, via: n };
    }
  }
  const blob = collectStrings(elements);
  return {
    ok: false,
    why: "未匹配期望值",
    errs: errs.slice(0, 3),
    tried: ordered.slice(0, 6),
    sample: blob.slice(0, 300),
    fullBlob: blob,
  };
}

// ---------------------------------------------------------------- 用例抽取（字符串感知）
// 供反回归门禁 / 还原工具复用：括号匹配时跳过字符串字面量（' " `）内的 [ ]，
// 否则 ref/expect 含 "(100,300]" 这类字符会让匹配错位 → eval 语法报错。
function extractCases(src) {
  const marker = "const CASES = [";
  const start = src.indexOf(marker);
  if (start === -1) return null;
  const i = src.indexOf("[", start);
  let depth = 0, inStr = null, escape = false, end = -1;
  for (let k = i; k < src.length; k++) {
    const ch = src[k];
    if (inStr) {
      if (escape) { escape = false; continue; }
      if (ch === "\\") { escape = true; continue; }
      if (ch === inStr) { inStr = null; continue; }
      continue;
    }
    if (ch === '"' || ch === "'" || ch === "`") { inStr = ch; continue; }
    if (ch === "[") { depth++; continue; }
    if (ch === "]") { depth--; if (depth === 0) { end = k; break; } }
  }
  if (end === -1) return null;
  const casesSrc = src.slice(start, end + 1).replace(marker, "[");
  // eslint-disable-next-line no-eval
  return eval(casesSrc);
}

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0;
  const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) {
      pass++;
      console.log(`✅ ${c.slug}  (via ${r.via})  — ${c.ref}`);
    } else {
      fails.push(c.slug);
      console.log(`❌ ${c.slug}  ${r.why}`);
      if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
      if (r.sample) console.log("     got: " + r.sample.slice(0, 200));
    }
  }
  console.log(`\n==== ${pass}/${cases.length} 通过 ====`);
  return fails.length;
}

module.exports = { runCase, CASES, inlineScripts, makeEl, collectStrings, extractCases };

// 注意：runCase 会清理用例往 globalThis（当作 window）挂的属性，process 可能被页面脚本覆盖，
// 故此处用 process.exitCode 而非 process.exit()。
if (require.main === module) main().then((f) => { process.exitCode = f ? 1 : 0; });
