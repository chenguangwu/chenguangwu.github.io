# Basic 认证生成器：无法生成空密码凭据

## 问题

输入用户名 `admin` 并将密码清空时，`generate()` 的 `!user || !pass` 判断会清空输出并提示必须填写密码；但 `admin:` 是可表示的 Basic 凭据，部分接口和调试场景需要空密码。页面因此无法生成相应的 `Authorization: Basic YWRtaW46`。

## 解决方案

允许用户明确选择使用空密码，并区分尚未填写与有意使用空密码；说明服务端仍可能拒绝该凭据。验证空密码、普通密码、密码含冒号及用户名含非法冒号时生成或提示是否正确。

## 受影响工具路径

- `tools/it/basic-auth-generator.html`（`generate` 和凭据输入区）
