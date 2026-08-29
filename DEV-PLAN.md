# DEV-PLAN

## GSC 优化（无数据方向）— 老板 8-29 22:38 批准启动
> 背景：技术 SEO 8-26 审计已 100% 覆盖零缺口；无数据可做的站内项已做完。
> 唯一真活 = 内容深度（打掉模板化页过滤 = 收录极低根因）+ 英文重复描述去重。

### ✅ 已完成（试点，commit 1e051b92）
- [GSC-A1] it/ 15 高频工具内容深度块（使用场景/示例/FAQ），`_build.py` step6 + `i18n/tools/content_deepdive.json`，幂等注入，四门禁全绿。
- [GSC-A2] 12 个同行业工具英文标题+描述去重（`_en_override.json` 写具体功能）。

### ⏳ 进行中（老板 8-29 已批"铺开"，同机制按行业分批）
- [GSC-A3] 内容深度铺开，已落地 9 行业共 214 页 deep-dive：
  - 试点 it/ 15（1e051b92）→ math/ 25 → design/ 22 → finance/ 22 → statistics/ 23 → science/ 23 → materials/ 28 → electromagnetism/ 28 → fluid/ 28（共 214 页）
  - 机制：`_build.py` step6 + `i18n/tools/content_deepdive.json`，幂等注入，四门禁每批全绿
  - 剩余候选：fluid/metrology/signal/investment/economics/process 等理工类，及 engineering/automotive/hydraulic/ai 等高质量行业
- [GSC-B] CTR 精修：等 GSC 查询 CSV（高展示低点击页定向改写 description）再动。

### 不做（已决策）
- 953 编号 URL / 104 basename 重复治理：SEO 风险>收益，8-24 已否决。
- 盲目全站 description 重写：8-24 否过的通用填充废话，禁止。
