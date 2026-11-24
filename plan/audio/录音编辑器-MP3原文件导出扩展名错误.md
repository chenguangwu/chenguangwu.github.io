# 录音编辑器：MP3 原文件导出扩展名错误

- 受影响工具：`tools/audio/audio-recorder.html`
- 问题：原文件导出通过 MIME 判断扩展名，但 MP3 的常见 MIME 为 `audio/mpeg`，当前只匹配包含 `mp3` 的类型，导致此类文件被下载为 `.bin`，用户和播放器难以识别。源码可确认，需使用实际 MP3 文件浏览器复核。
- 解决方案：支持 `audio/mpeg` 等常见 MIME 映射，原始文件优先保留安全的原扩展名，无法识别时明确提示；覆盖 MP3、WAV、WebM 及 MIME 为空的文件。
