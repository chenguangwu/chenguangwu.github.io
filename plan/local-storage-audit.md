# 全站本地存储与敏感字段审计（2026-11-05）

> 范围：根目录 9 页 + `tools/**/*.html` 4912 页 + `guides/*.html` 3410 页 + `js/**/*.js` 34 个，共 **8365 个文件（8331 个页面）**。
> 工具：`scripts/audit_local_storage.py`（新增，可复跑）。
> 口径：站点承诺「数据只在浏览器本地、不上传」，因此本地存储本身是隐私风险面；Cookie / IndexedDB 属规范硬禁止。

## 0. 结论速览

| 项目 | 结果 |
|---|---|
| 高风险（身份 / 健康 / 财务字段落盘） | **61 页**（静态扫描 60 + 人工补 1） |
| 中风险（业务中间态：草稿 / 历史 / 记录 / 队列） | **1091 页** |
| 低风险（偏好 / 主题 / 语言 / 本地统计） | **322 页** |
| 无本地存储 | 6858 页 |
| `document.cookie` 写入 | **0 页** ✅ |
| `indexedDB` 使用 | **0 页** ✅ |
| 明文凭证落盘 | **2 页**（password-generator、jwt-debugger）→ 已修 ✅ |
| 跨页共享同一字面量键 | **2 组**（`calorie_history`、`currency_history`）→ 已修 ✅ |
| 导出夹带未明示的敏感字段 | **未发现**（抽样 5 类身份/健康导出页，列 = 页面表格列） |

## 1. 审计口径

### 1.1 扫描对象

- `localStorage.setItem/getItem/removeItem`、`sessionStorage` 同族调用、方括号读写；
- 存储别名（`const HISTORY_STORE = sessionStorage`）与常量键（`const HISTORY_KEY = 'xxx'`）会回查声明处，避免漏报；
- `document.cookie` **写入**（先剥离 JS 字符串，排除 `tools/it/http-cookies.html` 这类把 `document.cookie` 当教学示例的数据）；
- `indexedDB` 打开/建库。

### 1.2 分档规则（按落盘内容，不按工具分类）

| 档位 | 判据 |
|---|---|
| **高风险** | 页面输入含个人身份（姓名 / 手机号 / 邮箱 / 证件 / 学号工号 / 患者标识）、健康（病史 / 诊断 / 用药 / 体重身高 / 心率血压 / BMI）、财务（收入 / 工资 / 贷款 / 月供 / 首付）语义，且该页存在实际落盘路径（tool-ux 自动回填、显式 `setItem`、ToolKit 历史）。 |
| **中风险** | 无上述敏感字段，但落盘业务中间态（历史、草稿、记录、队列、名单、日志）。含 tool-kit 自动历史与自定义业务键。 |
| **低风险** | 仅偏好（主题 / 语言 / 收藏 / 最近使用）或与个人无关的本地统计（最高分、计数器、游戏进度）。 |
| **无存储** | 页面与共享脚本均未调用 storage。 |

### 1.3 降低误报的两条门控

1. **身体指标只认人体上下文**：`体重/身高/心率/血压/血糖/体温/孕周` 仅当页面位于人体健康目录（`health / fitness / sports / medical / rehab / 各专科` 等）时计入；农业、畜牧、林业、地质、纺织页里的 `weight/height` 是作物、岩体、织物参数，不计入。英文泛化词（`name/weight/height/history/address` 等）仅在页面上下文属于对应语义域时计入，且按完整单词匹配（避免 `username` 被 `name` 命中）。
2. **哈希/加密落盘不算明文凭证**：`*_pwd_hash`、XOR/`enc()` 加密后的 vault、盐值等不计为「明文凭证」。`tools/security/virtual-safe.html` 与 `tools/safety/manager.html` 属此列——**非明文，但加密强度弱**，已登记待改（见 §6）。

## 2. 分档计数（页面口径）

| 档位 | 页面数 | 占比 |
|---|---|---|
| 高风险 Tier 1 | 61 | 0.73% |
| 中风险 Tier 2 | 1091 | 13.10% |
| 低风险 Tier 3 | 322 | 3.87% |
| 无存储 Tier 0 | 6858 | 82.30% |

> 中风险 1091 页中，绝大多数是 tool-kit 自动历史（每次计算把输入/结果写入 `tbk_hist_<path>`）；键按页面路径命名，不与其它页冲突。另有约 200 页使用自定义业务键（草稿、打卡、记录、队列）。
> 低风险 322 页主要是游戏最高分、计数器、主题/语言偏好。

## 3. 违规项（逐类）

### 3.1 Cookie —— 0 违规 ✅

全站无 `document.cookie =` 真实写入。`tools/it/http-cookies.html` 里的 7 处 `document.cookie` 均为「Cookie 构造/解析教学示例」字符串，未执行写入；`scripts/audit_local_storage.py` 已通过剥离脚本字符串将其排除。

### 3.2 IndexedDB —— 0 违规 ✅

全站无 `indexedDB` 引用。

### 3.3 明文凭证落盘 —— 2 页，已修 ✅

| 页面 | 问题 | 处置 |
|---|---|---|
| `tools/it/password-generator.html` | 「本次会话记录」把**生成的密码原文**写入 `sessionStorage`（键 `password_generator_session_history`），同源任意脚本可读；刷新后仍存活。 | 改为**仅页面内存数组** `sessionHistory`，刷新/关闭即清除；提示文案同步改为「仅保存在当前页面内存中」。 |
| `tools/it/jwt-debugger.html` | 解析历史把**完整 JWT 原文**写入 `localStorage`（键 `jwt_debugger_history`）；JWT 常为有效 bearer credential，等同令牌落盘。 | 改为**仅页面内存数组** `jwtHistory`，刷新/关闭即清除。 |

**非明文（登记待改，未改代码）**：

| 页面 | 现状 | 风险 |
|---|---|---|
| `tools/security/virtual-safe.html` | 落盘 `pwdHash` + `salt` | 非明文；但离线可暴力枚举弱口令，属设计强度问题。 |
| `tools/safety/manager.html` | XOR + 主密码派生的加密 blob | 非明文；XOR 非密码学安全，建议后续换 WebCrypto AES-GCM。 |

### 3.4 跨页共享同一键 —— 2 组，已修 ✅

| 键 | 冲突页 | 数据结构差异 | 处置 |
|---|---|---|---|
| `calorie_history` | `tools/health/calorie-needs.html` ↔ `tools/life/daily-calorie-needs.html` | 健康页存 `{date,height,weight,...}`；生活页存 `{label,time,id}`。互相读取会渲染 `undefined` / `NaN`。 | 拆为 `calorie_history:health` / `calorie_history:life`。 |
| `currency_history` | `tools/finance/currency-converter.html` ↔ `tools/travel/currency-cheat-sheet.html` | 财务页存 `{time,from,to,amount}`；旅行页存 `{code,name,flag,rate,time}`。 | 拆为 `currency_history:finance` / `currency_history:travel`。 |

> 其余跨页共用键均为设计内的全局键：`toolbox_theme`、`lang`、`favTools`、`recentTools`、`toolbox_metrics_*`、`tb_ai_*`。按页面路径命名的 `tb_ux_<path>#<id>`、`tb_uxp_<path>#<id>`、`tbk_hist_<path>`、`pk:ans:<slug>` 不会跨页冲突。

## 4. 高风险页清单（按目录）

> 共 61 页：静态扫描 60 页 + 人工补 1 页（cycle-7 的患者标识由动态输入生成，静态解析未命中）。
> 「落盘方式」中 `tool-ux 自动回填` 表示刷新后表单值自动恢复；`自定义键` 为页面显式保存；`ToolKit 历史` 为每次计算自动记录；`data-no-persist` 表示已关闭自动回填（显式保存仍生效）。

#### fitness（15 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `fitness/calc-2.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `fitness/calc-3.html` | health:height | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `fitness/calc-4.html` | health:weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `fitness/calc-5.html` | health:weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `fitness/calc-heart-rate.html` | health:心率 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/calc.html` | health:体重,身高 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/calculator-calc-13.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/calculator-calc-constitution.html` | health:体重,身高 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/estimate-2.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/estimate.html` | health:体重,身高 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/jianzhinengliangquekoujisuan.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/load.html` | health:weight | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/resistance.html` | health:体重,身高 | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/weight-capacity-training.html` | health:weight | tool-ux 自动回填 + ToolKit 历史 |
| `fitness/zuidasheyanglianggusuan.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |

#### health（7 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `health/body-fat-calculator.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `health/body-surface-area.html` | health:height,weight | tool-ux 自动回填 + ToolKit 历史 |
| `health/calc-1.html` | health:weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `health/calorie-needs.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `health/child-height-predictor.html` | health:身高 | tool-ux 自动回填 + ToolKit 历史 |
| `health/ibw-calculator.html` | health:height | tool-ux 自动回填 + ToolKit 历史 |
| `health/vo2-max-calculator.html` | health:bmi | tool-ux 自动回填 + ToolKit 历史 |

#### sports（6 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `sports/estimate-22.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |
| `sports/heart-rate-3.html` | health:心率 | tool-ux 自动回填 + ToolKit 历史 |
| `sports/ratio-18.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |
| `sports/rehab-motion.html` | health:体重 | tool-ux 自动回填 + ToolKit 历史 |
| `sports/xuerusuanyuzhiceding.html` | health:心率 | tool-ux 自动回填 + ToolKit 历史 |
| `sports/yangmaiboxiaolv.html` | health:weight,体重,心率 | tool-ux 自动回填 + ToolKit 历史 |

#### finance（4 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `finance/mortgage-calculator.html` | finance:downpayment,loanamount | tool-ux 自动回填 + ToolKit 历史 |
| `finance/payroll-calculator.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `finance/salary-calculator.html` | finance:salary | tool-ux 自动回填 + ToolKit 历史 |
| `finance/tax-calculator.html` | finance:salary | tool-ux 自动回填 + ToolKit 历史 |

#### medical（3 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `medical/calc-34.html` | health:height,weight | tool-ux 自动回填 + ToolKit 历史 |
| `medical/calculator-calc-2.html` | health:weight,体重 | tool-ux 自动回填 + ToolKit 历史 |
| `medical/estimate-metabolism.html` | health:height,weight | tool-ux 自动回填 + ToolKit 历史 |

#### rehabilitation（3 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `rehabilitation/respiratory-training.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `rehabilitation/walker-height.html` | health:height | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `rehabilitation/wheelchair-posture.html` | health:weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### healthcare（2 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `healthcare/bmi-calculator.html` | health:height,weight,体重 | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `healthcare/tdee-calculator.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### legal（2 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `legal/estimate-salary.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `legal/labor-compensation.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### nephrology（2 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `nephrology/jixingshensunshang-kdigo-fenqi.html` | health:weight | tool-ux 自动回填 + ToolKit 历史 |
| `nephrology/manager-1.html` | identity:patientname | 自定义键 + ToolKit 历史 + data-no-persist |

#### nutrition（2 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `nutrition/calc-1.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `nutrition/calc-60.html` | health:height,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### startup（2 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `startup/burn-rate.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `startup/calc-1.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### tcm-diagnosis（2 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `tcm-diagnosis/disease-tracking.html` | health:症状 | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |
| `tcm-diagnosis/tcm-medical-record.html` | identity:姓名,患者姓名; health:allergy,diagnosis,病史,过敏史 | 自定义键 + ToolKit 历史 + data-no-persist |

#### cardiology（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `cardiology/calc-3.html` | health:history,weight | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### cleaning（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `cleaning/staff-schedule.html` | identity:姓名 | 自定义键 + ToolKit 历史 + data-no-persist |

#### clinical-nursing（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `clinical-nursing/cycle-7.html` | identity:患者标识(动态输入) | 自定义键 + data-no-persist |

#### dermatology（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `dermatology/calc-1.html` | health:weight,体重 | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### hr（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `hr/social-insurance.html` | finance:salary | tool-ux 自动回填 + ToolKit 历史 |

#### life（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `life/bill-splitter.html` | identity:姓名 | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### property（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `property/cycle-elevator.html` | identity:姓名 | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### safety（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `safety/reminder-cycle-protection.html` | identity:姓名,工号 | 自定义键 + ToolKit 历史 + data-no-persist |

#### sales（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `sales/commission-calculator.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

#### security（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `security/emergency-contacts.html` | identity:电话号码; health:用药 | 自定义键 + ToolKit 历史 + data-no-persist |

#### tax（1 页）

| 页面 | 敏感字段 | 落盘方式 |
|---|---|---|
| `tax/calc-8.html` | finance:salary | tool-ux 自动回填 + 自定义键 + ToolKit 历史 |

## 5. 敏感字段与导出夹带核查

### 5.1 一键清除覆盖

61 页高风险页均具备清除入口：

- `tool-ux 自动回填` 页由全站浮动的「清空本地数据」入口统一覆盖（`js/tool-ux.js` 的 `tb_ux_*` / `tb_uxp_*` 前缀清理）；
- `自定义键` 页均有页面内「清空 / 清除 / 重置」按钮；
- 已标 `data-no-persist` 的 6 页关闭了自动回填，仅保留用户主动点击的显式保存。

### 5.2 JSON / CSV 导出是否夹带未明示字段

抽样核对 5 类代表页：

| 页面 | 导出内容 | 与页面显示对比 | 结论 |
|---|---|---|---|
| `life/bill-splitter.html` | 姓名、份数、应付 | 与表格列一致 | 无夹带 |
| `property/cycle-elevator.html` | 楼栋、电梯编号、型号、安装日期、类型、日期、维保人员、问题、部件 | 与表格列一致 | 无夹带 |
| `clinical-nursing/cycle-7.html` | 患者、约束类型、时间、皮肤评估、备注 | 与表格列一致 | 无夹带 |
| `clinical-nursing/reminder-time-1.html` | 部位、类型、时长、时间、备注 | 与表格列一致 | 无夹带（不含患者标识） |
| `fitness/training-volume.html` | 动作、组数、次数、重量 | 与表格列一致 | 无夹带 |

补充结论：

- `js/tool-kit.js` **没有**通用「导出全部历史」入口；导出数据一律由页面自己组装，不存在共享层隐式把 `tbk_hist_*` 全量写出的路径。
- 导出中的姓名 / 患者标识 / 工号本身就是页面已展示的业务数据，且由用户主动点击导出；**未发现**「页面未展示、但导出文件里出现」的字段。
- 需要提醒的产品决策：`clinical-nursing/cycle-7` 与 `tcm-diagnosis/tcm-medical-record` 的导出文件含患者标识，属于高敏业务数据；是否默认脱敏由业务方决定（本批不动）。

## 6. 已修项与自证

| 修复 | 文件 | 自证 |
|---|---|---|
| 生成密码不再落盘 | `tools/it/password-generator.html` | ① 静态：`grep sessionStorage` = 0；② 运行时 jsdom：调用 `addToHistory('TEST-PWD-123')` 后历史正常渲染，`localStorage` / `sessionStorage` 中均搜不到该密码；③ 内联脚本语法检查通过。 |
| JWT 历史不再落盘 | `tools/it/jwt-debugger.html` | ① 静态：`HISTORY_KEY` / `jwt_debugger_history` / `localStorage` 引用 = 0；② 历史读写改走 `jwtHistory` 内存数组；③ 内联脚本语法检查通过。 |
| `calorie_history` 拆键 | `tools/health/calorie-needs.html`、`tools/life/daily-calorie-needs.html` | 全站 `grep 'calorie_history'` 只剩 `calorie_history:health` / `calorie_history:life` 各一处。 |
| `currency_history` 拆键 | `tools/finance/currency-converter.html`、`tools/travel/currency-cheat-sheet.html` | 全站 `grep 'currency_history'` 只剩 `:finance` / `:travel` 各一处。 |
| 审计脚本 | `scripts/audit_local_storage.py`（新增） | 复跑输出：Tier1 60 / Tier2 1091 / Tier3 322 / 无存储 6858；Cookie 0 / IndexedDB 0 / 明文凭证 0 / 跨页键冲突 0。`--check` 正常 exit 0，注入 Cookie 写入后 exit 1。 |

涉及页面的回归门禁：`verify_it_calc` 987/987、`verify_health_calc` 81/81、`verify_life_calc` 322/322、`verify_finance_calc` 346/346、`verify_travel_calc` 31/31、`_test_static.py` 0 失败 0 告警。

> 说明：两处拆键后，用户旧键下的历史不会自动迁移（旧数据被自然弃用）。这是有意的：避免旧键继续被两个页面交叉读取；历史本身是低价值中间态。

## 7. 登记待改（本批不做批量文案）

1. **高敏页缺少显式「仅本机 / 可清除」提示**：61 页高风险页目前依赖全站隐私声明与浮动清除入口，页面内没有逐页提示。按用户要求**先出清单，不批量改文案**；清单见 §4。
2. **弱加密存储**：`security/virtual-safe.html`（哈希+盐）与 `safety/manager.html`（XOR）建议后续统一换 WebCrypto AES-GCM；不属「明文凭证」，未在本次强改。
3. **`clinical-nursing/cycle-7` 患者标识导出**：是否默认脱敏需业务确认。
4. **动态生成的 PII 输入**：静态扫描只能解析 HTML 里的 `input`；由 JS 动态插入的患者/客户表单（如 `cycle-7`）需人工补录。已在清单中补 1 页，后续新增此类页面应同步补审计脚本的识别规则。

## 8. 复跑与局限

```bash
python3 scripts/audit_local_storage.py --check    # 有违规/0 页面 → exit 1；当前 exit 0
python3 scripts/audit_local_storage.py --json /tmp/ls.json   # 明细
```

`--check` 已做两向自证：正常全站 exit 0；临时注入一个 `document.cookie = 'x=1'` 的探针页后 exit 1（探针已删除）。

局限：

- 纯静态解析：无法还原「运行时才拼出的键名」与「JS 动态插入的输入控件」；已通过人工抽查补齐已知漏项。
- 敏感判定基于字段名/标签/页面上下文，不做自然语言理解；泛化英文词已做语义域门控，仍建议对 §4 清单做产品复核。
- 不检查第三方脚本自身写入（本站除固定统计入口外无第三方写 storage；统计脚本见 `js/analytics.js` / `js/metrics.js`，仅写匿名事件）。
