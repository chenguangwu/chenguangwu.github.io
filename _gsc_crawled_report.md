# GSC 已抓取 URL 数据分析报告（2026-10-12）

> 数据源：Google Search Console 后台导出「已抓取 URL」1000 条（无重复）。
> 对比基准：本地 `sitemap.xml`（16680 条 = 8340 zh-CN + 8340 zh-TW）。
> 脚本：`/tmp/analyze_gsc.py`，原始清单 `/tmp/gsc_crawled_1000.txt`。

## 1. 基础统计

| 指标 | 数值 | 说明 |
|------|------|------|
| 已抓取 URL | 1000 | 去重后 1000，无重复 |
| zh-CN | 581 | 占 58.1% |
| zh-TW | 412 | 占 41.2%（镜像站获得四成抓取配额，健康） |
| ?lang=en-US | 7 | canonical 全部指回中文无参 URL（设计上不收英文） |
| 行业覆盖 | 168 / 207 | 39 个行业有提交但零抓取 |
| 行业 index 页 | 12 | science/pediatrics/life/acoustics/dynamics/thermodynamics/ophthalmology/nuclear/signal/acupuncture 等，索引Hub 生效 |
| 非 tools 页 | 2 | sitemap.html、guides/index.html |

## 2. 收录覆盖率（核心结论）

| 维度 | 已抓 | sitemap 提交 | 覆盖率 |
|------|------|------|--------|
| 全站 | 1000 | 16680 | **6.0%** |
| zh-CN | 581 | 8340 | 7.0% |
| zh-TW | 412 | 8340 | 4.9% |

**收录（发现）是当前最大瓶颈，而非内容质量**——全站质量分级已 100% A 级（HEAD commit a2cca4a0f3），但 Google 仅发现 6% 的提交 URL。

## 3. 异常清单（P0，直接可执行）

### 3.1 5 个已抓 URL 对应「分类转移中途批次」（最高优先级）

Google 已抓取的 5 个旧 URL，本地已不存在，且**旧路径无重定向存根**：

| 旧 URL（线上仍 200，在 HEAD） | 新 URL（本地已就位，**线上 404，未提交**） | 转移 |
|------|------|------|
| tools/health/pace-calculator.html | tools/fitness/pace-calculator.html | health→fitness |
| tools/sports/zhangpengfangfengxishu.html | tools/travel/zhangpengfangfengxishu.html | sports→travel |
| tools/niche/pet-age.html | tools/pet/pet-age.html | niche→pet |
| tools/legal/calc-8.html | tools/tax/calc-8.html | legal→tax |
| tools/fun/hotpot-portion.html | tools/restaurant/hotpot-portion.html | fun→restaurant |

**真相**：这不是历史遗留 404，而是**一批 15 个工具页的分类转移改动卡在 git 暂存区未提交**（连同 i18n en 字典同步搬迁、38 个 guides 链接修正、构建产物已重建）。当前状态：
- 旧 URL 在 HEAD → 线上 200（Google 抓到的还是旧地址）
- 新 URL 不在 HEAD → **线上 404**
- 本地磁盘/暂存区/构建产物已是新状态

同批 15 个迁移还包括：driver-license-validator(finance→automotive)、fuel-converter(life→automotive)、csv-json(life→data)、yaml-json(life→data)、housing-fund-loan(legal→finance)、running-calories(health→fitness)、step-stride(fun→fitness)、fish-tank-volume(niche→pet)、bbq-portion(fun→restaurant)、car-residual(misc2→usedcar)、wedding-banquet(fun→wedding)。

**处置**：该批次必须收口（build → 5 道门禁 → commit → push → Actions success），**部署成功后**再按 AGENTS.md §4.6 对全部旧 URL 提 IndexNow 死链（默认校验，部署前提交会被误判"存活"而跳过）。

### 3.2 2 个重定向存根被 Google 抓到

| 存根 URL | 目标 | 问题 |
|------|------|------|
| tools/design/color-contrast-check.html | tools/design/contrast-checker.html | 存根未登记进 `_redirect_stubs_todo.md`，且无死链提交记录（对比 pets 批次 2026-10-10 有 `_deadlinks_2026-10-10_pets.txt` 证据） |
| tools/pets/grooming-guide.html | tools/pet/grooming-guide.html | 已登记（到期 2026-11-10）、已提交，合规 |

**处置**：color-contrast-check 补登记 + `--no-verify` 补提死链。

## 4. 行业抓取热度 Top 15（ crawled / sitemap / 覆盖率 ）

| 行业 | crawled | sitemap | cov | 行业 | crawled | sitemap | cov |
|------|------|------|------|------|------|------|------|
| it | 44 | 674 | 6% | acoustics | 16 | 58 | 27% |
| science | 44 | 196 | 22% | ai | 14 | 130 | 10% |
| surveying | 31 | 88 | 35% | legal | 14 | 98 | 14% |
| sports | 27 | 152 | 17% | design | 13 | 218 | 5% |
| general | 27 | 364 | 7% | tax | 13 | 62 | 20% |
| statistics | 27 | 104 | 25% | structural | 13 | 54 | 24% |
| life | 20 | 140 | 14% | optical | 12 | 82 | 14% |
| urology | 20 | 50 | 40% | accounting | 12 | 72 | 16% |
| health | 19 | 80 | 23% | robotics | 12 | 58 | 20% |
| rheumatology | 18 | 52 | 34% | textile | 12 | 52 | 23% |
| hydraulic | 18 | 114 | 15% | marketing | 11 | 92 | 11% |
| ophthalmology | 16 | 64 | 25% | reproductive-medicine | 11 | 52 | 21% |

小行业（surveying/urology/rheumatology）覆盖率高、大行业（it/design/general）覆盖率低——符合 Google 按站点权重分配抓取额的规律。医疗/工程/统计类是本站抓取基本盘。

## 5. 零抓取行业 40 个（sitemap 有、Google 从未抓）

economics(56) clinical-nursing(54) electromagnetism(54) dentistry(48) dermatology(48) ecommerce(48) ent(48) beauty(44) electronics(44) electrical(36) advertising(34) image(30) dyeing(28) mining(26) hvac(22) baking(18) cleaning(18) cognition(18) decor(18) chinese-cook(14) exhibition(14) film(14) floral(14) funeral(14) office(14) packaging(14) video(14) aquaculture(12) audit(12) bonding(12) ceramics(12) chess(12) chinese(12) edu2(12) fengshui(12) futures(12) kids(12) logistics2(12) service(12) railway(12)

注：economics/clinical-nursing/electromagnetism/dentistry 等是 sitemap 中的较大分类却零抓取，优先查内链入口。

## 6. 重复/近义分类对（主题权重稀释）

抓取数据证实以下分类对**都被 Google 分别抓取**（内链与主题权重被拆分）：

| 分类对 | 各自 crawled | 判断 |
|------|------|------|
| pet / pets / pet-training | 5 / 1 / 1 | pets 已迁空（存根 2026-11-10 到期），pet-training 待定 |
| photo / photo2 | 10 / 2 | 同主题双目录 |
| medical / medical2 | 2 / 2 | 同主题双目录 |
| misc / misc2 | 2 / 1 | 同主题双目录 |
| gardening / gardening2 | 2 / 2 | 同主题双目录 |
| woodwork / woodworking | 9 / 2 | 同主题双目录 |
| legal / legal2 | 14 / 1 | legal2 仅存 zh-tw 抓取 |
| edu / edu2 | 9 / 0 | edu2 零抓 |
| logistics / logistics2 | 2 / 0 | logistics2 零抓 |
| stats / statistics | 2 / 27 | 同主题双目录 |
| chemical / chemistry | 1 / 6 | 同主题双目录 |
| optical / optics | 12 / 4 | 同主题双目录 |

处置原则（AGENTS.md §7）：**不动 URL**。靠行业索引页互链 + 关联卡片聚合；未来新增工具只入主分类。彻底合并属于独立专项（需存根机制 + 死链提交），成本高，建议排在 P2 评估。

## 7. URL 命名质量

- 纯泛名 slug（assessor-N / detector-N / calc-N / generator-N 等）：**136/1000 = 13%**
- 结论（沿用 2026-10-12 清理专项审计口径）：960 个泛名 slug 均有真实功能，**改名 = 动 960 URL/SEO 资产，零价值，绝不动**。泛名本身不惩罚排名，靠内容与内链补权。

## 8. 其他发现

1. **英文页策略**：7 个 ?lang=en-US 被抓，canonical 全部 self 指回中文无参 URL → 英文变体永不被独立收录。这是有意的权重集中设计；若未来要英文流量，需 hreflang + 自指 canonical，属独立决策。
2. **guides/index.html 不在 sitemap**（6818 个 guides 详情页都在，唯独索引页缺失），Google 仍抓到了它。小缺口，可在 `_build.py` sitemap 生成处补一行。
3. **zh-tw 构建不清理孤儿文件**：迁移后 zh-tw 旧路径文件仍在本地（如 zh-tw/tools/health/pace-calculator.html），属构建产物残留，不影响线上（CI 从源码重建），无需处理。

## 9. 行动清单（P0/P1/P2）

### P0（本周，数据直接暴露）
1. **收口暂存区中的 15 页分类转移批次**（build → run_gates 5 道 → commit → push → Actions success）→ 部署成功后对 15 个旧 URL 提 IndexNow 死链（默认校验）。
2. color-contrast-check 存根补登记 `_redirect_stubs_todo.md` + `--no-verify` 补提死链。

### P1（本月，收录运营）
3. 用 `_gsc_inspect_urls.py` 对未抓取的高价值页批量 inspect + 请求收录（配额有限，优先 A 级/医疗/工程类）。
4. 建立月度 GSC 已抓清单 diff 监控（新抓=进展，掉抓=隐患）。
5. 40 个零抓行业做内链入口巡检（行业索引页是否被首页/导航覆盖）。

### P2（持续/评估）
6. 重复分类彻底合并评估（约 12 对，动 URL 需存根+死链，成本高）。
7. guides/index.html 补进 sitemap。
8. 英文收录策略决策（要/不要英文流量）。
