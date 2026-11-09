# 复核失败重做批次 · 申请再次复核

> 原条目：plan/复核失败/2026-11-09-第一批.md § SF-N95
> 修复批次：Batch 11（本地提交，攒满 5 批后统一构建/推送触发 CI 复核）
> 状态：已修复 + 回归用例 + 门禁实测通过

## 失败点（复核不通过原记录）
- 40 岁老将、体重 88 kg、抓举 140 kg、挺举 170 kg（总成绩 310 kg），目标体重仍选 88 kg。
- 页面显示等效总成绩 **320.1 kg**，而同年龄、同体重的等效值应精确还原为原成绩 **310 kg**。
- 根因：以「老将修正总成绩」为跨体重基数，逆运算只除目标体重端 Sinclair 系数，遗漏目标端年龄系数。

## 根因
跨体重等效的本意是同年龄、同 Sinclair 水平下的成绩换算。旧实现 `var baseVal=isMasters?mastersTotal:sinclairTotal;` 把「老将修正后的总成绩」当跨体重基数，导致逆运算在目标端只除 Sinclair 系数、遗漏目标端年龄系数；当目标体重 = 原体重时应精确还原 310.0 kg，却得到 320.1 kg。

## 修复位点
文件：`tools/sports/juzhongzongchengji-sinclair-xishu.html`（calc 段，约 line 302）
- 改为 `var baseVal=sinclairTotal;`（跨体重等效保持同等 Sinclair 水平、同年龄比较，以非老将的 Sinclair 总成绩为基数；老将修正只作用于当前体重展示，不进入跨体重基数）。
- equiv 提示行删除冗余的 `(isMasters?'老将修正 ':'' )+` 前缀，改为「若保持同等 Sinclair 水平（baseVal），等效总成绩 ≈ equiv kg」。

## 证据
- 源码落盘：`tools/sports/juzhongzongchengji-sinclair-xishu.html` 两处改动已写入。
- 回归用例（`scripts/verify_sports_calc.js`）新增：
  - slug `sports/juzhongzongchengji-sinclair-xishu`，inputs `{gender:"m", bw:"88", age:"40", snatch:"140", cj:"170", targetBw:"88"}` → expect `["等效总成绩 ≈ 310.0 kg"]`（旧实现得 320.1，现精确还原）。
- 判别力：注入失败（换默认值）时该用例 FAIL（见下）。

## 判别力实测
- `env -u NODE_OPTIONS node scripts/verify_sports_calc.js juzhongzongchengji-sinclair-xishu` → 通过。
- `env -u NODE_OPTIONS node scripts/discriminate_check.js verify_sports_calc.js` → 217/217 用例在注入失败时均变红（0 逃生项），含本页新增同年龄跨体重用例（目标=原体重与默认态可区分）。
- 整个 sports 分类 `verify_sports_calc.js` → **217/217 通过**。
