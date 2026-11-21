# 重定向存根待删登记（TOOLBOX-REDIRECT Stubs → 保留 1 个月后删除）

> 本文件是 `AGENTS.md` §4.6 规定的**统一登记处**。所有 `TOOLBOX-REDIRECT` 迁移存根（临时过渡，最长保留 **1 个月**）必须登记于此，到期由维护者**主动删除**，**不依赖定时任务**。
>
> 维护约定：
> - 新建重定向存根的同一批次 → 在此追加一行 + 同步 `--no-verify` 提死链（见 §4.6）。
> - 到「到期日」后 → 按底部「删除 SOP」主动处理，并把状态改为「已删（commit xxx）」。
> - 每条记录删完后**保留历史行**（标「已删」），便于审计，不要整行删除。

## 字段
| 字段 | 含义 |
|------|------|
| 源 URL | 旧地址（重定向存根，到期真正 404） |
| 目标 URL | 新地址（跳转目的地） |
| 建存根日期 | 写入 `TOOLBOX-REDIRECT` 的日期 |
| 到期日 | 建存根日期 + 1 个月，须物理删除 |
| 状态 | 待删 / 已删（注明删除 commit） |
| 备注 | 繁体 zh-tw 由 CI 自动消失等 |

## 待删清单

| 源 URL | 目标 URL | 建存根日期 | 到期日 | 状态 | 备注 |
|--------|----------|-----------|--------|------|------|
| https://chenguangwu.github.io/tools/pets/pet-age-convert.html | https://chenguangwu.github.io/tools/pet/pet-age-converter.html | 2026-10-10 | 2026-11-10 | 已删（ea0240209b） | 繁体 `zh-tw/tools/pets/pet-age-convert.html` 同规则，CI 自动消失 |
| https://chenguangwu.github.io/tools/pets/feeding-amount.html | https://chenguangwu.github.io/tools/pet/pet-feeding-calc.html | 2026-10-10 | 2026-11-10 | 已删（ea0240209b） | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/vaccine-reminder.html | https://chenguangwu.github.io/tools/pet/reminder-vaccine-deworming.html | 2026-10-10 | 2026-11-10 | 已删（ea0240209b） | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/grooming-guide.html | https://chenguangwu.github.io/tools/pet/grooming-guide.html | 2026-10-10 | 2026-11-10 | 已删（ea0240209b） | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/kennel-space.html | https://chenguangwu.github.io/tools/pet/kennel-space.html | 2026-10-10 | 2026-11-10 | 已删（ea0240209b） | 繁体同理 |
| https://chenguangwu.github.io/tools/pets/index.html | https://chenguangwu.github.io/tools/pet/index.html | 2026-10-10 | 2026-11-10 | 已删（ea0240209b） | 分类落地页存根；繁体同理 |
| https://chenguangwu.github.io/tools/music/frequency-3.html | https://chenguangwu.github.io/tools/music/instrument-tuning.html | 2026-10-12 | 2026-11-12 | 已删（本批次，含死链补录） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/insurance/calc-pv-1.html | https://chenguangwu.github.io/tools/realestate/pv.html | 2026-08-25 | 2026-09-25 | 已删（2026-11-03） | 2026-10-25 公式审计时发现漏登记；指南 15 处反链已改指新 URL；繁体由 CI 自动消失 |
| https://chenguangwu.github.io/tools/insurance/estimate-20.html | https://chenguangwu.github.io/tools/insurance/surrender-value.html | 2026-08-25 | 2026-09-25 | 已删（2026-11-03） | 同上 |
| https://chenguangwu.github.io/tools/insurance/stats-5.html | https://chenguangwu.github.io/tools/insurance/loss-ratio.html | 2026-08-25 | 2026-09-25 | 已删（2026-11-03） | 同上 |
| https://chenguangwu.github.io/tools/general/calculator-calc-11.html | https://chenguangwu.github.io/tools/math/complex-number.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc/unit-prefix.html | https://chenguangwu.github.io/tools/general/convert-22.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc/scientific-notation.html | https://chenguangwu.github.io/tools/general/convert-21.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc/statistics-distribution.html | https://chenguangwu.github.io/tools/general/calc-stats-1.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc/truth-table.html | https://chenguangwu.github.io/tools/general/generator-23.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc2/tax-refund.html | https://chenguangwu.github.io/tools/travel/estimate-15.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc2/cigarette-tar.html | https://chenguangwu.github.io/tools/health/convert-content.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/misc2/coin-grade.html | https://chenguangwu.github.io/tools/antiques/rater-1.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/niche/succulent-watering.html | https://chenguangwu.github.io/tools/gardening/reminder-cycle-succulent.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/niche/convert-fps.html | https://chenguangwu.github.io/tools/video/video-fps.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/niche/convert-sample.html | https://chenguangwu.github.io/tools/audio/audio-sample-rate.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/niche/recommender-temp-pottery.html | https://chenguangwu.github.io/tools/ceramics/ceramic-firing.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |
| https://chenguangwu.github.io/tools/niche/photography-exposure.html | https://chenguangwu.github.io/tools/photo/calc-exposure-aperture.html | 2026-10-12 | 2026-11-12 | 已删（839719048a） | 跨分类重复副本；繁体同理 |

| https://chenguangwu.github.io/tools/agriculture/estimate-analysis.html | https://chenguangwu.github.io/tools/agriculture/canopy-coverage.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/edu/stats.html | https://chenguangwu.github.io/tools/edu/essay-word-counter.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/edu/ranking.html | https://chenguangwu.github.io/tools/edu2/exam-analysis.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/edu/wenbenquzhong-paixu-fanzhuan.html | https://chenguangwu.github.io/tools/it/text-dedupe-sort.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/cardiology/convert-rehab.html | https://chenguangwu.github.io/tools/cardiology/cardiac-rehab-mets.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/design/analysis.html | https://chenguangwu.github.io/tools/design/palette-extractor.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/design/generator-time-1.html | https://chenguangwu.github.io/tools/video/subtitle-tool.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/design/color-contrast-check.html | https://chenguangwu.github.io/tools/design/contrast-checker.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/electrical/voltage-capacity-battery.html | https://chenguangwu.github.io/tools/electrical/battery-bank.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/electrical/calc-power-capacitance.html | https://chenguangwu.github.io/tools/electrical/power-factor-compensation.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/rehabilitation/analysis-time.html | https://chenguangwu.github.io/tools/rehabilitation/gait-analysis.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/usedcar/estimate-14.html | https://chenguangwu.github.io/tools/usedcar/car-residual.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/pulmonology/analysis-14.html | https://chenguangwu.github.io/tools/pulmonology/tb-resistance.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/acupuncture/analysis-10.html | https://chenguangwu.github.io/tools/acupuncture/cupping-mark-analysis.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/property/area-shared.html | https://chenguangwu.github.io/tools/property/shared-area.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metallurgy/estimate-temp-time-1.html | https://chenguangwu.github.io/tools/metallurgy/decarburization.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/forensic-medicine/analysis-15.html | https://chenguangwu.github.io/tools/forensic-medicine/fall-injury.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/it/analysis-66.html | https://chenguangwu.github.io/tools/science/statistics-calculator.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/it/analysis-manager-1.html | https://chenguangwu.github.io/tools/science/statistics-calculator.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/science/yiyuanercifangchengqiujie.html | https://chenguangwu.github.io/tools/math/quadratic-solver.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/railway/noise-1.html | https://chenguangwu.github.io/tools/eco/noise-superposition.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/railway/qiaoliang-qiaodun-zhizuo-hezai.html | https://chenguangwu.github.io/tools/bridge/load-calc.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/railway/slope-4.html | https://chenguangwu.github.io/tools/road/grade-calc.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/analysis-4.html | https://chenguangwu.github.io/tools/fun/blood-type-personality.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/laugh-generator.html | https://chenguangwu.github.io/tools/fun/generator-laugh.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/convert-speed-stride.html | https://chenguangwu.github.io/tools/fitness/step-stride.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/caishuzi-1-100fanwei.html | https://chenguangwu.github.io/tools/fun/number-guess.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/sudoku-generator.html | https://chenguangwu.github.io/tools/fun/generator-2.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/maze-generator.html | https://chenguangwu.github.io/tools/fun/generator-3.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/analysis-tester-rhythm.html | https://chenguangwu.github.io/tools/fun/typing-rhythm.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/stats-blink.html | https://chenguangwu.github.io/tools/fun/blink-counter.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/food-testing/summary.html | https://chenguangwu.github.io/tools/food-testing/heavy-metal-migration.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/library/convert-ref-cite.html | https://chenguangwu.github.io/tools/library/citation-format.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/language/hanyuyanwenchaijie-yuanyin-fuyin.html | https://chenguangwu.github.io/tools/language/korean-hangul-decomposer.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/language/xibanyayuzhongyinweizhipanduan-neizhiguize.html | https://chenguangwu.github.io/tools/language/spanish-accent-rules.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/obstetrics/gonggao-fuweiyutaiertizhong-hadlock.html | https://chenguangwu.github.io/tools/obstetrics/fetal-weight-hadlock.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/baking/mold.html | https://chenguangwu.github.io/tools/baking/mold-volume.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/sports/tent-wind-rating.html | https://chenguangwu.github.io/tools/travel/zhangpengfangfengxishu.html | 2026-10-12 | 2026-11-12 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/sports/convert-13.html | https://chenguangwu.github.io/tools/sports/climbing-grade-converter.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/safety/stats-report-frequency.html | https://chenguangwu.github.io/tools/safety/accident-stats.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/optical/mobian-jianbian-pingbian-guige.html | https://chenguangwu.github.io/tools/optical/edge-bevel.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/pet/kouling-shoushichongfucishuyujiyiquxian.html | https://chenguangwu.github.io/tools/pet-training/command-repetition.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/clinical-lab/analysis-8.html | https://chenguangwu.github.io/tools/clinical-lab/blood-gas-analysis.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/clinical-lab/analysis-9.html | https://chenguangwu.github.io/tools/clinical-lab/electrophoresis-analysis.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/clinical-lab/analysis-density-2.html | https://chenguangwu.github.io/tools/clinical-lab/semen-analysis.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/hr/analysis-conversion-recruit.html | https://chenguangwu.github.io/tools/hr/recruitment-funnel.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/hr/stats-report-attendance.html | https://chenguangwu.github.io/tools/hr/attendance-stats.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/food-processing/estimate-analysis-1.html | https://chenguangwu.github.io/tools/food-processing/residual-oxygen.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/marketing/analysis-strength-market-share.html | https://chenguangwu.github.io/tools/marketing/market-share.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fitness/estimate-1.html | https://chenguangwu.github.io/tools/fitness/calc-4.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fitness/carbon-ratio.html | https://chenguangwu.github.io/tools/fitness/macro-ratio.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/tcm-pharmacy/analysis-ratio-prescription.html | https://chenguangwu.github.io/tools/tcm-pharmacy/jun-chen-zuo-shi.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/ophthalmology/analysis-12.html | https://chenguangwu.github.io/tools/ophthalmology/visual-field-analysis.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metalwork/voltage-current.html | https://chenguangwu.github.io/tools/welding/speed-voltage-current.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metalwork/banjin-jianzhe-chongya-maohan-gongyi.html | https://chenguangwu.github.io/tools/metalwork/sheet-bend.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metalwork/qiege-denglizi-huoyan-shuidao-canshu.html | https://chenguangwu.github.io/tools/electrical/speed-9.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/falvwenshuguanjiancizidongtiqu.html | https://chenguangwu.github.io/tools/legal2/keyword-extract.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/estimate-12.html | https://chenguangwu.github.io/tools/legal/labor-compensation.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/falv-yijian-han-beiwanglu-bianxie.html | https://chenguangwu.github.io/tools/legal/generator-17.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/estimate-40.html | https://chenguangwu.github.io/tools/legal/work-injury-compensation.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/dentistry/length-3.html | https://chenguangwu.github.io/tools/dentistry/dental-arch-development.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/dentistry/analysis-11.html | https://chenguangwu.github.io/tools/dentistry/bridge-span.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/dentistry/kouqiangai-tnm-shaichagongju.html | https://chenguangwu.github.io/tools/dentistry/oral-cancer-screening.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/reproductive-medicine/stats-6.html | https://chenguangwu.github.io/tools/reproductive-medicine/ivf-statistics.html | 2026-09-19 | 2026-10-19 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/photo/capacity-fps.html | https://chenguangwu.github.io/tools/photo2/video-storage.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/surveying/distance-4.html | https://chenguangwu.github.io/tools/surveying/horizontal-from-slope.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/hematology/quetie-juyou-rongxue-shiyanshijianbie.html | https://chenguangwu.github.io/tools/hematology/anemia-differential.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/machinery/speed-cutting-feed.html | https://chenguangwu.github.io/tools/mechanical/cutting-speed.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/machinery/zaoyin-shengya-pinpu-jiangzao-yugu.html | https://chenguangwu.github.io/tools/eco/noise-addition.html | 2026-09-22 | 2026-10-22 | 已删（本批次） | 2026-11-03 审计补登记；繁体同理 |

## 删除 SOP（到期执行）
1. `cd /Users/cgw/project/cgw/chenguangwu.github.io`
2. 先 grep 全站（排除 `zh-tw/`、排除 `tools/pets/` 存根自身）所有指向待删源 URL 的内部链接（`href`/`src`），改写为目标 URL 或删除，避免删除后产生内部死链（`_audit_links.py` 门禁不过）。
3. `git rm tools/pets/<file>.html …`（删空目录由 git 处理）。
4. `zh-tw/` 是 CI 构建产物，删源后自动消失，无需手动删。
5. `python3 scripts/run_gates.py` → 确认 216 项全过（存根本就被 `_test_static` 跳过，删除不应破坏门禁）。
6. 旧 URL 已是真 404，用默认校验提死链：`python3 _submit_indexnow_deadlinks.py --file _deadlinks_2026-10-10_pets.txt`（脚本自动 HTTP 校验，只交已 404 的；**不要再 `--no-verify`**）。
7. `git add -A` → `commit`（说明「删除 pets 重定向存根，旧 URL 真正 404」）→ `push origin master`。
8. 单次查询 GitHub Actions 确认部署成功（不轮询）。
9. 回本文件把对应行状态改为「已删（commit xxx）」。

## 2026-11-16 校正：存量 29 个存根按真实建存根日期登记（均在保留期内）

> 来源：全站 `grep TOOLBOX-REDIRECT`（29 文件）。建存根日期取每个文件首次引入 `TOOLBOX-REDIRECT` 的提交作者日期，
> 逐文件执行 `git log --reverse --format='%ad %h' --date=short -S TOOLBOX-REDIRECT -- <文件>`，
> 29 个文件均为 2026-11-14（提交 `029cf0e035` 5 个、`d58e5d690f` 11 个、`760de4410b` 6 个、`34ec610b81` 6 个、`13bb26182e` 1 个），
> 非原页面入库日 2026-08-25。到期日按 +1 个月记 2026-12-14，当前状态「保留期内」。
> 到期后删除须按「删除 SOP」：全站内链改写 → 删文件 → `sitemap-deadlinks.xml` 登记 → 部署 success 后 `_submit_indexnow_deadlinks.py`。

| 源 URL | 目标 URL | 建存根日期 | 到期日 | 状态 | 备注 |
|---|---|---|---|---|---|
| https://chenguangwu.github.io/tools/acoustics/intensity-level.html | https://chenguangwu.github.io/tools/acoustics/sound-intensity-level.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/agriculture/calc-2.html | https://chenguangwu.github.io/tools/agriculture/calculator-calc-density.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/biz/text-compare.html | https://chenguangwu.github.io/tools/it/text-diff.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/design/generator-9.html | https://chenguangwu.github.io/tools/biz/barcode-generator.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/design/image-cropper.html | https://chenguangwu.github.io/tools/image/image-crop.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/design/image-resizer.html | https://chenguangwu.github.io/tools/image/image-resize.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/dynamics/inelastic-collision.html | https://chenguangwu.github.io/tools/dynamics/momentum-conservation.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/dynamics/period-pendulum.html | https://chenguangwu.github.io/tools/science/pendulum-period.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/economics/pv-annuity.html | https://chenguangwu.github.io/tools/insurance/annuity-present.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/edu/generator-4.html | https://chenguangwu.github.io/tools/it/summary-generator.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/energy/electrical-power.html | https://chenguangwu.github.io/tools/electromagnetism/electric-power.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/finance/password.html | https://chenguangwu.github.io/tools/life/generator-strength.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/finance/word-counter.html | https://chenguangwu.github.io/tools/text/stats-1.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/fitness/calculator-calc-constitution.html | https://chenguangwu.github.io/tools/healthcare/bmi-calculator.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/hr/overtime-pay-calc.html | https://chenguangwu.github.io/tools/legal/overtime-pay.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/investment/annuity-pv-inv.html | https://chenguangwu.github.io/tools/insurance/annuity-present.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/it/calc-2.html | https://chenguangwu.github.io/tools/life/base-convert.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/math/calc-1.html | https://chenguangwu.github.io/tools/life/percentage-calculator.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/mechanical/calc-1.html | https://chenguangwu.github.io/tools/machinery/calc-lifespan-belt.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/medical/calculator-calc-due-date.html | https://chenguangwu.github.io/tools/health/pregnancy-due-date.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/nuclear/specific-activity-from-halflife.html | https://chenguangwu.github.io/tools/nuclear/specific-activity.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/optical/rayleigh-resolution.html | https://chenguangwu.github.io/tools/optics/rayleigh-criterion.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/optical/snell-refraction.html | https://chenguangwu.github.io/tools/glass/snell-refraction.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/pet/pet-age-converter.html | https://chenguangwu.github.io/tools/pet/pet-age.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/realestate/calc-2.html | https://chenguangwu.github.io/tools/finance/rental-yield-calculator.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/safety/detector-strength.html | https://chenguangwu.github.io/tools/it/password-strength.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/science/factorial-calculator.html | https://chenguangwu.github.io/tools/math/factorial-calc.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/science/range-calculator.html | https://chenguangwu.github.io/tools/statistics/range-stat.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/statistics/variance-list.html | https://chenguangwu.github.io/tools/statistics/sample-variance.html | 2026-11-14 | 2026-12-14 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/cosmetic-derm/time-23.html | https://chenguangwu.github.io/tools/cosmetic-derm/post-procedure-recovery.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/cosmetic-derm/area-12.html | https://chenguangwu.github.io/tools/cosmetic-derm/telangiectasia-area.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/cosmetic-derm/maokongcudafenji.html | https://chenguangwu.github.io/tools/cosmetic-derm/pore-grading.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/cosmetic-derm/pifuphceding.html | https://chenguangwu.github.io/tools/cosmetic-derm/skin-ph.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/cosmetic-derm/formula-1.html | https://chenguangwu.github.io/tools/cosmetic-derm/meso-cocktail.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/cosmetic-derm/ratio-composition-injection.html | https://chenguangwu.github.io/tools/cosmetic-derm/mesotherapy.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/life/date-diff.html | https://chenguangwu.github.io/tools/life/date-difference-calculator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/sports/youyonghuashuixiaolv-swolf.html | https://chenguangwu.github.io/tools/sports/swimming-stroke-efficiency.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/psychiatry/lsas-social.html | https://chenguangwu.github.io/tools/psychiatry/rater-23.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/clinical-nursing/braden-score.html | https://chenguangwu.github.io/tools/clinical-nursing/calc-rater-risk.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/finance/calc-2.html | https://chenguangwu.github.io/tools/finance/irr-calculator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/dentistry/rater-risk-2.html | https://chenguangwu.github.io/tools/dentistry/caries-risk.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian.html | https://chenguangwu.github.io/tools/pediatrics/neonatal-jaundice.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/clinical-nursing/convert-flow-concentration.html | https://chenguangwu.github.io/tools/clinical-nursing/oxygen-concentration.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/hematology/pnh-flow.html | https://chenguangwu.github.io/tools/hematology/detector-5.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/finance/calc-3.html | https://chenguangwu.github.io/tools/finance/npv-calculator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/clinical-nursing/morse-score.html | https://chenguangwu.github.io/tools/clinical-nursing/assessor-rater-risk.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/clinical-nursing/generator-pressure.html | https://chenguangwu.github.io/tools/clinical-nursing/pressure-injury-description.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/hematology/generator-analysis.html | https://chenguangwu.github.io/tools/hematology/thrombin-generation.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/food-testing/generator-27.html | https://chenguangwu.github.io/tools/food-testing/colony-count.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/obstetrics/calc-risk.html | https://chenguangwu.github.io/tools/obstetrics/down-screening.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/tcm-pharmacy/calc-time-concentration.html | https://chenguangwu.github.io/tools/tcm-pharmacy/medicinal-wine.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/food-testing/convert-37.html | https://chenguangwu.github.io/tools/food-testing/protein-kjeldahl.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/fishery/calc-power.html | https://chenguangwu.github.io/tools/fishery/winter-heating.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/dentistry/assessor-5.html | https://chenguangwu.github.io/tools/dentistry/zirconia-aesthetics.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/clinical-nursing/surgical-position-risk.html | https://chenguangwu.github.io/tools/clinical-nursing/assessor-pressure-risk.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/hematology/mpn-scoring.html | https://chenguangwu.github.io/tools/hematology/rater-5.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/obstetrics/kupperman-score.html | https://chenguangwu.github.io/tools/obstetrics/rater-26.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/endocrinology/sex-hormone-cycle.html | https://chenguangwu.github.io/tools/endocrinology/cycle-hormone.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/agriculture/calc-7.html | https://chenguangwu.github.io/tools/agriculture/fertigation-ratio.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/hvac/kongtiaolengfuhejisuan.html | https://chenguangwu.github.io/tools/hvac/cooling-load.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/construction/calc-6.html | https://chenguangwu.github.io/tools/construction/window-shading.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/optical/aspheric-design.html | https://chenguangwu.github.io/tools/optical/calc-47.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/pulmonology/calc-48.html | https://chenguangwu.github.io/tools/pulmonology/oxygenation-index.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/rheumatology/assessor-10.html | https://chenguangwu.github.io/tools/rheumatology/essdai.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/rheumatology/rater-16.html | https://chenguangwu.github.io/tools/rheumatology/sledai.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/neurology/twstrs.html | https://chenguangwu.github.io/tools/neurology/rater-21.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/psychiatry/cdrisc-resilience.html | https://chenguangwu.github.io/tools/psychiatry/rater-24.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/psychiatry/asrs-adhd.html | https://chenguangwu.github.io/tools/psychiatry/self-assess-4.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/pulmonology/feigongneng-fev1-fvc-fenji.html | https://chenguangwu.github.io/tools/pulmonology/pulmonary-function.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/obstetrics/placenta-grading.html | https://chenguangwu.github.io/tools/obstetrics/taipanchengshudu-grannumfenji.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/ophthalmology/osdi-scale.html | https://chenguangwu.github.io/tools/ophthalmology/self-assess-2.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/rehabilitation/berg-balance-scale.html | https://chenguangwu.github.io/tools/rehabilitation/tester-rater.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/gastroenterology/hp-resistance.html | https://chenguangwu.github.io/tools/gastroenterology/detector-7.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/urology/iief5-score.html | https://chenguangwu.github.io/tools/urology/rater-4.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/neurology/rater-19.html | https://chenguangwu.github.io/tools/neurology/updrs.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/nephrology/aki-kdigo.html | https://chenguangwu.github.io/tools/nephrology/jixingshensunshang-kdigo-fenqi.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/rheumatology/detector-8.html | https://chenguangwu.github.io/tools/rheumatology/lupus-anticoagulant.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/finance/salary-after-tax.html | https://chenguangwu.github.io/tools/finance/salary-calculator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/automotive/tire-wear.html | https://chenguangwu.github.io/tools/automotive/estimate-wear-tire.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/it/regex-common.html | https://chenguangwu.github.io/tools/it/regex-cheatsheet.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/automotive/oil-change-countdown.html | https://chenguangwu.github.io/tools/automotive/countdown-engine-oil.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/automotive/maintenance-schedule.html | https://chenguangwu.github.io/tools/automotive/scheduler-cycle-maintenance.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/fishery/feed-rate-calculator.html | https://chenguangwu.github.io/tools/fishery/feeding-rate.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/agriculture/convert-content-1.html | https://chenguangwu.github.io/tools/agriculture/dry-matter-conversion.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/eco/noise-addition.html | https://chenguangwu.github.io/tools/eco/noise-superposition.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/design/shadow-generator.html | https://chenguangwu.github.io/tools/design/css-box-shadow-generator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/it/html-entity-encoder.html | https://chenguangwu.github.io/tools/it/html-entities-encode.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/it/whitespace.html | https://chenguangwu.github.io/tools/it/text-cleaner.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/it/calc-3.html | https://chenguangwu.github.io/tools/it/color-converter.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/ai/token.html | https://chenguangwu.github.io/tools/ai/token-usage.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/elderly/medication-schedule.html | https://chenguangwu.github.io/tools/elderly/reminder-time.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/acoustics/spl-add.html | https://chenguangwu.github.io/tools/acoustics/combine-two-spl.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/acoustics/decibel-power.html | https://chenguangwu.github.io/tools/acoustics/decibel-power-ratio.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/tools/acoustics/decibel-voltage.html | https://chenguangwu.github.io/tools/acoustics/decibel-voltage-ratio.html | 2026-11-21 | 2026-12-21 | 保留期内 | 简体+繁体各 1 页 |
| https://chenguangwu.github.io/guides/convert-content-1-guide.html | https://chenguangwu.github.io/guides/dry-matter-conversion-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至dry-matter-conversion 使用指南 |
| https://chenguangwu.github.io/guides/generator-4-guide.html | https://chenguangwu.github.io/tools/edu/summary-generator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至摘要生成器工具页 |
| https://chenguangwu.github.io/guides/variance-list-guide.html | https://chenguangwu.github.io/guides/sample-variance-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至sample-variance 使用指南 |
| https://chenguangwu.github.io/guides/period-pendulum-guide.html | https://chenguangwu.github.io/guides/pendulum-period-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至pendulum-period 使用指南 |
| https://chenguangwu.github.io/guides/annuity-pv-inv-guide.html | https://chenguangwu.github.io/guides/annuity-present-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至annuity-present 使用指南 |
| https://chenguangwu.github.io/guides/twstrs-guide.html | https://chenguangwu.github.io/guides/rater-21-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至rater-21 使用指南 |
| https://chenguangwu.github.io/guides/rater-19-guide.html | https://chenguangwu.github.io/guides/updrs-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至updrs 使用指南 |
| https://chenguangwu.github.io/guides/sex-hormone-cycle-guide.html | https://chenguangwu.github.io/guides/cycle-hormone-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至cycle-hormone 使用指南 |
| https://chenguangwu.github.io/guides/feigongneng-fev1-fvc-fenji-guide.html | https://chenguangwu.github.io/guides/pulmonary-function-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至pulmonary-function 使用指南 |
| https://chenguangwu.github.io/guides/calc-48-guide.html | https://chenguangwu.github.io/guides/oxygenation-index-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至oxygenation-index 使用指南 |
| https://chenguangwu.github.io/guides/intensity-level-guide.html | https://chenguangwu.github.io/tools/acoustics/sound-intensity-level.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至声强级（L_I = 10·log₁₀(I / I₀)）工具页 |
| https://chenguangwu.github.io/guides/decibel-voltage-guide.html | https://chenguangwu.github.io/tools/acoustics/decibel-voltage-ratio.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至电压分贝（L = 20·log₁₀(V / V₀)）工具页 |
| https://chenguangwu.github.io/guides/decibel-power-guide.html | https://chenguangwu.github.io/tools/acoustics/decibel-power-ratio.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至功率分贝（L = 10·log₁₀(P / P₀)）工具页 |
| https://chenguangwu.github.io/guides/spl-add-guide.html | https://chenguangwu.github.io/tools/acoustics/combine-two-spl.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至两声压级叠加（L = 10·log₁₀(10^(L₁/10)+10^(L₂/10))）工具页 |
| https://chenguangwu.github.io/guides/calc-power-guide.html | https://chenguangwu.github.io/guides/winter-heating-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至winter-heating 使用指南 |
| https://chenguangwu.github.io/guides/medication-schedule-guide.html | https://chenguangwu.github.io/tools/elderly/reminder-time.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至用药提醒表工具页 |
| https://chenguangwu.github.io/guides/factorial-calculator-guide.html | https://chenguangwu.github.io/guides/factorial-calc-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至factorial-calc 使用指南 |
| https://chenguangwu.github.io/guides/kongtiaolengfuhejisuan-guide.html | https://chenguangwu.github.io/guides/cooling-load-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至cooling-load 使用指南 |
| https://chenguangwu.github.io/guides/convert-37-guide.html | https://chenguangwu.github.io/guides/protein-kjeldahl-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至protein-kjeldahl 使用指南 |
| https://chenguangwu.github.io/guides/generator-27-guide.html | https://chenguangwu.github.io/guides/colony-count-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至colony-count 使用指南 |
| https://chenguangwu.github.io/guides/kupperman-score-guide.html | https://chenguangwu.github.io/guides/rater-26-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至rater-26 使用指南 |
| https://chenguangwu.github.io/guides/placenta-grading-guide.html | https://chenguangwu.github.io/guides/taipanchengshudu-grannumfenji-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至taipanchengshudu-grannumfenji 使用指南 |
| https://chenguangwu.github.io/guides/calc-risk-guide.html | https://chenguangwu.github.io/guides/down-screening-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至down-screening 使用指南 |
| https://chenguangwu.github.io/guides/noise-addition-guide.html | https://chenguangwu.github.io/guides/noise-superposition-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至noise-superposition 使用指南 |
| https://chenguangwu.github.io/guides/detector-strength-guide.html | https://chenguangwu.github.io/tools/safety/password-strength.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至密码强度检测工具页 |
| https://chenguangwu.github.io/guides/aspheric-design-guide.html | https://chenguangwu.github.io/guides/calc-47-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至calc-47 使用指南 |
| https://chenguangwu.github.io/guides/pet-age-converter-guide.html | https://chenguangwu.github.io/guides/pet-age-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至pet-age 使用指南 |
| https://chenguangwu.github.io/guides/token-guide.html | https://chenguangwu.github.io/guides/token-usage-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至token-usage 使用指南 |
| https://chenguangwu.github.io/guides/calculator-calc-due-date-guide.html | https://chenguangwu.github.io/guides/pregnancy-due-date-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至pregnancy-due-date 使用指南 |
| https://chenguangwu.github.io/guides/overtime-pay-calc-guide.html | https://chenguangwu.github.io/guides/overtime-pay-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至overtime-pay 使用指南 |
| https://chenguangwu.github.io/guides/pv-annuity-guide.html | https://chenguangwu.github.io/guides/annuity-present-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至annuity-present 使用指南 |
| https://chenguangwu.github.io/guides/salary-after-tax-guide.html | https://chenguangwu.github.io/tools/finance/salary-calculator.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至工资税后计算器工具页 |
| https://chenguangwu.github.io/guides/calculator-calc-constitution-guide.html | https://chenguangwu.github.io/guides/bmi-calculator-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至bmi-calculator 使用指南 |
| https://chenguangwu.github.io/guides/osdi-scale-guide.html | https://chenguangwu.github.io/guides/self-assess-2-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至self-assess-2 使用指南 |
| https://chenguangwu.github.io/guides/morse-score-guide.html | https://chenguangwu.github.io/guides/assessor-rater-risk-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至assessor-rater-risk 使用指南 |
| https://chenguangwu.github.io/guides/surgical-position-risk-guide.html | https://chenguangwu.github.io/guides/assessor-pressure-risk-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至assessor-pressure-risk 使用指南 |
| https://chenguangwu.github.io/guides/braden-score-guide.html | https://chenguangwu.github.io/guides/calc-rater-risk-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至calc-rater-risk 使用指南 |
| https://chenguangwu.github.io/guides/generator-pressure-guide.html | https://chenguangwu.github.io/guides/pressure-injury-description-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至pressure-injury-description 使用指南 |
| https://chenguangwu.github.io/guides/convert-flow-concentration-guide.html | https://chenguangwu.github.io/guides/oxygen-concentration-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至oxygen-concentration 使用指南 |
| https://chenguangwu.github.io/guides/assessor-5-guide.html | https://chenguangwu.github.io/guides/zirconia-aesthetics-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至zirconia-aesthetics 使用指南 |
| https://chenguangwu.github.io/guides/rater-risk-2-guide.html | https://chenguangwu.github.io/guides/caries-risk-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至caries-risk 使用指南 |
| https://chenguangwu.github.io/guides/formula-1-guide.html | https://chenguangwu.github.io/guides/meso-cocktail-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至meso-cocktail 使用指南 |
| https://chenguangwu.github.io/guides/maokongcudafenji-guide.html | https://chenguangwu.github.io/guides/pore-grading-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至pore-grading 使用指南 |
| https://chenguangwu.github.io/guides/pifuphceding-guide.html | https://chenguangwu.github.io/tools/cosmetic-derm/skin-ph.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至皮肤pH测定工具页 |
| https://chenguangwu.github.io/guides/ratio-composition-injection-guide.html | https://chenguangwu.github.io/tools/cosmetic-derm/mesotherapy.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至水光针配比计算工具页 |
| https://chenguangwu.github.io/guides/time-23-guide.html | https://chenguangwu.github.io/guides/post-procedure-recovery-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至post-procedure-recovery 使用指南 |
| https://chenguangwu.github.io/guides/area-12-guide.html | https://chenguangwu.github.io/guides/telangiectasia-area-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至telangiectasia-area 使用指南 |
| https://chenguangwu.github.io/guides/mpn-scoring-guide.html | https://chenguangwu.github.io/guides/rater-5-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至rater-5 使用指南 |
| https://chenguangwu.github.io/guides/pnh-flow-guide.html | https://chenguangwu.github.io/guides/detector-5-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至detector-5 使用指南 |
| https://chenguangwu.github.io/guides/generator-analysis-guide.html | https://chenguangwu.github.io/guides/thrombin-generation-guide.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至thrombin-generation 使用指南 |
| https://chenguangwu.github.io/guides/calc-7-guide.html | https://chenguangwu.github.io/tools/agriculture/fertigation-ratio.html | 2026-11-21 | 2026-12-21 | 保留期内 | 指南重定向至水肥配比工具页 |
