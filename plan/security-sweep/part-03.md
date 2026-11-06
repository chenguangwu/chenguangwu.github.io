## 十七、第八批：隐私面扫描（2026-11-04，只扫不改）

### 17.1 localStorage 全景与机制

- **根因级发现**：`js/tool-ux.js` 对所有工具页 `.container` 内的 `input/textarea/select`（排除 `password/file/hidden`）在用户输入后自动持久化，键名为 `tb_ux_<页面路径>#<字段id>`。全站约 **4705 页**默认带此行为，绝大多数页面**没有「清空本地数据」入口**。
- 另有约 90 页使用页面自有 `localStorage` 键（历史记录/清单/提醒），部分带清空按钮。
- 区分「存结果数值」与「存用户输入原文」：前者是计算参数，后者才是隐私面。以下分级只统计后者。

### 17.2 三档分级

| 档位 | 页数 | 口径 |
| --- | --- | --- |
| 高 | **594** | 健康/医学类 566 + 个人身份标识类 26 + 个人收入类 2 |
| 中 | **6** | 车辆身份/行程地点/宠物照护 |
| 低 | **约 4106** | 纯计算参数、偏好设置、公开数据 |

**高敏（个人身份标识，26 页，含清除入口标注）**：

| 页面 | 持久化内容 | 清除入口 |
| --- | --- | --- |
| legal/will-template-generator | 立遗嘱人姓名/身份证/住址/见证人 | 无 |
| rental/reminder-4 | 租客/地址/电话/租金/租期 | 有（自有键） |
| security/emergency-contacts | 联系人姓名/电话/备注 | 无 |
| wedding/seating-chart | 宾客姓名/分组 | 无 |
| life/stats-13 | 名单/价格 | 无 |
| funeral/memorial-date、grave-design | 逝者姓名/生卒年/碑文 | 无 |
| finance/vcard-qr | 姓/名/电话/邮箱 | 无 |
| design/initials-avatar | 用户姓名 | 无 |
| biz/team-roster-generator | 成员姓名名单 | 无 |
| text/text-extract-phones、biz/text-extract-emails | 批量手机号/邮箱原文 | 有 |
| it/sms-qr、phone-qr、email-qr、phone-parser、email-normalizer | 手机号/邮箱/短信正文 | 无 |
| finance/msisdn-validator、life/phone-lookup | 手机号 | 无 |
| elderly/reminder-time | 药名/剂量/服药时间 | 有 |
| ecommerce/cycle-15 | 客户姓名 | 有 |
| edu/chinese-zodiac、fengshui/birthday-analysis、life/age-in-days | 出生日期/时辰/性别 | 部分有 |
| pr/media-invite | 媒体联系人 | 无 |
| cleaning/staff-schedule | 员工姓名/区域 | 有 |
| tcm-diagnosis/tcm-medical-record、ten-questions、nephrology/manager-1 | 患者姓名/性别/年龄/病史/检验值 | 部分有 |

**高敏（健康/医学 566 页）**：health 40、fitness 37、ophthalmology 31、clinical-nursing 26、hematology 26、neurology 25、rheumatology 25、pediatrics 24、urology/psychiatry 24、cardiology/ent/nephrology/dentistry/dermatology 23、endocrinology/clinical-lab/gastroenterology 22、rehabilitation/beauty/tcm-diagnosis/tcm-pharmacy 21、medical 14、medical2 5 等。共同点：自动保存年龄、性别、身高体重、血压血糖、检验值、症状等健康数据。
（已剔除 `food-testing` 26 页与 `tcm-chemistry` 22 页：前者是食品检测参数、后者是方剂配伍参数，不含个人健康信息。）

**高敏（个人收入 2 页）**：`tax/progressive-income-tax`、`tax/effective-tax-rate`（输入工资/收入并自动持久化）。

**中敏 6 页**：`automotive/countdown-engine-oil`（车名+保养日期）、`automotive/detector-recorder-fuel`（车辆+加油/里程记录）、`usedcar/car-purchase-cost`、`usedcar/recorder-maintenance`（车辆+维保记录）、`hotel/itinerary-planner`（行程地点）、`pet/reminder-vaccine-deworming`（宠物名+疫苗日期+体重）。

### 17.3 URL 参数 / 分享链接

- 全站工具页 **0 处自动写 `location.hash` / `location.search` / `history.pushState|replaceState`**。
- 仅两个用户主动分享入口：`geometry/triangle-heron.html`「复制分享链接」按钮、`it/regex.html` 读取 `#regex=` 回填（只读不写）。
- 结论：不存在「输入即写 URL」导致进浏览器历史/Referer 外泄的路径。

### 17.4 依赖老化（只出清单，不升级）

15 个静态 CDN 标签 / 12 个库，全部固定确切版本 + SRI（15/15/0 不变）。

| 库 | 版本 | 结论 |
| --- | --- | --- |
| pdf.js | 3.11.174 | **有公开 CVE：CVE-2024-4367**（字体处理缺失类型检查 → 任意 JS 执行；修复版 4.2.67）。使用页：office/pdf-split、pdf-rotate（本地渲染用户 PDF） |
| mermaid | 10.9.8 | CVE-2026-71436 影响 `<10.9.8`，当前版本已在修复边界；另有 HTML 注入问题 10.9.6 已修 |
| bcryptjs | 2.4.3 | 2.4.3 为末版（2021 后基本停更），未检索到针对该版本的公开 CVE |
| markmap-lib / markmap-view | 0.17.2 | 版本较旧；未检索到针对该版本的公开 CVE |
| pdf-lib | 1.17.1 | 维护缓慢；未检索到针对该版本的公开 CVE |
| sql.js | 1.8.0 | 可用；未检索到针对该版本的公开 CVE |
| typescript | 5.3.3 | 落后主线（5.x 已有更新版本），无已知 CVE |
| less | 4.9.1 | 较新，未检索到 CVE |
| js-yaml | 4.1.0 | 4.x 已修复旧的 merge-key 问题，未检索到新 CVE |
| acorn | 8.19.0 | 维护中，无已知 CVE |
| d3 | 7.9.2 | v7 末版，无已知 CVE |

唯一建议单独立项升级的是 **pdf.js → ≥4.2.67**（若继续在本地渲染用户上传 PDF）。

### 17.5 共享导出回归（CSV 前缀不误伤）

抽 3 个不同行业页面，在页面上下文直接调用 `TBKit.util.exportCsv` 并截获 Blob 文本：

| 页面 | 首行 | 首列 | 误加前缀 |
| --- | --- | --- | --- |
| agriculture/fertilizer-calculator | `项目名称,数值,备注` | `项目名称` | 否 |
| daily-goods/shoe-size | `项目名称,数值,备注` | `项目名称` | 否 |
| finance/credit-card-interest | `项目名称,数值,备注` | `项目名称` | 否 |

3/3 通过，0 pageerror；正常中文/数字单元格未加 `'`。

### 17.6 处置记录（2026-11-04）

- **pdf.js CVE-2024-4367**：`office/pdf-split`、`office/pdf-rotate` 由 CDN 3.11.174 改为自托管 4.2.67（`vendor/pdfjs/4.2.67/`，legacy ESM，主文件与 worker 同版本）。4.x 官方仅发布 `.mjs`，`import` 语句无法挂 `integrity`，因此改为同源自托管（消除第三方供应链环节，强于 SRI）；文件与 npm 包、jsDelivr 双源 sha384 一致。
  真机实测：单页 PDF 拆 1 页、6 页 PDF 拆 `2,4-5` 得 3 页且文本逐页正确；旋转 90/180/270/0 角度与页面朝向正确、文本无损；0 pageerror。
- **tool-ux 自动持久化**：新增「清空本地数据」浮动入口（按当前页路径前缀删除 `tb_ux_*` 与旧版 `tb_uxp_*`，不触碰其它页），并支持 `data-no-persist`（`<body>` 或控件级）；命中时不回填、不保存，并清除历史遗留键。29 个身份/医疗高敏页（遗嘱、急救联系人、婚宴座位、租客、名单生成、药名提醒、通讯录/电话/邮箱类、中医病历等）已加 body 属性。健康页不改行为，仅依赖统一入口。

### 17.6.1 线上真机复核：pdf.js 4.2.67 自托管（2026-11-05）

- 线上 commit：`d7fa6da8d6`（含 pdf.js 4.2.67 自托管、`5a7becf407` 的 `js/common.js`、`e6712423d5` 的守卫用例）。
- 复核方式：headless Chrome 直接访问 `https://chenguangwu.github.io`（非本地），全新浏览器上下文（无旧 SW 缓存），用 `page.pdf()` 生成 6 页 / 1 页四角文本测试 PDF 后真实上传、真实点击。
- **pdf-split**：6 页 PDF 提取 `1` → 输出 1 页，文本 `PAGE-1`；提取 `2,4-5` → 输出 3 页，逐页文本依次为 `PAGE-2` / `PAGE-4` / `PAGE-5`。
- **pdf-rotate**：90/180/270/0 四档都输出正确的 `/Rotate`，四角标签落位与顺时针旋转映射一致（90: TL→TR, TR→BR, BR→BL, BL→TL；180: TL→BR, TR→BL；270: TL→BL, TR→TL, BR→TR, BL→BR；0: 原位）。
- **运行时报错**：两页 `pageerror = 0`；`console.error = 0`；无任何 `Failed to fetch` / `Cannot find module`。
- **网络与 SW**：页面只拉 `/vendor/pdfjs/4.2.67/pdf.min.mjs`（200, `text/javascript; charset=utf-8`；部分响应 `fromServiceWorker=true`，但 URL 与内容均为当前 4.2.67，非旧版回灌）；无任何 `3.11.174` / `pdfjs@3` 请求。
- **4xx 扫描**：两页全量子资源（含 pdf-lib CDN、图标、JSON）0 个 4xx / 0 个 requestfailed。旧路径 `vendor/pdfjs/3.11.174/*.mjs` 线上返回 404，确认旧版本未残留。
- 结论：**线上复核通过（2026-11-05，线上 commit `d7fa6da8d6`）**。

### 17.7 结构性无法 SRI 的两个项（2026-11-04，只记录不改代码）

| 项 | 使用位置 | 为何无法 SRI | 实际风险 | 日后检测手段 |
| --- | --- | --- | --- | --- |
| `sql-wasm`（sql.js 1.8.0） | [tools/it/sqlite-runner.html](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/it/sqlite-runner.html#L29) | 主脚本 `sql-wasm.js` 已挂 `integrity`，但它通过 `locateFile` 在运行时按固定版本路径 `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/${file}` 拉取 `sql-wasm.wasm`；wasm 由 Emscripten 运行时 fetch，无法给 `fetch` 挂 `integrity` | 版本路径固定意味着「替换同名 wasm」可绕过主脚本 SRI；cdnjs 同版本路径被篡改/投毒时，页面会执行被替换的 wasm。影响仅限打开 sqlite-runner 且主动执行 SQL 的用户 | ① 定期对 `sql-wasm.wasm` 取 sha256 并与 npm `sql.js@1.8.0` 包内文件比对（可写成 cron 脚本，只比对哈希不下载执行）；② 站点若上 CSP，把 `cdnjs.cloudflare.com` 收敛为白名单并记录变更告警；③ 更彻底：把 `sql-wasm.js` + `sql-wasm.wasm` 收进 `vendor/` 自托管（同 pdf.js 做法） |
| TTZZ（字节 goofy 埋点） | 全站 16,668 个 HTML（首页、分类页、工具页；唯一 URL 去重后 1 条） | 由内联脚本 `document.createElement('script')` 动态插入 `https://lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?<token>`；`src` 在运行时拼出，无法在静态 HTML 上挂 `integrity`/`crossorigin` | **token 不是随机数、也不是签名**：全站为同一固定 224 位十六进制串（`85d6452a…`），因此它只是分发/版本标识，不能用于完整性校验。供应商可随时在同 URL 下发新脚本 → 全站执行面随供应商更新而变，属「第三方脚本供应链信任」而非「版本固定」 | ① 每周抓取一次该 URL，记录脚本 sha256 前缀并与上周比对，变化即人工复核（变化可能是正常更新，也可能是劫持）；② 监控 `lf1-cdn-tos.bytegoofy.com` 域名/DNS 与证书变更；③ 若日后供应商改名或该域名不可用，`try/catch` 已容错（脚本失败不阻断页面），但应在构建层统一替换注入源；④ 评估移除：该脚本不承载业务功能，可按合规要求整站下线 |

### 17.8 PII 落盘复审（2026-11-04，数据驱动）

判据由「页面类型敏感」改为「运行时实际写入的键与值形态」：对 68 个含身份线索（姓名/电话/邮箱/证件/地址/车牌/学号）的候选页，在真实浏览器逐页填入 PII 样例（张三 / 13800138000 / pii.test@example.com / 110101199001011234 / 北京市朝阳区建国路88号 / 京A12345 / 20260001），再读 `tb_ux_*`、`tb_uxp_*` 键并用正则判定。

- 68 页抽样，0 加载错误；17 页实际落盘命中 PII 正则。
- 人工复核后**真 PII 且未标 `data-no-persist` 的 6 页**（字段语义即个人身份数据，且为 tool-ux 自动持久化的「顺手存」）：`edu2/exam-analysis`（姓名,分数）、`sports/stats-11`（姓名,成绩）、`clinical-nursing/cycle-7`（患者编号/姓名）、`safety/reminder-cycle-protection`（使用人 姓名/工号）、`it/area-code-lookup`（电话号码）、`kids/memory-palace`（待记忆内容，示例含电话号码）。已全部加 `<body data-no-persist>`。
- 其余 11 页为**假阳性**：数值字段（staffCount/routeLen/phone(小时数)/staff 等）、非身份文本（IPv6、UTM source/medium）、通用自由文本（keyword-extractor、nato-alphabet、qr-decoder 等）。自由文本页仍保留「用户自行粘贴 PII」的残余风险，但字段无身份语义，本轮不改。
- **必须存（显式保存功能，非自动持久化）**：`security/emergency-contacts`、`security/virtual-safe`、`nephrology/manager-1`、`rental/reminder-4`、`funeral/memorial-date`、`cleaning/staff-schedule`、`elderly/reminder-time`、`ecommerce/cycle-15`、`edu/chinese-zodiac`、`tcm-diagnosis/tcm-medical-record` 等页有自定义 `localStorage` 键（`tb_ppe_cycle`/`tb_ckd_patients`/`leases`/`staff`/`meds`/`customers` 等）。`data-no-persist` 只停用 tool-ux 自动回填，不阻断这些显式保存；站点全局隐私徽标已声明「数据仅在本机处理、不上传」。
- 一致性遗留：`reminder-cycle-protection` 的 PPE 队列通过自定义 `tb_ppe_cycle` 保存 `person`，属于「必须存」，加 `data-no-persist` 只关闭了输入框冗余自动保存，队列功能不受影响。

**§17.7 四档结论（2026-11-05 收口）**

| 项 | 结论档位 | 依据 |
|---|---|---|
| `sql-wasm`（sql.js 1.8.0） | **已核 + 登记待改** | 已确认主脚本有 `integrity`、wasm 由 Emscripten `fetch` 无法挂 SRI；版本路径固定≠内容固定。待改项：自托管到 `vendor/`，或加 sha256 巡检。 |
| TTZZ（字节 goofy 埋点） | **已核 + 登记待改** | 已确认 token 为全站同一固定串、非签名，无法做完整性校验；属第三方供应链信任。待改项：每周哈希巡检 / 评估整站下线。 |

**§17.8 四档结论（2026-11-05 收口）**

| 对象 | 结论档位 | 依据 |
|---|---|---|
| 68 个身份线索候选页 | **已核** | 真实浏览器逐页注入 PII 样例后读取 `tb_ux_*` / `tb_uxp_*`，17 页命中、0 加载错误。 |
| 6 个真 PII 且自动持久化页 | **已修** | `edu2/exam-analysis`、`sports/stats-11`、`clinical-nursing/cycle-7`、`safety/reminder-cycle-protection`、`it/area-code-lookup`、`kids/memory-palace` 均已加 `<body data-no-persist>`。 |
| 11 个假阳性页 | **判安全** | 命中项为数值字段、IPv6、UTM 参数、通用自由文本，字段无身份语义；自由文本「用户自行粘贴」的残余风险保留记录。 |
| 显式保存页（`emergency-contacts` / `virtual-safe` / `manager-1` / `staff-schedule` / `tcm-medical-record` 等） | **判安全（功能所需）** | 均为用户主动点击保存的本地业务数据，非自动回填；全局隐私徽标已声明仅本机、不上传。 |
| `reminder-cycle-protection` 一致性遗留 | **判安全** | `tb_ppe_cycle` 保存 PPE 队列属必须存；`data-no-persist` 仅关闭输入框冗余自动保存，队列功能不受影响。 |

### 17.9 第三方依赖与完整性（2026-11-05）

#### 17.9.1 枚举口径与总数

脚本化台账：[scripts/audit_external_deps.py](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/audit_external_deps.py)（`python3 scripts/audit_external_deps.py`，`--check` 对「CDN 脚本未锁精确版本」判失败）。只统计运行时真正发起请求的资源（`<script src>`、`<link rel=stylesheet|preload>`、`import()`、`fetch()`、`loadScript()` / `script.src=`）；淘宝客、GitHub、社交分享等导航链接与 `example.com` / `placehold.co` 代码示例不计。

| 指标 | 数值 |
| --- | --- |
| origin 总数 | **10**（功能库 4 + 统计/广告 6） |
| 资源条目 | **23**（10 个静态 CDN 脚本文件 + 1 个 Transformers ESM + 5 个 HF 模型仓 + 1 个 Google Fonts CSS + 6 个统计/广告端点） |
| 静态外链脚本标签 | 12 个（10 个文件；pdf-lib 在 3 个 PDF 页复用） |
| ① 无版本锁 | **7**（可锁未锁 0；供应商动态下发 6；Google Fonts CSS 1） |
| ② 有版本但无 SRI | **1**（Transformers ESM；sql-wasm 已自托管并加哈希校验） |
| ③ vendor 台账 | **4 条** |
| 无降级页 | 修前 4 → **修后 0**（16 个第三方依赖页全部有降级） |

功能库 origin：`cdn.jsdelivr.net`、`cdnjs.cloudflare.com`、`huggingface.co`、`fonts.googleapis.com`（`fonts.gstatic.com` 仅 preconnect，字体二进制由 Google CSS 间接拉取）。
统计/广告 origin：`sdk.51.la`、`v6-widget.51.la`、`hm.baidu.com`、`zz.bdstatic.com`、`lf1-cdn-tos.bytegoofy.com`、`pagead2.googlesyndication.com`（AdSense 仅在设置 `TOOLBOX_ADS_CLIENT` 时才注入）。

#### 17.9.2 功能依赖台账

| origin | 文件 | 版本锁定 | SRI | crossorigin | 本地兜底 |
| --- | --- | --- | --- | --- | --- |
| cdn.jsdelivr.net | `acorn@8.19.0` / `bcryptjs@2.4.3` / `d3@7.9.2` / `js-yaml@4.1.0` / `less@4.9.1` / `markmap-lib@0.17.2` / `markmap-view@0.17.2` / `mermaid@10.9.8` / `pdf-lib@1.17.1` | 精确 | **有** | **有** | 无 vendor 副本；页面级守卫（见 17.9.6） |
| cdn.jsdelivr.net | `@huggingface/transformers@3.8.1`（`js/ai-core.js` 动态 `import()`） | 精确 | **不可用**（动态 import 无法挂 `integrity`） | 不适用 | 5 个 AI 页 `try/catch` 显示错误 |
| cdnjs.cloudflare.com | `typescript/5.3.3` | 精确 | **有** | **有** | `tsReady` 状态提示 |
| huggingface.co | 5 个模型仓，均已 pin commit sha（`resolve/<sha>/`） | **精确**（sha） | **不可用** | 不适用 | `catch` 显示错误 |
| fonts.googleapis.com | `css2?family=…`（`design/font-pairing.html` 动态创建 `<link>`） | **无** | **不可用**（CSS 由 Google 按 UA 生成） | preconnect 有 | 字体栈回退 `sans-serif` |

#### 17.9.3 ① 无版本锁清单（7 处）

| # | 项 | 类别 | 处置判断 |
| --- | --- | --- | --- |
| 1 | `fonts.googleapis.com/css2` | 可改需权衡 | CSS 无版本号；字体名来自页面内置白名单（非用户输入），失败回退 `sans-serif`。全量自托管成本高，登记为后续候选。 |
| 2 | `sdk.51.la/js-sdk-pro.min.js` | 不可锁 | 供应商动态下发，官方要求直引；统计 SDK，无业务功能。 |
| 3 | `v6-widget.51.la/v6/<id>/quote.js` | 不可锁 | 同上；滚动到页脚才懒挂载。 |
| 4 | `hm.baidu.com/hm.js?id=…` | 不可锁 | 百度统计，URL 带站点 id 而非版本。 |
| 5 | `zz.bdstatic.com/linksubmit/push.js` | 不可锁 | 百度自动推送。 |
| 6 | `lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?<token>` | 不可锁 | 见 §17.7：token 为固定分发标识、非签名。 |
| 7 | `pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=…` | 不可锁（条件启用） | 仅 `window.TOOLBOX_ADS_CLIENT` 存在时注入。 |

**「可锁但未锁」= 0 处**。HF 5 个模型仓已从本清单移出（改为 commit sha pin，见 17.9.7）；10 个静态 CDN 脚本全部精确版本 + `integrity` + `crossorigin="anonymous"`（§9.1 已把浮动版本清零）。

#### 17.9.4 已知限制：有版本但无 SRI（2 处）

| 项 | 为何结构上无法挂 SRI | 缓解手段（落地状态） |
| --- | --- | --- |
| `@huggingface/transformers@3.8.1` | `import()` 语法没有 `integrity` 参数；库内部还会二次 `import` 分片，SRI 无处挂载。 | **已落地**：精确版本 `3.8.1` + 固定 `cdn.jsdelivr.net` 域名 + `getTransformers()` 内 `tf.env.version !== '3.8.1'` 断言（不匹配即抛错，AI 页显示「出错：Transformers.js 版本校验失败」）。残留：无法做内容哈希校验。 |
| `sql.js/1.8.0/sql-wasm.wasm` | `integrity` 只作用于 HTML 解析器的 `<script>/<link>` 请求；Emscripten 是程序内 `fetch` + `WebAssembly.instantiate`，标签属性无法注入。 | **已彻底解决**：改为 `vendor/sql.js/1.8.0/` 自托管，页面先 `fetch → crypto.subtle.digest('SHA-256')` 比对，通过后才 `initSqlJs({ wasmBinary })`（字节直接交给实例化，不再二次请求）。校验失败时明确拒绝启动并提示「校验失败：拒绝启动」。 |

> 结论：wasm 已从「已知限制」转为「已加固」；Transformers ESM 因动态 import 的结构限制保留登记，但断言使其从「静默换码」降为「可感知失败」。

#### 17.9.5 ③ vendor 台账

| 组件 | 版本 | 本地路径 | 来源 | 备注 |
| --- | --- | --- | --- | --- |
| PDF.js | 4.2.67 | `vendor/pdfjs/4.2.67/pdf.min.mjs`、`pdf.worker.min.mjs` | npm `pdfjs-dist` | §17.6 由 CDN 3.11.174 升级自托管（CVE-2024-4367） |
| Fuse.js | 7.0.0 | `vendor/fuse.min.js` | npm `fuse.js` | `index.html` 搜索 + SW 预缓存 |
| Plus Jakarta Sans | **2.071** | `vendor/fonts/`（5 字重 × woff2/ttf + `fonts.css`） | Google Fonts 本地副本 | `index.html` / `404.html` 使用；版本取自 TTF name 表 ID5（`Version 2.071;gftools[0.9.30]`） |
| sql.js | 1.8.0 | `vendor/sql.js/1.8.0/sql-wasm.js`、`sql-wasm.wasm` | cdnjs `sql.js/1.8.0` | 自托管；wasm 启动前 SHA-256 校验（失败拒绝启动） |

台账由 `vendor_ledger()` 从磁盘读取版本目录 / 文件头注释自动生成，避免手写漂移。

#### 17.9.6 兜底修复（4 页）

修前有 4 个页面在 CDN 失败时静默失效（`pdf-merge` 直接解构 `PDFLib`、`flowchart` 直接调 `mermaid.initialize`、`bcrypt` / `yaml-validator` 直接调用库函数）。统一加「依赖兜底提示」内联脚本：`DOMContentLoaded` 时判 `typeof <lib> === 'undefined'`，命中则在 `.container` 顶部插入中日英双语提示（中/英按 `documentElement.lang` 与 `?lang=en-US` 切换），不阻断其余页面逻辑。

修改页：`office/pdf-merge`、`office/flowchart`、`it/bcrypt`、`it/yaml-validator`。

**两向自证**（无头 Chrome，拦截 `cdn.jsdelivr.net` 请求 vs 正常放行）：

```
PASS flowchart.html    blocked=true/true normal=false
PASS pdf-merge.html    blocked=true/true normal=false
PASS bcrypt.html       blocked=true/true normal=false
PASS yaml-validator.html blocked=true/true normal=false
RESULT 4/4
```

`blocked/true` = 出现提示且位于容器首位；`normal=false` = 正常加载时不误报。改动后 `python3 scripts/audit_external_deps.py` 的「无降级页」由 4 变 0。

#### 17.9.7 本批加固与自证

**① HF 模型 pin commit sha**（`js/ai-core.js`）

- 新增 `MODEL_REVISIONS`（5 个仓库 → 40 位 sha），`getPipeline()` 内部自动补 `revision`；cache key 改为 `${task}|${model}|${revision}`。
- 未登记模型走 `main` 时 `console.warn('[ai-core] 模型 X 未登记 revision，回退 main；上游更新不会被感知。')`，防止新增模型静默漏 pin。
- 依据：`pipelines.js:3448-3488` 接收 `revision` → `pretrainedOptions` → `hub.js:467-478` 替换 `env.remotePathTemplate` 的 `{revision}`；`hub.js:486-488` 在 revision ≠ main 时把 revision 计入缓存键。**pin 后首载会重新下载属预期；升级 Transformers.js 时需复验该 API 仍被透传。**
- 真机取证（无头 Chrome 打开 `tools/ai/sentiment-analysis.html`，输入英文后点击分析，拦截 HF 请求）：

```
https://huggingface.co/Xenova/distilbert-base-uncased-finetuned-sst-2-english/resolve/0b6928efcb76139cae2c6881d49cda67fe119f42/...
```

请求 URL 已从 `resolve/main/` 变为 `resolve/<commit-sha>/`。

**② sql-wasm 自托管 + 启动前 SHA-256 校验**（`tools/it/sqlite-runner.html`、`vendor/sql.js/1.8.0/`）

- `sql-wasm.js` 与 `sql-wasm.wasm` 均移入 vendor，页面不再向 `cdnjs.cloudflare.com` 发请求（该页 origin 归零）。
- 加载顺序：`fetch(local wasm)` → `crypto.subtle.digest('SHA-256')` → 与内置常量比对 → `initSqlJs({ wasmBinary })`。用 `wasmBinary` 传入字节，Emscripten 不再二次请求 wasm。
- 校验失败：`setStatus('error','校验失败：拒绝启动')`，执行按钮保持禁用，不创建数据库实例。
- **哈希来源与升级流程**：`SQL_WASM_SHA256` 是页面内 JS 常量（`tools/it/sqlite-runner.html:520`），**不读清单/构建元数据**。升级时须整组同改：① 换 `vendor/sql.js/<新版本>/sql-wasm.js` + `sql-wasm.wasm`；② `shasum -a 256 sql-wasm.wasm` 取新值；③ 同步改 `SQL_WASM_URL`（含版本目录）与 `SQL_WASM_SHA256`。三者任一漏改都会在启动时因哈希不符而拒绝启动，属于可感知失败。

两向自证（同一 URL，正常响应 vs 篡改末字节）：

```
PASS sqlite positive: ready
PASS sqlite positive: no cdnjs request :: cdnjs=0
PASS sqlite positive: local wasm fetched
PASS sqlite positive: query executes :: 共执行 1 条语句 · 失败 0 条
PASS sqlite negative: refuses tampered wasm :: intercepted=1
PASS sqlite negative: run disabled
PASS sqlite negative: status not ready :: 校验失败：拒绝启动
```

**③ Google Fonts 瘦身（自托管暂缓）**

- `font-pairing.html` 的 `loadFonts()` 去掉未使用的 `300` 字重：`wght@300;400;500;600;700` → `wght@400;500;600;700`，@font-face 声明由 **175 降至 140**（-20%）。
- 自托管（42 文件 / 0.8–1.2MB / OFL 许可证 / 懒加载改造）记为后续候选，本批不做。
- `vendor/fonts/` 的 Plus Jakarta Sans 版本由 TTF name 表 ID5 解析为 **2.071**，已进台账。

**AI + 字体回归**（同一无头脚本）：

```
PASS ai: HF request observed
PASS ai: URL contains pinned sha
PASS ai: no version assertion failure
PASS font: css2 drops 300 weight :: ...wght@400;500;600;700&display=swap
RESULT 11/11
```

#### 17.9.8 门禁与边界

- **两个审计脚本已挂进 `scripts/run_gates.py`**（紧随 `asset audit`，与既有 python 门禁同等待遇，只读退出码）：
  `local storage audit` → `python3 scripts/audit_local_storage.py --check`；
  `external dependency audit` → `python3 scripts/audit_external_deps.py --check`。门禁总数 **222 → 224**。
- **造红自证（探针用完即删）**：
  - 根目录探针页含真实 `document.cookie = '...'` → `audit_local_storage.py --check` **exit 1**（`违规：Cookie 写入 1`）；
  - 根目录探针页含 `<script src="https://cdn.jsdelivr.net/npm/lodash/dist/lodash.min.js">`（无 `@x.y.z`）→ `audit_external_deps.py --check` **exit 1**（`[FAIL] 外部脚本未锁定精确版本：…lodash.min.js（_probe_cdn.html）`）；
  - 删除两个探针后复跑，双双 **exit 0**（Cookie 0 / 未锁 0）。
- **CI 可跑性（干净 worktree 实测）**：`git worktree add --detach /tmp/tb-clean HEAD` 后确认无 `node_modules/`、无 `zh-tw/`，两脚本均 **exit 0**；`audit_external_deps.py` 的 `SKIP_DIRS` 显式排除 `zh-tw`/`node_modules`，`audit_local_storage.py` 只遍历根 `*.html` + `tools/` + `guides/` + `js/`，均不读构建产物。
- **本批全量门禁结果**：`python3 scripts/run_gates.py` → **222/224 通过**。两项未通过均非本批引入：`science calc correctness`（203 例中 3 例失败）来自并行线未提交的 `verify_science_calc.js` 新用例与 3 个 science 页面改动，同一脚本在 **HEAD 干净树 196/196 全过**；`marketing calc correctness` 的 `social-media-image-sizes`（`ToolBox.downloadText` 桩失效）在 **HEAD 干净树上同样 exit 1**，属导出收敛批次遗留。
- `python3 _audit_assets.py --check` / `python3 _audit_links.py --check`：16689 文件，0 死链 / 0 lang 缺失 / 0 重复 id。
- 计算回归：`verify_it_calc.js sqlite-runner`、`bcrypt`、`yaml-validator` 全过；office 两页无既有用例（0/0）。
- 为拿到全量门禁计数，本批按用户指令跑了一次 `run_gates.py`（内含 `_build.py`），`zh-tw/` 与 `json/*.json` 因此被重建；按路径级提交纪律，构建产物与并行线未提交改动**均未纳入本批提交**。未 push。工具页 HTML / `js/ai-core.js` 改动在下次构建时随 SW 版本戳统一生效。
- 新增入库文件：`scripts/audit_external_deps.py`、`vendor/sql.js/1.8.0/sql-wasm.js`、`vendor/sql.js/1.8.0/sql-wasm.wasm`；本地无头验证脚本放 `/tmp`，未入库。

