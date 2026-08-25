# N2-01 移动端 / 无障碍 / 性能问题矩阵

> 盘点日期：2026-08-20
> 方法：静态扫描全站 5278 个工具页 + `css/common.css`、`css/style.css` 公共样式；维度覆盖 390px 横向滚动、固定底栏遮挡、键盘焦点、触控目标、aria/alt/lang、reduced-motion。
> 配套任务：N2-02 按本矩阵修复（先 P0 后 P1）。

## 已确认良好（绿，无需修）

1. **键盘焦点**：`common.css` 全局 `*:focus-visible` 轮廓（774 行）+ 各交互元素 `a/button/input/select/textarea/[tabindex]/.btn/.nav-icon-btn/.fav-btn/.theme-btn/.guide-link/.privacy-badge` 的 `:focus-visible` 规则（985-996）。键盘可达且焦点清晰。
2. **屏幕阅读器**：`.sr-only` 屏幕阅读器专用隐藏类（common.css:3）。
3. **动效减弱**：`prefers-reduced-motion` 两处（628、1012）。
4. **响应式体系**：`common.css` / `style.css` 完善的 `@media(max-width:768px)` 断点——首页侧边栏→单列、工具页容器/卡片/输入行（`.input-row`、`.datetime-combo`）单列且 `min-width:0` 防溢出。
5. **首页底栏留位**：`style.css` `.tab-bar`(fixed bottom:0) + `.tab-bar-spacer{height:58px}`(247) + `.jump-top{bottom:80px}`(303) 避免底栏遮挡主要操作。
6. **表格 / 公式横向**：数据表格 `overflow-x:auto`；`.formula-eq{overflow-x:auto}`(962)。
7. **图表类溢出**：3 个图表页（decor/scheduler、electrical/load-curve、fun/keyboard-heatmap）的 `min-width≥390px` 容器均包裹在 `overflow-x:auto` 父容器（`.gantt`/`.chart-wrap`/`.kbd`）内，页面不横向滚动。

## P0（页面级横向滚动 / 底栏遮挡）：0 例

- 全站脚本扫描 5278 页，仅 3 页有 `min-width≥390px` 块级布局容器，且均被 `overflow-x:auto` 父容器包裹，**无页面级横向滚动**。
- 工具页 HTML/JS 均无 `.tab-bar` / `.mobile-bottom-bar` 底栏类引用（Grep 全仓零匹配），**工具页不存在移动端固定底栏**，不遮挡。

## P1（建议修复）

- **P1-1 触控目标未达标**：公共 `.btn` 及 `input/select/textarea` 在移动端未显式 `min-height:44px`（当前靠 padding 约 38-40px，接近但未达 WCAG 2.1 AA 触控目标 44px）。影响全站所有按钮与输入控件。修复：在 `common.css` 的 `@media(max-width:768px)` 内补充 `min-height:44px` + 内容居中。
- **P1-2 部分图标按钮缺 aria-label**：抽样见个别纯图标交互按钮缺 `aria-label`（多数 swap/互换按钮已加，仍有遗漏）。记为后续批逐页补充，不在首批公共修复范围。

## P2（可选 / 低优先）

- **P2-1 死 CSS**：`common.css:421` 的 `.mobile-bottom-bar`（全站零引用，工具页无底栏）属遗留死规则，可清理减少困惑。
- **P2-2 性能**：首屏 Tailwind CDN + Lucide CDN 属外部依赖（AGENTS.md 允许），不在本阶段范围。

## 下一步

N2-02 首批：修复 P1-1（公共 CSS 触控目标加固）+ 清理 P2-1（死 CSS），随后 `python3 scripts/run_gates.py` 验收全绿。
