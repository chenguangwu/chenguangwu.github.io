# 2026-11-14-400 IT · whitespace 描述模板重复

## 复核失败原文（交接单第四节，2026-11-04 快照）
- `tools/it/whitespace.html`：曾被记「压成一行」选项缺失，审计后疑似已修，先核验再决定。

## 核验
- 「压成一行（换行变空格）」`#top_onespace` 已存在且接入 `calcTool()`，功能可用，原条目滞后。
- 同页发现真实缺陷：`meta description` / `og:description` / `twitter:description` / WebApplication JSON-LD 为
  「文本空白清理工具是一款免费的在线IT 开发工具，文本空白清理工具是一款免费的在线IT 开发工具，……纯前端运行、数据不上传、无需注册，打开浏览器即可使用。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。」
  同一句模板重复两遍，超过 120 字被截断，属套话堆叠。

## 根因
`i18n/tools/it.json` 的 `whitespace` 只有 `en-US`，缺 `zh-CN.intro`。构建取不到中文简介时回退读取页面旧 description（本身已重复），再套模板，形成二次堆叠。

## 修复
- 在 `i18n/tools/it.json` 补 `zh-CN`（h1/title/intro/desc），intro 覆盖实际功能：去首尾空白、删空行、合并连续空格、末尾单换行、压成一行，纯前端本地处理。
- intro 长度 ≥70 字符，避免构建再补模板前缀；重建后四类描述一致且无重复。

## 验证
- [x] `python3 _build.py` 通过
- [x] `meta description` / `og` / `twitter` / JSON-LD 四者一致，均无「是一款免费的在线IT 开发工具」前缀
- [x] JSON-LD 可被 `json.loads` 解析
- [x] zh-tw 派生页随构建重建

## 同批核验（无需改动）
- `tools/rehabilitation/fim-scale.html`、`tools/life/assessor-target.html` 的 `opt-guide` / `opt-faq` 已是页面专属内容（FIM 18 项口径、选址六项权重），非套话。
- `tools/life/assessor-target.html` 的 `shopArea` 有真实参与评分（40–120㎡ 区间计分），非死输入。

## 销账
- 交接单第四节 whitespace 条目已闭环。
