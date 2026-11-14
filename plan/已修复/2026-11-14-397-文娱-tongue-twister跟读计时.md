# 2026-11-14-397 文娱 · tongue-twister 落地可选跟读计时

## 修复内容
`tools/fun/tongue-twister.html` 存在自相矛盾的「名不副实」缺陷（fake-tools C 类，part-02:184 / W批）：
- 主描述写「不录音、不计时、不评分」属诚实声明，但**深度解析（第 180–193 行）却承诺「跟读计时」「点开始计时、读完点停止、performance 计时」「计时准吗」**，而全文无计时状态、无停止按钮、无用时显示（grep 证实 `setInterval=0`、无计时逻辑）。

本次**实现真实可选计时器**（先实现功能、再统一文案，符合「禁止假功能、优先实现真功能」纪律）：

1. **跟读计时**：新增「⏱ 计时」按钮，用 `performance.now()` 记录当前绕口令跟读用时，实时显示（requestAnimationFrame 刷新）；点「停止」给出本次用时。
2. **最佳成绩**：按绕口令文本存 `localStorage.__tbn_tw_best`（每条最佳用时），抽题/重置时展示「最佳：X 秒」。
3. **状态联动**：`next()`/`reset()` 自动停止进行中的计时并刷新最佳显示，避免跨题串扰。
4. **文案统一**：三处 meta 描述、formula-desc（中英）、注意事项条目、tool-intro 正文、desc-en 均把「不计时」改为「支持可选本地计时记录跟读用时与最佳成绩」；深度解析原本承诺的计时功能现已真实存在。

## 证据
- 修复前：grep `setInterval`=0；part-02:184 记录成立（深解承诺计时但无实现）。
- 修复后：`node --check` 内联脚本语法通过；计时仅由用户点击触发（requestAnimationFrame 在 stub 不跑但无害）；点「开始/下一条」基线交互不受影响。

## 验证
- [x] 内联 JS `node --check` 语法通过
- [ ] 待跑 `python3 _build.py` + `scripts/run_gates.py` 全绿
- [ ] 真机确认：点计时→走表、点停止出用时、最佳成绩记录、换题/重置同步

## 销账
- `plan/fake-tools/part-02.md` 第 184 行整条删除

## 门禁
- 待执行 `scripts/run_gates.py`（5 道门禁全过）后本地 commit（不 push，等指令）。
