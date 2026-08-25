#!/usr/bin/env python3
# 探测"四则运算壳"变体：calc 函数体里存在某对变量(X,Y)，
# 同时出现 X*Y / X+Y / X-Y(或Y-X) / X/Y(或Y/X) 四种基本运算，
# 且不调用 Math.*、无循环、无数字系数乘变量（排除真公式）。
# 这是 P4 清 score 壳、B-OPT15 清 p0*p1 壳时可能漏掉的其他模板变体。
import os, re, json
ROOT="."
TOOLS=os.path.join(ROOT,"tools")
REDIRECT=re.compile(r"TOOLBOX-REDIRECT")

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

BIN=re.compile(r'([A-Za-z_$][\w$]*)\s*([*+\-/])\s*([A-Za-z_$][\w$]*)')
MATH=re.compile(r'Math\.[A-Za-z]+')
LOOP=re.compile(r'\b(for|while)\s*\(')
# 数字系数乘变量（真公式特征），如 1.2*x1 / 0.5*a
NUMCOEF=re.compile(r'\d+(?:\.\d+)?\s*[*+\-/]\s*[A-Za-z_$][\w$]*|[A-Za-z_$][\w$]*\s*[*+\-/]\s*\d+(?:\.\d+)?')

def is_shell(calcs):
    for c in calcs:
        if MATH.search(c): return None
        if LOOP.search(c): return None
        if NUMCOEF.search(c): return None
        ops=[(m.group(1),m.group(3),m.group(2)) for m in BIN.finditer(c)]
        if not ops: return None
        vars_=set(a for a,_,_ in ops)|set(b for _,b,_ in ops)
        for X in vars_:
            for Y in vars_:
                if X==Y: continue
                has_mul=any(((a==X and b==Y) or (a==Y and b==X)) and op=='*' for a,b,op in ops)
                has_add=any(((a==X and b==Y) or (a==Y and b==X)) and op=='+' for a,b,op in ops)
                has_sub=any((a==X and b==Y) and op=='-' for a,b,op in ops) or any((a==Y and b==X) and op=='-' for a,b,op in ops)
                has_div=any((a==X and b==Y) and op=='/' for a,b,op in ops) or any((a==Y and b==X) and op=='/' for a,b,op in ops)
                if has_mul and has_add and has_sub and has_div:
                    return (X,Y)
    return None

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
    pair=is_shell(calcs)
    if pair:
        m=re.search(r'<title>([^<]*)</title>',h)
        title=m.group(1).replace(' - ToolBox','') if m else '?'
        hits.append((t['industry'],t['path'],title,pair))

print(f"四则壳变体命中: {len(hits)}")
# 按质量统计
from collections import Counter
qc=Counter()
paths=[]
for ind,p,title,pair in hits:
    qc[json.load(open('json/tools.json')) and 0]  # placeholder
print("\n抽样（前30）[变量对]:")
for ind,p,title,pair in hits[:30]:
    print(f"  {ind:14s} {title:28s} [{pair}]  {p}")
# 写出全部供后续核查
with open('scripts/_shell_variants.json','w') as f:
    json.dump([{"industry":i,"path":p,"title":t,"pair":list(pr)} for i,p,t,pr in hits],f,ensure_ascii=False,indent=1)
print(f"\n已写出 scripts/_shell_variants.json ({len(hits)} 条)")
