# 全站剩余任务清单（2026-11-23 第 550 批后）

> 8 类全扫与第 513–535 批修复记录见 `plan/已修复/`。
> 本文件只保留**唯一仍未到期、不可提前执行**的迁移壳清理项。

## 状态总览

| 类别 | 已收口 | 剩余 |
|---|---|---|
| 1 功能 Bug | 4,925 页加载期 0 缺陷；120 页点击烟测 0；TWSTRS 满分口径已修；宠物喂食工具错配旧指南、连续性指南相关工具错配已修 | 无 |
| 2 UI 布局 | 全站 UX 8.64/9；家具布局页与语言切换器 320px 已修；209 个行业首页 320px 横向溢出已修；热门工具前 100 页 320px 实扫，二维码生成器 343px 溢出已修 | 无 |
| 3 中英文 | 16 个零词典指南已全量英文化；3,131 个指南页补齐英文标题/描述兜底，3,428 页相关工具链接、CTA 与导语已批量英文化；209 个行业首页中英文标题重复显示与英文重复 emoji 已修；第 548 批接入 `GUIDE_EN_PACK`、修复 data-i18n 重置、2,744 条公共免责声明入词典，119 个结构化指南英文态清零；全量 3,250 个有效指南扫描 61 页有中文，第 549 批已全部清零；第 550 批 4,822 个工具页正文英文态仅 1 页 1 条、128 页 head 中文，均已清零；工具与指南英文正文/标题/描述复扫 0 残留 | 无 |
| 4 SEO 文案 | 工具/指南描述 <70 = 0；TWSTRS 工具与指南的 75 分残留已统一为 85 分制 | 无 |
| 5 新增同类工具 | `trash-bag-size`、`winter-feed-syrup`、`box-fit`、`water-filter-lifespan`、`ac-energy-cost`、`appliance-lifespan`、`repair-or-replace`、`water-heater-sizing` 已交付 | 无 |
| 6 无用脚本 | 累计清理 `_en-i18n` 1,017 + `scripts` 1,235 个 | 无 |
| 7 批量误插 | 占位 `formula-desc` 0；65 页通用历史模块命名已统一；连续性指南整块无关相关工具已修 | 无 |
| 8 其他 | 全站加载 0 缺陷；核心页元数据补齐 | 迁移壳未到期 |

## 第 548 批：指南英文态根因修复（已本地提交）

- 根因：119 个结构化指南页把 `i18n.js` / `guide-i18n.js` / `guide-en-pack.js` 写死成 `https://chenguangwu.github.io/js/...`，本地改动测不到；同时 `js/i18n.js` 不消费 `GUIDE_EN_PACK`，`data-i18n` 在 init/语言切换时会把指南脚本刚译好的正文重置回中文。
- 修复：指南页三处脚本改站内根相对路径；`resolve()`/`has()` 在 EN 态补查 `GUIDE_EN_PACK`；`scripts/audit_guide_en_head.py` 增加“禁止写死线上 JS 域名 + 必须消费 GUIDE_EN_PACK”回归锁。
- 文案：2,744 条公共免责声明/迁移提示/教育类说明入各指南词典；`checker-manager` 八维评分说明补齐；`text-diff` 示例改英文；`unit-converter` 半中半英步骤修正。
- 验证：119 个结构化指南英文态 0 中文；全量 3,250 个有效指南扫描 61 页残留，已清 10 个高残留页，余 51 页；272 项门禁通过。

## 第 549 批：指南英文正文长尾收口（已本地提交）

- 工具页英文词典自动回填 63 条到 61 个残留指南。
- 人工补齐 15 个高残留页（ratio-hormone、calc-39、chinese-zodiac、bandwidth-1、study-planner、agri-calculator、inference-throughput、cycle-6、calc-gear-2、assessor-1、visitor-route、xiangqi-endgame、step-stride、text-extract-html-tags、sequence-puzzle）。
- 用“片段匹配”补齐剩余 44 页的 1–2 条专业说明；最后补 7 个工具标题（protein-needs、smoking-cost-calculator、tdee-calculator、waist-hip-ratio、vo2-max-calculator、pregnancy-due-date、stretch-generator）。
- 验证：全量 3,250 个有效指南（排除 178 个 meta-refresh 迁移存根）英文态复扫 **0 页残留中文**；272 项门禁通过。

## 第 550 批：工具页英文正文与 head 清零（已本地提交）

- 4,822 个工具页英文态正文扫描：仅 `agriculture/calc-15` 标题中文，补 `Sowing Date Calculator (count back from harvest date)`。
- 工具页 head 扫描：128 页 description 中文、1 页 title 中文（实际为分类页旧值）。根因是 `tool_desc_source.en_desc()` 未读取第三层 `i18n/tools/en/<ind>/<slug>.json`。
- `scripts/tool_desc_source.py` 增加第三层英文描述回退（缓存），`_build.py` 自动写 `desc-en`；3 个仍缺页（ovulation-calculator、citation-format、checker-assessor-1）补 `_en_override.json` 人工英文描述。
- 验证：128 页 head 复扫 0 中文；工具页正文 1 页复扫 0；272 项门禁通过。

## R3：迁移壳到期清理（唯一按日期等待项）

- `grep -rl TOOLBOX-REDIRECT tools guides --include='*.html'` 当前 109 个；最近一批创建于 2026-11-14 / 2026-11-22，按 1 个月保留期，**最早到期日 2026-12-14**。
- 处置结论：**当前无一到期，禁止提前物理删除**。到期后按 AGENTS §4.6：
  1. 物理删除存根；
  2. 部署成功后再用默认校验 `python3 _submit_indexnow_deadlinks.py` 提交死链；
  3. 同步更新 `_redirect_stubs_todo.md` 与 `sitemap-deadlinks.xml`；
  4. 删除前复核搜索流量与目标页可用性。
