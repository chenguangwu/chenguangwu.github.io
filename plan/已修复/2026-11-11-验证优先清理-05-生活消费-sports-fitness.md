# 验证优先清理归档（仅含已验证修复记录）

来源：05-生活消费/sports-fitness.md

- **处置（2026-11-06 A批·真修复）**：已修复。`tools/fitness/calc.html` `calc()` 加年龄/身高/体重范围校验（10–100/100–230/30–300），越界即 return 提示、不再按 0 代入渲染负热量。verify 因 `calc()` 有 1s 节流、harness 同步采集拿不到拦截提示（盲区），改走 `scripts/_verify_fitness_batch_a.mjs` 运行时断言（5/5，HEAD 回退 2/5 证有效）。移交 `plan/已修复/2026-11-06-SF-N7-N12-体育健身A.md`。
