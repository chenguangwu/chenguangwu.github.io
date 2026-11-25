# Docker 运行命令转换丢失未知选项

## 问题
解析器对不支持的选项静默跳过且不识别其参数，例如 `docker run --network host nginx` 可能将 `host` 当镜像、`nginx` 当命令；无参数选项也可能被静默丢弃。

## 解决方案
支持常见选项及其参数形式，对无法解析的选项停止生成或清晰列出未转换内容，避免产出误导配置；测试带值和无值选项。

## 受影响工具路径
- `tools/it/docker-run-converter.html`
