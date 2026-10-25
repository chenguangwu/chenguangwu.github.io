# 移交文档（HANDOFF）· 全站审计任务续作指引

> 写于 2026-10-25 会话 token 收尾时。任务总目标：**所有工具审计一遍，plan/ 只记未修复问题（已修的不写）**。本文件给接手 agent 的完整续作指引；进度总表见 `plan/MASTER.md`。

## 一、当前进度快照

| 批次 | 范围 | 状态 |
|---|---|---|
| 批1-16 | ~60 个主要目录（statistics/math/science/金融6/工程5/健康4/土木化学6/检验生理6/物理地物6/商运6/量表6/专科6/食品农业6/IT媒体6/生活6/声学航空6/产业6/生活商业6） | ✅ 全覆盖（发现的问题已修复并登记） |
| 批17 | machinery/life/biz/fun/automotive/general（212 计算页） | ✅ 已归档（life.md L1 胸罩码 / biz-startup.md Z1 量纲 / machinery M3 死代码） |
| 批18 | realestate/legal/marketing/metalwork/meteorology/energy/optical/fire-rescue/eco（322 计算页） | ✅ 已归档（eco E1 万kWh 量纲 / metalwork 7 对比页功能单薄） |
| 批19 | cosmetic-derm/ophthalmology/encode/metrology/textile/robotics/nuclear/geometry/signal/food-testing/reproductive-medicine/rheumatology（316 计算页） | 🟡 **进行中**：cosmetic-derm+ophthalmology+encode 三目录已读毕（发现 specialties.md C1 游离酸颠倒，已归档）；**metrology 起共 9 目录未读** |
| 批20 | 其余 <25 页小目录 ~90 个（~800 页） | ⚪ 未开始 |

## 二、批19 续作（先做这个）

转储已生成：`/tmp/dump_b19.txt`（3126 行，316 页）。若 /tmp 被清，用文末脚本重新生成。

**已读**：`########## cosmetic-derm`（第2行）→ `########## encode` 段结束（第897行）。这三目录核对结论：cosmetic-derm 除 C1 外全部自洽（SPF=1/(1−uvb/100) ✓、刷酸渗透/微针密度/射频温度模型 ✓）；ophthalmology 全对（IOP-CCT 校正 0.7mmHg/10μm ✓、SRK/T vergence ✓、OSDI=sum×100/(答×4) ✓、内皮 CV ✓）；encode 全对（Base32/Base64/汉明/熵/碰撞公式 ✓）。

**未读**（用 Read 工具分段读，每段 ≤900 行防超限）：
- metrology：第 898–1140 行（bias-absolute 已开头）
- textile：第 1141–1419 行
- robotics：第 1420–1613 行
- nuclear：第 1614–1812 行（此前批1/批7 审过部分核素页，快扫确认即可）
- geometry：第 1813–2035 行
- signal：第 2036–2269 行（S 批公式框对照过，重点看 calc 本身）
- food-testing：第 2270–2525 行
- reproductive-medicine：第 2526–2804 行（医学量表，参照批9 口径逐条核对计分/阈值）
- rheumatology：第 2805–3126 行（SLEDAI 等此前多页已审，快扫）

读完把未修复发现按归属追加进 `plan/categories/**`（归类规则见 MASTER），并更新 MASTER 批19 状态为 ✅。

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

```python
# /tmp/gen_dump.py  用法: python3 /tmp/gen_dump.py > /tmp/dump_bXX.txt
import io, re, os
dirs=['metrology','textile','robotics','nuclear','geometry','signal','food-testing','reproductive-medicine','rheumatology']  # 批19剩余；批20按清单分组替换
def grab(path):
    s=io.open(path,encoding='utf-8').read()
    def body(pat):
        m=re.search(pat,s)
        if not m: return None
        i=s.index('{',m.end()-1); d=0;j=i
        while j<len(s):
            if s[j]=='{':d+=1
            elif s[j]=='}':
                d-=1
                if d==0:break
            j+=1
        return s[m.start():j+1]
    b=body(r'function\s+calcTool\s*\(') or body(r'function\s+calc\s*\(')
    if not b: return None
    lines=[l.strip() for l in b.split('\n') if re.search(r'[*/^]|\bMath\.|toFixed', l)]
    return lines[:11]
for d in dirs:
    base='tools/'+d
    print(f'\n########## {d} ##########')
    for f in sorted(os.listdir(base)):
        if not f.endswith('.html') or f=='index.html': continue
        b=grab(os.path.join(base,f))
        if not b: continue
        print(f'\n=== tools/{d}/{f}')
        for l in b: print('   ',l[:150])
```

未覆盖目录现算命令（批20 用）：
```bash
covered=" statistics math science finance banking investment securities accounting tax mechanical electrical structural hydraulic thermodynamics health healthcare medical fitness civil construction surveying chemical chemistry petrochem clinical-lab cardiology nephrology endocrinology hematology pulmonology psychiatry psychology clinical-nursing pediatrics obstetrics gastroenterology ent dermatology dentistry urology rehabilitation neurology astronomy kinematics materials optics quantum geology maritime transport logistics logistics2 economics insurance edu food baking agriculture livestock fishery it photo video design audio media sports home music wedding office edu2 acoustics dynamics electromagnetism electronics engineering aerospace forestry aquaculture beekeeping glass dyeing ceramics cleaning decor restaurant telecom urban paper machinery life biz fun automotive general realestate legal marketing metalwork meteorology energy optical fire-rescue eco cosmetic-derm ophthalmology encode metrology textile robotics nuclear geometry signal food-testing reproductive-medicine rheumatology "
for d in tools/*/; do n="${d#tools/}"; n="${n%/}"; c=$(ls tools/$n/*.html 2>/dev/null | grep -vc 'index.html'); case "$covered" in *" $n "*) ;; *) echo "$c $n";; esac; done | sort -rn
```

## 六、其他未了事项（非本任务，勿混入）

- 本地提交未推送（收尾时 2 个 + 本批归档若干）；origin 曾被外部推进，恢复时先 `git fetch`。
- G01 裁量项 / G02 存根删除 / G06 留存升级——等老板指令，与审计任务分开。
