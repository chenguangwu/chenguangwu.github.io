# 教育/语言 · tools/{edu,edu2,language,chinese}（~60 页）

## 已知问题
### E2. 遗留：GPA 页「加权平均权重和≠1」未系统扫（列入：输入学分权重后校验 Σw 提示）。
- 受影响：tools/edu/gpa-calculator.html、grade-weight-calculator 等

## 功能缺陷
- 成绩页缺「目标分反推」（期末要考多少分才能到绩点 X）——学生刚需。
- 中文页（chinese-culture/lunar）静态，缺「生辰八字/节气」交互深挖。

## 优化点
- ✅ S2 场景（2026-10-26）：exam-score-calculator 加 3 分制预设「四级 710 分制」（456 题对 → 456.0 分 vs 及格线 425）「高考 750 分制」「考研 500 分制」，labelEn 双语；verify edu 70→73、判别器 0 逃生；顺带修该页 #result EN 存量泄漏（成绩/等级/对比全 __T 化）→ OK_EN。倒计时类因铁律④（测试禁依赖当前时间）不纳入测试，未做。
- S4 分享卡：倒计时打卡卡。

## 受影响范围
- tools/edu/（47）、tools/edu2/、tools/language/、tools/chinese/

## 进度
- 🟡 续批中（S2 分制场景已落地；剩余：目标分反推 / 生辰八字节气深挖 / S4 打卡分享卡）
