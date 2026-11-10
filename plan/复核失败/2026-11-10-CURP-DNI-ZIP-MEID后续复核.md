# F-N202/F-N203、F-N204、F-N206、F-N208 复核失败

## F-N202/F-N203 CURP

世纪、日期和州码样例独立执行均符合移交结论：`GARW150820HMNERN58` 显示 1915；`BOXW100820HZZERNA6` 对州码 ZZ 判失败；`BOXW310230HMNERNA4` 日期无效。但非法输入未经转义插入 `innerHTML`，`<svg id=x onload=alert(1)>` 会在输出中生成 svg 节点；详见同批 CURP 安全记录。待修复并覆盖真实 DOM。

## F-N204 DNI

移交宣称 FAQ、例题均已更新，但当前 `tools/finance/dni-validator.html` 的 deep-dive 仍写 `12345678 mod 23 = 5` 和 24 字符表 `TRWAGMYFPDXBNJZSQVHLCKET`。独立计算 `12345678 % 23 = 14`，顶层常量及实际计算为正确 23 字符。`i18n/tools/content_deepdive.json` 和 `i18n/tools/en/finance/dni-validator.json` 亦有相同错误，需同时修正权威数据与英文映射，构建后复查存活；页面的非法输入注入见同批 DNI 安全记录。

## F-N206 MEID

`A0000012345678G` 已拒绝，连字符样例能解析。但非法字符路径将原始输入插入 `innerHTML`；JSDOM 独立执行输入 `<svg id=x onload=alert(1)>` 后 `#output svg` 存在并带事件属性。修复输出转义，并保留非法字符拒绝和分隔符回归。

## F-N208 ZIP

`00000`、`99999` 已拒绝，`10001` 和 `95014-1234` 可通过格式校验。但非法格式路径将原始输入插入 `innerHTML`；JSDOM 独立执行输入 `<svg id=x onload=alert(1)>` 后 `#output svg` 存在并带事件属性。修复输出转义并覆盖回归。范围守卫只能排除两端区间，范围内仍可能未分配，不应声称已证明地址存在。
