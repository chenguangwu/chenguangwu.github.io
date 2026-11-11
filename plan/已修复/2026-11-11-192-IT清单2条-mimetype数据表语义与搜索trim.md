# 2026-11-11 第192批 · IT-N107/N108 MIME 类型速查表：数据表语义 + 搜索 trim

## 清单项
- **IT-N107**：「数据表」与「导出明细 CSV」实际是搜索历史而非 MIME 清单，首屏导出静默无反应（中，功能语义错误）
- **IT-N108**：搜索词不 trim，前导空格导致 0 条（低，粘贴误判）

## 根因
- `__mime_typeRender()` 把 `TBKit.history.list()` 的时间/search/结果写进 `#mime_typeTable`，而历史已有独立 `#mime_typeHist` 页签；导出直接导这张历史表。首屏 `init()` 在 render 包装前执行、不产生历史，导出遇空表 `return false` 且无提示，表现像坏按钮。
- `render()` 中 `q = value.toLowerCase()` 未 trim，粘贴带来的行首/行尾空格使过滤全部落空。

## 改动
`tools/it/mime-type.html`：
1. 新增 `__mime_typeDataTable()`：把完整 `MIME`（84 条）渲染为「扩展名 / MIME 类型 / 分类」三列表（英文态表头与分类走内置双语映射），在 `__mime_typeBoot()`（DOMContentLoaded）中初始化；
2. `__mime_typeRender()` 删除写 `#mime_typeTable` 的历史表分支（历史仍 `mount` 到 `#mime_typeHist`、diff/chart 路径不变）；
3. `__mime_typeExport()` 改为：先重建 MIME 数据表 → 导出 `#mime_typeTable` 为 `mime-type.csv`；TBKit 未就绪或 MIME 为空时经 `__mime_typeToast()` 给中英双语提示（不再静默）；
4. `render()` 的搜索词改为 `(value||'').trim().toLowerCase()`；「工作原理与说明」公式串同步改为「先 trim 再转小写」。

`i18n/tools/en/it/mime-type.json`：对应公式串的中文键与英译同步更新为 trim 口径。

`scripts/verify_it_calc.js` 新增 4 条强锁：两侧空格搜索命中 2 条、数据表三列 84 行首行锚、导出调用序列 TAB→EXP、历史渲染不写数据表（`n=0|` 显式标记防前缀逃生）。

## 验证证据
- **真机** `scripts/_verify_it_batch192.mjs`（JSDOM，TBKit 全桩含 matrix.table 真实写 DOM）：**22/22**——数据表表头/84 行/首行/DOM tr、表内无历史列、前导/尾随/两侧空格均命中 2 条、空结果归零与恢复、导出前重建表且导出目标正确、历史渲染不写数据表且仍挂载 `#mime_typeHist`、空 MIME 导出无文件且有「暂无可导出的数据」提示、数据恢复、英文态表头/分类英译、英译说明含 trim。
  **旧源码 6/22**（页面取 `/tmp/mime-type.N107N108.before.html`，英译取 `git show HEAD:...`）——差分成立。
- **verify 用例级旧源码差分**：修好版 **1534/1534**；临时换入旧源码后 **1530/1534**，4 条新锁全红；恢复后页面 MD5 与修好版一致（`fb34346916677d498f8839aee64834b1`）。全程 `/tmp` 备份往返，未用 `git checkout --`。
- audit 注入键 **30841**、用例 10330、僵尸 id 0；单文件判别力正确变红 1532/1533，唯一逃生 `it/vector-magnitude` 为既有基线、跳过 1 为既有；i18n `--check` 0 残留、`--roundtrip` 0 不一致。

## 备注
- **踩坑**：本页 verify harness 未注入全局 `TBKit`，3 条 clicks 探针初版直接 `TBKit is not defined`；按既有做法在 clicks 开头自建 `globalThis.TBKit` 桩（util/chart/matrix/history/preset）后通过。
- **口径同步**：「先 trim 再转小写」同时改了页面公式串、en JSON 中文键与英译值；下一批完整门禁的 build 会验证 formula-eq 是否被权威源覆盖（若被覆盖需改权威源重做）。
- **IT-N109（个别 MIME 映射过时/分类不当）仍未处理**：涉及 IANA 注册值核实与 `.ai`/`.m3u8` 归类判断，本批未动，留清单。
- 只本地提交、不 push。
