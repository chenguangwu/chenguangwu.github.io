# 单位换算 + 日期时间族审计矩阵（07 批·只读）

> 扫描日期：2026-11-05｜纪律：只读，未改任何工具页、未跑 `_build.py`、未 push。
> 基准：[units-factors.md](../units-factors.md)（面积/农业/水分/林业/能量因子权威表）。
> 覆盖：`tools/**/*.html` 中 `cat=convert` **297 页** + 含 `type="date"` **127 页**；核心换算/日期页全读 30 页，真机抽验 5 页 / 11 例。

## 结论摘要

| 族 | 候选页 | 真缺陷 | 声明超出实现 | 一致/已核对 |
|---|---|---|---|---|
| 单位换算 | 297（cat=convert） | **2**（`nm` 键误用、温度无绝对零度拦截） | **2**（浓度页、高级换算页） | 长度/质量/体积/温度/压力/功率/能量/数据量/角度/速度/面积核心页 13 页 |
| 日期时间 | 127（含 date 输入） | **5 页 / 9 项**（时区 3、月末 1、UTC 解析 2、BPD 1、2/29 2） | **2**（教育时区页、世界时区页 FAQ） | `date-diff`、`date-add-subtract`、`workday-calculator`、`leap-year-checker`、`zodiac-calculator`、`travel/timezone-converter-advanced` |

---

## 一、单位换算族矩阵

### 1.1 逐量纲核对

| 量纲 | 代表页 | 核对的关键因子 | 判定 |
|---|---|---|---|
| 长度 | `life/length-converter.html`、`life/unit-converter.html`、`science/si-unit-converter.html` | in=0.0254 m（25.4 mm ✓）、ft=0.3048、yd=0.9144、mi=1609.344、nmi=1852（✓）、ly≈9.4607e15 | ✅ 一致 |
| 质量 | `life/weight-converter.html`、`life/unit-converter.html` | lb=0.45359237、oz=28.349523125、ct=0.2 g、斤=500 g、两=50 g、troy oz=0.0311035 kg、stone=6.35029 | ✅ 一致 |
| 体积 | `life/volume-converter.html`、`life/unit-converter.html` | 美加仑=3.785411784 L、英加仑=4.54609、桶=158.987、ft³=28.3168、in³=0.0163871 | ✅ 一致 |
| 温度 | `life/temperature-converter.html`、`life/unit-converter.html`、`science/si-unit-converter.html`、`edu/convert-area-volume.html` | C↔F 均为 `(F−32)×5/9`（等价 `÷1.8`，非 `F/1.8−17.78`）；K=C+273.15；R=F+459.67；Ré=C×0.8 | ✅ 数值一致；⚠️ 无绝对零度下限拦截（低） |
| 压力 | `life/pressure-converter.html`、`science/science-pressure-converter.html`、`automotive/tire-pressure.html` | psi=6894.757293 Pa ⇒ **psi↔kPa=6.894757**（✓）；bar=100 kPa；kgf/cm²=98.0665 kPa；mmHg=133.322 | ✅ 一致 |
| 功率 | `life/power-converter.html`、`life/unit-converter.html` | hp(英)=745.699872 W、hp(公制)=735.49875、BTU/h=0.293071、冷吨=3516.85；dBm→W=`10^((dBm−30)/10)` | ✅ 一致 |
| 能量 | `life/energy-converter.html`、`life/unit-converter.html` | **1 kWh=3.6 MJ**（✓）、1 cal=4.184 J、1 BTU=1055.05585 J、1 ft·lb=1.35582 J | ✅ 一致 |
| 数据量 | `life/data-unit-converter.html`、`it/unit-converter-advanced.html` | 十进制 1000 / 二进制 1024 双档；B→bit=1/8；页面已明示 `1 KB=1024 B` | ✅ 一致（命名 KB 而非 KiB，但已声明） |
| 角度 | `life/angle-converter.html`、`life/unit-converter.html` | rad=180/π=57.29578°、grad=0.9°、rev=360° | ✅ 一致 |
| 浓度 | `life/concentration-converter.html` | 1%=10000 ppm、1 ppb=0.001 ppm、1 ppt=1e-6 ppm、1 mg/L≈1 ppm（水，ρ≈1） | ✅ 数值一致；❌ 声明 mol/L 与密度见 §三 |
| 面积 | `life/area-converter.html`、`life/unit-converter.html` | **1 亩=666.6666667 ㎡**（✓）、1 顷=66666.7 ㎡、1 ha=10000 ㎡、acre=4046.8564224 | ✅ 一致 |
| 速度 | `life/speed-converter.html`、`life/unit-converter.html` | knot=0.514444 m/s、mph=0.44704、mach=340.3 m/s、1 m/s=3.6 km/h | ✅ 一致；⚠️ 综合页另设「音速=343 m/s」与「马赫=340.29」并置，属口径并列表述（低） |
| 时间 | `life/time-converter.html`、`life/unit-converter.html` | 月=2629800 s（30.4375 天）、年=31557600 s（365.25 天） | ⚠️ 与综合页「月=30 天 / 年=365 天」不一致，但各自标签已注明口径（低） |

### 1.2 单位族真缺陷

| # | 页面:行 | 现状 | 正确值 | 复算依据 |
|---|---|---|---|---|
| U1 | [unit-converter-advanced.html:223](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/it/unit-converter-advanced.html#L223) | 长度表 `nm:1852`，输入 `1 nm` 被当作 **1 海里=1852 m** | `nm=1e-9`（纳米）；海里应用 `nmi=1852` | 1 nm=10⁻⁹ m；1 海里=1852 m，相差 1.852×10¹² 倍；页面单位键为自由文本输入，用户按 SI 习惯输入 `nm` 必错 |
| U2 | [temperature-converter.html:428-431](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/temperature-converter.html#L428-L431) | 输入 −300 ℃ 仍输出 −300 ℃ / −508 ℉ / −26.85 K（负开尔文） | 输入 < −273.15 ℃ 时应拒绝并提示「低于绝对零度」 | 绝对零度 0 K = −273.15 ℃；K=C+273.15，C=−300 时 K=−26.85 无物理意义 |

---

## 二、日期时间族矩阵

### 2.1 逐陷阱核对

| 陷阱 | 扫描口径 | 命中/风险 | 判定 |
|---|---|---|---|
| `new Date('YYYY-MM-DD')` 按 UTC 解析 | 含 `type="date"` 且 `new Date(...)` | 127 页含 date 输入；5 页直接把 `.value` 传入 `new Date` | ❌ 负时区回退一天（已真机复现） |
| `toISOString()` 取日期 | 全站含 `toISOString()` | 111 页 | ❌ UTC+8 的 00:00–08:00 取到前一日；3 页直接写入日期输入框 |
| 月末 `setMonth` 溢出 | 含 `.setMonth(` | 17 页 | ❌ 31 日 + 1 月 → 3 月 3 日（已复现）；另有 3 页默认预填受影响 |
| 闰年 2/29 | `new Date(y,1,29)` / 里程碑 | 2 页 | ⚠️ 非闰年静默滚到 3/1（低） |
| 跨年 | 倒计时/纪念日循环 | `countdown-2`、`wedding/countdown-time`、`funeral/memorial-date` | ✅ 已按本地日期解析并跨年回绕 |
| 夏令时 DST | `isDST` / `dstMonths` / `Intl` | 3 页 | ❌ 世界时区页 DST 死代码；❌ 教育时区页按月粗判；✅ 高级时区页用 `Intl` 正确 |
| `getDay()` 0=周日 | 全站星期数组 | `date-diff` 等用 `['日','一'…]` | ✅ 数组口径正确；但 UTC 解析负时区下 `getDay()` 本身偏移一天 |
| 固定偏移时区 | `timestamp.html` 选项 | 显式写「北美东部**标准**时间 UTC−05:00」 | ✅ 已声明为固定标准偏移，不声称 DST |

### 2.2 日期族真缺陷

| # | 页面:行 | 现状 | 正确值 | 复算依据 |
|---|---|---|---|---|
| D1 | [world-timezone-converter.html:366](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/travel/world-timezone-converter.html#L366) | `targetTime.setHours(0,0,0,0)` 原地改写 `targetTime`，随后各城市卡片用它格式化 → **所有城市时钟恒显示 00:00** | 先取当日零点差值，另建 `midnight` 副本，原 `targetTime` 保留时刻 | 真机：北京/东京/伦敦/纽约卡片均 `time=00:00`；输入当前时刻应为 12:00/13:00/04:00/23:00（跨日） |
| D2 | [world-timezone-converter.html:316-320](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/travel/world-timezone-converter.html#L316-L320) | 定义 `isDST()` 但**从未调用**；`diff=data.offset-localOffset` 只用固定 `offset`（纽约 −5、伦敦 0） | 用 `Intl.DateTimeFormat` 取所选日期的实际偏移，或至少调用 `isDST` 修正 | 纽约 2026-07-01 实为 EDT −4，页面按 −5 输出，晚 1 小时；伦敦 2026-07-01 实为 BST +1，页面按 0 输出 |
| D3 | [world-timezone-converter.html:357](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/travel/world-timezone-converter.html#L357) | `now.toISOString().slice(0,10)` 写回 `localDate` | 用本地年/月/日格式化（`getFullYear/getMonth/getDate`） | UTC+8 下本地 00:00–07:59 的 `toISOString()` 日期为前一日，会把用户选的日期覆盖成昨天 |
| D4 | [date-difference-calculator.html:516](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/date-difference-calculator.html#L516) | `result.setMonth(result.getMonth()+months)` 无月末夹取 | 目标月无该日时取该月最后一天（1/31 +1 月 → 2/28） | 真机：`2026-01-31 +1 月` 输出 **2026-03-03**，正确 2026-02-28；JS `setMonth` 溢出规则所致 |
| D5 | [date-difference-calculator.html:445](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/date-difference-calculator.html#L445) | `new Date('YYYY-MM-DD')` 按 UTC 解析，随后用本地 `getDay()`/`setDate()` 迭代 | 用 `new Date(y, m-1, d)` 本地构造 | 真机（America/New_York）：`2026-01-01.getDay()`=3（周三），正确周四=4；`countWorkdays(1/1–1/31)`=23，正确 22 |
| D6 | [date-difference-calculator.html:409](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/date-difference-calculator.html#L409)、[:856](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/date-difference-calculator.html#L856)、[:860](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/date-difference-calculator.html#L860) | 默认日期与「下月同日」均用 `toISOString()` | 本地日期格式化；下月同日需月末夹取 | 同 D3；且 `nextMonth.setMonth(+1)` 在 1/31 同样溢出为 3/3 |
| D7 | [gestational-age.html:354-355](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/obstetrics/gestational-age.html#L354-L355) | BPD 孕周 `(2.11 + BPD(cm)×1.942)×7` 天 | Hadlock(1984)：`GA(周)=9.54+1.482×BPD+0.1676×BPD²`（BPD 单位 cm） | 真机 BPD=45 mm → 页面 **10+6**；Hadlock = 9.54+6.669+3.395 = **19.6 周≈19+4**；校正预产期页面 2026-12-22，正确 2026-10-22（280−137=143 天） |
| D8 | [age-calculator.html:610](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/age-calculator.html#L610) | 里程碑用 `new Date(by+age, bm-1, bd)`，2/29 出生在平年滚到 3/1 | 与 `nextBirthday` 一致夹取到 2/28 | 2000-02-29 出生，1 岁里程碑显示 2001-03-01；页面下一生日已按 2/28 处理，两处口径矛盾 |
| D9 | [age-in-days.html:566](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/age-in-days.html#L566) | `nextBirthday` 用 `new Date(y,1,29)`，平年 → 3/1 | 夹取 2/28（或按当地惯例 3/1，需与全站统一） | 2/29 出生、平年时「距下次生日」多算 1 天 |

### 2.3 同类风险（未逐页真机，按模式登记）

- **默认日期 `setMonth` 溢出**：`agriculture/harvest-date-predictor.html:255`、`legal2/statute-deadline.html:406`、`date-difference-calculator.html:859` —— 仅在当天为 29–31 日时预填日期偏移 1–3 天（低）。
- **`new Date(.value)` 直接解析**（UTC 风险）：`health/pregnancy-due-date.html`、`health/ovulation-calculator.html`、`fire/detector-44.html`、`legal/late-payment-interest.html`、`edu/ebbinghaus-curve.html`。这些页在 UTC+8 无可见偏差，负时区用户会差 1 天。

---

## 三、声明超出实现

| # | 页面 | 声明 | 实现 | 建议 |
|---|---|---|---|---|
| C1 | [concentration-converter.html:10](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/life/concentration-converter.html#L10) | meta/og/JSON-LD/FAQ 称「在 ppm、mg/L、百分比与**摩尔浓度**间换算，**依据溶液密度**处理水溶液」 | 仅有 ppm/ppb/ppt/%/mg/L/μg/L，**无 mol/L 单位、无密度输入** | 删去「摩尔浓度」「依据溶液密度」，或补 mol/L 与密度输入 |
| C2 | [unit-converter-advanced.html:108](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/it/unit-converter-advanced.html#L108) | 类别列表写「…速度、数据存储、**压强与能量**」 | `U` 仅 length/mass/area/volume/time/speed/data/temperature，**无压力、无能量** | 删去「压强与能量」或补两组单位 |
| C3 | [timezone-converter.html:596](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/edu/timezone-converter.html#L596) | FAQ/引据表称「各时区偏移以 **IANA 数据库**为准，含历史变更与夏令时」 | 静态 `TIMEZONES` 表 + `dstMonths` 按月粗判；`dstMonths:[3..10]`，无过渡日 | 改用 `Intl.DateTimeFormat` 的 IANA 时区；或把声明降级为「按月近似」 |
| C4 | [world-timezone-converter.html:216](file:///Users/cgw/project/cgw/chenguangwu.github.io/tools/travel/world-timezone-converter.html#L216) | FAQ：「夏令时按各城 offset 与月份经验判断，**主要城市准确**」 | `isDST()` 死代码，DST 完全未应用 | 同 D2 |

---

## 四、一致 / 已核对清单

- 单位：`life/length-converter`、`weight-converter`、`volume-converter`、`area-converter`、`temperature-converter`（公式）、`pressure-converter`、`power-converter`、`energy-converter`、`data-unit-converter`、`angle-converter`、`speed-converter`、`time-converter`（口径已标注）、`life/unit-converter`、`science/si-unit-converter`、`science/science-pressure-converter`。
- 日期：`life/date-diff`（本地 `parseDate` + 含首尾计数 + 周日数组正确）、`life/date-add-subtract`（月末夹取已实现）、`life/workday-calculator`、`life/leap-year-checker`、`life/zodiac-calculator`（已改本地解析）、`travel/timezone-converter-advanced`（`Intl` + 两段式偏移，真机 4 例正确）、`life/timestamp`（固定偏移已在选项标注「标准时间」）。

### 真机抽验记录（Chrome headless，本地 8137 端口）

| 页面 | 用例 | 页面输出 | 期望 | 结果 |
|---|---|---|---|---|
| `travel/world-timezone-converter` | 加载默认城市卡片 | 4 城均 `00:00` | 各城不同时刻 | ❌ 复现 D1 |
| `life/date-difference-calculator` | 2026-01-31 +1 月 | 2026-03-03 | 2026-02-28 | ❌ 复现 D4 |
| `life/date-difference-calculator` | America/New_York 下 1/1 星期与 1/1–1/31 工作日 | 周 3 / 23 天 | 周四 / 22 天 | ❌ 复现 D5 |
| `obstetrics/gestational-age` | BPD 45 mm、2026-06-01 | 10+6、EDD 2026-12-22 | 19+4、EDD 2026-10-22 | ❌ 复现 D7 |
| `edu/timezone-converter` | 北京 12:00 → 纽约 2026-03-01（勾 DST） | UTC−4 | UTC−5 | ❌ 复现 C3 |
| `edu/timezone-converter` | 北京 12:00 → 伦敦 2026-10-31（勾 DST） | UTC+1 | UTC+0 | ❌ 复现 C3 |
| `travel/timezone-converter-advanced` | 北京 20:00 → 纽约（7/1、3/8、11/1） | 08:00 / −1 日 23:00 / 00:00 | 同左 | ✅ 通过 |

---

## 五、建议与边界

1. 单位族优先修 **U1 `nm` 键**（静默 1.852×10¹² 倍误差）与 **C1 浓度声明**；其余因子全部与 `units-factors.md` 一致。
2. 日期族优先修 **D1（全城 00:00）**、**D7（BPD 孕周减半）**、**D4（月末溢出）**、**D2/D3（DST 与 ISO 日期）**；D5/D6 属「负时区/清晨窗口」误差，可与全站 `new Date('YYYY-MM-DD')` 清理一并处理。
3. 统一口径：全站日期字符串一律用 `parseLocalDate(y,m,d)`；月份加法一律「目标月夹取到月末」；跨时区展示一律 `Intl`，禁用固定 offset 表。
4. 本批未逐页读 297 个 `cat=convert` 页全部因子表，采用「核心 15 页全读 + 全站常量模式扫描（25.4/6.894757/3.6/666.67/1852/1.8/17.78/0.03937）」；未命中额外数值错误。剩余页建议由各行业修复线按 `units-factors.md` 复核。
