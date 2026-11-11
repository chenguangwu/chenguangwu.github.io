# 2026-11-11 第227批 · IT-N212–N216（nanoid-generator 3 条 + markdown-table-generator 2 条）

## 一、进批探测结论

清单 5 条全标「确认缺陷」，真机复算确认均为真缺陷（本批无漏销账），且 N213 比清单描述更深：

- **N212**：`nanoid()` 的 `idx = bytes[i] & mask`，单字节最大 255 ⇒ 字母表 257+ 时后段字符不可达。
- **N213**：`getAlphabet()` 用 `a.length`/`new Set(a)`/`alphabet[idx]` 按 UTF-16 码元处理，emoji 拆代理对；真机进一步发现 **`nanoid()` 内部 `id.length === size` 也按码元计数**，导致 100 位 emoji 只生成 50 个（100 码元）提前停；且 `gen()` 的 catch 只 `alert()`，非法字母表时不清空旧结果（G10 旧结果残留）。
- **N214**：`__nanoid_generatorResText()` 用 `querySelector('.result-box')` 取到静态说明块，历史/图表 `结果` 恒为同一段说明。
- **N215**：`escapeMarkdown()` 只把 `|` 换 `\|`，输入自带 `\` 时变 `\\|`，GFM 把 `\\` 当字面反斜杠、`|` 重新成列分隔符。
- **N216**：`syncColumns()` 把补齐的 `列/值` 写回 input.value，键入时值立即变 `a,列,列`，光标跳末尾、删掉的尾列被立刻补回。

## 二、改动清单

| 编号 | 文件 | 改动 |
| --- | --- | --- |
| N212/N213 | `tools/it/nanoid-generator.html` | `getAlphabet()` 用 `Array.from(a)` 按码点校验（长度/去重/取值）；`nanoid()` 用码点数组，≤256 沿用字节 mask 法，>256 改用 32 位无符号加密随机数拒绝采样（`limit=floor(2^32/n)*n`，`v<limit` 才 `%n`），保证全码点等概率可达；计数用 `taken` 而非 `id.length`（emoji 一个码点算一个） |
| N213 | 同上 | `gen()` catch 清空 `#results` 旧结果并写页面内错误提示；`getAlphabet()` 两条抛错串走 `isEn()` 双语（EN 态零 CJK） |
| N214 | 同上 | `__nanoid_generatorResText()` 改读 `#results` 内 `code` 列表文本（无 code 才回落 textContent），排除 `⚠` 错误态；不再碰静态 `.result-box` |
| N215 | `tools/it/markdown-table-generator.html` | `escapeMarkdown()` 先 `replace(/\\/g,'\\\\')` 再 `replace(/\|/g,'\\|')` 再换行换空格 |
| N216 | 同上 | `syncColumns()` 只调 `renderPreview()`，不写回 input.value；缺列由 `fillCells()` 的 `C{i+1}` 占位补齐 |
| 公式 | 两页 `formula-eq` + 各自 `i18n/tools/en/it/*.json` | nanoid 补码点/拒绝采样口径；markdown 补反斜杠转义顺序；中英同步、原位改值保键序 |
| verify | `scripts/verify_it_calc.js` | 新增 4 条强锁（N213 emoji 直测 nanoid、N215 反斜杠、N216 不写回；含 N212 由真机覆盖） |
| 真机 | `scripts/_verify_it_batch227.mjs`（新增） | 16 项断言，含 300 字母表全可达、emoji 码点、历史取值、转义列结构、编辑期不写回、状态链 |

```javascript
// N212/N213 核心：码点数组 + 32 位拒绝采样
if(n <= 256){
  const mask = (2 << Math.floor(Math.log(n - 1) / Math.log(2))) - 1;
  ...
  if(idx < n){ id += alphabet[idx]; if(++taken === size) return id; }
}
const limit = Math.floor(4294967296 / n) * n;
while(taken < size){
  c.getRandomValues(buf); const v = buf[0];
  if(v < limit){ id += alphabet[v % n]; taken++; }
}
```

## 三、验证证据

| 项 | 结果 |
| --- | --- |
| JSDOM 真机（修好版，含两页） | **16/16** |
| JSDOM 旧源码差分 | **4/14**，10 项红；五条核心断言旧页全红 |
| `verify_it_calc.js` | **1581/1581**（新增 4 条；无回归） |
| `discriminate_check.js verify_it_calc.js` | 已检 1580 / 正确变红 1579 / 逃生 1（既有 `it/vector-magnitude`）/ 跳过 1 ⇒ 基线不变 |
| EN 态真机 | 错误提示中/英双语正确，EN 零 CJK |
| `audit_verify_input_ids.js` | 10377 用例 / 僵尸 id 0 / 缺页 0 |
| `audit_deepdive_source_sync.py --check` | 扫描 4573 页，不一致 0 页 |
| 语法 / 页面 script 块 / `git diff --check` | 通过 |

## 四、踩坑（记死）

1. **码点修复要扫全函数**：N213 清单只提 `getAlphabet()`/`alphabet[idx]`，但 `nanoid()` 内 `id.length === size` 仍按 UTF-16 码元计数 ⇒ 100 emoji 只生成 50 个。改成独立 `taken` 计数器才是完整修复；>`256` 分支的 `while(id.length < size)` 同款。
2. **catch 只 alert 是 G10 旧结果残留**：非法字母表抛错后旧结果/历史仍沿用上一次生成，必须在 catch 清空结果区并写页面内提示；提示串还要过 `isEn()` 双语（e.message 本身来自 helper 抛错，需让抛错点按语言生成）。
3. **harness stub 的 radio.checked 恒 false**：verify 里无法通过 `document.querySelector('input[name=...][value=custom]').checked=true` 切换字母表，会读回默认字母表并报错；改为直接调用全局 `nanoid(100, Array.from('😀😁😃😄'))` 测核心函数，判别力等价。
4. **长度上限要按页面约束设**：`gen()` 把 length clamp 到 1–100，测试想采样 4000 字符无效；改为 count=10 × 循环 60 轮累积覆盖。
5. **源码断言正则要留空格**：`function syncColumns() {`（括号前有空格），正则 `function syncColumns\(\)\{` 匹配不到；用 `\s*\{\s*[\s\S]*?\n\s*\}`。
6. **1 列表格判据不能用裸 `|` 计数**：转义后的 `|` 前有双反斜杠，负向后顾 `(?<!\\)\|` 会把列分隔符和转义竖线都算错；改锚「表头行 `| … |` + 分隔行只有一段 `:---`」的形态。

## 五、纪律

- 只**本地 commit**，不 push；只 `git add` 具体文件；`.workbuddy` 不入库。
- 旧源码差分用「`git show` 写临时文件 + 脚本读临时文件」，全程不覆盖工作区、不用 `git checkout --`。
- 本批为 227–231 攒批第 1 批，只跑轻量验证；攒满 5 批后统一跑全站判别 + `run_gates.py` 并查 build 后 `git status` / 产物 diff。
