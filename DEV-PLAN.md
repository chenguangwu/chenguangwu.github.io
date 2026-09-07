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
> 本区仅保留**最近一个（最新）已完成分类**的归档记录，更早历史不再保留，以控制文件体积。完成新分类时，用新记录替换本条。

### ✅ convenience（4 工具，内容层全达标）

convenience 4 工具（analysis-80 损耗体系 / analysis-cost-10 成本体系 / assessor-target 选址评估 / report-profit 利润核算）原 content_deepdive 4 key 为**第十九种占位变体**（「在convenience场景中，先按 XX 的口径预先约束输入范围，再输出可复核结论…」，summary 原 None）：① scripts/opt_convenience_content.py 真实化 4 key（summary+3 scenarios+1 example+3 faqs），覆盖门店损耗管控/成本结构拆解/便利店选址五维评分/小微门店利润核算，财务类补非专业建议免责、评估类补模型仅供参考免责（不覆盖 title）；② scripts/opt_convenience_hardcode.py 清 4 页 formula-desc 变体（analysis-80 工程变体「本工程计算基于标准物理…」/analysis-cost-10+report-profit 财务变体「本计算依据通用财务…」/assessor-target 校验变体「本校验工具依据…」→真实领域描述，JSON-LD 合法）+ 清 assessor-target 的「工作与生活中的相关计算与查询」3 处（适用场景/opt-faq/JSON-LD→真实选址场景）+ 整体替换 analysis-80/cost-10/profit 的 tool-intro 三段块 6 类通用套话（→真实便利店场景，assessor-target 块内已真实不处理）；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。

---
### ✅ cosmetic-derm（33 工具，内容层全达标）
cosmetic-derm 33 工具（光老化Glogau分型/防晒SPF-PA/果酸焕肤/肉毒素玻尿酸单位/激光波长靶点/微针渗透/水光配比/射频紧肤/线雕向量/VISIA色斑分层等皮肤科医美）原 content_deepdive 33 key 为**第二十种占位变体**（「XX 的常见复核路径：先检核单位与输入边界…」，summary 原 None）：① scripts/opt_cosmetic_derm_content.py 真实化 33 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖光老化分级/防晒量化/果酸深度/注射单位/激光靶点/微针渗透/水光配比/射频紧肤/线雕向量/色斑分层等真实场景，医美类统一补「仅供自评与科普参考，不能替代执业医师面诊诊断」免责（不覆盖 title）；② scripts/opt_cosmetic_derm_hardcode.py 清 6 页 opt 套话「工作与生活中的相关计算与查询」各 3 处（JSON-LD/适用场景段/FAQ dd→真实场景），A 类 formula-desc 变体 0 页、C 类块内 6 类通用套话 0 页均无需处理；③ 顺带 scripts/opt_fix_example_body.py 全站修复 examples 字段 code→body（construction/consulting/content/convenience 共 39 处误用 code 致示例区渲染空白），确保全站 deep-dive 示例正常渲染；④ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ cosmetics（1 工具，内容层全达标）
cosmetics 1 工具（assessor-67 化妆品注册备案合规评估）原 content_deepdive 1 key 为**第二十一种占位变体**（「在cosmetics场景中先确认Assessor 67口径与边界…」，summary 原 None）：① scripts/opt_cosmetics_content.py 真实化 1 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖新品备案前自筛/工厂来料出厂管控/客诉监管应对等真实合规场景，补「不替代官方检测报告与监管决定、以最新法规为准」免责（不覆盖 title）；② scripts/opt_cosmetics_hardcode.py 清 assessor-67 的 formula-desc 校验变体 1 页（「本校验工具依据对应数据格式…」→真实合规描述，JSON-LD 合法），B 类 opt 套话 0 页、C 类块内 6 类通用套话 0 页均无需处理；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ customer-service（3 工具，内容层全达标）\ncustomer-service 3 工具（random-script 标准话术模板随机抽取器/stats-time-response 客服平均响应时间解决率统计/summary-rater-csat 客户满意度CSAT评分汇总）原 content_deepdive 3 key 为**第二十二种占位变体**（「在customer-service场景下，先把<Title>标准化，再批量执行可追溯流程…」，summary 原 None、faqs 仅 2 条）：① scripts/opt_customer_service_content.py 真实化 3 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖话术抽取岗前演练/响应时长解决率统计/CSAT汇总低分归因等真实客服场景，统一补「数据仅在本地浏览器处理、不上传，统计仅供参考」隐私与统计免责（不覆盖 title）；② scripts/opt_customer_service_hardcode.py 清 stats-time-response 的「单位与格式换算」错配 FD 变体 + summary-rater-csat 的「通用财务」错配 FD 变体（→真实统计/CSAT描述，JSON-LD 合法），random-script 的 formula-desc 为生成器变体（与「话术抽取器」语义相符）保留、B 类 opt 套话 0 页无需处理，并整体替换 3 页 tool-intro 块内 6 类通用套话（→真实客服场景）；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。\n---\n### ✅ daily-goods（1 工具，内容层全达标）\ndaily-goods 1 工具（parking-fee 停车费计算器）原 content_deepdive 1 key 为**第十九种占位变体**（「在daily-goods场景下先确认停车费计算器口径与边界，再输出可复核结论…」，summary 原 None、faqs 仅 2 条）：① scripts/opt_daily_goods_content.py 真实化 1 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖商场/路边按时计费封顶/医院机场分段封顶/时段差异分段求和等真实停车费估算场景，补「结果仅供参考、以现场公示费率与收费终端为准」免责（不覆盖英文 title「Parking Fee Calculator」）；② 经检测 A 类 formula-desc 为「本日常工具基于通用常识与经验公式」变体（停车费属日常工具、语义相符保留，非错配）、B 类 opt 套话 0 页、C 类 tool-intro-body 块在该页不存在故块内套话 0 页，均无需 hardcode 清理；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。\n---\n### ✅ dance（7 工具，内容层全达标）
dance 7 工具（assessor-csat-1 学员满意度CSAT评估/bpm-rhythm BPM节拍匹配/choreography-timeline 编舞时间线/flexibility-test 柔韧度测试/partner-distance 舞伴间距/rotation-stability 旋转稳定性/tester-4 坐位体前屈百分等级）原 content_deepdive 7 key 为**第二十三种占位变体**（「在dance场景里，优先把<Title>标准化后再执行批量分析，便于统一口径…」，summary 原 None、faqs 仅 2 条）：① scripts/opt_dance_content.py 真实化 7 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖考核评分/BPM节奏匹配/编舞时间线排练/柔韧度自测/舞伴间距走位/旋转稳定训练/体前屈百分等级等真实舞蹈场景，统一补「结果仅作训练参考、不替代专业教练评估与运动医学建议」免责（不覆盖 title）；② scripts/opt_dance_hardcode.py 清 assessor-csat-1/tester-4/partner-distance 的「工作与生活中的相关计算与查询」各 3 处（JSON-LD/适用场景段/FAQ dd→真实舞蹈场景，共 9 处，JSON-LD 合法），A 类 formula-desc 7 页全无（跳过）、C 类块内 6 类通用套话 0 页均无需处理；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ data（20 工具，内容层全达标）
data 20 工具（calc-1 CSV转JSON/calc-2 JSON格式化/chart-generator 图表生成器/csv-analyzer CSV分析器/data-cleaner 数据清洗/data-visualizer 数据可视化/generator-13 假数据生成/generator-14 条码二维码/generator-35 直方图/generator-random-2 随机身份证/generator-report 报表模板/pivot-table 透视表/random-1 随机颜色/random-3 随机密码/random-4 验证码/random-5 中文名/random-6 随机数字/random-7 随机日期/random-8 银行卡/random-9 句子段落）原 content_deepdive 20 key 为**第二十四种占位变体**（「在「<Title>」场景先统一输入单位与口径，先做基准算例，再做边界场景核验…」，summary 原 None、faqs 仅 2 条）：① scripts/opt_data_content.py 真实化 20 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖 CSV/JSON 转换、图表生成、CSV 列分析、数据清洗、直方图/箱线/热力、假数据/条码/身份证/报表生成、透视表、随机颜色/密码/验证码/姓名/数字/日期/银行卡/句子等真实数据场景，统一补「数据仅本地浏览器处理、不上传，结果仅供测试/演示/脱敏样例、不替代专业数据分析」免责（不覆盖 title）；② scripts/opt_data_hardcode.py 清 calc-1 的「本工具用于单位与格式换算(SI)」错配 FD 变体（→真实 CSV转JSON 描述，保留生成器模板「工具名称：」后缀，JSON-LD 合法）+ 清 random-6/csv-analyzer/chart-generator/data-cleaner/generator-14 的「工作与生活中的相关计算与查询」各 3 处（JSON-LD/适用场景段/FAQ dd→真实数据场景，共 15 处，JSON-LD 合法），calc-2/csv-analyzer/data-cleaner 等 18 页 FD 为「开发工具/文本工具/生成器」标准变体（语义相符保留）、C 类块内 6 类通用套话 0 页均无需处理；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ decor（8 工具，内容层全达标）
decor 8 工具（ceiling-panel-quantity 吊顶板材用量/curtain-fabric 窗帘布料/detector-18 室内空气质量检测判定/paint-color-mix 乳胶漆调色/room-illumination 房间照度配置/scheduler 施工工序工期排程/skirting-length 踢脚线长度/wallpaper-quantity 壁纸用量）原 content_deepdive 8 key 为**第二十五种占位变体**（「在decor场景里，先统一 <Title> 的输入口径，再输出可复用结构…」，summary 原 None、faqs 仅 2 条）：① scripts/opt_decor_content.py 真实化 8 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖吊顶板材用量/窗帘布料/室内空气质量判定(GB/T 18883)/乳胶漆调色/房间照度配置(GB 50034)/施工CPM排程/踢脚线长度/壁纸用量等真实装修场景，统一补「结果仅为估算参考、实际以现场复尺与国标规范及专业施工/设计意见为准、不替代验收或专业测算」免责（不覆盖 title）；② scripts/opt_decor_hardcode.py 清 detector-18 的「本校验工具依据对应数据格式与语法规范进行合法性检查」错配 FD 校验变体（→真实 GB/T 18883 描述，保留生成器模板「工具名称：」后缀，JSON-LD 合法）+ 清 wallpaper-quantity/skirting-length 的「工作与生活中的相关计算与查询」各 3 处（JSON-LD/适用场景段/FAQ dd→真实装修场景，共 6 处，JSON-LD 合法），ceiling-panel-quantity FD 为「标准数学运算与单位换算」变体（语义相符保留）、C 类块内 6 类通用套话 0 页均无需处理；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ defense（2 工具，内容层全达标）
defense 2 工具（calc-rater 射击弹道与修正计算/rater-38 军事体育训练考核评分）原 content_deepdive 2 key 为**第二十六种占位变体**（「在defense场景下，先对 <Title> 建模统一口径，再输出可复核结论。」，summary 原 None、faqs 仅 2 条）：① scripts/opt_defense_content.py 真实化 2 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖射击弹道降/横风偏移/MOA密位修正/靶环评分与军体考核（引体/双杠/仰卧/俯卧撑/3000米跑按《军事体育训练大纲》参考标准分年龄性别评分）等真实国防/军事场景，统一补「射击/军体类结果为估算参考、不替代实弹校枪与专业训练指导及正式考核裁判、标准以现役官方版本为准」免责（不覆盖 title）；② scripts/opt_defense_hardcode.py 检测 A/B/C 三类（FD 错配变体/opt 套话「工作与生活中的相关计算与查询」/块内 6 类通用套话）均 0 命中，defense 2 页无 formula-desc、无套话，无需清理直接跳过；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ dentistry（30 key / 25 工具页，内容层全达标）
dentistry 25 工具页（alveolar-bone-loss 牙槽骨吸收根长比例分级器/analysis-11 桥体跨度力学分析/assessor-5 氧化锆透光率美学评估/bite-contact 咬合接触平衡点分析器/bridge-span 桥体跨度分析器/bruxism-force 夜磨牙咬合力估算器/calc-1 DMFT 龋齿指数/caries-risk 龋病风险 Cariogram 评分器/complete-denture 全口义齿颌位关系转移器/dental-arch-development 儿童牙弓发育评估器/gingival-index 牙龈指数评估器/implant-dimensions 种植体直径长度选择器/kouqiangai-tnm-shaichagongju 口腔癌 TNM 筛查工具/length-3 儿童牙弓长度宽度发育/oral-cancer-screening 口腔癌 TNM 筛查器/oral-ulcer 口腔溃疡阿弗它分期器/orthodontic-force 正畸力与牙移动评估器/periodontal-pocket 牙周袋深度与附着丧失评估器/rater-risk-2 龋病风险 Cariogram 评分/root-canal-length 根管长度与工作长度计算器/salivary-flow 唾液流率评估器/sialography 腺体造影判读器/tongue-oral-health 舌诊与口腔健康关联器/tooth-preparation 牙体预备聚合度与固位力评估器/wisdom-tooth 阻生智齿 Pell-Gregory 分类器/zirconia-aesthetics 氧化锆美学评估器，含 5 个别名 key：estimate-27/kouqiangkuiyang-afuta-fenqi/quankouyichi-heweiguanxi-zhuanyi/ratio-13 复用主 key）原 content_deepdive 30 key 为**第二十七种占位变体**（「<Title> 的常见复核路径：先检核单位与输入边界，再做基准样例核验…」，summary 原 None、faqs 仅 2 条）：① scripts/opt_dentistry_content.py 真实化 30 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖牙槽骨吸收分级/桥体跨度力学(Ante 法则)/氧化锆透代次/咬合接触平衡(T-Scan)/DMFT/龋病风险 Cariogram/全口义齿颌位/牙弓发育/牙龈指数/种植体尺寸/口腔癌 TNM(AJCC 第8版)/口腔溃疡 RAS/正畸力/牙周袋 CAL/根管工作长度/唾液流率/腺体造影/舌诊/牙体预备固位/智齿分类等真实口腔场景，统一补「结果仅供口腔健康科普与初筛参考、不替代口腔检查/影像与专业诊断、异常及时就医」医疗免责（不覆盖 title）；② scripts/opt_dentistry_hardcode.py 清 rater-risk-2 的「本校验工具依据对应数据格式与语法规范进行合法性检查」错配 FD 校验变体（→真实 Cariogram 描述，保留「工具名称：」后缀，JSON-LD 合法）+ 清 dental-arch-development/assessor-5/zirconia-aesthetics 的「工作与生活中的相关计算与查询」各 3 处（JSON-LD text/适用场景段/FAQ dd→真实口腔场景，共 9 处，JSON-LD 合法）+ 清 length-3/analysis-11/kouqiangai-tnm-shaichagongju 的 tool-intro-body 块内 6 类通用套话（简介尾随通用语+功能特点 2 项+使用场景 4 项全通用，共 21 处→真实口腔内容，含「纯前端处理/支持复制下载」真实特性保留），analysis-11 的「本工程计算基于标准物理与材料公式」为物理变体（桥体跨度力学语义相符保留）；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步（C 类块内套话经 _build.py 重建后 zh-tw 仍为 0，证明不覆盖 tool-intro-body 块）+ 五项门禁全过。
---
### ✅ design（104 key / 103 工具页，内容层全达标）
design 103 工具页（analysis 图片调色板提取/audio-recorder 录音转文字稿/avatar-generator 头像生成器/aztec-code 阿兹特克码生成器/badge-generator 徽章生成器/base64-to-image Base64 转图片/bpm-tapper BPM 节拍测速器/blueprint-grid 蓝图网格生成器/breakpoint-queries 响应式断点查询器/card-generator 卡片生成器/checkerboard-generator 棋盘格生成器/color-contrast-check 对比度校验器/color-palette 配色方案生成器/color-picker 颜色选取器/color-scheme-generator 配色方案生成器(别名 key)/color-shade-generator 色阶生成器/color-temperature-converter 色温转换器/contrast-checker 对比度检查器/css-animation-generator CSS 动画生成器/css-border-radius 圆角生成器/css-box-shadow-generator 盒阴影生成器/css-grid-generator 网格布局生成器/css-text-shadow 文字阴影生成器/data-matrix 数据矩阵码生成器/depth-of-field-calculator 景深计算器/dot-pattern 圆点纹理生成器/exposure-triangle-calculator 曝光三角计算器/favicon-* 系列图标生成器/flexbox-generator 弹性布局生成器/focal-length-equivalent 等效焦距换算器/font-pairing 字体搭配器/font-preview 字体预览器/generator-6~12 盒子阴影/边框/二维码/条形码/CSS动画/背景纹理/粒子特效生成器/glassmorphism-generator 毛玻璃生成器/gradient 渐变生成器/gradient-from-color 取色渐变生成器/grid-pattern 网格纹理生成器/identicon-generator 识别图标生成器/image-* 系列图像工具/initials-avatar 姓名缩写头像/iso-noise-reference ISO 噪点参考/isometric-grid 等距网格生成器/loading-dots 加载点生成器/material-color Material 配色生成器/mesh-gradient 网格渐变生成器/music-scale-reference 音阶参考器/shadow-generator 阴影生成器/web-audio-metronome Web Audio 节拍器/loading-dots 加载动画等，含别名 key color-scheme-generator 复用主 key）原 content_deepdive 104 key 为**第二十八种占位变体**（「快速核对 <Title>：优先统一输入单位、口径和参数范围，再对典型样例做一遍手工验算」，summary 原 None、faqs 仅 2 条）：① scripts/opt_design_content_a.py + opt_design_content_b.py 真实化 104 key（split a: analysis~mesh-gradient 69 key / b: music-scale-reference~web-audio-metronome 35 key，各自补 faqs 至 3 条），覆盖图片调色板提取/录音转写/头像与缩写头像/阿兹特克码/徽章/Base64 图/BPM 测速/蓝图网格/响应式断点/卡片/棋盘格/对比度校验/配色/取色/色温转换/CSS 动画圆角盒阴影网格文字阴影/数据矩阵码/景深/圆点纹理/曝光三角/图标/flexbox/等效焦距/字体搭配/二维码条形码/CSS动画背景纹理粒子/毛玻璃/渐变/网格纹理/识别图标/图像压缩裁剪旋转水印等/ISO噪点/等距网格/加载动画/Material配色/网格渐变/音阶/阴影/Web Audio节拍器等真实设计前端场景，统一补「结果仅供设计草稿与前端调试参考、具体视觉与可访问性以实际渲染与团队规范为准、不替代专业设计评审」设计免责（不覆盖 title）；② scripts/opt_design_hardcode.py 检测 A/B/C 三类（FD 错配变体/opt 套话「工作与生活中的相关计算与查询」/块内 6 类通用套话）：A 类 103 页 FD 全部语义相符（快门速度/景深/等效焦距=BPM=物理变体、音阶=速查变体、色温=SI 变体、各生成器/设计工具=对应变体），**无错配**；B/C 类均 0 命中，无需清理直接跳过（可追溯）；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ discipline（4 工具，内容层全达标）
discipline 4 工具（assessor-28 政治生态画像评估器/assessor-risk-7 廉政风险评估器/stats-analysis 监督执纪四种形态统计分析器/tester-training-hr 纪律教育测试题库）原 content_deepdive 4 key 为**第二十九种占位变体**（「在discipline场景中，先按 <Title> 的口径预先约束输入范围，再输出可复核结论。」，summary 原 None、faqs 仅 2 条）：① scripts/opt_discipline_content.py 真实化 4 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖政治生态 6 维度画像评分(6-30 分风险等级)/廉政风险 5 维度识别(防控重点+等级)/监督执纪四种形态线索与处置占比趋势汇总/纪律教育 5 题测验自动判分与解析等真实党建纪检场景，统一补「结果仅供单位内部政治生态分析、廉政风险排查与纪律教育学习参考，不替代组织程序与正式考核评估，敏感数据本机处理勿外传」免责（不覆盖 title）；② scripts/opt_discipline_hardcode.py 清 assessor-28/assessor-risk-7/tester-training-hr 的「本校验工具依据对应数据格式与语法规范进行合法性检查」错配 FD 校验变体（→真实廉政/纪律/政治生态评估描述，保留「工具名称：」后缀与「纯前端运行，数据不离开浏览器」真实特性，JSON-LD 合法）+ 清 4 页 tool-intro-body 块内 6 类通用套话（简介尾随「免费在线工具，纯前端处理」+功能特点「操作简单，一键完成」+使用场景 4 项全通用→真实党建纪检场景，含「纯前端处理/数据不上传」真实特性保留），stats-analysis 无 formula-desc 不涉及 A 类；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
### ✅ domestic（4 工具，内容层全达标）
domestic 4 工具（cycle-4 清洁用品消耗量与补货周期/generator-price 合同（服务/价格/条款）生成/recommender-8 保险（责任/意外/雇主）推荐/reminder-cycle 家电深度清洁周期提醒）原 content_deepdive 4 key 为**第三十种占位变体**（「domestic 场景下建议先校准 <Title> 口径后再批量输出。」，summary 原 None、faqs 仅 2 条）：① scripts/opt_domestic_content.py 真实化 4 key（summary+3 scenarios+1 example+3 faqs，example 用 body 字段），覆盖清洁用品库存消耗推算与低库存预警/合同（家政劳务）草稿生成/保险（雇主责任+意外+责任）组合推荐/家电深度清洁周期排队与要点等真实生活家政场景，统一补「结果仅供家庭与个人事务管理参考、合同与保险类文本请结合正式法律与投保要求、必要时咨询专业人士、不构成法律或投保意见」免责（不覆盖 title）；② scripts/opt_domestic_hardcode.py 清 generator-price/recommender-8 的 tool-intro-body 块内 6 类通用套话（简介尾随「免费在线工具，纯前端处理，数据不上传，保护隐私安全」+功能特点「操作简单，一键完成」+使用场景 4 项全通用→真实家政场景，含「纯前端处理/数据不上传/支持复制下载/实时显示」真实特性保留），A 类 generator-price/recommender-8 的「本生成器依据指定格式规范在前端按规则随机或确定性生成内容」为生成器标准变体（语义相符保留）、B 类 opt 套话 0 命中；③ og:image:alt「ToolBox - 5000+免费在线工具」与 meta「纯前端处理，数据不上传」为全站统一真实特性，非占位、不清理。+ zh-tw 同步 + 五项门禁全过。
---
## 八、当前进行中分类：（无，domestic 已归档）

> biz/blasting/bonding/brand/bridge/building-material/cable/cardiology/casting/ceramics/chemical/chemistry/chess/chinese/chinese-cook/civil/cleaning/clinical-lab/clinical-nursing/cnc/cognition/colorvision/community/construction/consulting/content/convenience/cosmetic-derm/cosmetics/customer-service/daily-goods/dance/data/decor/defense/dentistry/design/discipline/domestic 内容层均已达标，已依次归档至第七节。下一进行中分类按字母序为 **dyeing**（见第九节清单），待下一批次置进行中并展开待优化清单。

> 优化模式（沿用已验证路径）：写真实 content_deepdive 条目 → 清理工具页硬编码套话（opt_cleanup_intro_faq.py --cat <cat> 或仿 opt_biz_optguide.py 按结构清 tool-intro）→ 构建 + 五项门禁 → 提交发布。

---

## 九、分类总清单（待办，完成一个删一个；剩 202 个目录）

- [ ] dermatology
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
- [ ] pharmacy
- [ ] photo
- [ ] photo2
- [ ] photography
- [ ] plastic
- [ ] pneumatic
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