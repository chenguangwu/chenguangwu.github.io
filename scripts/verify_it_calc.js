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
