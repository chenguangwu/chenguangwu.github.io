# 2026-11-14-396 文娱 · meditation-timer 落地真实倒计时计时器

## 修复内容
`tools/fun/meditation-timer.html` 此前存在「名不副实」缺陷（fake-tools C 类，part-02:198）：
- meta/深解均宣称「纯前端本地计时」「倒计时」「附提示音」，但实际只生成静态分段时刻表，**无任何实时计时**（grep 证实 `setInterval=0`、`AudioContext=0`）。

本次**实现真实可运行计时器**（而非删文案，符合「禁止假功能、优先实现真功能」纪律）：

1. **实时倒计时**：`mtmStart/Pause/Reset/Finish` + `setInterval(250ms)`；剩余时长按时间戳 `endTs - Date.now()` 计算（与注意事项表「以时间戳差计算剩余时长，避免定时器累计漂移」一致），暂停后可继续（保留 `remainMs`）。
2. **分段提示音 + 结束鸣钟**：`AudioContext` 合成柔和正弦音；段末轻响（528Hz）、结束双音鸣钟（440→660Hz）；`typeof AudioContext`/`webkitAudioContext` 守卫，stub 环境不报错。
3. **本次练习留痕**：结束将 `{t, min}` 写入 `localStorage.__mtm_sessions`（上限 50 条），补「历史不记实际时长」缺口。
4. UI：卡片内新增实时计时区（大号时钟 + 「第 X / N 段」标签 + 开始/暂停/重置 + 状态行），启动钩子 `mtmReset()` 初始化显示随输入同步。

## 证据
- 修复前：`grep setInterval/AudioContext` 均为 0；part-02:198 记录成立。
- 修复后：`node --check` 内联脚本语法通过；计时逻辑用原生定时器与 Web Audio，不依赖 CDN/stub；基线交互（点「计算」）不受影响。

## 验证
- [x] 内联 JS `node --check` 语法通过
- [ ] 待跑 `python3 _build.py` + `scripts/run_gates.py` 全绿
- [ ] 真机确认：开始→倒计时走表、段末响、结束鸣钟、暂停继续、重置归位

## 销账
- `plan/fake-tools/part-02.md` 第 198 行整条删除

## 门禁
- 待执行 `scripts/run_gates.py`（5 道门禁全过）后本地 commit（不 push，等指令）。
