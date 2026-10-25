# ToolBox 优化任务总控（MASTER）

> 本文件是 `plan/` 任务体系的唯一进度登记处。**只分析不开发**：本目录全部文件为问题清单 + 解决方案 + 受影响工具路径，供后续按批开发。
> 更新纪律：每完成一个任务，把对应行改为 ✅ 并注明 commit；新发现的问题按归属追加到对应文件，不新开重复文件。

## 体系结构

- `plan/G0x-*.md`：**全站共性问题**（多个分类存在相似问题）专题任务文件。
- `plan/categories/<大分类>/<小分类>.md`：**分类问题文件**，含该分类下所有工具的问题、功能缺陷与优化点。
- 热门分类顺序（按工具页数 + 搜索需求排序，规则 6）：IT开发 > 金融财务 > 医疗健康 > 设计创意 > 生活消费 > 商业运营 > 教育学习 > 工程制造 > 自然科学 > 农业养殖 > 文娱爱好 > 长尾行业。

## 全站专题（G 系列）

| 文件 | 主题 | 状态 |
|---|---|---|
| G01-公式与计算正确性裁量项.md | 16 批精度审计后仍待老板裁定的口径/阈值/条目结构 | 🔴 待裁断 |
| G02-重定向存根清理与索引合规.md | 超期存根删除 + 死链提交流程 | 🔴 待办（pets 2026-11-10 到期） |
| G03-构建数据源还原坑.md | HTML 手改被 _build.py 冲掉（json/i18n 源未改） | 🔴 待办 |
| G04-verify用例与判别力债务.md | 逃生项/弱用例/坏用例存量与补强规则 | 🟡 规则已固化，存量见文内 |
| G05-EN态i18n与国际化质量.md | 英文态残留/词典覆盖/繁体口径 | 🟡 部分通过门禁，深水区见文内 |
| G06-留存与竞争力升级.md | **核心**：用户「看一眼就走」的破局方案 | 🔴 待开发 |
| G07-性能与移动端.md | 首屏速度/移动端可用性/弱网 | 🔴 待排查 |

## 分类任务进度

| 大分类 | 文件 | 状态 |
|---|---|---|
| 01-IT开发 | it.md / ai.md / encode-telecom-security-data.md | 🔴 待开发 |
| 02-金融财务 | finance.md / banking-investment-securities.md / tax-accounting-audit.md / insurance.md | 🔴 待开发 |
| 03-医疗健康 | scales.md / lab-diagnosis.md / drug-dosing.md / specialties.md | 🔴 待开发 |
| 04-设计创意 | design.md / image.md | 🔴 待开发 |
| 05-生活消费 | photo-video.md / food-travel.md / sports-fitness.md / home-decor.md | 🔴 待开发 |
| 06-商业运营 | marketing-sales.md / ecommerce-logistics.md / hr-legal.md / realestate.md | 🔴 待开发 |
| 07-教育学习 | edu-language.md / research-library.md | 🔴 待开发 |
| 08-工程制造 | machinery-metalwork.md / electrical-electronics.md / construction-energy.md / aero-robotics.md | 🔴 待开发 |
| 09-自然科学 | science-math-statistics.md / physics-optics-quantum.md / earth-geo.md | 🔴 待开发 |
| 10-农业养殖 | agriculture.md / fishery-aquaculture.md / livestock-eco-forestry.md | 🔴 待开发 |
| 11-文娱爱好 | fun-entertainment.md / culture-collection.md | 🔴 待开发 |
| 12-长尾行业 | _others.md（<20 页的其余 190+ 行业） | 🟡 仅收录已知问题 |

## 已完成基线（本轮分析前的存量战果，避免重复开发）

- ✅ formula-eq 短框升级 1316 页（S2–S33，commit 92546a6513）
- ✅ 图表/预设扩补 93 页真缺池闭环（八批 65 页注入 + 28 页甄别为不需要，`_chart_presets_screening.md`）
- ✅ hydraulic 5 个模板壳页重建（004bc99736）
- ✅ 公式精度审计 16 批 ~1560 页，68 处真缺陷已修复并 verify 同步（含血糖换算方向、CHA₂DS₂-VASc、Wells、M-CHAT 方向倒置、CMC 色差、GDD、农机效率等）
- ✅ rater-22/detector-time/rater-17/echo-report/egfr 误标等缺陷清算
- ✅ 门禁 218/218 多轮全过；判别器逃生项清零
- ⚠️ 未完成收尾：本地 2 个提交待推送（1e87e1cdc1 等），恢复时先 `git fetch` 核对远端（origin 曾被外部推进）

> 状态图例：🔴 待开发 ｜ 🟡 进行中/部分完成 ｜ ✅ 已完成（注明 commit）
