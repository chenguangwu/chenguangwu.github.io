# DEV-PLAN — ToolBox 下一阶段开发计划

> 载体：有活跃任务才填，无活跃任务时清空。当前由「笨鸟」接管全部开发（含 i18n 英文），无并发 agent。
> 构建/门禁纪律：仅 `git add <具体文件>`，**禁止 `git add -u`**；动仓库前先 `git fetch`+`status` 确认无并发改动、本地不落后；不动他人/其他会话已 push 的成果。

## 一、现状基线（2026-08-28 实测）

| 指标 | 数值 | 备注 |
|---|---|---|
| 工具总数 | 5023 | A 级 100%，质量门禁全绿 |
| 行业目录 | 276 | |
| 指南页 | 149 页 | 已覆盖 11 行业核心场景 |
| GSC 收录 | ~6154 URL 判「unknown」 | 核心瓶颈：收录率极低 |
| i18n 英文-字典 | override 5066 条 + per-industry 651 文件/28372 键 + tool-i18n.js 9667 行 | 数据齐备 |
| i18n 英文-**构建期预渲染** | **仅 489/5316 页 `<title>` 为英文** | ⚠️ 瓶颈：Google 首抓仍见中文 |

## 二、构建与门禁命令（每次开发必跑）

```bash
python3 _build.py                      # 重建索引/sitemap/SEO 注入
python3 _test_static.py                # 标题/元数据/结构合规，须 0 失败 0 告警
python3 _audit_links.py --check        # 死链门禁，须 exit 0
python3 _audit_assets.py --check       # 资产完整性门禁，须 exit 0
node js/verify_calc.js                 # 公式回归（改工具页后）
# 提交：仅 git add 改动文件；推送前先 git fetch + pull --rebase
```

## 三、下一阶段计划（按 ROI 排序）

### P0 — GSC 收录提升（核心瓶颈，直接影响流量/变现）
- **根因**：github.io 子域权重低 + 全站模板化页，Google 不爱收（6154 URL unknown）。
- **我可直接做（纯前端、零成本）**：
  1. 站内内链权重强化（相关工具互链、分类页串联、面包屑闭环）
  2. sitemap 优先级/lastmod 调优（已有 `sitemap_lastmod.json` 持久化，功能优化页手动提级）
  3. 结构化数据（WebApplication/BreadcrumbList）补全与校验
  4. GSC 重点 URL 分批 inspect + 重新提交 sitemap
- **待您拍板的根因杠杆**：是否上独立域名（绕过 github.io 权重惩罚，属根因级）。

### P1 — i18n 英文深化（归「笨鸟」接管，当前最大遗漏点）
- **现状**：英文翻译字典已齐（override 5066 + per-industry 28372 键 + tool-i18n.js 9667 行），运行时切换可用；但 `_build.py` 仅对 **489 个 Top 工具页**做构建期英文 `<title>` 预渲染，其余 4827 页 Google 首抓仍是中文。
- **任务（数据驱动、分批）**：
  1. 扩展 `_build.py` 的 `apply_en_override` / 预渲染白名单，将 5023 工具页的 `<title>`、`<meta description>` 在构建期注入英文（或全量双语），让 Google 首抓即见英文
  2. 同步 `og:locale:alternate` 英文落地内容；确认 `html lang` 切换语义正确
  3. 跑 `gen_en_override.py` 补全任何标题/简介英文缺失项（键=行业/basename）
- **价值**：英文流量广告单价高，国际 SEO 直收；字典已备齐，主要是「构建期注入」这步没做完。
- **风险与纪律**：改 `_build.py` 须先 `git fetch`+`status` 确认干净；改完必跑 `python3 _build.py` + 四道门禁 + `verify_calc.js`；构建产物（sitemap/json）变化须随提交一起 commit，不挑文件回退。

### P2 — 工具页 meta description 精修（数据驱动）
- 先核实**页面实际 `<meta name=description>` 长度**（非 json 的 `desc` 字段），确认多少页真 <30 字，再分批精修。等 P0/P1 起量后做更有意义。

## 四、明确不做的（避免重复投入）
- **AdSense 接入**（R8 已定零成本；且收录低时接了也没量）
- **继续堆新工具**（>5031，A 级已 100%，边际价值低、易引入重复/质量风险）
- **URL 命名规范化 / basename 去重（301 迁移）**（SEO 风险高，已跳过）
- **math 分类重构 / 空壳清理**（前提已不成立，自然清零）
