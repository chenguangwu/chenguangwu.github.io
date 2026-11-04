# 遗留未提交改动处置记录

> 2026-11-04 集成线处置：长期处于「他人未提交改动」的 5 个僵尸页面。
> 判定口径：改动语义完整且与页面实现一致 → 收编提交；与当前实现/口径矛盾或构成夸大承诺 → 丢弃并在此存档摘要。

## 已收编（提交入库）

| 路径 | 改动摘要 |
| --- | --- |
| `tools/hr/hris-zizhuyuaiduibijisuanqi.html` | icon 👥→⚖️；title/og/twitter 描述后缀统一为「输出综合差距」；`title-en` 从占位 `Hris Zizhuyuaiduibijisuanqi` 改为真实英文名；FAQ 补 term-link。语义完整、与实现一致。 |
| `tools/hr/social-insurance.html` | icon 💰→👥（与上条 ⚖️ 交换，避免图标撞车）；h2 与按钮 emoji 同步。语义完整。 |

## 已丢弃（`git checkout --`）

| 路径 | 改动摘要 | 丢弃理由 |
| --- | --- | --- |
| `tools/hr/attendance-stats.html` | 深解示例把「出勤率 95.5%，因有迟到 → 评级封顶良好」改成「出勤率 95.5%（优秀）」。 | **与页面实现直接矛盾**。页面 L295-297 明确：有迟到/早退/旷工/请假任一记录者不得评「优秀」，封顶良好。该改动会让示例与计算结果自相矛盾。 |
| `tools/hr/calc-81.html` | 两段精确算例简化为「10 人成功、基数 500、系数 1.2 → 6000 元」；FAQ 由「按一次性计发口径测算，不做自动滚动统计」改为「工具可按过保人数滚动统计」。 | **与页面实现矛盾**。页面 L694 口径为「激励按岗位系数一次性计发」，无滚动统计实现；FAQ 改为滚动统计属虚构功能。 |
| `tools/marketing/email-subject-line-tester.html` | description / og:description / twitter:description / JSON-LD description 四处删掉「（启发式评分，非真实打开率预测）」，改为「帮助提升邮件打开率与送达率」。 | **夸大承诺 / 与实现冲突**。页面为前端启发式评分，无法预测真实打开率与送达率；删除免责声明会误导用户且违反内容真实性口径。 |

## 备注

- 三条丢弃只针对上述明确路径，未批量回退任何其它文件。
- 商业/HR 线与假工具线可于下一批直接接手这 5 页。

## 2026-11-04 追加：`tools/manufacturing/quality-control.html`

- 改动摘要：仅把 `</div><h3>❓ 常见问题（FAQ）</h3>` 拆成两行，纯空白/换行变化，无任何文案或逻辑改动（diff 1 增 1 删）。
- mtime 19:22，非活跃写入。
- 处置：**存档后丢弃**（`git checkout --`）。土建线可正常接手该页。
- 21:26 该页再次出现同类拆行改动（mtime 21:26，非秒级活跃），语义不变 ⇒ **收编提交** `2f0dc614fa`（message：收编遗留改动：tools/manufacturing/quality-control.html）。

## 2026-11-04 追加：IT 6 文件复核（IT 线报的 ast-viewer / charset-detector / index / less-compiler / whitespace / yaml-validator）

- 实际脏路径仅 3 个（其余 3 个已由安全线/假工具线提交，工作区干净）：
  - **收编**：`tools/it/index.html` —— MD5 卡片标题「MD5加密工具」→「MD5 哈希计算器」，与假工具线 `af986271e5` 的页面标题口径一致，1 行、语义完整。
  - **丢弃**：`tools/it/charset-detector.html` —— 新文案宣称「识别 GBK/Big5/UTF-8 编码」并给 `C4E3BAC3` 十六进制字节示例，但页面实现只做「已解码字符串的乱码还原」，原 FAQ 明确「不做 GBK/Big5 猜测」；改动属**与实现相反**的虚构功能描述。
  - **丢弃**：`tools/it/whitespace.html` —— 示例/FAQ 把选项名写成「压缩所有连续空白」「删除行首尾空白」，页面实际 label 是「合并连续空格为单个」「去除每行首尾空白」，**口径与 UI 不一致**；示例也删掉了勾选项与输出对应关系。
- 处置仅针对上述明确路径，未批量回退。

