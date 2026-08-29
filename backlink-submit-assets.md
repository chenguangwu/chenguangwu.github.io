# 外链提交直达链接 + 媒体素材规格清单

> 用途：配合 `backlink-plan.md`（作战手册）与 `backlink-submit-copy.md`（复制即用文案），
> 把「去哪提交」「提交时填什么」「图要做多大」一次性说清。
> 本文件为人工运营手册，**不进 `scripts/gen_backlink_plan.py` 生成范围**，重跑脚本不会被覆盖。

---

## 一、AlternativeTo：逐竞品关联直达

### 机制（先搞懂，少走弯路）
AlternativeTo 的外链是这样来的：**在竞品的产品页点 "Add alternative"，填入 ToolBox 官网**，
审核通过后，ToolBox 就出现在该竞品的 "Alternatives" 列表里，且为 **DoFollow** 外链。
注意：是「去竞品页添加 ToolBox」，不是「在 ToolBox 页添加竞品」。

### 第 1 步：先让 ToolBox 本体被收录
- 提交入口：`https://alternativeto.net/submit/`
- 字段：`Software URL` 填 `https://chenguangwu.github.io`
- 提交后系统分配产品 slug（形如 `alternativeto.net/software/<slug>/`），**slug 以站内实际为准**，下方为构造模板，不要当成确定链接。

### 第 2 步：去头部竞品页添加 ToolBox
操作路径（通用，适用于每个竞品）：
1. 在 AlternativeTo 搜索框搜竞品名（如 `it-tools`）→ 进其产品页
2. 产品页右侧/底部点 **"Add alternative"**
3. 填 `https://chenguangwu.github.io`，提交等待审核

#### 头部竞品官网清单（决定"关联到谁"）
下表取自 `backlink-targets.csv` 中已匹配真实竞品的头部工具，按权重优先排序。
带 `★` 的是流量最大、最该先做的。

| 优先级 | 竞品官网 | 关联到的 ToolBox 工具（示例） | 为什么值得做 |
|--------|----------|------------------------------|--------------|
| ★ | `https://it-tools.tech` | 全站聚合（JSON/编解码/正则/Cron 等） | 最直接竞品，Dr 高、搜索量大 |
| ★ | `https://toolfk.com` | 全站聚合 | 同类聚合站，用户高度重合 |
| ★ | `https://smallpdf.com` | PDF 压缩/合并/转换类 | PDF 类搜索量极大 |
| `https://www.jsonformatter.org` | JSON 格式化/校验 | JSON 高频词 |
| `https://www.base64decode.org` | Base64 编解码 | Base64 超高搜索量 |
| `https://crontab.guru` | Cron 表达式 | 开发者强需求 |
| `https://jwt.io` | JWT 编解码/校验 | 开发者强需求 |
| `https://www.passwordgenerator.net` | 密码生成器 | 通用词 |
| `https://www.uuidgenerator.net` | UUID 生成器 | 开发者常用 |
| `https://regex101.com` | 正则测试 | 开发者强需求 |
| `https://www.pdfescape.com` | PDF 编辑 | PDF 类 |
| `https://www.iloveimg.com` | 图片格式转换 | 图片类高频 |
| `https://tinypng.com` | 图片压缩 | 图片类高频 |
| `https://www.unitconverters.net` | 单位换算 | 通用词 |
| `https://www.timeanddate.com` | 时区/日期计算 | 通用词 |

> 长尾工具（CSV 中标记为「行业资源页」的 4715 个）不走 AlternativeTo，改走「资源页投稿」（见 `backlink-plan.md` 第 8 节）。

### 第 3 步：让已收录的 ToolBox 页反向带竞品标签
ToolBox 本体收录后，在其产品页的 **"What's this an alternative to?"** 字段里，
关联上述竞品（it-tools / toolfk 等），双向加固。

---

## 二、Product Hunt：媒体素材规格（最容易踩坑的就是尺寸）

### 必交素材与尺寸
| 素材 | 尺寸 / 格式 | 要点 |
|------|-------------|------|
| **Gallery 首图** | `1270 × 760 px`，PNG/JPG | 第 1 张最重要；含产品名 + 一句价值主张 + 界面截图；用品牌色 `#FF6B35` 做对比；**不要纯文字海报** |
| Gallery 附加图 | 同上，最多 5 张 | 截图为主，展示核心功能 |
| **Icon（产品图标）** | `240 × 240 px`，PNG，透明背景，圆角 | 用站标或工具图标；不要带文字 |
| 视频 / GIF（可选） | MP4 或 GIF，≤ 60s，16:9 | 录一段「打开即用」的演示，比静态图转化高 |
| Tagline | ≤ 60 字符 | 见 `backlink-submit-copy.md` PH 段 |

### 制作要点（照做就能过审）
- 首图比例严格 1270×760（约 5:3），比例错会被压缩变形。
- 首图左上角放 Logo + 站名，中部放 1 句价值主张（如「6000+ 免费在线工具，数据不上传」），右侧/下方放真实界面截图。
- 字体用无衬线（站里已是 Plus Jakarta Sans / Noto Sans SC），保持统一。
- Icon 必须透明背景，PH 会把它放在圆形/圆角容器里。
- 用 Figma / Canva 做，导出 2x 防糊（实际传 1x 尺寸即可，PH 自动适配）。

### Launch 时间（流量窗口）
- **周二 ~ 周四** 的 `12:01 AM PST`（即北京时间 当天 15:01）发布，流量最高。
- 避免周五 / 周末 / 节假日。
- 发布后前 2 小时自己 + 好友点赞评论，冲当日排行榜。

---

## 三、其他平台素材规格（一览）

| 平台 | 图要求 | 备注 |
|------|--------|------|
| **Hacker News (Show HN)** | 无图，纯文本 | 标题格式 `Show HN: <产品> - <一句话>`；见 `backlink-submit-copy.md` |
| **少数派** | 题图 16:9（建议 1200×675），正文配图宽 ≤ 1000px，JPG | 投稿走「效率工具」栏目；先给价值后落链接 |
| **V2EX** | 正文可插图床图（.imgur / 微博图床），宽 ≤ 800px | 发「分享发现」节点；不硬广 |
| **Reddit** | 帖图 16:9；社区无强制 icon | 发 r/usefulwebsites、r/software、r/SideProject；遵守各版规则 |
| **GitHub awesome-*** | 无图，Markdown 链接 | 提 PR 到 `awesome-*` 列表，一行 `⭐ [ToolBox](url) - 描述` |
| **资源页 (Link Building)** | 通常无图，纯链接 | 见 `backlink-plan.md` 第 8 节邮件模板 |

---

## 四、ToolBox 官方素材（各平台复用，统一口径）

| 项 | 值 |
|----|----|
| 官网 | `https://chenguangwu.github.io` |
| og 分享图 | `/og-image.png`（1200 × 630，已存在，可直接当社媒题图） |
| 一句话定位 | 「6000+ 免费在线工具，纯前端运行，数据不上传」 |
| 与 it-tools 差异 | 工具更全（6000+ vs 几十）、中文界面、零后端 |
| 主色 | `#FF6B35` |
| 辅色 | `#7C3AED` |
| 字体 | Plus Jakarta Sans / Noto Sans SC |

> 复用同一句定位 + 同一张 og 图，保证各平台品牌一致，也省得每次重新做图。

---

## 五、执行顺序（避免一天暴涨被判作弊）

1. **第 1 周**：提交 ToolBox 本体到 AlternativeTo（第 1 步），同时做好 PH 首图/Icon。
2. **第 2 周**：AlternativeTo 添加 5 个 ★ 竞品（it-tools / toolfk / smallpdf / jsonformatter / base64decode）。
3. **第 3 周**：Product Hunt Launch（周二~周四 15:01 北京时间）+ 同日 Hacker News Show HN。
4. **之后每周**：匀速做 2~3 个资源页投稿 / 社区文章，长尾工具靠这个慢慢覆盖。

> 节奏核心：**渐进、自然、相关性高**。单周外链增量控制在个位数，远好于一天上百条（后者必被算法盯上）。
