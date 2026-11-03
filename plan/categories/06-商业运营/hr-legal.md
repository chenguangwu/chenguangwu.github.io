# 人力/法务 · tools/{hr,legal,legal2}（~60 页）

## 已知问题
### L2. 遗留：labor-compensation FAQ（满半年按 1 年）vs 代码（N=0.5）口径分歧——待裁断改 FAQ 或代码。
- 受影响：tools/legal/labor-compensation.html

## 功能缺陷
- 个税/年终奖在 finance；HR 侧缺「offer 对比器」（base/期权/年终并排）。
- 法务缺「诉讼费+保全费+律师费合计预算表」整合页。

## 优化点
- S2 场景：「N+1 赔偿金速算」「竞业补偿金」。
- S7 引据：劳动合同法条号标注。→ ✅ 已落地 10 页（2026-10-27 批27）：hr/annual-leave-prorate + social-insurance + comp-time-calculator、legal/labor-compensation(-n1) + double-wage-no-contract + severance-pay + overtime-pay + work-injury-compensation、legal2/compensation-n1；每页 tool-notes 前插 id="legalRefBox" 卡（条号 ASCII 可见 + data-zh 中文，EN 零 CJK）。L2 口径分歧未动（仅加引据不改逻辑）。余：hr/annual-leave-calc、hr/overtime-pay-calc、legal/estimate-12 三页无 tool-notes 锚点待补锚；民法典系页（抚养/继承/遗嘱/消费/人身损害等）待续批。

## 受影响范围
- tools/hr/、tools/legal/、tools/legal2/（~60 页）

## 进度
- 🟡 进行中（S7 引据批27-30 已落地 36 页覆盖 legal 公式页；L2 待裁断勿动；S2 场景待续）

## 2026-11-03 第一轮抽样补充

### 年假半天取整与本页 FAQ 自相矛盾（高，确认页面口径冲突）
- 问题与证据：`tools/hr/annual-leave-prorate.html:177-181,255-276` 输出按半天向下取整，FAQ 称不足整天通常不折算。2026-07-01 入职、5 年工龄、2026-12-31 截止，原函数给精确约 2.52 天、折算 2.5 天。
- 影响：`tools/hr/annual-leave-prorate.html`，用户无法判断具体口径；本次只确认页内矛盾，不独立裁定具体案件的法定天数。
- 方案：请专业人士核对适用规则，区分法定及企业自定义口径并统一公式、FAQ 与示例；可本地保存并清除日期、工龄和口径以供复核。

### 自定义零利率被代为 6%（高，确认函数缺陷）
- 问题与证据：`tools/legal/late-payment-interest.html:297-325` 使用 `parseFloat(customRate)||6`；本金 100000、2026-01-01 至 12-31、自定义 0%，原函数显示 6% 和利息 5983.56 元。
- 影响：`tools/legal/late-payment-interest.html`，零利率模拟结果错误。
- 方案：区分空值、非法值和有效数字零；LPR 同类回退亦需检查。可让用户主动保存、删除本地计算案例并标明手工利率与计算期间，不宣称实时利率。

### 覆盖
- 本次仅抽查上述 2 页，使用原函数内存 DOM 桩；法律依据、真实浏览器和其余页面未验证。

