# 航空/机器人 · tools/{aerospace,robotics}（~60 页）

## 已知问题
### A2. 遗留：breguet ISP=6000s 为 TSFC 口径（自洽不立案，建议页面加单位注释）。
- 受影响：tools/aerospace/breguet-range.html

## 功能缺陷
- 无人机缺「续航/图传距离」实用计算（消费级场景）。

## 优化点
- S2 场景：「多旋翼 5kg 载荷悬停时间」。

## 受影响范围
- tools/aerospace/（37）、tools/robotics/

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 覆盖
- 本轮抽查上述 3 页，仅源码和算术推导，未实测浏览器及线上；其余页面未逐页覆盖。三条已全部修复销账。

## 2026-11-03 续查（并行批 I）

### AR-N1 编码器使用指南仍用 CPR 口径，与工具页 PPR 口径冲突（低，确认文本冲突）
- 现状：工具页、深解、i18n 元描述已统一为「PPR（单相脉冲/转），四倍频后计数 4×PPR」，公式 Δθ=360°/(4·PPR)。
- 残留：`guides/encoder-angle-resolution-guide.html:7,60,62,64,66,68` 与 `i18n/guides/encoder-angle-resolution-guide.json:5` 仍写「CPR（已四倍频）+360°/(4·CPR)」，同一公式用「已四倍频」的词再乘 4，读起来自相矛盾；示例标注「CPR=1000 → 0.09°」与工具页「PPR=1000 → 0.09°」同名不同义。
- 影响：从工具页跳转指南的用户会把 PPR 当 CPR 填，或反过来理解成两次四倍频。
- 方案：指南正文、示例标签与指南 i18n 键/译文统一改为 PPR，并保留一句「CPR=4×PPR（计数/转）」的换算说明；改后跑 `_build.py` 与 `_test_static.py`。

### 留存优化
- 两 Δv 页合并口径：统一 g₀ 与 m0>mf 校验，并互相加「本页用比冲 / 本页用排气速度」的交叉说明，避免同源工具给出不同默认值。
- 编码器页：把 PPR/CPR 做成下拉口径选择，或直接在输入框后给出「若手册标 CPR，请填 CPR/4」的换算提示。
- 轮式里程计与差速驱动两页共用一句符号约定（「右轮快 → 逆时针，ω>0」），减少方向类重复答疑。
- 二连杆三页（FK / IK / 工作空间）的示例坐标统一由 node 生成并回填，杜绝手写尾数漂移。
- 重力补偿页可补一张「θ 从水平起算」的小示意图，替代纯文字定义。

### 续查覆盖
- 已覆盖 8 页：`tools/aerospace/delta-v-rocket.html`、`tools/aerospace/rocket-delta-v.html`、`tools/aerospace/specific-impulse.html`、`tools/aerospace/turn-radius.html`、`tools/robotics/forward-kinematics-2r.html`、`tools/robotics/wheel-odometry.html`、`tools/robotics/gravity-comp-torque.html`、`tools/robotics/encoder-angle-resolution.html`。
- 未覆盖：aerospace 其余 31 页与 robotics 其余 22 页（扣除第一轮已查 4 页）本批未逐页审计。
- 验证声明：仅源码阅读 + node 内存复算（未开浏览器），未做英文态（`?lang=en-US`）、移动端、门禁或线上验证；专业标准取值未逐条核对。
