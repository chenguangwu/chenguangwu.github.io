# 量表总账白名单（无法机械核对上限的页面）

> 由 `scripts/audit_scale_ledger.py` 生成口径分类后人工复核。  
> 收录口径：页面含 `refBar` 或「满分」字样、但静态求和规则无法可靠还原总分上限的 17 页（119 页中的剩余部分）。  
> 2026-11-04 台账修复后，原 27 页中有 10 页已可机械还原（essdai、assessor-10、womac、rater-16、easi、gags、pasi、kupperman、rater-26、fim），逐页核对见第五节。  
> 维护规则：新增同类页面先跑脚本；落入下列口径的，在此登记并人工核一次，不得默认「脚本已覆盖」。

## 一、口径分类与机械覆盖

| 口径 | 页面数 | 处理方式 |
|---|---|---|
| 逐项求和（静态 select / `o:[…]` / `opts:[{v}]` / radio 组 / 构造式声明 / score-pts / number max / 系数数组 × 单项上限 / 显式系数表 / 域对象 / 症状权重 / 嵌套分组） | 102 | 已机械化，脚本自动比对满分与切点 |
| 加权量表（TBSA / TDS / SALT / VASI / Agatston / LES / BASDAI 等非逐项求和口径） | 7 | 白名单 |
| 复合加权公式（SCORAD = A/5 + 3.5B + C，含归一除法） | 1 | 白名单 |
| 动态/分支（行数或满分随年龄、性别、病程变化） | 3 | 白名单 |
| 同页多量表（ACT + GINA 分级等） | 2 | 白名单 |
| 成分计分（PSQI 等由 C1–C7 成分合成） | 1 | 白名单 |
| 序数量表（EDSS 等 0.5 步进） | 1 | 白名单 |
| radio 动态生成（静态 HTML 不含选项） | 2 | 白名单 |

合计 119 页 = 102 机械覆盖 + 17 白名单。

机械判定新增规则（本批，`audit_scale_ledger.py`）：
- **系数数组**：`(factors|weights|coefs)=[…]` 与静态 select 数量相等且 ≥3 → `Σ(单项上限 × 系数)`（GAGS 6 个 `[2,2,2,1,1,3]` = 44）。
- **显式系数表**：表头含「系数/权重」且为「部位 / 系数 / 严重度」三列 → `Σ(单部位满分 × 系数)`（ESSDAI = 123）。
- **域对象**：`{name,weight,levels:[{v:0}…{v:M}]}` → `Σ(权重 × 本域最高档 v)`。
- **症状对象**：存在 `setSev(` / `data-s="3"` 时，`{name,weight}` → `Σ(权重 × 3)`（Kupperman = 63）。
- **嵌套分组**：`{group,weight,list:[{key:…}]}` → 组内条目数 × 组权重（SLEDAI-2K = 105）。
- **复合除法公式**：`A/5 + …` 形式的归一加权显式跳过，避免把 SCORAD 的静态和 38 误标成「已补解析」。
- **自检**：`python3 scripts/audit_scale_ledger.py --self-test` 断言 GAGS = 44、PHQ-9 = 27。

## 二、白名单（17 页，人工核对记录）

| 页面 | 口径 | 页面自述 | 人工核对结论 |
|---|---|---|---|
| neurology/edss.html | 序数 | 0–10（0.5 步进） | 原版 EDSS 为序数刻度，非逐项求和；脚本跳过合理 |
| neurology/psqi.html | 成分 | 7 成分合计 21 | C1–C7 各 0–3，满分 21 ✔（C5 已按原版 9 项合计映射） |
| neurology/phq9-stroke.html | 动态 radio | 9 题 0–3 = 27 | 动态生成 radio，静态不可还原；按题数×上限=27 ✔ |
| neurology/rls-severity.html | 动态 radio | 10 题 0–4 = 40 | 同上，10×4=40 ✔ |
| psychiatry/les-stress.html | 加权 | 未声明满分 | LES 43 项生活事件按 LCU 权重累加，无固定满分，跳过合理 |
| psychiatry/rater-23.html | 动态 | LSAS 24 项 | 24 项（恐惧/回避各 0–3）上限 144；`refBar` 顶档 105+ 为页面自述分档 |
| psychiatry/self-assess-4.html | 结果非满分制 | 阳性项数 | 输出阳性条目计数而非分值总和，不适用满分比对 |
| rheumatology/basdai.html | 结果非满分制 | 0–10 均分 | 6 项 0–10，取前 4 项 + 后 2 项均值再除以 5，结果 0–10 |
| pulmonology/gina-asthma.html | 同页多量表 | ACT 25 / 分级 | ACT 5 题×5=25 ✔，另有 GINA 控制分级，非单一满分 |
| dentistry/rater-risk-2.html | 动态 | 7 项 0–2 = 14 | 7×2=14 ✔（页面自述一致） |
| cardiology/coronary-calcium.html | 加权 | Agatston 指数 | 输出钙化积分（无上限），不适用满分比对 |
| dermatology/calc-1.html | 加权 | 九分法 TBSA | 头 9 + 双臂 9×2 + 前后躯干 18×2 + 双腿 18×2 + 会阴 1 = 100% ✔ |
| dermatology/dermatoscopy-abcd.html | 加权 | 未声明满分 | TDS = A×1.3 + B×0.1 + C×0.5 + D×0.5；最大 2.6+0.8+3.0+2.5 = 8.9 ✔ |
| dermatology/salt-alopecia.html | 加权 | 0–100% | 0.40/0.24/0.18/0.18 权重和 1.0，满分 100% ✔ |
| dermatology/scorad-index.html | 复合公式 | 未声明满分 | SCORAD = A/5（0–20）+ 7B/2（0–63）+ C（0–20）= 103；静态 select 和 38 不可用，保持跳过 |
| dermatology/vasi-vitiligo.html | 加权 | 未声明满分 | 5 区域 × 手掌单位 × 色素脱失 %，无固定满分 |
| pediatrics/pediatric-asthma.html | 同页多量表 | ACT 25 / TRACK 等 | 同页含多个量表（ACT 25、TRACK 等），非单一满分 |

## 三、反向计分扫描（`scripts/audit_reverse_scoring.py`）

扫描 4705 页中含「反向」字样者，收敛到计分语境 15 页（13 页显式声明反向条目）：

- **11 页已实现翻转**（抽查确认）：`psychology/sas-assessment`（`SAS_REV` 0 基索引 + `5-v`）、`psychiatry/eat26-eating`（`REV_IDX` 权重）、`neurology/aq-autism`（`FWD` 正向/反向表）、`psychology/bigfive-personality-test`（外置脚本 `6-v`）、`psychology/attachment-style-test`（`q.r ? 8-raw : raw`）、`tcm-diagnosis/constitution-test`（`6−raw`）、`design/tester-assessor`（SUS 奇偶 `6-v`）、`research/analysis-47`（`11-g[3]`）、`psychology/self-test-pressure`（`4-v`）等。
- **2 页声明反向但代码无翻转（已定性）**：
  - `psychology/tester-2`：**判定为文案不实，改文案、不补实现**。依据：`MT_QS` 60 条全部以 `d:'E'/'I'/'S'/'N'/'T'/'F'/'J'/'P'` 标示所属极性，每条陈述都直接指向本极（如 E 题「聚会后觉得被充电」、I 题「独处一周末是享受」），计分 `raw[d] += v; raw[MT_PAIR[d]] -= v;` 是二极量表的正负累加，**不存在需要 `max+1-v` 翻转的反向条目**。已删除「含反向题」，改为「成对维度两个方向的陈述混合出现」，并同步 `i18n/tools/psychology.json` 与 `i18n/tools/en/psychology/tester-2.json`；不改计分。
  - `research/analysis-49`：**确认为误报，不改页面**。该页是 Cronbach's α 计算器，「反向」仅出现在示例说明文字（提示条目方向相反时先统一方向），页面本身不是逐题量表、无反向计分实现，不适用「声明反向但未翻转」的判据。

**静态扫描无法判定的一类**：原量表条目为负向措辞（如「我很少感到紧张」）但页面未写「反向」，代码按正向累加。这类需逐题比对原始量表措辞，脚本不做推断。

### 3.1 五个常用量表逐题抽样（2026-11-04，只出结论、不改页面）

| 量表 | 页面 | 逐题比对结论 | 反向条目 |
|---|---|---|---|
| PHQ-9 | `tools/psychiatry/phq9-depression.html`（`QS` 9 条） | 9 条措辞与原版一致：兴趣减退、情绪低落、睡眠、疲乏、食欲、自责/失败感、注意力、精神运动、自伤念头 | 无（全部为症状频率越高分越高） |
| GAD-7 | `tools/psychiatry/gad7-anxiety.html`（`QS` 7 条） | 7 条与原版一致：紧张焦虑、无法控制担忧、担忧过多、难放松、坐立不安、易怒、害怕 | 无（全部正向） |
| PSQI | `tools/neurology/psqi.html`（C1–C7） | C5 取原版 Q5b–Q5j 的 9 个睡眠障碍子项（夜醒、夜尿、呼吸不畅、咳嗽打鼾、太冷、太热、噩梦、疼痛、其他）；原版 Q5a「30 分钟内无法入睡」由独立入睡潜伏期题项覆盖 ⇒ C5 9 项 ×0–3=0–27 映射 0–3 的边界与原版一致。C6/C7 按原版取均值四舍五入 | 无（主观睡眠质量、热情两项靠选项分值顺序编码，非 `max+1-v`） |
| HAMD | **仓库内无页面**（全库 `HAMD|HDRS|汉密尔顿` 零命中） | 无法抽样；如需覆盖须先建页，否则在规划性任务中标注「未覆盖」 | — |
| MMSE | `tools/rehabilitation/mmse-scoring.html`（30 项） | 与原版 11 组一致（定向 10、注册 3、注意/计算 5、回忆 3、语言 9），全部「答对 1 分、答错 0 分」；「回忆皮球（第 1 次注册）」措辞略偏（原版为注册/复述三词），但计分口径一致 | 无 |

**抽样结论**：这 5 个常用量表本身均无反向条目，因此「未声明反向」对它们不构成缺陷；「负向措辞但未声明」的风险主要在其它自评量表，需继续逐页人工抽样。

### 3.2 高频自评量表 Top 10 反向条目逐题比对（2026-11-04，只出结论、不改页面）

挑选口径：覆盖高频标准化自评量表，并纳入已有反向实现的量表验证「声明 = 实现」。PHQ-9 / GAD-7 / PSQI 沿用 3.1 结论。

| 量表 | 页面 | 原版反向条目（英文原文） | 页面声明 | 实现 | 结论 |
|---|---|---|---|---|---|
| PHQ-9 | `psychiatry/phq9-depression.html` | 无反向条目 | 未声明 | 不适用 | 未声明但原版无反向 |
| GAD-7 | `psychiatry/gad7-anxiety.html` | 无反向条目 | 未声明 | 不适用 | 未声明但原版无反向 |
| PSQI | `neurology/psqi.html` | 无反向条目（C1–C7 成分计分） | 未声明 | 不适用 | 未声明但原版无反向 |
| SAS（Zung） | `psychology/sas-assessment.html` | 第 5/9/13/17/19 题为正向措辞，需反向：5 “I feel that everything is all right and nothing bad will happen.”；9 “I feel calm and can sit still easily.”；13 “I can breathe in and out easily.”；17 “My hands are usually dry and warm.”；19 “I fall asleep easily and get a good night's rest.”（Zung 1971） | 显式声明 5/9/13/17/19 反向 | `SAS_REV` 0 基索引 + `5-v` | 声明+实现 |
| SCL-90 | `psychology/scl90-assessment.html` | 无反向条目（90 项均为症状严重度，越高越重） | 未声明 | 不适用 | 未声明但原版无反向 |
| ISI | `psychiatry/isi-insomnia.html` | 无反向条目（7 项均「越重分越高」：入睡困难、维持睡眠困难、早醒、睡眠满意度、他人可见程度、担忧程度、日间功能影响） | 未声明 | 不适用 | 未声明但原版无反向 |
| PSS-10 | `psychology/self-test-pressure.html` | 第 4/5/7/8 题为正向措辞，需反向：4 “felt confident about your ability to handle your personal problems”；5 “felt that things were going your way”；7 “been able to control irritations in your life”；8 “felt that you were on top of things”（Cohen 1983） | 显式声明 4/5/7/8 反向 | `PSS_REV` 0 基 `{3,4,6,7}` + `4-v` | 声明+实现 |
| Big Five（BFI） | `psychology/bigfive-personality-test.html` | 16 道反向键：2 “Tends to find fault with others”；6 “Is reserved”；8 “Can be somewhat careless”；9 “Is relaxed, handles stress well”；12 “Starts quarrels with others”；18 “Tends to be disorganized”；21 “Tends to be quiet”；23 “Tends to be lazy”；24 “Is emotionally stable, not easily upset”；27 “Can be cold and aloof”；31 “Is sometimes shy, inhibited”；34 “Remains calm in tense situations”；35 “Prefers work that is routine”；37 “Is sometimes rude to others”；41 “Has few artistic interests”；43 “Is easily distracted”（John & Srivastava 1999） | 显式声明「反向」标签 | 外置脚本 `if (it.r) v = 6 - v` | 声明+实现 |
| ECR | `psychology/attachment-style-test.html` | 原版回避维度含反向键条目，如 “I am very comfortable being close to romantic partners”；“I find it relatively easy to get close to my partner”；“I feel comfortable depending on romantic partners”；“I tell my partner just about everything”（Brennan 1998）；本页 36 题中 8 道反向（焦虑 13–16、回避 29–32） | 显式声明「含 8 道反向计分题」 | `q.r ? 8 - raw : raw` | 声明+实现 |
| EAT-26 | `psychiatry/eat26-eating.html` | 原版反向键 8 “I feel that others would prefer if I ate more”；13 “Other people think that I am too thin”；26 “I enjoy trying new rich foods”（Garner 1982） | 显式声明「反向条目(8/13/25)」 | `REV_IDX {7,12,24}` 0 基 + `REV/NORM` 权重表 | 声明+实现（注：页面第 25/26 题顺序与原版相反，反向键与页面自身措辞一致，计分不受影响） |

**结论分布**：`声明+实现` 5 条（SAS、PSS-10、Big Five、ECR、EAT-26）；`未声明但原版无反向` 5 条（PHQ-9、GAD-7、PSQI、SCL-90、ISI）；`原版有反向但页面全正向` **0 条（无真缺陷）**。

## 四、工作区未提交改动（WIP）处置纪律（2026-11-04 起）

> 背景：本仓多个批次共用同一工作区，已多次出现「工作区里的未提交改动其实是别线正在写的 WIP」。

1. **发现不属于自己这批的未提交改动时，不要静默 revert**。先记下：路径、`git diff` 内容摘要、文件 mtime、疑似来源（哪条线 / 哪个批次）。
2. **判断是否可能是别线正在写**：mtime 在近 10 分钟内，或改动主题与在办批次一致 → **只上报、不动**（不改、不 `git checkout`、不 `git add`、不 `git restore --staged` 以外任何操作）。
3. 只有确认是「僵尸遗留 / 与页面实现矛盾」时才处置；处置前先把摘要存档到 `plan/_stash_notes.md`，再决定收编提交或 `git checkout -- <明确路径>`，**禁止批量回退**。
4. **每次回报前**对自己要提交的路径跑 `git status --short`，确认只剩本批改动；提交一律 `git commit -m "..." -- <具体路径>`，提交前 `git diff --cached --name-only` 自查。若误暂存了他人文件，用 `git restore --staged <路径>` **只 unstage，不 checkout**。

## 五、17 页加权表逐页系数核对（2026-11-04）

口径：`部位/条目 → 系数 → 单部位满分`；合计满分 = `Σ(单部位满分 × 系数)`。状态：已核 / 待核 / 无原版满分。只核对，不改页面；本批仅 ESSDAI、assessor-10 发现真实系数错并已修（同批改 verify）。

| 页面 | 部位/条目 → 系数 → 单部位满分 | 合计满分 | 原版出处 | 状态 |
|---|---|---|---|---|
| dermatology/gags-acne.html | 前额/右颊/左颊 → 2 → 8；鼻/下颌 → 1 → 4；胸+上背 → 3 → 12（严重度 0–4） | 44 | Doshi et al. 1997, Int J Dermatol（GAGS） | 已核 |
| dermatology/easi-eczema.html | 头 → 0.1 → 7.2；躯干 → 0.3 → 21.6；上肢 → 0.2 → 14.4；下肢 → 0.4 → 28.8（每区面积 0–6 + 4 项强度 0–3，未加权单区 72） | 72 | Hanifin et al. 2001, J Am Acad Dermatol（EASI） | 已核 |
| dermatology/pasi-score.html | 头 → 0.1 → 7.2；躯干 → 0.3 → 21.6；上肢 → 0.2 → 14.4；下肢 → 0.4 → 28.8（每区 E/I/D 0–4 + 面积 0–6，未加权单区 72） | 72 | Fredriksson & Pettersson 1978, Dermatologica（PASI） | 已核 |
| rheumatology/rater-16.html | 8 分组 8 项 ×8 = 64；4 分组 6 项 ×4 = 24；2 分组 7 项 ×2 = 14；1 分组 3 项 ×1 = 3 | 105 | Bombardier et al. 1992, Arthritis Rheum（SLEDAI；SLEDAI-2K Gladman 2002） | 已核 |
| obstetrics/kupperman-score.html | 13 项权重：潮热 4；感觉异常/失眠/易激动/泌尿/性生活各 2；抑郁疑心/眩晕/疲乏/骨关节痛/头痛/心悸/蚁走感各 1；每项 × 程度 0–3 → 12/6/6/6/6/6/3×7 | 63（权重和 21 × 3） | Kupperman et al. 1953, J Clin Endocrinol Metab（国内改良 13 项） | 已核 |
| obstetrics/rater-26.html | 11 项权重 `[4,2,2,2,1,1,1,1,1,1,1]`，每项 × 程度 0–3 → 12/6/6/6/3×7 | 51（权重和 17 × 3） | Kupperman et al. 1953（原版 11 项） | 已核 |
| rheumatology/essdai.html | 12 域权重 `[3,4,2,2,3,5,5,6,5,5,2,1]`；单域满分 = 权重 × 最高档（全身/腺体/生化 2 档，其余 3 档）→ 6/12/4/6/9/15/15/18/15/15/6/2 | 123 | Seror et al. 2010/2015, Ann Rheum Dis（EULAR ESSDAI） | 已核（已修：原权重 3/4/2/3/3/6/4/3/3/5/2/3 + 三域 3 档 → 129/96；现 123，并修 5 分切点） |
| rheumatology/assessor-10.html | 同 ESSDAI 12 域权重与单域满分 | 123 | 同 ESSDAI | 已核（已修：同 ESSDAI；另修 5 分切点与 refBar 0–5/5–14） |
| rheumatology/guguanjieyan-womac-zhishu.html | 疼痛 5 项 + 僵硬 2 项 + 功能 17 项 = 24 项 × 0–4 → 每项 4 | 96（原始分；标准分 0–100） | Bellamy et al. 1988, J Rheumatol（WOMAC） | 已核 |
| rehabilitation/fim-scale.html | 18 项（13 运动 + 5 认知）× 1–7 → 每项 7 | 126（最低 18） | Keith et al. 1987, Am J Phys Med Rehabil（FIM） | 已核 |
| cardiology/coronary-calcium.html | Agatston：面积 × 密度系数 1–4 | 无固定上限 | Agatston et al. 1990, J Am Coll Cardiol | 无原版满分 |
| dermatology/calc-1.html | 头 9；双臂 9/9；前后躯干 18/18；双腿 18/18；会阴 1 | 100% | Wallace 九分法 / 中国九分法 | 已核（TBSA 百分比） |
| dermatology/dermatoscopy-abcd.html | A ×1.3 → 2.6；B ×0.1 → 0.8；C ×0.5 → 3.0；D ×0.5 → 2.5 | 8.9 | Stolz et al. 1989 / Nachbar et al. 1994（TDS） | 已核 |
| dermatology/salt-alopecia.html | 顶 0.40 → 40；后 0.24 → 24；右 0.18 → 18；左 0.18 → 18（各 0–100%） | 100% | Olsen et al. 2004, J Am Acad Dermatol（SALT） | 已核 |
| dermatology/scorad-index.html | A/5 → 0–20；7B/2 → 0–63；C → 0–20 | 103 | European Task Force on Atopic Dermatitis 1993, Dermatology（SCORAD） | 已核（复合除法公式，脚本保持跳过） |
| dermatology/vasi-vitiligo.html | 5 区域 × 手掌单位 × 色素脱失 % | 无固定上限 | Hamzavi et al. 2004, J Am Acad Dermatol（VASI） | 无原版满分 |
| psychiatry/les-stress.html | 43 项生活事件 → LCU 权重累加（各项权重不同） | 无固定满分（全选 = ΣLCU） | Holmes & Rahe 1967, J Psychosom Res（LES） | 无固定满分 |

**核对结论**：17 页中 14 页「已核」、3 页「无原版满分/无固定上限」（Agatston 指数、VASI、LES LCU 累加）。真实系数错 2 页（ESSDAI、assessor-10），已改页面并同批更新 `scripts/verify_rheumatology_calc.js`（28/28 通过）。

## 六、教育 / 心理 / 认知 / 护理评分族三维核对（2026-11-05）

口径：① 量表满分 / 项数 / 权重 / 切点；② 反向计分（声明 vs 实现）；③ 学业评分（GPA / 加权 / 标准分）；④ `selectedIndex` 当分值。

机械覆盖：`python3 scripts/audit_scale_ledger.py edu edu2 psychology cognition clinical-nursing`。台账命中 2 页，经人工核对**均为台账误判**（符合「先怀疑台账」的历史经验）：`psychology/calc-self-assess` 的 6 题 1–5 制上限 30 被按静态 select 上限 4 误读为 24；`psychology/self-assess` 的「维度满分 16」是页面旧文案，总分上限 100 本身正确。修复后复跑台账 **0 偏差**。`selectedIndex` 在四个目录零命中（第 ④ 类无样本）。

覆盖：**42 页**（教育 12、心理 14、认知 8、护理评分 8）。判定：**真缺陷 8 条**（已改页面并同批更新 verify）；**登记不改 13 条**（无权威依据 / 版本差异 / 自建量表）。另有 3 个类型归类页（`bubble-tea-personality-quiz`、`tester-2`、`tester-3`）沿用前批结论，不计入本批页数。

### 6.1 真缺陷（已修）

| 页面 | 指标 | 修前页面取值 | 权威取值 / 依据 | 修法 |
|---|---|---|---|---|
| `clinical-nursing/morse-score.html` | 高度风险切点 | 25–50 低危、≥51 高危 | **≥45 高危、25–44 低危**（Morse 1989；页面自身 ref-cite 与深读段亦写 ≥45） | refBar 与 3 处 classify 改为 25/45；补 verify「45 分」用例 |
| `clinical-nursing/braden-score.html` | 中文备注方向 | 「≥9 为极高危」 | **≤9**（Braden 原版；同页英文为 9 or below） | `data-zh` 改「≤9」 |
| `psychology/self-assess.html` | 维度满分 / 总分区间 | 每题 0~4、维度满分 16、合计 0–100 | **每题 1–5、维度满分 20、合计 20–100**（同页代码 `ans+1` 与 `dim.s/20`） | 文案改为 1–5 / 20 / 20–100 |
| `psychology/calc-self-assess.html` | 满分 / 题目构成 / 反向题数 | 总分 0–30、FAQ 0~24；宣称 3 乐观 + 3 悲观，实际 4 乐观 + 2 悲观且 2 道 filler 计入 | **LOT-R 6 个计分项 = 3 乐观 + 3 悲观、3 道反向；1–5 制总分 6–30**（Scheier, Carver & Bridges 1994） | 用原版缺失的 2 个计分项替换 filler；`LR_REV` 改 `{1,2,5}`；文案改 6–30；verify 20→18 |
| `psychology/scl90-assessment.html` | 计分制 / 总分 / 阳性项 | 深读段写 0–4、0–360、阳性≥1 | **1–5、90–450、阳性≥2；PSDI=(总分−90)/阳性数**（页面自身实现与公式段） | 改深读段（HTML + `content_deepdive.json` + en 字典） |
| `psychology/calc-12.html` | 分级阈值文案 | 60 中等 / 70+ 良好 / 80+ 较高 | **31–50 偏下、51–70 中等、71–85 较高、≥86 很高（≤30 偏低）**（同页代码） | info-box 对齐代码 |
| `edu/calc-4.html` | 深读算例 | (85−70×0.4)/0.6 = **91.7** | **95.0**（node 实算：57 ÷ 0.6） | 改 95.0 |
| `edu/gpa-calculator.html` | 4.0 制 C− 文案 | C− = 1.5 | **C− = 1.7**（同页 `gradeSystems` 4.0 表 65–67 → 1.7） | 改 1.7 |

反向计分复核：SAS（5 题 `5-v`）、PSS-10（4 题 `4-v`）、Big Five（`6-v`）、ECR（`8-raw`）、EAT-26（前批）均**声明 + 实现一致**；PHQ-9 / GAD-7 / PSQI / SCL-90 / ISI 原版无反向条目。本批新增确认 `calc-self-assess` 的反向题数声明与实现不一致（已修，见上表）。

### 6.2 登记不改（13 条）

| 页面 | 项 | 处置理由 |
|---|---|---|
| `edu/exam-gpa-calculator.html` | 4.0 制「D (60)」与「D+ (60–63)」标签在 60 分重叠 | 各校 GPA 换算不统一，无单一权威；仅标签提示、不参与自动换算 |
| `edu/exam-score-calculator.html` | 64–67 → 1.5（与 `exam-gpa` 的 1.7 不同） | 两套常见院校口径并存，无官方统一表；不改数字 |
| `edu2/exam-analysis.html` | 标准差按总体口径（÷n） | 页面未声明样本/总体；班级成绩描述性统计用总体口径合理，无权威强制 |
| `edu/assessor-27.html` | 6 维 0–10 自评 → 5 级 | 自建量表，等级线无外部权威 |
| `clinical-nursing/barthel-index.html` | 75/50/25 分级 | 国内常见版本之一（另有 61/41/21 版本）；满分 100 与 10 项权重已核正确 |
| `clinical-nursing/assessor-rater-risk.html` | 25–44 标「中风险」 | 数值 ≥45 / 25 与 Morse 原版一致，仅中文命名与 low risk 不同；无统一译名 |
| `clinical-nursing/assessor-pressure-risk.html` | 手术体位压力风险 6/10 界值 | 自建评分，无权威切点 |
| `clinical-nursing/surgical-position-risk.html` | 高危压力点计数分级 | 自建评分，无权威切点 |
| `cognition/cognitive-assessment.html` | 四层年龄常模 | 页面已声明非标准化常模；`SS=100+15z`、`PR=Φ(z)` 公式与方向处理正确，常模数值无公开出处 |
| `cognition/*` 7 个绩效测试（corsi / digit-span / nback / schulte / stroop / time-perception / human-benchmark） | 原始成绩 | 无临床切点，不属满分制量表 |
| `psychology/psqi-assessment.html`、`psychology/rater.html` | 7 项简版 PSQI，6/11/16 分级 | 页面已明确声明与完整版 7 成分计分不同；完整版无单一分级权威 |
| `psychology/assessor.html` | 拖延自评 10 题 | 自建量表，无权威满分/切点 |
| `psychology/calc-12.html` | 常模 62 分 | 页面自述「约 62 分」，无公开常模出处；仅登记 |

### 6.3 门禁

- fidelity（`TB_STUB_FIDELITY=1 node scripts/discriminate_check.js <file>`）：psychology 11/11、逃生 0；clinical-nursing 42/42、逃生 0；edu 83/83；cognition 13/13；edu2 14/14。
- `selfcheck_false_pass` 的 `all_default`：psychology 0（基线 0）、clinical-nursing 0（基线 0），未上升。
- 「注入失败会变红」：新增 Morse 45 分用例在 fidelity 下为红；初版用高危 desc 会因「NaN 兜底 → 高度风险」逃生，已改锚 `totalNum=45`（默认 0 / NaN 均不含 45）。
- 本轮未执行 `_build.py`、未 push（按工单要求）。

