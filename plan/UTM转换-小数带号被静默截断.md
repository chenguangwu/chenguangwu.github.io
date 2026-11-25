# UTM 转换：小数带号被静默截断

## 问题

逆转换使用 `parseInt` 解析带号，输入 32.9 时会静默作为 32 计算，生成的经纬度不对应用户输入。

## 解决方案

完整解析带号并验证为 1–60 的整数；对小数、空值和越界值给出提示，覆盖合法边界。

## 受影响工具路径

- `tools/science/latlon-utm-converter.html`
- `tools/science/astronomy-toolkit.html`
