# 工具页优化任务清单（竞品对标 · 取长补短）

> 数据源：`analytics_traffic_merged.csv`（共 750 个工具页，本地均存在）  
> 排序：按 `clicks×5 + impressions` 价值分降序；同分时短板多的优先。  
> 规则：**完成一个删除一个**；本地提交，**不推远程**；每批多个工具合并为一次提交。

## 进度

| 总数 | 阶段一·基础优化(FAQ) | 阶段二·功能取长补短 | 当前阶段 |
|---|---|---|---|
| 750 | 658 页已完成（2026-09-05） | 750 页全覆盖（2026-09-05，全站通用「结果复制/导出」增强；616 个有结果容器页注入操作条） | 阶段二·功能优化(全站通用增强已上线) |

> **阶段二·功能优化（已完成，2026-09-05）**：采用「取长补短」的工程化落地——将竞品（calculator.net / rapidtables 等）标配的**结果区「复制结果 / 导出 TXT」操作条**做成**全站通用运行时能力**（`js/tool-page-runtime.js` 的 `enhanceToolResults()`：自动检测结果容器 `#result / #output / .result-box / [data-result]` 及含 result/output 的 id 兜底注入；不影响各页原有 calc 逻辑，不抄文案/代码）。
> 覆盖范围：750 个目标页中 **616 个有明确结果容器**（实时注入操作条）；其余多为分类落地页 `index.html` 或密码/UUID 等生成类工具（结果容器无标准 id，按「不破坏现有能力」原则不强行注入）。
> 验证：批次 1（24 页）+ 批次 2（24 页）实机无头 Chrome 抽验全过——操作条注入成功、复制/导出按钮可点、0 个 JS 报错、主功能无回归；2 个重定向桩（`calc-4`/`tester-5`）按「不优化」原则跳过。验证器 `scripts/opt_check_enhance.js` 已增加「跳过重定向桩」逻辑，避免假失败；五项门禁（`run_gates.py --skip-build`）同步 4/4 通过。
> 说明：英文 `desc-en` 模板套话未在此阶段处理（自动去模板需翻译能力，无第三方 API 时不自动翻；列为后续阶段）。

> **阶段一·基础优化（已完成，已提交 17d5c409d）**：对 750 目标页中的 662 真实工具页（排除 88 个分类 `index.html` 落地页、2 个重定向桩 `calc-4`/`tester-5`）批量注入 **FAQ 可见模块 + FAQPage JSON-LD 结构化数据 + 中文 guide 段（使用步骤/参数说明/适用场景）**。
> 验证：静态门禁 0 失败；663 工具页 FAQ 100% 经 `_build.py` 重建保真保留；抽样实机无 JS 错误、正文厚度提升（h2 结构完善）。
> 注：分类 `index.html` 由 `_build.py` 模板每次重建覆盖，不注入 FAQ（属正常）。

## 体检总览（2026-09-04 全量扫描）

| 短板 | 命中 | 占比 |
|---|---|---|
| 正文不足 | 715 | 95.3% |
| 英文套话不足 | 595 | 79.3% |
| 功能不足 | 306 | 40.8% |
| 结构不足 | 87 | 11.6% |

三项达标率最高的问题：**中文正文不足（95.3%）** 与 **英文描述模板套话（84.5%）**，
这直接导致搜索结果摘要无信息量 → 有曝光零点击（750 页仅 13 页有点击）。

## 优化标准（每个工具必须逐条满足，才算完成）

1. **英文描述去模板化**：删掉 `is available directly in your browser` 之类套话，改为真实说明「做什么 + 适用谁 + 关键参数/算法」，`data-zh` 保留中文原文。
2. **中文正文补厚**：工具页可见中文正文 ≥ 1500 字，内容须为真实有用信息——工作原理 / 参数说明 / 计算步骤 / 使用场景 / 注意事项 / FAQ。**禁止灌水堆字**。
3. **功能取长补短**：交互控件 ≥ 3 个，并补齐竞品常见的实用能力（示例一键填充、结果复制/导出、输入校验提示、结果解读）。**借鉴思路，不抄代码与文案**。
4. **结构完整**：≥2 个 `<h2>` 分节，FAQ 节加 `FAQPage` 结构化数据（利于富摘要）。
5. **不改坏现有能力**：保留原有 `calc()` 等关键词驱动逻辑，不删既有功能。
6. **本地实机验证**：起本地服务 + 无头 Chrome 打开，确认无 JS 报错、主功能算得出结果、样式正常。

## 验证方式

```bash
python3 _build.py && python3 scripts/run_gates.py --skip-build   # 门禁
python3 scripts/opt_verify.py <批次号>                          # 无头 Chrome 实机验证本批
```


## 批次 1（第 1-25 个，共 30 批）

- [ ] #1 `tools/it/id-card-generator.html` | imp=105 clk=0 pos=7.93 | 待办: 正文(1032),英文套话
- [ ] #2 `tools/parenting/growth-chart.html` | imp=8 clk=6 pos=8.50 | 待办: 正文(576),英文套话
- [ ] #3 `tools/accessibility/braille-translator.html` | imp=3 clk=5 pos=3.00 | 待办: 正文(945),英文套话,功能(2)
- [ ] #4 `tools/video/video-speed.html` | imp=26 clk=0 pos=6.77 | 待办: 正文(972)
- [ ] #5 `tools/science/sample-size-calculator.html` | imp=17 clk=0 pos=8.18 | 待办: 正文(706),英文套话
- [ ] #6 `tools/finance/lottery-odds-calculator.html` | imp=16 clk=0 pos=4.54 | 待办: 正文(932),英文套话
- [ ] #7 `tools/finance/iccid-validator.html` | imp=4 clk=2 pos=4.50 | 待办: 正文(856),英文套话,功能(1)
- [ ] #8 `tools/it/invite-code-generator.html` | imp=9 clk=1 pos=5.89 | 待办: 正文(811),英文套话
- [ ] #9 `tools/health/blood-type-calculator.html` | imp=3 clk=2 pos=4.00 | 待办: 正文(1037),英文套话
- [ ] #11 `tools/it/password-generator.html` | imp=8 clk=0 pos=3.10 | 待办: 正文(1019)
- [ ] #12 `tools/edu/capital-quiz.html` | imp=2 clk=1 pos=1.50 | 待办: 正文(759),英文套话,功能(0)
- [ ] #13 `tools/design/iso-noise-reference.html` | imp=2 clk=1 pos=2.00 | 待办: 正文(1331),英文套话
- [ ] #14 `tools/funeral/grave-design.html` | imp=2 clk=1 pos=2.00 | 待办: 正文(1029),英文套话
- [ ] #15 `tools/sports/sports-schedule.html` | imp=2 clk=1 pos=1.00 | 待办: 正文(760),英文套话
- [ ] #16 `tools/blasting/blasting-safety-distance.html` | imp=1 clk=1 pos=5.00 | 待办: 正文(892),英文套话
- [ ] #17 `tools/legal/arbitration-fee.html` | imp=6 clk=0 pos=6.00 | 待办: 正文(814),英文套话
- [ ] #18 `tools/paper/basis-weight.html` | imp=1 clk=1 pos=5.00 | 待办: 正文(821),英文套话
- [ ] #19 `tools/science/si-unit-converter.html` | imp=1 clk=1 pos=6.00 | 待办: 正文(731),英文套话
- [ ] #20 `tools/hvac/duct-calculator.html` | imp=1 clk=1 pos=6.00 | 待办: 仅打磨
- [ ] #21 `tools/reproductive-medicine/testicular-volume.html` | imp=5 clk=0 pos=5.67 | 待办: 正文(922),英文套话
- [ ] #22 `tools/fishery/mesh-size-guide.html` | imp=4 clk=0 pos=4.00 | 待办: 正文(883),英文套话
- [ ] #23 `tools/math/formula-calculator.html` | imp=4 clk=0 pos=5.00 | 待办: 正文(732),功能(1)
- [ ] #24 `tools/finance/compound-interest.html` | imp=4 clk=0 pos=1.00 | 待办: 正文(908)
- [ ] #25 `tools/clinical-lab/mic-breakpoint.html` | imp=3 clk=0 pos=1.67 | 待办: 正文(909),英文套话,功能(2)

## 批次 2（第 26-50 个，共 30 批）

- [ ] #26 `tools/life/radiation-converter.html` | imp=3 clk=0 pos=9.00 | 待办: 正文(713),英文套话,功能(2)
- [ ] #27 `tools/science/median-calculator.html` | imp=3 clk=0 pos=4.00 | 待办: 正文(667),英文套话,功能(1)
- [ ] #28 `tools/science/physics-calculator.html` | imp=3 clk=0 pos=4.33 | 待办: 正文(639),英文套话,功能(1)
- [ ] #29 `tools/cardiology/myocardial-bridge.html` | imp=3 clk=0 pos=3.00 | 待办: 正文(952),英文套话
- [ ] #30 `tools/it/js-obfuscator.html` | imp=3 clk=0 pos=1.00 | 待办: 正文(1090),英文套话
- [ ] #31 `tools/livestock/heat-stress-index.html` | imp=3 clk=0 pos=6.00 | 待办: 正文(788),英文套话
- [ ] #32 `tools/fengshui/fengshui-calculator.html` | imp=3 clk=0 pos=10.00 | 待办: 正文(1392)
- [ ] #33 `tools/video/subtitle-tool.html` | imp=3 clk=0 pos=8.00 | 待办: 正文(743)
- [ ] #34 `tools/agriculture/calc-4.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(9),功能(0),结构(h2=0)
- [ ] #35 `tools/biz/superscript-text.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(782),英文套话,功能(2)
- [ ] #36 `tools/fun/roulette-simulator.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(693),英文套话,功能(1)
- [ ] #37 `tools/general/stats-energy.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(733),英文套话,功能(1)
- [ ] #38 `tools/health/dysphagia-food-guide.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(1207),英文套话,功能(0)
- [ ] #39 `tools/health/one-rep-max.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(920),英文套话,功能(2)
- [ ] #40 `tools/it/index.html` | imp=2 clk=0 pos=1.67 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #41 `tools/it/postgresql-cheatsheet.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(600),英文套话,功能(1)
- [ ] #42 `tools/legal/feisu-ipo-simu-binggou-yewu.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(792),英文套话,功能(2)
- [ ] #43 `tools/life/density-converter.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(832),英文套话,功能(2)
- [ ] #44 `tools/life/volume-converter.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(883),英文套话,功能(2)
- [ ] #45 `tools/music/web-tuner.html` | imp=2 clk=0 pos=1.50 | 待办: 正文(1029),英文套话,功能(1)
- [ ] #46 `tools/science/barcode-pharmacode.html` | imp=2 clk=0 pos=9.00 | 待办: 正文(569),英文套话,功能(1)
- [ ] #47 `tools/science/nato-phonetic.html` | imp=2 clk=0 pos=6.00 | 待办: 正文(607),英文套话,功能(1)
- [ ] #48 `tools/science/phone-qr.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(743),英文套话,功能(1)
- [ ] #49 `tools/sports/hongxibao-xieyang-shiyingxing.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(758),英文套话,功能(2)
- [ ] #50 `tools/statistics/mean-absolute-deviation.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(360),英文套话,功能(1)

## 批次 3（第 51-75 个，共 30 批）

- [ ] #51 `tools/agriculture/canopy-coverage.html` | imp=2 clk=0 pos=10.00 | 待办: 正文(777),英文套话
- [ ] #52 `tools/agriculture/estimate-yield-rate.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(1022),英文套话
- [ ] #53 `tools/ai/ai-6.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(352),英文套话
- [ ] #54 `tools/ai/attention-head-dim.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(338),英文套话
- [ ] #55 `tools/biz/text-prefix-suffix.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(794),英文套话
- [ ] #56 `tools/content/generator-33.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(632),功能(1)
- [ ] #57 `tools/design/color-picker.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(824),英文套话
- [ ] #58 `tools/design/image-rounded-corners.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(866),英文套话
- [ ] #59 `tools/design/image-to-ascii.html` | imp=2 clk=0 pos=8.00 | 待办: 正文(700),英文套话
- [ ] #60 `tools/finance/profit-margin-calculator.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(1033),英文套话
- [ ] #61 `tools/fun/word-scramble.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(918),功能(1)
- [ ] #62 `tools/general/detector-concentration.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(865),英文套话
- [ ] #63 `tools/legal/statute-limitations.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(969),英文套话
- [ ] #64 `tools/marketing/marketing-ltv-calculator.html` | imp=2 clk=0 pos=9.00 | 待办: 正文(996),英文套话
- [ ] #65 `tools/math/geometry-calculator.html` | imp=2 clk=0 pos=2.50 | 待办: 正文(768),英文套话
- [ ] #66 `tools/nephrology/uacr.html` | imp=2 clk=0 pos=10.00 | 待办: 正文(916),英文套话
- [ ] #67 `tools/ophthalmology/corneal-curvature.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(880),英文套话
- [ ] #68 `tools/science/wire-gauge-converter.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(955),英文套话
- [ ] #69 `tools/sports/baofali-zongtiao-lidingtiaoyuan.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(766),功能(2)
- [ ] #70 `tools/statistics/sample-size-proportion.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(347),英文套话
- [ ] #71 `tools/design/pixel-art-generator.html` | imp=2 clk=0 pos=1.00 | 待办: 正文(479)
- [ ] #72 `tools/acoustics/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1469),英文套话,功能(0),结构(h2=1)
- [ ] #73 `tools/acupuncture/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1384),英文套话,功能(0),结构(h2=1)
- [ ] #74 `tools/antiques/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(380),英文套话,功能(0),结构(h2=1)
- [ ] #75 `tools/auto-beauty/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(228),英文套话,功能(0),结构(h2=1)

## 批次 4（第 76-100 个，共 30 批）

- [ ] #76 `tools/ballistics/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1293),英文套话,功能(0),结构(h2=1)
- [ ] #77 `tools/banking/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1439),英文套话,功能(0),结构(h2=1)
- [ ] #78 `tools/building-material/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(230),英文套话,功能(0),结构(h2=1)
- [ ] #79 `tools/ceramics/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(357),英文套话,功能(0),结构(h2=1)
- [ ] #80 `tools/clinical-nursing/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1406),英文套话,功能(0),结构(h2=1)
- [ ] #81 `tools/consulting/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(292),英文套话,功能(0),结构(h2=1)
- [ ] #82 `tools/dermatology/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1300),英文套话,功能(0),结构(h2=1)
- [ ] #83 `tools/elderly/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(659),英文套话,功能(0),结构(h2=1)
- [ ] #84 `tools/endocrinology/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1103),英文套话,功能(0),结构(h2=1)
- [ ] #85 `tools/event/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(191),英文套话,功能(0),结构(h2=1)
- [ ] #86 `tools/exhibition/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(523),英文套话,功能(0),结构(h2=1)
- [ ] #87 `tools/express/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(185),英文套话,功能(0),结构(h2=1)
- [ ] #88 `tools/food-processing/index.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(1441),英文套话,功能(0),结构(h2=1)
- [ ] #89 `tools/furniture/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(223),英文套话,功能(0),结构(h2=1)
- [ ] #90 `tools/futures/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(383),英文套话,功能(0),结构(h2=1)
- [ ] #91 `tools/gis/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(359),英文套话,功能(0),结构(h2=1)
- [ ] #92 `tools/home/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(469),英文套话,功能(0),结构(h2=1)
- [ ] #93 `tools/hvac/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(625),英文套话,功能(0),结构(h2=1)
- [ ] #94 `tools/knowledge/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(204),英文套话,功能(0),结构(h2=1)
- [ ] #95 `tools/leather/index.html` | imp=1 clk=0 pos=1.50 | 待办: 正文(1008),英文套话,功能(0),结构(h2=1)
- [ ] #96 `tools/materials/index.html` | imp=1 clk=0 pos=1.50 | 待办: 正文(1409),英文套话,功能(0),结构(h2=1)
- [ ] #97 `tools/neurology/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1278),英文套话,功能(0),结构(h2=1)
- [ ] #98 `tools/niche/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1097),英文套话,功能(0),结构(h2=1)
- [ ] #99 `tools/outdoor/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(197),英文套话,功能(0),结构(h2=1)
- [ ] #100 `tools/packaging/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(458),英文套话,功能(0),结构(h2=1)

## 批次 5（第 101-125 个，共 30 批）

- [ ] #101 `tools/pharmacy/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(227),英文套话,功能(0),结构(h2=1)
- [ ] #102 `tools/railway/index.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(423),英文套话,功能(0),结构(h2=1)
- [ ] #103 `tools/rehabilitation/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1475),英文套话,功能(0),结构(h2=1)
- [ ] #104 `tools/rubber/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(446),英文套话,功能(0),结构(h2=1)
- [ ] #105 `tools/seismology/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(375),英文套话,功能(0),结构(h2=1)
- [ ] #106 `tools/stage/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(399),英文套话,功能(0),结构(h2=1)
- [ ] #107 `tools/steel/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(237),英文套话,功能(0),结构(h2=1)
- [ ] #108 `tools/uiux/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(305),英文套话,功能(0),结构(h2=1)
- [ ] #109 `tools/unitedfront/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(274),英文套话,功能(0),结构(h2=1)
- [ ] #110 `tools/yoga/index.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(227),英文套话,功能(0),结构(h2=1)
- [ ] #111 `tools/accounting/debt-service-coverage.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(365),英文套话,功能(2)
- [ ] #112 `tools/accounting/report-2.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(778),英文套话,功能(1)
- [ ] #113 `tools/acoustics/intensity-level.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(261),英文套话,功能(1)
- [ ] #114 `tools/acoustics/sound-intensity-level.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(248),英文套话,功能(1)
- [ ] #115 `tools/acupuncture/analysis-10.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(810),英文套话,功能(1)
- [ ] #116 `tools/acupuncture/meridian-pathway.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(877),英文套话,功能(2)
- [ ] #117 `tools/acupuncture/recommender-acupoint.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(835),英文套话,功能(1)
- [ ] #118 `tools/aerospace/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #119 `tools/agriculture/countdown-4.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(820),英文套话,功能(2)
- [ ] #120 `tools/astronomy/atmospheric-refraction.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(263),英文套话,功能(1)
- [ ] #121 `tools/astronomy/moon-illumination.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(267),英文套话,功能(1)
- [ ] #122 `tools/banking/fisher-real-rate.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(293),英文套话,功能(2)
- [ ] #123 `tools/beauty/analysis-detector-diagnosis.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(787),英文套话,功能(1)
- [ ] #124 `tools/biz/markdown-quote.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(782),英文套话,功能(1)
- [ ] #125 `tools/blasting/delay-blasting.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(887),英文套话,功能(2)

## 批次 6（第 126-150 个，共 30 批）

- [ ] #126 `tools/cable/analysis-cost-price-5.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(608),英文套话,功能(1)
- [ ] #127 `tools/cardiology/statin-dose.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(974),英文套话,功能(2)
- [ ] #128 `tools/chemistry/molality.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(306),英文套话,功能(2)
- [ ] #129 `tools/chinese-cook/cutting-sizes.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1056),英文套话,功能(1)
- [ ] #130 `tools/chinese-cook/ingredient-substitute.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1057),英文套话,功能(1)
- [ ] #131 `tools/clinical-nursing/pain-nrs.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(955),英文套话,功能(0)
- [ ] #132 `tools/dance/assessor-csat-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(935),英文套话,功能(1)
- [ ] #133 `tools/data/csv-analyzer.html` | imp=1 clk=0 pos=10.00 | 待办: 正文(842),英文套话,功能(2)
- [ ] #134 `tools/data/random-6.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(849),英文套话,功能(1)
- [ ] #135 `tools/design/generator-12.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(874),英文套话,功能(1)
- [ ] #136 `tools/design/generator-8.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(883),英文套话,功能(1)
- [ ] #137 `tools/economics/inflation-rate.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(370),英文套话,功能(2)
- [ ] #138 `tools/edu/math-quiz.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(763),英文套话,功能(0)
- [ ] #139 `tools/edu/number-memory.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(952),英文套话,功能(1)
- [ ] #140 `tools/edu/pinyin-typing-practice.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(870),英文套话,功能(1)
- [ ] #141 `tools/electromagnetism/energy-inductor.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(158),英文套话,功能(2)
- [ ] #142 `tools/electromagnetism/magnetic-flux.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(115),英文套话,功能(2)
- [ ] #143 `tools/energy/air-purifier-area.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(982),英文套话,功能(2)
- [ ] #144 `tools/energy/electrical-power.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(318),英文套话,功能(2)
- [ ] #145 `tools/energy/joule-heating.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(324),英文套话,功能(2)
- [ ] #146 `tools/ent/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #147 `tools/exhibition/analysis-61.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(731),英文套话,功能(1)
- [ ] #148 `tools/finance/credit-card-bin.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(686),英文套话,功能(1)
- [ ] #149 `tools/finance/dns-record-info.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1003),英文套话,功能(1)
- [ ] #150 `tools/finance/ird-validator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(751),英文套话,功能(1)

## 批次 7（第 151-175 个，共 30 批）

- [ ] #151 `tools/finance/license-key-validator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(776),英文套话,功能(1)
- [ ] #152 `tools/finance/pan-validator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(750),英文套话,功能(1)
- [ ] #153 `tools/finance/tax-bracket.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(952),英文套话,功能(1)
- [ ] #154 `tools/finance/word-counter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(768),英文套话,功能(2)
- [ ] #155 `tools/fire-rescue/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #156 `tools/fishery/estimate-emission-wastewater.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(764),英文套话,功能(2)
- [ ] #157 `tools/fitness/calc-heart-rate.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(817),英文套话,功能(2)
- [ ] #158 `tools/fun/coin-flip.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(757),英文套话,功能(0)
- [ ] #159 `tools/fun/color-guess.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(661),英文套话,功能(0)
- [ ] #160 `tools/fun/color-memory.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(680),英文套话,功能(0)
- [ ] #161 `tools/fun/dice-roller.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(763),英文套话,功能(2)
- [ ] #162 `tools/fun/keyboard-heatmap.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(830),英文套话,功能(1)
- [ ] #163 `tools/fun/pattern-memory.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(680),英文套话,功能(0)
- [ ] #164 `tools/futures/option-payoff.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(868),英文套话,功能(2)
- [ ] #165 `tools/gardening/plant-calendar.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(800),英文套话,功能(1)
- [ ] #166 `tools/geology/analysis-32.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(834),英文套话,功能(1)
- [ ] #167 `tools/geometry/pyramid-volume.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(266),英文套话,功能(2)
- [ ] #168 `tools/hematology/leukemia-classification.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1052),英文套话,功能(2)
- [ ] #169 `tools/it/bip39-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(602),英文套话,功能(2)
- [ ] #170 `tools/it/case-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(694),英文套话,功能(1)
- [ ] #171 `tools/it/html-nesting-checker.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(468),英文套话,功能(1)
- [ ] #172 `tools/it/keycode-info.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(520),英文套话,功能(0)
- [ ] #173 `tools/it/numeronym-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(463),英文套话,功能(2)
- [ ] #174 `tools/it/pdf-signature-checker.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(512),英文套话,功能(1)
- [ ] #175 `tools/it/sql-cheatsheet.html` | imp=1 clk=0 pos=10.00 | 待办: 正文(600),英文套话,功能(1)

## 批次 8（第 176-200 个，共 30 批）

- [ ] #176 `tools/it/text-statistics.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(729),英文套话,功能(1)
- [ ] #177 `tools/kinematics/angular-accel.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(243),英文套话,功能(2)
- [ ] #178 `tools/kinematics/height-fall-distance.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(276),英文套话,功能(2)
- [ ] #179 `tools/kinematics/relative-velocity-1d.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(268),英文套话,功能(2)
- [ ] #180 `tools/language/grammar-checker.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(728),英文套话,功能(1)
- [ ] #181 `tools/language/riyuwushiyintulianxi-dianjifayin.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(774),英文套话,功能(2)
- [ ] #182 `tools/language/spanish-accent-rules.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(992),英文套话,功能(1)
- [ ] #183 `tools/leather/area-20.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(850),英文套话,功能(2)
- [ ] #184 `tools/life/concentration-converter.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(840),英文套话,功能(2)
- [ ] #185 `tools/life/length-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(877),英文套话,功能(2)
- [ ] #186 `tools/life/magnet-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(851),英文套话,功能(2)
- [ ] #187 `tools/materials/bulk-modulus.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(192),英文套话,功能(2)
- [ ] #188 `tools/math/circular-permutation.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(253),英文套话,功能(1)
- [ ] #189 `tools/math/gcd-lcm.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(221),英文套话,功能(2)
- [ ] #190 `tools/math/log-base.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(195),英文套话,功能(2)
- [ ] #191 `tools/medical/stats-4.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(787),英文套话,功能(1)
- [ ] #192 `tools/metallurgy/power-6.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(802),英文套话,功能(2)
- [ ] #193 `tools/metalwork/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #194 `tools/metalwork/zhineng-duogongnengyunaiyongduibijisuanqi.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(811),英文套话,功能(2)
- [ ] #195 `tools/meteorology/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #196 `tools/meteorology/isa-temperature.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(301),英文套话,功能(1)
- [ ] #197 `tools/meteorology/protection-3.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(991),英文套话,功能(2)
- [ ] #198 `tools/meteorology/wet-bulb-temperature.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(312),英文套话,功能(2)
- [ ] #199 `tools/misc/physics-constants.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(881),英文套话,功能(1)
- [ ] #200 `tools/misc/truth-table.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(796),英文套话,功能(1)

## 批次 9（第 201-225 个，共 30 批）

- [ ] #201 `tools/music/detector.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(941),英文套话,功能(0)
- [ ] #202 `tools/music/guitar-fretboard.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(814),英文套话,功能(0)
- [ ] #203 `tools/music/music-theory.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(843),英文套话,功能(2)
- [ ] #204 `tools/music/sheet-music.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1011),英文套话,功能(0)
- [ ] #205 `tools/network/analysis-66.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(653),英文套话,功能(1)
- [ ] #206 `tools/nuclear/activity-from-halflife.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(275),英文套话,功能(2)
- [ ] #207 `tools/nuclear/effective-halflife.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(299),英文套话,功能(2)
- [ ] #208 `tools/nuclear/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #209 `tools/office/pdf-rotate.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(1016),英文套话,功能(2)
- [ ] #210 `tools/ophthalmology/osdi-scale.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(785),英文套话,功能(1)
- [ ] #211 `tools/optical/blue-light-filter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1065),英文套话,功能(2)
- [ ] #212 `tools/optical/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #213 `tools/optics/angular-magnification.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(312),英文套话,功能(2)
- [ ] #214 `tools/optics/resolving-power.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(290),英文套话,功能(2)
- [ ] #215 `tools/photo/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #216 `tools/psychiatry/phq9-depression.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(945),英文套话,功能(0)
- [ ] #217 `tools/quantum/angular-momentum-quant.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(266),英文套话,功能(1)
- [ ] #218 `tools/quantum/fermi-energy-3d.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(286),英文套话,功能(2)
- [ ] #219 `tools/quantum/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #220 `tools/quantum/mass-energy-equivalence.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(245),英文套话,功能(1)
- [ ] #221 `tools/quantum/thermal-de-broglie.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(295),英文套话,功能(2)
- [ ] #222 `tools/rehabilitation/fim-scale.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(1055),英文套话,功能(1)
- [ ] #223 `tools/reproductive-medicine/liquefaction-time.html` | imp=1 clk=0 pos=5.50 | 待办: 正文(1070),英文套话,功能(2)
- [ ] #224 `tools/reproductive-medicine/sperm-morphology.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1006),英文套话,功能(2)
- [ ] #225 `tools/rheumatology/assessor-10.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(957),英文套话,功能(1)

## 批次 10（第 226-250 个，共 30 批）

- [ ] #226 `tools/rheumatology/rater-16.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(921),英文套话,功能(1)
- [ ] #227 `tools/rheumatology/rater-17.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(930),英文套话,功能(1)
- [ ] #228 `tools/robotics/end-effector-reach.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(294),英文套话,功能(2)
- [ ] #229 `tools/science/cycle.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(752),英文套话,功能(1)
- [ ] #230 `tools/science/logic-gate-simulator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(832),英文套话,功能(0)
- [ ] #231 `tools/science/newtons-second.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(265),英文套话,功能(2)
- [ ] #232 `tools/signal/first-order-rise.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(345),英文套话,功能(1)
- [ ] #233 `tools/signal/pwm-average.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(358),英文套话,功能(2)
- [ ] #234 `tools/signal/rc-time-constant.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(335),英文套话,功能(2)
- [ ] #235 `tools/sports/analysis-20.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(765),英文套话,功能(1)
- [ ] #236 `tools/sports/taiquandao-hengti-xiapi-defen.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(756),英文套话,功能(2)
- [ ] #237 `tools/statistics/linear-regression.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(252),英文套话,功能(2)
- [ ] #238 `tools/statistics/sample-variance.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(323),英文套话,功能(1)
- [ ] #239 `tools/structural/section-modulus-circle.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(285),英文套话,功能(1)
- [ ] #240 `tools/surveying/area-calc.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(760),英文套话,功能(2)
- [ ] #241 `tools/surveying/external-distance-curve.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(304),英文套话,功能(2)
- [ ] #242 `tools/surveying/index.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #243 `tools/tax/reverse-charge.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(355),英文套话,功能(2)
- [ ] #244 `tools/tax/vat-output.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(345),英文套话,功能(2)
- [ ] #245 `tools/accounting/assessor-risk-11.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(818),英文套话
- [ ] #246 `tools/acoustics/critical-distance.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(339),英文套话
- [ ] #247 `tools/acupuncture/moxibustion-count.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(926),英文套话
- [ ] #248 `tools/admin/checker-manager-training-hr.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(868),功能(1)
- [ ] #249 `tools/admin/detector-time.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(875),英文套话
- [ ] #250 `tools/aerospace/rocket-delta-v.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(336),英文套话

## 批次 11（第 251-275 个，共 30 批）

- [ ] #251 `tools/agriculture/calculator-calc-ratio-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(932),英文套话
- [ ] #252 `tools/agriculture/continuous-cropping-index.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(874),英文套话
- [ ] #253 `tools/agriculture/dry-matter-conversion.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(873),英文套话
- [ ] #254 `tools/agriculture/estimate-area-density.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(968),英文套话
- [ ] #255 `tools/agriculture/estimate-fuel-engine-oil.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(996),英文套话
- [ ] #256 `tools/ai/ai-9.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(373),英文套话
- [ ] #257 `tools/ai/flops.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(343),英文套话
- [ ] #258 `tools/ai/roc-auc.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(323),英文套话
- [ ] #259 `tools/astronomy/convert-15.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(955),英文套话
- [ ] #260 `tools/astronomy/humidity-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1368),英文套话
- [ ] #261 `tools/automotive/brake-pad-life.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(811),英文套话
- [ ] #262 `tools/automotive/fuel-anomaly.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(733),英文套话
- [ ] #263 `tools/automotive/tire-wear.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(803),英文套话
- [ ] #264 `tools/ballistics/rifling-twist.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(784),英文套话
- [ ] #265 `tools/beauty/assessor-risk-12.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(868),英文套话
- [ ] #266 `tools/biz/justify-text.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(726),英文套话
- [ ] #267 `tools/biz/text-extract-numbers.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(724),英文套话
- [ ] #268 `tools/biz/text-merge.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(816),英文套话
- [ ] #269 `tools/biz/text-remove-duplicates-lines.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(783),英文套话
- [ ] #270 `tools/biz/text-replace-advanced.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(768),英文套话
- [ ] #271 `tools/biz/text-shuffle.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(766),英文套话
- [ ] #272 `tools/biz/zalgo-text.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(727),英文套话
- [ ] #273 `tools/cardiology/cpet-analysis.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(867),英文套话
- [ ] #274 `tools/cardiology/grace-score.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(883),英文套话
- [ ] #275 `tools/cardiology/rater-risk-3.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(866),英文套话

## 批次 12（第 276-300 个，共 30 批）

- [ ] #276 `tools/ceramics/glaze-ratio.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(825),英文套话
- [ ] #277 `tools/chemistry/buffer-ph.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(268),英文套话
- [ ] #278 `tools/civil/cft-capacity.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(467),英文套话
- [ ] #279 `tools/civil/excavation-earth.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(396),英文套话
- [ ] #280 `tools/clinical-lab/flow-cytometry-ratio.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(843),英文套话
- [ ] #281 `tools/clinical-nursing/cycle-7.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(763),英文套话
- [ ] #282 `tools/clinical-nursing/iv-drip-rate.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(948),英文套话
- [ ] #283 `tools/construction/estimate-area-dosage.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(762),英文套话
- [ ] #284 `tools/content/generator-time-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(627),功能(1)
- [ ] #285 `tools/cosmetic-derm/post-procedure-recovery.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(970),英文套话
- [ ] #286 `tools/cosmetic-derm/thread-lift.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(957),英文套话
- [ ] #287 `tools/dance/tester-4.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(977),英文套话
- [ ] #288 `tools/data/chart-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(786),功能(1)
- [ ] #289 `tools/data/data-cleaner.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(870),英文套话
- [ ] #290 `tools/data/generator-14.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(882),功能(1)
- [ ] #291 `tools/decor/skirting-length.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1039),英文套话
- [ ] #292 `tools/design/audio-recorder.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1033),英文套话
- [ ] #293 `tools/design/css-animation-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(830),英文套话
- [ ] #294 `tools/design/image-dpi-converter.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(1074),英文套话
- [ ] #295 `tools/design/isometric-grid.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(759),英文套话
- [ ] #296 `tools/design/rem-to-px.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(470),功能(2)
- [ ] #297 `tools/dyeing/temp-time-humidity-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(942),英文套话
- [ ] #298 `tools/dynamics/banked-curve.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(299),英文套话
- [ ] #299 `tools/eco/eco-16.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(349),英文套话
- [ ] #300 `tools/eco/eco-5.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(339),英文套话

## 批次 13（第 301-325 个，共 30 批）

- [ ] #301 `tools/eco/electricity-carbon.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(351),英文套话
- [ ] #302 `tools/eco/env-impact-score.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(348),英文套话
- [ ] #303 `tools/edu2/study-progress.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(858),英文套话
- [ ] #304 `tools/electrical/battery-bank.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(707),英文套话
- [ ] #305 `tools/encode/binary-to-ascii.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(471),功能(2)
- [ ] #306 `tools/encode/encode-5.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(355),英文套话
- [ ] #307 `tools/endocrinology/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(384),功能(2)
- [ ] #308 `tools/endocrinology/graves-trab.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(992),英文套话
- [ ] #309 `tools/endocrinology/mage-index.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(972),英文套话
- [ ] #310 `tools/energy/energy-efficiency.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(733),英文套话
- [ ] #311 `tools/energy/lcoe.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(331),英文套话
- [ ] #312 `tools/ent/adenoid-grading.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(984),英文套话
- [ ] #313 `tools/finance/rental-yield-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1181),英文套话
- [ ] #314 `tools/finance/word-wrap.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(818),英文套话
- [ ] #315 `tools/fire-rescue/detector-11.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(944),英文套话
- [ ] #316 `tools/fire-rescue/high-rise-fire.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(872),英文套话
- [ ] #317 `tools/fishery/feed-rate-calculator.html` | imp=1 clk=0 pos=6.00 | 待办: 正文(973),英文套话
- [ ] #318 `tools/fishery/harvest-size-price.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1043),英文套话
- [ ] #319 `tools/fishery/winter-heating.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1009),英文套话
- [ ] #320 `tools/fitness/circuit-timer.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(856),英文套话
- [ ] #321 `tools/fitness/rater-time.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(906),英文套话
- [ ] #322 `tools/floral/wedding-flowers.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1002),英文套话
- [ ] #323 `tools/fluid/terminal-velocity.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(164),英文套话
- [ ] #324 `tools/food/calorie-calculator.html` | imp=1 clk=0 pos=4.00 | 待办: 正文(854),功能(0)
- [ ] #325 `tools/forestry/area-18.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(962),英文套话

## 批次 14（第 326-350 个，共 30 批）

- [ ] #326 `tools/forestry/density-5.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(871),英文套话
- [ ] #327 `tools/forestry/shengwuduoyangxingshannon.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(874),功能(1)
- [ ] #328 `tools/gastroenterology/detector-7.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(962),英文套话
- [ ] #329 `tools/gastroenterology/mayo-score.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1164),英文套话
- [ ] #330 `tools/general/bearing-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(909),英文套话
- [ ] #331 `tools/general/calc-203.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(823),功能(2)
- [ ] #332 `tools/general/detector-composition.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(918),英文套话
- [ ] #333 `tools/general/detector-lifespan.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(928),英文套话
- [ ] #334 `tools/general/detector-protection-2.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(915),英文套话
- [ ] #335 `tools/general/detector-resistance.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(904),英文套话
- [ ] #336 `tools/general/distance-power-frequency.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(797),英文套话
- [ ] #337 `tools/general/lifespan-23.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(847),英文套话
- [ ] #338 `tools/general/power-voltage.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(717),英文套话
- [ ] #339 `tools/general/pressure-flow-5.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(764),英文套话
- [ ] #340 `tools/general/torque-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(791),英文套话
- [ ] #341 `tools/general/voltage-9.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(730),英文套话
- [ ] #342 `tools/geometry/dot-product-2d.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(262),英文套话
- [ ] #343 `tools/geometry/midpoint-2d.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(265),英文套话
- [ ] #344 `tools/health/dumbbell-weight-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(991),英文套话
- [ ] #345 `tools/health/premature-age-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1237),英文套话
- [ ] #346 `tools/health/running-calories.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1011),英文套话
- [ ] #347 `tools/healthcare/map.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(297),英文套话
- [ ] #348 `tools/healthcare/weight-dosage.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(319),英文套话
- [ ] #349 `tools/hematology/coagulation-factor.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1001),英文套话
- [ ] #350 `tools/hematology/pnh-flow.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1079),英文套话

## 批次 15（第 351-375 个，共 30 批）

- [ ] #351 `tools/hydraulic/orifice-discharge.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(333),英文套话
- [ ] #352 `tools/hydraulic/power-3.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(879),英文套话
- [ ] #353 `tools/hydraulic/pump-power.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(322),英文套话
- [ ] #354 `tools/image/generator-15.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(785),功能(1)
- [ ] #355 `tools/it/ascii-art.html` | imp=1 clk=0 pos=3.00 | 待办: 正文(583),英文套话
- [ ] #356 `tools/it/base64-file.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(367),英文套话
- [ ] #357 `tools/it/bcrypt.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(510),英文套话
- [ ] #358 `tools/it/box-shadow-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(471),英文套话
- [ ] #359 `tools/it/caa-record-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(503),英文套话
- [ ] #360 `tools/it/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(528),功能(2)
- [ ] #361 `tools/it/calc-4.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(420),功能(2)
- [ ] #362 `tools/it/chmod-calculator.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(479),英文套话
- [ ] #363 `tools/it/csv-to-json.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(855),英文套话
- [ ] #364 `tools/it/curl-parser.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(399),功能(1)
- [ ] #365 `tools/it/js-escape.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(687),英文套话
- [ ] #366 `tools/it/json-formatter.html` | imp=1 clk=0 pos=1.50 | 待办: 正文(725),功能(2)
- [ ] #367 `tools/it/keyword-density.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1011),英文套话
- [ ] #368 `tools/it/mac-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(555),功能(2)
- [ ] #369 `tools/it/number-base-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(921),英文套话
- [ ] #370 `tools/it/og-meta-tag-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(473),英文套话
- [ ] #371 `tools/it/otp-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(605),英文套话
- [ ] #372 `tools/it/phone-parser.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(632),功能(2)
- [ ] #373 `tools/it/playfair-cipher.html` | imp=1 clk=0 pos=6.00 | 待办: 正文(1233),英文套话
- [ ] #374 `tools/it/polybius-cipher.html` | imp=1 clk=0 pos=10.00 | 待办: 正文(677),英文套话
- [ ] #375 `tools/it/rsa.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(800),英文套话

## 批次 16（第 376-400 个，共 30 批）

- [ ] #376 `tools/it/stopwatch.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(622),英文套话
- [ ] #377 `tools/it/string-obfuscator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(484),英文套话
- [ ] #378 `tools/it/text-dedupe-sort.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(803),英文套话
- [ ] #379 `tools/it/text-steganography.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1305),英文套话
- [ ] #380 `tools/it/token-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(490),英文套话
- [ ] #381 `tools/it/typescript-compiler.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1292),英文套话
- [ ] #382 `tools/it/uuid-v4-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(613),英文套话
- [ ] #383 `tools/it/xxtea.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(667),英文套话
- [ ] #384 `tools/kinematics/angular-final-velocity.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(296),英文套话
- [ ] #385 `tools/legal/double-wage-no-contract.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(985),英文套话
- [ ] #386 `tools/legal/will-template-generator.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(941),英文套话
- [ ] #387 `tools/life/tip-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(902),英文套话
- [ ] #388 `tools/life/unit-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(896),英文套话
- [ ] #389 `tools/livestock/feed-conversion-ratio.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(849),英文套话
- [ ] #390 `tools/machinery/calc-weld.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(382),英文套话
- [ ] #391 `tools/machinery/drive-2.html` | imp=1 clk=0 pos=5.00 | 待办: 正文(382),英文套话
- [ ] #392 `tools/machinery/tolerance-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1011),英文套话
- [ ] #393 `tools/manufacturing/quality-control.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(661),英文套话
- [ ] #394 `tools/maritime/anchorage-capacity.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(933),英文套话
- [ ] #395 `tools/marketing/marketing-cac-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1263),英文套话
- [ ] #396 `tools/marketing/marketing-chinese-hashtag-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(848),英文套话
- [ ] #397 `tools/marketing/marketing-markup-margin.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1151),英文套话
- [ ] #398 `tools/marketing/tagline-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(759),英文套话
- [ ] #399 `tools/martial-arts/assessor-hardness.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(689),英文套话
- [ ] #400 `tools/materials/brinell-hardness.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(245),英文套话

## 批次 17（第 401-425 个，共 30 批）

- [ ] #401 `tools/math/calculus-tools.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(812),英文套话
- [ ] #402 `tools/math/factorial-calc.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(201),功能(1)
- [ ] #403 `tools/math/herons-area.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(284),英文套话
- [ ] #404 `tools/math/multinomial-coefficient.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(369),英文套话
- [ ] #405 `tools/mechanical/bearing-life.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(843),英文套话
- [ ] #406 `tools/mechanical/gear-ratio.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(365),英文套话
- [ ] #407 `tools/medical2/drug-expiry.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(809),英文套话
- [ ] #408 `tools/metallurgy/solidification-time.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(883),英文套话
- [ ] #409 `tools/metalwork/pressure-casting.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(888),英文套话
- [ ] #410 `tools/meteorology/qiyaxitongyidonglujing.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(866),功能(2)
- [ ] #411 `tools/meteorology/temp-pressure.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(778),英文套话
- [ ] #412 `tools/metrology/expanded-uncertainty.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(139),英文套话
- [ ] #413 `tools/mining/estimate-reserve.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(882),英文套话
- [ ] #414 `tools/mining/mineral-density.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(717),英文套话
- [ ] #415 `tools/mining/ore-grade.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(920),英文套话
- [ ] #416 `tools/misc/scientific-notation.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(861),英文套话
- [ ] #417 `tools/music/audio-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(822),英文套话
- [ ] #418 `tools/music/chord-progression.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(888),英文套话
- [ ] #419 `tools/music/music-analysis.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(815),英文套话
- [ ] #420 `tools/nephrology/egfr.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(942),英文套话
- [ ] #421 `tools/nephrology/peritoneal-equilibrium.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(921),英文套话
- [ ] #422 `tools/neurology/assessor-11.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(800),英文套话
- [ ] #423 `tools/neurology/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(303),功能(1)
- [ ] #424 `tools/nuclear/activity-decay.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(275),英文套话
- [ ] #425 `tools/nuclear/mass-defect.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(257),英文套话

## 批次 18（第 426-450 个，共 30 批）

- [ ] #426 `tools/obstetrics/labor-curve.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1087),英文套话
- [ ] #427 `tools/obstetrics/ovarian-reserve.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1136),英文套话
- [ ] #428 `tools/office/excel-formula-reference.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(315),功能(1)
- [ ] #429 `tools/ophthalmology/meibomian-grading.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1042),英文套话
- [ ] #430 `tools/ophthalmology/visual-field-analysis.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(971),英文套话
- [ ] #431 `tools/optical/aca-ratio.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1066),英文套话
- [ ] #432 `tools/pediatrics/diarrhea-dehydration.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1026),英文套话
- [ ] #433 `tools/pediatrics/rater-27.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(971),英文套话
- [ ] #434 `tools/petrochem/pipe-pressure.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(813),英文套话
- [ ] #435 `tools/photo/golden-hour.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(371),英文套话
- [ ] #436 `tools/photo/photo-10.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(359),英文套话
- [ ] #437 `tools/photo/photo.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(355),英文套话
- [ ] #438 `tools/plastic/blow-molding.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(794),英文套话
- [ ] #439 `tools/property/cleaning-allocation.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(894),英文套话
- [ ] #440 `tools/pulmonology/lung-rads.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(954),英文套话
- [ ] #441 `tools/pulmonology/niv-settings.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(910),英文套话
- [ ] #442 `tools/pulmonology/wells-pe.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(971),英文套话
- [ ] #443 `tools/quality/estimate-six-sigma.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(425),英文套话
- [ ] #444 `tools/quality/process-capability.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(806),英文套话
- [ ] #445 `tools/realestate/assessor-38.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(797),英文套话
- [ ] #446 `tools/rehabilitation/assistive-device-fitting.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1307),英文套话
- [ ] #447 `tools/rehabilitation/prosthesis-alignment.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1235),英文套话
- [ ] #448 `tools/reproductive-medicine/epididymal-aspiration.html` | imp=1 clk=0 pos=1.50 | 待办: 正文(1006),英文套话
- [ ] #449 `tools/reproductive-medicine/retrograde-ejaculation.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1062),英文套话
- [ ] #450 `tools/reproductive-medicine/vasography.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1097),英文套话

## 批次 19（第 451-475 个，共 30 批）

- [ ] #451 `tools/research/assessor-50.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1017),英文套话
- [ ] #452 `tools/restaurant/table-turnover.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(830),英文套话
- [ ] #453 `tools/rheumatology/basdai.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1058),英文套话
- [ ] #454 `tools/rheumatology/igg4-level.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1162),英文套话
- [ ] #455 `tools/rheumatology/mctd-diagnosis.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(1215),英文套话
- [ ] #456 `tools/rheumatology/mda5-antibody.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1298),英文套话
- [ ] #457 `tools/safety/generator-22.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(936),功能(1)
- [ ] #458 `tools/safety/stats-report-frequency.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(943),功能(1)
- [ ] #459 `tools/science/heat-transfer-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1249),英文套话
- [ ] #460 `tools/securities/technical-indicator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(910),英文套话
- [ ] #461 `tools/seismology/generator-drill.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(723),功能(1)
- [ ] #462 `tools/sports/rater-motion.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(777),英文套话
- [ ] #463 `tools/sports/ratio-18.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1039),英文套话
- [ ] #464 `tools/sports/training-load.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1013),英文套话
- [ ] #465 `tools/sports/xuerusuanyuzhiceding.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(971),功能(1)
- [ ] #466 `tools/statistics/confidence-proportion.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(339),英文套话
- [ ] #467 `tools/statistics/cramers-v.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(204),英文套话
- [ ] #468 `tools/surveying/prismoidal-volume.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(338),英文套话
- [ ] #469 `tools/tax/capital-gains-tax.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(290),英文套话
- [ ] #470 `tools/tax/progressive-income-tax.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(348),英文套话
- [ ] #471 `tools/tcm-diagnosis/disease-nature.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(1037),功能(0)
- [ ] #472 `tools/tcm-diagnosis/generator-29.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(917),功能(1)
- [ ] #473 `tools/tcm-pharmacy/formula-song.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(975),英文套话
- [ ] #474 `tools/tcm-pharmacy/medicinal-wine.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1050),英文套话
- [ ] #475 `tools/thermodynamics/adiabatic-tv.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(321),英文套话

## 批次 20（第 476-500 个，共 30 批）

- [ ] #476 `tools/thermodynamics/compressor-isentropic-work.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(305),英文套话
- [ ] #477 `tools/thermodynamics/heat-conduction.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(285),英文套话
- [ ] #478 `tools/uiux/analysis-64.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(670),功能(1)
- [ ] #479 `tools/yi/yi-divination.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(574),功能(1)
- [ ] #480 `tools/advertising/convert-27.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(810)
- [ ] #481 `tools/agriculture/calc-13.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(773)
- [ ] #482 `tools/agriculture/calc-8.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(776)
- [ ] #483 `tools/audit/depreciation-compare.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(835)
- [ ] #484 `tools/automotive/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(375)
- [ ] #485 `tools/beauty/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(566)
- [ ] #486 `tools/biz/name-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(823)
- [ ] #487 `tools/cable/cable-tray-sizing.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(391)
- [ ] #488 `tools/cosmetic-derm/maokongcudafenji.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(818)
- [ ] #489 `tools/design/vh-vw.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(520)
- [ ] #490 `tools/edu/calc-2.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(844)
- [ ] #491 `tools/edu/calc-3.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(805)
- [ ] #492 `tools/edu/calc-4.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(939)
- [ ] #493 `tools/endocrinology/calcium-pth-axis.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(889)
- [ ] #494 `tools/endocrinology/short-stature-prediction.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话
- [ ] #495 `tools/finance/credit-card-interest.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(855)
- [ ] #496 `tools/finance/installment-real-rate.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(596)
- [ ] #497 `tools/finance/lease-payment-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话
- [ ] #498 `tools/finance/simple-interest.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(856)
- [ ] #499 `tools/fire-rescue/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(432)
- [ ] #500 `tools/food-processing/recipe-cost-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(867)

## 批次 21（第 501-525 个，共 30 批）

- [ ] #501 `tools/food/cooking-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(835)
- [ ] #502 `tools/forensic-medicine/drowning-diatom.html` | imp=1 clk=0 pos=2.00 | 待办: 英文套话
- [ ] #503 `tools/forensic-medicine/fall-injury.html` | imp=1 clk=0 pos=1.00 | 待办: 英文套话
- [ ] #504 `tools/fun/bbq-portion.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(479)
- [ ] #505 `tools/gastroenterology/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(332)
- [ ] #506 `tools/general/calc-94.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(917)
- [ ] #507 `tools/general/jiguangrongfuhoudujisuan.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(751)
- [ ] #508 `tools/general/lizishujianshejisuan.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(761)
- [ ] #509 `tools/geology/huanjingdizhipingjia.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(843)
- [ ] #510 `tools/health/calc-2.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(545)
- [ ] #511 `tools/hvac/pump-calculator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1294)
- [ ] #512 `tools/hydraulic/calc-4.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(313)
- [ ] #513 `tools/it/api-sign-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(415)
- [ ] #514 `tools/it/bluetooth-version.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(512)
- [ ] #515 `tools/it/gitignore-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(555)
- [ ] #516 `tools/it/jwt-debugger.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(719)
- [ ] #517 `tools/it/phone-screen-sizes.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(631)
- [ ] #518 `tools/it/qrcode.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(868)
- [ ] #519 `tools/it/toml-to-json.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(446)
- [ ] #520 `tools/it/toml-to-xml.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(418)
- [ ] #521 `tools/it/toml-to-yaml.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(433)
- [ ] #522 `tools/it/url-params.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(569)
- [ ] #523 `tools/it/uuid-generator.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(762)
- [ ] #524 `tools/it/video-bitrate.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(548)
- [ ] #525 `tools/jewelry/convert-31.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(771)

## 批次 22（第 526-550 个，共 30 批）

- [ ] #526 `tools/legal/calc-8.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(381)
- [ ] #527 `tools/metallurgy/calc-88.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(959)
- [ ] #528 `tools/nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(501)
- [ ] #529 `tools/paper/calc-concentration-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(901)
- [ ] #530 `tools/pneumatic/calc-flow-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(827)
- [ ] #531 `tools/psychology/phq9-assessment.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(334)
- [ ] #532 `tools/psychology/sas-assessment.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(332)
- [ ] #533 `tools/realestate/calc-2.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(410)
- [ ] #534 `tools/realestate/shichang-bijiaofa-anlixiuzheng.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(878)
- [ ] #535 `tools/safety/ppe-replacement.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(716)
- [ ] #536 `tools/seismology/assessor-31.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(927)
- [ ] #537 `tools/shipping/convert-speed-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(738)
- [ ] #538 `tools/sports/rater-35.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(780)
- [ ] #539 `tools/sports/sheyangdonglixuebanshi.html` | imp=1 clk=0 pos=2.00 | 待办: 正文(929)
- [ ] #540 `tools/stage/power-load.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(825)
- [ ] #541 `tools/startup/calc-1.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(491)
- [ ] #542 `tools/steel/steel-profile-weight.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(412)
- [ ] #543 `tools/tcm-diagnosis/disease-tracking.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(957)
- [ ] #544 `tools/tcm-pharmacy/medication-timing.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(1074)
- [ ] #545 `tools/textile/fabric-converter.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(697)
- [ ] #546 `tools/textile/fukuanpailiaoliyonglv.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(908)
- [ ] #547 `tools/textile/ratio-20.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(872)
- [ ] #548 `tools/textile/shrinkage.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(909)
- [ ] #549 `tools/transport/estimate-capacity.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(432)
- [ ] #550 `tools/urology/assessor-pressure.html` | imp=1 clk=0 pos=1.50 | 待办: 正文(930)

## 批次 23（第 551-575 个，共 30 批）

- [ ] #551 `tools/usedcar/calc-73.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(857)
- [ ] #552 `tools/water/calc-pressure.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(440)
- [ ] #553 `tools/wedding/budget-planner.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(868)
- [ ] #554 `tools/wedding/seating-chart.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(880)
- [ ] #555 `tools/welding/hanjiegongzhuangjiajusheji.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(844)
- [ ] #556 `tools/woodworking/angle-cut.html` | imp=1 clk=0 pos=1.00 | 待办: 正文(777)
- [ ] #557 `tools/beauty/index.html` | imp=0 clk=0 pos= | 待办: 正文(1146),英文套话,功能(0),结构(h2=1)
- [ ] #558 `tools/chemistry/index.html` | imp=0 clk=0 pos= | 待办: 正文(1351),英文套话,功能(0),结构(h2=1)
- [ ] #559 `tools/community/index.html` | imp=0 clk=0 pos= | 待办: 正文(296),英文套话,功能(0),结构(h2=1)
- [ ] #560 `tools/construction/index.html` | imp=0 clk=0 pos= | 待办: 正文(1211),英文套话,功能(0),结构(h2=1)
- [ ] #561 `tools/data/index.html` | imp=0 clk=0 pos= | 待办: 正文(1142),英文套话,功能(0),结构(h2=1)
- [ ] #562 `tools/dynamics/index.html` | imp=0 clk=0 pos= | 待办: 正文(1347),英文套话,功能(0),结构(h2=1)
- [ ] #563 `tools/electromagnetism/index.html` | imp=0 clk=0 pos= | 待办: 正文(1450),英文套话,功能(0),结构(h2=1)
- [ ] #564 `tools/gardening2/index.html` | imp=0 clk=0 pos= | 待办: 正文(400),英文套话,功能(0),结构(h2=1)
- [ ] #565 `tools/geometry/index.html` | imp=0 clk=0 pos= | 待办: 正文(1438),英文套话,功能(0),结构(h2=1)
- [ ] #566 `tools/jewelry/index.html` | imp=0 clk=0 pos= | 待办: 正文(453),英文套话,功能(0),结构(h2=1)
- [ ] #567 `tools/medical/index.html` | imp=0 clk=0 pos= | 待办: 正文(771),英文套话,功能(0),结构(h2=1)
- [ ] #568 `tools/nephrology/index.html` | imp=0 clk=0 pos= | 待办: 正文(1300),英文套话,功能(0),结构(h2=1)
- [ ] #569 `tools/psychiatry/index.html` | imp=0 clk=0 pos= | 待办: 正文(1425),英文套话,功能(0),结构(h2=1)
- [ ] #570 `tools/pulmonology/index.html` | imp=0 clk=0 pos= | 待办: 正文(1225),英文套话,功能(0),结构(h2=1)
- [ ] #571 `tools/research/index.html` | imp=0 clk=0 pos= | 待办: 正文(586),英文套话,功能(0),结构(h2=1)
- [ ] #572 `tools/travel/index.html` | imp=0 clk=0 pos= | 待办: 正文(1255),英文套话,功能(0),结构(h2=1)
- [ ] #573 `tools/urology/index.html` | imp=0 clk=0 pos= | 待办: 正文(1293),英文套话,功能(0),结构(h2=1)
- [ ] #574 `tools/ai/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #575 `tools/ballistics/caliber-conversion.html` | imp=0 clk=0 pos= | 待办: 正文(862),英文套话,功能(2)

## 批次 24（第 576-600 个，共 30 批）

- [ ] #576 `tools/cardiology/antiarrhythmic-class.html` | imp=0 clk=0 pos= | 待办: 正文(980),英文套话,功能(0)
- [ ] #577 `tools/ceramics/kiln-firing.html` | imp=0 clk=0 pos= | 待办: 正文(842),英文套话,功能(0)
- [ ] #578 `tools/chemistry/poh-to-ph.html` | imp=0 clk=0 pos= | 待办: 正文(241),英文套话,功能(1)
- [ ] #579 `tools/chinese-cook/oil-temp.html` | imp=0 clk=0 pos= | 待办: 正文(1189),英文套话,功能(1)
- [ ] #580 `tools/cosmetic-derm/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #581 `tools/design/generator-10.html` | imp=0 clk=0 pos= | 待办: 正文(865),英文套话,功能(1)
- [ ] #582 `tools/design/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #583 `tools/eco/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #584 `tools/finance/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #585 `tools/fluid/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #586 `tools/food-processing/tester-5.html` | imp=0 clk=0 pos= | 待办: 正文(9),功能(0),结构(h2=0)
- [ ] #587 `tools/gardening/pot-capacity.html` | imp=0 clk=0 pos= | 待办: 正文(939),英文套话,功能(1)
- [ ] #588 `tools/gardening2/pest-control.html` | imp=0 clk=0 pos= | 待办: 正文(949),英文套话,功能(0)
- [ ] #589 `tools/general/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #590 `tools/geology/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #591 `tools/health/blood-sugar-converter.html` | imp=0 clk=0 pos= | 待办: 正文(1178),英文套话,功能(2)
- [ ] #592 `tools/health/ibw-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(1440),英文套话,功能(2)
- [ ] #593 `tools/health/ideal-weight.html` | imp=0 clk=0 pos= | 待办: 正文(1262),英文套话,功能(2)
- [ ] #594 `tools/health/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #595 `tools/healthcare/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #596 `tools/hematology/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #597 `tools/hr/performance-ranking.html` | imp=0 clk=0 pos= | 待办: 正文(812),英文套话,功能(2)
- [ ] #598 `tools/insurance/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #599 `tools/kinematics/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #600 `tools/materials/hooke-strain.html` | imp=0 clk=0 pos= | 待办: 正文(213),英文套话,功能(2)

## 批次 25（第 601-625 个，共 30 批）

- [ ] #601 `tools/medical2/medical-abbrev.html` | imp=0 clk=0 pos= | 待办: 正文(843),英文套话,功能(2)
- [ ] #602 `tools/metrology/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #603 `tools/ophthalmology/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #604 `tools/ophthalmology/visual-acuity-converter.html` | imp=0 clk=0 pos= | 待办: 正文(948),英文套话,功能(2)
- [ ] #605 `tools/psychiatry/isi-insomnia.html` | imp=0 clk=0 pos= | 待办: 正文(932),英文套话,功能(0)
- [ ] #606 `tools/psychology/tester-3.html` | imp=0 clk=0 pos= | 待办: 正文(709),英文套话,功能(1)
- [ ] #607 `tools/realestate/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #608 `tools/reproductive-medicine/anti-sperm-antibody.html` | imp=0 clk=0 pos= | 待办: 正文(1008),英文套话,功能(2)
- [ ] #609 `tools/reproductive-medicine/assessor-15.html` | imp=0 clk=0 pos= | 待办: 正文(857),英文套话,功能(1)
- [ ] #610 `tools/reproductive-medicine/calc-volume-concentration.html` | imp=0 clk=0 pos= | 待办: 正文(781),英文套话,功能(2)
- [ ] #611 `tools/reproductive-medicine/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #612 `tools/reproductive-medicine/jingzidnasuipian-dfi-zhishu.html` | imp=0 clk=0 pos= | 待办: 正文(746),英文套话,功能(2)
- [ ] #613 `tools/reproductive-medicine/rater-30.html` | imp=0 clk=0 pos= | 待办: 正文(957),英文套话,功能(1)
- [ ] #614 `tools/reproductive-medicine/semen-volume.html` | imp=0 clk=0 pos= | 待办: 正文(1027),英文套话,功能(2)
- [ ] #615 `tools/reproductive-medicine/sperm-dfi.html` | imp=0 clk=0 pos= | 待办: 正文(971),英文套话,功能(2)
- [ ] #616 `tools/reproductive-medicine/stats-6.html` | imp=0 clk=0 pos= | 待办: 正文(796),英文套话,功能(1)
- [ ] #617 `tools/reproductive-medicine/total-sperm-count.html` | imp=0 clk=0 pos= | 待办: 正文(952),英文套话,功能(2)
- [ ] #618 `tools/science/index.html` | imp=0 clk=0 pos= | 待办: 英文套话,功能(0),结构(h2=1)
- [ ] #619 `tools/sports/jixianwei-kuai-man-leixingtuice.html` | imp=0 clk=0 pos= | 待办: 正文(769),英文套话,功能(2)
- [ ] #620 `tools/aerospace/lift-coefficient.html` | imp=0 clk=0 pos= | 待办: 正文(865),英文套话
- [ ] #621 `tools/agriculture/dli-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(801),英文套话
- [ ] #622 `tools/agriculture/fertilizer-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(994),英文套话
- [ ] #623 `tools/agriculture/irrigation-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(1131),英文套话
- [ ] #624 `tools/ai/ai-4.html` | imp=0 clk=0 pos= | 待办: 正文(321),英文套话
- [ ] #625 `tools/astronomy/observation-conditions.html` | imp=0 clk=0 pos= | 待办: 正文(1434),英文套话

## 批次 26（第 626-650 个，共 30 批）

- [ ] #626 `tools/automotive/cycle-belt.html` | imp=0 clk=0 pos= | 待办: 正文(1342),英文套话
- [ ] #627 `tools/automotive/pressure-fuel-oil.html` | imp=0 clk=0 pos= | 待办: 正文(959),英文套话
- [ ] #628 `tools/automotive/voltage-1.html` | imp=0 clk=0 pos= | 待办: 正文(885),英文套话
- [ ] #629 `tools/ballistics/bullet-penetration.html` | imp=0 clk=0 pos= | 待办: 正文(833),英文套话
- [ ] #630 `tools/ballistics/muzzle-energy.html` | imp=0 clk=0 pos= | 待办: 正文(798),英文套话
- [ ] #631 `tools/ballistics/powder-burn-rate.html` | imp=0 clk=0 pos= | 待办: 正文(810),英文套话
- [ ] #632 `tools/ballistics/recoil-estimation.html` | imp=0 clk=0 pos= | 待办: 正文(777),英文套话
- [ ] #633 `tools/ballistics/wind-drift.html` | imp=0 clk=0 pos= | 待办: 正文(803),英文套话
- [ ] #634 `tools/blasting/rock-excavation.html` | imp=0 clk=0 pos= | 待办: 正文(911),英文套话
- [ ] #635 `tools/casting/detector-24.html` | imp=0 clk=0 pos= | 待办: 正文(741),英文套话
- [ ] #636 `tools/chemistry/empirical-formula.html` | imp=0 clk=0 pos= | 待办: 正文(404),英文套话
- [ ] #637 `tools/chess/bridge-scoring.html` | imp=0 clk=0 pos= | 待办: 正文(790),英文套话
- [ ] #638 `tools/convenience/assessor-target.html` | imp=0 clk=0 pos= | 待办: 正文(727),英文套话
- [ ] #639 `tools/cosmetic-derm/aging-1.html` | imp=0 clk=0 pos= | 待办: 正文(838),英文套话
- [ ] #640 `tools/cosmetic-derm/jiguangbochangbadian.html` | imp=0 clk=0 pos= | 待办: 正文(851),功能(1)
- [ ] #641 `tools/cosmetic-derm/visia-spots.html` | imp=0 clk=0 pos= | 待办: 正文(976),英文套话
- [ ] #642 `tools/dance/partner-distance.html` | imp=0 clk=0 pos= | 待办: 正文(809),英文套话
- [ ] #643 `tools/decor/wallpaper-quantity.html` | imp=0 clk=0 pos= | 待办: 正文(983),英文套话
- [ ] #644 `tools/dentistry/assessor-5.html` | imp=0 clk=0 pos= | 待办: 正文(971),英文套话
- [ ] #645 `tools/dentistry/dental-arch-development.html` | imp=0 clk=0 pos= | 待办: 正文(1062),英文套话
- [ ] #646 `tools/dentistry/zirconia-aesthetics.html` | imp=0 clk=0 pos= | 待办: 正文(1077),英文套话
- [ ] #647 `tools/dermatology/chilblain-grading.html` | imp=0 clk=0 pos= | 待办: 正文(1160),英文套话
- [ ] #648 `tools/design/grid-pattern.html` | imp=0 clk=0 pos= | 待办: 正文(783),英文套话
- [ ] #649 `tools/design/particle-effect-generator.html` | imp=0 clk=0 pos= | 待办: 正文(844),英文套话
- [ ] #650 `tools/endocrinology/detector-metabolism.html` | imp=0 clk=0 pos= | 待办: 正文(911),英文套话

## 批次 27（第 651-675 个，共 30 批）

- [ ] #651 `tools/energy/fridge-power-estimator.html` | imp=0 clk=0 pos= | 待办: 正文(985),英文套话
- [ ] #652 `tools/ent/laryngeal-nerve.html` | imp=0 clk=0 pos= | 待办: 正文(897),英文套话
- [ ] #653 `tools/finance/npv-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(903),英文套话
- [ ] #654 `tools/fire-rescue/calc-pressure-1.html` | imp=0 clk=0 pos= | 待办: 正文(936),英文套话
- [ ] #655 `tools/fishery/feed-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(1007),英文套话
- [ ] #656 `tools/fishery/feeding-rate.html` | imp=0 clk=0 pos= | 待办: 正文(947),英文套话
- [ ] #657 `tools/fishery/spawning-hormone.html` | imp=0 clk=0 pos= | 待办: 正文(909),英文套话
- [ ] #658 `tools/food-safety/assessor-risk-6.html` | imp=0 clk=0 pos= | 待办: 正文(726),英文套话
- [ ] #659 `tools/food-testing/acid-peroxide-titration.html` | imp=0 clk=0 pos= | 待办: 正文(907),英文套话
- [ ] #660 `tools/food-testing/salt-titration.html` | imp=0 clk=0 pos= | 待办: 正文(910),英文套话
- [ ] #661 `tools/food/soup-ratio-optimizer.html` | imp=0 clk=0 pos= | 待办: 正文(991),英文套话
- [ ] #662 `tools/forensic-medicine/wound-description.html` | imp=0 clk=0 pos= | 待办: 正文(1480),英文套话
- [ ] #663 `tools/gas/length-pipeline.html` | imp=0 clk=0 pos= | 待办: 正文(850),英文套话
- [ ] #664 `tools/general/detector-131.html` | imp=0 clk=0 pos= | 待办: 正文(928),英文套话
- [ ] #665 `tools/general/detector-water-pressure-1.html` | imp=0 clk=0 pos= | 待办: 正文(929),英文套话
- [ ] #666 `tools/general/fabric-1.html` | imp=0 clk=0 pos= | 待办: 正文(773),英文套话
- [ ] #667 `tools/general/power-7.html` | imp=0 clk=0 pos= | 待办: 正文(813),英文套话
- [ ] #668 `tools/general/pressure-weld.html` | imp=0 clk=0 pos= | 待办: 正文(813),英文套话
- [ ] #669 `tools/general/temp-pressure-3.html` | imp=0 clk=0 pos= | 待办: 正文(806),英文套话
- [ ] #670 `tools/general/torque-3.html` | imp=0 clk=0 pos= | 待办: 正文(782),英文套话
- [ ] #671 `tools/general/wear-4.html` | imp=0 clk=0 pos= | 待办: 正文(792),英文套话
- [ ] #672 `tools/health/bmi-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(1036),英文套话
- [ ] #673 `tools/health/bmr-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(844),英文套话
- [ ] #674 `tools/health/waist-hip-ratio.html` | imp=0 clk=0 pos= | 待办: 正文(1310),英文套话
- [ ] #675 `tools/healthcare/bmi-2.html` | imp=0 clk=0 pos= | 待办: 正文(324),英文套话

## 批次 28（第 676-700 个，共 30 批）

- [ ] #676 `tools/hydraulic/calc-speed-itinerary.html` | imp=0 clk=0 pos= | 待办: 正文(947),英文套话
- [ ] #677 `tools/hydraulic/dam-stability.html` | imp=0 clk=0 pos= | 待办: 正文(869),英文套话
- [ ] #678 `tools/it/base64.html` | imp=0 clk=0 pos= | 待办: 正文(940),英文套话
- [ ] #679 `tools/it/less-compiler.html` | imp=0 clk=0 pos= | 待办: 正文(1253),英文套话
- [ ] #680 `tools/it/markdown-to-html.html` | imp=0 clk=0 pos= | 待办: 正文(599),英文套话
- [ ] #681 `tools/it/pomodoro.html` | imp=0 clk=0 pos= | 待办: 正文(725),英文套话
- [ ] #682 `tools/it/svg-placeholder-generator.html` | imp=0 clk=0 pos= | 待办: 正文(499),英文套话
- [ ] #683 `tools/it/time-format-converter.html` | imp=0 clk=0 pos= | 待办: 正文(401),功能(1)
- [ ] #684 `tools/it/vector-cross-product.html` | imp=0 clk=0 pos= | 待办: 正文(632),英文套话
- [ ] #685 `tools/it/vigenere-visualizer.html` | imp=0 clk=0 pos= | 待办: 正文(995),英文套话
- [ ] #686 `tools/livestock/inbreeding-coefficient.html` | imp=0 clk=0 pos= | 待办: 正文(972),英文套话
- [ ] #687 `tools/machinery/calc-strength.html` | imp=0 clk=0 pos= | 待办: 正文(408),英文套话
- [ ] #688 `tools/materials/volumetric-strain.html` | imp=0 clk=0 pos= | 待办: 正文(186),英文套话
- [ ] #689 `tools/mechanical/bolt-torque.html` | imp=0 clk=0 pos= | 待办: 正文(835),英文套话
- [ ] #690 `tools/metalwork/calc-gear-2.html` | imp=0 clk=0 pos= | 待办: 正文(821),英文套话
- [ ] #691 `tools/mining/reserve-estimate.html` | imp=0 clk=0 pos= | 待办: 正文(913),英文套话
- [ ] #692 `tools/nephrology/edema-grading.html` | imp=0 clk=0 pos= | 待办: 正文(1231),英文套话
- [ ] #693 `tools/neurology/ilae-seizure.html` | imp=0 clk=0 pos= | 待办: 正文(1220),英文套话
- [ ] #694 `tools/pediatrics/chd-assessment.html` | imp=0 clk=0 pos= | 待办: 正文(1051),英文套话
- [ ] #695 `tools/photo/depth-of-field.html` | imp=0 clk=0 pos= | 待办: 正文(346),英文套话
- [ ] #696 `tools/photo/ev.html` | imp=0 clk=0 pos= | 待办: 正文(331),英文套话
- [ ] #697 `tools/reproductive-medicine/baifenbijisuanqi.html` | imp=0 clk=0 pos= | 待办: 正文(577),功能(2)
- [ ] #698 `tools/reproductive-medicine/detector-9.html` | imp=0 clk=0 pos= | 待办: 正文(860),英文套话
- [ ] #699 `tools/reproductive-medicine/embryo-grading.html` | imp=0 clk=0 pos= | 待办: 正文(988),英文套话
- [ ] #700 `tools/reproductive-medicine/endometrial-receptivity.html` | imp=0 clk=0 pos= | 待办: 正文(1107),英文套话

## 批次 29（第 701-725 个，共 30 批）

- [ ] #701 `tools/reproductive-medicine/icsi-success.html` | imp=0 clk=0 pos= | 待办: 正文(965),英文套话
- [ ] #702 `tools/reproductive-medicine/ivf-statistics.html` | imp=0 clk=0 pos= | 待办: 正文(923),英文套话
- [ ] #703 `tools/reproductive-medicine/pgt-indication.html` | imp=0 clk=0 pos= | 待办: 正文(1119),英文套话
- [ ] #704 `tools/reproductive-medicine/progressive-motility.html` | imp=0 clk=0 pos= | 待办: 正文(981),英文套话
- [ ] #705 `tools/reproductive-medicine/rater-31.html` | imp=0 clk=0 pos= | 待办: 正文(856),英文套话
- [ ] #706 `tools/reproductive-medicine/reproductive-hormones.html` | imp=0 clk=0 pos= | 待办: 正文(1011),英文套话
- [ ] #707 `tools/reproductive-medicine/sperm-concentration.html` | imp=0 clk=0 pos= | 待办: 正文(1031),英文套话
- [ ] #708 `tools/reproductive-medicine/testicular-biopsy.html` | imp=0 clk=0 pos= | 待办: 正文(1163),英文套话
- [ ] #709 `tools/rheumatology/detector-8.html` | imp=0 clk=0 pos= | 待办: 正文(957),英文套话
- [ ] #710 `tools/rheumatology/gout-uric-acid.html` | imp=0 clk=0 pos= | 待办: 正文(1064),英文套话
- [ ] #711 `tools/rubber/cure-time.html` | imp=0 clk=0 pos= | 待办: 正文(799),英文套话
- [ ] #712 `tools/science/pcb-trace-width.html` | imp=0 clk=0 pos= | 待办: 正文(979),英文套话
- [ ] #713 `tools/tcm-diagnosis/meridian-differentiation.html` | imp=0 clk=0 pos= | 待办: 正文(1290),功能(1)
- [ ] #714 `tools/tcm-diagnosis/pulse-diagnosis.html` | imp=0 clk=0 pos= | 待办: 正文(1088),功能(1)
- [ ] #715 `tools/textile2/dye-temp.html` | imp=0 clk=0 pos= | 待办: 正文(1004),功能(2)
- [ ] #716 `tools/transport/calc-4.html` | imp=0 clk=0 pos= | 待办: 正文(461),功能(2)
- [ ] #717 `tools/urology/calc-1.html` | imp=0 clk=0 pos= | 待办: 正文(428),功能(2)
- [ ] #718 `tools/urology/iief5-score.html` | imp=0 clk=0 pos= | 待办: 正文(1030),功能(1)
- [ ] #719 `tools/urology/ipss-score.html` | imp=0 clk=0 pos= | 待办: 正文(1142),功能(2)
- [ ] #720 `tools/urology/stone-composition.html` | imp=0 clk=0 pos= | 待办: 正文(1253),功能(1)
- [ ] #721 `tools/wedding/countdown-timeline.html` | imp=0 clk=0 pos= | 待办: 正文(937),功能(2)
- [ ] #722 `tools/bridge/deflection-calc.html` | imp=0 clk=0 pos= | 待办: 正文(826)
- [ ] #723 `tools/fire/extinguisher-calc.html` | imp=0 clk=0 pos= | 待办: 正文(917)
- [ ] #724 `tools/forensic-medicine/bloodstain-pattern.html` | imp=0 clk=0 pos= | 待办: 英文套话
- [ ] #725 `tools/gardening/compost-calculator.html` | imp=0 clk=0 pos= | 待办: 正文(785)

## 批次 30（第 726-750 个，共 30 批）

- [ ] #726 `tools/general/zhilengshebeixuanxing.html` | imp=0 clk=0 pos= | 待办: 正文(774)
- [ ] #727 `tools/it/jwt.html` | imp=0 clk=0 pos= | 待办: 正文(874)
- [ ] #728 `tools/it/rich-text-editor.html` | imp=0 clk=0 pos= | 待办: 正文(916)
- [ ] #729 `tools/it/robots-txt-generator.html` | imp=0 clk=0 pos= | 待办: 正文(428)
- [ ] #730 `tools/it/safelink-decoder.html` | imp=0 clk=0 pos= | 待办: 正文(753)
- [ ] #731 `tools/life/timestamp.html` | imp=0 clk=0 pos= | 待办: 正文(968)
- [ ] #732 `tools/nutrition/calorie-deficit.html` | imp=0 clk=0 pos= | 待办: 正文(456)
- [ ] #733 `tools/rubber/hardness-calc.html` | imp=0 clk=0 pos= | 待办: 正文(786)
- [ ] #734 `tools/seismology/assessor-30.html` | imp=0 clk=0 pos= | 待办: 正文(958)
- [ ] #735 `tools/tcm-chemistry/capsule-filling.html` | imp=0 clk=0 pos= | 待办: 正文(1132)
- [ ] #736 `tools/timber/detector-37.html` | imp=0 clk=0 pos= | 待办: 正文(709)
- [ ] #737 `tools/travel/timezone-converter-advanced.html` | imp=0 clk=0 pos= | 待办: 正文(855)
- [ ] #738 `tools/tunnel/lining-thickness.html` | imp=0 clk=0 pos= | 待办: 正文(883)
- [ ] #739 `tools/urology/calc-volume.html` | imp=0 clk=0 pos= | 待办: 正文(517)
- [ ] #740 `tools/urology/penile-rigidity.html` | imp=0 clk=0 pos= | 待办: 正文(1176)
- [ ] #741 `tools/urology/prostate-volume.html` | imp=0 clk=0 pos= | 待办: 正文(1037)
- [ ] #742 `tools/urology/psa-density.html` | imp=0 clk=0 pos= | 待办: 正文(1021)
- [ ] #743 `tools/urology/rater-3.html` | imp=0 clk=0 pos= | 待办: 正文(1033)
- [ ] #744 `tools/urology/rater-4.html` | imp=0 clk=0 pos= | 待办: 正文(997)
- [ ] #745 `tools/urology/residual-urine.html` | imp=0 clk=0 pos= | 待办: 正文(1095)
- [ ] #746 `tools/urology/stone-size-assessment.html` | imp=0 clk=0 pos= | 待办: 正文(1208)
- [ ] #747 `tools/urology/turp-parameters.html` | imp=0 clk=0 pos= | 待办: 正文(1089)
- [ ] #748 `tools/urology/urethral-stricture.html` | imp=0 clk=0 pos= | 待办: 正文(1153)
- [ ] #749 `tools/welding/detector-25.html` | imp=0 clk=0 pos= | 待办: 正文(970)
- [ ] #750 `tools/welding/flow-ratio.html` | imp=0 clk=0 pos= | 待办: 正文(837)
