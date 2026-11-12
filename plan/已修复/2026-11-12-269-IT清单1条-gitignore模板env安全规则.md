# 2026-11-12 · 第269批 · IT 清单 1 条（攒批第 9 批）

分类：`01-IT开发/it.md`
条目：IT-N270（高，安全承诺落空）

## 处理结果

### IT-N270 .env 安全规则落地（高）— 真改

- 问题：页面注意事项「机密文件（.env）务必忽略」、deep-dive 示例「选 Node → 输出 node_modules/、dist/、.env」，但 8 个模板 29 条规则无任何 `.env`（只有 `env/` 目录，语义完全不同）⇒ 用户以为密钥已被忽略，实际 `.env` 仍入库，安全承诺落空。
- 修复：8 个模板（py/node/go/rust/java/dotnet/c/ide）items 统一追加 `.env`、`.env.*`、`!.env.example`（最后一条取反保留样例文件）。选任一栈都会输出机密文件规则，示例承诺与实际一致。
- deep-dive 示例与英文 map 值本就声称输出 `.env`，改模板后即为真实，无需改文案。仅改页面内联 `<script>` 模板数据，不涉权威源/SEO。

## 验证证据

- JSDOM 新旧差分 `scripts/_verify_it_batch269.mjs`：新源码 **9/9**，旧源码（`/tmp/bk269`）**4/9**，5 个判别点。
  - 8 个模板逐一勾选各自断言 `.env`/`.env.*`/`!.env.example`（旧态 8 栈全缺）；Node 模板具体规则与示例承诺一致性；全选汇总仍含各栈代表规则。
- verify 新增 1 条强锁 `GIENV`（注入只勾 node，断言输出 .env 三件套）：全站 **1669/1669**、单分类 3/3；旧源码差分 2/3（新锁红、两条历史 py+go / rust+ide 回归绿）；判别力单文件版 1/1、零逃生。
  - 现有两条 gitignore 用例锚 `*.py[cod]` / `/vendor/` / `**/*.rs.bk` / `# IDE/编辑器` 等栈独有规则，追加 .env 不影响 ⇒ 保持绿。
- build 幂等：首次差异仅 sitemap 时间戳，第三次 build 稳定（`3fafa6e3bc…`）；`.env` 三件套 8 处保留；build 后 JSDOM 复验 9/9。`node --check` 两脚本 + 内联 JS 通过；`audit_verify_input_ids.js` 207 文件 / 10465 用例 / 31039 注入键，缺页 0、僵尸 0。

## 待复核要点

- 真机：勾选任一技术栈（尤其 Node）→ 生成结果应含 `.env`、`.env.*`、`!.env.example` 三行；部署时 `.env.example` 样例文件不被忽略（取反规则生效）。
- 真机：deep-dive 示例「选 Node → 输出 .env」与实际生成结果一致；原有各栈规则、历史/CSV 导出不受影响。
- 同页 N271（预设全选 8 项）、N272（历史/图表取截断文本）仍未做，留清单后续批次。
