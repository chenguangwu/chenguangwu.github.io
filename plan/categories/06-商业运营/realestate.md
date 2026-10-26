# 房地产/物业 · tools/{realestate,property,rental}（~80 页）

## 已知问题
## 功能缺陷
- 购房页缺「首付比例/税费/中介费合计一口价」整合（和 finance 联动）。
- 租金页缺「租售比/回本年限」联动输出。

## 优化点
- ✅ S2 场景（2026-10-26）：down-payment 加 3 预设「一线首套 500万」（30%/30年）「二套改善 800万」（50%/25年）「刚需小户型 150万」（30%/30年），labelEn 双语；商住 LOFT 税费待税费页续批。verify realestate 232→235、判别器 0 逃生、门禁 218/218。
- ✅ S3 分步（2026-10-26）：down-payment 加「📊 逐年摊还明细」表（renderAmort：等额本息/等额本金逐月复算、按年汇总年还本金/利息/年末剩余本金，__T 双语）；verify realestate 235→236、判别器 0 逃生。

## 受影响范围
- tools/realestate/（54）、tools/property/、tools/rental/（~80 页）

## 进度
- 🟡 续批中（S2 首付场景、S3 摊还表已落地；剩余：LOFT 税费场景 / 购房一口价整合 / 租售比联动）
