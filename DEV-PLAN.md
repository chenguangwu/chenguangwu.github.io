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
## 八、当前进行中分类：（无，cosmetic-derm 已归档）

> biz/blasting/bonding/brand/bridge/building-material/cable/cardiology/casting/ceramics/chemical/chemistry/chess/chinese/chinese-cook/civil/cleaning/clinical-lab/clinical-nursing/cnc/cognition/colorvision/community/construction/consulting/content/convenience/cosmetic-derm 内容层均已达标，已依次归档至第七节。下一进行中分类按字母序为 **cosmetics**（见第九节清单），待下一批次置进行中并展开待优化清单。

> 优化模式（沿用已验证路径）：写真实 content_deepdive 条目 → 清理工具页硬编码套话（opt_cleanup_intro_faq.py --cat <cat> 或仿 opt_biz_optguide.py 按结构清 tool-intro）→ 构建 + 五项门禁 → 提交发布。

---

## 九、分类总清单（待办，完成一个删一个；剩 213 个目录）

- [ ] cosmetics
- [ ] customer-service
- [ ] daily-goods
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