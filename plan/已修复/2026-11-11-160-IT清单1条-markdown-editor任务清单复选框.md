# 第160批 · IT 清单 1 条 · markdown-editor 预设「任务清单」复选框渲染

- 来源：`plan/categories/01-IT开发/it.md` → IT-N289（已整条删除）
- 修复日期：2026-11-11
- 类型：中风险确认缺陷（预设承诺功能不支持），纯前端渲染逻辑，无口径裁断

## 失败点
`tools/it/markdown-editor.html` 的 `parseLists()` 只把 `^[-*+]\s+(.+)$` 整段塞进 `<li>`，不识别 GFM task list 的 `[x]` / `[ ]`。预设「任务清单」的 `- [x] 编写文档` 在预览中被渲染成字面量 `<li>[x] 编写文档</li>`，勾选状态完全丢失。

## 根因
列表解析无 task list 分支；`[x]` 前缀在链接解析阶段（`[text](url)` 正则需 `(`）不会被误吃，原样到 parseLists，但这里无条件当普通文本。

## 修复位点
`tools/it/markdown-editor.html` `parseLists()` 无序列表项渲染处：对 item 应用 `/^\[([ xX])\]\s+(.+)$/`，命中则输出 `<li class="task-list-item"><input type="checkbox" disabled[ checked]> 内容</li>`，`x/X` 视为勾选、空格为待办；未命中走原 `<li>` 分支。复选框 `disabled`（预览只读），无新文案（i18n 0 残留），未碰 XSS/属性转义（另项 IT-N288）。

## 证据
1. **verify 强锁**：`scripts/verify_it_calc.js` 新增 it/markdown-editor 用例（注入 `- [x] done-item` / `- [ ] todo-item`，clicks 探针读 `mdPreview.innerHTML`，断言含 checkbox+checked+task-list-item 且无字面 `[x]` 且文本保留，expect `TASKCHECK OK`）。it 全量 **1485/1485**。
2. **旧源码差分**：换回 `HEAD` 旧源码 → 该用例红（3/4，预览含字面 `[x]`、无 checkbox）；恢复修好版 → 4/4 绿。判别力成立。
3. **JSDOM 真机**（`scripts/_verify_it_batch160.mjs`）：**12/12 PASS**，覆盖三任务复选框数/勾选数、无字面 `[x]`/`[ ]`、大写 X、普通无序列表不受影响、混合列表、有序列表不受影响、无空格不误判、batch153 的 NaN/Infinity 正文守卫回归。踩坑：页面有 200ms debounce，input 事件后须 `delay(280)` 才渲染完。
4. **判别力**：单文件 1484 已检 / 1483 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1。
5. **门禁辅助**：`audit_verify_input_ids.js` 10279 用例僵尸 id=0；`_en_i18n_probe --check it/markdown-editor` 残留 0 页。

## 备注
- verify 用例 clicks 探针内禁用 `\"` 转义引号（memory 铁律：反相态会吞闭合括号），改用 `indexOf('checkbox')` 等无引号串。
- 本批只改源码 + verify + 清单条目 + 真机脚本 + 本移交档；按节奏攒批后统一跑全站门禁。
