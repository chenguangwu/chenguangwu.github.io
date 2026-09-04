# Google Search Console 人工编入索引任务

属性：`https://chenguangwu.github.io/`
操作入口：<https://search.google.com/search-console?resource_id=https://chenguangwu.github.io/>
浏览器要求：必须使用已登录 Google 账号的 Google Chrome。

## 执行规则

- 通过“网址检查”输入完整 URL，先确认是否已编入索引；已编入索引的地址记录到“已收录/跳过”，不再请求。
- 未收录地址点击“请求编入索引”；每个属性每天约 10 次，达到配额后停止并保留队列。
- 严格按阶段执行：先完成“行业分类首页”，再处理“热门工具”。
- 每次操作后记录日期、结果和 Search Console 页面显示的提示；不要把“检查 URL”误记为“已提交”。
- 行业首页名单来自当前 `tools/*/index.html` 扫描，共 276 个；热门工具名单来自 `analytics_traffic_merged.csv` 按 impressions 降序、clicks 降序选取的 60 个工具（排除分类首页）。

## 本次执行

- 开始日期：2026-09-04
- 当日请求编入索引次数：5
- 当前阶段：行业分类首页
- 备注：本文件用于后续每日人工操作，完成一项就把地址从待处理区移到已提交或已收录/跳过区。

## 已提交

- 2026-09-04：`https://chenguangwu.github.io/tools/accessibility/index.html`（Search Console 显示“已请求编入索引”，已加入优先抓取队列）
- 2026-09-04：`https://chenguangwu.github.io/tools/accounting/index.html`（Search Console 显示“已请求编入索引”，已加入优先抓取队列）
- 2026-09-04：`https://chenguangwu.github.io/tools/acoustics/index.html`（Search Console 显示“已请求编入索引”，已加入优先抓取队列）
- 2026-09-04：`https://chenguangwu.github.io/tools/acupuncture/index.html`（Search Console 显示“已请求编入索引”，已加入优先抓取队列）
- 2026-09-04：`https://chenguangwu.github.io/tools/admin/index.html`（Search Console 显示“已请求编入索引”，已加入优先抓取队列）

## 已收录/跳过

（暂无；只有 Search Console 明确显示“网址已在 Google 上”时记录。）

## 今日配额后留待明日

- 2026-09-04：`https://chenguangwu.github.io/tools/advertising/index.html`（已检查：未收录；请求时 Google 明确提示“超出了配额”，未提交成功）

## 待提交：行业分类首页（第一阶段）

按热度排序；热度按 `analytics_traffic_merged.csv` 中各行业工具页 impressions 总量降序、clicks 总量降序、工具页数量降序、行业名排序；已提交/配额区不重复进入队列。

```text
tools/it/index.html
tools/science/index.html
tools/finance/index.html
tools/video/index.html
tools/general/index.html
tools/design/index.html
tools/sports/index.html
tools/agriculture/index.html
tools/biz/index.html
tools/math/index.html
tools/legal/index.html
tools/life/index.html
tools/health/index.html
tools/fun/index.html
tools/reproductive-medicine/index.html
tools/music/index.html
tools/parenting/index.html
tools/edu/index.html
tools/fishery/index.html
tools/statistics/index.html
tools/rheumatology/index.html
tools/ai/index.html
tools/cardiology/index.html
tools/marketing/index.html
tools/endocrinology/index.html
tools/energy/index.html
tools/data/index.html
tools/meteorology/index.html
tools/nephrology/index.html
tools/ophthalmology/index.html
tools/automotive/index.html
tools/hydraulic/index.html
tools/astronomy/index.html
tools/eco/index.html
tools/kinematics/index.html
tools/nuclear/index.html
tools/quantum/index.html
tools/tax/index.html
tools/textile/index.html
tools/livestock/index.html
tools/clinical-lab/index.html
tools/cosmetic-derm/index.html
tools/photo/index.html
tools/tcm-diagnosis/index.html
tools/fire-rescue/index.html
tools/machinery/index.html
tools/mining/index.html
tools/beauty/index.html
tools/clinical-nursing/index.html
tools/fitness/index.html
tools/forestry/index.html
tools/gastroenterology/index.html
tools/geometry/index.html
tools/hematology/index.html
tools/language/index.html
tools/metallurgy/index.html
tools/misc/index.html
tools/pulmonology/index.html
tools/realestate/index.html
tools/rehabilitation/index.html
tools/safety/index.html
tools/signal/index.html
tools/surveying/index.html
tools/tcm-pharmacy/index.html
tools/thermodynamics/index.html
tools/content/index.html
tools/fengshui/index.html
tools/blasting/index.html
tools/hvac/index.html
tools/paper/index.html
tools/funeral/index.html
tools/chemistry/index.html
tools/forensic-medicine/index.html
tools/materials/index.html
tools/chinese-cook/index.html
tools/dance/index.html
tools/food/index.html
tools/healthcare/index.html
tools/mechanical/index.html
tools/metalwork/index.html
tools/neurology/index.html
tools/pediatrics/index.html
tools/psychology/index.html
tools/seismology/index.html
tools/wedding/index.html
tools/cable/index.html
tools/civil/index.html
tools/electromagnetism/index.html
tools/encode/index.html
tools/geology/index.html
tools/obstetrics/index.html
tools/office/index.html
tools/optical/index.html
tools/optics/index.html
tools/quality/index.html
tools/urology/index.html
tools/ballistics/index.html
tools/gardening/index.html
tools/welding/index.html
tools/aerospace/index.html
tools/ceramics/index.html
tools/decor/index.html
tools/ent/index.html
tools/food-processing/index.html
tools/medical2/index.html
tools/psychiatry/index.html
tools/transport/index.html
tools/audit/index.html
tools/banking/index.html
tools/construction/index.html
tools/dyeing/index.html
tools/dynamics/index.html
tools/economics/index.html
tools/edu2/index.html
tools/electrical/index.html
tools/exhibition/index.html
tools/floral/index.html
tools/fluid/index.html
tools/futures/index.html
tools/image/index.html
tools/jewelry/index.html
tools/leather/index.html
tools/manufacturing/index.html
tools/maritime/index.html
tools/martial-arts/index.html
tools/medical/index.html
tools/metrology/index.html
tools/network/index.html
tools/petrochem/index.html
tools/plastic/index.html
tools/pneumatic/index.html
tools/property/index.html
tools/research/index.html
tools/restaurant/index.html
tools/robotics/index.html
tools/securities/index.html
tools/shipping/index.html
tools/stage/index.html
tools/startup/index.html
tools/steel/index.html
tools/structural/index.html
tools/uiux/index.html
tools/usedcar/index.html
tools/water/index.html
tools/woodworking/index.html
tools/yi/index.html
tools/dentistry/index.html
tools/food-testing/index.html
tools/rubber/index.html
tools/bridge/index.html
tools/casting/index.html
tools/chess/index.html
tools/convenience/index.html
tools/dermatology/index.html
tools/fire/index.html
tools/food-safety/index.html
tools/gardening2/index.html
tools/gas/index.html
tools/hr/index.html
tools/nutrition/index.html
tools/tcm-chemistry/index.html
tools/textile2/index.html
tools/timber/index.html
tools/travel/index.html
tools/tunnel/index.html
tools/antiques/index.html
tools/aquaculture/index.html
tools/archaeology/index.html
tools/archive/index.html
tools/audio/index.html
tools/auto-beauty/index.html
tools/automation/index.html
tools/baking/index.html
tools/beekeeping/index.html
tools/beneficiation/index.html
tools/bonding/index.html
tools/brand/index.html
tools/building-material/index.html
tools/chemical/index.html
tools/chinese/index.html
tools/cleaning/index.html
tools/cnc/index.html
tools/cognition/index.html
tools/colorvision/index.html
tools/community/index.html
tools/consulting/index.html
tools/cosmetics/index.html
tools/customer-service/index.html
tools/daily-goods/index.html
tools/dailychem/index.html
tools/defense/index.html
tools/discipline/index.html
tools/domestic/index.html
tools/ecommerce/index.html
tools/elderly/index.html
tools/electronics/index.html
tools/embedded/index.html
tools/engineering/index.html
tools/environment/index.html
tools/event/index.html
tools/exam/index.html
tools/express/index.html
tools/film/index.html
tools/forex/index.html
tools/fresh/index.html
tools/furniture/index.html
tools/gis/index.html
tools/glass/index.html
tools/hardware/index.html
tools/heattreat/index.html
tools/history/index.html
tools/home/index.html
tools/hotel/index.html
tools/insurance/index.html
tools/interior/index.html
tools/investment/index.html
tools/kids/index.html
tools/knowledge/index.html
tools/labor-protection/index.html
tools/landscape/index.html
tools/legal2/index.html
tools/library/index.html
tools/livestream/index.html
tools/logistics/index.html
tools/logistics2/index.html
tools/martial/index.html
tools/media/index.html
tools/misc2/index.html
tools/mold/index.html
tools/municipal/index.html
tools/museum/index.html
tools/niche/index.html
tools/outdoor/index.html
tools/packaging/index.html
tools/paint/index.html
tools/pet/index.html
tools/pet-training/index.html
tools/pets/index.html
tools/pharma/index.html
tools/pharmacy/index.html
tools/photo2/index.html
tools/photography/index.html
tools/pipe/index.html
tools/port/index.html
tools/pr/index.html
tools/printing/index.html
tools/process/index.html
tools/procurement/index.html
tools/project/index.html
tools/railway/index.html
tools/rental/index.html
tools/road/index.html
tools/sales/index.html
tools/security/index.html
tools/security-guard/index.html
tools/service/index.html
tools/sports-event/index.html
tools/stats/index.html
tools/stone/index.html
tools/supplychain/index.html
tools/surface/index.html
tools/telecom/index.html
tools/text/index.html
tools/unitedfront/index.html
tools/urban/index.html
tools/valve/index.html
tools/warehouse/index.html
tools/woodwork/index.html
tools/writing/index.html
tools/yoga/index.html
```

## 待提交：热门工具（第二阶段，共 60 个）

来源：`analytics_traffic_merged.csv`；括号内为来源快照的 impressions/clicks，仅用于排序，不代表 Google 收录状态。

```text
https://chenguangwu.github.io/tools/it/id-card-generator.html  # 105/0
https://chenguangwu.github.io/tools/video/video-speed.html  # 26/0
https://chenguangwu.github.io/tools/science/sample-size-calculator.html  # 17/0
https://chenguangwu.github.io/tools/finance/lottery-odds-calculator.html  # 16/0
https://chenguangwu.github.io/tools/science/factorial-calculator.html  # 12/0
https://chenguangwu.github.io/tools/it/invite-code-generator.html  # 9/1
https://chenguangwu.github.io/tools/parenting/growth-chart.html  # 8/6
https://chenguangwu.github.io/tools/it/password-generator.html  # 8/0
https://chenguangwu.github.io/tools/legal/arbitration-fee.html  # 6/0
https://chenguangwu.github.io/tools/reproductive-medicine/testicular-volume.html  # 5/0
https://chenguangwu.github.io/tools/finance/iccid-validator.html  # 4/2
https://chenguangwu.github.io/tools/finance/compound-interest.html  # 4/0
https://chenguangwu.github.io/tools/fishery/mesh-size-guide.html  # 4/0
https://chenguangwu.github.io/tools/math/formula-calculator.html  # 4/0
https://chenguangwu.github.io/tools/accessibility/braille-translator.html  # 3/5
https://chenguangwu.github.io/tools/health/blood-type-calculator.html  # 3/2
https://chenguangwu.github.io/tools/cardiology/myocardial-bridge.html  # 3/0
https://chenguangwu.github.io/tools/clinical-lab/mic-breakpoint.html  # 3/0
https://chenguangwu.github.io/tools/fengshui/fengshui-calculator.html  # 3/0
https://chenguangwu.github.io/tools/it/js-obfuscator.html  # 3/0
https://chenguangwu.github.io/tools/life/radiation-converter.html  # 3/0
https://chenguangwu.github.io/tools/livestock/heat-stress-index.html  # 3/0
https://chenguangwu.github.io/tools/science/median-calculator.html  # 3/0
https://chenguangwu.github.io/tools/science/physics-calculator.html  # 3/0
https://chenguangwu.github.io/tools/video/subtitle-tool.html  # 3/0
https://chenguangwu.github.io/tools/design/iso-noise-reference.html  # 2/1
https://chenguangwu.github.io/tools/edu/capital-quiz.html  # 2/1
https://chenguangwu.github.io/tools/funeral/grave-design.html  # 2/1
https://chenguangwu.github.io/tools/sports/sports-schedule.html  # 2/1
https://chenguangwu.github.io/tools/agriculture/calc-4.html  # 2/0
https://chenguangwu.github.io/tools/agriculture/canopy-coverage.html  # 2/0
https://chenguangwu.github.io/tools/agriculture/estimate-yield-rate.html  # 2/0
https://chenguangwu.github.io/tools/ai/ai-6.html  # 2/0
https://chenguangwu.github.io/tools/ai/attention-head-dim.html  # 2/0
https://chenguangwu.github.io/tools/biz/superscript-text.html  # 2/0
https://chenguangwu.github.io/tools/biz/text-prefix-suffix.html  # 2/0
https://chenguangwu.github.io/tools/content/generator-33.html  # 2/0
https://chenguangwu.github.io/tools/design/color-picker.html  # 2/0
https://chenguangwu.github.io/tools/design/image-rounded-corners.html  # 2/0
https://chenguangwu.github.io/tools/design/image-to-ascii.html  # 2/0
https://chenguangwu.github.io/tools/design/pixel-art-generator.html  # 2/0
https://chenguangwu.github.io/tools/finance/profit-margin-calculator.html  # 2/0
https://chenguangwu.github.io/tools/fun/roulette-simulator.html  # 2/0
https://chenguangwu.github.io/tools/fun/word-scramble.html  # 2/0
https://chenguangwu.github.io/tools/general/detector-concentration.html  # 2/0
https://chenguangwu.github.io/tools/general/stats-energy.html  # 2/0
https://chenguangwu.github.io/tools/health/dysphagia-food-guide.html  # 2/0
https://chenguangwu.github.io/tools/health/one-rep-max.html  # 2/0
https://chenguangwu.github.io/tools/it/postgresql-cheatsheet.html  # 2/0
https://chenguangwu.github.io/tools/legal/feisu-ipo-simu-binggou-yewu.html  # 2/0
https://chenguangwu.github.io/tools/legal/statute-limitations.html  # 2/0
https://chenguangwu.github.io/tools/life/density-converter.html  # 2/0
https://chenguangwu.github.io/tools/life/volume-converter.html  # 2/0
https://chenguangwu.github.io/tools/marketing/marketing-ltv-calculator.html  # 2/0
https://chenguangwu.github.io/tools/math/geometry-calculator.html  # 2/0
https://chenguangwu.github.io/tools/music/web-tuner.html  # 2/0
https://chenguangwu.github.io/tools/nephrology/uacr.html  # 2/0
https://chenguangwu.github.io/tools/ophthalmology/corneal-curvature.html  # 2/0
https://chenguangwu.github.io/tools/science/barcode-pharmacode.html  # 2/0
https://chenguangwu.github.io/tools/science/nato-phonetic.html  # 2/0
```

## 每日操作日志

| 日期 | 检查/请求数量 | 已请求 | 已收录跳过 | 配额/错误 | 备注 |
|---|---:|---:|---:|---|---|
| 2026-09-04 | 6 | 5 | 0 | 已达每日配额 | Chrome；5 个行业首页请求成功；advertising 检查后因配额未提交，明日优先 |
