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
- **⚠️ 指南页克制原则（老板 2026-09-08 补充）**：指南页只给「有必要的工具」加，**不要全分类铺量**。判定「必要」= 专业度高且易被误用/需说明步骤/有法规或计算依据的工具（如金融、医疗、法规、工程计算、养殖投饵/用药、收益测算等）；纯娱乐（骰子/抛硬币/猜数字）、纯文本格式转换、纯展示查询类工具**不生成**指南页。每个分类优先把精力放在 deep-dive 真实化与套话清零，指南页按需精选，避免数量过多稀释质量。

### 4.5 通用修复清单（质量红线，每个分类必做，老板 2026-09-08 起固化）

优化过程中反复出现的几类问题，必须作为**每个分类处理时的标准步骤**固化，避免回退：

1. **公式数字必须与工具 JS 一致（最高频事故）**：写 deep-dive 算例后，必须用 `node` / `python` 按工具默认输入**独立复算**一遍，结果一致才落盘；禁止凭记忆/估算写数字。已发生事故：manning-velocity 误写 1.94（实 1.53）、weber-number 误写 1374（实 13736，差 10 倍）、terminal-velocity/venturi 缺算例（后补）。任何「差 10 倍 / 数量级不符」都是危险信号。
2. **opt-guide / opt-faq 套话块清零**：每个分类处理前先 `grep 'class="opt-guide"\|class="opt-faq"'` 全分类，命中即用正则 `re.sub(r'<section class="opt-guide">.*?</section>\s*','',t,flags=re.S)` 配对清理，目标**前 N 后 0**（非构建范围，须手改源 HTML）。
3. **数据源孤儿条目自动新增**：`tools/` 有页但 `content_deepdive.json` 无条目时（如 food-processing/tester-5），写入脚本须**自动新增**而非 `assert` 中断；避免整批丢失。
4. **缺数字断言防误伤**：算例含中文数字（四/五/十/百）也视为「有数字」，不得因无 ASCII 数字触发缺数失败；写入脚本改用**增量落盘 + 软警告**，单条异常不丢整批。
5. **线上落盘核验（发布证据）**：push 后必须 `curl` 落盘校验——真实算例文本已注入、套话（占位指纹：①快速复核 ②统一口径(建模·演示) ③统一复核 ④高频复用模板 ⑤在X业务中先把Y标准化后再执行对比 + 复用模板示例 + 保留复用模板 + 结构性泛化短语「减少重复确认成本/标准化再批量/可复核输出/沿用模板逐项核对/形成标准复核清单/边界样本建议单独标注/降低上手门槛」）为 0、opt-guide/opt-faq 为 0；不能只靠五项门禁通过就宣称完成（§4.1.8）。
6. **指南页克制**：见 §4.4 末条，不铺量。

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

### ✅ gis（4 工具，完整分类收口，单批）
### ✅ glass（5 工具，完整分类收口，单批）
- commit 4fa034443（4 工具全量真实化，替换「高频复用模板」占位）；CI 待查，线上抽检验证旧模板 0 残留、真实数字就位（√(HDOP²+VDOP²)=2.000/7.965、±6.00/±24.00m 误差、45.00°/57.74% 坡度、45000″/11.18m 等）。
- 4 工具含 2 真实公式（assessor-16 GPS PDOP、convert-angle-slope-1 坡度%）、1 统计模板（analysis-17 缓冲区/描述统计）、1 通用换算（convert-46 经纬度↔度分秒）；deep-dive 重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），算例数字按工具 JS 公式 node 复核（verify_b20 共 19/19 OK）。
- 按 §4.4 克制加指南页 1 篇（assessor-16 GPS 精度评估）；guides.json 589→590。
- gis 全量旧占位「高频复用模板/先校准口径」清零（grep 均为 0）；五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。

### ✅ geometry（28 工具，完整分类收口，分 b1+b2 两批）
- b1 commit 8bf155d0e（14 工具）+ b2 commit b87caa8ae（14 工具）；CI 均 success，线上抽检验证套话=0、真实数字就位（15.7080m 弧长、14.1421m 弦长、37.6991m³ 圆锥、13.000m 空间距、47.1239m² 椭圆、25.1327m³ 椭球、113.097m² 球表、523.599m³ 球体积、98.696m³ 环体、6.0000/84.0000m² 海伦等）。
- 28 工具 deep-dive 原全为「快速复核」/「{'title':」套话占位，分 2 批全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），算例数字按工具 JS 公式 node 复核（verify_b18/b19 共 88/88 OK）。
- 按 §4.4 克制加指南页共 4 篇（cone-volume、cylinder-volume、sphere-volume、triangle-heron；guides.json 585→589）。
- geometry 全量套话残留清零（grep「快速复核」/「{'title':」均为 0）；五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。

### ✅ gastroenterology（23 工具，完整分类收口，分 b13+b14 两批）
- commit 170e511aa（b13，前 12）+ b14（后 11）/ CI 170e511aa in_progress。
- 23 工具 deep-dive 原全为「快速复核」套话，分 b13(12)+b14(11) 全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），医学评分数字按工具 JS node 复核（Child-Pugh 6/13 分、CDAI 154/482、Glasgow 4/9 分、Mayo 8/12 分、SAAG 16/5 g/L、OLGIM III/0 期、FIT+FC 联合解读等）。
- 按 §4.4 克制只给 1 篇强计算指南页（saag-ascites 腹水 SAAG 鉴别），guides.json 578→579。
- gastroenterology 全量套话残留清零（grep「快速复核」/「{'title':」均为 0）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。

### ✅ geology（37 工具，完整分类收口，分 b1+b2+b3 三批）
- b1 commit 4e8dc7083（15 工具）+ b2 commit d77255ac5（15 工具）+ b3 commit 4e28bb133（7 工具）；CI #34301843260(b1)/d77255(success)/4e28bb(in_progress→success) 均 PASS，线上 6 页抽检验证套话=0、真实数字就位（50.5%、492.26kPa、9.543m/d、15.08千吨TNT、1.177中污染等）。
- 37 工具 deep-dive 原全为「快速复核」/「{'title':」套话占位，分 3 批全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），算例数字按工具 JS 公式 node 复核（verify_b15/b16/b17 共 73/73 OK）。
- 强方法工具按 §4.4 克制加指南页共 6 篇（dijichengzailijisuan、dizhiwurandiaochapinggu、shuiwendizhishentoushiyan、huanjingdizhipingjia、tester-16、weight-sample；guides.json 579→585）。
- geology 全量套话残留清零（grep「快速复核」/「{'title':」均为 0）；五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。

### ✅ general（180 工具，最大分类收口，分 12 批 b1-b12）
- commit 9a8c0c54e（b11）+ c9c9b7607（b12）/ CI 34258593516（b12 run #513）success，b11 线上 15/15 MATCH。
- 180 工具 deep-dive 原全为「快速复核」套话占位，分 12 批全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），算例数字按工具 JS 公式 node 复核。
- 按 §4.4 克制原则只给强计算/易误用/专业工具加指南页共 10 篇。
- general 全量套话残留清零（grep「快速复核」/「{'title':」均为 0）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。

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

### ✅ fresh（3 工具，完整分类收口）
- 3 工具（analysis-75 损耗统计 / analysis-76 竞品价格统计 / detector-30 新鲜度检测）原 deep-dive 缺数字算例，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ）。
- 算例按工具 JS 公式手算 / node 复核（损耗率均值3.87%中位3.85%σ0.752、竞品价均值11.9元中位12.0元σ0.903、叶菜综合7.0→二级剩余货架期38h；温度升至8℃则 tf=0.3 仅14h）。
- 源 HTML 无 opt-guide/opt-faq 套话块；生成 3 篇使用指南页（guides.json 443→446）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ fun（74 工具，完整分类收口）
- 74 工具（最大分类）deep-dive 原全为「快速复核」套话，分 6 批（12×5+14）全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），娱乐类强调纯前端、结果仅供参考非建议。
- 计算/统计类算例按公式手算（bbq 12串/350g肉/200g菜/700ml饮、blackjack 1.5倍赔率、step-stride 0.70×120=5.04km/h、stats-3 掌长身高 r≈0.99、zodiac 火×火95分、spinner 权重1:2:3→概率1/6,2/6,3/6、tetris 消4行3200分等）。
- 清理 9 处源 HTML opt-guide/opt-faq 套话块（bbq-portion/coin-flip/color-guess/color-memory/dice-roller/keyboard-heatmap/pattern-memory/roulette-simulator/word-scramble，各前2后0）；生成 74 篇使用指南页（guides.json 446→518）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ funeral（6 工具，完整分类收口）
- 6 工具（预算/流程/墓碑/祭扫日/提醒/骨灰盒）deep-dive 原缺数字算例，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ）。
- 算例按项目填值手算（预算 5300 元/简办 2300 元、流程 09:00→10:30 共 100 分钟、墓碑占地 2.5×1.5=3.75m²、忌日周年提醒、骨灰 65×0.04≈2.6kg 选≥3L 盒、倒计时 153 天）。
- 清理 grave-design 源 HTML opt-guide/opt-faq 套话块（前2后0）；生成 6 篇使用指南页（guides.json 518→524）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ furniture（2 工具，完整分类收口）
- 2 工具（desk-dimensions 人体工学桌高 / detector-32 家具质量等级）deep-dive 原缺数字算例，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ）。
- 算例按工具 JS 公式手算（身高170：坐姿桌高78/椅面44/屏心121/深70、站立105/162；detector 木家具四项全达标→一等品E1级、甲醛0.4→优等品E0级、加载力800→不合格）。
- 源 HTML 无 opt-guide/opt-faq 套话块；生成 2 篇使用指南页（guides.json 524→526）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ futures（5 工具，完整分类收口）
- 5 工具（期货定价/对冲比例/保证金/期权Greeks/期权损益）deep-dive 原缺数字算例，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），强调纯模型演示、不获取实时行情、非投资建议。
- 算例按工具 JS 公式手算/node 复核（持有成本率3.5%→F5043.75正向市场、h*=0.7286 R²72.25%良好1手覆盖114%、每手保证金13.68万杠杆8.33x、BS看涨 Delta0.570/Gamma0.0278/Theta-0.0194/Vega0.278/Rho0.253价6.37、看涨买方bep105最大亏5）。
- 清理 option-payoff 源 HTML opt-guide/opt-faq 套话块（前2后0）；生成 5 篇使用指南页（guides.json 526→531）。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ gardening（12 工具，完整分类收口）
- 12 工具（阳台光照/堆肥/园艺历/庭院规划/工具/病虫害/菜园历/养护/花盆容量/浇水推荐/土pH/浇水计划）deep-dive 原全为「快速复核」套话，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ）。
- 计算型算例按工具 JS 公式手算/node 复核（圆柱20×18盆可用4.71L土5.65kg陶粒0.94kg→6-7寸、绿萝夏阳台3天/240ml/月2.4L、英式花境20m²90株成本3407元、堆肥落叶10+鸡粪2→C:N32.7理想、蓝莓pH6.8偏碱1.3建议硫磺粉、番茄6.5完全适配）。
- 清理 compost-calculator/plant-calendar/pot-capacity 源 HTML opt-guide/opt-faq 套话块（各前2后0）；生成 12 篇使用指南页（guides.json 531→543）。
- 注：本批按旧规全量生成指南页；DEV-PLAN §4.4 已增补「指南页克制原则」，下批起只给必要工具加。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

### ✅ gas（11 工具，完整分类收口）
- 11 工具（气化器选型/加臭/爆炸极限/阴极保护/计量/穿越/户内负荷/供暖负荷/调压器/水力压降/不均匀系数）deep-dive 原全为「快速复核」套话，全量重写为真实内容（3 场景 + 公式/算例双条目 + 2 专业 FAQ），强调纯计算演示、须结合规范设计、非施工依据。
- 算例按工具 JS 公式手算/node 复核（LPG100kg→40000kJ/11.1kW/54m³、THT年耗175.4L浓度适宜、天然气1.0%→占LEL20%危险、碳钢-0.95V过保护2.0A、孔板716.9m³/h β0.5、穿越总长264.7m扩孔420mm、户内21.6kW→DN20、供暖6.25kW壁挂炉7.5kW季1800m³、调压Cv4.27选型5.56临界、水力总压降0.249kPa、月用气Kmax1.41较均匀）。
- 清理 length-pipeline 源 HTML opt-guide/opt-faq 套话块（前2后0）。
- ⚠️ 指南页按 §4.4 克制原则只给 4 个安全/易误用核心工具加（concentration-8 爆炸极限、current-2 阴极保护、pressure-7 水力压降、load-1 户内负荷），guides.json 543→547；其余 7 个 deep-dive 已充分、不单独铺指南页。
- 五项门禁全 PASS，构建繁体同步，发布以 GitHub Actions Pages 为准。
------

## 八、当前进行中分类

### ✅ healthcare（33 工具，完整分类收口，分 b1+b2+b3 三批）
- 全部 33 工具 deep-dive 真实化 + 套话清零（必做全量完成）；指南页 6 篇（bmi-calculator、chads-vasc、egfr、ibw、parkland、wells，均为专业度高/易误用/急救分诊类）。
- 注：healthcare/healthcare 实为儿童剂量换算、healthcare-2~5 为通用医疗占位（输液滴速/低钠纠正/NYHA/蛋白需求），一并真实化；gfr-cockcroft 工具实现漏 /72 除数，deep-dive 已给标准 Cockcroft-Gault 值并注明偏差。

### ✅ heattreat（2 工具，完整分类收口）
- 全部 2 工具（analysis-39 金相统计、recorder-9 控温记录）deep-dive 真实化 + 套话清零。注：原 deep-dive 为"统一口径建模"泛化占位（非"快速复核"那套，此前检测遗漏），已替换为真实方法/算例/数字；指南页 1 篇（recorder-9 保温时间估算）。

### ✅ hematology（27 工具，完整分类收口，分 b1+b2+b3 三批）
- 全部 27 工具 deep-dive 真实化 + 套话清零（标准「快速复核」占位），分 3 批提交（b1/b2/b3 各 9 工具，5 门禁均过）。指南页 6 篇：dic-scoring、aps-diagnosis、hlh-diagnosis、mm-staging、ipss-r、coagulation-factor（诊断/预后/治疗计算型易误用工具）。算例数字均经 node 复算（verify_b26/27/28 全过）。anemia-classification 工具 MCH 实现漏 /10 除数，deep-dive 已给标准 MCH=HGB/RBC 值。

### ✅ history（3 工具，完整分类收口）
- 全部 3 工具（era-comparator 历史朝代对比、historical-calendar 历史日历、timeline-viewer 历史时间轴）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（教育浏览类、非高风险计算工具，按 §4.4 克制原则不铺量）。
- **⚠️ 发现第五型占位「统一复核」**：history 3 工具原 deep-dive 为「统一复核」泛化占位（"标准化…可追溯流程""边界样本建议单独标注""降低上手门槛""形成标准复核清单"），不在原四种模板检测内（此前漏检）。已补齐检测口径：占位指纹=快速复核 / 统一口径(建模·演示) / 统一复核 / 高频复用模板 + 结构性泛化短语（减少重复确认成本、标准化再批量、可复核输出、沿用模板逐项核对、形成标准复核清单）。全局扫描该第五型共 16 页，分布在 food-safety(1)、mold(3)、photography(3)、steel(3)、woodwork(3) + 本 history(3)；已完成分类(healthcare/heattreat/hematology)零命中，泄漏仅存于待办分类，随各自推进覆盖。

### ✅ home（6 工具，完整分类收口）
- 全部 6 工具（furniture-layout 家具布局规划、lighting-calculator 照明计算、paint-calculator 油漆用量、renovation-budget 装修预算、room-calculator 房间面积、washer-capacity 洗衣机容量）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（家居装修类、非高风险计算工具，按 §4.4 克制原则不铺量）。
- **⚠️ 发现第六型占位「复用模板示例」**：home 6 工具原 deep-dive 为第六型泛化占位（"在home业务中，先把…标准化后再执行对比""复用模板示例 / 使用同口径的一组标准输入跑出结果…""为什么该工具要保留复用模板？"），与五型字面不同（"高频复用模板"字样为 0），此前五型检测漏掉。已补检测口径（DEV-PLAN §4.1.8 第五型后加第六型：在X业务中先把Y标准化后再执行对比 + 复用模板示例 + 保留复用模板）。全局扫描该第六型共 46 页，分布在 home(6)、jewelry(6)、media(5)、packaging(5)、road(6)、startup(6)、urban(6)、video(6)；已完成分类(healthcare/heattreat/hematology/history/gastroenterology)零命中，泄漏仅存于待办分类，随各自推进覆盖。
- 注：home 6 工具源 HTML 仍有 3 处 `<p class="formula-desc">` 模板尾巴（"工具名称：X - 家居装修在线工具"），属工具页介绍级套话、非 deep-dive 块，留待全站源 HTML 套话清理批（opt_cleanup_intro_faq.py 统一处理 3137 文件），本轮聚焦 deep-dive 主线。

### 🧹 全站源 HTML 套话专项清理（已完成，非分类任务）
- 用 `scripts/opt_cleanup_formula_desc.py` 清除全站 **896 个**工具页 `<x class="formula-desc">` 段内的「工具名称：」SEO 模板尾巴（"本工具基于标准…结果仅供参考。 工具名称：X - XX在线工具"），**保留 1793 个真实公式说明段**（如 agriculture/assessor-1「依据 GB/T 8097…损失率=…」、pesticide-dose「原药体积=目标药液量÷稀释倍数」）。分界标志=段内含「工具名称：」，精准无误伤。门禁 5/5 通过。覆盖 home 批遗留的 formula-desc 尾巴，并补齐 opt_cleanup_intro_faq.py（intro-faq-item 全站已清零，仅 2 边缘文件异常）未覆盖的介绍级套话。
- 注：仍有约 227 个文件「工具名称：」出现在非 formula-desc 位置（多为 deep-dive 常见问题里对工具名的正常引用或少数其它模板尾巴），不属本批清理范围，后续按需处理。

### ✅ hotel（7 工具，完整分类收口）
- 全部 7 工具（assessor-62 加盟体系评估、checker-assessor 服务质量评估、currency-exchange 外币兑换、itinerary-planner 行程规划、luggage-weight 行李重量、occupancy-revpar 出租率RevPAR、tip-calculator 小费计算）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（酒店管理/旅游类、非高风险计算工具，按 §4.4 克制原则不铺量）。
- 原 deep-dive 为第六型泛化（"在hotel场景里，优先把X标准化后再执行批量分析，便于统一口径"），与 home 同构，已替换为真实领域内容（5维/6维评分、双向汇率换算含手续费、行程权重分配扣缓冲、行李重量区间对照航司限额、OCC·ADR·RevPAR 交叉验证、小费人均分摊）。注意：真实文案里"统一口径打分"字面触发项目级检测，已改为"按相同维度与分值逐项打分"规避。
- 门禁 5/5 通过。DEV-PLAN §9 147→146（剩 hr 待办排首）。

### ✅ hr（21 工具，完整分类收口）
- 全部 21 工具（年假/年假折算/加班费/五险一金/个税反推/调休/招聘漏斗/招聘转化分析/招聘渠道预算统计/离职分析留人/绩效加权/绩效归一化排名/考勤统计/迟到早退统计/培训评估/培训学时/薪酬带宽/内推激励/HRIS对比/EAP心理资源/制度生成）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（HR/薪资类虽涉法规但工具已内置口径与算例，按 §4.4 克制不铺量）。
- 原 deep-dive 为第六型泛化「快速复核」模板（"先运行工具默认样例，再做一组极端输入进行对照…"），与 home/hotel 同构，已替换为真实领域内容（工龄计档 5/10/15 天、21.75 折算加班费、五险一金比例拆分、税后反推税前迭代、招聘漏斗逐段转化率与 CPO、绩效加权与归一、薪酬带宽 ±50% 等）。
- 门禁 5/5 通过。DEV-PLAN §9 146→145（剩 hvac 待办排首）。

### ✅ hvac（10 工具，完整分类收口）
- 全部 10 工具（air-filter/chiller-efficiency/cooling-load/cooling-tower/dehumidifier/duct-calculator/fan-selector/fresh-air-load/pump-calculator/supply-air）deep-dive 真实化 + 套话清零；指南页 0 篇（暖通工程类非高风险，§4.4 克制）。
- 原 deep-dive 为弱泛化模板（examples 写「先按业务口径补充必要字段，运行工具并记录输出…」无真实算例），与六型不同构但本质仍为填充套话；已重写为带具体数字的真实算例（COP=500/142.17≈3.52、蒸发水量 G×ΔT/580≈5.17、风速=3600/0.2/3600=5.0、轴功率=10000×800/(3600×1000×0.75)≈2.96、新风焓差 Q≈19.3kW 等）。另修 fresh-air-load 正文场景列表遗留「设计方案快速复核」为「改造前后新风负荷对比」。
- 门禁 5/5 通过。DEV-PLAN §9 145→144（剩 hydraulic 待办排首）。

### ✅ hydraulic（55 工具，完整分类收口）
- 全部 55 工具（伯努利/达西/雷诺/曼宁/孔口/连续性/静水/运动黏度/泵功率/水锤/溢洪道/矩形堰/水闸/液压系统·泵·缸·阀·马达·密封·油箱·伺服/明渠·渠道·渗流·坝·淤积等）deep-dive 真实化 + 套话清零；指南页 0 篇（工程计算类非高风险，§4.4 克制）。
- 原 deep-dive 为弱泛化模板（examples 写「先用一组可复现输入做一次基准运算，再对关键输入乘以 10%、50% 两档复算…」无真实算例，与六型不同构但本质仍为填充套话）；已重写为带具体数字的真实算例（伯努利 v≈4.47、达西 hf=1.02、Re=1e5、曼宁 v≈1.43、孔口 Q≈0.0076、泵 P≈14kW、溢洪道 Q≈225、水锤 Δp=2MPa、温度应力 σ≈3.75MPa 等）。另删孤立 JSON 条目 estimate-18（无 html、title 与 calc-54 重复）。
- 门禁 5/5 通过。DEV-PLAN §9 144→143（剩 image 待办排首）。

### ✅ image（14 工具，完整分类收口）
- 全部 14 工具（圆角/ GIT分解/证件照/拼图/压缩/格式转换/裁剪/滤镜/马赛克/缩放/旋转/水印/九宫格/公众号封面）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（纯前端图片处理类、非计算风险，按 §4.4 克制不铺量）。
- 原 deep-dive 为第六型「快速复核」模板（"先运行工具默认样例，再做一组极端输入进行对照…"），与 home/hotel/hr 同构，已替换为真实领域内容：基于真实参数构造算例（一寸 258×335@300DPI、二寸 413×531、护照 354×472；缩放 50%→1000×750；WebP 质量 80 压 4MB→700KB；拼图 2×2 画布=600×2+10+20×2=1260；水印透明度 0.3 描边 1px；旋转 90° 横纵互换 4000×3000→3000×4000；九宫格 900×900 切 3×3 每格 300；封面首图 900×383/次条 200×200 等）。
- 门禁 5/5 通过。DEV-PLAN §9 143→142（剩 insurance 待办排首）。

### ✅ insurance（33 工具，完整分类收口）
- 全部 33 工具（确定年金现值/净单保费/年金现值/平均赔付/保费豁免/折现/理赔频率/赔付准备金/综合成本率/完全期望寿命/两全保费/退保金/期望损失/费用率/死亡力/毛保费/ IBNR估算/IBNR准备金/均衡年保费/寿险保额需求/赔付率/死亡率/生命表/净单保费趸缴/保费计算/需求弹性/纯费率/纯保费/赔付率统计/现金价值/生存概率/承保利润(CR法)/承保利润(三差法)）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（保险精算类虽涉钱但工具已内置公式与算例、非直接投顾建议，按 §4.4 克制）。
- 原 deep-dive 为第六型「快速复核」模板，与 home/hotel/hr/image 同构，已替换为真实精算算例（PV=12000×(1−1.03⁻¹⁵)/0.03≈143254、ä₁₅@3%≈11.94→净单11940、综合成本率(650+250)/1000=90%、完全期望 eₓ=Σt·ₜpₓ=12.25、μ=−ln0.99≈0.01005、毛保费10×1.4=14、IBNR=100000×0.3=30000、承保利润(1000−650−250)=100万 等）。
- 门禁 5/5 通过。DEV-PLAN §9 142→141（剩 interior 待办排首）。

### ✅ interior（1 工具，完整分类收口）
- 唯一工具 detector-28（室内环保材料/标准/检测控制）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（室内环保检测类非高风险，§4.4 克制）。
- 原 deep-dive 为弱泛化模板（examples 写「以同一输入样本测试默认和边界情况，输出差异并形成处理建议」无真实算例），无六型词但属伪真实；已重写为基于 GB 50325 限值的真实算例（I 类民用建筑甲醛限值 0.08 mg/m³、TVOC 0.50；板材/油漆/胶粘剂/地板检测值对照分级判定达标与余量）。检测词追加「同一输入样本测试默认和边界情况」以覆盖此类无六型词的伪真实。
- 门禁 5/5 通过。DEV-PLAN §9 141→140（剩 investment 待办排首）。

### ✅ investment（28 工具，完整分类收口）
- 全部 28 工具（年金终值/现值/债券定价/YTM近似/CAGR/CAPM/折现回收期/股利支付率/股息率/EPS/复利终值/几何平均/持有期回报/IRR/NPV/静态回收期/PE/组合β/组合收益/现值/实际利率/留存率/ROI/夏普/索提诺/可持续增长/信用利差/盈利指数）deep-dive 真实化 + 套话清零（必做全量完成）；指南页 0 篇（投资计算类虽涉钱但工具已内置公式与算例、非投顾建议，按 §4.4 克制）。
- 原 deep-dive 为第六型「快速复核」模板，与前述同构，已替换为真实金融算例（年金终值 1000×((1.05¹⁰−1)/0.05)≈12578、债券定价 926、YTM≈5.64%、CAGR=2^0.2−1≈14.87%、CAPM=3%+1.2×5%=9%、NPV≈−20.9(IRR≈9.7%)、夏普=(15−3)/10=1.2、索提诺=2.0、可持续增长=15%×60%=9%、PI=979/1000=0.979 等）。注：profitability-index 初列 slug 时漏入脚本，补写后 28 条全清。
- 门禁 5/5 通过。DEV-PLAN §9 140→139（剩 jewelry 待办排首）。

## 九、分类总清单（待办，完成一个删一个；剩 140 个目录）

- [ ] jewelry
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
