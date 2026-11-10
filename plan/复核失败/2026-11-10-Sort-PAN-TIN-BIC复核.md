# F-N197/F-N198、F-N199/F-N200、F-N190–192、F-N187 复核失败

独立 JSDOM 执行各页真实业务脚本验证：

## Sort Code F-N197/F-N198

`12A34B56` 已被拒绝、`12-34-56` 可通过；但 `abc` 仍显示「等待输入」，因为按提取后的数字判空先于非法字符守卫，与含字母提示格式错误的承诺不符。输入 `1<svg id=x onload=alert(1)>` 错误路径生成 `#output svg`。须先区分原始空值和非空非法字符，安全回显。

## PAN F-N199/F-N200

`ABCZS1234E` 被拒绝，`ABCPS1234E` 可通过且末位标注无算术校验位。但页面 deep-dive 示例仍为 `ABCPD1234E`、仍称末位「校验字母」，与移交的三处统一和无校验说明不符；非法输入 `<svg id=x onload=alert(1)>` 会生成 `#output svg`。应核对深度内容数据源和英文映射，构建后确认，并安全回显。

## TIN F-N190–192

`12-3456789` 被识别为 EIN、公式框已有三分支；但 `abc` 显示「等待输入」而不是非法字符错误；`1<svg id=x onload=alert(1)>` 经非法字符分支产生 `#output svg`。须按原始输入判空并安全回显。

## BIC F-N187

`ABCDEFGH` 因 EF 非 ISO 码被拒、`DEUTPTFF` 被接受；但任意非 BIC 形态输入被送入反向行名查询并原样写入 HTML；`<svg id=x onload=alert(1)>` 可生成 `#output svg`。须安全渲染输入并覆盖反向查询错误路径。
