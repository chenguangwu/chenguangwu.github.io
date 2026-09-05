# 结果解读·逐工具深度增强任务清单（竞品取长补短·阶段六）


> 范围：**750 目标页内** `inputs<3` 且**有结果容器**的可解读短板页，共 **122** 个（输入数 0:11 / 1:45 / 2:66）。
> 做法：逐工具在结果容器旁注入可见「📊 结果解读」模块（`<section class="opt-result-interpret">`），文案**基于该页自身计算/评估逻辑**撰写——结果含义、单位、适用边界、注意事项；不编造超出工具算法的领域断言，医学/心理量表类加「结果仅供参考，不替代专业诊断」免责。
> 验证：每批实机无头 Chrome 打开，确认无 JS 报错、模块渲染正常、主功能无回归；`run_gates.py --skip-build` 4/4、`_test_static.py` 0 失败。
> 规则：完成一个勾掉一个；本地提交、不推送；每批合并一次提交。

> 提交历史：见 git log（本地领先 origin/master，未推送）。

## 批次 1（18 个）

- [ ] #1 `tools/clinical-nursing/pain-nrs.html` — 疼痛数字评分 (NRS) 与表情对照器（输入0）
- [ ] #2 `tools/edu/capital-quiz.html` — 首都测验（输入0）
- [ ] #3 `tools/edu/math-quiz.html` — 数学测验（输入0）
- [ ] #4 `tools/fun/coin-flip.html` — 抛硬币（输入0）
- [ ] #5 `tools/fun/color-guess.html` — 猜颜色（输入0）
- [ ] #6 `tools/fun/color-memory.html` — 颜色记忆（Simon）（输入0）
- [ ] #7 `tools/fun/pattern-memory.html` — 图案记忆（输入0）
- [x] #8 `tools/it/keycode-info.html` — 按键码 Keycode 查询（输入0）
- [ ] #9 `tools/psychiatry/isi-insomnia.html` — 睡眠(ISI)失眠严重度评估器（输入0）
- [ ] #10 `tools/psychiatry/phq9-depression.html` — 抑郁(PHQ-9)量表评估器（输入0）
- [ ] #11 `tools/tcm-diagnosis/disease-nature.html` — 病性辨析器（六淫）（输入0）
- [x] #12 `tools/acoustics/intensity-level.html` — 由声强求声强级（I₀=10⁻¹² W/m²）（输入1）
- [x] #13 `tools/acoustics/sound-intensity-level.html` — 声强级（L_I = 10·log₁₀(I / I₀)）（输入1）
- [x] #14 `tools/astronomy/atmospheric-refraction.html` — 折射量（R = 1.02 / tan(h + 10.3/(h+5.11)) ′）（输入1）
- [x] #15 `tools/astronomy/moon-illumination.html` — 照明比例（k = (1 − cos(2π·D/29.53)) / 2）（输入1）
- [ ] #16 `tools/biz/markdown-quote.html` — Markdown 引用转换器（输入1）
- [x] #17 `tools/chemistry/poh-to-ph.html` — 由 [OH⁻] 求 pOH 与 pH（输入1）
- [ ] #18 `tools/chinese-cook/cutting-sizes.html` — 切配尺寸对照（输入1）

## 批次 2（18 个）

- [ ] #19 `tools/chinese-cook/ingredient-substitute.html` — 食材替代查询（输入1）
- [ ] #20 `tools/chinese-cook/oil-temp.html` — 油温烹饪指南（输入1）
- [ ] #21 `tools/data/chart-generator.html` — 图表生成器（输入1）
- [ ] #22 `tools/finance/credit-card-bin.html` — 信用卡 BIN 查询（输入1）
- [ ] #23 `tools/finance/iccid-validator.html` — ICCID 验证（SIM 卡号）（输入1）
- [ ] #24 `tools/finance/ird-validator.html` — 新西兰 IRD 验证（输入1）
- [ ] #25 `tools/finance/license-key-validator.html` — 许可证密钥验证（输入1）
- [ ] #26 `tools/finance/pan-validator.html` — 印度 PAN 卡验证（输入1）
- [ ] #27 `tools/finance/tax-bracket.html` — 税率档次速查（输入1）
- [ ] #28 `tools/fun/keyboard-heatmap.html` — 键盘热力图（输入1）
- [ ] #29 `tools/fun/roulette-simulator.html` — 轮盘模拟器（输入1）
- [ ] #30 `tools/gardening/pot-capacity.html` — 花盆容量计算（输入1）
- [ ] #31 `tools/it/html-nesting-checker.html` — HTML 嵌套检查器（输入1）
- [ ] #32 `tools/it/pdf-signature-checker.html` — PDF 签名检查（输入1）
- [ ] #33 `tools/it/text-statistics.html` — 文本统计分析（输入1）
- [ ] #34 `tools/language/grammar-checker.html` — 语法检查（输入1）
- [ ] #35 `tools/language/spanish-accent-rules.html` — 西班牙语重音位置判断（输入1）
- [x] #36 `tools/math/circular-permutation.html` — 由元素个数求环形排列数（输入1）

## 批次 3（18 个）

- [ ] #37 `tools/math/factorial-calc.html` — 阶乘计算器（输入1）
- [x] #38 `tools/meteorology/isa-temperature.html` — 温度（输入1）
- [x] #39 `tools/misc/truth-table.html` — 逻辑真值表生成器（输入1）
- [ ] #40 `tools/neurology/calc-1.html` — NIHSS 脑卒中评分（输入1）
- [ ] #41 `tools/ophthalmology/osdi-scale.html` — 干眼症(OSDI)自评量表（输入1）
- [ ] #42 `tools/quantum/angular-momentum-quant.html` — 由主量子数求角动量（输入1）
- [ ] #43 `tools/quantum/mass-energy-equivalence.html` — 质能等价计算器（输入1）
- [ ] #44 `tools/rehabilitation/fim-scale.html` — 康复结局(FIM)量表总分计算器（输入1）
- [ ] #45 `tools/science/barcode-pharmacode.html` — Pharmacode 条形码（输入1）
- [ ] #46 `tools/science/median-calculator.html` — 中位数计算器（输入1）
- [ ] #47 `tools/science/nato-phonetic.html` — NATO 音标字母（输入1）
- [ ] #48 `tools/science/phone-qr.html` — 电话二维码（输入1）
- [ ] #49 `tools/science/physics-calculator.html` — 物理计算器（输入1）
- [ ] #50 `tools/signal/first-order-rise.html` — 上升时间（t_r ≈ 2.2·τ）（输入1）
- [ ] #51 `tools/statistics/mean-absolute-deviation.html` — 由数值序列求平均绝对偏差（输入1）
- [ ] #52 `tools/statistics/sample-variance.html` — 样本方差计算器（输入1）
- [ ] #53 `tools/structural/section-modulus-circle.html` — 由直径求圆截面抗弯模量（输入1）
- [ ] #54 `tools/tcm-diagnosis/meridian-differentiation.html` — 经络辨证疼痛对应器（输入1）

## 批次 4（18 个）

- [ ] #55 `tools/urology/iief5-score.html` — 勃起功能(IIEF-5)评分器（输入1）
- [ ] #56 `tools/yi/yi-divination.html` — 周易占卜（输入1）
- [ ] #57 `tools/accounting/debt-service-coverage.html` — 由经营现金流与债务偿付额求保障倍数（输入2）
- [ ] #58 `tools/ballistics/caliber-conversion.html` — 口径换算器（输入2）
- [ ] #59 `tools/banking/fisher-real-rate.html` — 费雪实际利率计算器（输入2）
- [ ] #60 `tools/biz/superscript-text.html` — 上标文字（输入2）
- [ ] #61 `tools/blasting/delay-blasting.html` — 微差延迟优化器（输入2）
- [ ] #62 `tools/cardiology/statin-dose.html` — 他汀(降脂幅度)剂量换算器（输入2）
- [ ] #63 `tools/chemistry/molality.html` — 质量摩尔浓度（b = n / m_溶剂）（输入2）
- [ ] #64 `tools/data/csv-analyzer.html` — CSV 分析器（输入2）
- [ ] #65 `tools/design/rem-to-px.html` — Rem to Px Converter（输入2）
- [ ] #66 `tools/economics/inflation-rate.html` — 通货膨胀率计算器（输入2）
- [ ] #67 `tools/electromagnetism/energy-inductor.html` — 由电感与电流求储能（输入2）
- [ ] #68 `tools/electromagnetism/magnetic-flux.html` — 磁通（Φ = B·A）（输入2）
- [ ] #69 `tools/encode/binary-to-ascii.html` — Binary / Hex to ASCII（输入2）
- [ ] #70 `tools/endocrinology/calc-1.html` — HOMA-IR 胰岛素抵抗指数（输入2）
- [ ] #71 `tools/energy/air-purifier-area.html` — 空气净化器适用面积计算（输入2）
- [ ] #72 `tools/energy/electrical-power.html` — 由电压与电流求电功率（输入2）

## 批次 5（18 个）

- [ ] #73 `tools/energy/joule-heating.html` — 由电流与电阻求热功率（输入2）
- [ ] #74 `tools/futures/option-payoff.html` — 期权盈亏图（输入2）
- [ ] #75 `tools/geometry/pyramid-volume.html` — 由底面积与高求棱锥体积（输入2）
- [ ] #76 `tools/it/bip39-generator.html` — BIP39 助记词生成器（输入2）
- [ ] #77 `tools/it/calc-1.html` — 文件大小单位换算（输入2）
- [ ] #78 `tools/it/calc-4.html` — CSS单位换算（px / em / rem / pt / %）（输入2）
- [ ] #79 `tools/it/mac-generator.html` — MAC Address Generator（输入2）
- [ ] #80 `tools/it/numeronym-generator.html` — Numeronym 数字缩写（输入2）
- [ ] #81 `tools/it/phone-parser.html` — Phone Number Parser &amp; Formatter（输入2）
- [ ] #82 `tools/kinematics/angular-accel.html` — 角加速度计算器（输入2）
- [ ] #83 `tools/kinematics/height-fall-distance.html` — 由下落时间求下落距离（输入2）
- [ ] #84 `tools/kinematics/relative-velocity-1d.html` — 由两物体速度求相对速度（输入2）
- [ ] #85 `tools/life/concentration-converter.html` — 浓度换算器（输入2）
- [ ] #86 `tools/life/density-converter.html` — 密度换算器（输入2）
- [ ] #87 `tools/life/length-converter.html` — 长度换算器（输入2）
- [ ] #88 `tools/life/magnet-converter.html` — 磁场强度换算器（输入2）
- [ ] #89 `tools/life/radiation-converter.html` — 辐射剂量换算器（输入2）
- [ ] #90 `tools/life/volume-converter.html` — 体积换算器（输入2）

## 批次 6（18 个）

- [ ] #91 `tools/materials/bulk-modulus.html` — 体积模量（K = E / (3(1−2ν))）（输入2）
- [ ] #92 `tools/materials/hooke-strain.html` — 轴向应变（ε = σ / E）（输入2）
- [ ] #93 `tools/math/gcd-lcm.html` — GCD / LCM 计算器（输入2）
- [ ] #94 `tools/math/log-base.html` — 任意底数对数计算器（输入2）
- [ ] #95 `tools/medical2/medical-abbrev.html` — 医学术语缩写（输入2）
- [ ] #96 `tools/meteorology/wet-bulb-temperature.html` — 湿球温度 T_w（输入2）
- [ ] #97 `tools/nuclear/activity-from-halflife.html` — 由半衰期与原子核数求活度（输入2）
- [ ] #98 `tools/nuclear/effective-halflife.html` — 由物理与生物半衰期求有效半衰期（输入2）
- [ ] #99 `tools/ophthalmology/visual-acuity-converter.html` — 视力表(Snellen/logMAR)换算器（输入2）
- [ ] #100 `tools/optical/blue-light-filter.html` — 防蓝光透射比计算器（输入2）
- [ ] #101 `tools/optics/angular-magnification.html` — 由明视距离与焦距求简单放大镜角放大率（输入2）
- [ ] #102 `tools/optics/resolving-power.html` — 由孔径与波长求圆形孔径分辨本领（输入2）
- [ ] #103 `tools/quantum/fermi-energy-3d.html` — 由自由电子密度求费米能（输入2）
- [ ] #104 `tools/quantum/thermal-de-broglie.html` — 由温度与质量求热德布罗意波长（输入2）
- [ ] #105 `tools/reproductive-medicine/anti-sperm-antibody.html` — 抗精子抗体 MAR 结果器（输入2）
- [ ] #106 `tools/reproductive-medicine/liquefaction-time.html` — 精液液化时间判定器（输入2）
- [ ] #107 `tools/reproductive-medicine/semen-volume.html` — 精液量评估器（输入2）
- [ ] #108 `tools/reproductive-medicine/sperm-dfi.html` — 精子 DNA 碎片(DFI)指数评估器（输入2）

## 批次 7（14 个）

- [ ] #109 `tools/reproductive-medicine/sperm-morphology.html` — 精子形态分类器（严格标准）（输入2）
- [ ] #110 `tools/reproductive-medicine/total-sperm-count.html` — 总精子数计算器（输入2）
- [ ] #111 `tools/robotics/end-effector-reach.html` — 二连杆工作空间计算器（输入2）
- [ ] #112 `tools/science/newtons-second.html` — 牛顿第二定律 F = ma（输入2）
- [ ] #113 `tools/signal/pwm-average.html` — 平均电压（V_avg = D · V_cc）（输入2）
- [ ] #114 `tools/signal/rc-time-constant.html` — 时间常数（τ = R·C）（输入2）
- [ ] #115 `tools/statistics/linear-regression.html` — 最小二乘回归计算器（输入2）
- [ ] #116 `tools/surveying/external-distance-curve.html` — 由半径与转角求外距（输入2）
- [ ] #117 `tools/tax/reverse-charge.html` — 由代扣金额与征收率求代扣代缴税额（输入2）
- [ ] #118 `tools/tax/vat-output.html` — 由销售额与增值税率求销项税额（输入2）
- [ ] #119 `tools/textile2/dye-temp.html` — 染色温度对照表（输入2）
- [ ] #120 `tools/urology/calc-1.html` — IPSS 前列腺症状评分（输入2）
- [ ] #121 `tools/urology/ipss-score.html` — IPSS评分(国际前列腺症状)自动计算器（输入2）
- [ ] #122 `tools/wedding/countdown-timeline.html` — 婚礼倒计时（输入2）