// Node DOM-stub harness: runs each tool's calcTool() with default inputs,
// captures #result innerHTML, and reports JS errors.
const fs = require("fs");
const path = require("path");

const TOOLS_DIR = path.join(__dirname, "..", "tools");
const targets = [
  // Batch 70 aerospace II
  "aerospace/dynamic-pressure", "aerospace/drag-force",
  "aerospace/lift-equation", "aerospace/thrust-to-weight",
  "aerospace/orbital-velocity", "aerospace/escape-velocity",
  "aerospace/centripetal-accel", "aerospace/orbital-period",
  "aerospace/rocket-delta-v", "aerospace/payload-fraction",
  "aerospace/aspect-ratio", "aerospace/wing-area-from-loading",
  "aerospace/reynolds-number", "aerospace/bank-angle-load",
  // N4-02 batch 01 (it tools)
  "it/url-params", "it/image-to-base64", "it/csv-to-html-table",
  "it/line-ending-converter", "it/code-line-counter",
  // N4-02 batch 02 (finance/securities/health)
  "finance/installment-real-rate", "securities/bond-duration",
  "health/pregnancy-weight-gain", "health/safe-period-calculator",
  "health/milk-tea-calories",
  // N4-02 batch 03 (securities/decor/construction/electrical)
  "securities/bond-convexity", "decor/ceiling-panel-quantity",
  "construction/renovation-labor-cost", "construction/cement-mortar-ratio",
  "electrical/wire-gauge-selector",
  // N4-02 batch 04 (electrical/steel/fun)
  "electrical/breaker-sizing", "steel/steel-profile-weight",
  "fun/hotpot-portion", "fun/bbq-portion", "fun/random-name-gen",
  // N4-02 batch 05 (ecommerce/sales/hr)
  "ecommerce/groupon-filler", "sales/cost-price-margin",
  "hr/comp-time-calculator", "hr/annual-leave-prorate",
  // N4-02 batch 06 (parenting/home/electrical)
  "parenting/feeding-amount-baby", "parenting/formula-mixing",
  "parenting/diaper-usage", "parenting/pumping-plan",
  "home/washer-capacity", "electrical/home-load-estimate",
  // P3-1 batch 07 (life/fun/finance/hr)
  "life/drinking-water-plan", "fun/meditation-timer",
  "finance/salary-after-tax",
  "finance/credit-card-grace-period",
  // P3-1 batch 08 (finance/fun/gardening/furniture/cable)
  "finance/points-redemption-value", "fun/wedding-banquet",
  "gardening/balcony-sunlight", "furniture/desk-dimensions",
  "cable/cable-tray-sizing",
  // P3-1 batch 09 (it/design)
  "it/markdown-to-html", "it/regex-common",
  "design/css-grid-generator", "design/breakpoint-queries",
  "it/phone-screen-sizes",
  // P3-1 batch 10 (it/design)
  "it/video-bitrate", "design/color-contrast-check",
  "design/pixel-art-generator", "it/bluetooth-version",
  "it/usb-version",
  // Q1 batch 01 (design/it converters & generators)
  "design/px-to-rem", "design/rem-to-px",
  "design/flexbox-generator", "design/vh-vw",
  "it/text-to-ascii", "it/text-to-unicode",
  // Q1 batch 02 (it csv/mac/ipv6/phone/git)
  "it/csv-to-yaml", "it/mac-generator",
  "it/ipv6-ula", "it/phone-parser",
  // Q1 batch 03 (it yaml/toml/json + emoji/latex)
  "it/yaml-to-toml", "it/toml-to-yaml",
  "it/yaml-to-json", "it/toml-to-json",
  "it/emoji-picker", "it/latex",
  // Q1 batch 04 (it xml/yaml/toml converters + random-string/whitespace)
  "it/xml-to-yaml", "it/yaml-to-xml",
  "it/xml-to-toml", "it/toml-to-xml",
  "it/random-string", "it/whitespace",
];

function extract(html) {
  // default input values
  const defaults = {};
  const re = /<input[^>]*id="([^"]+)"[^>]*value="([^"]*)"/g;
  let m;
  while ((m = re.exec(html))) {
    defaults[m[1]] = m[2];
  }
  // textarea values (content between open/close tags)
  const taRe = /<textarea[^>]*id="([^"]+)"[^>]*>([\s\S]*?)<\/textarea>/g;
  let tm;
  while ((tm = taRe.exec(html))) {
    defaults[tm[1]] = tm[2].replace(/&#10;/g, "\n").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
  }
  // script block containing calcTool (split on script tags, find the right chunk)
  const chunks = html.split(/<script>|<\/script>/);
  const script = chunks.find((c) => c.includes("function calcTool"));
  if (!script) throw new Error("no calcTool script found");
  return { defaults, script };
}

let failures = 0;
for (const t of targets) {
  const file = path.join(TOOLS_DIR, t + ".html");
  const html = fs.readFileSync(file, "utf8");
  // skip redirect stubs (TOOLBOX-REDIRECT): they have no calcTool script
  if (html.includes("TOOLBOX-REDIRECT")) {
    console.log(`\n[${t}] ⏭️  SKIP (redirect stub)`);
    continue;
  }
  const { defaults, script } = extract(html);
  // DOM stub
  const resultCapturer = { innerHTML: "" };
  const inputs = {};
  for (const k in defaults) {
    inputs[k] = { value: defaults[k] };
  }
  const elements = Object.assign({}, inputs, { result: resultCapturer });
  const document = {
    getElementById: (id) => {
      if (!(id in elements)) {
        // create on demand to avoid crashes
        elements[id] = { value: "0", innerHTML: "", checked: false, addEventListener() {}, appendChild() {}, querySelectorAll: () => [] };
      }
      return elements[id];
    },
    documentElement: { setAttribute() {}, getAttribute() { return null; } },
    createElement: () => { const el = { _t: "", _h: "" }; Object.defineProperty(el, "textContent", { set(v) { this._t = v; this._h = String(v == null ? "" : v); }, get() { return this._t; } }); Object.defineProperty(el, "innerHTML", { set(v) { this._h = v; }, get() { return this._h; } }); return el; },
    querySelectorAll: () => [],
    addEventListener() {},
  };
  const ToolBox = {
    setResult: (id, html) => { document.getElementById(id).innerHTML = html; },
    toggleToolTheme() {},
  };
  try {
    const fn = new Function("document", "ToolBox", "Math", "parseFloat", "isNaN", "console", script + "\n; calcTool(); return document.getElementById('result').innerHTML;");
    const out = fn(document, ToolBox, Math, parseFloat, isNaN, console);
    // sanity: result not empty, no obvious "NaN"/"undefined"
    const bad = /NaN|undefined|Infinity/.test(out);
    const len = out ? out.length : 0;
    if (bad) failures++;
    console.log(`\n[${t}] ${bad ? "❌ BAD VALUE" : "✅ ok"}  outlen=${len}`);
    // strip tags for compact display
    const txt = out.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
    console.log("   " + txt.slice(0, 400));
  } catch (e) {
    failures++;
    console.log(`\n[${t}] ❌ JS ERROR: ${e.message}`);
  }
}
console.log(`\n==== ${failures === 0 ? "ALL OK" : failures + " FAILURES"} ====`);
process.exit(failures === 0 ? 0 : 1);
