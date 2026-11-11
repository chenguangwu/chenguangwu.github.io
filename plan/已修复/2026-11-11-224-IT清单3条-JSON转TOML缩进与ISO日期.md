# 2026-11-11 第224批 · IT-N199–N201 `json-to-toml`（3 条）

## 一、进批探测结论

清单 3 条标注「确认缺陷」，真机复算后：

- **N199 已由其他 Agent 修好（漏销账）**：`tomlKey()` 已按 `/^[A-Za-z0-9_-]+$/` 判裸键，不匹配则 `JSON.stringify` 加引号；`{"a.b":1}` → `"a.b" = 1`、`{"a b":1}` → `"a b" = 1`、`{"":1}` → `"" = 1`（TOML quoted key 允许空串，比清单「空键改报错」的方案更合规）。
- **N201 的 null / 混合数组已修（漏销账）**：`tomlVal(null)` 抛「TOML 没有 null 类型」、对象与标量混排数组抛「不支持对象与标量混排」；verify 已有 IT-N23 两把锁。
- **N200 仍是真缺陷**：`getIndent` 声明两次且全文件从未被 `toToml` 调用，输出固定无缩进，三档下拉与「Tab 缩进」预设完全无效。
- **N201 的 ISO 日期仍未修**：字符串一律 `JSON.stringify`，`{"d":"2020-01-01T00:00:00Z"}` 输出 `d = "2020-01-01T00:00:00Z"`，与 meta/简介「支持 ISO 日期字符串」宣称不符。
- **顺带发现**：313–322 行是一组重复注入的同名函数，后者静默覆盖前者；生效的 `setErr` 只要 `s` 非空就不给 `ok` 类 ⇒ 连「✅ 转换成功」都显示红色。

## 二、改动清单

| 编号 | 文件 | 改动 |
| --- | --- | --- |
| N199 | — | 已修，本批补 5 项真机证据 + 1 条 verify 防回退锁 |
| N200 | `tools/it/json-to-toml.html` | `toToml(v, prefix, depth, unit)` 接收 `getIndent()` 结果，标量行与表头按 `unit.repeat(depth)` 缩进；表数组 `[[...]]`、压缩转换 `doMinToml()` 同步生效 |
| N200 | 同上 | 删掉重复注入的一组同名函数（`getIndent`/`setOut`/`setErr`/`clearAll`/`loadSample` 各留一份）；`setErr` 成功/空态给 `err ok` 绿、失败态给 `err` 红 |
| N201 | 同上 | 新增 `tomlDateLiteral()`：严格 ISO 8601 date / datetime / time 输出 TOML 原生裸值，保留小数秒与偏移、空格分隔归一为 `T`，月日/时分秒先做范围校验；不合格与普通字符串仍双引号转义 |
| 公式 | 页面 `formula-eq` + `i18n/tools/en/it/json-to-toml.json` | 补键名引用 / 缩进 / ISO 日期三条规则，中文 key 与英译同步，旧「strings are always double-quoted」口径清零 |
| verify | `scripts/verify_it_calc.js` | 新增 4 条强锁 `UC224I/T/D/K` |
| 真机 | `scripts/_verify_it_batch224.mjs`（新增） | 36 项断言，含三档缩进互异与语义等价、日期边界、全链路、状态链、公式三源 |

```javascript
function toToml(v, prefix, depth, unit){
  prefix = prefix || ''; depth = depth || 0;
  if(unit === undefined) unit = getIndent();
  const pad = unit.repeat(depth);
  ...
  for(const k in scalar) s += pad + tomlKey(k) + ' = ' + tomlVal(scalar[k]) + '\n';
  ... s += '\n' + pad + '[' + full + ']\n' + toToml(tables[k], full, depth + 1, unit);
}
```

**ISO 日期取舍**：JSON 没有日期类型，本批按页面宣称把严格 ISO 字符串识别成 TOML 原生 date/datetime/time（裸值）。`2020-13-45`、`25:99:99` 这类范围不合法的仍按普通字符串加引号，避免产出非法 TOML；数组内的日期同样按裸值。

## 三、验证证据

| 项 | 结果 |
| --- | --- |
| JSDOM 真机（修好版） | **36/36** |
| JSDOM 旧源码差分（`git show HEAD:` → `/tmp/bk224/old.html`，不碰工作区） | **18/36**，18 项红；N199 五项、null/混排数组两项在旧页仍过 ⇒ 印证漏销账 |
| `verify_it_calc.js` | **1572/1572**（新增 4 条；缩进与删重复函数后全集无回归） |
| `discriminate_check.js verify_it_calc.js` | 已检 1571 / 正确变红 1570 / 逃生 1（既有 `it/vector-magnitude`）/ 跳过 1 ⇒ 基线不变 |
| `audit_verify_input_ids.js` | 10364 用例 / 30887 注入键 / 缺页 0 / 僵尸 id 0 |
| `audit_deepdive_source_sync.py --check` | 扫描 4573 页，不一致 0 页 |
| `node --check` + script 块 `new Function` + `git diff --check` | 通过 |

## 四、踩坑（记死）

1. **en JSON 可能有多个同前缀中文键**：本页有两个「递归转换：把当前层级的键分为标量与表两类…」键（短 151 字 / 长 215 字），页面 formula-eq 用的是**长键**。用短键做 `str.replace` 会把长文本的前缀替换掉、残留旧后半段，页面公式变成 497 字的「新文案 + 旧文案」拼接，且 en JSON 出现新旧两把键。正确做法：从 `git show HEAD:` 恢复 map 顺序 → 只替换长键 → 把 formula-eq **整块**设为纯新文案 → 短键原样保留。三源同步前必须先枚举所有同前缀键并比对长度。
2. **函数重复定义不一定无害**：生成器两次注入同一组辅助函数，后定义的 `setErr` 会静默覆盖前一个更正确的实现；删重复块时要确认保留的是语义正确的那份。
3. **缩进断言要在页内判形态**：harness blob 折叠空白，4 空格 / Tab 差异写不进 expect，须用 clicks 探针把「是否匹配 `\n {4}c = 2` / `\n\tc = 2`」编码成哨兵。
4. **ISO 自动识别必须先做范围校验**：否则 `2020-13-45` 会变成裸值导致 TOML 解析失败；宁可退回加引号的普通字符串。

## 五、纪律

- 只**本地 commit**，不 push；只 `git add` 具体文件；`.workbuddy` 不入库。
- 旧源码差分用「`git show HEAD:` 写临时文件 + 脚本读临时文件」，全程不覆盖工作区、不用 `git checkout --`。
- 本批为 222–226 攒批第 3 批，只跑轻量验证；攒满后统一跑全站判别 + `run_gates.py` 并查 build 后 `git status`。
