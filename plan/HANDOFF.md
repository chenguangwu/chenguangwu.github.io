# 移交文档（HANDOFF）· 修复开发阶段交接

> 2026-10-25 全站审计闭环。**审计任务（批1-20，212 目录 / 5008 页）已全部完成**，本文件不再描述审计续作，而是交接下一阶段：**按 plan 清单做修复开发 + G06 留存升级**。进度总表见 `plan/MASTER.md`。

## 一、当前状态快照

- 工作树干净；本地领先 origin **2 个提交**（5df4063c87、f8567af3e3，均为 docs(plan)，不进构建产物）。
- 远端无新推进（fetch --dry-run 为空）。**推送等老板指令**；推送前先 `git fetch`，docs-only 提交推送后无需等 Actions 部署（不影响线上页面字节）。
- 审计期 4 个代码类提交（9fb602145d 等 formula-eq batch40-44）已在远端。

## 二、修复开发任务清单（按优先级，全部为未修复项）

### P0 计算错误——用户会拿到错误数字，优先修

| 问题 | 归档位置 | 要点 |
|---|---|---|
| O6 重金属迁移「食品中含量」虚高 1000 倍 | 12-长尾行业/_others.md | `conc(mg/L)×volume(mL)÷foodVol(mL)` 已是 mg/kg，代码的 `×1000` 多乘；删 ×1000 即可，默认值代入即误判超标 |
| C1 游离酸比例公式颠倒 | 03-医疗健康/specialties.md | 改 `1/(1+10^(pH−pKa))`，与 chemical-peel 对齐（✅ 2026-10-25 已修） |
| C2 法医骨龄胎儿支路胎龄公式失真 | 03-医疗健康/specialties.md | FL 改 0.43×FL+8.5（或分段表）；CRL 改 0.1×CRL+6.5；公式框/注释三处矛盾一并统一（✅ 2026-10-25 已修） |
| L4 鞋码 US/UK 偏大 8 码 | 05-生活消费/life.md | 代码改 `usM=eu−32; usW=eu−30.5; uk=eu−33`（公式框本来是对的）（✅ 2026-10-25 已修） |
| E2 桥梁荷载 Pk 内插基线 270 应 180 | 08-工程制造/construction-energy.md | JTG D60-2015 表 4.3.1-2：L≤5m→180、L≥50m→360（✅ 2026-10-25 已修） |
| Z1 unit-price-compare 固液量纲混用 | 06-商业运营/biz-startup.md | ml/L 与 g/kg 不可直接比单价（✅ 2026-10-25 已修） |
| O1 dyeing/tester-9 输入 C 未参与计算 | 12-长尾行业/_others.md | GB/T 20944.2 口径（✅ 2026-10-25 已修） |
| L1 bra-size 美码=英码且口径粗糙 | 05-生活消费/life.md | ✅ 2026-10-25 已修（EU→US/UK 等效 75→34；US 与 UK 同号，原「US=UK+2」与权威尺码表不符已按标准实现） |
| E1 eco-10/16「万 kWh」量纲口径存疑 | 10-农业养殖/livestock-eco-forestry.md | ✅ 2026-10-25 已修（标「万 kWh」→「MWh（千 kWh）」，数值不动） |

### P1 口径/标签矛盾——数字对但表述误导

- **O7** fire/detector-44 硬编码 `new Date('2026-07-31')` → 改 `new Date()`（_others.md） ✅ 2026-10-25 已修
- **L3** 年假折算 `ceil` 与页面例题/条例矛盾 → 统一 `floor`（06-商业运营/hr-legal.md） ✅ 2026-10-25 已修（半天粒度 `Math.floor(days*2)/2`，与页面例题 3.99→3.5、8.36→8 一致）
- **F1** ratio-analysis 权益乘数误用产权比率定义 → `ta/eq`（02-金融财务/tax-accounting-audit.md） ✅ 2026-10-25 已修（公式框/代码统一为总资产÷股东权益，并列输出产权比率）
- **Z2** cost-price-margin 利润率/加价率同值 → 利润率改 `(p−cost)/p`（marketing-sales.md） ✅ 2026-10-25 已修（两个分支的利润率均改为售价口径，公式框补「输入率为成本加成口径」说明）
- **Z3** stats-on-time-1「未达标率」括注写反（ecommerce-logistics.md） ✅ 2026-10-25 已修（标签改「未同时达标率（迟到或质量不良）」，并集口径，公式框/JSON/verify 同步）
- **H2** insulin-adjustment deep-dive 示例文案错 → 改 `i18n/tools/content_deepdive.json` 源（home-decor.md 备注） ✅ 2026-10-25 已修（补 ÷18：ISF=(1800/36)÷18≈2.78、校正剂量≈2.5U，消除「0.14U/约1.4U」自相矛盾；顺带修 tab-isf 参考表 ISF 列 40/60/80 行误用 2000 法则值）

### P2 待老板裁断后才动（勿自行决定口径）

- **G01** 公式与计算正确性裁量项（M1 量表条目重建、M2 阈值口径、parkland、qtc、EAT-26 等 16 批遗留）
- **L2** labor-compensation 满半年按 1 年 vs 代码 N=0.5（hr-legal.md）

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

- **推送**：本地 2 个 docs 提交待推；推送前 `git fetch`。
- **G01 裁断** / **L2 裁断**（见 P2）。
- **G02 存根**：宠物类 3 个 TOOLBOX-REDIRECT 存根 **2026-11-10 到期**须物理删除并按 §4.6 提死链；到期前主动处理。
- **G06 留存升级排期**——审计后站点质量基础已夯实，这是把「看一眼就走」变成「收藏回头」的主战场。
