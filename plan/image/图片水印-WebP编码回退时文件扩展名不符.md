# 图片水印：WebP 编码回退时文件扩展名不符

- 受影响工具：`tools/image/image-watermark.html`
- 问题：导出按用户选择固定使用 `.webp` 文件名和成功提示，没有检查返回 Blob 的实际 MIME。若浏览器不支持 WebP 编码而将 `canvas.toBlob` 回退为 PNG，文件内容和扩展名会不一致。基于 API 回退行为及源码的兼容性风险，需在不支持 WebP 编码的环境或受控桩中复核。
- 解决方案：检查 Blob 的实际 MIME，按实际格式设置扩展名和提示；如果无法确认格式则明确报告失败，不误称 WebP。覆盖正常 WebP、PNG 回退和空 Blob。
