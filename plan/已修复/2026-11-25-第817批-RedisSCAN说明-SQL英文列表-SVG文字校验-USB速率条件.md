# 第817批：Redis SCAN 说明、SQL 英文列表、SVG 文字校验、USB 速率条件

日期：2026-11-25

## Redis 速查：SCAN 不再承诺「不阻塞」

- 权威内容源 `i18n/tools/content_deepdive.json` 中正文场景与 FAQ 同步改写：SCAN 只是把一次大遍历拆成多次小调用，降低单次阻塞时长与内存压力，**不保证完全不阻塞**；每次调用仍占用主线程/事件循环，COUNT 越大占用越久。
- 明确 COUNT 是工作量提示而非严格返回上限；同一游标结果可能为空、可能重复，游标返回 0 才结束；生产需限速、去重、观察延迟，优先用前缀/索引结构缩小范围。
- 页面 `COMMANDS` 的 SCAN 条目同步：desc 改为「游标渐进遍历 key（降低单次阻塞，不保证零阻塞）」，params 补「游标返回 0 才结束；COUNT 是工作量提示而非严格上限；结果可能为空或重复」。
- 英文第三层字典 `i18n/tools/en/it/redis-cheatsheet.json` 更新对应 FAQ、场景与 SCAN 条目的英文译文；`?lang=en-US` 下显示 `does NOT guarantee zero blocking` / `COUNT is a workload hint`，不再回退中文。

## SQL 速查：动态列表整体英文化 + 搜索体验

- 新增 `SQL_CAT_EN`（18 个分类）与 `SQL_DESC_EN`（48 条描述）顶层映射；`renderCategories` / `renderCommands` 按当前语言渲染，`currentCategory` 仍存中文以兼容筛选。
- 英文态计数显示 `N command(s)`，分类标签、参数/语法/分类标签、复制按钮、搜索框占位与 aria-label 全部英文化。
- 搜索同时匹配命令、中文/英文描述、中文/英文分类、参数与示例；英文关键词（如 `pagination`）可直接命中。
- 无结果时给出本地化提示和「清除筛选 / Clear filters」按钮，点击后清空关键字与分类并恢复 48 条。
- 监听 `toolbox:langchange` 重新渲染分类、命令与占位文案。

## SVG 占位图：只校验数值字段，文字不触发预览错误

- `render()` 只对宽度/高度做数值校验：空值、非数字、超出 10–2000 时明确提示并停止生成；不再对整串 SVG/结果摘要跑 `/Infinity|NaN/`。
- 占位文字中的 `NaN`、`Infinity` 作为普通文本原样转义显示。
- 预览、`svgCode`（复制/下载源）使用同一份已验证的 SVG 字符串，避免三处不一致。

## USB 版本对比：版本号不直接推断接口速率

- 比较逻辑改为区分「版本号高低」与「实际链路速率」：同版本输出「同版本档位」；更高版本只说明标称上限更高，实际速率取两端设备、线缆与端口的最低共同能力，不能仅凭版本号推断。
- 接口形态说明改为「Type-A / Type-C / Micro 只是物理形态，不承诺速率」，USB-C 不再写成自动等于全速率；USB 2.0 保留「可承载 480 Mbps」但补充仍受协议/线缆/端口约束。
- 移除 `escH` 与 `ToolBox.setResult` 对字符串的 Infinity/NaN 整体替换。

## 验证

- 定向：`node scripts/verify_it_calc.js it/sql-cheatsheet it/svg-placeholder-generator it/usb-version it/redis-cheatsheet` → 17/17 通过；新增 SQL 英文渲染/英文搜索/清除筛选、SVG 文字 NaN/Infinity、USB 同版本共 6 条用例。
- 全量：`node scripts/verify_it_calc.js` → **2460/2460 通过**。
- 真机（Puppeteer + Chrome，本地 8178 端口）：Redis 中英文 FAQ/SCAN 条目、SQL 英文列表/英文搜索/无结果/清除筛选、SVG 文字与非法宽度、USB 同版本比较 → **12/12 通过**。
- 门禁：`_test_static.py` 4654 通过 / 0 失败 / 0 告警；`_audit_links.py --check` 16795 文件 / 167642 内链 / 0 死链；`_audit_assets.py --check` 0 死链 / 0 lang 缺失 / 0 重复 id；`audit_inline_marker_placement.js` 0 违规。
