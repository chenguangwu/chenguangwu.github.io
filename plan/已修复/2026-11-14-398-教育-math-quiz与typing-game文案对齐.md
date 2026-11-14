# 第 398 批 · 教育 · math-quiz 与 typing-game 文案对齐（P3 纯文案）

## 来源
fake-tools 清单（part-01: typing-game C 类 / math-quiz D 类；part-02: 同两页「真」缺陷行）。
属「名不副实」轻度项：功能基本已实现，仅描述/FAQ/opt-guide 与页面能力错位。

## 改动
### tools/edu/math-quiz.html
- `opt-guide` 第 2 步「点击计算/生成」套话 → 改为「设置难度与题量后点击『开始』，系统随机出题并限时作答、自动判分」。
- 深度解析 FAQ「如何使用」dd 同步修正。
- JSON-LD `FAQPage` 中「如何使用数学测验？」答案同步修正（消除结构化数据误导）。
- 验证：残留 `点击「计算」或「生成」` = 0；JSON-LD 经 `json.loads` 校验合法。

### tools/edu/typing-game.html
- 四处一致 meta「提供练习文本与错题回看」→「提供练习文本，自动统计正确率与速度（字/分）」（消除「错题回看」虚假承诺）。
- 深度解析 FAQ「本地？」原「成绩存本地，不上传」→「本页只本地统计正确率与速度，不保存历史成绩或错题，刷新即清空；所有计算在浏览器本地完成，不上传数据」（如实描述 localStorage 仅存主题的现状）。
- 验证：残留 `错题回看` = 0、`成绩存本地` = 0。

## 销账
- 整条删除 `plan/fake-tools/part-01.md` 中 math-quiz / typing-game 两行。
- 整条删除 `plan/fake-tools/part-02.md` 中 math-quiz / typing-game 两行。

## 校验
- 两文件 inline JS 经 `node --check` 通过；math-quiz JSON-LD 合法。
- 本批为纯文案改动，未触发逻辑变更，轻量校验即通过；全量门禁并入收尾统一跑。

## 同批未动（说明）
- part-02:97 的「优先改」清单组句仍列两页名，属分组备注非缺陷行，保留不删。
