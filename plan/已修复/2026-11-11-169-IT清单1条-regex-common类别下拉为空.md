# 第169批 · IT 清单 1 条 · regex-common 类别下拉无 option

- 来源：`plan/categories/01-IT开发/it.md` → IT-D27（问题表格行 + 族矩阵 + 逐页结论摘要已同步更新）
- 修复日期：2026-11-11
- 类型：功能缺失（8 类正则仅默认 email 可达），纯前端 UI + 英译映射

## 失败点
`tools/it/regex-common.html` 的 `<select id="cat"></select>` 全文件没有任何 `<option>`，页面用 `getElementById('cat').value||'email'` 取值恒为空 → 恒回退 email；工作原理解释了 8 类、速查表也列了 6 类，但用户无法切换，手机/URL/IPv4/日期/身份证/用户名/中文 7 类正则永不生效。

## 根因
构建页面时漏写下拉选项，`regs`/`names` 字典虽完整但无入口选中。

## 修复位点
1. `tools/it/regex-common.html`：`#cat` 内补齐 8 个 option（email 默认 selected），value 与 `regs`/`names` 键一一对应，文本沿用 `names` 中文原文。
2. `js/tool-i18n-en.js`：GEN_UI_MAP 前段新增 9 条精确整节点映射（label「正则类别」+ 8 个 option 文本），保证英文态零 CJK 残留、中文往返一致。
3. 输出逻辑、原文高亮与命中偏移明细未动。

## 证据
1. **verify 强锁**：`scripts/verify_it_calc.js` 新增用例，经 clicks 探针读 `#cat.options.length`（旧源码 0 → 新源码 8）；regex-common 4/4、it 全量 **1497/1497**。
   - **踩坑**：harness 的 stub DOM 对 select 不建模 `innerHTML`，探针初版读 `innerHTML` 永远空；改读 `options.length` 后判别成立（harness `makeEl` 由静态 `<option>` 预解析出 `options` 数组）。
2. **旧源码差分**：换回 `HEAD` 旧 HTML → regex-common 3/4 红（新锁失败）；恢复修好版 → 4/4 绿。
3. **JSDOM 真机**（`scripts/_verify_it_batch169.mjs`）：**14/14 PASS**，覆盖 8 个 option 结构/值序、默认 email、8 类逐一切换均能产出对应类别名与命中内容、同一文本切不同类别结果不同、resetForm 回 email、option 中文原文就位。
4. **判别力**：单文件 1496 已检 / 1495 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1。
5. **门禁辅助**：`audit_verify_input_ids.js` 10237 用例全键命中、僵尸 id 0 / 缺页 0；`_en_i18n_probe --check it/regex-common` 残留 0 页、`--roundtrip` 不一致 0 页。

## 备注
- 本批只改源码 + i18n 英译表 + verify + 清单条目（表格行+族矩阵+摘要）+ 真机脚本 + 本移交档；攒批后统一跑全站门禁。
- IT-D39（ini `:` 分隔）、IT-D29（regex-escape `\d` 反转义口径）经核对均属口径灰区（工具原理/反转义口径与清单期望冲突），未擅动，仍留清单待裁断。
