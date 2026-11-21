# 移交文档（HANDOFF）· 修复开发阶段交接

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

> **2026-11-03 修订**：原「2026-10-25 全站审计闭环」表述已过期——此后仓库又落地 **107 个 `feat(preset)` 提交（S2 场景预设，具体覆盖页数待复核）**，并新增暖通 13 页、删除 pets 6 个到期存根。当前进入「第一轮只读审计续作」，问题按分类与 G01-G09 归档；总进度见 `plan/MASTER.md`。
> 下方「一、当前状态快照」先列 2026-11-03 最新状态，并保留 2026-10-25 历史快照备查（历史条目中的「领先 2 个提交」「待推送」均已不成立）。

## 一、当前状态快照

### 2026-11-03（最新）
- **更正（2026-11-03 后续快照）**：此前 13 个暂存删除及页面/指南改动已进入 `839719048a`；当前 `git status -sb` 显示 plan 文档修改及未跟踪临时文件，本地 `master` 与本地 `origin/master` 跟踪引用无 ahead/behind 标记，未联网核查远端。
- 最近提交：`839719048a`（删除 13 个存根及改写内部链接）、`f4018c71b9`（暖通 13 页预设）、`ea0240209b`（删除 pets 6 存根）。`_tmp_*.mjs` 与 `.trae-html-share-packages/` 当前是未跟踪文件；此前所写 `0340a8718d` 及「临时文件已被该提交加入」缺乏当前仓库证据，撤回。
- **S2 已有多批落地**；此前 3131/753 等扫描数字口径不一致，待重新统计。`encode/convert-4.html` 的英文预设标签含汉字、`general/convert-21.html` 的预设标签重复可由源码核验。
- **G02 存根**：旧快照中存根登记及死链覆盖候选见 G02；文件首次加入日期不能证明存根创建日期，原「约 75 个已超期」结论撤回，须核查存根转换提交。
- 审计口径：只读，不跑 `_build.py` / `run_gates.py`，不执行 git 写操作。

### 2026-10-25（历史，已过期）
- 工作树干净；本地领先 origin **2 个提交**（5df4063c87、f8567af3e3，均为 docs(plan)，不进构建产物）。
- 远端无新推进（fetch --dry-run 为空）。**推送等老板指令**；推送前先 `git fetch`，docs-only 提交推送后无需等 Actions 部署（不影响线上页面字节）。
- 审计期 4 个代码类提交（9fb602145d 等 formula-eq batch40-44）已在远端。

## 二、修复开发任务清单（按优先级，全部为未修复项）

### P0 计算错误——用户会拿到错误数字，优先修

| 问题 | 归档位置 | 要点 |
|---|---|---|
| O6 重金属迁移「食品中含量」虚高 1000 倍 | 12-长尾行业/_others.md | ✅ 2026-11-21 复核：已删除多余 ×1000，公式与量纲一致 |

### P2 专业口径复核记录（已转为边界提示 + 免责，不再作为未完成缺陷）

- **G01** 已改为「公式与计算正确性复核记录」：涉及量表条目重建、阈值口径、parkland、qtc、EAT-26 等专业口径的页面统一补边界提示与免责，不擅自改写临床标准。
- **L2** labor-compensation 满半年按 1 年 vs 代码 N=0.5：页面按「满半年按 0.5 年」并在说明中披露口径，属法定解释差异提示，不再作为代码缺陷。

### P3 功能增强/体验类（非缺陷，配合 G06 排期）

- 各分类文件里的「功能缺陷/优化点」小节（offer 对比器、随访计划生成器、孕周时间轴等）
- **G06 留存与竞争力升级**——「用户看一眼就走」的破局方案，价值核心
- G04 verify 用例债务 / G05 EN 态 i18n / G07 性能移动端，各有独立文件

## 三、修复开发守则（必读，AGENTS.md 之外的经验补充）

1. **G03 数据源规则**：deep-dive/FAQ/intro 被 `_build.py` 从 json/i18n 源重注入——改 HTML 无效会被还原，必须改源（`json/tools.json`、`i18n/tools/<ind>.json`、`i18n/tools/content_deepdive.json`）。formula-eq 公式框可直接改页内（首个 `<p>` 陷阱：说明块用 `<div class="formula-desc">` 不用 `<p>`）。
2. **提交节奏**（老板原话）：一批攒 6–12 个文件再提交，别太碎；「优化任务没有结束的时候，一直干」。
3. **每批收口流程**：改完 → `python3 _build.py`（必须是提交前最后一步）→ `python3 scripts/run_gates.py` 218/218 → sitemap lastmod（`/tmp/sync_lastmod_generic.py`，42 页批次 84/84）→ commit（不 push，等指令）。
4. **verify 用例同步**：修公式后同步 `scripts/verify_*_calc.js` 用例；expect 不能是纯输入回显或分级词锚点；改 `collectStrings` 口径须重跑 `selfcheck_false_pass`/`discriminate_check`。
5. **修复后登记**：按 MASTER 登记纪律「已修不写」——修完把对应 plan 条目**删除**（或整条改为 ✅ 一行），并在 MASTER 分类任务表更新该文件状态；一批修复一个 commit：`fix(calc): 批N 修复 O6/C1/C2/L4 …（逐条核对 JTG/产科/尺码表标准）`。
6. **公式修复的取数纪律**：标准值/系数一律查权威来源（JTG/产科 Hadlock/尺码表/会计准则），不凭印象；deep-dive 算例数字用 node 实跑取值。

## 四、方法论沉淀（未来复扫新工具时复用）

1. **审计法**：dump 每页第一个 `function calcTool(/calc(` 函数体的数学行 → 主 agent 分段读（Read ≤900 行/段）→ 疑点读原页核实 → 归档。脚本见文末。
2. **双段模板页**：`grep -c 'function calc('` ==2 时第一段常是被覆盖的死模板（`score=(a+b)/2`），生效版在后段；两段都通用 → 记「功能单薄」不算计算错误。
3. **三口径核对**：系数与量纲（默认值代入心算复现）、阈值区间、标签与自身文档（公式框/例题/FAQ）是否互相矛盾——批20 的 L3/L4/E2/F1/Z2/Z3 全是「代码 vs 自身文档」矛盾型，说明该口径命中率最高。
4. **常见误报排除**：文档化近似（页内自标"简化估算"）、合法常量日期（专利法 2021-06-01、天文历元）、自带 polyfill 的 Math.erf/erfc、if/else 分支被 dump 压平造成的"连续赋值假象"。
5. 子代理曾撞模型并发限制，审计全程主 agent 内联；若下个会话可用 Explore/scanner 可并行只读检索。

## 五、附：转储生成脚本（argv 传目录，逗号分隔）

`/tmp/gen_dump.py` 若被清，内容如下（抓每页首个 calc 函数体数学行前 11 条；无 calc 打 `[no-calc]`）：

```python
import re,sys,glob
dirs=sys.argv[1].split(',')
def grab(path):
    try: c=open(path,encoding='utf-8').read()
    except: return []
    m=re.search(r'function (calcTool|calc)\s*\(',c)
    if not m: return []
    i=c.index('{',m.end()-1); d=0
    for j in range(i,len(c)):
        if c[j]=='{': d+=1
        elif c[j]=='}':
            d-=1
            if d==0: body=c[i+1:j]; break
    else: return []
    out=[];math=False
    for ln in body.split('\n'):
        s=ln.strip()
        if re.search(r'[+\-*/]=?|Math\.|toFixed|pow|sqrt',s) and not s.startswith('//') and 'innerHTML' not in s[:6]:
            out.append(s[:150]);math=True
        elif math and len(out)>=3: break
        if len(out)>=11: break
    return out
for dd in dirs:
    print('########## '+dd+' ##########')
    for f in sorted(glob.glob('tools/'+dd+'/*.html')):
        r=grab(f)
        if r:
            print('=== '+f)
            for l in r: print('    '+l)
        else:
            print('=== '+f+'  [no-calc]')
```

用法：`python3 /tmp/gen_dump.py "sales,procurement,..." > /tmp/dump_bXX.txt`。
ai 目录页用 `__vN = (表达式)` 模式，上面脚本只能抓到取值行，需改抓 `__v\d+\s*=|Math\.` 且排除 `getElementById`（前 8 条）。

## 六、未了事项（等老板指令）

- **推送**：旧「本地 2 个 docs 提交待推」已过期；当前仅确认本地与 `origin/master` 跟踪引用无 ahead/behind，未联网核对；本审计禁止 git 写操作。
- **G01 裁断** / **L2 裁断**（见 P2）。
- **G02 存根**：pets 6 个在 `ea0240209b` 已删除；线上部署与 IndexNow 提交情况未核实。存根数量和超期日期需稳定快照复核，详见 G02。
- **G06 留存升级排期**：S2 已有多批落地，覆盖统计待复核；S1 金融 validator 专项及 S4–S8 按各专题文件排期。

---

## 七、2026-11-14 会话交接（fix-dev 收尾 · 给后续 agent）

> 本段是**修复开发阶段**（非 11-03 的只读审计态）。本次会话共落地 395–398 四批 + 1 个源同步修复，已全部 push（`3f666c1967..c8f11dcfee`，共 5 个提交），工作树干净。

### 7.1 本会话已落地批次（已全部 push 完成）
| 批号 | 工具 | 修复内容 | commit |
|---|---|---|---|
| 395 | `tools/edu/flag-quiz.html` | C 类「名不副实」：英文简介称 timed quiz、深解承诺错题库，但代码无计时/错题存储 → **实现真实功能**：每题限时10秒+超时判错、localStorage 错题库+只练错题模式；同步三处 meta/原理文案如实 | `58dcc92da3` |
| 396 | `tools/fun/meditation-timer.html` | C 类：meta/深解宣称本地计时与提示音，实际仅静态计划表 → **实现真实倒计时计时器**（时间戳防漂移、段末轻响+结束鸣钟 Web Audio、暂停继续、本次练习留痕） | `0f336791c4` |
| 397 | `tools/fun/tongue-twister.html` | C 类：主描述写「不计时」但深解承诺「跟读计时/performance 计时」自相矛盾 → **实现可选跟读计时器**+统一四处文案为「支持可选本地计时」 | `7e6682a302` |
| 398 | `tools/edu/math-quiz.html` `tools/edu/typing-game.html` | P3 文案对齐（初版误改 HTML，见下注） | `5a4b319957` |
| 398-源同步 | `json/tools.json` `json/industry-edu.json` `i18n/tools/edu.json` `i18n/guides/typing-game-guide.json` `i18n/tools/content_deepdive.json` `i18n/tools/en/edu/typing-game.json` + 重建产物 | **重要**：398 初版直接改 typing-game.html 的 meta/FAQ，但被 `_build.py` 从 i18n/json 源重注入还原（G03 数据源规则）。本提交改**源**消除「错题回看」虚假宣称（typing-game 无错题库功能），FAQ 改为「成绩实时显示，不保存历史记录，不上传」。务必改源而非 HTML。 | `c8f11dcfee` |

四批均 `node --check` 语法通过、JSON-LD 校验合法；395–397 已各自单独跑过全量 `run_gates.py`（264 道全过），398 为纯文案改动并入收尾统一跑。

### 7.2 ⚠️ 关键教训：fake-tools 清单严重滞后，必须「先核验再动手」
- fake-tools 清单（`part-01/02/03.md`）是 **2026-11-04 快照**，而 `audit/interaction-review` 分支已一次性冲刷 **9017 文件（+145100/-100022 行）** 并合并进本地 master。
- 实测：清单中大量标「真」的条目在**当前源码里其实已修好**（capacitor-calculator、child-support、court-fee、salary-after-tax、flow-cytometry-ratio、semen-analysis、gradient、stats-13、calc-angle-slope、generator-laugh、random-training-rhythm、http-cookies、whitespace 等）。照单盲改会重复劳动甚至改坏已修好的页。
- **铁律**：挑清单条目后，**先用 grep 在当前源码核验**「声称缺失的功能是否真的不存在」再动手。核验手段：
  - 计时/音效缺失：`grep -c "setInterval\|AudioContext\|OscillatorNode" 文件`
  - 真实实现 vs 伪实现：`grep -cE "Reed|rsEncode|qrEncode|createOscillator|function detect|号段|区号|lookup|dictionary|词库|质数|阶乘|坡度|atan" 文件`
  - 文案误导：`grep -nE "opt-guide|点击计算|点击生成|Parse and build|错题回看" 文件`
- 不要相信清单的「已确认（真）」标签，信当前源码。

### 7.3 新提速协议（详见 `plan/门禁提速与工作协议.md`）
老板 2026-11-14 明确：**全量门禁太频繁太重，改为每 2–3 小时跑一次，跑通即 push；平时只做轻量校验、多个同类修复合并提交、不频繁 push。**
- 平时：改完用 `node --check`（抽取 inline script）+ `json.loads` 校验 JSON-LD，不跑全量门禁、不 push。
- 攒 3–5 批（或 2–3 小时）跑一次 `env -u NODE_OPTIONS python3 scripts/run_gates.py`；全过即 `git push origin master`，等单次 Actions 查询确认（不轮询）。
- 合并提交：同类修复（如 P3 文案对齐、或同类计时器）一起改一起 commit，每批 6–12 文件。

### 7.4 fake-tools 剩余规模与下一批候选（已 triage）
- 剩余缺陷行：part-01 ≈ 62、part-02 ≈ 23（其中多数为滞后过期项，需核验）、part-03 ≈ 21。
- **真正名不副实 + 改动轻、建议优先**：
  - `tools/it/whitespace.html`：曾被记「压成一行」选项缺失，但审计后疑似已修（需重新 grep 核验）；
  - `tools/museum/index.html`：卡片模板文案（rt-desc/card-desc）疑似套话；
  - `tools/rehabilitation/fim-scale.html` / `tools/life/assessor-target.html`：opt-guide 套话（assessor-target 还含面积 `shopArea` 死输入，动逻辑）；
  - `tools/it/phone-parser.html` / `tools/it/charset-detector.html`：归属地表/编码探测是否真实查表；
  - `tools/edu/anagram-game.html` / `tools/fun/sequence-puzzle.html`：硬编码词库/仅少数序列类。
- **已确认审计修好、清单滞后（不要再改）**：见 7.2 列表。
- **重活（伪二维码需重写编码，不优先排期）**：`tools/it/url-qr.html`、`email-qr.html`、`location-qr.html` 等若被记「伪二维码/占位图」，需真实 Reed-Solomon/BCH 编码，工程量大，建议单独立项。

### 7.5 销账与登记纪律（不变）
- 每批写 `plan/已修复/YYYY-MM-DD-<批号>-<分类>-<主题>.md`（批号继续 399 起）；
- 改源不改 HTML（deep-dive/FAQ/intro 走 `json/tools.json`、`i18n/tools/<ind>.json`、`i18n/tools/content_deepdive.json` 源；formula-eq 公式框可改页内首 `<div class="formula-desc">`）；
- 改完 `python3 _build.py` 是提交前最后一步；收尾统一跑门禁 + push。

### 7.6 收尾状态（已完成）
- 5 个提交已 push：`3f666c1967..c8f11dcfee`；工作树干净。
- Actions run `43577410231`（headSha `c8f11dcfeef`）已触发部署，前序 run 均 success。按协议仅单次查询未轮询。
- 后续 agent 可从本会话的已修复批次（`plan/已修复/2026-11-14-39x-*`）继续，或直接接 7.4 下一批候选。
