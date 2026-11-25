# Dockerfile 启动命令被当成单个可执行文件

## 问题
默认启动命令 `npm start` 被生成为 `CMD ["npm start"]`。Docker exec 格式会将整个字符串当作可执行文件名，容器启动时无法按预期运行 npm。

## 解决方案
明确命令输入格式，正确生成参数数组或有意使用 shell 形式，处理引号和转义；使用带参数的默认命令验证生成结果。

## 受影响工具路径
- `tools/it/dockerfile-generator.html`
