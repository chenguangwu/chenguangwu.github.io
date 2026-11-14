# 379 设计 · waveform / spectrum 画布非等比拉伸与无 DPR 修复（D-N132 / D-N135）

- **分类**：04-设计创意
- **工具页**：`tools/design/waveform-visualizer.html`、`tools/design/spectrum-visualizer.html`
- **日期**：2026-11-14
- **缺陷编号**：D-N132（中）、D-N135（中）

## 缺陷与根因（两页同源）

内部画布固定 `<canvas width="800" height="200">`，CSS 却是 `width:100%; height:200px`：

- **横向**随容器宽度缩放（350px → ×0.438；1080px → ×1.350），**纵向**恒 ×1.000；
- 未按 `devicePixelRatio` 重设内部像素 ⇒ 高 DPR 屏在已拉伸位图上再放大一次，笔画发虚。

具体后果：

- **waveform**：波形周期疏密随窗口宽度漂移，同一组参数在不同宽度下观感不同；
- **spectrum 圆环模式**：圆环按内部坐标 `r = min(w,h)/4` 画正圆，显示时横向被压缩/拉伸 ⇒ 移动端 350px 容器下纵横比约 **0.438**，正圆变竖椭圆。

## 修复（两页同一套）

1. **CSS 固定 4:1 比例**：`canvas{width:100%;height:auto;aspect-ratio:4/1}` —— 显示尺寸恒为 `容器宽 × 容器宽/4`，与内部 4:1 一致，从根上消除非等比拉伸。
2. **`fitCanvas()` 按 DPR 重设内部像素**：

```js
const dpr = window.devicePixelRatio || 1;
const cw = Math.max(1, Math.round(canvas.clientWidth || 800));
const ch = Math.max(1, Math.round(cw / 4));
const nw = Math.round(cw * dpr), nh = Math.round(ch * dpr);
if (canvas.width !== nw || canvas.height !== nh) { canvas.width = nw; canvas.height = nh; }
canvas.__dpr = dpr;
```

只在尺寸变化时真正赋值（避免每帧重建位图）；`clientWidth || 800` 兜底隐藏/无布局场景。

3. **绘制入口先适配**：`drawWave()` / `draw()` 首行调用 `fitCanvas()`；线宽与阴影按 `dpr` 缩放（waveform `1×dpr` / `2×dpr` / `shadowBlur 8×dpr`，spectrum 圆环 `3×dpr`），保证不同 DPR 下视觉粗细一致。
4. **补 `resize` 监听**（两页均原先没有）：窗口宽度变化 / 屏幕旋转后重设并重绘。

两页绘制逻辑本身全部基于 `canvas.width/height`（无硬编码 800/200），故适配后自动等比，无需改坐标计算。

## 验证

**比例复算**（`/tmp/canvas_ratio_probe.js`，横向缩放比 ÷ 纵向缩放比 = 变形比，1.000 为不变形）：

| 容器宽 | DPR | 旧 变形比 | 新 变形比 | 新内部像素 |
|---|---|---|---|---|
| 350px | 1 | **0.438** | 1.006 | 350×88 |
| 350px | 2 | **0.438** | 1.006 | 700×176 |
| 860px | 1 | **1.075** | 1.000 | 860×215 |
| 860px | 2 | **1.075** | 1.000 | 1720×430 |
| 1080px | 1 | **1.350** | 1.000 | 1080×270 |
| 1080px | 2 | **1.350** | 1.000 | 2160×540 |

（新方案 1.006 的残差来自 `Math.round(cw/4)` 取整，1px 级，可忽略。）

**门禁**：
- `verify_design_calc.js design/waveform-visualizer` → **4/4 通过**
- `verify_design_calc.js design/spectrum-visualizer` → **4/4 通过**
- `check_inline_js_syntax.js` → **12141** 个内联脚本语法正确

harness 的 canvas stub 无 `clientWidth`（兜底 800）、`devicePixelRatio` 为 undefined（兜底 1）⇒ 内部尺寸仍为 800×200，与原行为一致，故既有用例零回归。

## 影响面

仅两个 `tools/design/*.html`（内联 CSS + 内联 JS）。无 i18n / EN 字典 / 构建源变更，`_build.py` 无需重跑。
