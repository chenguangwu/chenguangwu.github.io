#!/usr/bin/env python3
# 探测 P4 清 score 壳时可能漏掉的"平均/评分壳"变体：
# calc 里 score/avg/result/mean 是对输入变量(p0,p1,...或a,b,c)的简单平均或求和，
# 无 Math.*、无循环、无数字系数(排除真公式)、无函数调用；标题不含合法平均/评分词。
import os, re, json
TOOLS="tools"
REDIRECT=re.compile(r"TOOLBOX-REDIRECT")
MATH=re.compile(r'Math\.[A-Za-z]+')
LOOP=re.compile(r'\b(for|while)\s*\(')
NUMCOEF=re.compile(r'\d+(?:\.\d+)?\s*[*+\-/]\s*[A-Za-z_$]|[A-Za-z_$][\w$]*\s*[*+\-/]\s*\d+(?:\.\d+)?')
# 合法标题词（这些是真实的平均/评分/求和工具，不算壳）
LEGIT=re.compile(r'(平均|均值|均分|平均分|评分|打分|总分|加权|合计|总计|求和|累加|累计|分数|成绩|量表|得分|评级|评价|指数|综合|混合|合并|汇总|统计)')

def extract_calc(h):
    starts=[m.start() for m in re.finditer(r'function\s+calc\s*\(',h)]
    if not starts:
        m2=re.search(r'(?:const|let|var)\s+calc\s*=\s*(?:function\s*)?\(',h)
        if m2: starts=[m2.start()]
    out=[]
    for s in starts:
        i=h.find('{',s)
        if i<0: continue
        depth=0;j=i
        while j<len(h):
            if h[j]=='{':depth+=1
            elif h[j]=='}':
                depth-=1
                if depth==0: break
            j+=1
        out.append(h[s:j+1])
    return out

# 平均壳指纹：(var+var+...)/N 或 var+var+.../N，变量是 p\d 或 a/b/c 短名
AVG=re.compile(r'\(?\s*(?:[pa][\w$]*|avg|sum|total)\s*(?:\s*[+\-]\s*(?:[pa][\w$]*|avg|sum|total)){1,}\s*\)?\s*/\s*\d+')
SUMASSIGN=re.compile(r'(?:score|avg|result|mean|average|total|sum)\s*=\s*\(?\s*(?:[pa][\w$]*)\s*(?:\s*[+\-]\s*(?:[pa][\w$]*)){1,}\s*\)?')

def is_avg_shell(calcs, title):
    if LEGIT.search(title): return False
    for c in calcs:
        if MATH.search(c): return False
        if LOOP.search(c): return False
        if NUMCOEF.search(c): return False
        if AVG.search(c) or SUMASSIGN.search(c):
            # 确认等号左侧是 score/avg/result 等聚合名
            m=re.search(r'(score|avg|result|mean|average|total|sum)\s*=\s*', c, re.I)
            if m: return True
    return False

d=json.load(open('json/tools.json'))
items=d if isinstance(d,list) else d.get('tools',[])
hits=[]
for t in items:
    p=os.path.join('tools',t['path']) if not t['path'].startswith('tools/') else t['path']
    if not os.path.exists(p): continue
    h=open(p,encoding='utf-8',errors='ignore').read()
    if REDIRECT.search(h): continue
    calcs=extract_calc(h)
    if not calcs: continue
    m=re.search(r'<title>([^<]*)</title>',h)
    title=m.group(1).replace(' - ToolBox','') if m else '?'
    if is_avg_shell(calcs, title):
        hits.append((t['industry'],t['path'],title))

print(f"平均/评分壳残留命中: {len(hits)}")
for ind,p,title in hits[:40]:
    print(f"  {ind:14s} {title:30s}  {p}")
with open('scripts/_avg_shell.json','w') as f:
    json.dump([{"industry":i,"path":p,"title":t} for i,p,t in hits],f,ensure_ascii=False,indent=1)
print(f"\n已写出 scripts/_avg_shell.json")
