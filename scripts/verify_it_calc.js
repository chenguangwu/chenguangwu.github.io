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
    // 原为 all_default 弱用例：textarea 默认内容就是 "123456789"；且 expect 同时列大写/小写 → 无论 upper 如何都命中，零判别力。
    // 改注入 "abc"（独立核对 python zlib.crc32(b"abc") = 0x352441c2）+ 显式声明 upper 选中 → 只断言大写形态。
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    checkIds: ["upper"],
    expect: ["CRC-32 0x352441C2"],
    ref: "python zlib.crc32(b'abc') = 0x352441c2（CRC-32/ISO-HDLC）→ 页面大写渲染 0x352441C2。回退默认（input=123456789 且 upper 未选中）→ 0xcbf43926（小写），不命中。",
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

  // —— §7.4 覆盖缺口线（BATCH161）——
  {
    slug: "it/atbash-cipher",
    inputs: { input: "abc" },
    expect: ["zyx"],
    ref: "阿塔巴什密码：字母表镜像 26−k+1 ⇒ a→z、b→y、c→x，'abc' 加密仍得 'zyx'。默认态 input 为空、encodeAtbash 走 alert 早退，结果区无 'zyx'（双态核验：注入 PASS / 默认 FAIL）。",
  },
  {
    slug: "it/bacon-cipher",
    inputs: { input: "ab", mode: "01" },
    expect: ["0000000001"],
    ref: "培根密码 mode=01：每字母 5 位，A=00000、B=00001 ⇒ 'ab' → '0000000001'。默认态 input 为空 ⇒ 早退，不命中。",
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", b: "10", op: "AND" },
    expect: ["结果： 8 = 0x8 = 0b1000"],
    ref: "12 & 10 = 8（二进制 1100 ∧ 1010 = 1000）；页面按 十进制/十六进制/二进制 三进制并排输出，锚完整连续串。默认 a=b=0 且 op=AND ⇒ 结果区为 0，不命中。",
  },
  {
    slug: "it/binary-to-text",
    inputs: { input: "01000001" },
    expect: ["A"],
    ref: "8 位二进制按字节解码：01000001 = 0x41 = 'A'。默认态解码区为空 ⇒ 不命中（双态核验已确认判别力；此处仅断言单字符是够用的，因为默认态 blob 完全不含该输出）。",
  },
  {
    slug: "it/adfgvx-cipher",
    inputs: { input: "abc" },
    expect: ["A A F D D G"],
    ref: "ADFGVX 多表替换：'abc' 经加密方格替换后再按 ADFGVX 列调位置排列，得 'A A F D D G'。默认态输入为空 ⇒ 不命中。",
  },
  {
    slug: "it/binomial-distribution",
    inputs: { n: "10", p: "0.5", k: "3" },
    expect: ["P(X = 3) = 0.117", "C(10, 3) = 120"],
    ref: "X~B(10,0.5)：P(X=3)=C(10,3)·0.5³·0.5⁷=120×0.125×0.0078125=0.1172（Python comb(10,3)=120、binom.pmf(3,10,0.5)=0.1172）；分步区同步给出 C(10,3)=120。默认 n/p/k 与注入值不同，两串均不出现。",
  },
  {
    slug: "it/clamp-calculator",
    // 页面斜率取两路较大值：slope1=(pref−min)/(vwMin/100)、slope2=(max−min)/(vwMax/100)，rem=pref−vw·vwMin/100。
    // 注入 min=10 / max=100 / vwMin=50（pref 用默认 24）⇒ slope1=(24−10)/0.5=28、slope2=90/14.4=6.25 ⇒ vw=28、rem=24−28×0.5=10。
    inputs: { min: "10", max: "100", vwMin: "50" },
    expect: ["生成表达式： clamp(10px, 28vw + 10px, 100px)"],
    ref: "独立复算：slope1=(24−10)/(50/100)=28、slope2=(100−10)/(1440/100)=6.25 ⇒ 取大者 28vw；截距 rem=24−28×50/100=10 ⇒ clamp(10px, 28vw + 10px, 100px)。默认 min/max/vwMin 为 16/48/375，表达式不同 ⇒ 不命中。",
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "100", std: "15", n: "30", conf: "0.95" },
    expect: ["[ 94.632 , 105.368 ]", "临界值 z = 1.960"],
    ref: "独立复算：SE=s/√n=15/√30=2.7386；95% 双侧 z=1.960 ⇒ ME=1.960×2.7386=5.3677 ⇒ CI=[94.632, 105.368]。默认输入不同（区间两端数不同）⇒ 两串均不出现。",
  },
  {
    slug: "it/code-line-counter",
    // textarea 注入带换行的代码：input event 阶段直接喂多行串（runner 的 inputs 支持多行值）。
    inputs: { codeInput: "def f():\n    return 1\n", langSel: "python" },
    expect: ["3 总行数 2 代码行 0 注释行 1 空行 66.7% 代码占比"],
    ref: "注入 3 行文本（末行为空）：总行数 3 = 2 代码行 + 1 空行，代码占比 2/3=66.7%。默认示例代码行数与占比不同 ⇒ 不命中。detectLang 在注入非空时可用，故结果区实际刷新。",
  },
  {
    slug: "it/charset-detector",
    inputs: { txt: "hello" },
    expect: ["未检测到明显乱码特征。 修复输出： hello"],
    ref: "普通 ASCII 文本无乱码特征 ⇒ 判为「未检测到明显乱码特征」并把原文原样回吐为修复结果。默认态正文（中文占位）走另一分支，不命中（双态核验：注入 PASS / 默认 FAIL）。",
  },
  {
    slug: "it/hypergeometric-distribution",
    // 超几何分布：P(X=k)=C(K,k)·C(N−K,n−k)/C(N,n)。N=20,K=5,n=3,k=2 ⇒ 10×15/1140=0.13158。
    inputs: { N: "20", K: "5", n: "3", k: "2" },
    expect: ["P(X = 2) = 0.132", "C(20, 3) = 1,140"],
    ref: "Python comb(5,2)=10、comb(15,1)=15、comb(20,3)=1140 ⇒ P=10×15/1140=0.1316（页面渲染 0.132、分步区给出 C(20,3)=1,140）。默认 N/K/n/k 与注入值不同，两串均不出现。",
  },
  {
    slug: "it/hmac-generator",
    // 页面 crypto.subtle.importKey 在 harness 下抛 2，但结果区仍渲染出正确 HMAC 串 ⇒ 走的是页面自实现分支。
    inputs: { key: "secret", msg: "hello" },
    expect: ["HMAC-SHA1 5112055c05f944f85755efc5cd8970e194e9f45b",
             "HMAC-SHA256 88aab3ede8d3adf94d26ab90d3bafd4a2083070c3bcce9c014ee04a443847c0b"],
    ref: "Python hmac.new(b'secret', b'hello', sha1).hexdigest() = 5112055c05f944f85755efc5cd8970e194e9f45b；sha256 = 88aab3ede8d3adf94d26ab90d3bafd4a2083070c3bcce9c014ee04a443847c0b（四档 SHA1/256/384/512 页侧与 Python 逐一核对一致）。注：harness 下 subtle.importKey 抛错，但结果区仍落正确值，断言的是「正确值」而非错误分支。",
  },
  {
    slug: "it/json-minify",
    inputs: { input: '{"a": 1, "b": [2, 3]}' },
    expect: ['{"a":1,"b":[2,3]}', "原始 21 字节 → 输出 17 字节 · Compression ratio 19.0%"],
    ref: "独立复算：原文 len('{\"a\": 1, \"b\": [2, 3]}')=21、压缩后 len('{\"a\":1,\"b\":[2,3]}')=17 ⇒ 比值 (21−17)/21=19.05% ⇒ 页面渲染 19.0%。默认示例的字节数与比值均不同 ⇒ 不命中。",
  },
  {
    slug: "it/json-path",
    inputs: { input: '{"a":{"b":[1,2,3]}}', path: "$.a.b" },
    expect: ["[ 1 , 2 , 3 ]"],
    ref: "JSONPath 表达式 $.a.b 命中数组 [1,2,3] ⇒ 输出按页侧格式展开为 `[ 1 , 2 , 3 ]`。默认 path 与默认 JSON 不同，不命中；expr 不以 $ 开头时页面直接报错（`jsonPath: JSONPath 表达式必须以 $ 开头`），不影响本例。",
  },
  {
    slug: "it/keyword-density",
    inputs: { inputText: "aa bb aa cc bb aa dd" },
    expect: ["排名 关键词 出现次数 占比 密度条 1 aa 3 42.86%"],
    ref: "注入 7 token（aa×3、bb×2、cc×1、dd×1）⇒ 排行表首行「aa 3 42.86%」（3/7=42.86%）；默认正文的排行表完全不同 ⇒ 不命中。锚取「表头 + 首行」的连续串，避免只锚 42.86% 这类可能被默认态作为子串命中的短数值。",
  },
  {
    slug: "it/locale-lookup",
    inputs: { input: "zh-CN" },
    expect: ["语言（ISO 639-1）： zh 国家（ISO 3166-1）： CN 完整名称： 简体中文（中国大陆）"],
    ref: "locale 标签解析：zh-CN ⇒ 语言 zh / 国家 CN / 完整名「简体中文（中国大陆）」/ 书写系统 Hans / 排序拼音。默认输入不同 ⇒ 不命中（双态核验：注入 PASS / 默认 FAIL）。",
  },
  {
    slug: "it/ipv6-converter",
    // 注意：默认地址（2001:db8::1）与注入值同串，属逃生项；改用非默认地址即可。
    inputs: { addr: "fe80::abcd" },
    expect: ["压缩形式：fe80::abcd"],
    ref: "IPv6 展开 + 压缩：fe80::abcd ⇒ 全展 `fe80:0000:…:abcd`、压缩回 `fe80::abcd`。**踩坑记录**：注入 `2001:db8::1`（也是页面默认地址）时默认态同样命中（逃生项，via=calcTool）；换成 fe80::abcd 后双态通过。",
  },
  {
    slug: "it/ipv4-range-expander",
    inputs: { cidr: "192.168.1.0/30" },
    expect: ["192.168.1.0 网络地址 192.168.1.3 广播地址 2 可用主机数 30 前缀长度"],
    ref: "/30 网段：网络地址 192.168.1.0、广播 192.168.1.3、可用主机 2（4−2）。默认示例前缀不同 ⇒ 不命中。",
  },
  {
    slug: "it/poisson-distribution",
    // 泊松分布 P(X=k)=λ^k·e^(−λ)/k!。λ=2,k=3 ⇒ 8×0.13534/6=0.180。
    inputs: { lambda: "2", k: "3" },
    expect: ["P(X = 3) = 0.18", "步骤 1： λ 3 = 8"],
    ref: "独立复算：λ^k=2³=8、e^(−2)=0.13534、k!=6 ⇒ P=8×0.13534/6=0.180（页面渲染 0.18），分步区同时给出 λ 3 = 8。默认 λ/k 与注入值不同 ⇒ 不命中。",
  },
  {
    slug: "it/numeronym-generator",
    inputs: { input: "global navigation" },
    expect: ["global → g4l navigation → n8n"],
    ref: "numeronym（首字母+中间字母个数+末字母）：global(6字母⇒4中间)→g4l；navigation(11字母⇒8中间)→n8n。默认示例单词不同 ⇒ 不命中。",
  },
  {
    slug: "it/prime-checker",
    // 注：n=97 的「97 是质数 ✅」是默认态同串（逃生项，via=calcTool），故改用 n=2 这个最小质数。
    inputs: { n: "2" },
    expect: ["2 是质数"],
    ref: "2 是最小质数。踩坑：注入 n=97 得到「97 是质数 ✅」在默认态同样命中（默认示例就是 97），属逃生项 ⇒ 改用 n=2（同样为真质数，但默认态不出现）。",
  },
  {
    slug: "it/rail-fence-cipher",
    // 只锚矩阵展示串：depth=2 的轨道矩阵 row0 取下标 0/2/4、row1 取 1/3/5。
    // 实测 enc/dec 两条渲染路径下 `acbbac` / `aabbcc` / `abcabc` 三串在注入态都能命中（分别由 enc/dec/默认渲染写入），
    // 故不存在「输出与逐行读法不符」的缺陷，别据此写缺陷报告。
    inputs: { input: "abcabc", depth: "2" },
    expect: ["行0: a · c · b · 行1: · b · a · c"],
    ref: "轨道围栏 depth=2：下标偶数位归入 row0（a,c,b）、奇数位归入 row1（b,a,c）⇒ 矩阵展示串 `行0: a · c · b · 行1: · b · a · c`。默认示例（不同 depth/文本）不命中。",
  },
  {
    slug: "it/triangle-calculator",
    // 三边 5/6/7 的最大角为 arccos(12/60)=78.46° < 90° ⇒ 锐角三角形；
    // 海伦面积 √(9·4·3·2)=√216≈14.697。默认态默认边 3/4/5 是直角三角形，不命中。
    inputs: { a: "5", b: "6", c: "7" },
    expect: ["锐角三角形", "14.697"],
    ref: "独立复算：p=18、s=9、area=√(9×4×3×2)=14.697；最大角 arccos((25+36−49)/60)=78.46° ⇒ 锐角三角形。踩坑：注入 3/4/5 与页面默认值相同 ⇒ 逃生项，改用 5/6/7。",
  },
  {
    slug: "it/time-format-converter",
    inputs: { inTime: "1600000000" },
    expect: ["2020-09-13T12:26:40.000Z"],
    ref: "Unix 秒 1600000000 = 2020-09-13T12:26:40.000Z（UTC）。踩坑：默认 1700000000，注入值撞默认会逃生。",
  },
  {
    slug: "it/statistical-power",
    // 只锚「功效 = 88.54%」；原 expect 第二条「临界值 z* = 1.96」是 α=0.05 双侧常量，
    // 默认态同样命中 ⇒ 逃生项（判据⑤静态常量），已剔除。
    inputs: { d: "1", n: "20", alpha: "0.05", tail: "two" },
    expect: ["功效 = 88.54%"],
    ref: "独立复算：δ=d×√(n/2)=1×3.162=3.162，z*=1.96 ⇒ 功效=Φ(1.202)+Φ(−5.122)≈0.885 ⇒ 88.5%；默认 d=0.5/n=64 得 80.7%，不命中。",
  },
  {
    slug: "it/text-truncate",
    // 默认「省略号」select 值为 "..."；words 模式 limit=2 ⇒ "Alpha beta" + "..."。
    inputs: { input: "Alpha beta gamma delta", limit: "2", mode: "words" },
    expect: ["Alpha beta..."],
    ref: "独立复算：按空白切词取前 2 个 ⇒ `Alpha beta`，附加省略号 `...`（页面省略号默认选项）⇒ `Alpha beta...`。默认态是长中文文本 + limit 20，不命中。",
  },
  {
    slug: "it/text-statistics",
    inputs: { textInput: "ab cd ab ef" },
    expect: ["11 总字符", "4 总词数"],
    ref: "独立复算：\"ab cd ab ef\" 共 11 个字符（含 2 个空格）、按空白切出 4 个英文词、去重 3 个 ⇒ `11 总字符` / `4 总词数`。默认态为中文长文本，不命中。",
  },
  {
    slug: "it/string-obfuscator",
    // mode 取值是 b64（不是 base64）；选错 mode 会落到空结果分支（输出 0 字符）。
    inputs: { input: "Hi there 42", mode: "b64" },
    expect: ["SGkgdGhlcmUgNDI="],
    ref: "独立复算：b64(\"Hi there 42\")=\"SGkgdGhlcmUgNDI=\"（16 字符），与页面「输出 16 字符」自洽。踩坑：mode=base64 不是合法选项。",
  },
  {
    slug: "it/toml-to-json",
    // 锚空输入兜底分支。该页曾因 `document.getElementById('sort')` 取到 null（排序复选框实际 id 为 top_1）
    // 在加载即抛 TypeError、整页无输出（jsdom 已验证，2026-09-26 修正为 id=\"sort\"）。
    // 本例锁的是修正后的空输入分支；JSON 正文走 escH()，harness 的 createElement 桩不回写
    // textContent→innerHTML（既有盲区），故无法锚 JSON 内容。
    inputs: { source: "" },
    expect: ["请输入 TOML 文本"],
    ref: "空输入时页面写入 `请输入 TOML 文本`；默认 TOML 非空不命中。该页此前为 P0 死页（sort id 不匹配），修复后本例才有判别力。",
  },
  {
    slug: "it/sql-formatter",
    // textarea 无 oninput ⇒ 注入不触发重算，必须在 clicks 里显式调 formatSql()。
    inputs: { input: "select a,b from t where a=1" },
    clicks: ["formatSql()"],
    expect: ["SELECT a, b FROM t WHERE a=1"],
    ref: "独立复算：关键字大写 + `a,b` 逗号后补空格 ⇒ `SELECT a, b FROM t WHERE a=1`（值 `a=1` 不加空格，与输入一致）。默认示例是长联表 SQL，不命中。",
  },
  {
    slug: "it/slugify",
    inputs: { input: "Hello World ToolBox" },
    expect: ["Hello-World-ToolBox"],
    ref: "独立复算：空格转连字符 ⇒ `Hello-World-ToolBox`（默认 `mode=空白转-`）。默认输入是中文标题（走拼音分支），不命中。",
  },
  {
    slug: "it/summary-generator",
    inputs: { inputText: "甲一句。乙二句？丙三句。" },
    expect: ["甲一句。"],
    ref: "独立复算：按句号/问号/叹号分句 3 句，权重取首个选中句 ⇒ 摘要以 `甲一句。` 开头。默认示例是 14 句长文，不命中。",
  },
  {
    slug: "it/text-replace",
    // 页面把 `doReplace` 挂在 `window` 上（非顶层 function 声明）⇒ 必须 clicks 显式驱动。
    inputs: { sourceText: "ab cd ab", findInput: "ab", replaceInput: "XY" },
    clicks: ["doReplace()"],
    expect: ["XY cd ab"],
    ref: "独立复算：非全局替换 ⇒ `ab cd ab` 只换第一处 `ab` ⇒ `XY cd ab`（第二处保留）。默认态源文本为空、直接 return，不命中。",
  },
  {
    slug: "it/text-similarity",
    inputs: { textA: "alpha beta", textB: "alpha gamma" },
    expect: ["0.6364", "编辑距离: 4"],
    ref: "独立复算：莱文斯坦距离 4、`len(A)=11` ⇒ 归一化 1−4/11=0.6364，与页面「63.64%（距离: 4）」自洽。默认态是更长示例文本，不命中。",
  },
  {
    slug: "it/text-dedupe-sort",
    // 页面函数都包在闭包里（`applyOp` 非顶层声明）⇒ 只能从 clicks 进，不能直接 input 事件驱动。
    inputs: { input: "fig\napple\nfig\npear" },
    clicks: ["applyOp('dedupe')"],
    expect: ["fig apple pear"],
    ref: "独立复算：按整行去重保留首次出现顺序 ⇒ fig / apple / pear 三行（原 4 行、删 1 行）。默认示例是 banana/file10 那套，不命中。",
  },
  {
    slug: "it/text-cleaner",
    inputs: { "input-text": "  a  b \n\n\n  c \n" },
    expect: ["a b c"],
    ref: "独立复算：去首尾空格 + 合并连续空格 + 删空行 ⇒ `a b c`（3 个 token）。默认态源文本为空、直接 return，不命中。",
  },
  {
    slug: "it/slug-generator-advanced",
    inputs: { text: "Foo Bar Baz!!! 中文标题", sep: "_", maxLen: "40" },
    clicks: ["generate()"],
    expect: ["Foo_Bar_Baz"],
    ref: "独立复算：分隔符 `-`→`_` + 转小写 + 去首尾符号 ⇒ `foo_bar_baz_再截断`（页面同时把原文回显在 `←` 右侧，锚只取左侧真产物 `Foo_Bar_Baz`）。生成走按钮 onclick，必须 clicks。",
  },
  {
    slug: "it/shell-script-formatter",
    inputs: { input: "echo a\necho b" },
    clicks: ["doMinify()"],
    expect: ["echo a; echo b"],
    ref: "独立复算：minify 对不以 `;/{(/\\\\/then/do` 结尾的行补 `; ` 连接 ⇒ `echo a; echo b`（单行合并）。**不要用 doBeautify**：harness 内 indent select 取不到数字 ⇒ `IND()` 为 `repeat(NaN)` 空串， beautify 产物与输入同形、任何锚都退化成输入回显伪锚（非缺陷，真机正常）。",
  },
  {
    slug: "it/sql-escape",
    inputs: { input: "O'Brien" },
    clicks: ["esc()"],
    expect: ["O\\'Brien"],
    ref: "独立复算：MySQL 方言把单引号转义为 `\\'` ⇒ `O\\'Brien`（反斜杠转义后长度 9）。默认态输入为空直接 return，不命中。",
  },
  {
    slug: "it/text-to-binary",
    inputs: { input: "AB", encoding: "ascii" },
    expect: ["01000001 01000010"],
    ref: "独立复算：ASCII 模式下 A=65/B=66 补 8 位 ⇒ 空格分隔的两字节码。默认态示例是 Hello 的 UTF-8，不命中。",
  },
  {
    slug: "it/text-to-ascii",
    inputs: { txt: "AZ" },
    clicks: ["calcTool()"],
    expect: ["0x41"],
    ref: "独立复算：A 的十进制 65 转十六进制 ⇒ `0x41`、二进制 `01000001`（结果表走 dataGrid，非纯 innerHTML）。默认示例 `Hello, ToolBox!` 不含 A 且码点从 72 起，不命中。",
  },
  {
    slug: "it/case-converter",
    inputs: { inputText: "foo bar BAZ" },
    expect: ["fooBarBaz"],
    ref: "独立复算：驼峰命名按「词边界合并」（3 词）⇒ `fooBarBaz`；同批产物 `FOO BAR BAZ` / `FOO_BAR_BAZ` 与输入仅大小写不同、易误判回显，故选形态差异最大的驼峰串。默认示例 `Hello World Test Case` 走另一分支，不命中。",
  },
  {
    slug: "it/url-encoder-advanced",
    inputs: { input: "a b&c=d/e?f" },
    clicks: ["enc()"],
    expect: ["a%20b%26c%3Dd%2Fe%3Ff"],
    ref: "独立复算：默认 `encodeURIComponent` 对空格 `& = / ?` 全部百分号编码 ⇒ 空 `%20`、`&`→`%26`、`=`→`%3D`、`/`→`%2F`、`?`→`%3F`。textarea 与 select 均无 oninput/onchange ⇒ 必须 clicks `enc()`。",
  },
  {
    slug: "it/list-converter",
    inputs: { input: "alpha\nbeta\ngamma", mode: "quote" },
    expect: ['"alpha", "beta", "gamma"'],
    ref: "独立复算：3 行按带引号格式用 `, ` 连接 ⇒ 双引号包裹的逗号串（产物在 textarea#output，非 result）。默认示例是水果词表，不命中。",
  },
  {
    slug: "it/list-converter",
    inputs: { input: "alpha\nbeta\ngamma", mode: "sql" },
    expect: ["('alpha', 'beta', 'gamma')"],
    ref: "独立复算：SQL IN 子句形态 ⇒ 单引号包裹、以 `, ` 连接、整体套圆括号。与 quote 模式同页同输入，靠 select 档位区分（判据⑧）。",
  },
  {
    slug: "it/char-encoder",
    inputs: { input: "Hi~" },
    expect: ["SGl+"],
    ref: "独立复算：`Hi~` 的 Base64 ⇒ `SGl+`（同批 ASCII 码 72,105,126 / Unicode U+0048… / 二进制 01001000…，任一都行）。默认态 input 为空 ⇒ 各编码块只渲染标题不渲染值，不命中。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=b&c" },
    clicks: ["enc()"],
    expect: ["a=3d"],
    ref: "独立复算：QP 编码把 `=` 转义为 `=3d` ⇒ `a=3db&c`（`&` 保留）。默认态输入为空直接 return，不命中。",
  },
  {
    slug: "it/html-entities",
    inputs: { encoderInput: "<b>Tom & Jerry</b>" },
    clicks: ["encodeAll()"],
    dumpIds: ["encoderOutput"],
    expect: ["&#60;&#98;&#62;"],
    ref: "独立复算：全字符编码把 `<` `b` `>` 转成 `&#60;&#98;&#62;`（`encodeText()` 只转 `&`/`<`/`>` 命名实体，产物是 `&lt;b&gt;Tom &amp; Jerry&lt;/b&gt;`，两者形态不同故可区分）。结果容器 `encoderOutput` 不在 harness 默认回写清单，须在用例里带 `dumpIds`。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "30", f_hour: "2" },
    expect: ["30 2 * * *"],
    ref: "独立复算：分钟/小时注入 30 / 2、日月月星期保持 `*` ⇒ 五段表达式 `30 2 * * *`。默认态是 `0 9 * * *`，不命中。",
  },
  {
    slug: "it/morse-decode-advanced",
    inputs: { input: ".. --- .." },
    clicks: ["dec()"],
    expect: ["IOI"],
    ref: "独立复算：`..` `---` `..` 三段解码 ⇒ `IOI`。**入口是 `dec()` 不是 `decode()`**（后者不存在，errs 会直接报 not defined）。默认示例是 `... --- ...` ⇒ SOS，不命中；常量参考表里有单字母电码但不含连续三字母串。",
  },
  {
    slug: "it/normal-distribution",
    inputs: { mu: "0", sigma: "1", x0: "1.96" },
    clicks: ["calculate()"],
    expect: ["P(X ≤ 1.96) = 0.975"],
    ref: "独立复算：标准正态 Φ(1.96)=0.975（Z 分数公式 (x−μ)/σ 一致 ⇒ 分步区显示 Z = 1.96、Φ = 0.975）。**只锚这一条**：同页还有 α=0.05 双侧临界值 `1.96` 与「0.025 / 0.975」等常量，默认态同命中（判据⑤），锚须带 `P(X ≤ …)` 前缀才唯一。",
  },
  {
    slug: "it/video-bitrate",
    inputs: { w: "1920", h: "1080", fps: "30", dur: "60", br: "5" },
    expect: ["3433.2 MB"],
    ref: "独立复算：页面口径 `大小 = 码率(Mbps) × 时长(s) ÷ 8 ÷ 1.048576` ⇒ 5 Mbps、60 s ⇒ 2145.8 MB；同公式下 1080p 推荐码率 8 Mbps ⇒ **3433.2 MB**（锚取推荐码率档的那一支，避开默认示例的当前码率值）。数字走 dataGrid，非 innerHTML。",
  },
  {
    slug: "it/uniform-distribution",
    inputs: { a: "2", b: "8", x: "5" },
    clicks: ["calculate()"],
    expect: ["F(5) = 0.5"],
    ref: "独立复算：U(a=2,b=8) 的 CDF F(5) = (5−2)/(8−2) = 0.5，PDF 1/6 = 0.167、均值 5、方差 3 均与之自洽（分步区写 (5−2)/6）。默认态是 a=0,b=1 那套，不命中。",
  },
  {
    slug: "it/color-converter",
    inputs: { colorInput: "#1E90FF" },
    clicks: ["fromInput('#1E90FF')"],
    expect: ["#1E90FF"],
    ref: "独立复算：`#1E90FF`(DodgerBlue) 转 HEX 大写 `#1E90FF`、RGB `rgb(30, 144, 255)`、HSL `hsl(210, 100%, 56%)`。抠 `#1E90FF` 这一支而非 `rgb(30, 144, 255)`：默认态示例 `#667eea` 走的是另一色，两条锚都不命中。入口是 `fromInput(v)`（带参），`convert()` 不存在。",
  },
  {
    slug: "it/margin-of-error",
    inputs: { n: "400", p: "0.5", conf: "0.95" },
    clicks: ["calculate()"],
    expect: ["±0.049"],
    ref: "独立复算：SE = √[0.5×0.5/400] = 0.025，E = 1.96 × 0.025 = ±0.049（相对 4.90%）⇒ 95% CI [0.451, 0.549]。**注入值避开默认 n=100** —— 默认态 SE=0.05、E=±0.098，与注入态不同 ⇒ 双态成立；但同页 `z* = 1.96` / `α = 0.05` 是 α=0.05 双侧常量（判据⑤），不能单独当锚。",
  },
  {
    slug: "it/password-strength",
    inputs: { pwd: "Abcdef1!" },
    expect: ["良好"],
    ref: "独立复算：8 位、含大小写+数字+特殊符号、非键盘序列、非弱密码 ⇒ 评分 4/5 档「良好」（页面另给熵 52 bit 与破解耗时）。默认示例是更长的弱串，落另一档，不命中。",
  },
  {
    slug: "it/whitespace",
    inputs: { source: "  a   b \n\n c \n" },
    clicks: [
      "document.getElementById('top_trim').checked=true;document.getElementById('top_blank').checked=true;document.getElementById('top_collapse').checked=true;document.getElementById('top_trail').checked=true;calcTool()",
    ],
    expect: ["处理后字符数 6"],
    ref: "独立复算：4 行输入（含 1 个空行）⇒ 删空行后 2 行、合并连续空格 + 去首尾空白 ⇒ 14 字符降到 6（`a b c\\n`）。**四个开关在桩内恒未勾 ⇒ 必须在 clicks 里逐个置 `checked=true` 再调 `calcTool()`**，否则与默认态完全一致（零差异）。",
  },
  {
    slug: "it/chmod-calculator",
    inputs: {},
    clicks: [
      "document.getElementById('r0').checked=true;document.getElementById('w0').checked=true;document.getElementById('x0').checked=true;document.getElementById('r1').checked=true;document.getElementById('x1').checked=true;document.getElementById('r2').checked=true;document.getElementById('w2').checked=true;document.getElementById('x2').checked=true;calc()",
    ],
    expect: ["chmod 757"],
    ref: "独立复算：用户 rwx=7、组 r-x=5、其他 rwx=7 ⇒ `757` 且符号位 `rwxr-xrwx`。checkbox 在桩内恒未勾（`inputs` 写 `checked` 不生效）⇒ 必须走这段 clicks；默认态（全勾 7）显示的是随机预设的另一组值，不命中。",
  },
  {
    slug: "it/regex-escape",
    inputs: { input: "a.b*c" },
    clicks: ["esc()"],
    expect: ["a\\.b\\*c"],
    ref: "独立复算：默认「通用 (JS)」风味下 `.` `*` 被转义、`/` 不转（勾「转义 /」另算）⇒ `a\\.b\\*c`。默认态输入为空直接 return，不命中。",
  },
  {
    slug: "it/markdown-lint",
    inputs: { src: "### 标题" },
    clicks: ["calcTool()"],
    expect: ["未发现明显风格问题"],
    ref: "独立复算：`### 标题` 属合法 ATX 标题、无其他风格项 ⇒ 问题 0 并落该结论串。默认示例含多个待整改项，结论不同，不命中。",
  },
  {
    slug: "it/c-string-escape",
    inputs: { input: "a\"b\\c\nd" },
    clicks: ["esc()"],
    expect: ["a\\\"b\\\\c\\nd"],
    ref: "转义产物非输入回显：引号→\\\"、反斜杠→\\\\、换行→\\n 逐一对应。默认示例不含该转义串。",
  },
  {
    slug: "it/java-escape",
    inputs: { input: "a\"b\\c", unicode: "1" },
    clicks: ["esc()"],
    expect: ["a\\\"b\\\\c"],
    ref: "Java 串内转义产物；unicode 档仅作形态区分，锚取与档位无关的基础转义部分。默认态不命中。",
  },
  {
    slug: "it/python-escape",
    inputs: { input: "a\"b\\c", qtype: "s" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\\\\c\""],
    ref: "qtype=s 走普通字符串 ⇒ 结果带双引号包裹，锚取含引号的完整产物，避开与 raw 串分支的同形。",
  },
  {
    slug: "it/rust-escape",
    inputs: { input: "a\"b\\c" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\\\\c\""],
    ref: "Rust 串内转义产物，默认输入（非引号/反斜杠）不产生同串。",
  },
  {
    slug: "it/css-escape",
    inputs: { input: "foo(bar)" },
    clicks: ["esc()"],
    expect: ["foo\\(bar\\)"],
    ref: "CSS.escape 风格逐字符加反斜杠，产物非原文回显。harness 内 escapeChar 报 undefined.code 属桩盲区（真机 DOM 事件源缺失），不影响产物串。",
  },
  {
    slug: "it/js-escape",
    inputs: { input: "a\"b\\c" },
    clicks: ["esc()"],
    expect: ["\"a\\\"b\\\\c\""],
    ref: "JS 串内转义产物（与 Rust/Python 同形态但页内实现独立），默认态不含。",
  },
  {
    slug: "it/polybius-cipher",
    inputs: { input: "AB" },
    expect: ["11 12"],
    ref: "A→11、B→12 的方格坐标拼接，随输入变化；默认示例对应其它坐标，不命中。",
  },
  {
    slug: "it/xor-cipher",
    inputs: { input: "AB", key: "XY" },
    clicks: ["calcTool()"],
    expect: ["191b"],
    ref: "0x19 0x1b 两字节异或密文（A^X=19、B^Y=1b）十六进制小写拼接。默认输入/密钥组合产物不同。",
  },
  {
    slug: "it/curl-parser",
    inputs: { cmd: "curl https://a.test/x?a=1" },
    expect: ["URL： https://a.test/x?a=1"],
    ref: "URL 由命令行解析得出（方法 GET、无 Header、无 Body），非原文回显；默认示例指向另一域名，不命中。",
  },
  {
    slug: "it/ini-parser",
    inputs: { input: "[s]\na=1\n[t]\nb=2" },
    clicks: ["iniToJson()"],
    expect: ['{ "s": { "a": "1" }, "t": { "b": "2" } }'],
    ref: "两个 section 各自成对象、键值保持字符串形态；默认示例 section 名不同，不命中。",
  },
  {
    slug: "it/properties-parser",
    inputs: { input: "a=1\nb=two" },
    clicks: ["propsToJson()"],
    expect: ['{ "a": "1", "b": "two" }'],
    ref: "properties 键值转 JSON 对象，值原样保留（含非数字串 two）；默认示例键/值组合不同。",
  },
  {
    slug: "it/json-schema-validator",
    inputs: { data: '{"a":1}', schema: '{"type":"object","required":["b"]}' },
    clicks: ["validateJSON()"],
    expect: ["未通过： 缺少必填字段: root.b"],
    ref: "schema 要求必填 b 而数据缺 b ⇒ 必报缺失字段并点名路径；默认示例通过校验，结论相反。",
  },
  {
    slug: "it/email-normalizer",
    inputs: { input: "A.B+tag@Google.com" },
    expect: ["a.b+tag@google.com"],
    ref: "小写化后输出（保留标签部分、未去点）；默认示例地址不同形，不命中。",
  },
  {
    slug: "it/protobuf-parser",
    inputs: { input: "message M { optional string a = 1; }" },
    clicks: ["parseProto()"],
    expect: ['"name": "M"'],
    ref: "message 名与字段（type/name/number/标记位）由语法树解析得出；默认示例 message 名不同，不命中。",
  },
  {
    slug: "it/math-evaluator",
    inputs: { expr: "2*(3+4)" },
    clicks: ["calc()"],
    expect: ["结果： 14"],
    ref: "先乘括号后乘除：2×7=14，验证运算符优先级与括号处理正确；默认表达式结果不同。",
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "苹果 香蕉 苹果 橙子 香蕉 苹果" },
    clicks: ["extractKeywords()"],
    expect: ["1 苹果 3 100.0%"],
    ref: "词频统计 + 相对频率（3/3=100.0%、2/3=66.7%），默认语料词表与频次均不同。",
  },
  {
    slug: "it/csv-to-html-table",
    inputs: { csvInput: "a,b\n1,2", sepSel: "," },
    expect: ["预览（2 行）"],
    ref: "行数统计随注入行数变化（默认示例行数不同 ⇒ 双态已排除同值巧合）。",
  },
  {
    slug: "it/regex-visualizer",
    inputs: { pattern: "^a(z+)" },
    clicks: ["render()"],
    expect: ["3 --z--> 4"],
    ref: "默认 pattern 为 `^a[0-9]+b$`（含 a 转移、无 z 转移）⇒ 锚取注入态独有的 z 转移边；`1 --a--> 2` 在默认态同命中，不可用。",
  },
  {
    slug: "it/markdown-to-html",
    inputs: { md: "## Hello World" },
    expect: ["Hello World"],
    ref: "二级标题渲染出的文本节点（注入串去掉 `##` 前缀后作为标题文本落进结果区）；默认示例标题词表不含该串。",
  },
  {
    slug: "it/emoji-picker",
    inputs: { q: "cat" },
    expect: ["共 1 个 emoji（点击复制） 🐱"],
    ref: "关键词 cat 命中的唯一 emoji 及其计数与复制提示组成连续串；默认关键词命中集合不同，不命中。",
  },
  {
    slug: "it/html-minifier",
    inputs: { input: "<p>a</p>\n<p>b</p>" },
    clicks: ["minify()"],
    expect: ["a b"],
    ref: "标签被剥除、两个块内文本以空格相连（`a b`），非原文回显；默认示例压缩结果不同。",
  },
  {
    slug: "it/python-formatter",
    inputs: { input: "x=1\nif x>0:\n  print(x)" },
    clicks: ["doMinify()"],
    expect: ["x=1; if x>0: print(x)"],
    ref: "压缩路径把语句以 `; ` 连接、缩进丢弃；默认示例结构不同，不命中。",
  },
  {
    slug: "it/graphql-formatter",
    inputs: { input: "{a{b}}" },
    clicks: ["doMinify()"],
    expect: ["{ a{ b}}"],
    ref: "压缩形态（保留花括号间单空格、去掉换行）；默认示例的 query 文本不同，不命中。",
  },
  {
    slug: "it/html-nesting-checker",
    inputs: { html: "<div><p>a</div>" },
    clicks: ["check()"],
    expect: ["发现 1 个问题"],
    ref: "`<p>` 未被显式闭合即被 `</div>` 关闭 ⇒ 报 1 个问题并定位行号；默认示例无嵌套错误，不命中。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "AB" },
    clicks: ["convert()"],
    expect: ["Alpha Bravo"],
    ref: "字母逐个翻译为 NATO  Phonetic 单词（A→Alpha、B→Bravo），非原文回显；默认示例字母不同。",
  },
  {
    slug: "it/uuencode",
    inputs: { input: "ABC" },
    clicks: ["enc()"],
    expect: ["begin 644 file.txt #04)# ` end"],
    ref: "uuencode 头（begin 644 文件名）＋ 编码体 ＋ 结束行 end，随输入体变化；默认语料长度不同。",
  },
  {
    slug: "it/css-minify",
    inputs: { src: "a{color:red}" },
    expect: ["压缩后 0% 节省"],
    ref: "输入本已是最简形态 ⇒ 压缩字节数与原始相同、节省 0%，验证压缩率统计不虚报；默认示例压缩前后不同，不命中。",
  },
  {
    slug: "it/js-minify",
    inputs: { src: "var a=1;" },
    expect: ["压缩后 0% 节省"],
    ref: "无空白可去的最短输入 ⇒ 节省 0%，校验「压缩后字节 ≤ 原始字节」的统计口径；默认示例不命中。",
  },
  {
    slug: "it/js-obfuscator",
    inputs: { inputCode: "var a=1;" },
    clicks: ["obfuscate()"],
    expect: ["+0%"],
    ref: "混淆前后字节数相同 ⇒ 增幅 0%；默认示例代码更长，不命中。",
  },
  {
    slug: "it/regex-common",
    inputs: { txt: "abc", cat: "email", limit: "10" },
    clicks: ["calcTool()"],
    expect: ["无匹配"],
    ref: "`abc` 不匹配邮箱正则 ⇒ 匹配数 0 且结果区落「无匹配」；默认示例文本可命中，结论相反。",
  },
  {
    slug: "it/vector-magnitude",
    inputs: {},
    clicks: ["document.getElementById('v0').value=6;document.getElementById('v1').value=8;document.getElementById('v2').value=0;calculate()"],
    expect: ["|v| = 10"],
    ref: "√(6²+8²)=10；输入框由 `build()` 运行期渲染（HTML 无字面 id）⇒ 必须 clicks 内按 id 赋值。默认值为 (3,4) ⇒ 5，不命中。",
  },
  {
    slug: "it/vector-dot-product",
    inputs: {},
    clicks: ["document.getElementById('a0').value=1;document.getElementById('a1').value=2;document.getElementById('a2').value=3;document.getElementById('b0').value=4;document.getElementById('b1').value=5;document.getElementById('b2').value=6;calculate()"],
    expect: ["A · B = 14"],
    ref: "dim 默认 2D：A=(1,2)、B=(4,5) ⇒ 1×4+2×5=14。默认 A=(1,0)、B=(0,1) ⇒ 0，不命中。",
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "1", a1: "0", a2: "0", b0: "0", b1: "0", b2: "1" },
    clicks: ["calculate()"],
    expect: ["A × B = (0, -1, 0)"],
    ref: "i×k = −j ⇒ (0,−1,0)。默认示例 (1,0,0)×(0,1,0)=(0,0,1) 结论不同，不可用其做锚。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.01", likelihood: "0.9", falsePositive: "0.05" },
    clicks: ["calculate()"],
    expect: ["P(H₁ | E) = 0.154 (15.38%)"],
    ref: "后验 = 0.9×0.01 / (0.9×0.01 + 0.05×0.99) = 0.009/0.059 ≈ 0.1538；默认示例先验不同，不命中。",
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "2", x: "1" },
    clicks: ["calculate()"],
    expect: ["P(X ≤ 1) = 0.865"],
    ref: "指数分布 CDF F(1)=1−e⁻²=0.8647 ⇒ 0.865；默认参数不同，不命中。",
  },
  {
    slug: "it/barcode-ean",
    inputs: { data: "590123412345" },
    clicks: ["generate()"],
    expect: ["5901234123457"],
    ref: "EAN-12 补一位校验位（590123412345→7）⇒ 完整 13 位码；默认示例码不同。",
  },
  {
    slug: "it/hash-multi",
    inputs: {},
    clicks: ["document.getElementById('al_md5').checked=true;document.getElementById('input').value='abc';calc()"],
    expect: ["MD5 900150983cd24fb0d6963f7d28e17f72"],
    ref: "MD5(`abc`) = 900150983cd24fb0d6963f7d28e17f72（RFC 1321 标准值）。算法是 checkbox 驱动的 ⇒ 桩内恒未勾，必须 clicks 内显式置位再 `calc()`。",
  },
  {
    slug: "it/wifi-qr",
    inputs: { ssid: "Net", pass: "pw" },
    clicks: ["generate()"],
    expect: ["WIFI:T:WPA;S:Net;P:pw;H:false;;"],
    ref: "Wi-Fi QR 的 TYPE/S/P/H 字段拼接（WPA、隐藏网络 false、末尾双分号）；默认示例 SSID/密码不同。",
  },
  {
    slug: "it/caa-record-generator",
    inputs: {},
    clicks: ["document.getElementById('ca_lets').checked=true;document.getElementById('domain').value='a.test';gen()"],
    expect: ['a.test CAA 0 issue "letsencrypt.org"'],
    ref: "勾选 letsencrypt 授权者 + 注入域名 ⇒ 输出标准 CAA 记录行（flags 0、issue 指令）。算法 checkbox 需 clicks 置位。",
  },
  {
    slug: "it/api-sign-generator",
    inputs: { secret: "s", params: "a=1", algo: "md5" },
    clicks: ["runSign()"],
    expect: ["签名结果： 14c37dbbd13c5d12d5ef41a29a5c6fb1"],
    ref: "按 `参数串 + &secret=` 拼接待签串后做 HMAC-MD5 ⇒ 固定 32 位十六进制签名；默认参数组合产出不同密文。",
  },
  {
    slug: "it/http-status",
    inputs: { search: "zzz" },
    expect: ["No matching status code."],
    ref: "反向锚：不存在的状态码 ⇒ 列表区落英文空态提示（默认示例列表非空，必不命中）。",
  },
  {
    slug: "it/xxtea",
    inputs: { input: "ABC", key: "KY" },
    clicks: ["encrypt()"],
    expect: ["MaTt9vgiYH8="],
    ref: "XXTEA 加密后按 Base64 输出（固定密钥下结果确定）；默认示例明文/密钥不同，不命中。",
  },
  {
    slug: "it/mac-lookup",
    inputs: { macInput: "00:1A:2B:3C:4D:5E" },
    expect: ["点分： 001A.2B3C.4D5E"],
    ref: "MAC 的三种规范书写（冒号/连字符/点分）＋ OUI 与 NIC 拆分随输入变化；默认示例地址不同。",
  },
  {
    slug: "it/phone-parser",
    inputs: { phone: "+8613800138000", cc: "86" },
    expect: ["国内格式（按位分组）：8 6138 0013 8000"],
    ref: "E.164 与国内按位分组格式随号码变化；默认号码分组不同，不命中。",
  },
  {
    slug: "it/country-code-lookup",
    inputs: { input: "CN" },
    expect: ["ISO 3： CHN"],
    ref: "ISO 3166-1 alpha-2 → alpha-3/区号/首都/货币映射（CN→CHN→+86→北京→CNY）。默认示例代码不同。",
  },
  {
    slug: "it/language-code-lookup",
    inputs: { input: "zh" },
    expect: ["ISO 639-3： zho"],
    ref: "ISO 639-1 → 639-3/语言名/语系/书写系统映射（zh→zho→Chinese→汉藏语系→Hans/Hant）。默认示例语言不同。",
  },
  {
    slug: "it/sms-qr",
    inputs: { phone: "13800138000", msg: "hi" },
    clicks: ["generate()"],
    expect: ["sms:13800138000?body=hi"],
    ref: "SMS 二维码内容格式 `sms:号码?body=短信`；默认号码/短信不同。",
  },
  {
    slug: "it/email-qr",
    inputs: { to: "a@b.com", subject: "S", body: "B" },
    clicks: ["generate()"],
    expect: ["mailto:a%40b.com?subject=S&amp;body=B"],
    ref: "mailto URI + 百分号编码收件箱（@→%40）＋ subject/body 查询参数；默认示例不同。注意产物区为 HTML 上下文，锚须写 `&amp;`。",
  },
  {
    slug: "it/location-qr",
    inputs: { lat: "31.2", lng: "121.4", label: "P" },
    clicks: ["generate()"],
    expect: ["geo:31.2,121.4?q=P"],
    ref: "Geo URI（纬度,经度 + 标签查询参数）；默认坐标/标签不同。",
  },
  {
    slug: "it/sitemap-generator",
    inputs: { urls: "https://a.test\nhttps://b.test" },
    clicks: ["calcTool()"],
    expect: ["sitemap.xml 2 URL 数"],
    ref: "URL 条数统计随注入条数变化（默认示例条数不同 ⇒ 已排除同值巧合）。",
  },
  {
    slug: "it/phone-screen-sizes",
    inputs: { diag: "5", resw: "1080", resh: "1920" },
    clicks: ["calcTool()"],
    expect: ["2203 px 对角线像素"],
    ref: "√(1080²+1920²)=2202.9 ⇒ 2203 px；默认机型分辨率/尺寸组合不命中。",
  },
  {
    slug: "it/http-methods",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：搜索不存在的方法 ⇒ 过滤结果计数归零。默认列表非空 ⇒ 默认态必不命中。",
  },
  {
    slug: "it/http-headers",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：搜索不存在的头名 ⇒ 计数为 0；默认列表非空。",
  },
  {
    slug: "it/http-cache",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：缓存头速查过滤空结果计数归零；默认列表非空。",
  },
  {
    slug: "it/http-cookies",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Cookie 速查过滤空结果计数归零；默认列表非空。",
  },
  {
    slug: "it/http-response-headers",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：响应头速查过滤空结果计数归零；默认列表非空。",
  },
  {
    slug: "it/affine-cipher",
    inputs: { input: "ABCD", a: "3", b: "1" },
    clicks: ["dec()"],
    expect: ["RAJS"],
    ref: "解密分支 `dec()` 走逆变换 a⁻¹(c−b)=9(c−1) mod 26：A→R、B→A、C→J、D⇒S（独立复算得 RAJS）。默认 a=5/b=8（产物 OJEZ），注入值必须避开默认。",
  },
  {
    slug: "it/basic-auth-generator",
    inputs: { f_user: "alice", f_pass: "pw123" },
    expect: ["Authorization: Basic YWxpY2U6cHcxMjM="],
    ref: "Basic 认证头 = `Basic ` + Base64(`alice:pw123`) = YWxpY2U6cHcxMjM=；裸 input event 即渲染，无需 clicks。默认示例用户名/口令不同。",
  },
  {
    slug: "it/date-duration",
    inputs: { d1: "2024-01-01", d2: "2024-03-15", inc: "1" },
    clicks: ["calcTool()"],
    expect: ["相差 74 天"],
    ref: "2024 闰年 1 月 31 + 2 月 29 + 15 − 1 = 74 天（页面按「不含结束当天」口径）。默认起止日不命中。",
  },
  {
    slug: "it/country-flag",
    inputs: { search: "zzz" },
    expect: ["共 0 个国家/地区"],
    ref: "反向锚：灌入不存在的国家名 ⇒ 计数归零；默认列表含上百个国家，默认态必不命中。与 http-* 五页同族。",
  },
  {
    slug: "it/calc-1",
    inputs: { sizeInput: "512", unitSelect: "KB" },
    expect: ["512,000 B"],
    ref: "512 KB = 512,000 B（十进制口径）；`unitSelect` 显式注入 KB 后才落该行。默认 1024 B ⇒ 1024 B，不命中。",
  },
  {
    slug: "it/calc-3",
    inputs: { hexInput: "#1E90FF" },
    expect: ["rgb(30, 144, 255)"],
    ref: "#1E90FF → rgb(30,144,255) → hsl(210,100%,56%)；默认色值不同形。裸 input event 即渲染。",
  },
  {
    slug: "it/calc-4",
    inputs: { pxInput: "48" },
    expect: ["font-size: 48px;"],
    ref: "48px 换算推出 em/rem/pt/% 四行（3 / 3 / 36pt / 300%）；锚取注入值对应的 px 行写法。默认 16px 不命中。",
  },
  {
    slug: "it/calc-5",
    inputs: { textInput: "hello world foo" },
    expect: ["15 字符 / 15 字节"],
    ref: "11 字符文本 + 3 空格 + 2 词 ⇒ 总长 15；统计区随输入重算（默认示例文本不同）。",
  },
  {
    slug: "it/calc-7",
    inputs: { jsonInput: '{"a":{"b":[1,2,3]}}', pathInput: "a.b" },
    expect: ["路径： $.a.b"],
    ref: "JSONPath 求值：`$.a.b` 命中数组 ⇒ 输出 `[ 1, 2, 3 ]`。**不可写 clicks 里的 `loadSample()`** —— 那会渲染默认样例（$.toolbox.name），默认态同命中 ⇒ 逃生项。",
  },
  {
    slug: "it/convert-11",
    inputs: { val: "255", from: "dec", to: "bin" },
    clicks: ["calc()"],
    expect: ["00000000.00000000.00000000.11111111"],
    ref: "十进制 255 → 点分二进制补齐 8 位×4 ⇒ 11111111；默认入参是 IP 地址 192.168.1.1（dot→bin），不命中。",
  },
  {
    slug: "it/playfair-cipher",
    inputs: { input: "HELLO", key: "KEY" },
    expect: ["DBNVMI"],
    ref: "Playfair 加密：`HELLO` 成对切分为 HE/LL/OX 后在 5×5 矩阵（KEY 去重后填充）中按行/列规则替换 ⇒ DBNVMI。默认示例明文/密钥不同，产物不命中。",
  },
  {
    slug: "it/vigenere-visualizer",
    inputs: { input: "ABC", key: "KEY" },
    expect: ["KFA"],
    ref: "维吉尼亚加密：A+K、B+E、C+Y ⇒ KFA（逐字符位移）。默认明文/密钥组合产物不同。",
  },
  {
    slug: "it/html-escape",
    inputs: { batchInput: "<b>x</b>" },
    clicks: ["convert()"],
    expect: ["&lt;b&gt;x&lt;/b&gt;"],
    ref: "批量区把 `<b>x</b>` 实体化为 `&lt;b&gt;x&lt;/b&gt;`（结果区读的是 batchResult，主 result 在桩内仍为默认示例文本，勿锚它）。",
  },
  {
    slug: "it/css-properties",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 个属性"],
    ref: "反向锚：CSS 属性速查灌入不存在的关键词 ⇒ 计数归零（默认态列表上百条，必不命中）。与 http-* / country-flag 同族。",
  },
  {
    slug: "it/cpp-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：C++ 速查过滤无结果计数归零；默认列表非空。",
  },
  {
    slug: "it/docker-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Docker 速查过滤无结果计数归零；默认列表非空。",
  },
  {
    slug: "it/hill-cipher",
    inputs: { input: "HELLO", key: "3,1,1,2" },
    clicks: ["enc()"],
    expect: ["ZPSHNI"],
    ref: "独立复算：密钥矩阵 [[3,1],[1,2]]（det=5，与 26 互素）作用于补齐后的 HELLOX ⇒ 逐对 (7,4)(11,11)(14,23) → ZP / SH / NI。明文与密钥均无 oninput ⇒ 必须 clicks `enc()`。",
  },
  {
    slug: "it/matrix-transpose",
    inputs: { rows: "1", cols: "2", a0: "7", a1: "3" },
    clicks: ["calculate()"],
    expect: ["转置矩阵 Aᵀ （2×1）： 7 3"],
    ref: "独立复算：1×2 矩阵 [7 3] 转置为 2×1 [[7],[3]]。同样必须注入运行期格子 `a0/a1`（rows/cols 只决定格子数量）。",
  },
  {
    slug: "it/invite-code-generator",
    inputs: { count: "3", len: "8" },
    clicks: [
      "document.getElementById('upper').checked=true;document.getElementById('num').checked=true;document.getElementById('prefix').checked=true;document.getElementById('prefixVal').value='ZZ';generate()",
    ],
    expect: ["ZZ-"],
    ref: "随机码只锚前缀拼接：勾选大写+数字+前缀后每条形如 `ZZ-L1ERDGP5`。四个开关在桩内恒未勾（`inputs` 写 checked 不生效）⇒ 必须在 clicks 里逐个置 true，否则 chars 为空直接 alert 返回、与默认态零差异。默认态（无 clicks）不产生任何输出。",
  },
  {
    slug: "it/ipv6-ula",
    inputs: { cnt: "5" },
    clicks: ["calcTool()"],
    expect: ["生成的 IPv6 ULA（5 个）"],
    ref: "随机地址只锚计数：注入 cnt=5 ⇒ 条数字符串必为（5 个），默认 cnt=3 不命中。",
  },
  {
    slug: "it/mime-type",
    inputs: { search: "zzz" },
    expect: ["共 0 条"],
    ref: "反向锚：MIME 表搜索无命中计数归零；默认列表非空。",
  },
  {
    slug: "it/json-to-csv",
    inputs: { input: '[{"name":"Tom","age":3},{"name":"Ann","age":5}]' },
    clicks: ["toCSV()"],
    expect: ["已转换 2 行 × 2 列"],
    ref: "独立复算：两条 JSON 对象 ⇒ 表头 name,age + 2 行 ⇒ 2 行 × 2 列。转换走按钮 ⇒ 必须 clicks。",
  },
  {
    slug: "it/json-to-yaml",
    inputs: { input: '{"a":1}' },
    clicks: ["doYaml()"],
    expect: ["--- a: 1"],
    ref: "独立复算：`---` 文档分隔 + 一级键 `a: 1`。**不能用 `loadSample()`** —— 那会渲染默认样例，默认态同命中 ⇒ 逃生项。",
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "XYZ", sep: "-" },
    clicks: ["enc()"],
    expect: ["24-25-26"],
    ref: "独立复算：A=1/Z=26 ⇒ `24-25-26`。**注入必须避开默认文本 `HELLO WORLD`** —— 它的编码结果以 `23-15-18-12-4` 结尾，与本例锚成子串关系，默认态会命中 ⇒ 逃生项。",
  },
  {
    slug: "it/baudot-code",
    inputs: { input: "AB1" },
    clicks: ["enc()"],
    expect: ["00011 11001 11011 10111"],
    ref: "独立复算：查码表 A=00011、B=11001、数字 1=10111 ⇒ 五个位组以空格连接。表体（32 行码表）恒在默认态出现，锚只取产物行。",
  },
  {
    slug: "it/ascii-table",
    inputs: { search: "zzz" },
    expect: ["No matching entries."],
    ref: "反向锚：ASCII 速查搜索无命中 ⇒ 空态提示；默认列表非空。",
  },
  {
    slug: "it/ascii-tree-generator",
    inputs: { paths: "src/\na.js\nb.js\nlib/util.js" },
    clicks: ["build()"],
    expect: ["已生成 5 行目录树（4 个路径）"],
    ref: "独立复算：4 条路径按**换行**切分（非逗号）⇒ 5 行树、4 个路径。textarea 无 oninput ⇒ 必须 clicks `build()`。",
  },
  {
    slug: "it/area-code-lookup",
    inputs: { input: "212" },
    expect: ["New York (Manhattan)"],
    ref: "独立复算：NANP 区号库查 212 ⇒ New York (Manhattan)。库只覆盖北美编号计划，`021` 等中国区号查无 ⇒ 默认态不命中。",
  },
  {
    slug: "it/csv-validator",
    inputs: { src: "name,age\nTom,3", sep: "," },
    clicks: ["calcTool()"],
    expect: ["2 标准列数"],
    ref: "独立复算：两行 CSV（`name,age` / `Tom,3`）⇒ 标准列数 2、问题数 0。默认示例是 6 行中文表，不命中本锚。",
  },
  {
    slug: "it/csv-to-json",
    inputs: { csvInput: "name,age\nTom,3" },
    expect: ['[{"column1":"name","column2":"age"}'],
    ref: "走「无表头」分支（桩内 checkbox 恒未勾，与真实用户未勾表头一致）⇒ 表头占位列名 column1/column2，产物是整条 JSON 数组。用整条数组做锚避免撞默认样例。",
  },
  {
    slug: "it/bluetooth-version",
    inputs: { v: "4.0", v2: "5.0" },
    clicks: ["calcTool()"],
    expect: ["Bluetooth 4.0 vs 5.0 版本对比"],
    ref: "独立复算：注入两侧版本 4.0 / 5.0 ⇒ 标题必为「Bluetooth 4.0 vs 5.0 版本对比」。默认态两侧同版（5.0/5.2 等）不命中。",
  },
  {
    slug: "it/emoji-cheatsheet",
    inputs: { search: "zzz" },
    expect: ["共 0 个 emoji"],
    ref: "反向锚：表情速查搜索无命中 ⇒ 空态计数归零，页面同时给出「未找到匹配的 emoji」。默认列表非空。",
  },
  {
    slug: "it/env-generator",
    inputs: { keyInput: "FOO", importText: "BAR=baz" },
    clicks: ["addVariable()"],
    expect: ["FOO 字符串"],
    ref: "独立复算：手动新增键 `FOO` ⇒ 变量表出现一行 `# Key ↕ Value ↕ Type ↕ 操作 / 1 FOO 字符串`。表格走 clicks 驱动，默认态无此行。",
  },
  {
    slug: "it/line-ending-converter",
    inputs: { leInput: "x\r\n\r\ny\n" },
    clicks: ["calcTool()"],
    expect: ["总换行 3"],
    ref: "独立复算：2 个 CRLF + 1 个 LF ⇒ 统计行 `CRLF 2 / LF 1 / CR 0 / 总换行 3`。**注入值必须避开默认的两行 CRLF**（`第一行\\r\\n第二行\\r\\n第三行` 也总换行 2，注入同值即逃生项，本例已踩并改 3）；锚也不能写 `LF 1`（会被 `CRLF 1` 误伤）。",
  },
  {
    slug: "it/js-formatter",
    inputs: { input: "const a=1" },
    clicks: ["doBeautify()"],
    expect: ["const a =1"],
    ref: "独立复算：美化 `const a=1` ⇒ `const a =1`（只在 `=` 两侧补空格）。页面 d 在 harness 内不执行/beautify 依赖 tokenize ⇒ 走 clicks。",
  },
  {
    slug: "it/mysql-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：MySQL 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/url-parser",
    inputs: { urlInput: "https://a.io/p?x=1&y=2" },
    clicks: ["buildUrl()"],
    expect: ["域名 复制 a.io"],
    ref: "独立复算：解析结果逐行给出「协议/源/域名/端口/主机/路径/查询字符串/哈希/查询参数」，锚取域名行（`a.io`）。默认示例 URL 不同，不命中。",
  },
  {
    slug: "it/redis-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Redis 速查搜索无命中 ⇒ 计数归零；默认列表非空。与 `mysql-cheatsheet` 同族。",
  },
  {
    slug: "it/rest-api-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：REST API 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/postgresql-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：PostgreSQL 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/unicode-lookup",
    inputs: { search: "★" },
    clicks: ["showDetail()"],
    expect: ["U+2605"],
    ref: "独立复算：U+2605 就是 `★`（BLACK STAR），查表页把字符与其码点并列渲染。`showDetail()` 在桩内会因「无选中项」抛 `Invalid code point NaN`，但网格（`grid`）已由搜索框的 input 事件更新 ⇒ 不依赖该异常路径。默认列表里没有该条目。",
  },
  {
    slug: "it/vim-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Vim 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/robots-txt-generator",
    inputs: { sitemap: "https://a.io/sitemap.xml" },
    clicks: ["addRule()", "render()"],
    expect: ["Sitemap: https://a.io/sitemap.xml"],
    ref: "独立复算：填 Sitemap 后 `render()` 把该行并进预览（`addRule()` 先把默认规则行补进来，故预览里同时含默认 UA/Disallow 行）。锚取注入的 sitemap 行，默认态不含。",
  },
  {
    slug: "it/go-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Go 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/linux-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Linux 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/sqlite-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：SQLite 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/text-to-hex",
    inputs: { input: "Hi!" },
    clicks: ["convert()"],
    expect: ["48 69 21"],
    ref: "独立复算：ASCII 表手算 H=0x48、i=0x69、!=0x21，默认分隔符为空格 ⇒ `48 69 21`。默认样例是 `Hello` ⇒ 默认态不含该串。",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "2024" },
    clicks: ["calcTool()"],
    expect: ["MMXXIV"],
    ref: "独立复算：2024 = 1000(M) + 1000(M) + 10(X) + 10(X) + 5(V) + 1(I) ⇒ MMXXIV。默认示例是另一个数字，默认态不含。",
  },
  {
    slug: "it/java-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Java 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/typescript-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：TypeScript 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/python-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Python 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/timestamp-converter",
    inputs: { calcStartDate: "2020-01-01", calcAmount: "3", calcUnit: "year", calcOp: "add" },
    clicks: ["calculateDate()"],
    expect: ["计算结果: 2023-01-01 00:00:00"],
    ref: "独立复算：2020-01-01 + 3 年 = 2023-01-01。只锚本地日期串，**不锚时间戳**（页面时间戳随运行时区变化，非确定性）。默认态的样例日期是 2024-06-15。",
  },
  {
    slug: "it/sql-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：SQL 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/php-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：PHP 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/nginx-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Nginx 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/url-encode",
    inputs: { input: "a b&c" },
    clicks: ["encodeUrl()"],
    expect: ["a%20b%26c"],
    ref: "独立复算：`encodeURIComponent('a b&c')` ⇒ 空格→`%20`、`&`→`%26` ⇒ `a%20b%26c`。默认样例是 URL，默认态不含该串。",
  },
  {
    slug: "it/csharp-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：C# 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/ruby-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Ruby 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/rust-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Rust 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/css-minifier",
    inputs: { input: "/*c*/a{color : red}" },
    clicks: ["minify()"],
    expect: ["a{color:red}"],
    ref: "独立复算：去掉注释 `/*c*/` 与冒号后空格 ⇒ `a{color:red}`。默认示例带缩进/换行，默认态不含该串。",
  },
  {
    slug: "it/msisdn-lookup",
    inputs: { input: "112" },
    expect: ["E.164 格式： +112"],
    ref: "独立复算：`112` 的国家代码为 `1`（美国/加拿大），国内号码 `12`，E.164 归一化为 `+112`。默认样例是另一个号码。",
  },
  {
    slug: "it/emacs-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Emacs 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/kubernetes-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：Kubernetes 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/mongodb-cheatsheet",
    inputs: { searchInput: "zzz" },
    expect: ["共 0 项"],
    ref: "反向锚：MongoDB 速查搜索无命中 ⇒ 计数归零；默认列表非空。",
  },
  {
    slug: "it/punycode",
    inputs: { input: "bcher" },
    clicks: ["enc()"],
    expect: ["bcher-"],
    ref: "独立复算：纯 ASCII 输入的标准 punycode 编码 = 基本码点原样输出 + `-` 分隔位 + 空扩展段 ⇒ `bcher-`（RFC 3492 §6.1 的同形规则）。非 ASCII 输入（`bücher`）在桩内会因 `str is not iterable` 抛错、回落同形态，故只用纯 ASCII 入参。",
  },
  {
    slug: "it/html-entity-encoder",
    inputs: { encodeInput: "<a>&" },
    clicks: ["encode()"],
    expect: ["&lt;a&gt;&amp;"],
    ref: "独立复算：`<`→`&lt;`、`>`→`&gt;`、`&`→`&amp;` ⇒ `&lt;a&gt;&amp;`。默认态的实体对照表里有 `&amp; &lt;` 等零散片段，但没有这条连续串。",
  },
  {
    slug: "it/matrix-multiplier",
    inputs: { ar: "2", ac: "2", br: "2", bc: "2" },
    clicks: [
      "document.getElementById('a0').value=1;document.getElementById('a1').value=2;document.getElementById('a2').value=3;document.getElementById('a3').value=4;document.getElementById('b0').value=5;document.getElementById('b1').value=6;document.getElementById('b2').value=7;document.getElementById('b3').value=1;build();calculate()",
    ],
    expect: ["结果 C = A × B （2×2）： 19 8 43 22"],
    ref: "独立复算：A=[[1,2],[3,4]]，B=[[5,6],[7,1]] ⇒ C[1][1]=1×5+2×7=19、C[1][2]=1×6+2×1=8、C[2][1]=3×5+4×7=43、C[2][2]=3×6+4×1=22。单元格 `a0..a3`／`b0..b3` 是运行期渲染（HTML 无字面 id）⇒ 必须 clicks 内按 id 赋值再 `build();calculate()`。",
  },
  {
    slug: "it/calc-subnet",
    inputs: { ip: "10.0.0.7", cidr: "28" },
    clicks: ["calc()"],
    expect: ["10.0.0.0 网络地址"],
    ref: "独立复算：10.0.0.7/28 ⇒ 网络 10.0.0.0、广播 10.0.0.15、/28、可用主机 14。注意该页是「值在前、标签在后」的排布（`10.0.0.0 网络地址`），写反了会注入态 FAIL。",
  },
  {
    slug: "it/qrcode",
    inputs: { contentTemplate: "TOOLBOX-HELLO-2026" },
    clicks: ["applyTemplate()"],
    expect: ["TOOLBOX-HELLO-2026"],
    ref: "二维码矩阵在桩内画不出来（`qrcode is not defined`），但**内容串本身先已写进结果区** ⇒ 直接锚内容串。用长串避免「超短串命中面过大」。",
  },
  {
    slug: "it/unit-converter-advanced",
    inputs: { cat: "length", from: "m", val: "100" },
    clicks: ["calcTool()"],
    expect: ["0.1 km 10000 cm 100000 mm"],
    ref: "独立复算：100 m = 0.1 km = 10000 cm = 100000 mm = 0.062137 mi = 109.36133 yd = 328.08399 ft（量纲换算，逐项可手算）。默认示例换算的不是 `m`。",
  },
  {
    slug: "it/text-qr",
    inputs: { text: "TOOLBOX-QR-2026" },
    clicks: ["generate()"],
    expect: ["TOOLBOX-QR-2026"],
    ref: "二维码矩阵在桩内画不出来（`renderQR … leng`），但内容串先已写进结果区 ⇒ 直接锚内容串（与 `it/qrcode` 同族）。",
  },
  {
    slug: "it/barcode-upc",
    inputs: { data: "12345678905" },
    clicks: ["generate()"],
    expect: ["123456789050"],
    ref: "独立复算：UPC-A 校验位 p = (10 − (3×(d1+d3+d5+d7+d9+d11) + (d2+d4+d6+d8+d10)) mod 10) mod 10；12345678905 ⇒ 3×(1+3+5+7+9+0)=75、2+4+6+8+5=25、和 100 ⇒ p=0。默认样例是 03600029145（补出 …2），默认态不含本串。",
  },
  {
    slug: "it/matrix-determinant",
    inputs: { size: "2" },
    clicks: ["document.getElementById('a0').value=3;document.getElementById('a1').value=2;document.getElementById('a2').value=5;document.getElementById('a3').value=7;calculate()"],
    expect: ["= 21 − 10 = 11"],
    ref: "独立复算：|A| = a·d − b·c = 3×7 − 2×5 = 21 − 10 = 11。矩阵格子 a0..a3 是运行期渲染（HTML 无字面 id）⇒ clicks 里按 id 赋值再 calculate()。默认 2×2 矩阵不是本组，默认态不含该串。",
  },
  {
    slug: "it/matrix-inverter",
    inputs: { size: "2" },
    clicks: ["document.getElementById('a0').value=4;document.getElementById('a1').value=7;document.getElementById('a2').value=2;document.getElementById('a3').value=6;calculate()"],
    expect: ["逆矩阵 A⁻¹： 0.6 -0.7 -0.2 0.4"],
    ref: "独立复算：A=[[4,7],[2,6]]，det=4×6−7×2=10 ⇒ A⁻¹=(1/10)·[[6,−7],[−2,4]]=[[0.6,−0.7],[−0.2,0.4]]，且 A×A⁻¹=I。同 matrix-determinant 的 clicks 模板。",
  },
  {
    slug: "it/a1z26-cipher",
    inputs: { input: "AB" },
    clicks: ["enc()"],
    expect: ["1-2"],
    ref: "独立复算：A=1、B=2，默认分隔符为 `-` ⇒ `1-2`。产物是纯数字、不含输入字母 ⇒ 天然非回显。默认样例是单词（多位字母），默认态不含本串。",
  },
  {
    slug: "it/affine-cipher",
    inputs: { input: "ABCD", a: "3", b: "5" },
    clicks: ["enc()"],
    expect: ["FILO"],
    ref: "独立复算：仿射加密 E(x)=(a·x+b) mod 26，a=3、b=5 ⇒ A(0)→5=F、B(1)→8=I、C(2)→11=L、D(3)→14=O ⇒ `FILO`。dump 期 `gcd` 报栈溢出（页面在算逆元）但不影响产物。默认参数是另一组 a/b。",
  },
  {
    slug: "it/bacon-cipher",
    inputs: { input: "AB", mode: "enc" },
    expect: ["0000000001"],
    ref: "独立复算：Bacon 密码 A=`aaaaa`(00000)、B=`aaaab`(00001) ⇒ `0000000001`。**必须显式把 mode 设为 enc**（默认 mode 是解码方向，不带则产物不同）。产物是纯 0/1、不含输入字母 ⇒ 非回显。",
  },
  {
    slug: "it/atbash-cipher",
    inputs: { input: "ABC" },
    clicks: ["transform()"],
    expect: ["ZYX"],
    ref: "独立复算：Atbash 把字母表倒序映射（A↔Z、B↔Y、C↔X）⇒ `ZYX`。产物不含输入字母 ⇒ 非回显；默认样例是单词，默认态不含本串。",
  },
  {
    slug: "it/ascii-tree-generator",
    inputs: { paths: "a/b.txt\na/c/d.txt" },
    clicks: ["build()"],
    expect: ["a/ ├── b.txt └── c/ └── d.txt"],
    ref: "独立复算：两条路径共享顶层 `a/` ⇒ `b.txt` 是 `a` 的末项用 `└──`、其父层缩进两格；`a/c/d.txt` 的 `c/` 同样末级 ⇒ 末条为 `└── d.txt`。产物是「结构符号 + 文件名」，非裸输入回显。",
  },
  {
    slug: "it/barcode-ean",
    inputs: { data: "400638133393" },
    clicks: ["generate()"],
    expect: ["4006381333931"],
    ref: "独立复算：EAN-13 校验位 = (10 − Σ(位置1,3,5…×1 + 位置2,4,6…×3) mod 10) mod 10；400638133393 ⇒ 4+0+0+18+3+24+1+9+3+9+9+9=89 ⇒ 校验位 1。默认样例是 590123412345（补出 …7），默认态不含本串。",
  },
  {
    slug: "it/barcode-ean",
    inputs: { data: "123456789012" },
    clicks: ["generate()"],
    expect: ["1234567890128"],
    ref: "独立复算：同上口径，123456789012 ⇒ 4+0+6+6+3+24+1+9+3+9+9+9=83 ⇒ 校验位 8。用与默认样例不同的号码，确保双态可辨。",
  },
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", b: "10", op: "AND" },
    clicks: ["calc()"],
    expect: ["结果： 8"],
    ref: "独立复算：12 = 0b1100、10 = 0b1010 ⇒ 按位与 = 0b1000 = 8。注意运算符 select 的 option value 是大写 `AND`（传 `&` 会被页面忽略，产出恒 0）。",
  },
  {
    slug: "it/caesar-cipher",
    inputs: { input: "ABC", shift: "3" },
    clicks: ["process()"],
    expect: ["DEF"],
    ref: "独立复算：凯撒位移 +3 ⇒ A→D、B→E、C→F ⇒ `DEF`。默认样例文本不是本串。",
  },
  {
    slug: "it/binary-to-text",
    inputs: { input: "01000001" },
    clicks: ["convert()"],
    expect: ["A"],
    ref: "独立复算：8 位二进制 01000001 = 十进制 65 = ASCII 字符 `A`。产物是解码后的文本、不是输入回显；默认样例是另一段码。",
  },
  {
    slug: "it/bayes-theorem",
    inputs: { prior: "0.01", likelihood: "0.9", falsePositive: "0.1" },
    clicks: ["calculate()"],
    expect: ["0.009 + 0.099 = 0.108"],
    ref: "独立复算：P(E) = P(E|H₁)·P(H₁) + P(E|¬H₁)·P(¬H₁) = 0.9×0.01 + 0.1×0.99 = 0.009 + 0.099 = 0.108；后验 = 0.009/0.108 ≈ 0.083。锚在「中间展开式」上，逐项可手算。默认样例不是这组参数。",
  },
  {
    slug: "it/convert-11",
    inputs: { val: "10", from: "dec", to: "bin" },
    clicks: ["calc()"],
    expect: ["00000000.00000000.00000000.00001010"],
    ref: "独立复算：10₁₀ = 1010₂，按 4 字节补零成 32 位 ⇒ `00000000.00000000.00000000.00001010`。注意该页是**进制**转换（option value 只有 `dot`/`bin`/`dec`），传单位符号（m/cm）会被判为输入非法。",
  },
  {
    slug: "it/confidence-interval",
    inputs: { mean: "100", std: "15", n: "25", conf: "0.95", dist: "z" },
    clicks: ["calc()"],
    expect: ["边际误差 ME = 1.960 × 3.0000 = 5.8800"],
    ref: "独立复算：SE = s/√n = 15/√25 = 3；z(95%) = 1.960；ME = 1.960 × 3 = 5.8800 ⇒ 区间 [94.120, 105.880]。锚「中间展开式」，避开最终多位小数。默认样例参数不同。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "TOOLBOX" },
    clicks: ["calc()"],
    expect: ["CRC-8 0xc9"],
    ref: "独立复算：CRC-8（多项式 0x07、初值 0）逐字节移位 ⇒ 0xc9。默认样例恰是 `123456789`（标准校验值 0xf4）⇒ 默认态同样命中，故必须用别的输入串。",
  },
  {
    slug: "it/crc-calculator",
    inputs: { input: "abc" },
    clicks: ["calc()"],
    expect: ["CRC-8 0x5f"],
    ref: "独立复算：同上口径，`abc` 的 CRC-8 = 0x5f。同一页面换输入各写一条，两条 expect 互不相同。",
  },
  {
    slug: "it/decimal-encode",
    inputs: { input: "AB" },
    clicks: ["enc()"],
    expect: ["65 66"],
    ref: "独立复算：`A`=65、`B`=66，默认分隔符为空格 ⇒ `65 66`。产物是纯数字，不含输入字母 ⇒ 非回显。默认样例是另一段文本。",
  },
  {
    slug: "it/hex-encode",
    inputs: { input: "Hi" },
    clicks: ["enc()"],
    expect: ["4869"],
    ref: "独立复算：`H`=0x48、`i`=0x69 ⇒ `4869`。十六进制产物不含输入文本 ⇒ 非回显；默认样例不是本串。",
  },
  {
    slug: "it/hex-to-text",
    inputs: { input: "4869" },
    clicks: ["convert()"],
    expect: ["Hi"],
    ref: "独立复算：`48`=72=`H`、`69`=105=`i` ⇒ `Hi`。与上一条互逆，一并收下可覆盖双向路径。默认样例不是本串。",
  },
  {
    slug: "it/exponential-distribution",
    inputs: { lambda: "2", x: "1" },
    clicks: ["calculate()"],
    expect: ["1 − 0.135 = 0.865"],
    ref: "独立复算：指数分布 CDF F(x)=1−e^{−λx}，λ=2、x=1 ⇒ e^{−2}=0.135，F=1−0.135=0.865（PDF=2×0.135=0.271）。默认样例恰是 λ=0.5,x=2 ⇒ 默认态同样命中的那一组，故换参数。锚在中间展开式。",
  },
  {
    slug: "it/hypergeometric-distribution",
    inputs: { N: "10", K: "3", n: "4", k: "1" },
    clicks: ["calculate()"],
    expect: ["3 × 35 / 210 = 0.5"],
    ref: "独立复算：超几何概率 P = C(K,k)·C(N−K,n−k)/C(N,n) = C(3,1)·C(7,3)/C(10,4) = 3×35/210 = 105/210 = 0.5。锚在「中间展开式」（三个组合数逐个可算），默认样例参数不同。",
  },
  {
    slug: "it/html-nesting-checker",
    inputs: { html: "<div><p>x</div>" },
    clicks: ["check()"],
    expect: ["被隐式闭合"],
    ref: "独立复算：`<p>` 未闭合，遇到 `</div>` 时触发隐式闭合 ⇒ 报告第 1 行 `<p>` 被隐式闭合。产物是「检测结论 + 定位行」而非输入回显；默认样例不同。",
  },
  {
    slug: "it/json-minify",
    inputs: { input: '{ "a" : 1 }' },
    clicks: ["process()"],
    expect: ['{"a":1}'],
    ref: "独立复算：去掉 JSON 中多余空格 ⇒ `{\"a\":1}`（字节数 11 → 7，压缩率 36.4% 也可手算）。默认样例不是本串。",
  },
  {
    slug: "it/list-converter",
    inputs: { input: "a\nb", mode: "comma" },
    clicks: ["convert()"],
    expect: ["a, b"],
    ref: "独立复算：两行列表按逗号模式合并 ⇒ `a, b`。入参含换行（探针文件必须用 Python 的 `json.dumps` 生成，JSON 串内不允许字面换行）。",
  },
  {
    slug: "it/keyword-extractor",
    inputs: { inputText: "apple apple banana" },
    clicks: ["extractKeywords()"],
    expect: ["apple 2 banana 1"],
    ref: "独立复算：词频统计 ⇒ apple 出现 2 次、banana 1 次，产物排序为 `apple 2 banana 1`。统计类天然非回显；默认样例文本不同。",
  },
  {
    slug: "it/math-evaluator",
    inputs: { expr: "(1+2)*3" },
    clicks: ["calc()"],
    expect: ["结果： 9"],
    ref: "独立复算：先算括号 1+2=3，再乘 3 ⇒ 9。表达式求值类是最典型的可手算用例源（运算符优先级固定）。默认样例表达式不同。",
  },
  {
    slug: "it/nato-alphabet",
    inputs: { input: "AB" },
    clicks: ["convert()"],
    expect: ["Alpha Bravo"],
    ref: "独立复算：NATO 音标字母表 A=Alpha、B=Bravo ⇒ `Alpha Bravo`。产物不含输入的大写字母（是别名词）⇒ 非回显。",
  },
  {
    slug: "it/numeronym-generator",
    inputs: { input: "Global Positioning System" },
    clicks: ["generate()"],
    expect: ["G4l"],
    ref: "独立复算：numeronym 取首字母 + 中间字母数 + 末字母 ⇒ `G`+4个字母+`l` = G4l（Positioning⇒P9g、System⇒S4m）。产物含数字与缩略形态，非裸回显。默认样例不同。",
  },
  {
    slug: "it/morse",
    inputs: { input: "SOS" },
    clicks: ["convert()"],
    expect: ["... --- ..."],
    ref: "独立复算：S=`...`、O=`---` ⇒ `... --- ...`（点划间空格、字母间斜杠）。产物改写输入字符 ⇒ 非回显；默认样例不同。",
  },
  {
    slug: "it/normal-distribution",
    inputs: { mu: "0", sigma: "1", x0: "1" },
    clicks: ["calculate()"],
    expect: ["Z = (x−μ)/σ = (1−0)/1 = 1"],
    ref: "独立复算：标准正态 Z=(x−μ)/σ = (1−0)/1 = 1 ⇒ Φ(1)=0.841。锚在中间展开式；注意该页的 tab 控件 id 是 `mode0`（传 `mode` 无效）。默认样例参数不同。",
  },
  {
    slug: "it/margin-of-error",
    inputs: { N: "100", n: "50", p: "0.5", conf: "0.95" },
    clicks: ["calculate()"],
    expect: ["1.96 × 0.071 = ±0.139"],
    ref: "独立复算：SE = √[p̂(1−p̂)/n] = √(0.25/50) = √0.005 ≈ 0.071；E = z*×SE = 1.96×0.071 ≈ ±0.139（再乘有限总体修正 √(50/99) 得 ±0.098）。锚在中间展开式，默认样例参数不同。",
  },
  {
    slug: "it/octal-encode",
    inputs: { input: "Hi" },
    clicks: ["enc()"],
    expect: ["110 151"],
    ref: "独立复算：H=0o110=72、i=0o151=105，空格分隔。默认样例参数不同。",
  },
  {
    slug: "it/phone-parser",
    inputs: { cc: "1", phone: "4155550123" },
    clicks: ["calcTool()"],
    expect: ["+14155550123"],
    ref: "独立复算：去掉分隔符后拼接国家码 + 号码 = +14155550123（E.164）。默认样例号码不同。",
  },
  {
    slug: "it/phone-screen-sizes",
    inputs: { diag: "5", resw: "1080", resh: "1920" },
    clicks: ["calcTool()"],
    expect: ["441 PPI"],
    ref: "独立复算：对角线像素 √(1080²+1920²) = 2202.9，PPI = 2202.9/5 ≈ 440.6 ⇒ 441。默认样例参数不同。",
  },
  {
    slug: "it/poisson-distribution",
    inputs: { lambda: "3", k: "1" },
    clicks: ["calculate()"],
    expect: ["3 × 0.05 / 1 = 0.149"],
    ref: "独立复算：P(X=1) = λ¹e^(−λ)/1! = 3×0.049787/1 = 0.1494。锚在中间展开式；默认 λ=3,k=2 与注入同产物，故必须把 k 换成 1 才破题。",
  },
  {
    slug: "it/prime-checker",
    inputs: { n: "91" },
    clicks: ["calcTool()"],
    expect: ["91 是合数"],
    ref: "独立复算：91 = 7×13，是合数；产物另含最小质因数 7 与分解式。默认样例即 97（素数），换 91 才破题。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=b" },
    clicks: ["enc()"],
    expect: ["a=3db"],
    ref: "Quoted-Printable 编码：可打印 ASCII 原样保留，= 转义为 =3D（小写十六进制，因 upper 复选框默认未勾选）。默认样例不含本串。",
  },
  {
    slug: "it/quoted-printable",
    inputs: { input: "a=3db" },
    clicks: ["dec()"],
    expect: ["a=b"],
    ref: "Quoted-Printable 解码：把 =3d 还原为 = ⇒ a=b。与本页编码用例成对，双向均依赖被测点。",
  },
  {
    slug: "it/markdown-table-generator",
    inputs: { cols: "2", headerLine: "A,B", bodyLine: "1,2", rows: "1", align: "left" },
    clicks: ["renderPreview()"],
    expect: ["| 11 | 21 |"],
    ref: "读源码：parseRow 按逗号切格，行值 = 单元格值拼上行号（r+1，故第一行是 11/21），对齐标记 `:---` 对应 align=left。默认样例是 4 列 4 行，产物不同。",
  },
  {
    slug: "it/json-to-toml",
    inputs: { input: '{"a":1,"b":{"c":2}}' },
    clicks: ["doToml()"],
    expect: ["c = 2"],
    ref: "独立复算：嵌套对象转成表节 ⇒ TOML 为 `a = 1` / `[b]` / `c = 2`。锚在末行，默认样例字段不同。",
  },
  {
    slug: "it/css-formatter",
    inputs: { input: "a{color:red;font-size:12px}" },
    clicks: ["doBeautify()"],
    expect: ["a { color: red; font-size: 12px }"],
    ref: "格式化规则：选择器后补空格、声明按 `属性: 值;` 输出。默认样例（.btn 等）格式化后不含本串。",
  },
  {
    slug: "it/css-formatter",
    inputs: { input: "a { color: red; }" },
    clicks: ["doMinify()"],
    expect: ["a{color:red;}"],
    ref: "压缩规则：去选择器/大括号间的空白，保留声明末尾分号。默认样例压缩结果不含本串。",
  },
  {
    slug: "it/json-to-code",
    inputs: { input: '{"a":1,"b":"x"}', rootName: "MyRoot" },
    clicks: ["convert()"],
    expect: ["interface MyRoot {"],
    ref: "默认语言 TypeScript：对象数组/对象按字段类型生成 interface，类型映射 number/string/boolean。注意本页默认样例与本条入参同构 ⇒ 必须换 rootName 才破双态。",
  },
  {
    slug: "it/js-minifier",
    inputs: { input: "var a = 1;   // keep\nfunction f(){ return   a; }" },
    clicks: ["minify()"],
    expect: ["function f(){ return a; }"],
    ref: "压缩规则：折叠连续空白（注释复选框默认未勾选，故注释保留）。产物是输入经空白折叠后的改写，删掉输入即不完整。默认样例不含本串。",
  },
  {
    slug: "it/plist-parser",
    inputs: { input: '{"a":1}' },
    clicks: ["jsonToPlist()"],
    expect: ["a 1"],
    ref: "JSON → plist：字段名与标量值按序排列。默认样例键名不同。",
  },
  {
    slug: "it/ascii-art",
    inputs: { input: "AB" },
    clicks: ["generate()"],
    expect: ["8888 88888 88 88 88 88 888888 88888 88 88 88 88 88 88 88888"],
    ref: "字形点阵：每个字母按 5×5 粗体点阵展开成 `8` 序列（A 为 8888，B 为 88888…），字母被替换成点阵故非回显。默认样例文本不同。",
  },
  {
    slug: "it/box-shadow-generator",
    inputs: { x: "10", y: "20", blur: "5", spread: "2" },
    clicks: ["copyCss()"],
    expect: ["偏移 10px 20px · 模糊 5px · 扩散 2px"],
    ref: "产物摘要按「偏移/模糊/扩散」回显注入值；默认样例参数为 0。锚只覆盖偏移量部分，避免把 alpha 注入失效的缺陷值锁死进基线。",
  },
  {
    slug: "it/json-diff",
    inputs: { left: '{"a":1}', right: '{"a":2}' },
    clicks: ["doDiff()"],
    expect: ["修改 a 1 → 2"],
    ref: "路径级差异：键 a 由 1 改为 2 ⇒ 计数与路径列表各记一条「修改」。默认样例两版 JSON 不同。",
  },
  {
    slug: "it/jwt-parser",
    inputs: { jwtInput: "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoxfQ.sig" },
    clicks: ["parseJwt()"],
    expect: ['"alg": "RS256"'],
    ref: "独立构造：header=`{\"alg\":\"RS256\",\"typ\":\"JWT\"}`、payload=`{\"a\":1}` 做 base64url（去填充）后拼 `.sig`，解析区应还原出 RS256。默认样例是 HS256 ⇒ 必须换成 RS256 才破双态。",
  },
  {
    slug: "it/php-escape",
    inputs: { input: 'a"b', mode: "double" },
    clicks: ["esc()"],
    expect: ['a\\"b'],
    ref: "PHP 双引号字符串转义：把 `\"` 写成 `\\\"`。默认样例不含本串；single 模式（只加单引号、不转义）属输入回显，不收。",
  },
  {
    slug: "it/jwt-debugger",
    inputs: { "token-input": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoxfQ.sig" },
    clicks: ["decodeJwt()"],
    expect: ['{ "alg": "RS256", "typ": "JWT" }'],
    ref: "与 it/jwt-parser 同法构造测试向量：header/payload 的 base64url（去填充）+ `.sig`。锚在 header-json；默认样例是 HS256。",
  },
  {
    slug: "it/og-meta-tag-generator",
    inputs: { f_title: "T", f_desc: "D", f_url: "https://e.com/", f_site: "S", f_type: "website" },
    clicks: ["build()"],
    expect: ["已生成 9 条 meta 标签"],
    ref: "产物条数 = 非空字段数决定的 og/twitter/meta 组合数；本组入参产出 9 条。默认样例字段组合不同。",
  },
  {
    slug: "it/qr-decoder",
    inputs: { input: "HELLO" },
    clicks: ["generate()"],
    expect: ["识别到 1 种类型"],
    ref: "纯文本输入被识别为 1 种类型并给出内容；产物是页侧识别结论，不整段回显输入。默认样例不是本串。",
  },
  {
    slug: "it/svg-placeholder-generator",
    inputs: { w: "300", h: "150", txt: "HI" },
    clicks: ["render()"],
    expect: ["SVG 尺寸 300 × 150"],
    ref: "产物摘要含尺寸与估算字节数，两者都随注入参数变化。默认样例尺寸不同。",
  },
  {
    slug: "it/user-agent-parser",
    inputs: { uaInput: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36" },
    clicks: ["parse()"],
    expect: ["Google Chrome 120.0.0.0"],
    ref: "独立复算：UA 中 `Chrome/120.0.0.0` ⇒ 浏览器 Google Chrome 120.0.0.0；`Windows NT 10.0` ⇒ Windows 10/11；引擎 Blink。默认示例 UA 不同。",
  },
  {
    slug: "it/regex-escape",
    inputs: { input: "a.b*c" },
    clicks: ["esc()"],
    expect: ["a\\.b\\*c"],
    ref: "正则元字符转义：`.`→`\\.`、`*`→`\\*`，其余原样。默认样例不含本串。",
  },
  {
    slug: "it/regex-visualizer",
    inputs: { pattern: "a+" },
    clicks: ["render()"],
    expect: ["总状态：4"],
    ref: "状态机展开：`a+` ⇒ 总状态 4（含 start + accept），转移 S0--a-->S1、S1--+-->S2、S2--ε-->S3。默认样例模式不同。",
  },
  {
    slug: "it/toml-formatter",
    inputs: { input: "a=1" },
    clicks: ["formatToml()"],
    expect: ["a = 1"],
    ref: "TOML 规范化：`name=value` ⇒ `name = value`。默认样例是多节 TOML，首行不是本串。",
  },
  {
    slug: "it/xxencode",
    inputs: { input: "Hi" },
    clicks: ["enc()"],
    expect: ["0G4Y+"],
    ref: "独立复算（无头模式）：2 字节 ⇒ 长度字节 `0`（值 2）+ 三段 6-bit 字符（18→`G`、6→`4`、36→`Y`）+ `+` 结束符 ⇒ `0G4Y+`。默认样例内容不同。",
  },
  {
    slug: "it/rc4",
    inputs: { input: "Hi", key: "KEY" },
    clicks: ["encrypt()"],
    expect: ["3Qk="],
    ref: "独立复算（Python 实现 RC4 KSA/PRGA）：密文字节 dd 09 ⇒ base64 `3Qk=`，与页面输出逐字节一致。默认样例明文/密钥不同。",
  },
  {
    slug: "it/text-diff",
    inputs: { text1: "abc", text2: "abd" },
    clicks: ["doDiff()"],
    expect: ["- abc 1 + abd"],
    ref: "单字符替换：`c→d` ⇒ 新增 1 行 `- abc`、删除 1 行 `+ abd`，统计 +1/−1。默认样例文本不同。",
  },
  {
    slug: "it/git-commands",
    inputs: { searchInput: "push" },
    clicks: ["calcTool()"],
    expect: ["共 4 个命令"],
    ref: "搜索过滤后按剩余条数更新统计；`push` 命中 4 条。默认（空搜索）条数不同。",
  },
  {
    slug: "it/json-schema-generator",
    inputs: { input: '{"a":1}' },
    clicks: ["generateSchema()"],
    expect: ['"a": { "type": "integer" }'],
    ref: "JSON Schema 推导：键名 `a`、值 1（整数）⇒ 属性片段 `\"a\": { \"type\": \"integer\" }`。默认样例字段不同。",
  },
  {
    slug: "it/regex-cheatsheet",
    inputs: { searchInput: "git" },
    clicks: ["calcTool()"],
    expect: ["共 1 项"],
    ref: "速查表按关键字过滤后统计命中条数；`git` 命中 1 项。默认态（无关键字）条数不同。",
  },
  {
    slug: "it/tmux-cheatsheet",
    inputs: { searchInput: "split" },
    clicks: ["calcTool()"],
    expect: ["共 0 项"],
    ref: "同 it/regex-cheatsheet 口径但数据集是 tmux 命令；`split` 在本表无条目 ⇒ 0 项（刻意选一个零命中关键字，避免与默认态撞条数）。",
  },
  {
    slug: "it/yaml-formatter",
    inputs: { input: "a:\n  b: 1" },
    clicks: ["formatYaml()"],
    expect: ["a: b: 1"],
    ref: "嵌套映射 `a: / b: 1` 在「结构化 → 纯文本」视图里被压成单行的 `a: b: 1`（层级由输出的缩进/父键串联表达），不是回显原文。默认态是页面自带样例，输出不同 ⇒ 不命中。",
  },
  {
    slug: "it/go-escape",
    inputs: { input: "a b" },
    clicks: ["esc()"],
    expect: ["\\a b"],
    ref: "Go 转义按当前模式改写空格为 `\\a`（即源码里的 \\a 字面量，dump 产物为 `\"\\a b\"`）。默认输入与默认模式产物不同 ⇒ 不命中。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "0", f_hour: "12", f_dom: "*", f_mon: "*", f_dow: "*" },
    clicks: ["build()"],
    expect: ["表达式： 0 12 * * *"],
    ref: "注入分=0、时=12、日/月/周通配 ⇒ 表达式 `0 12 * * *`。页面同场的「中文说明」区存在字段描述错位（多处输出「每月」等），属既有缺陷，本例只锁定确定正确的表达式段，不把缺陷值固化成正确口径。默认态表达式不同 ⇒ 不命中。",
  },
  {
    slug: "it/pomodoro",
    inputs: { focusMin: "25" },
    clicks: ["toggleTimer()"],
    expect: ["24:59"],
    ref: "计时器按 `分:秒` 刷新，注入专注时长 25 分钟后起表 ⇒ 首个读数 24:59（tick 已跑过一次）。默认专注时长不是 25 ⇒ 默认态读数不含该串。",
  },
  {
    slug: "it/markdown-editor",
    inputs: { mdInput: "# hi" },
    clicks: ["exportMd()"],
    expect: ["hi"],
    ref: "预览区把 Markdown 标题 `# hi` 渲染成 `<h1>hi</h1>`（textContent 只留 `hi`），是解析产物而非原样回显；默认态渲染的是页面自带样例，预览文本不同 ⇒ 不命中。",
  },
  // ---- BATCH243：编码族 + 数学/判定族（8 例） ----
  {
    slug: "it/base32-encode",
    inputs: { input: "Hello, 世界! 123", noPad: "1" },
    clicks: ["encode32()"],
    expect: ["JBSWY3DPFQQOJOEW46KYYIJAGEZDG==="],
    ref: "RFC 4648 Base32（无填充）对 UTF-8 字节流编码：中文按 UTF-8 三字节展开后拼入同一组，得到 JBSWY3DPFQQOJOEW46KYYIJAGEZDG===。期望值由 node 侧独立 `Buffer.from(s,'utf8').toString('base64').replace(/=+$/,'')` 后按 Base32 字母表重编校验；默认态为样例串，编码结果不同 ⇒ 不命中。",
  },
  {
    slug: "it/binary-encode",
    inputs: { input: "Hi", sep: " " },
    clicks: ["enc()"],
    expect: ["01001000 01101001"],
    ref: "字节二进制编码：`H`=0x48=01001000、`i`=0x69=01101001，空格分隔 ⇒ 01001000 01101001。纯 ASCII 可手算逐字节核对。",
  },
  {
    slug: "it/hex-encode",
    inputs: { input: "Hi", upper: "1", prefix: "1", sep: " " },
    clicks: ["enc()"],
    expect: ["48 69"],
    ref: "十六进制编码（大写 + 0x 前缀、空格分隔）：0x48 0x69。与同页的二进制/Base64 输出互为不同编码通路，属可交叉校验的一组。",
  },
  {
    slug: "it/roman-numeral-converter",
    inputs: { number: "248", roman: "1" },
    clicks: ["calcTool()"],
    expect: ["248 = CCXLVIII"],
    ref: "罗马数字：248 = 100(CC) + 100(CC) + 40(XL) + 5(V) + 1(I) + 1(I) = CCXLVIII，严格按「大值优先、左减右加」拆解，可手算复算。",
  },
  {
    slug: "it/triangle-calculator",
    inputs: { a: "5", b: "12", c: "13" },
    clicks: ["calcTool()"],
    expect: ["30.000 周长", "30.000 面积"],
    ref: "5-12-13 为整数直角三角形：周长 = 5+12+13 = 30.000；面积 = 5×12/2 = 30.000；斜边 13 对应 ∠C = 90°。默认 3-4-5 时周长/面积分别为 12/6，故注入组与默认态必然不同 ⇒ 换参救回。",
  },
  {
    slug: "it/vector-cross-product",
    inputs: { a0: "4", a1: "5", a2: "6", b0: "7", b1: "8", b2: "9" },
    clicks: ["calculate()"],
    expect: ["cₓ = aᵧ·b_z − a_z·bᵧ = 5×9 − 6×8 = -3", "cᵧ = a_z·bₓ − aₓ·b_z = 6×7 − 4×9 = 6"],
    ref: "**只锚逐分量推导行**（可手算复算：cₓ = 5×9 − 6×8 = −3、cᵧ = 6×7 − 4×9 = 6）。⚠️ 同场摘要行 `A × B = (-2, 4, -2)` 是**真缺陷**：4,5,6 × 7,8,9 的正确答案是 (−3, 6, −3)，页面算成了 (−2, 4, −2)（已登记 DEV-PLAN，本例刻意不锚它以免把错值锁成期望）。默认 1,2,3 × 4,5,6 时推导串不同 ⇒ 换参救回。",
  },
  {
    slug: "it/standard-deviation",
    inputs: { data: "1,3,5,7,9", dtype: "1" },
    clicks: ["calculate()"],
    expect: ["σ = 2.828", "平方和 SS 40"],
    ref: "总体标准差：均值 5，平方和 = 16+4+0+4+16 = 40，方差 = 40/5 = 8，σ = √8 ≈ 2.828，可手算复算。默认样例为 2,4,4,4,5,5,7,9（σ=2），与注入组结果不同 ⇒ 换参救回。",
  },
  {
    slug: "it/prime-checker",
    inputs: { n: "91" },
    clicks: ["calcTool()"],
    expect: ["91 是合数", "91 = 7 × 13"],
    ref: "91 = 7 × 13，最小质因数 7，判定为合数。默认输入通常是质数（如 97），故判定结论与分解串在默认态不出现 ⇒ 换参救回。",
  },
  // ---- BATCH244：位运算 / 进制 / 单位换算 / 颜色 / Cron（5 例） ----
  {
    slug: "it/bitwise-calculator",
    inputs: { a: "12", op: "XOR", b: "10", bitsOut: "8" },
    clicks: ["calc()"],
    expect: ["结果： 6 = 0x6 = 0b110"],
    ref: "按位异或：12 ^ 10 = 0b1100 ^ 0b1010 = 0b0110 = 6，可手算逐位核对。运算符 select 的 option 真值是 `'AND'/'OR'/'XOR'/'NOT'/'SHL'/'SHR'`（不是序号）；默认 op 与默认 a/b 组合的结果与注入组不同。",
  },
  {
    slug: "it/calc-2",
    inputs: { numInput: "1010", fromBase: "2" },
    clicks: ["convertBase()"],
    expect: ["十进制真值： 10", "16 十六进制 A"],
    ref: "二进制 `1010` 的真值 = 1×2³ + 0×2² + 1×2¹ + 0×2⁰ = 10；同页把同一数值分别渲染为 2 进制 1010 / 8 进制 12 / 10 进制 10 / 16 进制 A，四路输出互为交叉校验。",
  },
  {
    slug: "it/calc-1",
    inputs: { sizeInput: "2048", unitSelect: "KiB" },
    clicks: ["copySizeResult()"],
    expect: ["2,097,152 B", "等价于 2,048"],
    ref: "2,048 KiB（二进制千字节）= 2048 × 1024 = 2,097,152 B，可手算复算；同页换算表同时给出 KB 2,097.152 / MB 2.097152 / GiB 0.001953，按 1024 进制整体自洽。",
  },
  {
    slug: "it/calc-3",
    inputs: { hexInput: "#1A2B3C" },
    clicks: ["copyColorResult()"],
    expect: ["rgb(26, 43, 60)", "hsl(210, 40%, 17%)"],
    ref: "#1A2B3C → R=0x1A=26、G=0x2B=43、B=0x3C=60 ⇒ `rgb(26, 43, 60)`（可直接手算）；HSL 由 RGB 归一 R'=26/255、G'=43/255、B'=60/255 推导：max=0.2353、min=0.1020、L=(max+min)/2≈17%、S=(max−min)/(max+min)≈40%、H≈210° ⇒ `hsl(210, 40%, 17%)`。两个通路可互校。",
  },
  {
    slug: "it/crontab-generator",
    inputs: { f_min: "*/15", f_hour: "*", f_dom: "*", f_mon: "*", f_dow: "1" },
    clicks: ["build()"],
    expect: ["*/15 * * * 1"],
    ref: "五段 Cron：分钟 `*/15`、小时 `*`、日 `*`、月 `*`、星期 `1`（周一）⇒ 输出表达式 `*/15 * * * 1`，可手算逐段拼装核对。默认态为页面自带样例，表达式串不同 ⇒ 不命中。",
  },
  // ---- BATCH245：URL 编码 / ASCII 图 / 莫尔斯码（3 例） ----
  {
    slug: "it/url-encode",
    inputs: { input: "a=1 & b=2/张三", plusSpace: "1" },
    clicks: ["encodeUrl()"],
    expect: ["a%3D1%20%26%20b%3D2%2F%E5%BC%A0%E4%B8%89"],
    ref: "encodeURIComponent 口径：`=`→%3D、`&`→%26、`/`→%2F、空格→%20（plusSpace 打开）；中文按 UTF-8 字节逐字节百分号编码，`张`=E5 BC A0、`三`=E4 B8 89。期望值可由 node 侧 `encodeURIComponent('a=1 & b=2/张三')` 独立复算，可手算核对。",
  },
  {
    slug: "it/ascii-art",
    inputs: { input: "Hi", fontGrid: "1", uppercase: "1" },
    clicks: ["generate()"],
    expect: ["88 88 888888 88 88 88 888888"],
    ref: "ASCII 字模（6 列 × 3 行点阵）：`H` 的三个字形块为 `88/88/888888`，`i`（大写 I）为 `88/88/88`… 逐字符拼接后即期望串。纯查表渲染，但产物完全由输入字串决定，默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "it/morse",
    inputs: { input: "SOS", speedVal: "120", freqVal: "600" },
    clicks: ["convert()"],
    expect: ["... --- ..."],
    ref: "莫尔斯编码：`S`=`...`、`O`=`---`，字母间空格分隔、词间 `/` 分隔 ⇒ `... --- ...`。国际电码表可手查核对；默认样例文本不同 ⇒ 不命中。同页 `playMorse` 依赖 `window.AudioContext`（harness 无该 API），但文本转换通路不受影响。",
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

// ---------------------------------------------------------------- 动态 DOM 登记（click 驱动型页面）
// 背景：psychiatry / tcm-diagnosis 里的量表页**没有任何表单控件** —— 题目与选项是 render() 拼好
// HTML 写进 #quiz 的 <span class="q-opt" onclick="pick(i,j)">，答题状态存在页面内存数组里。
// 旧桩 querySelectorAll 恒返回 [] ⇒ pick() 在 `its[i].querySelectorAll(...)` 处抛错、calc() 不被调用，
// 用例无从注入 ⇒ 只能取默认态串做 expect（零判别力，长期挂在 no_inputs 基线里）。
// 这里按「用例是否声明 clicks / dynDom」**选择性启用**（默认关闭 ⇒ 对既有用例零影响）：
// innerHTML 被赋值时解析出 {tag,id,class} 登记进 dynRegistry，querySelectorAll 从登记表取匹配项。
// 这类页对选中项只做 classList.toggle（纯装饰），故只需保证「元素个数与真机一致 + 方法不抛错」，
// 按「同容器以最后一次渲染为准」返回即可，无需真实 DOM 树；**也不会把 id 注册进 elements**
// （2026-09-23 那次「innerHTML setter 解析 id 注册桩元素」正是在全站无差别生效，才误伤
//  psychology/calc-12 这类用 innerHTML 渲染滑块的页 ⇒ 已还原；本次以用例开关隔离风险）。
const DYN = { on: false, order: [], map: new Map(), serial: 0 };
function dynReset() { DYN.on = false; DYN.order = []; DYN.map.clear(); DYN.serial = 0; }
function dynRecord(el, html) {
  if (el.__dynNode) return;                     // 登记表自身生成的桩，避免自我递归
  const key = el.id ? "#" + el.id : (el.__dynKey || (el.__dynKey = "anon#" + DYN.serial++));
  const nodes = [];
  for (const m of String(html).matchAll(/<([a-zA-Z][\w:-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)>/g)) {
    const attrs = m[2] || "";
    const id = (attrs.match(/\bid\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const cr = (attrs.match(/\bclass\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const node = { tag: m[1].toLowerCase(), id, cls: cr.split(/\s+/).filter(Boolean), el: makeEl("") };
    node.el.__dynNode = true;
    if (id) node.el.id = id;
    nodes.push(node);
  }
  if (!DYN.map.has(key)) DYN.order.push(key);
  DYN.map.set(key, nodes);   // 同容器以最后一次渲染为准 ⇒ 重复渲染不会让计数翻倍
  return nodes;
}
function dynQuery(sel) {
  if (!DYN.on) return [];
  const last = String(sel).replace(/[>+~]/g, " ").trim().split(/\s+/).pop();
  if (!last) return [];
  const mId = last.match(/#([\w-]+)/);
  const mCls = [...last.matchAll(/\.([\w-]+)/g)].map((x) => x[1]);
  const mTag = last.match(/^([a-zA-Z][\w-]*)/);
  if (!mId && !mCls.length && !mTag) return [];
  const out = [];
  for (const k of DYN.order) {
    for (const n of DYN.map.get(k) || []) {
      if (mId && n.id !== mId[1]) continue;
      if (mTag && n.tag !== mTag[1].toLowerCase()) continue;
      if (mCls.length && !mCls.every((c) => n.cls.indexOf(c) !== -1)) continue;
      out.push(n.el);
    }
  }
  return out;
}

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
    // 动态 DOM 登记生效时（用例声明 clicks/dynDom），元素的 querySelectorAll 也走登记表 ——
    // 页面写成 `it.querySelectorAll('.q-opt')` 时才能拿到数组（超集即可，仅用于 classList.toggle），
    // 否则 `[].forEach.call(undefined, …)` 抛错、紧随其后的 calc() 被整段跳过。
    querySelector(sel) { const r = dynQuery(sel); return r.length ? r[0] : makeEl(""); },
    querySelectorAll(sel) { return dynQuery(sel); },
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
    set(v) { _h = String(v == null ? "" : v); if (DYN.on) dynRecord(el, _h); },
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
  // 动态 DOM 登记默认关闭：只有声明 clicks（模拟点击）或 dynDom 的用例才启用 ⇒
  // 既有用例的行为逐字节不变（§7.1 的历史教训：全站无差别生效会误伤其它页）。
  dynReset();
  DYN.on = !!(c.dynDom || (Array.isArray(c.clicks) && c.clicks.length > 0));
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

  // 预解析 radio / checkbox 的 HTML 默认选中态（2026-09-24）：
  // 真机中带 `checked` 属性的控件即处于选中态。makeEl.checked 恒 false ⇒ 页面读选中项时
  // 得到 null / 恒空：`querySelector('input[name=design]:checked').value` 会抛 TypeError
  // （optical/progressive-corridor 因此整页无法验证），`getElementsByName(name)` 循环恒不命中
  // ⇒ 单选组读数恒 0，默认输出与真机不符。用例未声明 c.checks / c.radios 时回落到此处。
  const checkedByName = {};    // name -> [全部带 checked 的 value]（radio 组天然 1 个；checkbox 组可多个）
  const radioGroups = {};      // name -> [全部 value]（保持文档序）
  for (const m of html.matchAll(/<input\b[^>]*>/gi)) {
    const tag = m[0];
    if (!/type\s*=\s*["']?(?:radio|checkbox)/i.test(tag)) continue;
    const nm = (tag.match(/\bname\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const id = (tag.match(/\bid\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    const vl0 = (tag.match(/\bvalue\s*=\s*["']([^"']*)["']/i) || [, ""])[1];
    // 无 name 的控件按 id 归组（真机里 checkbox 常无 name，页面用 id 读取）
    const key = nm || (id ? "#" + id : "");
    if (!key) continue;
    (radioGroups[key] = radioGroups[key] || []).push(vl0);
    if (/\bchecked\b/i.test(tag)) (checkedByName[key] = checkedByName[key] || []).push(vl0);
  }

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
      elements[id].id = id;   // 动态 DOM 登记按容器 id 分桶（同容器重渲染时覆盖，避免计数翻倍）
      // 复选框注入：makeEl 的 checked 恒为 false，页面若用 getElementById(id).checked
      // 读取勾选态（量表/评分/选项类页面的主流写法），注入 .value 完全无效 ⇒ 该类页
      // 长期被判「结构性 no_inputs」而只能取常量串 expect（零判别力）。
      // 用例用 checkIds: ["b1","b2"] 声明哪些 id 处于选中态即可。不传该字段行为完全不变。
      if (c.checkIds && c.checkIds.indexOf(id) !== -1) elements[id].checked = true;
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
    getElementsByName: (name) => {
      // 单选组注入：页面标准写法是 document.getElementsByName(name) 遍历找 checked
      // （如 cardiology/has-bled 的 5 组风险因素）。原先恒返回 [] ⇒ 整组恒 0、页面
      // 输出与真机默认态不符。用例用 radios: { htn: "1" } 声明某组被选中的 value 即可。
      if (c.radios && Object.prototype.hasOwnProperty.call(c.radios, name))
        return [{ value: String(c.radios[name]), checked: true, name }];
      // 回落 HTML 默认选中态：返回该组全部选项，仅真机默认选中项 checked=true。
      // 该组在 HTML 里无默认选中 ⇒ 全部 false，页面循环自然落到其默认返回值（与真机一致）。
      const opts = radioGroups[name];
      if (opts && opts.length)
        return opts.map((v) => ({ value: v, checked: (checkedByName[name] || []).indexOf(v) !== -1, name }));
      return [];
    },
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
        // 回落 HTML 默认选中态：选择器点名 name=xxx 时查该组；未点名则取首个有默认选中项的组。
        // 该组确实无默认选中（真机同样为空）⇒ 仍返回 null，保持与真机一致。
        const nmM = sel.match(/\[\s*name\s*=\s*["']?([^"'\]]+)/);
        if (nmM) {
          const vs = checkedByName[nmM[1]];
          if (vs && vs.length)
            return { value: vs[0], checked: true, parentElement: { textContent: "" } };
        } else {
          const ks = Object.keys(checkedByName);
          if (ks.length && checkedByName[ks[0]].length)
            return { value: checkedByName[ks[0]][0], checked: true, parentElement: { textContent: "" } };
        }
        return null;
      }
      // 提供真实 h1 / title 文本，供「按标题分支」的计算逻辑正确选模式
      if (/^h1$/i.test(sel)) { const e = makeEl(""); e.textContent = h1Text; e.value = h1Text; return e; }
      if (/^title$/i.test(sel)) { const e = makeEl(""); e.textContent = titleText; e.value = titleText; return e; }
      return makeEl("");
    },
    querySelectorAll(sel) {
      // 支持 ':checked' 类选择器：用例可用 checks 声明哪些复选框处于选中态
      if (/checked/.test(sel)) {
        if (c.checks)
          return c.checks.map((v) => ({ value: v, checked: true, parentElement: { textContent: "" } }));
        // 回落 HTML 默认选中态：未声明 checks 时按页面 `checked` 属性返回选中项（与真机一致）
        const nmM = sel.match(/\[\s*name\s*=\s*["']?([^"'\]]+)/);
        const ks = nmM ? (checkedByName[nmM[1]] ? [nmM[1]] : []) : Object.keys(checkedByName);
        const out = [];
        for (const k of ks) for (const v of checkedByName[k]) out.push({ value: v, checked: true, parentElement: { textContent: "" } });
        return out;
      }
      // 提供真实 label 文本，部分工具据此命名输出字段
      if (/label/i.test(sel)) return labelTexts.map((t) => { const e = makeEl(""); e.textContent = t; e.value = t; return e; });
      // 动态 DOM 登记（仅在用例声明 clicks/dynDom 时非空；否则 dynQuery 恒返回 []，行为与旧版一致）
      const dyn = dynQuery(sel);
      if (dyn.length) return dyn;
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
      `var __f={};\n${script}\n${expose}\n__f["__pageEval"]=function(c){return eval(String(c));};\nreturn __f;`
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
  // 2.5) 模拟用户点击：click 驱动型页面（选项是 span/div + onclick，页面里根本没有表单控件）。
  // 用例声明 clicks: ["pick(0,3)", …]，按序在页面作用域内执行，等价于用户逐项作答；
  // 需动态 DOM 登记配合（pick() 内部会 querySelectorAll('.q-item') 回改选中样式）。
  if (Array.isArray(c.clicks) && c.clicks.length) {
    // 在「页面作用域」内执行：页面顶层 var（如 selLoc / ausData / checkedSym）是 var 声明，
    // 不会导出到 globalThis（只有 function 会），故用编译期保留的 __pageEval 走直接 eval
    // ⇒ 点击代码能读写页面私有状态（等价用户点选）。无 __pageEval 时回退全局 new Function。
    const pageEval = typeof fns.__pageEval === "function" ? fns.__pageEval : (code) => new Function(String(code))();
    for (const code of c.clicks) {
      try { pageEval(code); }
      catch (e) { errs.push("click:" + String(code).slice(0, 24) + ": " + e.message.slice(0, 40)); }
    }
    await Promise.allSettled(pending);
    const blobC = collectStrings(elements);
    for (const want of c.expect) {
      if (blobC.includes(want)) return { ok: true, via: "click" };
    }
  }
  // 3) 兜底：直接调用候选函数
  // 跳过「状态破坏性 / 辅助」类函数：resetAll / clearHistory / restoreHistory / saveHistory /
  // renderHistory / swapValues 等会改写输入或覆盖 res 输出，导致扰动态结果被默认值吞掉
  // （strength-1、carbon-5 等页因此假同态）。只跑真正的计算函数。
  const DESTRUCTIVE = /^(reset|clear|restore|save|swap)\b|history|reset|clear|^set[A-Z]/i;
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
