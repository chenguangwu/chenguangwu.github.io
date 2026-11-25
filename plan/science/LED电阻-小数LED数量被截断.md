# LED 电阻：小数 LED 数量被截断

## 问题

LED 数量使用 `parseInt` 读取且未校验整数，输入 1.9 会按 1 只计算并生成电阻结果，改变输入而没有提示。

## 解决方案

完整解析数量并验证为 1–50 范围内的整数；对小数、空值和越界值明确提示。

## 受影响工具路径

- `tools/science/led-resistor-calculator.html`
