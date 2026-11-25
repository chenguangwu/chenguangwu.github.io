# 代码运行器：未处理的 Promise 拒绝缺少控制台反馈

## 问题
运行环境通过 iframe 中的 `window.onerror` 转发同步异常，源码未见 `unhandledrejection` 监听。用户代码中未处理的 Promise 拒绝可能不出现在工具内控制台，容易误认为程序正常执行；需在浏览器中以 `Promise.reject(new Error('test'))` 复现并确认。

## 解决方案
监听并安全展示未处理的 Promise 拒绝原因，保持 iframe 隔离和输出转义；覆盖同步异常、异步拒绝与正常输出的浏览器验证。

## 受影响的工具路径
- `tools/it/code-runner.html`
