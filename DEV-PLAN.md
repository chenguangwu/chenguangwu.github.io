# ToolBox 开发计划（DEV-PLAN）

> 本文件整合原 `ROADMAP.md`（路线图总结）、`PLAN-TOOLS.md`（工具候选池）、`docs/guide-expansion-plan.md`（指南扩容）三份开发任务文档。
> 当前所有历史遗留任务已清零，本文件聚焦「现状基线 + 构建门禁 + 下一步活计划」。

---

## 一、现状基线（实测，2026-08-26）

| 指标 | 实测值 |
|---|---:|
| 索引收录工具 | 5,023 |
| 行业目录 | 266 |
| 质量分级 | A 5,023（**100%**） / B 0 / C 0 |
| 跳转桩 | 14 |
| 指南 | 74 篇正文（+6 cluster 页） |
| 质量门禁 | 五道全绿 |
| CI | 已配置（`.github/workflows/quality-gates.yml`，历史全绿） |
| 搜索能力 | 汉字 / 英文 / 拼音（完整 + 首字母） |
| LICENSE | MIT（已加） |

> **全部遗留任务已于 2026-08-26 清零**：命名规范化（953 编号 URL）/ 跨行业 basename 重复（104 组）因 URL 迁移 SEO 风险跳过；空壳 / 标题重复 / math 过载经实测已自然清零或前提不成立；高频工具质量打磨（30 个 B 级升 A）已完成。后续新工具严格语义化命名、避免同名。
> i18n 状态（行业英文名覆盖、翻译填充）由 i18n agent 跟踪，不在本计划范围。

---

## 二、构建与门禁命令

- 重建索引：`python3 _build.py`
- 质量门禁：`python3 scripts/run_gates.py`（需 5/5 全绿）
- 死链门禁：`python3 _audit_links.py --check`（exit 0）
- 资产门禁：`python3 _audit_assets.py --check`（exit 0）
- 英文同步：每批新增工具后必跑 `scripts/gen_en_override.py` → `_en_override.json`（标题/简介）+ 同步 `slug-en.json`（卡片）；高质量语义化英文，禁止 slug 直译
- 索引提交：不自动跑；`_build.py` 后由用户手动 `python3 _submit_indexnow.py`（定时任务由 crontab 管理）

---

## 三、新增工具候选池（Q1）

> 方向：新建工具候选池 + 分批开发上线（A 级质量）。依据：忽略 GSC，基于 it-tools.tech 竞品缺口 + 自身判断（计算/转换/速查/生成器优先）。去重：反查现有 5031 工具排除已覆盖项；`keycode-lookup`(=存量 keycode-info)、`text-to-nato`(=存量 nato-alphabet) 功能重叠已排除。
> 质量门槛：每批工具 A 级达标（own_len≥6000 或 ≥3000 且 inputs≥3），靠真实功能模块（参考表/明细/计算）而非代码膨胀。门禁：每批 `scripts/run_gates.py` 5/5 + `_build.py` 重建，独立 commit+push。

### 一期（13，转换器/编码/速查）— ✅ 已上线（gen_q1e）
| slug | industry | 定位 |
|---|---|---|
| roman-numeral-converter | it | 罗马数字 ↔ 阿拉伯数字互转 |
| mime-type-lookup | it | 文件扩展名 ↔ MIME 类型速查 |
| http-methods-reference | it | HTTP 方法语义/安全/幂等速查 |
| json-repair | it | 粘贴损坏 JSON 一键修复并校验 |
| text-to-braille | text | 文本转盲文 Unicode 点字 |
| text-to-1337 | text | 文本转 Leet 语（多强度） |
| binary-to-ascii | encode | 二进制/十六进制串转 ASCII 文本 |
| text-to-ascii-art | text | 文本转 ASCII 大字艺术字 |
| triangle-calculator | it | 三角形边长/角度/面积/周长计算 |
| prime-checker | it | 质数检测 + 因数分解 |
| color-shade-generator | design | 基色生成明暗梯度（tint/shade） |
| ipv4-range-expander | it | CIDR/范围展开网络地址与可用数 |
| ipv6-converter | it | IPv6 地址压缩/展开标准化 |

### 二期（13，生成器/计算/生活）— ✅ 已上线（gen_q1f）
| slug | industry | 定位 |
|---|---|---|
| wifi-qr-generator | it | WiFi 配置生成二维码文本 |
| docker-run-converter | it | docker run 命令 ↔ compose 互转 |
| gradient-generator | design | CSS 渐变生成器（线性/径向） |
| lorem-ipsum-generator | text | 占位文本生成器 |
| reading-time-estimator | text | 文章阅读时长估算 |
| split-bill | accounting | 多人分账/小费计算 |
| gst-calculator | tax | 增值税（含税/不含税）计算 |
| date-duration | it | 两日期相差天数/工作日 |
| recipe-scaler | baking | 配方按份量缩放 |
| fuel-cost-calculator | automotive | 油费/百公里成本估算 |
| parking-fee | daily-goods | 停车费阶梯计算 |
| unit-price-compare | biz | 不同规格单价对比 |
| unit-converter-advanced | it | 进阶单位换算（多类目） |

### 三期（13，校验/配置生成）— ✅ 已上线（gen_q1g，实际行业 it/design，因 data/security/seo 目录未建）
| slug | industry | 定位 |
|---|---|---|
| xml-validator | it | XML 格式校验 + 美化 |
| csv-validator | data | CSV 表头/列数校验 |
| css-minify | it | CSS 压缩 |
| js-minify | it | JS 压缩（安全去空白/注释） |
| markdown-lint | text | Markdown 常见规范检查 |
| hash-identifier | security | 哈希类型识别 |
| gitignore-generator | it | .gitignore 模板生成 |
| dockerfile-generator | it | Dockerfile 模板生成 |
| sitemap-generator | seo 或 it | 简易 sitemap.xml 生成 |
| color-blindness-sim | design | 色盲模拟预览 |
| nginx-config-generator | it | Nginx server 块配置生成 |
| kubernetes-yaml-generator | it | K8s Deployment YAML 生成 |
| meta-tags-generator | seo 或 it | SEO meta 标签生成 |

### 已排除候选（DUPLICATE / REJECTED）
- keycode-lookup → 存量 `keycode-info` 等价
- text-to-nato → 存量 `nato-alphabet` 等价
- 其余 it-tools 缺口（angle/energy/sql-formatter/git-cheatsheet/xml-formatter 等）已在更早批次上线

---

## 四、指南扩容计划（N3，25 篇）

> 制定：2026-08-20。目标：指南从 55 篇扩展到 80 篇（25 新篇 + 现有 55）。
> 数据说明：无实时 GSC 流量数据，选题依据为「功能复杂度 + 用户常见问题 + 跨行业覆盖 + 与现有指南无主题重复」。
> **现状**：实际已落地，guides.json 49→74，指南共 74 篇正文（+6 cluster），25 篇全部上线。

### 选题统计
| 维度 | 值 |
|---|---|
| 选题总数 | 25 |
| 覆盖行业数 | 11（accounting / banking / science / health / fitness / design / biz / realestate / securities / automotive / baking） |
| 单行业最多 | science = 5（≤8 ✓） |
| 与现有 55 篇重复 | 0（已逐条比对 title/slug/工具 URL） |
| 全部映射到真实工具 | 25/25（已校验 `tools/<ind>/<base>.html` 存在且入索引） |

### 选题明细（25 条，每批 5 篇）
**批次 01（金融 + 科学）**
| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异（vs 现有 55 篇） |
|---|---|---|---|---|---|
| 1 | calc-1 | tools/accounting/calc-1.html | 增值税计算 | 当期应纳增值税怎么算？含税价如何反推？ | 现有无税务类指南 |
| 2 | simple-interest | tools/banking/simple-interest.html | 单利利息 | 单利和复利差多少？到期利息怎么算？ | 现有无利息计算指南 |
| 3 | break-even-units | tools/accounting/break-even-units.html | 盈亏平衡产量 | 最少卖多少才不亏本？ | 现有无盈亏平衡指南 |
| 4 | effective-annual-rate | tools/banking/effective-annual-rate.html | 有效年利率 EAR | 名义利率和实际年化差多少？ | 现有无 EAR 指南 |
| 5 | fd-quarterly | tools/banking/fd-quarterly.html | 定期存款按季复利 | 定期到期能拿多少？ | 现有 mortgage 指南不含定期存款 |

**批次 02（科学）**
| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 6 | fraction-calculator | tools/science/fraction-calculator.html | 分数计算 | 分数加减乘除/约分 | 现有无分数指南 |
| 7 | gcd-calculator | tools/science/gcd-calculator.html | 最大公约数 | 辗转相除法怎么算 | 现有无 GCD 指南 |
| 8 | lcm-calculator | tools/science/lcm-calculator.html | 最小公倍数 | 通分/周期对齐怎么算 | 现有无 LCM 指南 |
| 9 | quadratic-equation | tools/science/quadratic-equation.html | 一元二次方程 | 求根公式/判别式 | 现有无方程求解指南 |
| 10 | equation-balancer | tools/science/equation-balancer.html | 化学方程式配平 | 反应式怎么配平 | 现有无化学配平指南 |

**批次 03（健康 + 健身）**
| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 11 | pregnancy-due-date | tools/health/pregnancy-due-date.html | 预产期计算 | 预产期怎么算？几周了？ | 现有无孕产指南 |
| 12 | water-intake-calculator | tools/health/water-intake-calculator.html | 每日饮水量 | 一天该喝多少水？ | 现有无饮水指南 |
| 13 | heart-rate-zones | tools/health/heart-rate-zones.html | 心率区间 | 有氧心率多少合适？ | 现有 blood-pressure 不同主题 |
| 14 | waist-hip-ratio | tools/health/waist-hip-ratio.html | 腰臀比 | 腹部肥胖怎么判断？ | 现有 BMI/体脂不同指标 |
| 15 | convert | tools/fitness/convert.html | 跑步配速 | 配速和速度怎么换？ | 现有无配速指南 |

**批次 04（设计 + 商务）**
| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 16 | favicon-generator | tools/design/favicon-generator.html | Favicon 生成 | 网站图标怎么做？ | 现有 color/qr 不同 |
| 17 | image-compress | tools/design/image-compress.html | 图片压缩 | 图片怎么瘦身不糊？ | 现有无压缩指南 |
| 18 | image-format-converter | tools/design/image-format-converter.html | 图片格式转换 | PNG/JPG/WebP 怎么转？ | 现有无格式转换指南 |
| 19 | text-diff | tools/biz/text-diff.html | 文本差异对比 | 两段文字哪里不同？ | 现有无文本对比指南 |
| 20 | text-extract-urls | tools/biz/text-extract-urls.html | 提取 URL | 从文本批量提取链接 | 现有无提取 URL 指南 |

**批次 05（商务 + 房产 + 证券 + 汽车 + 烘焙）**
| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 21 | text-compare | tools/biz/text-compare.html | 文本并排对比 | 中英/两版怎么并排看 | 与 text-diff 互补（并排 vs 差异摘要） |
| 22 | summary-second-hand | tools/realestate/summary-second-hand.html | 二手房税费 | 买房过户要交多少税？ | 现有无房产税费指南 |
| 23 | option-breakeven-call | tools/securities/option-breakeven-call.html | 看涨期权盈亏平衡 | 期权多久回本？ | 现有无期权指南 |
| 24 | oil-change-countdown | tools/automotive/oil-change-countdown.html | 机油更换倒计时 | 什么时候该换机油？ | 现有无保养提醒指南 |
| 25 | baker-percentage | tools/baking/baker-percentage.html | 烘焙百分比 | 配方怎么按比例缩放？ | 现有无烘焙指南 |

### 重复检查结论
- 逐条比对 `json/guides.json`（49 条映射）与 `guides/*.html`（55 篇）的 title / slug / 目标工具：25 个选题的工具均不在现有映射中，主题无重叠。
- 健康类选题（预产期/饮水/心率区间/腰臀比）与现有 blood-pressure/blood-sugar/bmi/body-fat/calorie 指南指标不同，非改名复制。
- 文本类（text-diff / text-extract-urls / text-compare）三者定位互补：差异高亮 / 链接提取 / 并排审阅，非同模板复制。

### 落地机制
- 生成器：`scripts/gen_n3_guides.py <batch>`（batch=1..5），复用 `scripts/gen_guides2.py` 的 TPL 模板。
- 每批动作：写 5 篇 `guides/<slug>-guide.html` + 合并对应 5 条到 `json/guides.json` + 向 `guides/index.html` 追加 5 个 `<li>`。
- 每批验收：`python3 scripts/run_gates.py` 全绿；新指南从指南中心或工具页可达；无重复 title/id/死链。
- 每批独立 commit：`feat(guides): N3-02 publish guide batch XX`。

### 完成账本（均已落地）
| 批次 | 状态 | 指南数累计 |
|---|---|---|
| 01 | 已完成 | 55→60 |
| 02 | 已完成 | 60→65 |
| 03 | 已完成 | 65→70 |
| 04 | 已完成 | 70→75 |
| 05 | 已完成 | 75→80 |
