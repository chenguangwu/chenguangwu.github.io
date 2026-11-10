# F-N207、F-N212/F-N216、F-N213、F-N195/F-N196 复核失败

## F-N207 MEID

独立执行 14 位 `A0000012345679` 和 18 位 `045035996579124856`，确认缺校验位显示部分态，十六/十进制转换符合移交示例。但非法输入路径将 raw 直接作为 HTML 输出，`<svg id=x onload=alert(1)>` 生成 svg 节点，见 F-N206 退回记录，须一并修复。

## F-N212 / F-N216 ABA / 路由号

独立执行两页：全零/99 前缀已拒绝，`021000021` 通过；但 `021000021x` 字母被 `raw.replace(/\D/g,'')` 静默剥离，两页均显示号码有效。原始输入并非九位数字却获得肯定结论，须拒绝非法字符，仅明确允许的分隔符可去除，并对两页分别回归。

## F-N213 选民 ID

`ABC1234567` 已显示未核对州码的限定，但输入 `<svg id=x onload=alert(1)>` 触发非法长度分支时原文被解析为 HTML，独立 JSDOM 检测到 `#output svg`。须安全回显并保留中英文标注。

## F-N195 / F-N196 TFN

源码实现权重为末位 10，8 位样例已前补 0 并按 3-3-3 展示；但 `tools/finance/tfn-validator.html` FAQ 当前仍写末位 11，与本次移交声称不符；权威数据 `i18n/tools/content_deepdive.json` 和英文映射 `i18n/tools/en/finance/tfn-validator.json` 同样保留错误。另以 `100000001<svg id=x onload=alert(1)>` 触发校验可生成 `#output svg`。须修正权威数据及英文内容、构建后复核，并对用户输入安全回显。
