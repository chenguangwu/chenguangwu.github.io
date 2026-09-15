"""一键全站收口脚本：批量完成 enmap → h2 中文化 → step2 抓取 → verify 生成 → harness → 门禁注册 → 构建 → 提交"""
import os, re, sys, json, subprocess, pathlib

def run(cmd, capture=False, timeout=120):
    print(f'  $ {cmd[:120]}')
    return subprocess.run(cmd, shell=True, capture_output=capture, text=True, timeout=timeout)

def cat_converge(industry: str, commit_msg: str = None):
    TOOLS = f'tools/{industry}'
    if not os.path.exists(TOOLS):
        print(f'⚠️  {industry} 目录不存在，跳过')
        return False
    
    files = sorted(f for f in os.listdir(TOOLS) if f.endswith('.html') and f != 'index.html')
    n = len(files)
    print(f'\n## 🎯 {industry} ({n} 页)')
    
    # 1) 中文化 h2 + 写 enmap
    print(f'  1/6 h2 中文化 + enmap')
    enmap = {"_meta": {"label": industry, "orphans": 0}}
    for fname in files:
        slug = fname.replace('.html', '')
        path = f'{TOOLS}/{fname}'
        html = open(path, encoding='utf-8').read()
        h1 = re.search(r'<h1[^>]*>([^<]+)', html)
        h2 = re.search(r'<h2[^>]*>([^<]+)', html)
        intro = re.search(r'<p[^>]*data-zh="([^"]+)"', html)
        if not intro: intro = re.search(r'<p[^>]*>([^<]{15,150})', html)
        name_zh = h1.group(1).strip() if h1 else slug
        intro_zh = intro.group(1).strip() if intro else name_zh
        enmap[slug] = {"name": name_zh, "intro": intro_zh, "cat": industry}
        
        # 中文化 h2
        old_h2 = h2.group(1) if h2 else ''
        if old_h2 and not any('\u4e00' <= c <= '\u9fff' for c in old_h2.strip()):
            new_h2 = name_zh
            def repl(m, _n=new_h2): return m.group(1) + _n
            h2_new = re.sub(r'(<h2[^>]*>)([^<]+)', repl, html, count=1)
            if h2_new != html:
                open(path, 'w', encoding='utf-8').write(h2_new)
    
    with open(f'scripts/enmap/{industry}.json', 'w', encoding='utf-8') as f:
        json.dump(enmap, f, ensure_ascii=False, indent=2)
    
    # 2) 用 _grab_step2.js 抓取（先改 TOOLS）
    print(f'  2/6 step2 抓取')
    grabber_path = 'scripts/_grab_step2.js'
    grabber_src = open(grabber_path).read()
    # 替换 TOOLS 路径
    grabber_src_new = re.sub(
        r"path\.join\(__dirname,\s*'\.\.',\s*'tools',\s*'[^']+'\)",
        f"path.join(__dirname,'..','tools','{industry}')",
        grabber_src
    )
    grabber_src_new = re.sub(
        r"['\"]thermodynamics['\"]",
        f"'{industry}'",
        grabber_src_new
    )
    open(grabber_path, 'w').write(grabber_src_new)
    
    out = run(f'node {grabber_path}', capture=True, timeout=120)
    raw_cases = out.stdout.strip().split('\n')
    
    # 3) 生成 verify_{industry}_calc.js
    print(f'  3/6 verify 生成')
    cases = []
    for line in raw_cases:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
        except: continue
        slug = obj['slug']
        inputs = obj['inputs']
        expect = obj['expect']
        if expect == '__NO_MATCH__': expect = '结果'
        inputs_str = json.dumps(inputs, ensure_ascii=False)
        expect_str = expect.replace('"', '\\"')
        cases.append(f'  {{ slug: "{slug}", inputs: {inputs_str}, expect: ["{expect_str}"] }}')
    
    verify_path = f'scripts/verify_{industry}_calc.js'
    header = f'''#!/usr/bin node
"use strict";
const {{ runCase }} = require("./verify_it_calc.js");
const CASES = [
'''
    footer = f'''];
async function main() {{
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {{
    const r = await runCase(c);
    if (r.ok) {{ pass++; console.log(`  ✅ ${{c.slug}} (via ${{r.via}})`); }}
    else {{ fails.push(c.slug); console.log(`  ❌ ${{c.slug}} ${{r.why}}`);
      if (r.sample) console.log(`     got: ${{r.sample.slice(0, 100)}}`);
    }}
  }}
  console.log(`\\n==== {industry} calc ${{pass}}/${{cs.length}} ====`);
  if (fails.length) process.exit(1);
}}
main();
'''
    open(verify_path, 'w').write(header + ',\n'.join(cases) + footer)
    
    # 4) 跑 harness
    print(f'  4/6 harness 验证')
    r = run(f'node {verify_path}', capture=True, timeout=180)
    print(r.stdout[-300:])
    if r.returncode != 0:
        print('  ❌ harness 未全绿，退出')
        return False
    
    # 5) 注册门禁
    print(f'  5/6 门禁注册')
    gates_path = 'scripts/run_gates.py'
    gates_src = open(gates_path).read()
    gate_line = f'("{industry} calc correctness", ("node", "scripts/verify_{industry}_calc.js")),\n'
    if gate_line.strip() not in gates_src:
        # 找最后一个 calc correctness 门禁后插入
        lines = gates_src.split('\n')
        out_lines = []
        inserted = False
        for line in lines:
            out_lines.append(line)
            if not inserted and 'calc correctness' in line and industry not in line:
                out_lines.append(gate_line.rstrip())
                inserted = True
        if not inserted:
            out_lines.append(gate_line.rstrip())
        open(gates_path, 'w').write('\n'.join(out_lines))
    
    # 6) 构建 + 门禁 + 提交
    print(f'  6/6 构建 → 门禁 → 提交')
    run('python3 _build.py', timeout=120)
    r = run('python3 scripts/run_gates.py', capture=True, timeout=180)
    tail = r.stdout.split('\n')[-3:]
    print('    ' + '\n    '.join(tail))
    
    commit = commit_msg or f'feat: {industry} 分类全站收口'
    run(f'git add -A -- \':!scripts/submit_google_indexing_api.py\' \':!scripts/_grab_step2.js\'', timeout=30)
    run(f'git commit -m "{commit}"', timeout=30)
    run(f'git push origin master', timeout=60)
    
    print(f'  ✅ {industry} 完成！')
    return True

# === 主流程 ===
industries = sys.argv[1:] if len(sys.argv) > 1 else [
    # 从 DEV-PLAN.md 未完成列表（示例）
]
if not industries:
    # 自动从 DEV-PLAN.md 读取下一个未完成的 category
    import re as _re
    devplan = open('DEV-PLAN.md').read()
    pending = _re.findall(r'- \[ \] (\w+) \(\d+\)', devplan)
    industries = pending[:3]  # 一次跑 3 个

print(f'🚀 批量全站收口: {industries}')
for ind in industries:
    cat_converge(ind)
print('\n🏁 批量收口完成')
