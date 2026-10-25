# 人力/法务 · tools/{hr,legal,legal2}（~60 页）

## 已知问题
### L2. 遗留：labor-compensation FAQ（满半年按 1 年）vs 代码（N=0.5）口径分歧——待裁断改 FAQ 或代码。
- 受影响：tools/legal/labor-compensation.html

## 功能缺陷
- 个税/年终奖在 finance；HR 侧缺「offer 对比器」（base/期权/年终并排）。
- 法务缺「诉讼费+保全费+律师费合计预算表」整合页。

## 优化点
- S2 场景：「N+1 赔偿金速算」「竞业补偿金」。
- S7 引据：劳动合同法条号标注。

## 受影响范围
- tools/hr/、tools/legal/、tools/legal2/（~60 页）

## 进度
- 🔴 待开发（L2 小改）

### L3. hr/annual-leave-prorate 折算取整与自身文档/法规口径三方矛盾（批20）
- 描述：代码 `rounded = days<0.5?0:Math.ceil(days)`（3.99→4 天、8.36→9 天），但页面 deep-dive 例题写「3.99 → 实得 3.5 天」「8.36 → 取整 8 天」，FAQ 又称条例口径「折算后不足 1 整天部分不享受」（floor）。ceil 同时违背自身例题与法规默认，会多给用户年假。
- 方案：统一为法定 `Math.floor(days)`（或按 FAQ 半天粒度 `Math.floor(days*2)/2`），并同步修正例题 1（3.99→3.5）使文档与代码一致；深度解读同步（G03）。
- 受影响：tools/hr/annual-leave-prorate.html
- 置信度：高
