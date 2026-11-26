# JS 压缩：非 LF 换行丢失自动分号语义

- 受影响工具路径：`tools/it/js-formatter.html`

## 问题描述

压缩器识别空白后只在其中包含 LF 时保留换行，单独的 CR、U+2028 和 U+2029 虽是 JavaScript 行终止符，却可能被压成普通空格。源码推导，`function f(){return\r1}` 原函数返回 `undefined`，压缩后可能变为返回 1；语法检查无法发现行为变化。已有行注释任务关注注释吞掉后续代码，此处无需注释即可触发。

## 解决方案

识别全部 ECMAScript 行终止符并保留自动分号插入所需边界；比较压缩前后执行结果，覆盖 return、yield、后缀运算和 CRLF。
