# 移交文档（HANDOFF）· 全站审计任务续作指引

> 写于 2026-10-25 会话 token 收尾时。任务总目标：**所有工具审计一遍，plan/ 只记未修复问题（已修的不写）**。本文件给接手 agent 的完整续作指引；进度总表见 `plan/MASTER.md`。

## 一、当前进度快照

| 批次 | 范围 | 状态 |
|---|---|---|
| 批1-16 | ~60 个主要目录（statistics/math/science/金融6/工程5/健康4/土木化学6/检验生理6/物理地物6/商运6/量表6/专科6/食品农业6/IT媒体6/生活6/声学航空6/产业6/生活商业6） | ✅ 全覆盖（发现的问题已修复并登记） |
| 批17 | machinery/life/biz/fun/automotive/general（212 计算页） | ✅ 已归档（life.md L1 胸罩码 / biz-startup.md Z1 量纲 / machinery M3 死代码） |
| 批18 | realestate/legal/marketing/metalwork/meteorology/energy/optical/fire-rescue/eco（322 计算页） | ✅ 已归档（eco E1 万kWh 量纲 / metalwork 7 对比页功能单薄） |
| 批19 | cosmetic-derm/ophthalmology/encode/metrology/textile/robotics/nuclear/geometry/signal/food-testing/reproductive-medicine/rheumatology（316 计算页） | ✅ 全读毕（specialties C1 游离酸颠倒；_others O6 重金属迁移×1000；提交 862d884e54） |
| 批20-A | travel/fluid/ecommerce/acupuncture/tcm-pharmacy/tcm-chemistry/tcm-diagnosis/property/hr/food-processing/data/beauty/metallurgy/forensic-medicine/language/nutrition（16 目录 170 页） | ✅ 全读毕（specialties C2 法医胎龄公式失真；hr-legal L3 年假折算 ceil 口径矛盾；其余公式全核对通过，含 hr 加班 1.5/2/3 倍、food-processing F值/ASLT/过滤/喷雾干燥、metallurgy 杠杆定律/Chvorinov/Arrhenius、nutrition 添加剂量纲正确对照 O6） |

## 二、批20 续作（先做这个）

### 已就绪的转储
`/tmp/dump_b20b.txt`（1098 行）已生成未读：B 组 17 目录（welding/safety/advertising/pet/leather/gardening/image/usedcar/hvac/text/pr/mining/security/gas/fire/elderly/process，249 calc 页 + 91 no-calc 页标记）。若 /tmp 被清，用 §五脚本重新生成（dirs 参数见下行）。

```bash
python3 /tmp/gen_dump.py "welding,safety,advertising,pet,leather,gardening,image,usedcar,hvac,text,pr,mining,security,gas,fire,elderly,process" > /tmp/dump_b20b.txt
```

### B 组之后剩余目录（按 /tmp/rest_dirs.txt）
- **C 组**：`ai`（64 页，浏览器本地 AI 页，多为 module 脚本，dump 可能抓不到 calc，需 grep `<script type="module"` 另行处理）
- **D 组**：sales,procurement,research,rental,quality,museum,library,cognition,woodwork,printing,hotel,dance,admin（13 目录，93 页）
- **E 组**：startup,road,parenting,packaging,jewelry,funeral,floral,film,exhibition,chinese-cook,archaeology,antiques（12 目录，72 页）
- **F 组**：29 个 5 页目录：yi,woodworking,tunnel,stage,shipping,service,seismology,rubber,railway,project,plastic,pets,pet-training,niche,medical2,martial,manufacturing,legal2,kids,gardening2,futures,forex,fengshui,chinese,chess,bridge,bonding,audit,accessibility
- **G 组**：stats,photo2,misc,misc2,express,daily-goods,network（7 目录 17 页；network 0 页仅目录）

### 审读要点（沿用）
1. 双段模板页（第一段死模板 `score=(a+b)/2`）→ 看后段是否领域逻辑；两段都通用 → 记「功能单薄」。
2. 系数量纲错 / 医学量表阈值错是重点；发现后**读原页核实再归档**。
3. 已修不写；归档到 plan/categories/ 对应大分类（映射参考既有条目）。

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
