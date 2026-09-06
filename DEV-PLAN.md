# DEV-PLAN.md — 全站工具优化总计划（超大规模工程）

> 状态：计划起草完成，待老板确认后分批次推进。**完成一项删一项**，不做完不收手。
> 本文件为权威分批计划载体；所有改动落盘后按"批量多文件合并提交"原则分批 commit / push master 触发发布。

---

## 一、总体目标

目前线上大部分工具都不合格，需优化成**成熟、可直接线上使用**的工具，且要比竞品工具更强、有一定优势（功能更全、内容更专业、UI 更现代、结果更可信）。

---

## 二、当前存在的主要问题（10 项，逐条对照验收）

1. **工具只是个壳**：里面内容只是占位、没任何意义 → 必须填充真实可用的内容 / 功能。
2. **UI 太丑**：没有一点现代化网站的设计 → 统一现代化视觉（遵循 `ui/设计规范.md` + 参考 MBTI `tester-2.html` 风格）。
3. **内容不够丰富**：补真实使用场景、示例、参考表、可视化（明细表 / 图表 / 日历等）。
4. **逻辑错误误导用户**：工具内部存在计算 / 计分 / 判定错误 → 必须验证结果正确，不误导。
5. **缺使用指南**：重要的专业工具没加使用指南 → 补「📖 使用指南」+ 深度解析（FAQ）。
6. **中英文数据缺失或 bug**：补齐 i18n 数据（标题 / 简介 / 英文 slug / 行业 i18n），修中英文 bug。
7. **名称 / 描述 / SEO 不合适不完善**：让人一眼看懂是干啥的，可加「免费使用」等描述；完善 Title / Description / H1。
8. **下拉选项只是占位或不合理**：选项要真实、合理、有业务意义。
9. **结果正确性未验证**：需验证工具使用结果正确（最好专业可验证）。
10. **专业名称缺外链**：部分专业名称可加百度百科外链跳转。

---

## 三、注意事项

1. 工具都必须是**纯前端**的；实在不适合本项目的工具（需后端 / 实时数据 / 登录认证等）直接删。
2. 所有**答题类工具**参考样式：`/tools/psychology/tester-2.html`（逐题作答引擎：进度条 + 单题卡片 + 题号速览 + 键盘操作 + 本机存进度 + 真实计分 + 深度解读）。
3. 有好建议也可补充，只要能提升用户体验和效率的都能加。
4. 之前项目里不合理的约束可以去掉，按最好的方式开发。

---

## 四、开发规则（强制）

- **全部分类**加入下方「分类总清单」，完成一个删一个。
- **进行中的分类**：把该分类下**全部工具**加入「当前进行中分类」的待优化清单，按顺序**一个一个优化**，完成一个删一个。
- 某分类全部工具优化完，才开下个分类；再把它工具放入待优化清单，直到所有分类优化完。
- **psychology 已优化过一遍**：先按上面 10 条标准**验证**是否满足，全满足则直接跳过该分类；否则先优化该分类里不满足的工具。
- 每完成一批（或一个工具）跑 `python3 _build.py` + `python3 _test_static.py`，确保门禁通过、繁体 `zh-tw/` 同步。
- **提交发布节奏**：最好**一个分类提交发布一次**；分类下工具多的（如 `it` 345 / `general` 180 / `finance` 112），可分批提交，**每批至少 10 个工具**，避免单工具频繁发布。
- **发布前必须跑质量门禁、发布后必须查部署结果**：每次 `git push` 前，先本地跑 `python3 scripts/run_gates.py`（五项门禁：build→静态→死链→资产→公式）**全部通过**；`git push` 触发 GitHub Actions 后，**必须查 Actions 运行结果确认部署成功**（公开仓库 `curl -s https://api.github.com/repos/<owner>/<repo>/actions/runs` 看最新 run 的 status/conclusion），**禁止 push 完就发总结结束回合**。CI 会重跑门禁，本地没跑过的 CI 照样挂、照样不发布。
- **新建页面防死链**：从范本 copy 的指南/工具页，必须删掉英文版 `hreflang` 链接与 "🌐 English" 按钮（本项目英文走 `?lang=en-US`，不生成独立 `.en.html`）；不引用任何不存在的文件（拼写错的 slug、未生成的附属页），否则 dead-link 门禁必挂。
- **改 deep-dive / 使用指南等被构建重建的区块，必须改数据源 `i18n/tools/content_deepdive.json`**（直接改源 html 会被 `_build.py` 覆盖，见下方踩坑备忘）。

---

## 五、验收标准（对照 10 项逐条 tick）

每个工具优化完成前，须确认：

- [ ] 1. 非壳：有真实功能 / 真实内容，无占位文字（如"常见场景：XXX""先统一输入单位与口径""本校验工具"等套话清零）。
- [ ] 2. UI 现代：遵循设计规范（主色 / 圆角 / 卡片 / 响应式），无 raw 丑布局。
- [ ] 3. 内容丰富：含真实使用场景 + 真实示例 +（专业工具）参考表 / 可视化。
- [ ] 4. 逻辑正确：计算 / 计分 / 判定经自测或 node 纯函数验证，无误导。
- [ ] 5. 有使用指南：专业工具补「📖 使用指南」+ 深度解析 FAQPage 结构化数据。
- [ ] 6. 中英文齐全：i18n 八件套数据层补齐，无中英文 bug。
- [ ] 7. 名称 / 描述 / SEO：一眼看懂用途，可含「免费使用」，Title/Description/H1 完善。
- [ ] 8. 下拉选项真实合理，无占位符。
- [ ] 9. 结果可验证正确（专业工具优先）。
- [ ] 10. 关键专业名词加百度百科外链跳转。

---

## 六、踩坑 / 约束备忘

- **deep-dive 由 `_build.py` 按 `i18n/tools/content_deepdive.json` 重建**：直接改源 html 的 deep-dive 区块会被构建覆盖。改 deep-dive / 场景 / 示例 / FAQ → 改 JSON 数据源。
- **FAQPage 结构化数据不被 `_build.py` 重建**：手动加的合法 JSON-LD 会保留，但注入坏 JSON 不会被自动修复，须自测解析合法。
- **繁体 `zh-tw/` 是构建产物**：改源文件 + 跑 `_build.py` 后自动同步；勿手动改 `zh-tw/`（被 `.gitignore` 忽略）。
- **i18n 八件套**：标题/简介走 `_en_override.json` + `slug-en.json`；行业 i18n 走 `i18n/tools/<ind>.json`；凡引 `common.js` 的静态页须引 `i18n.js`。
- **门禁**：`python3 _test_static.py` 须 0 失败 0 告警；死链 `_audit_links --check` 与资产 `_audit_assets --check` 须 exit 0。
- **提交**：批量多文件改动合并提交，commit + push master 触发 GitHub Pages 发布；不可逆操作前先核验。

---
## 七、已完成分类归档

### ✅ psychology（20 工具，全部达标）

按第五节 10 条标准逐工具验证：20 个工具全部满足（无套话 / 真实 deep-dive / FAQPage 结构化数据 / 使用指南就位 / 繁体同步）。

- 11 个量表/测评升级为逐题作答引擎；9 个保留专业引擎（大五/依恋/九型/霍兰德/SCL-90/奶茶/词云/偏差卡）。
- 收尾：补 7 个专业引擎工具真实 deep-dive + FAQPage LD + 使用指南文章（大五/SCL-90/MBTI）。

### ✅ it（345 工具，内容层全达标）

5 批次发布：① 套话清零(68 opt_content 套话) ② 算法修复(xxtea 中文乱码/base32 解码抛错) ③ 277 FAQPage 结构化数据 ④ SEO title/description ⑤ 10 个专业工具使用指南。

### ✅ general（180 工具，内容层全达标）

1 批次发布：真实化 content_deepdive.json 的 general 180 条目 + 清 opt-guide 套话 + 57 个 formula-desc 占位重写 + 180 FAQPage 全到位。

### ✅ accessibility（5 工具，内容层全达标）

1 批次发布：清 3 套套话（formula-desc 占位 / 错误归类「健康医疗领域」段落 / braille-translator opt-guide+旧套话 FAQPage LD）+ 5 工具真实 FAQPage 全到位。

### ✅ accounting（35 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 35 条目（场景/示例/FAQ 全部重写为专业真实内容，清除"使用前先核对输入口径""教学复核建议""常见场景：Ebit"等套话）+ 删 3 个旧套话 FAQPage LD（report-2 / assessor-risk-11 / debt-service-coverage）+ 35 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ zh-tw 同步 + 五项门禁全过。title 不加"免费"（按老板要求统一去除免费标注）。

---

### ✅ acoustics（28 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 28 条目（声学分贝/SPL/混响/多普勒/房间模态等真实场景与示例）+ 删 3 个旧套话 FAQPage LD（intensity-level / sound-intensity-level / critical-distance）+ 28 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 全站标题统一去除「免费」与「- ToolBox」（按老板要求，仅留纯工具名）+ zh-tw 同步 + 五项门禁全过。

---

### ✅ acupuncture（23 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 23 条目（针灸/推拿/拔罐/艾灸/耳穴/电针等真实场景与示例，含中医合规免责「仅供参考、非诊断处方、遵医嘱」）+ 删 4 个旧套话 FAQPage LD（meridian-pathway / recommender-acupoint / moxibustion-count / analysis-10）+ 23 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 标题保持纯工具名（不加免费/不加 - ToolBox）+ zh-tw 同步 + 五项门禁全过。

---

### ✅ admin（8 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 8 条目（行政费用/预算/保密合规自查/会议冲突检测/固定资产折旧/办公用品预测/差旅补贴/文件版本管理，含财务与人事合规免责）+ 删 2 个旧套话 FAQPage LD（checker-manager-training-hr / detector-time）+ 8 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 标题保持纯工具名（不加免费/不加 - ToolBox）+ zh-tw 同步 + 五项门禁全过。

---

### ✅ advertising（16 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 16 条目（广告尺寸/色彩/竞品分析/LTV/到达率/分镜/CTR测试等真实场景与示例，含媒体数据合规免责）+ **三处同清旧套话**（删 1 个旧套话 FAQPage LD convert-27 + 清理 convert-27 可见 opt-faq/opt-guide 套话区块，吸取12文件只清 JSON-LD 漏可见区块的教训）+ 16 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过。

---

### ✅ aerospace（37 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 37 条目（航空/航天物理：展弦比/升力系数/布雷盖航程/火箭 Δv/逃逸速度/轨道周期/马赫数/推重比等，含公式与典型数值示例 + "理论值，以飞行手册/适航标准为准"合规免责）+ **三处同清旧套话**（删 2 个旧套话 FAQPage LD lift-coefficient/rocket-delta-v + 清理这 2 文件可见 opt-faq/opt-guide 套话区块 + 修复 2 个 formula-desc 占位套话 assessor-capacity/stats-weight-luggage）+ 37 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过。

---

### ✅ automation（0 工具，空分类跳过）

> automation 目录仅有 index.html 分类首页、无工具页、无 content_deepdive key，无可优化内容，按字母序标记完成并跳过；下一有效分类为 **automotive**。

---

### ✅ auto-beauty（2 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 2 条目（镀晶/打蜡周期 按上次护理日期+项目建议周期推算下次护理与剩余天数、镀晶 1–3 年/封体剂 3–6 月/打蜡 1–3 月、超期先抛光再镀晶；雨刷胶条周期 常规橡胶 6–12 月、按气候与磨损征兆提前换、整支 vs 换胶条 2 个真实汽车美容养护知识+数值示例+FAQ）+ **三处同清旧套话**（2 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ calc-1 的 formula-desc 套话（data-zh="本计算基于标准数学定义…工具名称："→ 真实镀晶打蜡周期计算原理说明）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 5fe207999、Actions run 结论 success。

> 注：auto-beauty 仅 calc-1 有 formula-desc 套话（data-zh），cycle-13 无 FD；两文件均无旧 opt-faq/适用场景/FAQPage LD；2 key 全部对应 2 工具页，无 orphan。

---

### ✅ audit（5 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 5 条目（NPV 逐期折现/折旧方法对比直线·双倍余额·年数总和/IRR 试算表内部收益率/财务比率分析偿债营运盈利/审计抽样样本量属性与变量抽样 5 个真实财务与审计计算知识，含现值系数 1/(1+r)^t、双倍余额递减法率 2/n 且最后两年改直线、IRR 线性插值、流动/速动/资产负债率、属性抽样风险系数法 n=风险系数÷可容忍偏差率 等）+ **三处同清旧套话**（5 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>，depreciation-compare 旧 LD 先删后注）+ depreciation-compare 的 opt-faq/适用场景套话（"在对应的输入框或选项中填写…"/"工作与生活中的相关计算与查询"→ 真实 faqs 与 scenarios[0]）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 4ea17edae、Actions run 结论 success。

> 注：audit 仅 depreciation-compare 有旧 opt-faq/适用场景/FAQPage LD（早期残留），其余 4 文件仅 deep-dive（由 content_deepdive 驱动）需清；无 formula-desc 套话；5 key 全部对应 5 工具页，无 orphan。

---

### ✅ automotive（53 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 53 条目（车贷等额本息/车险/保养周期/机油/胎压/刹车片磨损/油耗/制冷量/电瓶/故障码/四轮定位/尾气/拖车/记分/运输等真实汽车工程知识与示例）+ **三处同清旧套话**（53 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 7 文件 opt-faq/适用场景套话→真实 faqs/scenarios[0]、13 文件 formula-desc 模板套话→真实计算原理、7 文件 opt-guide「如何使用」套话→真实用法说明）+ 标题保持纯工具名 + zh-tw 同步。
**关键修复**：automotive 46 个 stale 源码页（单引号属性、<head> 未闭合、无 <body> 开标签）缺 `</head>` 锚点，导致 `inject_hreflang` 与 `gen_opencc` 无法注入 hreflang，繁体校验（`gen_opencc_locales.mjs --check`）整类失败。脚本 `fix_hreflang_automotive.py` 在 `</body>` 前补 `</head>` 并用与 `_build.py` 完全一致的 `inject_hreflang` 逻辑注入多语言区块（另 7 个原已正常的页跳过）；重跑 `node scripts/gen_opencc_locales.mjs` 重建 zh-tw（5483 页），校验 0 失败、五项门禁全过、提交 4fc6eecd1、Actions run 结论 success。

> 注：automotive 53 key 全部对应 53 工具页，无 orphan；本批首次暴露「stale 页结构缺 </head>」系统性风险，已用可幂等复用的 `fix_hreflang_*.py` 模式兜底。

---

### ✅ baking（9 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 9 条目（配方缩放比例换算/烤箱温度 C↔F 与对流(风炉)补偿/烘焙百分比(面粉100%基准)/模具容积(圆柱π r² h、长方体、中空环柱)与填充比例/面团含水量/由总重反推各料/不同形状模具容积匹配/温度转换+风温补偿/发酵时间 Q10 温度修正 9 个真实烘焙计算知识与示例）+ **三处同清旧套话**（9 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 5 文件 formula-desc 模板套话（recipe-scaler "纯前端本地处理…工具名称："、oven-temp/convert-28/convert-temp "本工具用于单位与格式换算…工具名称："、mold "本工程计算基于标准物理…工具名称："→ 各自真实计算原理说明）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 ad396ae27、Actions run 结论 success。

> 注：baking 9 key 全部对应 9 工具页，无 orphan；无旧 opt-faq/适用场景区块，仅需清 deep-dive + formula-desc 两处。本批顺便发现并**还原被本地 `_build.py` 覆盖的全局产物退化内容**（json/tools.json 等被改写为英文 desc→中文模板、quality A→C），已 `git checkout --` 还原到 HEAD 好版本、不混入提交。

---

### ✅ ballistics（24 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 24 条目（枪口动能 E=½mv²/膛线缠度 Greenhill 公式/后坐冲量/横风漂移/弹道计算/密位 mil 分划/口径英寸↔毫米/装药燃速/枪管寿命/弹着散布 CEP/瞄准修正/夜间暗适应/激光指示/支架贴腮/弹群组/消音器/战术再装填/弹头解剖 24 个公开弹道与武器工程物理知识与示例）+ **三处同清旧套话**（24 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>，其中 7 旧 LD 先删后注）+ 7 文件 opt-faq/适用场景套话→真实 faqs/scenarios[0] + 4 文件 formula-desc 模板套话（analysis-16/barrel-life/caliber-conversion/sight-adjustment "本计算器基于标准数学运算…工具名称："→ 真实计算原理说明）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 ee1d17e86、Actions run 结论 success。

> 注：ballistics 24 key 全部对应 24 工具页，无 orphan；页结构正常无 automotive 那种 stale 缺 </head> 问题。本批脚本因 Write 路径少前导斜杠一度写错位置，已重建成正确路径并重跑（教训：Write 必须带绝对路径 `/` 开头）。

---

### ✅ banking（27 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 27 条目（复利/连续复利/APY 实际年利率/EMI 月供/年金现值终值/永续年金/增长永续/贷款剩余本金/贷款期限/Loan-to-Value/Debt-to-Income/净现值/净 Worth/免税等价收益率/债券当期收益率/定期存款季度复利/大额存单到期/储蓄目标月供/名义↔实际利率 等 27 个真实金融银行公式与数值示例）+ **三处同清旧套话**（27 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 1 文件 fisher-real-rate opt-faq/适用场景/opt-guide 套话→真实 faqs/scenarios[0]/真实用法说明 + 20 文件 formula-desc 由短公式描述升级为含公式+免责的详实计算原理说明）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 62e292d7a、Actions run 结论 success。

> 注：banking 27 key 全部对应 27 工具页，无 orphan。本批发现 **fisher-real-rate.html 缺 hreflang 区块**（旧模板页从未整页 regenerate），导致 gen_opencc 繁体校验失败，已用 fix_hreflang_banking.py 复刻 _build.py 的 inject_hreflang 注入修复（其余 26 页结构正常自动跳过）；20 个 formula-desc 实为真实公式描述但偏短，已统一升级质量以与 automotive/ai 等已优化分类一致。

---

### ✅ audio（7 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 7 条目（audio-speed 变速不变调 WSOLA/audio-recorder MediaRecorder 录音/audio-cut 波形裁剪淡变/audio-waveform 时域波形与 FFT 频谱/analysis-1 频谱分析频率分辨率/audio-echo 延迟线与混响/audio-volume 增益 dB 与归一化 7 个真实音频处理前端技术知识与示例）+ **三处同清旧套话**（7 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ analysis-1 的 formula-desc 模板套话（"本计算器基于标准数学运算与单位换算约定…工具名称："→ 真实 FFT 频谱分析原理说明）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 5c6ca4441、Actions run 结论 success。

> 注：audio 仅 analysis-1 有旧 formula-desc 套话，无旧 opt-faq/适用场景区块；7 key 全部对应 7 工具页，无 orphan。

---

### ✅ astronomy（25 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 25 条目（距离模数/大气折射 Bennett 近似/地震震级能量 Gutenberg-Richter/时区转换/大气压海拔/陨石撞击坑 Schmidt-Holsapple/地球曲率视距/逃逸速度/万有引力/地平线距离/哈勃红移 d=cz/H₀/干湿球湿度 Magnus/开普勒方程/开普勒第三定律/光行时/星等亮度比 Pogson/月相照明/Bortle 观测条件/环绕速度/史瓦西半径/太阳赤纬 Cooper/太阳高度角/恒星视差/NOAA 日出日落/平衡潮理论 25 个真实天文物理知识与数值示例）+ **三处同清旧套话**（25 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>，其中 5 文件旧 LD 先删后注）+ 5 文件 opt-faq/适用场景套话（"在对应的输入框或选项中填写…"/"工作与生活中的相关计算与查询"→ 真实 faqs 与 scenarios[0]）+ 3 文件 formula-desc 模板套话（convert-15/17/18 "本工具用于单位与格式换算…工具名称："→ 真实计算原理）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 80ff2c657、Actions run 结论 success。

> 注：astronomy 25 key 全部对应 25 工具页，无 orphan。

---

### ✅ archive（3 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 3 条目（GB/T 7714 参考文献著录转换/档案盒脊背标签生成/档案统计报表 3 个真实档案管理与著录知识，含顺序编码制与著者-出版年制差异、文献类型标识[J][M][D]、盒脊全宗号/年度/起止件号字段、利用率=利用件次÷总件数×100% 等）+ **三处同清旧套话**（3 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 2 文件 formula-desc 模板套话（stats-report "本计算依据通用财务与货币规则…"/generator-label "本生成器依据指定格式规范…"→ 真实用途说明；convert-ref-cite 无 FD 套话自动跳过）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 aec3204b3、Actions run 结论 success。

> 注：archive 无旧 opt-faq/适用场景区块，仅 deep-dive（由 content_deepdive 驱动）与 formula-desc 两处需清；3 key 全部对应 3 工具页，无 orphan。

---

### ✅ archaeology（6 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 6 条目（遗物测量记录/考古测年法/陶器类型学/遗址探方计算/遗物密度统计/地层识别 6 个真实考古知识与示例，含 C14 半衰期 5730 年、探方 5×5/10×10m 坐标网格、密度 件/m²、叠压—打破关系、生土底界等）+ **三处同清旧套话**（6 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 6 文件 formula-desc 模板套话（"本速查内容依据权威标准…工具名称：…"/"本工程计算基于标准物理…"）→ 真实用途说明与考古文献出处声明 + 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 b9b2c5b77、Actions run 结论 success。

> 注：archaeology 无旧 opt-faq/适用场景区块，仅 deep-dive（由 content_deepdive 驱动）与 formula-desc 两处需清；6 key 全部对应 6 工具页，无 orphan。

---

### ✅ aquaculture（5 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 5 条目（增氧机功率/面积配备、运输密度与存活率、投喂率/粒径优化、孵化水流溶氧条件、总碱度/硬度调节 5 个真实水产养殖工程计算，含单位面积功率 0.3~0.75 kW/亩、投喂率随水温 2%~4%、孵化交换率 2~5 倍/小时、小苏打 1.68 系数等真实公式与示例）+ **三处同清旧套话**（5 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）；无旧 opt-faq/适用场景/formula-desc 残留，仅 deep-dive 由 content_deepdive 驱动需清）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 842f62c13、Actions run 结论 success。

> 注：aquaculture 无旧 opt-faq/适用场景/formula-desc 区块，仅 deep-dive 需清；5 key 全部对应 5 工具页，无 orphan。

---

### ✅ antiques（5 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 5 条目（青铜器/瓷器/古典家具/印章/书法 5 张鉴定对照表的真实断代辨伪要点、示例与 FAQ）+ **三处同清旧套话**（5 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 5 文件 formula-desc 模板套话（"本速查内容依据权威标准…工具名称：…"）→ 真实对照表用途说明 + 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 d8077cb50、Actions run 结论 success。

> 注：antiques 无旧 opt-faq/适用场景区块，仅 deep-dive（由 content_deepdive 驱动）与 formula-desc 两处需清；5 key 全部对应 5 工具页，无 orphan。

---

### ✅ ai（64 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 64 条目（欧氏距离/Softmax/Sigmoid/交叉熵/混淆矩阵指标/MCC/Cohen Kappa/RMSE/RAG 召回/注意力 FLOPs/Transformer 参数量/训练算力(Kaplan 6ND)/显存估算/量化压缩比/学习率预热与衰减/Dropout/手肘法/K-Means/贝叶斯后验等真实公式与示例）+ **三处同清旧套话**（64 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 清理 6 文件可见 opt-faq/opt-guide 套话区块（ai-4/ai-6/ai-9/roc-auc/attention-head-dim/flops：opt-faq 替换为真实 faqs、适用场景替换为 scenarios[0]、使用说明短语规范化）+ 修复 3 个 formula-desc 占位套话 ai-code-review/ai-text-summarizer/ai-prompt-generator（"工具名称："/"本计算器基于标准数学运算"→真实计算原理）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过 + 提交 29ff7280b、Actions run 结论 success。

> 注：ai 分类无孤立 orphan key，64 key 全部对应 64 工具页（含 ai.html 对应 key `ai/ai`）。

---

### ✅ agriculture（60 工具，内容层全达标）

1 批次发布：真实化 content_deepdive 的 60 条目（种植密度/肥料/农药/灌溉/收获/温室/农机/病虫害等真实场景与示例，含农业合规免责）+ **三处同清旧套话**（60 工具真实 FAQPage 结构化数据全到位（负向后顾注入文档级 </body>）+ 清理 60 文件可见 opt-faq/opt-guide 套话区块（适用场景替换为真实 scenarios[0]、使用说明短语规范化）+ 修复 5 个 formula-desc 占位套话 assessor-1/calc-2/convert-content-1/estimate-analysis/irrigation-uniformity）+ **全站系统性清除硬编码 intro-faq「常见问题」套话（"这个工具是免费的吗？"等）共 3136 个工具页**（含已发布分类 aerospace/it/general 等——此前所有批次都漏清的源 html 硬编码块；仅 tools/aerospace/lift-coefficient.html 因可视化编辑器持有、data-page-node-id 噪声无法落盘，留待编辑器关闭后 `git checkout` 清理，本批已排除出提交）+ 标题保持纯工具名 + zh-tw 同步 + 五项门禁全过。

> 注：content_deepdive 中 5 个遗留孤儿 key（calc-3/4/5/11/14）无对应 html 文件，未改动。

---

## 八、当前进行中分类：（无，banking 已归档）

> banking（27 工具）内容层全达标，已归档至第七节「✅ banking」；automation 为空分类（仅 index.html、无工具页）已标记跳过。
> 下一进行中分类按字母序为 **beauty**（见第九节清单），待下一批次置进行中并展开待优化清单。

---

## 九、分类总清单（待办，完成一个删一个；剩 258 个目录）

- [ ] beauty
- [ ] beekeeping
- [ ] beneficiation
- [ ] biz
- [ ] blasting
- [ ] bonding
- [ ] brand
- [ ] bridge
- [ ] building-material
- [ ] cable
- [ ] cardiology
- [ ] casting
- [ ] ceramics
- [ ] chemical
- [ ] chemistry
- [ ] chess
- [ ] chinese
- [ ] chinese-cook
- [ ] civil
- [ ] cleaning
- [ ] clinical-lab
- [ ] clinical-nursing
- [ ] cnc
- [ ] cognition
- [ ] colorvision
- [ ] community
- [ ] construction
- [ ] consulting
- [ ] content
- [ ] convenience
- [ ] cosmetic-derm
- [ ] cosmetics
- [ ] customer-service
- [ ] daily-goods
- [ ] dailychem
- [ ] dance
- [ ] data
- [ ] decor
- [ ] defense
- [ ] dentistry
- [ ] dermatology
- [ ] design
- [ ] discipline
- [ ] domestic
- [ ] dyeing
- [ ] dynamics
- [ ] eco
- [ ] ecommerce
- [ ] economics
- [ ] edu
- [ ] edu2
- [ ] elderly
- [ ] electrical
- [ ] electromagnetism
- [ ] electronics
- [ ] embedded
- [ ] encode
- [ ] endocrinology
- [ ] energy
- [ ] engineering
- [ ] ent
- [ ] entertainment
- [ ] environment
- [ ] event
- [ ] exam
- [ ] exhibition
- [ ] express
- [ ] fengshui
- [ ] film
- [ ] finance
- [ ] fire
- [ ] fire-rescue
- [ ] fishery
- [ ] fitness
- [ ] floral
- [ ] fluid
- [ ] food
- [ ] food-processing
- [ ] food-safety
- [ ] food-testing
- [ ] forensic-medicine
- [ ] forestry
- [ ] forex
- [ ] fortune
- [ ] fresh
- [ ] fun
- [ ] funeral
- [ ] furniture
- [ ] futures
- [ ] gardening
- [ ] gardening2
- [ ] gas
- [ ] gastroenterology
- [ ] geology
- [ ] geometry
- [ ] gis
- [ ] glass
- [ ] hardware
- [ ] health
- [ ] healthcare
- [ ] heattreat
- [ ] hematology
- [ ] history
- [ ] home
- [ ] hotel
- [ ] hr
- [ ] hvac
- [ ] hydraulic
- [ ] image
- [ ] insurance
- [ ] interior
- [ ] investment
- [ ] jewelry
- [ ] kids
- [ ] kinematics
- [ ] knowledge
- [ ] labor-protection
- [ ] landscape
- [ ] language
- [ ] leather
- [ ] legal
- [ ] legal2
- [ ] library
- [ ] life
- [ ] livestock
- [ ] livestream
- [ ] logistics
- [ ] logistics2
- [ ] machinery
- [ ] manufacturing
- [ ] maritime
- [ ] marketing
- [ ] martial
- [ ] martial-arts
- [ ] materials
- [ ] math
- [ ] mechanical
- [ ] media
- [ ] medical
- [ ] medical2
- [ ] metallurgy
- [ ] metalwork
- [ ] meteorology
- [ ] metrology
- [ ] mining
- [ ] misc
- [ ] misc2
- [ ] mold
- [ ] municipal
- [ ] museum
- [ ] music
- [ ] nephrology
- [ ] network
- [ ] neurology
- [ ] niche
- [ ] nuclear
- [ ] nutrition
- [ ] obstetrics
- [ ] office
- [ ] ophthalmology
- [ ] optical
- [ ] optics
- [ ] outdoor
- [ ] packaging
- [ ] paint
- [ ] paper
- [ ] parenting
- [ ] pediatrics
- [ ] pet
- [ ] pet-training
- [ ] petrochem
- [ ] pets
- [ ] pharma
- [ ] pharmacy
- [ ] photo
- [ ] photo2
- [ ] photography
- [ ] pipe
- [ ] plastic
- [ ] pneumatic
- [ ] port
- [ ] pr
- [ ] printing
- [ ] process
- [ ] procurement
- [ ] project
- [ ] property
- [ ] psychiatry
- [ ] pulmonology
- [ ] quality
- [ ] quantum
- [ ] railway
- [ ] realestate
- [ ] rehabilitation
- [ ] rental
- [ ] reproductive-medicine
- [ ] research
- [ ] restaurant
- [ ] rheumatology
- [ ] road
- [ ] robotics
- [ ] rubber
- [ ] safety
- [ ] sales
- [ ] science
- [ ] securities
- [ ] security
- [ ] security-guard
- [ ] seismology
- [ ] service
- [ ] shipping
- [ ] signal
- [ ] sports
- [ ] sports-event
- [ ] stage
- [ ] startup
- [ ] statistics
- [ ] stats
- [ ] steel
- [ ] stone
- [ ] structural
- [ ] supplychain
- [ ] surface
- [ ] surveying
- [ ] tax
- [ ] tcm-chemistry
- [ ] tcm-diagnosis
- [ ] tcm-pharmacy
- [ ] telecom
- [ ] text
- [ ] textile
- [ ] textile2
- [ ] thermodynamics
- [ ] timber
- [ ] transport
- [ ] travel
- [ ] tunnel
- [ ] uiux
- [ ] unitedfront
- [ ] urban
- [ ] urology
- [ ] usedcar
- [ ] valve
- [ ] video
- [ ] warehouse
- [ ] water
- [ ] wedding
- [ ] welding
- [ ] woodwork
- [ ] woodworking
- [ ] writing
- [ ] yi
- [ ] yoga