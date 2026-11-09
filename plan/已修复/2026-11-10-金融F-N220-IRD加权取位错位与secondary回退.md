# F-N220 IRD 校验页：加权取位整体错一位、无 secondary 权重回退

## 来源
- `plan/categories/02-金融财务/finance.md` F-N220（高，确认源码缺陷）。
- 修复方本批真修（分类清单线）。

## 根因
- `tools/finance/ird-validator.html` 的 `irdCheck()`：补 9 位后取 `base = d.substring(1,9)`（丢首位、把校验位算进加权），官方口径是「8 位补前导 0 成 9 位，前 8 位作 base，第 9 位为校验位」。
- 定义了 `IRD_WEIGHTS` 的 secondary 行 `[7,4,3,2,5,2,7,6]` 却固定 `weightSet=0`；primary 算出校验位 10（不可作校验位）时应回退 secondary，从不使用。
- 公式框写「mod 11 = 0」「9 位版前置补 0」与官方「check=(11−sum mod 11) mod 11、必要时 secondary」相反。
- 默认预填 `490918503` 本身是非法号（页面算法错位却判 ✅）。

## 修复位点
- `irdCheck()`：`base = d.substring(0,8)`、`checkDigit = parseInt(d[8])`；抽 `expectedWith(w)`；primary 得 `c===10` 时改用 secondary 重算，仍 `c===10` 返回 false。
- 公式框改为正确口径（含 secondary 回退）；`validate()` 的「校验算法」文案同步补 secondary 说明。
- 默认预填 `490918503` → `490918507`（node 实算 base 49091850、Σ=136、rem=4、校验位 7，合法号），修正「默认样例本身错误」。

## 验证（轻量四件套）
- `node scripts/verify_finance_calc.js`：419/419 PASS。
- `node scripts/discriminate_check.js verify_finance_calc.js`：已检 419，全部注入失败变红，逃生项 0。
- `node scripts/audit_verify_input_ids.js`：僵尸 id 0、缺页 0。
- 判别力实测（备份→`git show HEAD` 换旧源码→跑→恢复）：旧源码 417/419（两条新用例变红），恢复后 419/419。
- 算法实算：`49091850` 旧❌新✅、`490918503` 旧✅新❌、`10000009` 旧❌新✅、`10000019` 旧✅新❌，与清单复现完全一致。

## verify 用例变更
- 新增 2 条（带输入号+校验算法+结论的连续串，跨「格式化/长度/校验算法/校验和」）：`49091850` → ✅有效；`10000019` → ❌无效。
- 收紧 1 条：`123456789` 原 expect「校验和失败」在修复过程中因默认态一度变非法而命中成逃生项，改锁「输入： 123456789 格式化： 123-456-789 长度： 9 位」。
- **踩坑**：默认值改合法号后，「✅ 有效」类结论串在默认态也命中（默认就是合法号），故合法/非法两条新用例的 expect 必须带输入号与格式化串形成连续串，不能只锁结论。改默认值前须确认无其它用例依赖旧默认串（已 grep 确认）。

## 待复核提示
- 真机打开 `tools/finance/ird-validator.html`：默认 `490918507` 应 ✅；`49091850`/`10000009` ✅；`490918503`/`10000019` ❌；公式框口径已与官方一致。
