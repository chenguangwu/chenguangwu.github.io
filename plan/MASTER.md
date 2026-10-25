# ToolBox 优化任务总控（MASTER）

> 本文件是 `plan/` 任务体系的唯一进度登记处。**只分析不开发**：本目录全部文件为问题清单 + 解决方案 + 受影响工具路径，供后续按批开发。

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

## 全站审计覆盖进度（目标：所有工具审计一遍）

| 批次 | 覆盖目录 | 状态 |
|---|---|---|
| 批1-16 | statistics/math/science/金融6目录/工程5目录/健康4目录/土木化学6目录/检验生理6目录/物理地物6目录/商运6目录/量表6目录/专科6目录/食品农业6目录/IT媒体6目录/生活6目录/声学航空6目录/产业6目录/生活商业6目录 | ✅ 已覆盖（发现的问题已修复或已登记） |
| 批17 | machinery/life/biz/fun/automotive/general（212 计算页全读） | ✅ 已覆盖（新发现 3 项已归档：life.md L1/biz-startup.md Z1/machinery M3） |
| 批18 | realestate/legal/marketing/metalwork/meteorology/energy/optical/fire-rescue/eco（322 计算页全读） | ✅ 已覆盖（新发现 2 项归档：eco-10/16 量纲 E1、metalwork 7 对比页功能单薄；realestate/legal 双段式页生效版此前 S 批已对照） |
| 批19 | cosmetic-derm/ophthalmology/encode/metrology/textile/robotics/nuclear/geometry/signal/food-testing/reproductive-medicine/rheumatology（316 计算页全读） | ✅ 已覆盖（specialties.md C1 游离酸颠倒；_others.md O6 重金属迁移×1000 单位待核；其余 9 目录公式全核对通过） |
| 批20 | 其余全部 <25 页小目录（~90 个，~800 页） | ⚪ 未开始——目录清单与生成脚本见 plan/HANDOFF.md |

> 登记纪律：审计新发现的**未修复**问题按归属追加进对应任务文件；已修复问题一律不写入。

## 分类任务进度

| 大分类 | 文件 | 状态 |
|---|---|---|
| 01-IT开发 | it.md / ai.md / encode-telecom-security-data.md | 🔴 待开发 |
| 02-金融财务 | finance.md / banking-investment-securities.md / tax-accounting-audit.md / insurance.md | 🔴 待开发 |
| 03-医疗健康 | scales.md / lab-diagnosis.md / drug-dosing.md / specialties.md | 🔴 待开发 |
| 04-设计创意 | design.md / image.md | 🔴 待开发 |
| 05-生活消费 | photo-video.md / food-travel.md / sports-fitness.md / home-decor.md / life.md | 🔴 待开发 |
| 06-商业运营 | marketing-sales.md / ecommerce-logistics.md / hr-legal.md / realestate.md / biz-startup.md | 🔴 待开发 |
| 07-教育学习 | edu-language.md / research-library.md | 🔴 待开发 |
| 08-工程制造 | machinery-metalwork.md / electrical-electronics.md / construction-energy.md / aero-robotics.md | 🔴 待开发 |
| 09-自然科学 | science-math-statistics.md / physics-optics-quantum.md / earth-geo.md | 🔴 待开发 |
| 10-农业养殖 | agriculture.md / fishery-aquaculture.md / livestock-eco-forestry.md | 🔴 待开发 |
| 11-文娱爱好 | fun-entertainment.md / culture-collection.md | 🔴 待开发 |
| 12-长尾行业 | _others.md（<20 页的其余 190+ 行业） | 🟡 仅收录已知问题 |
