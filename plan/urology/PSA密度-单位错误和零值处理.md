# PSA 密度：单位错误和零值处理

- 受影响工具：`tools/urology/psa-density.html`
- 问题：计算为 PSA（ng/mL）除以前列腺体积（mL），结果单位却显示 `ng/mL²`，未表达体积维度；输入 PSA 为 0 被判无效，不能展示零值计算，年龄通过 `parseInt` 静默截断。风险标签“低危/中危/高危”即使附有解释，也容易被误解为总体肿瘤风险。
- 解决方案：统一使用明确的 `ng/mL/cc` 或等价单位；对有效零值和年龄精度进行明确校验；将标签改为密度区间，并在结果中保留不能单独判断总体风险及活检的提示。参考 [EAU 前列腺癌诊断评估](https://uroweb.org/guidelines/prostate-cancer/chapter/diagnostic-evaluation)。
- 验证建议：输入 PSA 6 ng/mL、体积 40 mL 应显示 0.150 ng/mL/cc；再测试 PSA 0、空值及小数年龄。
