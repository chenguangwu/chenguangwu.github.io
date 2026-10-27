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

