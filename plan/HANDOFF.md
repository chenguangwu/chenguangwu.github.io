# 移交文档（HANDOFF）· 全站审计任务续作指引

> 写于 2026-10-25 会话 token 收尾时。任务总目标：**所有工具审计一遍，plan/ 只记未修复问题（已修的不写）**。本文件给接手 agent 的完整续作指引；进度总表见 `plan/MASTER.md`。

## 一、当前进度快照

| 批次 | 范围 | 状态 |
|---|---|---|
| 批1-16 | ~60 个主要目录（statistics/math/science/金融6/工程5/健康4/土木化学6/检验生理6/物理地物6/商运6/量表6/专科6/食品农业6/IT媒体6/生活6/声学航空6/产业6/生活商业6） | ✅ 全覆盖（发现的问题已修复并登记） |
| 批17 | machinery/life/biz/fun/automotive/general（212 计算页） | ✅ 已归档（life.md L1 胸罩码 / biz-startup.md Z1 量纲 / machinery M3 死代码） |
| 批18 | realestate/legal/marketing/metalwork/meteorology/energy/optical/fire-rescue/eco（322 计算页） | ✅ 已归档（eco E1 万kWh 量纲 / metalwork 7 对比页功能单薄） |
| 批19 | cosmetic-derm/ophthalmology/encode/metrology/textile/robotics/nuclear/geometry/signal/food-testing/reproductive-medicine/rheumatology（316 计算页） | ✅ 全读毕（specialties C1 游离酸颠倒；_others O6 重金属迁移×1000；提交 862d884e54） |
| 批20 | 其余 95 目录 967 页（A: travel→nutrition 16 目录；B: welding→process 17 目录；C: ai；D+E: sales→antiques 25 目录；F+G: yi→daily-goods 36 目录） | ✅ **全读毕，全站审计闭环**（2026-10-25）。新发现 8 项：specialties C2 法医胎龄公式失真、hr-legal L3 年假折算 ceil 矛盾、_others O7 fire/detector-44 硬编码日期 2026-07-31、life L4 鞋码 US/UK 偏大 8 码、construction-energy E2 桥梁 Pk 内插基线 270 应 180、tax-accounting F1 权益乘数定义错、marketing-sales Z2 利润率/加价率同值、ecommerce-logistics Z3 未达标率标签反。其余目录公式全核对通过（含 ai 全目录 56 calc 页、process 六西格玛全套、forex/futures、medical2 病床统计等） |

## 二、任务状态：全站审计已完成 ✅

批1-20 全部闭环，212 目录 / 5008 页的计算页全数过目。**审计任务移交完毕，后续是两类工作**：

1. **按 plan 修复开发**（高优先级排序建议）：O6 重金属×1000 → C1 游离酸 → C2 法医胎龄 → L4 鞋码 → E1/E2 量纲/标准值 → L3/O7/F1/Z2/Z3 小改。修复时遵守 G03 数据源规则（改 json/i18n 源而非 HTML 直改）与 verify 用例同步。
2. **G06 留存与竞争力升级**（价值核心，「用户看一眼就走」破局）——等老板排期。

附：批 20 期间用的补充提取脚本（ai 目录 `__vN` 表达式专用，§五脚本对 ai 只能抓到取值行）：
```python
# 抓每页 __vN = (...) 或 Math.* 行（跳过 getElementById 取值行），前 8 条
for f in sorted(glob.glob('tools/ai/*.html')):
    ...同 §五 grab()...
    if re.search(r'__v\d+\s*=|Math\.',s) and 'getElementById' not in s: out.append(s)
```

## 三、批20（最后一批）

范围 = 全站 212 目录 − 前批已覆盖（用文末「未覆盖目录清单」命令现算）。约 90 个小目录、~800 页，多为 5–20 页行业。生成 dump 用同一脚本改 dirs 列表（按清单分 2–3 组，每组转储 ≤3500 行）。小目录多为查表/对比/评分页，重点关注：
1. 系数量纲错（同批17/18 套路）
2. 医学小科室量表阈值（refer 批9 口径）
3. `function calc(){...最简比/score=(a+b)/2...}` 双段模板页——**第一段常是被覆盖的死模板，生效版在后段**（realestate/legal 大量如此）；判定方法：grep -c 'function calc(' ==2 则看第二段是否领域逻辑；若第二段也是通用 A/B 比值→记「功能单薄」（参照 metalwork 7 页写法），不是计算错误。

## 四、方法论与坑（必读）

1. **子代理不可用**：Explore/scanner 会撞 `model concurrency limit exceeded`（Flash 额度尽 + 并发限制）。审计全部由主 agent 内联做：生成 calc 摘要转储 → Read 分段读 → 发现问题读原页核实 → 归档。脚本见文末。
2. **已修不写**：plan/ 只记未修复项；每条格式「描述/方案/受影响路径/置信度」。写入前先确认该问题不在已修复清单（MASTER 底部恢复点 + /tmp/bugs_found.txt）。
3. **归档位置**：按 12 大分类目录归属（cosmetic-derm→03-医疗健康/specialties.md 等）；全站性→plan/G0x。
4. **审计完成后**：MASTER 全部批次标 ✅ → 用户目标达成；后续开发另起（G06 留存升级是价值核心）。
5. 双段式页面陷阱、E1 量纲等具体判例见各分类文件内已写条目。

## 五、附：转储生成脚本（复用模板）

`/tmp/gen_dump.py` 已改为 **argv 传目录**（逗号分隔），用法：

```bash
python3 /tmp/gen_dump.py "sales,procurement,research,rental,quality,museum,library,cognition,woodwork,printing,hotel,dance,admin" > /tmp/dump_b20d.txt
```

若 /tmp 被清，脚本内容如下（与上文行为一致：抓每页第一个 `function calcTool(`/`function calc(` 函数体，输出前 11 行含数学行；无 calc 的页打 `[no-calc]` 标记，转储内含页名可直接跳过或按需另行处理）：

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

未覆盖目录现算命令（批20 用）：
```bash
covered=" statistics math science finance banking investment securities accounting tax mechanical electrical structural hydraulic thermodynamics health healthcare medical fitness civil construction surveying chemical chemistry petrochem clinical-lab cardiology nephrology endocrinology hematology pulmonology psychiatry psychology clinical-nursing pediatrics obstetrics gastroenterology ent dermatology dentistry urology rehabilitation neurology astronomy kinematics materials optics quantum geology maritime transport logistics logistics2 economics insurance edu food baking agriculture livestock fishery it photo video design audio media sports home music wedding office edu2 acoustics dynamics electromagnetism electronics engineering aerospace forestry aquaculture beekeeping glass dyeing ceramics cleaning decor restaurant telecom urban paper machinery life biz fun automotive general realestate legal marketing metalwork meteorology energy optical fire-rescue eco cosmetic-derm ophthalmology encode metrology textile robotics nuclear geometry signal food-testing reproductive-medicine rheumatology "
for d in tools/*/; do n="${d#tools/}"; n="${n%/}"; c=$(ls tools/$n/*.html 2>/dev/null | grep -vc 'index.html'); case "$covered" in *" $n "*) ;; *) echo "$c $n";; esac; done | sort -rn
```

## 六、其他未了事项（非本任务，勿混入）

- 本地提交未推送（收尾时 2 个 + 本批归档若干）；origin 曾被外部推进，恢复时先 `git fetch`。
- G01 裁量项 / G02 存根删除 / G06 留存升级——等老板指令，与审计任务分开。
