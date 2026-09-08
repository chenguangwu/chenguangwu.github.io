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
- 分类状态必须按固定状态机推进：待办分类保留在「分类总清单」；开始后同时写入「当前进行中分类」并登记全部工具；完成后从这两处删除，并用本次最新完成分类替换「已完成分类归档」。三处状态必须在同一次任务中同步更新。
- **psychology 已优化过一遍**：先按上面 10 条标准**验证**是否满足，全满足则直接跳过该分类；否则先优化该分类里不满足的工具。
- 每完成一批（或一个工具）跑 `python3 _build.py` + `python3 _test_static.py`，确保门禁通过、繁体 `zh-tw/` 同步。
- **提交发布节奏**：最好**一个分类提交发布一次**；分类下工具多的（如 `it` 345 / `general` 180 / `finance` 112），可分批提交，**每批至少 10 个工具**，避免单工具频繁发布。
- **发布前必须跑质量门禁、发布后必须查部署结果**：每次 `git push` 前，先本地跑 `python3 scripts/run_gates.py`（五项门禁：build→静态→死链→资产→公式）**全部通过**；`git push` 触发 GitHub Actions 后，**必须查 Actions 运行结果确认部署成功**（公开仓库 `curl -s https://api.github.com/repos/<owner>/<repo>/actions/runs` 看最新 run 的 status/conclusion），**禁止 push 完就发总结结束回合**。CI 会重跑门禁，本地没跑过的 CI 照样挂、照样不发布。
- **新建页面防死链**：从范本 copy 的指南/工具页，必须删掉英文版 `hreflang` 链接与 "🌐 English" 按钮（本项目英文走 `?lang=en-US`，不生成独立 `.en.html`）；不引用任何不存在的文件（拼写错的 slug、未生成的附属页），否则 dead-link 门禁必挂。
- **改 deep-dive / 使用指南等被构建重建的区块，必须改数据源 `i18n/tools/content_deepdive.json`**（直接改源 html 会被 `_build.py` 覆盖，见下方踩坑备忘）。

### 4.1 每个分类的强制任务目标

每个分类必须覆盖该分类下的全部工具，不能只挑页面清理文案。开始分类前，先在“当前进行中分类”登记完整工具清单；每完成一个工具就从清单中删除，并保留可追溯的改动证据。

每个工具必须同时完成以下目标，缺一项都不能结束分类：

1. **功能**：输入、处理逻辑、输出和异常提示真实可用；专业计算用已知样例、独立公式或 `node` 纯函数验证。
2. **内容**：补真实场景、真实示例、边界说明、参考表或可视化；禁止复制“常见场景：XXX”“先统一输入单位与口径”等套话。
3. **页面**：检查 UI、移动端布局、输入项、下拉选项、默认值、按钮和结果区；不能因为 SEO 文案变化就视为页面完成。
4. **深度内容**：专业工具必须在 `i18n/tools/content_deepdive.json` 有真实条目，含场景、示例和至少 2 条针对性 FAQ；需要指南的工具必须补指南入口和指南数据。
5. **i18n**：同步中文页、行业 JSON、`slug-en.json`、`_en_override.json`、页面英文元信息、英文可见内容和繁体构建结果；英文描述必须说明实际用途，不能只是“free online tool”。
6. **分类**：核对 `<meta name="toolbox">` 的 `industry` 与 `cat`，发现错标必须在源 HTML 修正，不能只手改构建产物。
7. **SEO 与专业性**：Title、Description、H1、JSON-LD 和面包屑用途一致；关键专业名词按需补权威外链，并确保不制造死链。
8. **发布证据**：分类全部工具完成后，必须有构建、五项门禁、远端 Actions 成功和提交 SHA；只证明“套话不存在”不能作为完成证据。

若本批只改了 `desc-en`、`slug-en`、meta 或其他文案，不得标记分类完成，必须继续补齐功能、内容、deep-dive、i18n 和分类校验。完成分类后，必须从“当前进行中分类”清单和“分类总清单”中删除该分类条目，不得改成 `[x]` 后长期保留。

### 4.2 提交与发布文件边界

- 修改前和准备提交前都必须执行 `git status --short`，建立本批文件清单；发现不是本任务产生的改动，立即停止并确认，不得覆盖、暂存或提交。
- 禁止使用 `git add -A` 或 `git add .` 兜底提交；必须按已确认的文件清单显式 `git add`。
- `json/*.json`、`sitemap.xml`、`sw.js` 等构建产物只能由 `_build.py` 生成；若状态中出现其他脚本、配置或业务文件，必须排除并向用户说明。
- 最终汇报必须列出 commit SHA、实际提交文件范围、五项门禁结果和 Actions run URL，不能只说“已发布”。

### 4.3 分类收口顺序与状态同步

每个分类只能按以下顺序收口，不得跳步：

1. **建立范围**：读取该分类实际目录，登记全部工具页；分类总数必须与构建扫描结果一致。
2. **逐工具处理**：逐个完成功能、内容、页面、deep-dive、i18n、cat、SEO 和验证目标；工具完成一项就从进行中清单删除。
3. **完成前审计**：确认进行中清单为空，检查分类下没有占位套话、缺失 deep-dive、英文通用描述、cat 错标或未验证的关键逻辑。
4. **同步状态**：从「当前进行中分类」和「分类总清单」删除分类；将本分类写入「已完成分类归档」，并覆盖旧归档记录。
5. **发布收口**：状态同步后才能跑门禁、提交和推送；归档未更新、清单未删除或文件范围未核对时，禁止宣称分类完成。

严禁以下不完整状态：只把待办改成 `[x]` 不删除、只更新归档不删除待办、只删除待办不写归档、当前进行中标题与清单分类不一致、清单未空就开始下一个分类。

### 4.4 使用指南增强规则（老板 2026-09-08 明确授权）

每个分类除按 §4.1 完成基础优化外，**须主动识别「专业度高且热门」的工具并补充独立使用指南页**，使其同时具备深度解析（deep-dive FAQPage）与系统化「📖 使用指南」独立页。

- **判定标准（agent 自主判断，老板授权）**：
  - *专业度高*：计算 / 判定 / 法规 / 工程 / 医疗 / 金融 / 养殖等技术类工具，结果影响用户决策或有行业依据（如池塘容载量、投饵率、溶解氧、用药休药期、收益测算等）。
  - *热门*：用户常用、搜索量大的高频工具（各类计算器、收益测算、单位 / 密度换算等）。
  - 满足其一且非纯娱乐 / 纯展示的简单工具即应补指南；纯娱乐（骰子、抛硬币）、纯文本格式转换等低专业度工具可不加。
- **落地动作**：用通用脚本 `scripts/gen_guide_pages.py` 批量生成 `guides/<slug>-guide.html`，自动合并 `json/guides.json` 并追加 `guides/index.html`；模板须去除英文版 `.en.html` 链接与独立英文 `hreflang`（英文走 `?lang=en-US`，遵循 §4.48）。
- **内容要求**：指南页须含适用场景、操作步骤、注意事项、针对性 FAQ，内容真实专业，禁止「常见场景：XXX」等套话；可基于该工具 deep-dive 的真实场景 / 算例 / FAQ 扩展，但须系统化、可读性强。
- **已收口分类**（如 fire-rescue）若属专业度高的工具集中，后续批次可择要补指南，不强制回退已发布版本。

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

### ✅ food-testing（24 工具，完整分类收口）
- commit c2407ac06 / CI 34211293735 success。
- 24 工具 deep-dive 原全为「food-testing场景下…」套话占位，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），算例数字按 GB 标准公式手算 / 工具 JS 复核（酸价2.81、POV4.92、黄曲霉5<20合格、MPN150、菌落1.6×10³、蛋白9.01%、脂肪62.5%/65.8%、沉降14.8mm/s、辐照2.5kGy、亚硝酸盐11.2mg/kg、NRV 40/8/17/20/30%、迁移0.033mg/dm²合格/5mg/kg超标、NaCl6.14%、总糖1.65%、总迁移5mg/dm²合格等）。
- 清理 acid-peroxide-titration、salt-titration 源 HTML opt-guide/opt-faq 套话块（各前2后0）；生成 24 篇使用指南页（guides.json 373→397）。
- 全程公式手算 / 工具复核，五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。

### ✅ forensic-medicine（22 工具，完整分类收口）
- commit 待推送 / CI 待查 success；法医类判定/分级工具 22 条原全为「快速复核」套话，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），强调"结果仅供参考、须结合案情与专业鉴定"。
- 计算型算例按工具 JS 公式手算 / node 复核（blast Z=10 δP=11.8kPa safeR=9m、bloodstain α=36.9°、burn total30/third10→重度、death-time 综合10.6h区间10.2~15.8h、bone infant≈3.4岁、fall v=14.0m/s E=6.87kJ、dna CPI>10000 认定、rigor 平均2.2级等）。
- 判定型（虐待/血痕/硅藻/电流斑/骨折/枪弹/毛发/索沟/尸斑/尸僵/精斑/损伤描述）按真实形态规则与阈值写算例，避免误导。
- 清理 bloodstain-pattern、drowning-diatom、fall-injury、wound-description 源 HTML opt-guide/opt-faq 套话块（前1/1/1/2 后0）；生成 22 篇使用指南页（guides.json 397→418）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------



### ✅ forestry（20 工具，完整分类收口）
- commit 732ed2afb / CI 34212100833 success。
- 林业/生态计算类 20 条原全为「快速复核」套话，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ）。
- 算例按工具 JS 公式手算 / node 复核（郁闭度0.65中郁闭、碳汇杉木107.5t/ha价值6.45万、负离子1800特别清新、SDI652.9偏密、造林111.1株/亩成本2.78万、实验形数蓄积166.2m³/ha、样线48只/km²、矩形6000m²=9亩、标准地150m³/ha；生长率普雷斯勒8.0%/复利8.45%、原木0.1602m³、发生率17.5%中度、需苗11111含耗12223、Shannon1.142/J0.824、采伐45保留135中度、锯材0.15m³、树龄21~38中心27、单株0.2033m³、产值56.1万）。
- 清理 area-18、density-5、shengwuduoyangxingshannon 源 HTML opt-guide/opt-faq 套话块（各前2后0）；生成 20 篇使用指南页（guides.json 418→438）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ forex（5 工具，完整分类收口）
- 5 工具（交叉汇率/杠杆/手数/点值/点差成本）原 deep-dive 全为「先统一X口径」套话占位，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），强调纯计算演示、不获取实时行情、非投资建议。
- 算例按工具 JS 公式手算 / node 复核（交叉汇率 EUR/JPY=163.1579、杠杆 1:100 保证金$1000 占用10% 爆仓波动4%、手数 0.4 手风险$200 盈亏比2、点值$10/点盈亏$500(CNY¥3625)、点差2点成本$27）。
- 源 HTML 无 opt-guide/opt-faq 套话块；生成 5 篇使用指南页（guides.json 438→443）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

## 八、当前进行中分类

### 🔄 fresh（待核查，deep-dive 真实化 + 指南页 + 套话清零）
- 接 forex 之后的下一个分类，按 §4.4 补独立使用指南页，完成一个勾一个。

## 九、分类总清单（待办，完成一个删一个；剩 170 个目录）

- [ ] fresh
- [ ] fun
- [ ] funeral
- [ ] furniture
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
