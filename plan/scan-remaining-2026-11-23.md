# 全站剩余任务清单（2026-11-23 第510批后）

> 8 类一次性全扫已完成，原清单见
> `plan/已修复/2026-11-23-全站8类扫描原始清单（已修复项归档）.md`。
> 本文件只保留**尚未收口**的条目；修完一条按 MASTER 流程归档并从本文件删除。

## 状态总览

| 类别 | 已收口 | 剩余 |
|---|---|---|
| 1 功能 Bug | `office/flowchart` CDN 守卫；全站 4,700 页无头加载 0 致命错误 | 无 |
| 2 UI 布局 | 390px 横向溢出 10 → 0；`.tabs` 负边距根因已修 | 无 |
| 3 中英文 | `desc-en` 退化 3,570 → 0；简体英文标题真缺陷 → 0；**全站英文态 852 页 / 1,078 条残留 → 0** | 无 |
| 4 SEO 文案 | 工具描述 <70 = 0；指南描述 <70 = 0；应用分类错配 17 → 0 | 无 |
| 5 新增同类工具 | 已新增 `railway/brake-distance`（含指南、i18n、UX 8/9） | 3 个候选 |
| 6 无用脚本 | 清理 `_en-i18n` 1,017 个 + `scripts` 959 个一次性脚本 | 长尾脚本待逐项评估 |
| 7 批量误插 | 197 页占位 `formula-desc` → 0；空面板未发现 | 无 |
| 8 其他 | 扫描项已入 269 项门禁；指南尾句幂等修复；台账归档 | 迁移壳与假工具历史账 |

## 剩余任务


### R2（中）新增同类工具 3 个

候选均为纯前端可完成：

1. `daily-goods/trash-bag-size`：按袋口周长/桶口尺寸与垃圾量估算所需袋型与厚度。
2. `beekeeping/winter-feed-syrup`：按蜂群量、越冬期与糖浆浓度配比冬饲料。
3. `express/box-fit`：按物品三维与箱内尺寸判断能否装入及最优摆放方向。

每个必须同时交付：中文工具页、`i18n/tools/<ind>.json` + `slug-en.json` +
`_en_override.json`、第三层英文词典、`guides/<slug>-guide.html`、`json/guides.json`
条目，并过 269 项门禁。

### R3（低）迁移壳超期清理

- `grep -rl TOOLBOX-REDIRECT tools guides --include='*.html'` 共 109 个。
- 按 AGENTS §4.6：建壳同批用 `--no-verify` 提死链并登记
  `_redirect_stubs_todo.md`；到期物理删除，删除后部署成功再用默认校验提交一次。
- **不要**把仍有搜索流量的壳一次性全删；先按 `_redirect_stubs_todo.md` 到期日排序。

### R4（低）脚本长尾评估

- `scripts/` 现有 762 个跟踪文件，其中约 280 个被 269 项门禁直接引用。
- 剩余为 audit/scan/check 等运维脚本；删除前必须确认：
  ① 不被 `_build.py` 的 `os.path.join(ROOT,'scripts','...')` 调用；
  ② 不被 workflow / `check_pages_artifact.py` 调用；
  ③ 文档未把它作为标准流程。
- 已因漏判动态调用误删 3 个构建脚本（`gen_industry_info/groups/hot_tools`），已恢复；
  后续清理必须跑一次完整 `_build.py` 再提交。

### R5（低）假工具历史账

- `fake_tools_129` 只记 `remaining_listed:69` 且无 slug 清单，已随
  `page-ledger.json` 归档到 `plan/已修复/2026-11-23-page-ledger历史档案.json`。
- 若重启该线，必须先从当时报告重建 69 页 slug 清单，否则不得按数字开工。
