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

| https://chenguangwu.github.io/tools/agriculture/estimate-analysis.html | https://chenguangwu.github.io/tools/agriculture/canopy-coverage.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/edu/stats.html | https://chenguangwu.github.io/tools/edu/essay-word-counter.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/edu/ranking.html | https://chenguangwu.github.io/tools/edu2/exam-analysis.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/edu/wenbenquzhong-paixu-fanzhuan.html | https://chenguangwu.github.io/tools/it/text-dedupe-sort.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/cardiology/convert-rehab.html | https://chenguangwu.github.io/tools/cardiology/cardiac-rehab-mets.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/design/analysis.html | https://chenguangwu.github.io/tools/design/palette-extractor.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/design/generator-time-1.html | https://chenguangwu.github.io/tools/video/subtitle-tool.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/design/color-contrast-check.html | https://chenguangwu.github.io/tools/design/contrast-checker.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/electrical/voltage-capacity-battery.html | https://chenguangwu.github.io/tools/electrical/battery-bank.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/electrical/calc-power-capacitance.html | https://chenguangwu.github.io/tools/electrical/power-factor-compensation.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/rehabilitation/analysis-time.html | https://chenguangwu.github.io/tools/rehabilitation/gait-analysis.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/usedcar/estimate-14.html | https://chenguangwu.github.io/tools/usedcar/car-residual.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/pulmonology/analysis-14.html | https://chenguangwu.github.io/tools/pulmonology/tb-resistance.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/acupuncture/analysis-10.html | https://chenguangwu.github.io/tools/acupuncture/cupping-mark-analysis.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/property/area-shared.html | https://chenguangwu.github.io/tools/property/shared-area.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metallurgy/estimate-temp-time-1.html | https://chenguangwu.github.io/tools/metallurgy/decarburization.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/forensic-medicine/analysis-15.html | https://chenguangwu.github.io/tools/forensic-medicine/fall-injury.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/it/analysis-66.html | https://chenguangwu.github.io/tools/science/statistics-calculator.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/it/analysis-manager-1.html | https://chenguangwu.github.io/tools/science/statistics-calculator.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/science/yiyuanercifangchengqiujie.html | https://chenguangwu.github.io/tools/math/quadratic-solver.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/railway/noise-1.html | https://chenguangwu.github.io/tools/eco/noise-superposition.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/railway/qiaoliang-qiaodun-zhizuo-hezai.html | https://chenguangwu.github.io/tools/bridge/load-calc.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/railway/slope-4.html | https://chenguangwu.github.io/tools/road/grade-calc.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/analysis-4.html | https://chenguangwu.github.io/tools/fun/blood-type-personality.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/laugh-generator.html | https://chenguangwu.github.io/tools/fun/generator-laugh.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/convert-speed-stride.html | https://chenguangwu.github.io/tools/fitness/step-stride.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/caishuzi-1-100fanwei.html | https://chenguangwu.github.io/tools/fun/number-guess.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/sudoku-generator.html | https://chenguangwu.github.io/tools/fun/generator-2.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/maze-generator.html | https://chenguangwu.github.io/tools/fun/generator-3.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/analysis-tester-rhythm.html | https://chenguangwu.github.io/tools/fun/typing-rhythm.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fun/stats-blink.html | https://chenguangwu.github.io/tools/fun/blink-counter.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/food-testing/summary.html | https://chenguangwu.github.io/tools/food-testing/heavy-metal-migration.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/library/convert-ref-cite.html | https://chenguangwu.github.io/tools/library/citation-format.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/language/hanyuyanwenchaijie-yuanyin-fuyin.html | https://chenguangwu.github.io/tools/language/korean-hangul-decomposer.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/language/xibanyayuzhongyinweizhipanduan-neizhiguize.html | https://chenguangwu.github.io/tools/language/spanish-accent-rules.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/obstetrics/gonggao-fuweiyutaiertizhong-hadlock.html | https://chenguangwu.github.io/tools/obstetrics/fetal-weight-hadlock.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/baking/mold.html | https://chenguangwu.github.io/tools/baking/mold-volume.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/sports/tent-wind-rating.html | https://chenguangwu.github.io/tools/travel/zhangpengfangfengxishu.html | 2026-10-12 | 2026-11-12 | 待删 | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/sports/convert-13.html | https://chenguangwu.github.io/tools/sports/climbing-grade-converter.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/safety/stats-report-frequency.html | https://chenguangwu.github.io/tools/safety/accident-stats.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/optical/mobian-jianbian-pingbian-guige.html | https://chenguangwu.github.io/tools/optical/edge-bevel.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/pet/kouling-shoushichongfucishuyujiyiquxian.html | https://chenguangwu.github.io/tools/pet-training/command-repetition.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/clinical-lab/analysis-8.html | https://chenguangwu.github.io/tools/clinical-lab/blood-gas-analysis.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/clinical-lab/analysis-9.html | https://chenguangwu.github.io/tools/clinical-lab/electrophoresis-analysis.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/clinical-lab/analysis-density-2.html | https://chenguangwu.github.io/tools/clinical-lab/semen-analysis.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/hr/analysis-conversion-recruit.html | https://chenguangwu.github.io/tools/hr/recruitment-funnel.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/hr/stats-report-attendance.html | https://chenguangwu.github.io/tools/hr/attendance-stats.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/food-processing/estimate-analysis-1.html | https://chenguangwu.github.io/tools/food-processing/residual-oxygen.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/marketing/analysis-strength-market-share.html | https://chenguangwu.github.io/tools/marketing/market-share.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fitness/estimate-1.html | https://chenguangwu.github.io/tools/fitness/calc-4.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/fitness/carbon-ratio.html | https://chenguangwu.github.io/tools/fitness/macro-ratio.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/tcm-pharmacy/analysis-ratio-prescription.html | https://chenguangwu.github.io/tools/tcm-pharmacy/jun-chen-zuo-shi.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/ophthalmology/analysis-12.html | https://chenguangwu.github.io/tools/ophthalmology/visual-field-analysis.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metalwork/voltage-current.html | https://chenguangwu.github.io/tools/welding/speed-voltage-current.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metalwork/banjin-jianzhe-chongya-maohan-gongyi.html | https://chenguangwu.github.io/tools/metalwork/sheet-bend.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/metalwork/qiege-denglizi-huoyan-shuidao-canshu.html | https://chenguangwu.github.io/tools/electrical/speed-9.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/falvwenshuguanjiancizidongtiqu.html | https://chenguangwu.github.io/tools/legal2/keyword-extract.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/estimate-12.html | https://chenguangwu.github.io/tools/legal/labor-compensation.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/falv-yijian-han-beiwanglu-bianxie.html | https://chenguangwu.github.io/tools/legal/generator-17.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/legal/estimate-40.html | https://chenguangwu.github.io/tools/legal/work-injury-compensation.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/dentistry/length-3.html | https://chenguangwu.github.io/tools/dentistry/dental-arch-development.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/dentistry/analysis-11.html | https://chenguangwu.github.io/tools/dentistry/bridge-span.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/dentistry/kouqiangai-tnm-shaichagongju.html | https://chenguangwu.github.io/tools/dentistry/oral-cancer-screening.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/reproductive-medicine/stats-6.html | https://chenguangwu.github.io/tools/reproductive-medicine/ivf-statistics.html | 2026-09-19 | 2026-10-19 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/photo/capacity-fps.html | https://chenguangwu.github.io/tools/photo2/video-storage.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/surveying/distance-4.html | https://chenguangwu.github.io/tools/surveying/horizontal-from-slope.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/hematology/quetie-juyou-rongxue-shiyanshijianbie.html | https://chenguangwu.github.io/tools/hematology/anemia-differential.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/machinery/speed-cutting-feed.html | https://chenguangwu.github.io/tools/mechanical/cutting-speed.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |
| https://chenguangwu.github.io/tools/machinery/zaoyin-shengya-pinpu-jiangzao-yugu.html | https://chenguangwu.github.io/tools/eco/noise-addition.html | 2026-09-22 | 2026-10-22 | 待删（超期） | 2026-11-03 审计补登记；繁体同理 |

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
