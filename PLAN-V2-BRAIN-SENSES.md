# PLAN-V2-BRAIN-SENSES.md
> 下一版本主推专题：**认知脑力 · 心理性格 · 感官知觉 · 色觉无障碍 · 趣味创意**
> 创建：2026-09-02 ｜ 状态：**待开工** ｜ 工具总数：**26 个全新独立开发**
> 铁律：① 一个工具一个任务卡，独立开发，**禁止套模板** ② A 级质量 ③ 中英文 SEO 一步到位 ④ 全部进首页热门工具 + 热门分类

---

## 0. 目标

把这 26 个工具做成站内**质量天花板**：功能深度对齐各自品类的头部竞品（humanbenchmark.com / Open Recall / WolfChart / colorblind-sim / Farnsworth D-15 等），全部 A 级，中英文双语 + 结构化数据完整，并作为首页热门位与热门分类的主推内容。

---

## 1. 现状核查结论（已逐文件验证，非推测）

**已存在、本次不再重复开发的工具（直接剔除或合并）：**

| 已存在文件 | 大小 | 覆盖掉的清单项 |
|---|---|---|
| `tools/fun/memory-game.html` | 27KB | ❌ MemoryGame（翻牌配对） |
| `tools/fun/reaction-tester.html` | 16KB | ❌ Speed_test 的「反应速度」 |
| `tools/fun/click-speed.html` / `cps-test.html` | 16KB×2 | ❌ Speed_test 的「连点速度」 |
| `tools/ophthalmology/ishihara-test.html` | 16KB | ❌ Ishihara-test ❌ Eye-Health-Color-Blindness-Test ❌ Open-Colour-Labs（**已含 Canvas 程序化生成 + 「重新生成」按钮 + 6 图评分**） |
| `tools/design/contrast-checker.html` / `color-contrast-check.html` | 31KB / 14KB | ❌ a11y WCAG 对比度检查 |
| `tools/design/color-palette-generator.html` | 36KB | ⚠️ pal（仅覆盖「生成」，**未覆盖「色觉可辨识度校验」**→ 保留但重新定义） |
| `tools/fun/number-guess.html` / `caishuzi-1-100fanwei.html` | 15KB / 35KB | ⚠️ 均为「电脑猜你的数」二分，**与 1A2B（Bulls & Cows）玩法不同**→ 保留 |
| `tools/fun/riddle-generator.html` | 10KB | ⚠️ 随机生成，**无每日/积分/连击**→ 保留但重新定义 |
| `tools/travel/aim-trainer.html`、`tools/it/typing-test.html`、`tools/fun/number-memory.html`、`tools/fun/sequence-memory.html`、`tools/fun/pattern-memory.html` | — | ⚠️ 均为**单项练习**，无统分/常模/百分位 → Human Benchmark 以「测评」形态保留 |

**站内完全没有、本次填补的空白：** N-Back、Stroop、舒尔特方格、Corsi 木块、心理旋转、SCL-90、大五人格(BFI/SBTI)、九型、霍兰德 RIASEC、成人依恋、专业视力表(WolfChart)、自适应近视估算、Amsler 方格、散光表、纯音测听、听觉时间分辨率、Farnsworth D-15、色盲模拟（8 型 + 图片 + 安全色）、CVD 安全配色、每日谜题、1A2B。

---

## 2. 老板清单 22 项 → 逐条判定

| # | 清单工具 | 判定 | 处置 |
|---|---|---|---|
| 1 | SCOPE 综合认知评估 | ✅ **做** | → **T01** `cognition/cognitive-assessment.html` |
| 2 | Human Benchmark TS | ⚠️ **改造做** | 剔除 auth / leaderboard（需后端，违反纯前端）。改为「8 项统一测评 + 常模百分位 + 脑力指数 + 本地历史曲线」→ **T02** |
| 3 | Speed_test 四合一 | ⚠️ **裁剪做** | 反应速度、连点速度已存在 → 只保留站内没有的「一秒感知 + 双击速度 + 节拍同步」→ **T03** |
| 4 | Open Recall (N-Back) | ✅ **做** | → **T04** `cognition/nback-training.html` |
| 5 | MemoryGame | ❌ **不做** | 已有 `fun/memory-game.html` |
| 6 | SCL-90 心理测试 | ✅ **做** | → **T09** `psychology/scl90-assessment.html` |
| 7 | SBTI 人格测试 | ✅ **做** | → **T10** `psychology/bigfive-personality-test.html` |
| 8 | whatbobaareyou | ✅ **做** | → **T11** `psychology/bubble-tea-personality-quiz.html` |
| 9 | WolfChart 视力表 | ✅ **做** | → **T15** `ophthalmology/eye-chart-toolkit.html` |
| 10 | Eye Vision Checker | ✅ **做** | → **T16** `ophthalmology/vision-screening-21.html` |
| 11 | GoldenHearing | ✅ **做** | → **T17** `ent/temporal-resolution-hearing.html` |
| 12 | Eye-Health-Color-Blindness-Test | ❌ **不做** | 已有 `ophthalmology/ishihara-test.html` |
| 13 | Open-Colour-Labs | ❌ **不做** | 已有页已是程序化生成 + 可重新生成，功能重合 |
| 14 | Ishihara-test | ❌ **不做** | 已有 |
| 15 | colorblind-sim | ✅ **做（旗舰）** | 现有 `design/color-blindness-simulator.html` 仅 4 型、无图片、无 WCAG；新版 8 型 + 图片上传 + WCAG + 安全色 → **T22** |
| 16 | dichroma | ❌ **不做** | 8 型并列网格已并入 **T22** |
| 17 | pal 调色板色觉 | ⚠️ **改造做** | 现有是「生成配色」，新版是「**校验配色在 8 型色觉/灰度下的可辨识度**」→ **T23** |
| 18 | a11y WCAG 对比度 | ❌ **不做** | 已有 `contrast-checker.html` + `color-contrast-check.html` |
| 19 | colorblind_image_tester | ❌ **不做** | 图片上传模拟已并入 **T22** |
| 20 | colorfuzz 输入网址模拟 | ❌ **不可行** | 需跨域抓取/iframe 嵌套目标站，CORS + `X-Frame-Options` 双重封死，**纯前端无法实现** |
| 21 | Daily Riddle & Puzzle | ✅ **做** | → **T25** `fun/daily-riddle.html` |
| 22 | 1A2B 猜数字 | ✅ **做** | → **T26** `fun/1a2b-guess.html` |

**清单 22 项 → 落地 13 个任务（T01–T04、T09–T11、T15–T17、T22、T23、T25、T26），剔除 9 项。**

---

## 3. 老板要求「补充推荐」→ 新增 13 项

全部为**纯前端可行 + 站内确认为空 + 搜索需求真实**的品类：

| 补充工具 | 归属 | 理由 |
|---|---|---|
| **Stroop 斯特鲁普效应测试** | cognition | 执行功能/抑制控制经典范式，认知类必补，搜索量大 |
| **舒尔特方格 Schulte Table** | cognition | 注意力/视觉搜索训练，国内家长群体刚需 |
| **Corsi 木块敲击测试** | cognition | 视觉空间工作记忆，与 N-Back（言语工作记忆）互补 |
| **心理旋转测试** | cognition | 空间能力经典范式，Vandenberg 题库可纯前端生成 |
| **九型人格 Enneagram** | psychology | 娱乐+专业双属性，传播性极强 |
| **霍兰德职业兴趣 RIASEC** | psychology | 高考志愿/求职季刚需，长尾流量稳定 |
| **成人依恋类型 ECR** | psychology | 亲密关系品类头部需求 |
| **纯音听力筛查（听力图）** | ent | Web Audio 生成 125–8000Hz 纯音，绘听力图，高价值 |
| **Amsler 阿姆斯勒方格** | ophthalmology | 黄斑变性自测，中老年刚需 |
| **散光放射线表** | ophthalmology | 全家自筛散光，与视力表互补 |
| **Farnsworth D-15 色相排列** | colorvision | 比石原更精细，可判型 + 严重度，专业向 |
| **CVD 安全配色生成器** | colorvision | 色盲友好配色，设计师刚需（与 T23 校验互补） |
| **数字广度 Digit Span** | cognition | 韦氏记忆核心分测验，SCOPE 之外的独立练习器 |

**最终：13（清单）+ 13（补充）= 26 个新工具。**

---

## 4. 行业归属方案（含 2 个新建行业）

| 行业 slug | 中文名 | 图标 | 状态 | 本次工具数 |
|---|---|---|---|---|
| `cognition` | 认知与脑力训练 | 🧠 | **新建** | 8 |
| `psychology` | 心理咨询 | 🫀 | 已有 | 6 |
| `ophthalmology` | 眼科医学 | 👁️ | 已有 | 4 |
| `colorvision` | 色觉与色彩可访问性 | 🎨 | **新建** | 4 |
| `ent` | 耳鼻喉 | 👂 | 已有 | 2 |
| `fun` | 游戏娱乐 | 🎮 | 已有 | 2 |

### 4.1 新建行业必须同步的 6 处改动（漏一处 = 页面显示英文 slug）

1. `_build.py` → `INDUSTRY_DEFS` 增加 `'cognition': ('🧠', '认知与脑力训练')`、`'colorvision': ('🎨', '色觉与色彩可访问性')`
2. `i18n/industry-en.json` → `"cognition": "Cognition & Brain Training"`、`"colorvision": "Color Vision & Accessibility"`
3. `i18n/tools/cognition.json` / `cognition-body.json` / `cognition-phrases.json` 三个文件（新建，先空 `{}` 再随工具填充）
4. `i18n/tools/colorvision.json` / `colorvision-body.json` / `colorvision-phrases.json`（同上）
5. 建目录 `tools/cognition/`、`tools/colorvision/`（`_build.py` 会自动生成各自的 `index.html`）
6. `js/app.js` → `HOT_INDUSTRIES` 数组追加 `'cognition'`、`'colorvision'`、`'psychology'`、`'ophthalmology'`（热门分类露出）

---

## 5. 全局开发规范（26 个工具通用，逐条遵守）

### 5.1 文件与目录
- 路径：`tools/<industry>/<slug>.html`，slug 全小写 + 连字符，**用 SEO 词不用 repo 名**（例：`nback-training.html`，不用 `open-recall.html`；品牌名写进 `<title>` 与 h1）
- 引用路径深度固定 2 层：`../../css/common.css`、`../../js/common.js`
- 单文件体积目标 25–90KB（A 级要求）；上限 200KB（静态测试告警线）

### 5.2 head 骨架（照抄 `tools/it/rich-text-editor.html` 的 head 结构，勿自由发挥）
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script src="/js/tool-page-runtime.js" defer></script>
<!-- TOOLBOX-TOOL-RUNTIME -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=<cat>,industry=<industry>,icon=<emoji>,bg=#<hex>">
<title>{EN_TITLE} - ToolBox</title>
<meta name="title-zh" content="{中文标题}">          <!-- 切回中文时用 -->
<link rel="canonical" href="https://chenguangwu.github.io/tools/<ind>/<slug>.html">
<meta property="og:title" content="{EN_TITLE}">
<meta property="og:description" content="{中文长描述}">
<meta property="og:url" content="https://chenguangwu.github.io/tools/<ind>/<slug>.html">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{EN_TITLE}">
<meta name="twitter:description" content="{中文长描述}">
<meta name="description" content="{中文长描述}">
<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>
</head>
```
`<!-- TOOLBOX-TOOL-RUNTIME -->`、`<!-- TOOLBOX-WEBAPP-LD -->`、`<!-- TOOLBOX-SECURITY -->` 三个锚点必须保留，`_build.py` 靠它们做幂等注入（BreadcrumbList / WebApplication JSON-LD / 安全头）。

### 5.3 A 级质量硬指标（`_build.py::classify_quality`）
满足任一即 A：
- 独有 `<script>` 字符数 **≥ 6000**；**或**
- 独有脚本 ≥ 3000 **且** `input+select+textarea` 数量 **≥ 3**；**或**
- 含 `formula-box` 或 `<canvas>` 或 `data-viz`

**达标路径（禁止堆废代码，必须靠真实功能模块）：**
① 结果可视化 canvas（曲线/雷达/热力/听力图/雷达图）② 完整计分与常模百分位表 ③ 本地历史记录 + 趋势图 ④ 领域知识面板（评分标准表 / 维度释义表 / 参考常模表）⑤ 导出（PNG / CSV / JSON）⑥ 分享结果卡片。

### 5.4 中英文 i18n 八件套（SEO 一步到位，**每个工具必须全做**）
| # | 落点 | 内容 |
|---|---|---|
| 1 | `<title>` | **英文**（构建期预渲染）；中文存 `<meta name="title-zh">` |
| 2 | `og:title` / `twitter:title` | **强制英文** |
| 3 | `description` / `og:description` / `twitter:description` | 中文长描述（60–120 字，含核心关键词 + 用途 + 免责） |
| 4 | `i18n/tools/_en_override.json` | `"<ind>/<slug>": {"en":"英文标题","ed":"英文长描述","ind":"<ind>"}` |
| 5 | `i18n/tools/slug-en.json` | 同上结构（缺 → `_test_static.py` 报「映射缺失」） |
| 6 | `i18n/tools/<ind>.json` | `{h1,title,intro,note[],desc}` 的 zh-CN + en-US 双语 |
| 7 | `i18n/tools/<ind>-body.json` | `{title,intro,h1,en:{...}}` |
| 8 | `i18n/tools/<ind>-phrases.json` | 页面内**每一个可见中文串** → 英文（含按钮、标签、结果等级名、提示语） |

> ⚠️ 两个 `*.json` 必须 `indent=1`，否则全文件大 diff。
> ⚠️ 英文**禁止 slug 直译**，须是母语者会搜的自然英文（参考下方任务卡给定文案）。

### 5.5 视觉规范（`ui/设计规范.md`）
主色 `#FF6B35`／辅色 `#7C3AED`／强调 `#00C9A7`／背景 `#FFFAF7`；卡片 `rounded-2xl` 16px、按钮 `rounded-xl` 12px、标签 `rounded-full`；渐变 `linear-gradient(135deg,#FF6B35,#7C3AED)`；图标 Lucide `data-lucide`。颜色一律走 CSS 变量，禁止硬编码。移动端必须可用（认知/游戏类尤其注意触摸目标 ≥ 44px）。

### 5.6 禁用项
- ❌ 禁止复制粘贴任何已有工具页代码结构（老板明令「不准套模板」）
- ❌ 禁止 `localStorage` 以外的数据持久化；禁止任何外发请求
- ❌ 禁止引入新第三方 CDN（图表用站内 `js/chart.js`，二维码用站内 `js/qrcode.js`）
- ❌ 医疗/心理类工具**必须**带免责声明：筛查用途、不替代专业诊断
- ❌ 禁止把 AI 生成的占位文案写进页面

---

## 6. 任务卡 T01 – T26

> 每张卡 = 一个工具 = 一次独立开发。开工前先读 §5 全局规范。
> 状态标记：`⬜ 待做` / `🟨 进行中` / `✅ 完成`

### 🧠 认知与脑力训练 `tools/cognition/`（8 个）

---
### T01 · SCOPE 综合认知评估中心 ⬜
- **路径**：`tools/cognition/cognitive-assessment.html`
- **meta**：`cat=validator,industry=cognition,icon=🧠,bg=#ede9fe`
- **中文名**：SCOPE 综合认知评估 ｜ **EN**：SCOPE Cognitive Assessment
- **中文简介**：开源综合性认知能力评估，涵盖注意力、工作记忆、加工速度与执行功能四大维度共 8 项分测验，逐项给出标准分、百分位与雷达图，全部数据本地保存、可导出。
- **EN desc**：SCOPE is a comprehensive open-source cognitive assessment covering attention, working memory, processing speed and executive function across 8 subtests, with standardized scores, percentile ranks and a radar chart. All data is stored locally and exportable.
- **竞品对标**：SCOPE (scope-lab)、CogniFit、Cambridge Brain Sciences
- **功能规格**
  1. 8 项分测验：① 简单反应时 ② 选择反应时 ③ 数字广度正背 ④ 数字广度倒背 ⑤ 符号数字模态(SDMT) ⑥ Stroop 干扰 ⑦ N-Back(2-back) ⑧ 连线测试 TMT-A/B
  2. 统一指导语页 + 练习试次（每项 3 题练习，成绩不计入）
  3. 计分：原始分 → 年龄分层常模 → Z 分 → 标准分(均值100,SD15) → 百分位
  4. 常模表内置（18–29 / 30–49 / 50–69 / 70+ 四层，按分层线性插值）
  5. 结果页：四维雷达图（canvas 自绘）+ 逐项明细表 + 文字解读（强项/弱项 Top2）
  6. 本地历史：localStorage 存最近 20 次，折线趋势图 + CSV 导出
  7. 结果分享卡片（canvas 导出 PNG）
- **技术方案**：状态机 `idle→instruction→practice→test→result`；`requestAnimationFrame` 计时（不用 `setTimeout` 保证精度）；雷达图 canvas 自绘；常模用 `{test:{ageBand:{mean,sd}}}` 常量表
- **A 级路径**：独有脚本 ≥6000（8 套测验逻辑 + 常模插值 + 雷达图 + 趋势图）
- **验收**：走完 8 项约 12 分钟；刷新后历史仍在；切英文标题/简介正确

---
### T02 · Human Benchmark 全项基准测评 ⬜
- **路径**：`tools/cognition/human-benchmark.html`
- **meta**：`cat=game,industry=cognition,icon=⚡,bg=#fff8e1`
- **中文名**：Human Benchmark 认知基准测评 ｜ **EN**：Human Benchmark Cognitive Test Suite
- **中文简介**：8 项经典认知基准测试合集（反应时间、目标点击、序列记忆、数字记忆、词汇记忆、猩猩闪记、视觉记忆、打字速度），每单项给出全球常模百分位，并合成综合脑力指数与能力画像。
- **EN desc**：A suite of 8 classic cognitive benchmark tests — reaction time, aim trainer, sequence memory, number memory, verbal memory, chimp test, visual memory and typing speed — each scored against a built-in global norm, combined into an overall brain index and ability profile.
- **差异化**（与站内已有单项练习页的区别）：**统一计分 + 常模百分位 + 综合指数**，是「测评」不是「练习」
- **功能规格**
  1. 8 项：Reaction Time（5 次取均值，含抢跑判定）、Aim Trainer（30 靶，命中时间+精度）、Sequence Memory（方格序列）、Number Memory（递增位数）、Verbal Memory（已见/未见词判定，60 词）、Chimp Test（数字闪现后按序点击）、Visual Memory（9×9 网格图形记忆）、Typing（30s WPM+准确率）
  2. 每项内置常模分布（基于公开均值+SD 的正态/对数正态模型）→ 百分位
  3. 综合脑力指数 = 8 项百分位的加权均值（记忆 30%、注意 25%、加工速度 25%、执行 20%），0–100
  4. 能力雷达图 + 排行榜式「你击败了 xx% 的人」文案
  5. 本地最佳成绩 + 历史曲线；可导出成绩单 PNG
- **技术方案**：子测验用独立 class 封装统一接口 `{id,name,render(),onResult(score)}`；`AudioContext` 做反馈音（不依赖外部音频）；随机序列用 `crypto.getRandomValues`
- **A 级路径**：≥6000 字符（8 套引擎 + 常模模型 + 雷达图）
- **验收**：每项可单独重测；百分位随成绩单调变化；移动端可点

---
### T03 · 时间感知与节奏精度测试 ⬜
- **路径**：`tools/cognition/time-perception.html`
- **meta**：`cat=game,industry=cognition,icon=⏱️,bg=#e0f2fe`
- **中文名**：时间感知与节奏精度测试 ｜ **EN**：Time Perception & Rhythm Accuracy Test
- **中文简介**：三项时间感知挑战：一秒挑战（不开计时器按下正好 1.000 秒）、双击速度（测量最短双击间隔）、节拍同步（跟随节拍器点击测偏差），给出毫秒级精度评分与百分位。
- **EN desc**：Three time-perception challenges: the one-second challenge (stop exactly at 1.000s), double-click speed (shortest reliable interval) and beat synchronization (tap along to a metronome and measure deviation), scored in milliseconds with percentile ranks.
- **功能规格**：① 一秒挑战 5 次，显示每次误差（±ms）、平均绝对误差、标准差 → 百分位 ② 双击速度：10 轮取最快有效间隔，含抖动分布直方图 ③ 节拍同步：BPM 可选 60/90/120，20 拍，输出提前/滞后均值与一致性 ④ 误差分布图（canvas 柱状）⑤ 本地最佳 + 历史
- **技术方案**：`performance.now()` 计时；节拍器用 `AudioContext.currentTime` 精确调度（不用 setInterval）
- **A 级路径**：≥6000（三套引擎 + 直方图 + 常模）
- **验收**：一秒挑战误差读数稳定在 ±5ms 内；音频不延迟

---
### T04 · N-Back 工作记忆训练 ⬜
- **路径**：`tools/cognition/nback-training.html`
- **meta**：`cat=game,industry=cognition,icon=🔁,bg=#ede9fe`
- **中文名**：N-Back 工作记忆训练 ｜ **EN**：N-Back Working Memory Training
- **中文简介**：经典 N-Back 双任务训练（位置 + 语音双通道），支持 1–5 back 自适应升降级，实时正确率与反应时曲线，可切换数字/字母/颜色/位置多种刺激材质，训练数据本地留档。
- **EN desc**：Classic dual N-Back working memory training (position + audio channels) with adaptive 1–5 back difficulty, live accuracy and reaction-time curves, multiple stimulus modes — digits, letters, colors or positions — and a local training log.
- **功能规格**：① 单通道/双通道切换 ② N 值固定或自适应（连续 4 对升、连续 3 错降）③ 刺激材质：数字/字母/颜色/位置 ④ 每轮 20+N 试次，实时显示 `位置命中率 / 语音命中率 / d'`（信号检测论灵敏度指数）⑤ 训练曲线（按天聚合的正确率与最高 N）⑥ 自适应难度升级建议
- **技术方案**：`d' = z(HitRate) − z(FalseAlarmRate)`，z 用 Acklam 逆正态近似；`SpeechSynthesisUtterance` 读字母（纯前端，无需后端）
- **A 级路径**：≥6000（自适应引擎 + d' 统计 + 曲线 + 语音）
- **验收**：自适应升降级逻辑正确；d' 计算边界（HR=1/FA=0）不崩溃

---
### T05 · Stroop 斯特鲁普效应测试 ⬜
- **路径**：`tools/cognition/stroop-test.html`
- **meta**：`cat=validator,industry=cognition,icon=🎨,bg=#fce4ec`
- **中文名**：Stroop 斯特鲁普效应测试 ｜ **EN**：Stroop Effect Test
- **中文简介**：经典 Stroop 干扰范式，含一致/不一致/中性三类试次，测量干扰效应量（不一致反应时 − 一致反应时）、错误率与自动化程度，附常模区间与执行功能解读。
- **EN desc**：The classic Stroop interference paradigm with congruent, incongruent and neutral trials, measuring the interference effect (incongruent RT minus congruent RT), error rates and automatization, with norm ranges and an executive-function interpretation.
- **功能规格**：① 三阶段：练习 → 一致块(24) → 混合块(48，含中性) ② 键盘/屏幕按钮双输入 ③ 输出：各条件平均 RT、错误率、Stroop 干扰量(ms)、干扰率(%)、与常模对比 ④ 干扰效应可视化（三条件柱状 + 误差棒）⑤ 逐试次 RT 散点（展示练习效应）⑥ 结果导出
- **A 级路径**：≥6000（范式引擎 + 统计 + 双图）
- **验收**：干扰量为正（不一致 > 一致）在多数人身上成立；移动端按钮够大

---
### T06 · 舒尔特方格注意力训练 ⬜
- **路径**：`tools/cognition/schulte-table.html`
- **meta**：`cat=game,industry=cognition,icon=🔲,bg=#e8f5e9`
- **中文名**：舒尔特方格注意力训练 ｜ **EN**：Schulte Table Attention Trainer
- **中文简介**：经典舒尔特方格训练，支持 3×3 到 7×7 五种规格、数字/字母/汉字/颜色四种模式、倒计时与统计模式，记录完成时间与每秒搜索效率，生成历史进步曲线。
- **EN desc**：Classic Schulte table training with 3×3 to 7×7 grid sizes, four modes — digits, letters, Chinese characters and colors — plus countdown and statistics modes, tracking completion time and search efficiency with a progress chart.
- **功能规格**：① 网格 3/4/5/6/7 阶 ② 模式：数字 1–N²、字母 A–Z、常用汉字、颜色名 ③ 正序/倒序 ④ 实时显示已点/总数、用时、速率（个/秒）⑤ 错误点击震动+计数 ⑥ 历史曲线（按规格分组）⑦ 每日建议训练量提示
- **A 级路径**：≥6000（多模式生成器 + 计时 + 曲线）
- **验收**：倒序模式正确；触摸点击响应无延迟

---
### T07 · Corsi 木块敲击测试 ⬜
- **路径**：`tools/cognition/corsi-block-test.html`
- **meta**：`cat=game,industry=cognition,icon=🧱,bg=#e3f2fd`
- **中文名**：Corsi 木块敲击测试 ｜ **EN**：Corsi Block-Tapping Test
- **中文简介**：经典视觉空间工作记忆测验，木块序列逐级加长，正序/倒序双条件，自动测算 Corsi 广度（最高正确长度）与总分，附年龄常模与空间记忆解读。
- **EN desc**：The classic visuospatial working memory test: block sequences grow progressively longer in both forward and backward conditions, yielding a Corsi span and total score with age norms and a spatial-memory interpretation.
- **功能规格**：① 9 块不规则布局（标准 Corsi 坐标）② 正序 + 倒序 ③ 阶梯法：同长度 2 次中 1 次对即晋升，连续 2 次错终止 ④ 输出：Corsi 广度、总正确试次、乘积分（广度×正确数）⑤ 序列演示动画（高亮节奏可调）⑥ 常模对比（儿童/成人/老年）⑦ 结果图
- **A 级路径**：≥6000（阶梯法引擎 + 动画 + 常模 + 图）
- **验收**：倒序序列判定正确；阶梯升降符合规则

---
### T08 · 数字广度记忆测验 ⬜
- **路径**：`tools/cognition/digit-span-test.html`
- **meta**：`cat=validator,industry=cognition,icon=🔢,bg=#fff3e0`
- **中文名**：数字广度记忆测验 ｜ **EN**：Digit Span Memory Test
- **中文简介**：韦氏记忆量表核心分测验，含正背（注意力）与倒背（工作记忆）双条件，序列逐级加长，输出数字广度、最长正确序列与年龄常模百分位。
- **EN desc**：A core subtest of the Wechsler memory scales, with forward (attention) and backward (working memory) conditions, progressively longer digit sequences, and outputs for digit span, longest correct sequence and age-based percentile.
- **功能规格**：① 数字 1 位/秒 匀速呈现（可调 0.5/1/1.5 秒）② 正背 + 倒背 + 排序（第三条件，数字升序复述）③ 阶梯终止规则（同长度两次全错终止）④ 输出：正背广度、倒背广度、总广度、序列分 ⑤ 与 WAIS 常模对比 ⑥ 听觉呈现可选（SpeechSynthesis）⑦ 历史对比
- **A 级路径**：≥3000 且 input ≥3（速度选择、模式选择、长度设置、输入作答）+ 阶梯引擎 + 图
- **验收**：三条件独立计分；听觉与视觉呈现结果一致

---

### 🧘 心理与性格分析 `tools/psychology/`（6 个）

---
### T09 · SCL-90 心理健康自评量表 ⬜
- **路径**：`tools/psychology/scl90-assessment.html`
- **meta**：`cat=validator,industry=psychology,icon=🫀,bg=#f3e5f5`
- **中文名**：SCL-90 心理健康自评量表 ｜ **EN**：SCL-90 Symptom Checklist
- **中文简介**：专业在线 SCL-90 心理健康评估，共 90 题、9 个症状维度（躯体化、强迫、人际敏感、抑郁、焦虑、敌对、恐怖、偏执、精神病性），给出各维度因子分、总分、阳性项目数与筛查判定，附解读建议。
- **EN desc**：A professional online SCL-90 mental health assessment with 90 items across nine symptom dimensions — somatization, obsessive-compulsive, interpersonal sensitivity, depression, anxiety, hostility, phobic anxiety, paranoia and psychoticism — reporting factor scores, global indices, positive symptom counts and screening outcomes with interpretation.
- **功能规格**
  1. 90 题，5 级评分（1 没有 / 2 很轻 / 3 中等 / 4 偏重 / 5 严重），分 9 维度（每维度 6–13 题）+ 7 道附加题
  2. 进度条 + 断点续答（localStorage 存草稿）
  3. 计分：总分(90–450)、总均分、阳性项目数、阴性项目数、阳性症状均分、9 个因子分（= 维度总分 / 题数）
  4. 判定：任一因子分 > 2 提示该维度需关注；总分 > 160 或阳性项目数 > 43 提示需进一步评估
  5. **九维雷达图**（canvas 自绘）+ 维度释义表
  6. 分维度解读文字（每维度 3–5 句，含典型表现 + 建议）
  7. 导出 PDF（打印样式）/ CSV；结果分享卡
  8. 免责声明：筛查工具，不替代临床诊断
- **技术方案**：题目表 `ITEMS=[{i,text,dim}]` 常量；因子分映射表；雷达图 canvas 自绘
- **A 级路径**：≥6000（90 题数据 + 计分 + 雷达图 + 九维解读）
- **验收**：全 90 题计分与手算一致；中途刷新可续答；雷达图九轴正确

---
### T10 · 大五人格测试（15 维度 / 28 型）⬜
- **路径**：`tools/psychology/bigfive-personality-test.html`
- **meta**：`cat=validator,industry=psychology,icon=🧩,bg=#ede7f6`
- **中文名**：大五人格测试（15 维度 28 型）｜ **EN**：Big Five Personality Test (15 Facets, 28 Types)
- **中文简介**：基于大五人格（OCEAN）理论的专业测评，60 题覆盖 5 大维度及 15 个子维度，通过 28 种人格原型匹配算法给出你的主导类型、次要类型与完整剖面图。
- **EN desc**：A professional Big Five (OCEAN) assessment with 60 items covering five domains and 15 facets, matching your profile to 28 personality archetypes through a centroid-matching algorithm to report your dominant type, secondary type and full facet profile.
- **功能规格**
  1. 60 题，Likert 5 点（1 非常不同意 – 5 非常同意），5 大维度各 12 题、**15 个子维度**各 4 题（开放性：审美/求知/创造；尽责性：自律/条理/成就动机；外向性：热情/乐群/果断；宜人性：信任/利他/顺从；神经质：焦虑/脆弱/易怒）
  2. 反向计分题处理；T 分数转换（均值 50，SD 10）
  3. **28 种人格原型**：由 5 维高低组合（32 种去掉 4 种极端不可能组合）定义质心，用**加权欧氏距离**匹配 Top3 类型
  4. 结果：主导型 + 次要型 + 五维柱状图 + 15 子维度剖面条形 + 优势/盲点/适配职业/人际关系建议
  5. 结果卡片导出 PNG + 分享文案
- **技术方案**：`TYPES=[{key,name,en,centroid:{O,C,E,A,N},desc,strengths,blindspots,careers[]}]` 28 条常量；距离 `sqrt(Σ(w_i·(t_i−c_i)²))`，神经质权重 1.2
- **A 级路径**：≥6000（60 题 + 15 子维 + 28 型匹配 + 双图 + 解读库）
- **验收**：同一答案多次计算结果一致；28 型文案无重复；反向计分正确

---
### T11 · 你是哪款珍珠奶茶（趣味人格测验）⬜
- **路径**：`tools/psychology/bubble-tea-personality-quiz.html`
- **meta**：`cat=game,industry=psychology,icon=🧋,bg=#fff3e0`
- **中文名**：你是哪款珍珠奶茶 ｜ **EN**：What Bubble Tea Are You?
- **中文简介**：12 道轻松有趣的奶茶人格测验，测出你对应哪一款饮品（经典珍珠、芋泥波波、芝士葡萄、青提茉莉…），每种结果含性格标签、糖度冰度人格映射与专属社交分享卡。
- **EN desc**：A lighthearted 12-question bubble tea personality quiz that reveals which drink matches you — classic tapioca, taro boba, cheese grape, jasmine green and more — each result with personality tags, a sweetness/ice personality mapping and a shareable card.
- **功能规格**：① 12 题情境选择题，每题 3–4 个选项计分到 4 个隐藏轴（甜度/浓度/温度/料感）② **10 种奶茶结果**，每种含：名称、emoji、性格描述（4–6 句）、关键词标签、契合度百分比、推荐搭配 ③ 结果卡片 canvas 导出 PNG（适合社交传播）④ 复制文案 + 分享 ⑤ 重测对比（上次结果）
- **技术方案**：`RESULTS` 10 条常量（质心在 4 轴上），最近邻匹配；结果卡用 canvas 手绘渐变背景
- **A 级路径**：≥3000 且 input ≥3（12 题为 radio 组）+ 结果库 + 卡片渲染
- **验收**：10 种结果均可达（每种至少一条答题路径）；卡片导出清晰

---
### T12 · 九型人格测试 ⬜
- **路径**：`tools/psychology/enneagram-test.html`
- **meta**：`cat=validator,industry=psychology,icon=🔯,bg=#f3e5f5`
- **中文名**：九型人格测试 ｜ **EN**：Enneagram Personality Test
- **中文简介**：144 题标准九型人格测验（RHETI 简化版），测出你的主导型、翼型、压力/安全状态下的动态变化，含九型完整描述、核心动机与成长建议。
- **EN desc**：A 144-item Enneagram assessment (condensed RHETI) identifying your dominant type, wing, and stress/security dynamics, with full type descriptions, core motivations and growth suggestions.
- **功能规格**：① 144 题强制配对选择（每组两句选更贴近的一句）② 9 型得分 + 翼型判定（相邻两型较高者为翼，如 9w1）③ **三中心**（腹/心/脑）与 **动态变化**（压力态/安全态类型）④ 九芒星图（canvas 自绘，标出主导型与连线）⑤ 每型描述：核心恐惧/核心欲望/关键词/优势/盲点/成长路径 ⑥ 结果卡导出
- **A 级路径**：≥6000（144 题数据 + 计分 + 九芒星图 + 九型解读库）
- **验收**：翼型判定规则正确；九芒星图标注准确

---
### T13 · 霍兰德职业兴趣测试（RIASEC）⬜
- **路径**：`tools/psychology/holland-career-test.html`
- **meta**：`cat=validator,industry=psychology,icon=🧭,bg=#e0f7fa`
- **中文名**：霍兰德职业兴趣测试（RIASEC）｜ **EN**：Holland Code Career Test (RIASEC)
- **中文简介**：基于霍兰德 RIASEC 六型职业兴趣理论，60 题测出你的兴趣代码（如 SAE），匹配 120+ 职业方向，给出六边形剖面图、适配专业与典型职业清单。
- **EN desc**：Based on Holland's RIASEC model, this 60-item test produces your three-letter interest code (e.g. SAE), matches 120+ occupations and reports a hexagonal profile with suitable majors and representative careers.
- **功能规格**：① 60 题（喜欢/不喜欢/不确定三级）覆盖现实型R、研究型I、艺术型A、社会型S、企业型E、常规型C ② 输出三字母 Holland Code ③ **六边形剖面图**（canvas 自绘）④ 职业库 120+ 条（每条含职业名、代码、学历、说明）→ 按余弦相似度排序 Top10 ⑤ 大学专业建议 12 类 ⑥ 一致性/区分度指标（霍兰德理论指标）⑦ 结果导出
- **A 级路径**：≥6000（60 题 + 120 职业库 + 六边形图 + 匹配算法）
- **验收**：代码排序与得分一致；职业匹配结果合理（S 型高分应出现教师/社工）

---
### T14 · 成人依恋类型测试（ECR）⬜
- **路径**：`tools/psychology/attachment-style-test.html`
- **meta**：`cat=validator,industry=psychology,icon=💞,bg=#fce4ec`
- **中文名**：成人依恋类型测试（ECR）｜ **EN**：Adult Attachment Style Test (ECR)
- **中文简介**：基于 Brennan 等人 ECR 量表的 36 题亲密关系评估，测量依恋焦虑与依恋回避两个维度，判定安全型、焦虑型、回避型、恐惧型四种依恋风格，附关系模式解读与改善建议。
- **EN desc**：A 36-item intimate-relationship assessment based on the Experiences in Close Relationships (ECR) scale, measuring attachment anxiety and avoidance to classify secure, anxious, avoidant or fearful attachment styles, with relationship-pattern analysis and growth advice.
- **功能规格**：① 36 题 7 点 Likert，18 题焦虑维 + 18 题回避维（含 8 道反向题）② 二维散点定位图（canvas 自绘，四象限标注四种依恋风格，标点你的位置）③ 四种风格描述：典型表现、在冲突中的反应、伴侣体验、成长方向 ④ 两维度分条 + 常模参考区间 ⑤ 结果导出
- **A 级路径**：≥6000（36 题 + 反向计分 + 二维定位图 + 四型解读）
- **验收**：四象限判定与两维分数一致；反向题计分正确

---

### 👁️ 感官知觉 `tools/ophthalmology/`（4 个）+ `tools/ent/`（2 个）

---
### T15 · 专业视力表工具箱 ⬜
- **路径**：`tools/ophthalmology/eye-chart-toolkit.html`
- **meta**：`cat=reference,industry=ophthalmology,icon=📊,bg=#e3f2fd`
- **中文名**：专业视力表工具箱 ｜ **EN**：Professional Eye Chart Toolkit
- **中文简介**：面向验光师与家庭自测的浏览器端视力表工具箱，内置 Snellen、logMAR(ETDRS)、Jaeger 近视力、儿童图形、Tumbling E、Landolt C、散光放射线共 7 类临床图表，支持屏幕 DPI 校准、检查距离设定与结果记录。
- **EN desc**：A browser-based eye chart toolkit for optometrists and home screening, with seven clinical charts — Snellen, logMAR (ETDRS), Jaeger near vision, pediatric picture, Tumbling E, Landolt C and astigmatism fan — plus screen DPI calibration, viewing-distance settings and result logging.
- **功能规格**
  1. **7 类图表**：① Snellen（6/6–6/60，字母）② logMAR/ETDRS（0.1–1.0，Sloan 字母）③ Jaeger 近视力（J1–J10 文本段落）④ 儿童图形（苹果/房子/鸭子/鱼/星/车）⑤ Tumbling E（四向）⑥ Landolt C（八缺口方位）⑦ 散光放射线表（Astigmatic fan）
  2. **屏幕 DPI 校准**：输入信用卡宽度（85.6mm）拖动校准条 → 计算 px/mm → 保证视标尺寸物理精确（**这是专业性的核心**）
  3. 检查距离设定（6m / 5m / 3m / 40cm 近用），自动换算视标大小
  4. 单行/单行遮蔽模式：点击行号只显示该行；随机化字母序列（防背诵）
  5. 镜像模式（供被检者看屏幕反射）
  6. 记录：每行正确数 → 输出 Snellen 分数、logMAR 值、小数视力、5 分记录法四种表示
  7. 结果换算表（四种表示法对照参考表）
- **技术方案**：视标几何严格按「5 分视角 1 分缺口」原理：`heightPx = 5/60 * distanceRad * pxPerMm`；SVG 绘制保证缩放不失真
- **A 级路径**：≥6000（7 套图表渲染 + DPI 校准 + 换算引擎 + 对照表）
- **验收**：DPI 校准后 6/6 行高度 = 检查距离 × 5/60 × tan 换算值（误差 <2%）；7 类图表均可切换

---
### T16 · 21 题自适应视力筛查 ⬜
- **路径**：`tools/ophthalmology/vision-screening-21.html`
- **meta**：`cat=reference,industry=ophthalmology,icon=👁️,bg=#e3f2fd`
- **中文名**：21 题自适应视力筛查（单眼度数估算）｜ **EN**：21-Question Adaptive Vision Screening
- **中文简介**：通过 21 道自适应问题分别评估左右眼，估算每只眼的球镜近视度数、散光轴位与散光度数，输出可保存的筛查报告与验光建议。
- **EN desc**：Twenty-one adaptive questions assess each eye separately to estimate spherical myopia, astigmatism axis and cylinder power, producing a savable screening report and refraction guidance.
- **功能规格**
  1. 分左右眼各 21 题（共 42 题），题型：① E 字/字母方向识别（尺寸递减）② 放射线哪条最黑（散光轴位）③ 红绿双色对比（球镜过矫/欠矫）④ 圆形/线条失真判断 ⑤ 小字阅读最小可辨行
  2. **自适应**：答对降一档视标尺寸（0.1 logMAR 步进），答错升一档，用 **阶梯法（staircase）+ 反转点均值** 估阈值
  3. 散光：12 方向放射线选最黑 → 轴位；不同轴位清晰度差 → 柱镜等级（0.25D 步进，0–3.00D）
  4. 输出：右眼 / 左眼 的 `球镜 S / 柱镜 C / 轴位 A`、等效球镜 (SE = S + C/2)、预估裸眼视力、建议（是否需配镜/复查）
  5. 处方卡样式结果 + 打印/导出 PNG
  6. 强免责：筛查值，配镜必须医学验光
- **技术方案**：阶梯法状态 `{level, reversals[], lastDir}`，阈值 = 后 6 个反转点均值；logMAR ↔ Snellen ↔ 小数 三向换算
- **A 级路径**：≥6000（自适应引擎 + 放射线/红绿渲染 + 换算 + 处方卡）
- **验收**：左右眼独立计分；阶梯收敛后不再震荡；结果在合理范围

---
### T17 · 听觉时间分辨率测试 ⬜
- **路径**：`tools/ent/temporal-resolution-hearing.html`
- **meta**：`cat=validator,industry=ent,icon=👂,bg=#e8f5e9`
- **中文名**：听觉时间分辨率测试 ｜ **EN**：Auditory Temporal Resolution Test
- **中文简介**：基于 Web Audio 的实验性听觉测试，用间隙检测（Gap Detection）与调制检测（Modulation Detection）评估听觉系统的时间分辨能力，输出毫秒级阈值与年龄常模对照。
- **EN desc**：A Web Audio experimental hearing test using gap detection and amplitude-modulation detection to assess temporal resolution of the auditory system, reporting millisecond thresholds against age norms.
- **功能规格**
  1. **音量校准**：播放 1kHz 参考音，用户调到刚能听见 → 建立个人听阈基准（避免设备差异）
  2. **间隙检测**：白噪声/纯音中嵌入 2–50ms 静音间隙，三选一强制选择（3AFC），阶梯法求 50% 正确阈值
  3. **调制检测**：4/16/64Hz 振幅调制，测调制深度阈值（%）
  4. **音调序列辨别**：两个短音的音高走向（上/下），测最短可辨时长
  5. 输出：三项阈值 + 时间分辨率综合评分 + 年龄常模对照（青年/中年/老年）+ 结果图（雷达或柱状）
  6. 强提示：需佩戴耳机；环境噪声会显著影响结果
- **技术方案**：`AudioContext` + `AudioBuffer` 精确生成（间隙用 buffer 采样级裁剪，不用定时器）；3AFC 阶梯法（3-down-1-up → 79.4% 正确点）
- **A 级路径**：≥6000（音频合成 + 三套阶梯引擎 + 校准 + 图）
- **验收**：间隙阈值落在 2–10ms 典型区间；耳机检测提示存在

---
### T18 · 纯音听力筛查（听力图）⬜
- **路径**：`tools/ent/pure-tone-audiometry.html`
- **meta**：`cat=validator,industry=ent,icon=🎧,bg=#e8f5e9`
- **中文名**：纯音听力筛查 · 听力图 ｜ **EN**：Pure-Tone Hearing Screening (Audiogram)
- **中文简介**：用 Web Audio 生成 125Hz–8kHz 共 8 个频率的纯音，逐耳测听阈，自动绘制标准听力图，按 WHO 分级判定听力损失程度与类型。
- **EN desc**：Generates pure tones from 125 Hz to 8 kHz with the Web Audio API to measure hearing thresholds for each ear, plots a standard audiogram and classifies degree and type of hearing loss using WHO criteria.
- **功能规格**
  1. 频率：125 / 250 / 500 / 1000 / 2000 / 4000 / 6000 / 8000 Hz（骨导不做）
  2. 强度：−10 至 100 dB HL，5dB 步进，**Hughson-Westlake 阶梯法**（降 10 升 5，同强度 3 次中 2 次听见为阈值）
  3. 左右耳分别测（播放时明确提示耳别）
  4. **标准听力图**：canvas 绘制（X 轴频率对数，Y 轴 dB，含言语香蕉区阴影）
  5. 判定：纯音平均 PTA（500/1k/2k/4k）→ WHO 分级（正常 ≤25 / 轻度 26–40 / 中度 41–60 / 重度 61–80 / 极重度 >80）
  6. 听力损失类型提示（传导性/感音性/混合性，基于气导形态的文本化判断）
  7. 结果导出 PNG + CSV；历史对比
  8. 强制提示：必须佩戴耳机、需在安静环境、不能替代专业纯音测听
- **技术方案**：`OscillatorNode` + `GainNode` 精确控制 dBFS→dB HL 映射（需每频率校准偏移量表）；听力图 canvas 手绘对数轴
- **A 级路径**：≥6000（Hughson-Westlake 引擎 + 8 频 2 耳 + 听力图绘制 + WHO 分级）
- **验收**：阶梯法收敛阈值稳定；听力图坐标与输入一致；WHO 分级边界正确

---
### T19 · 阿姆斯勒方格自测 ⬜
- **路径**：`tools/ophthalmology/amsler-grid-test.html`
- **meta**：`cat=reference,industry=ophthalmology,icon=▦,bg=#e3f2fd`
- **中文名**：Amsler 阿姆斯勒方格表（黄斑自测）｜ **EN**：Amsler Grid Macula Self-Test
- **中文简介**：标准阿姆斯勒方格表，用于黄斑变性等中心视野病变自测，支持单眼注视、方格规格切换、异常区域标记与历史对比，可导出报告供医生参考。
- **EN desc**：A standard Amsler grid for self-monitoring macular conditions such as age-related macular degeneration, with monocular fixation, grid size options, marking of distorted areas and history comparison, plus an exportable report for your doctor.
- **功能规格**：① 标准 10×10 方格（每格 5mm@30cm，对应中心 10° 视野）② 三种变体：标准黑白格 / 带对角线格 / 红色十字格（更易发现暗点）③ 单眼遮盖指引（左右眼分步）④ **交互标记**：用户可在网格上涂抹「变形区/暗点区/缺失区」三种标记 ⑤ 保存本次标记图 + 与上次叠加对比（canvas 图层）⑥ 阳性指征说明（直线变弯、方格缺失、中心暗点）+ 就医建议 ⑦ 导出 PNG 报告
- **A 级路径**：≥3000 且 input ≥3（眼别、格型、标记类型）+ canvas 标记层 + 对比逻辑
- **验收**：三种格型切换正常；标记可保存并在下次叠加显示

---
### T20 · 散光放射线自测表 ⬜
- **路径**：`tools/ophthalmology/astigmatism-chart.html`
- **meta**：`cat=reference,industry=ophthalmology,icon=✳️,bg=#e3f2fd`
- **中文名**：散光放射线自测表 ｜ **EN**：Astigmatism Fan Chart Self-Test
- **中文简介**：标准散光放射线（太阳纹）自测表，通过判断各方向线条的清晰度差异，初步评估是否存在散光及大致轴位方向与严重度，含单眼分步指引与结果解读。
- **EN desc**：A standard astigmatic fan chart: compare the sharpness of radial lines in different directions to screen for astigmatism, estimate its approximate axis and severity, with monocular step-by-step guidance and result interpretation.
- **功能规格**：① 12 方向放射线（每 15°）+ 钟表位标注 ② 单眼分步（右眼→左眼）+ 遮盖指引 ③ 用户勾选「最清晰的方向」与「最模糊的方向」（可多选）④ 结果：是否有散光迹象、估计轴位（最模糊方向垂直位，180−θ）、严重度自评（1–3 级）⑤ 放射线渲染可切换：黑白 / 红绿双色（辅助判断）⑥ 与 T15 视力表、T16 筛查互链 ⑦ 结果记录与导出
- **A 级路径**：≥3000 且 input ≥3 + canvas/SVG 放射线渲染 + 判定逻辑 + 互链
- **验收**：轴位换算说明清晰；红绿模式切换正常

---

### 🎨 色觉与色彩可访问性 `tools/colorvision/`（4 个，新建行业）

---
### T21 · Farnsworth D-15 色相排列测试 ⬜
- **路径**：`tools/colorvision/farnsworth-d15-test.html`
- **meta**：`cat=validator,industry=colorvision,icon=🎨,bg=#f3e8ff`
- **中文名**：Farnsworth D-15 色相排列测试 ｜ **EN**：Farnsworth D-15 Color Arrangement Test
- **中文简介**：专业色觉分型测试，拖拽 15 个色相帽按渐变顺序排列，通过色相轨迹图（polar diagram）判定正常色觉或红色盲/绿色盲/蓝色盲及其严重度。
- **EN desc**：A professional color vision classification test: drag 15 hue caps into a gradual sequence and use the polar hue-trace diagram to classify normal vision or protan / deutan / tritan deficiency with severity grading.
- **功能规格**
  1. 15 个色相帽（Munsell 色坐标，固定参考帽 1 个 + 14 个待排）
  2. 拖拽排序 + 点击交换两种操作（移动端友好）
  3. **计分**：`总错误分 TES = Σ(√( (Δx)² + (Δy)² ) − 1)`（CIE 色度图上相邻帽距离减 1）
  4. **色相轨迹图**：canvas 绘制 polar 图，正常者轨迹绕中心一圈，红色盲/绿色盲轨迹呈特定轴向（用 **Bowman 轴角法**判定：主轴与 0°/180° 接近 = protan，与 90°/270° 接近 = deutan，垂直向 = tritan）
  5. 判定输出：正常 / 疑似红色盲 / 疑似绿色盲 / 疑似蓝色盲 + 严重度（轻度/中度/重度，按 TES 阈值）
  6. 与石原筛查（已有页）互链说明：D-15 判型更精细
  7. 结果导出 PNG（含轨迹图）
- **技术方案**：15 帽 CIE 1931 xy 常量表；极坐标图 canvas 手绘；主轴用 PCA 或最小二乘拟合
- **A 级路径**：≥6000（色度常量 + 拖拽排序 + 轨迹图绘制 + 分型算法）
- **验收**：正确顺序 TES=0；故意排错时轨迹图方向符合 protan/deutan 判定

---
### T22 · 色盲模拟器 Pro（旗舰）⬜
- **路径**：`tools/colorvision/colorblind-simulator.html`
- **meta**：`cat=design,industry=colorvision,icon=👁️,bg=#ede9fe`
- **中文名**：色盲模拟器 Pro：8 型模拟 · 图片 · WCAG · 安全色 ｜ **EN**：Color Blindness Simulator Pro: 8 Types, Images, WCAG & Safe Colors
- **中文简介**：专业色觉缺陷模拟器，支持 8 种色盲类型（红色盲/红色弱/绿色盲/绿色弱/蓝色盲/蓝色弱/全色盲/蓝锥单色）实时模拟，可上传图片批量预览、做 WCAG 2.1 对比度检查并给出色盲安全配色建议。
- **EN desc**：A professional color vision deficiency simulator with 8 real-time modes — protanopia, protanomaly, deuteranopia, deuteranomaly, tritanopia, tritanomaly, achromatopsia and blue-cone monochromacy — plus image upload with batch previews, a WCAG 2.1 contrast checker and colorblind-safe palette recommendations.
- **功能规格**
  1. **8 型模拟**（Brettel/Viénot 色觉变换矩阵，含 anomaly 的严重度滑杆 0–100%）：protanopia / protanomaly / deuteranopia / deuteranomaly / tritanopia / tritanomaly / achromatopsia / blue-cone monochromacy
  2. **三种输入**：① 单色（HEX/RGB/HSL 输入 + 取色器）② 调色板（多色并列，最多 12 色）③ **图片上传**（FileReader → canvas 逐像素变换，输出 8 型并列网格 + 单张放大对比 + 原图/模拟图左右滑块对比）
  3. **WCAG 2.1 检查**：选前景/背景（含模拟后的颜色）→ 计算对比度 → 判定 AA(4.5:1) / AA Large(3:1) / AAA(7:1) / 失败，并标出在 8 型色觉下的对比度变化
  4. **安全色建议**：给定基准色 → 生成 6 个在 8 型下均可区分的替代色（在模拟空间里最大化最小色差）+ 明暗区分建议
  5. **可辨识度评分**：对输入的调色板，计算各型下两两色差 ΔE（CIE Lab）→ 输出「哪些色对在哪些型下会混淆」表格
  6. 导出：8 型并列图 PNG、分析报告 JSON
- **技术方案**：LMS 色彩空间变换（sRGB→linear→LMS→模拟→linear→sRGB）；图片处理用 `ImageData` 逐像素（配合 Web Worker 防卡顿，或限制尺寸 ≤1600px）
- **A 级路径**：≥6000（8 套变换矩阵 + 图片处理 + WCAG + ΔE + 安全色搜索）
- **验收**：8 型模拟结果符合已知样例（如 deutan 下红绿难分）；图片处理 1600px 内 <1s；WCAG 数值与标准公式一致

---
### T23 · 调色板色觉可辨识度检查器 ⬜
- **路径**：`tools/colorvision/palette-cvd-checker.html`
- **meta**：`cat=design,industry=colorvision,icon=🧩,bg=#f3e8ff`
- **中文名**：调色板色觉可辨识度检查器 ｜ **EN**：Palette Color Vision Distinguishability Checker
- **中文简介**：输入或粘贴一组配色，检查它在 8 种色觉类型及灰度下的可辨识度：输出两两色差矩阵、混淆预警、灰度可分辨性（明度阶梯）评分，并给出可访问的修正建议。
- **EN desc**：Paste or pick a palette and check its distinguishability under 8 color vision types and in grayscale: a pairwise color-difference matrix, confusion warnings, a lightness-ladder score for grayscale separation, and actionable accessibility fixes.
- **功能规格**：① 输入：HEX 列表（手输/粘贴/从图片提取主色，最多 12 色）② 8 型 + 灰度下的调色板并排预览 ③ **色差矩阵**：每对颜色在各型下的 CIE ΔE（<10 标红预警）④ **灰度检查**：转换明度 L*，检查相邻明度差是否 ≥10（保证黑白打印/全色盲可分）⑤ 综合评分（0–100）+ 逐条改进建议（如「#E33 与 #3A3 在 deutan 下 ΔE=4.2，建议拉开明度」）⑥ 一键应用建议修正 ⑦ 导出报告
- **技术方案**：sRGB→Lab（含 D65 白点）；ΔE76（1976）为主，附 ΔE2000 参考；明度阶梯排序
- **A 级路径**：≥6000（色彩空间转换 + 8 型变换 + 矩阵渲染 + 评分算法 + 修正建议）
- **验收**：ΔE 计算与标准样例一致；灰度阶梯检查合理

---
### T24 · 色盲安全配色生成器 ⬜
- **路径**：`tools/colorvision/cvd-safe-palette.html`
- **meta**：`cat=design,industry=colorvision,icon=🌈,bg=#e8f5e9`
- **中文名**：色盲安全配色生成器 ｜ **EN**：Colorblind-Safe Palette Generator
- **中文简介**：生成在 8 种色觉类型下都能清晰区分的配色方案，支持分类配色（顺序/发散/定性）、锁定色、明暗交替策略与 WCAG 校验，一键复制 HEX/CSS 变量/JSON。
- **EN desc**：Generate color schemes that stay clearly distinguishable across 8 types of color vision, with sequential / diverging / qualitative modes, color locking, a lightness-alternation strategy and WCAG checks, exported as HEX, CSS variables or JSON.
- **功能规格**：① 三种配色类型：顺序(sequential) / 发散(diverging) / 定性(qualitative) ② 色相起点 + 色数(3–10) + 明度范围滑杆 ③ **约束求解**：在模拟空间内最大化「两两最小 ΔE」，用贪心 + 迭代微调（保证 8 型下最小 ΔE ≥ 12）④ 锁定任意色不变，重生成其余 ⑤ 明暗交替模式（保证灰度可分）⑥ 实时预览：8 型并列 + 图表模拟（柱状图/折线图/饼图 三种真实图表场景预览）⑦ WCAG 文字对比度校验 ⑧ 导出：HEX / CSS 变量 / JSON / PNG
- **技术方案**：OKLCH 色彩空间生成（感知均匀）→ 变换到 8 型模拟空间 → 评估最小 ΔE → 迭代优化（最多 200 轮）
- **A 级路径**：≥6000（OKLCH 生成 + 8 型评估 + 约束优化 + 图表场景预览 + 导出）
- **验收**：生成结果在 8 型下最小 ΔE ≥ 12；图表预览真实渲染；导出格式可用

---

### 🎲 趣味与创意 `tools/fun/`（2 个）

---
### T25 · 每日谜题挑战 ⬜
- **路径**：`tools/fun/daily-riddle.html`
- **meta**：`cat=game,industry=fun,icon=🧩,bg=#e0f2fe`
- **中文名**：每日谜题挑战 ｜ **EN**：Daily Riddle Challenge
- **中文简介**：每天更新一道谜题或脑筋急转弯，支持三级提示、积分、连击记录与难度选择，答完可查看解析与排行榜式百分位，成绩本地保存。
- **EN desc**：A new riddle or brain teaser every day with three levels of hints, scoring, streak tracking and difficulty selection, plus explanations, percentile ranking and locally saved progress.
- **功能规格**：① **每日题**：用日期做种子（YYYYMMDD → 确定性 PRNG）选题，全球同日同题；另有「练习模式」随机刷题 ② 题库 ≥ 120 题，分三难度（简单/中等/困难），含谜题、脑筋急转弯、逻辑推理三类 ③ 三级提示（每级扣 20% 分值）④ 积分：基础分 × 难度系数 × 提示折扣 + 连击加成（连续答对天数 ×10%）⑤ **连击日历**：当月日历热力图显示答题情况 ⑥ 答案提交后显示解析 + 趣味知识 ⑦ 本地存档：总积分、最长连击、已答题目、正确率 ⑧ 结果分享卡（不剧透答案）
- **技术方案**：mulberry32 PRNG + 日期种子；题库常量数组；日历热力图 canvas 或 CSS grid
- **A 级路径**：≥6000（120 题库 + 日期种子 + 提示/计分/连击 + 日历热力图）
- **验收**：同日不同浏览器题目一致；连击跨天正确累计；分享卡不泄露答案

---
### T26 · 1A2B 猜数字（Bulls & Cows）⬜
- **路径**：`tools/fun/1a2b-guess.html`
- **meta**：`cat=game,industry=fun,icon=🔢,bg=#fff8e1`
- **中文名**：1A2B 猜数字 ｜ **EN**：1A2B Number Guessing Game (Bulls & Cows)
- **中文简介**：经典 1A2B 逻辑推理猜数字游戏：猜出电脑生成的 4 位（或 5 位）不重复数字，每次给出 xAyB 提示，含推理辅助表、步数统计、难度模式与最佳记录。
- **EN desc**：The classic 1A2B Bulls and Cows logic game: guess a 4- or 5-digit number with no repeated digits, receiving xAyB feedback after each guess, with a deduction helper grid, move counter, difficulty modes and personal bests.
- **功能规格**：① 位数可选 4/5 位，是否允许 0 开头、是否允许重复数字（三个难度档）② 输入校验 + 键盘/虚拟数字键盘（移动端）③ 每次猜测返回 `xAyB`（A=数字与位置都对，B=数字对位置错）④ **推理辅助表**：自动维护候选集，列出「已排除的数字」「位置已确定的数字」「剩余可能组合数」，并可按候选数智能推荐下一猜（最小化最大残留的启发式）⑤ 步数统计 + 用时 + 提示次数 ⑥ 最佳记录（按难度分档存 localStorage）⑦ 历史对局回放（逐步动画）⑧ 分享成绩
- **技术方案**：候选集过滤（`filter(c => bulls(c,g)===A && cows(c,g)===B)`）；推荐用 minimax 精简版（候选 ≤ 2000 时全评估，否则随机采样 300）
- **A 级路径**：≥6000（游戏引擎 + 候选推理表 + minimax 推荐 + 回放动画）
- **验收**：xAyB 计算正确；辅助表候选数随猜测单调下降；推荐策略平均步数 <6（4 位）

---

## 7. 全局收口任务 G01 – G07（26 个工具全部完成后集中执行）

| # | 任务 | 落点 | 验收 |
|---|---|---|---|
| **G01** | 注册 2 个新行业 | `_build.py` → `INDUSTRY_DEFS`；`i18n/industry-en.json`；新建 `tools/cognition/`、`tools/colorvision/`；新建 6 个 i18n 文件骨架 | build 后两个目录自动生成 `index.html`，行业名显示中文非 slug |
| **G02** | 首页热门工具 | `js/app.js` → `HOT_TOOLS` 数组**头部**追加 26 条 `{n,en,d,ed,i,c,u,ic,b}`（en/ed 必填，否则英文站显示中文） | 中英切换时标题/描述同步切换；首屏 spotlight 露出前 8 个 |
| **G03** | 首页热门分类 | `js/app.js` → `HOT_INDUSTRIES` 追加 `cognition`、`colorvision`、`psychology`、`ophthalmology`；`CAT_INFO` 如需新增 cat 同步补 | 首页分类 tag 出现四个新分类，点击可筛选 |
| **G04** | 英文 override | `i18n/tools/_en_override.json` + `slug-en.json` 各补 26 条（`indent=1`；英文禁止 slug 直译） | `_test_static.py` 映射缺失 = 0 |
| **G05** | 正文 i18n | `i18n/tools/<ind>.json`（双语 h1/title/intro/note/desc）+ `<ind>-body.json` + `<ind>-phrases.json` 补齐（phrases 覆盖页面内**全部**中文串） | 切英文后页面无残留中文（人工抽验 5 页） |
| **G06** | 构建 + 五道门禁 | `python3 scripts/run_gates.py`（build → `_test_static.py` → `_audit_links.py --check` → `_audit_assets.py --check` → `node scripts/verify_calc.js`），本机需先 `npm ci` | 五道全 PASS；静态 0 失败 0 告警；死链 0；资产 0 异常；公式回归 0 失败 |
| **G07** | 提交发布 | `git add -A && git commit && git push origin master`；提醒老板手动跑 `python3 _submit_indexnow.py` | GitHub Pages 更新；提醒已发出 |

---

## 8. 分批执行顺序

| 批次 | 任务 | 说明 |
|---|---|---|
| **第 0 批** | G01 | 先建骨架，后续工具才有归属；**先跑一次 build 验证行业注册成功** |
| **第 1 批** | T22 T23 T24 T21 | 色觉无障碍（新建行业 + 旗舰功能），先打样验证质量基线 |
| **第 2 批** | T01 T02 T03 T04 | 认知核心四件 |
| **第 3 批** | T05 T06 T07 T08 | 认知补充四件 |
| **第 4 批** | T09 T10 T11 | 心理主力（SCL-90 / 大五 / 奶茶） |
| **第 5 批** | T12 T13 T14 | 心理补充三件 |
| **第 6 批** | T15 T16 T19 T20 | 视力四件 |
| **第 7 批** | T17 T18 | 听力两件 |
| **第 8 批** | T25 T26 | 趣味两件 |
| **第 9 批** | G02 G03 G04 G05 | 首页露出 + i18n 收口 |
| **第 10 批** | G06 G07 | 门禁 + 提交发布 |

**每批执行纪律（不可跳过）**：逐个工具开发 → 每个工具写完立刻补自己的 4 处 i18n（en_override / slug-en / industry.json 三件套）→ 批内全部完成后 `python3 scripts/run_gates.py`（五道门禁）→ `git commit`。**禁止跨批堆积后一次性提交。**

---

## 9. 单工具验收清单（每个 T 任务完成前自检）

- [ ] 文件在 `tools/<industry>/<slug>.html`，head 骨架含全部必需 meta 与三个 TOOLBOX 锚点
- [ ] `<title>` 英文 & 以 ` - ToolBox` 结尾；`<meta name="title-zh">` 存中文
- [ ] `../../css/common.css` + `../../js/common.js` 引用正确
- [ ] `input+select+textarea` 数量 ≥3（A 级短路径时）
- [ ] 独有脚本 ≥6000 字符（或含 canvas / formula-box / data-viz）
- [ ] 功能规格逐条实现，无占位、无 TODO
- [ ] 移动端实测可用（触摸 ≥44px，无横向滚动）
- [ ] 深色/浅色主题均正常
- [ ] `i18n/tools/_en_override.json` 已补（indent=1）
- [ ] `i18n/tools/slug-en.json` 已补（indent=1）
- [ ] `i18n/tools/<ind>.json` + `-body.json` + `-phrases.json` 已补
- [ ] 切英文后页面无残留中文
- [ ] 医疗/心理类已加免责声明
- [ ] `python3 _build.py` 后该工具出现在 `json/industry-<ind>.json` 与 `sitemap.xml`
- [ ] `python3 _test_static.py` 0 失败 0 告警

---

## 10. 附：本次剔除项速查（避免后续重复提议）

已存在不再做：`fun/memory-game`、`fun/reaction-tester`、`fun/click-speed`、`fun/cps-test`、`ophthalmology/ishihara-test`（已程序化生成）、`design/contrast-checker`、`design/color-contrast-check`、`design/color-palette-generator`（仅生成，校验另立 T23）。
不可行：`colorfuzz`（跨域+CORS+`X-Frame-Options`，纯前端无解）。
已合并：dichroma / colorblind_image_tester → T22；Open-Colour-Labs → 已有 ishihara-test。
