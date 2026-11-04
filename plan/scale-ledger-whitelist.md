# 量表总账白名单（无法机械核对上限的页面）

> 由 `scripts/audit_scale_ledger.py` 生成口径分类后人工复核。  
> 收录口径：页面含 `refBar` 或「满分」字样、但静态求和规则无法可靠还原总分上限的 27 页（119 页中的剩余部分）。  
> 维护规则：新增同类页面先跑脚本；落入下列口径的，在此登记并人工核一次，不得默认「脚本已覆盖」。

## 一、口径分类与机械覆盖

| 口径 | 页面数 | 处理方式 |
|---|---|---|
| 逐项求和（静态 select / `o:[…]` / `opts:[{v}]` / radio 组 / 构造式声明 / score-pts / number max / ×2 加权项） | 92 | 已机械化，脚本自动比对满分与切点 |
| 加权表（区域权重 × 严重度 × 面积，或条目权重表） | 17 | 白名单（本文件） |
| 动态/分支（行数或满分随年龄、性别、病程变化） | 3 | 白名单 |
| 同页多量表（ACT + GINA 分级等） | 2 | 白名单 |
| 成分计分（PSQI 等由 C1–C7 成分合成） | 1 | 白名单 |
| 序数量表（EDSS 等 0.5 步进） | 1 | 白名单 |
| radio 动态生成（静态 HTML 不含选项） | 2 | 白名单 |
| 结果非满分制（均分 / 标准化 0–100 / 阳性项计数 / 指数） | 1（BASDAI 归入加权类，人工判定） | 白名单 |

机械判定新增规则（本批）：
- `radio` 组按 `name` 分组取组内最大 value 再求和（HAS-BLED 等；同页 checkbox 按 `.checked?1:0` 计 1 分）。
- 模板串 + `questions` 数组：`<select id="q${i}">` × 题数 × `opts` 真实分值（PHQ-9、IPSS 等）。
- 构造式声明：`N 项（每项 0–M）`、`A 项+B 项+C 项之和（每项 0–M）`、`N 项×1–M`、`权重合计 W × 程度 0–M`。
- `o:[…]` 数组：有配套 `v:[…]` 用真实分值，否则按下标（最大 = 元素数 − 1）。

## 二、白名单（27 页，人工核对记录）

| 页面 | 口径 | 页面自述 | 人工核对结论 |
|---|---|---|---|
| neurology/edss.html | 序数 | 0–10（0.5 步进） | 原版 EDSS 为序数刻度，非逐项求和；脚本跳过合理 |
| neurology/psqi.html | 成分 | 7 成分合计 21 | C1–C7 各 0–3，满分 21 ✔（C5 已按原版 9 项合计映射） |
| neurology/phq9-stroke.html | 动态 radio | 9 题 0–3 = 27 | 动态生成 radio，静态不可还原；按题数×上限=27 ✔ |
| neurology/rls-severity.html | 动态 radio | 10 题 0–4 = 40 | 同上，10×4=40 ✔ |
| psychiatry/les-stress.html | 加权 | 未声明满分 | LES 为加权生活事件量表，无固定满分，跳过合理 |
| psychiatry/rater-23.html | 动态 | LSAS 24 项 | 24 项（恐惧/回避各 0–3）上限 144；`refBar` 顶档 105+ 为页面自述分档 |
| psychiatry/self-assess-4.html | 结果非满分制 | 阳性项数 | 输出阳性条目计数而非分值总和，不适用满分比对 |
| rheumatology/assessor-10.html | 加权/动态 | 未声明满分 | DAS28 类复合指数，非简单求和 |
| rheumatology/basdai.html | 结果非满分制 | 0–10 均分 | 6 项 0–10，取前 4 项 + 后 2 项均值再除以 5，结果 0–10 |
| rheumatology/essdai.html | 加权 | 12 个域 | ESSDAI 各域按权重分级（0–3），满分由域权重决定，静态不可还原 |
| rheumatology/guguanjieyan-womac-zhishu.html | 加权/标准化 | 原始 96 → 标准化 0–100 | 原始总分 96 =（5+2+17）×4 ✔；页面输出为标准化 0–100 |
| rheumatology/rater-16.html | 加权 | SLEDAI-2K 105 | 24 项按权重计分，原版满分 105 ✔（页面自述一致） |
| pulmonology/gina-asthma.html | 同页多量表 | ACT 25 / 分级 | ACT 5 题×5=25 ✔，另有 GINA 控制分级，非单一满分 |
| dentistry/rater-risk-2.html | 动态 | 7 项 0–2 = 14 | 7×2=14 ✔（页面自述一致） |
| cardiology/coronary-calcium.html | 加权 | Agatston 指数 | 输出钙化积分（无上限），不适用满分比对 |
| rehabilitation/fim-scale.html | 加权/动态 | 18 项 1–7 = 126 | 18×7=126 ✔（页面自述一致） |
| dermatology/calc-1.html | 加权 | 未声明满分 | 皮肤病损面积/严重度复合指数，非简单求和 |
| dermatology/dermatoscopy-abcd.html | 加权 | 未声明满分 | ABCD 各项加权，非固定满分 |
| dermatology/easi-eczema.html | 加权 | 72 | 4 区域 × 面积 0–6 × 严重度 0–12 × 权重和 1.0 = 72 ✔ |
| dermatology/gags-acne.html | 加权 | 44 | 已按原版系数实现（前额/双颊 2、鼻/下颌 1、胸部与上背 3，合计 11），满分 4×11 = 44 ✔；此前台账「6×4=24 vs 44」是静态求和未计部位系数导致的**脚本误报**，页面计分本身正确。已补显式系数表（部位 / 系数 / 严重度 / 单部位最高分）与 8 分、44 分两条 verify 用例 |
| dermatology/pasi-score.html | 加权 | 72 | 同 EASI 结构，72 ✔ |
| dermatology/salt-alopecia.html | 加权 | 未声明满分 | SALT 为脱发面积百分比，非分值求和 |
| dermatology/scorad-index.html | 加权 | 未声明满分 | SCORAD = 面积/强度/主观症状加权，非简单求和 |
| dermatology/vasi-vitiligo.html | 加权 | 未声明满分 | VASI 为面积×色素脱失加权，无固定满分 |
| obstetrics/kupperman-score.html | 加权 | 63 | 13 项权重合计 21 × 程度 0–3 = 63 ✔ |
| obstetrics/rater-26.html | 加权 | 未声明满分 | 各症状 × 权重（4/2/1）求和，无固定满分 |
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

## 四、工作区未提交改动（WIP）处置纪律（2026-11-04 起）

> 背景：本仓多个批次共用同一工作区，已多次出现「工作区里的未提交改动其实是别线正在写的 WIP」。

1. **发现不属于自己这批的未提交改动时，不要静默 revert**。先记下：路径、`git diff` 内容摘要、文件 mtime、疑似来源（哪条线 / 哪个批次）。
2. **判断是否可能是别线正在写**：mtime 在近 10 分钟内，或改动主题与在办批次一致 → **只上报、不动**（不改、不 `git checkout`、不 `git add`、不 `git restore --staged` 以外任何操作）。
3. 只有确认是「僵尸遗留 / 与页面实现矛盾」时才处置；处置前先把摘要存档到 `plan/_stash_notes.md`，再决定收编提交或 `git checkout -- <明确路径>`，**禁止批量回退**。
4. **每次回报前**对自己要提交的路径跑 `git status --short`，确认只剩本批改动；提交一律 `git commit -m "..." -- <具体路径>`，提交前 `git diff --cached --name-only` 自查。若误暂存了他人文件，用 `git restore --staged <路径>` **只 unstage，不 checkout**。

