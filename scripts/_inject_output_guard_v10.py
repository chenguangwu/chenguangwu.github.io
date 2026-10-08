# -*- coding: utf-8 -*-
"""
输出守卫注入工具 v10（2026-10-08，统一升级版）

前序背景：
  - v8 只给 .innerHTML 结果写出点加守卫，且守卫弱（仅 ==='Infinity' 精确匹配，不含 ∞ 符号 /
    不含嵌入字符串的 "Infinity"）。commit 67411abd88 实际落盘用的是「强守卫」(substring Infinity +
    NaN 词)，但仍**不含 ∞ 符号**，且**完全漏掉 .textContent / document.querySelector().PROP**。
  - 极端输入 fuzz 复跑仍 99 BAD：泄漏形态为 ① .textContent 裸写 Infinity/NaN（v8 未覆盖）；
    ② innerHTML 写出 "∞ Pa" / "NaN" 等（v8 强守卫不含 ∞ 符号，弱守卫连 substring Infinity 都没有）。

v10 统一根治：
  - **覆盖全部结果写出路径**：getElementById/$()/var 的 .innerHTML/.textContent/.innerText，
    以及 document.querySelector(All)().innerHTML/.textContent/.innerText。
  - **强守卫（含 ∞ 符号）**：
        (typeof X==='number'&&!isFinite(X)) || /\u221E|Infinity|NaN/.test(String(X))
    既能抓 number 型 Infinity/NaN，也能抓字符串里的 ∞ / Infinity / NaN（含 "Infinity kcal"、
    "∞ Pa"、"NaN" 等多种泄漏形态）。
  - **先剥离后重注（幂等）**：在工具脚本块内，先移除已存在的 v8(__h)/v9(__g) 注入守卫，
    还原为原始 `LHS=EXPR;`，再统一以 v10 守卫重注。因此重复运行稳定、且把弱/旧守卫一并升级为
    含 ∞ 的强守卫。
  - **作用域隔离**：只处理工具自身内联脚本块（含 calc/calcTool/setResult），框架 stub/运行时块
    原样保留，避免给 escHtml 等全局工具误加守卫。
  - **唯一前缀 __g**（与 v8 __h 不冲突），静态字符串字面量 RHS 跳过。

用法：
  python3 _inject_output_guard_v10.py --dry  <filelist.txt>
  python3 _inject_output_guard_v10.py --force <filelist.txt>   # 实际注入
  python3 _inject_output_guard_v10.py --test  <page.html>
"""
import re, glob, os, sys, subprocess

ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io/tools/'
NODE = '/Users/cgw/.workbuddy/binaries/node/versions/22.22.2-6/bin/node'
JSCHECK = '/tmp/_jscheck.js'
WARN_HTML = '<p style="color:var(--danger)">⚠ 计算结果含无效值，请检查输入是否为有效正数。</p>'
WARN_TEXT = '⚠ 计算结果含无效值，请检查输入是否为有效正数。'

GUARD_U = "(typeof %s==='number'&&!isFinite(%s))||/\\u221E|Infinity|NaN/.test(String(%s))"

# 就地消毒表达式（v10b，2026-10-08 修正 blanket 误杀）：
#   - 数值型：非有限 → '—'；有限 → 原值
#   - 字符串型：仅把 ∞/Infinity/NaN 令牌替换成 '—'，其余合法内容（如 "161290"）原样保留
# 相比 v10 的「整块替换为 WARN」，避免次级统计 NaN%（如 totalQty=0 时的校正偏差%）误杀整段结果。
SAN_EXPR = "(typeof %s==='number'?(isFinite(%s)?%s:'—'):String(%s).replace(/\\u221E|Infinity|NaN/g,'—'))"
def san(hn):
    return SAN_EXPR % (hn, hn, hn, hn)

# ---------- scanners ----------
def skip_string(html, i, n):
    q = html[i]; i += 1
    while i < n:
        if html[i] == '\\': i += 2; continue
        if html[i] == q: return i + 1
        if q == '`' and html[i] == '$' and i + 1 < n and html[i + 1] == '{':
            i += 2; bd = 1
            while i < n and bd > 0:
                if html[i] == '{': bd += 1
                elif html[i] == '}': bd -= 1
                elif html[i] in "'\"`": i = skip_string(html, i, n); continue
                i += 1
            continue
        i += 1
    return i

def skip_comment(html, i, n):
    if i + 1 < n and html[i + 1] == '/':
        i += 2
        while i < n and html[i] != '\n': i += 1
        return i
    if i + 1 < n and html[i + 1] == '*':
        i += 2
        while i + 1 < n and not (html[i] == '*' and html[i + 1] == '/'): i += 1
        i += 2
        return i
    return i

def find_paren_str(html, start):
    depth = 0; i = start; n = len(html)
    while i < n:
        c = html[i]
        if c in "'\"`": i = skip_string(html, i, n); continue
        if c == '/':
            nxt = skip_comment(html, i, n)
            if nxt != i: i = nxt; continue
        if c == '(': depth += 1; i += 1; continue
        if c == ')':
            depth -= 1
            if depth == 0: return i
            i += 1; continue
        i += 1
    return -1

def find_semi_balanced(html, start):
    depth = 0; i = start; n = len(html)
    while i < n:
        c = html[i]
        if c in "'\"`": i = skip_string(html, i, n); continue
        if c == '/':
            nxt = skip_comment(html, i, n)
            if nxt != i: i = nxt; continue
        if c in '([{': depth += 1; i += 1; continue
        if c in ')]}': depth -= 1; i += 1; continue
        if c == ';' and depth == 0: return i
        i += 1
    return -1

# ---------- 结果写出模式（v10 全覆盖，含 += 追加）----------
RE_A = re.compile(r"ToolBox\.setResult\(")
RE_B = re.compile(r"(?:(?:window\.)?document\.)?getElementById\(([^)]*)\)\.(innerHTML|textContent|innerText)\s*(\+=|=)")
RE_C = re.compile(r"\$\s*\(\s*([\"']?)([^'\")\n]*)\1\s*\)\s*\.(innerHTML|textContent|innerText)\s*(\+=|=)")
RE_D = re.compile(r"([A-Za-z_$][\w$]*)\.(innerHTML|textContent|innerText)\s*(\+=|=)")
RE_Q = re.compile(r"document\.querySelector(?:All)?\(([^)]*)\)\.(innerHTML|textContent|innerText)\s*(\+=|=)")

# 已注入守卫语句，用于先剥离还原（v10b 同时支持 v10 blanket 与 v8/v9 return 两种形态）
# v10 blanket 形态：const __gN=EXPR;if(GUARD){LHS='WARN';}else{LHS=__gN;}
RE_STRIP_V10 = re.compile(r"const (__[hg]\d*)=([^;]*);if\(.*?\)\{.*?\}else\{([^;=]*?)=\1;\}")
# v8/v9 形态：const __gN=EXPR;if(GUARD){...return;}LHS=__gN;
RE_STRIP_V8 = re.compile(r"const (__[hg]\d*)=([^;]*);if\(.*?\)\{.*?return;\}([^;=]*?)=\1;")
# setResult v10 blanket 形态：const __gN=EXPR;if(GUARD){ToolBox.setResult(ID,'WARN');}else{ToolBox.setResult(ID,__gN);}
RE_STRIP_A_V10 = re.compile(r"const (__[hg]\d*)=([^;]*);if\(.*?\)\{.*?\}else\{ToolBox\.setResult\(([^,]*?),\1\);\}")
# setResult v8/v9 形态：const __gN=EXPR;if(GUARD){...return;}ToolBox.setResult(IDLIT,__gN);
RE_STRIP_A_V8 = re.compile(r"const (__[hg]\d*)=([^;]*);if\(.*?\)\{.*?return;\}ToolBox\.setResult\(([^,]*?),\1\);")

def is_static_string_literal(expr):
    r = expr.strip()
    if not r or r[0] not in "'\"`":
        return False
    if r[0] == '`' and '${' in r:
        return False
    i = skip_string(r, 0, len(r))
    return i >= len(r)

def guardable(expr):
    e = expr.strip()
    if not e: return False
    if is_static_string_literal(e): return False
    # 已消毒形态（RHS 为 (typeof ...).replace(/\u221E|Infinity|NaN/g,...)）跳过，保证幂等不嵌套
    if e.startswith('(typeof') or '/\\u221E|Infinity|NaN/g' in e:
        return False
    return True

def inject_one(lhs, expr, warn, hn, op='='):
    # 就地消毒：无论 = 还是 +=，都把 EXPR（已存为 __gN）消毒后写出，
    # 仅替换 ∞/Infinity/NaN 令牌，保留其余合法内容，杜绝 blanket 误杀整段结果。
    if op == '+=':
        return ("const %s=%s;%s+=%s;") % (hn, expr, lhs, san(hn))
    return ("const %s=%s;%s=%s;") % (hn, expr, lhs, san(hn))

def transform_segment(html, uid):
    # 先剥离已存在的 v10 blanket / v8 / v9 守卫，还原原始写出
    html = RE_STRIP_V10.sub(lambda m: "%s=%s;" % (m.group(3), m.group(2)), html)
    html = RE_STRIP_V8.sub(lambda m: "%s=%s;" % (m.group(3), m.group(2)), html)
    html = RE_STRIP_A_V10.sub(lambda m: "ToolBox.setResult(%s,%s);" % (m.group(3), m.group(2)), html)
    html = RE_STRIP_A_V8.sub(lambda m: "ToolBox.setResult(%s,%s);" % (m.group(3), m.group(2)), html)
    out = []; i = 0; n = len(html); changed = 0; skipped_static = 0
    while i < n:
        ma = RE_A.search(html, i)
        mb = RE_B.search(html, i)
        mc = RE_C.search(html, i)
        md = RE_D.search(html, i)
        mq = RE_Q.search(html, i)
        cands = []
        if ma: cands.append(('A', ma.start(), ma))
        if mb: cands.append(('B', mb.start(), mb))
        if mc: cands.append(('C', mc.start(), mc))
        if md: cands.append(('D', md.start(), md))
        if mq: cands.append(('Q', mq.start(), mq))
        if not cands:
            out.append(html[i:]); break
        cands.sort(key=lambda x: x[1])
        kind, pos, m = cands[0]
        # 已注入守卫尾部（RE_A 形态：setResult('id',__gN)）——跳过
        if kind == 'A':
            p = pos + len("ToolBox.setResult(")
            g = re.match(r"\s*(['\"])([^'\"]*)\1\s*,\s*([\s\S]*?)\s*\)\s*;", html[p:])
            if g and re.fullmatch(r"__[hg]\d*", g.group(3).strip()):
                end = p + g.end(); out.append(html[i:end]); i = end; continue
            # 新鲜 setResult(id, EXPR)：解析 id 与 expr，注入守卫
            lp = pos + len("ToolBox.setResult")
            cp = find_paren_str(html, lp)
            if cp < 0:
                out.append(html[i:m.end()]); i = m.end()
                if i < n and html[i] == ';': i += 1
                continue
            inner = html[lp + 1:cp]
            depth = 0; j = 0; L = len(inner)
            while j < L:
                c = inner[j]
                if c in "'\"`": j = skip_string(inner, j, L); continue
                if c == '(': depth += 1
                elif c == ')': depth -= 1
                elif c == ',' and depth == 0: break
                j += 1
            idlit = inner[:j].strip()
            expr = inner[j + 1:].strip()
            if not expr or not guardable(expr):
                out.append(html[i:m.end()]); i = m.end()
                if i < n and html[i] == ';': i += 1
                continue
            hn = '__g%d' % uid; uid += 1
            # 就地消毒：仅替换 ∞/Infinity/NaN 令牌，保留其余合法内容（非 return 形式，顶层/函数内均合法）
            repl = ("const %s=%s;ToolBox.setResult(%s,%s);") % (hn, expr, idlit, san(hn))
            out.append(html[i:pos]); out.append(repl); i = cp + 1
            if i < n and html[i] == ';': i += 1
            changed += 1
            continue
        hn = '__g%d' % uid; uid += 1
        if kind == 'B':
            idlit = m.group(1); prop = m.group(2); op = m.group(3)
            lhs = "document.getElementById(%s).%s" % (idlit, prop)
            semi = find_semi_balanced(html, m.end())
            if semi < 0: out.append(html[i:m.end()]); i = m.end(); continue
            expr = html[m.end():semi].strip()
            if re.fullmatch(r"__[hg]\d*", expr):
                out.append(html[i:m.end()]); i = m.end(); continue
            if not expr or not guardable(expr):
                if expr and not guardable(expr): skipped_static += 1
                out.append(html[i:m.end()]); i = m.end(); continue
            warn = WARN_TEXT if prop in ('textContent', 'innerText') else WARN_HTML
            repl = inject_one(lhs, expr, warn, hn, op)
            out.append(html[i:pos]); out.append(repl); i = semi + 1
            if i < n and html[i] == ';': i += 1
            changed += 1
        elif kind == 'C':
            sel = m.group(2); prop = m.group(3); op = m.group(4)
            lhs = "$('%s').%s" % (sel, prop)
            semi = find_semi_balanced(html, m.end())
            if semi < 0: out.append(html[i:m.end()]); i = m.end(); continue
            expr = html[m.end():semi].strip()
            if re.fullmatch(r"__[hg]\d*", expr):
                out.append(html[i:m.end()]); i = m.end(); continue
            if not expr or not guardable(expr):
                if expr and not guardable(expr): skipped_static += 1
                out.append(html[i:m.end()]); i = m.end(); continue
            warn = WARN_TEXT if prop in ('textContent', 'innerText') else WARN_HTML
            repl = inject_one(lhs, expr, warn, hn, op)
            out.append(html[i:pos]); out.append(repl); i = semi + 1
            if i < n and html[i] == ';': i += 1
            changed += 1
        elif kind == 'D':
            var = m.group(1); prop = m.group(2); op = m.group(3)
            lhs = "%s.%s" % (var, prop)
            semi = find_semi_balanced(html, m.end())
            if semi < 0: out.append(html[i:m.end()]); i = m.end(); continue
            expr = html[m.end():semi].strip()
            if re.fullmatch(r"__[hg]\d*", expr):
                out.append(html[i:m.end()]); i = m.end(); continue
            if not expr or not guardable(expr):
                if expr and not guardable(expr): skipped_static += 1
                out.append(html[i:m.end()]); i = m.end(); continue
            warn = WARN_TEXT if prop in ('textContent', 'innerText') else WARN_HTML
            repl = inject_one(lhs, expr, warn, hn, op)
            out.append(html[i:pos]); out.append(repl); i = semi + 1
            if i < n and html[i] == ';': i += 1
            changed += 1
        elif kind == 'Q':
            sel = m.group(1); prop = m.group(2); op = m.group(3)
            lhs = "document.querySelector(%s).%s" % (sel, prop)
            semi = find_semi_balanced(html, m.end())
            if semi < 0: out.append(html[i:m.end()]); i = m.end(); continue
            expr = html[m.end():semi].strip()
            if re.fullmatch(r"__[hg]\d*", expr):
                out.append(html[i:m.end()]); i = m.end(); continue
            if not expr or not guardable(expr):
                if expr and not guardable(expr): skipped_static += 1
                out.append(html[i:m.end()]); i = m.end(); continue
            warn = WARN_TEXT if prop in ('textContent', 'innerText') else WARN_HTML
            repl = inject_one(lhs, expr, warn, hn, op)
            out.append(html[i:pos]); out.append(repl); i = semi + 1
            if i < n and html[i] == ';': i += 1
            changed += 1
    return ''.join(out), changed, skipped_static, uid

TOOL_MARK = re.compile(r"ToolBox\.setResult\(|function\s+calcTool\s*\(|function\s+calc\s*\(")

def transform_html(html):
    out = []; i = 0; n = len(html); changed = 0; skipped_static = 0; uid = 0
    while i < n:
        s = html.find('<script', i)
        if s < 0:
            out.append(html[i:]); break
        e = html.find('>', s)
        if e < 0:
            out.append(html[i:]); break
        head = html[s:e + 1]
        close = html.find('</script>', e)
        if close < 0:
            out.append(html[i:]); break
        content = html[e + 1:close]
        tail = html[close:close + len('</script>')]
        if 'src=' in head.lower() or not TOOL_MARK.search(content):
            out.append(html[i:close + len('</script>')]); i = close + len('</script>'); continue
        newc, ch, sk, uid = transform_segment(content, uid)
        changed += ch; skipped_static += sk
        out.append(html[i:s]); out.append(head); out.append(newc); out.append(tail)
        i = close + len('</script>')
    return ''.join(out), changed, skipped_static

# ---------- file selection ----------
DRY = '--dry' in sys.argv
FORCE = '--force' in sys.argv
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    f = sys.argv[2]
    html = open(f, encoding='utf-8').read()
    new, ch, sk = transform_html(html)
    print('FILE', f)
    print('changed', ch, 'skipped_static', sk)
    idx = new.find('function calc')
    print(new[idx:idx + 500] if idx >= 0 else new[:500])
    sys.exit(0)

_list = [a for a in sys.argv[1:] if a not in ('--dry', '--force')]
if not _list:
    print('USAGE: _inject_output_guard_v10.py [--dry|--force] <filelist.txt>'); sys.exit(1)
listarg = _list[0]
if listarg.endswith('.txt'):
    files = []
    for l in open(listarg, encoding='utf-8').read().split('\n'):
        l = l.strip()
        if not l: continue
        if os.path.isabs(l) and l.endswith('.html') and os.path.isfile(l): files.append(l)
        elif os.path.isfile(os.path.join(ROOT, l)): files.append(os.path.join(ROOT, l))
        elif os.path.isfile(l): files.append(l)
        else: files.append(os.path.join(ROOT, l))
else:
    files = sorted(glob.glob(ROOT + '*/*.html'))

tot = 0; injected = 0; skipped = 0; safety = 0; static_total = 0
to_write = {}
for f in files:
    tot += 1
    html = open(f, encoding='utf-8').read()
    new, ch, sk = transform_html(html)
    static_total += sk
    if ch == 0 or new == html:
        continue
    # 仅做「结构损坏」特征检测：剥离正则都要求 __gN 回引用，只匹配此前注入点，
    # 不会误伤真实 setResult；v10b 把 blanket(2 个 setResult) 合并为消毒形态(1 个)，
    # setResult 计数下降属合法，不再据此判不安全。真正语法损坏由 SAFETY_JS 兜底。
    if re.search(r'(?<![A-Za-z_.])oolBox', new):
        safety += 1
        print('SAFETY_PY', f.split('/tools/')[-1])
        continue
    to_write[f] = (html, new)

if DRY:
    for f in to_write:
        print('WILL_INJECT', f.split('/tools/')[-1])
    print('SCANNED', tot, 'WILL_INJECT', len(to_write), 'SAFETY_PY', safety, 'STATIC_STRING_SKIPPED', static_total)
    sys.exit(0)

for f, (html, new) in to_write.items():
    open(f, 'w', encoding='utf-8').write(new)
    injected += 1

restored = 0
if to_write:
    allf = list(to_write.keys())
    bad = set()
    for k in range(0, len(allf), 300):
        chunk = allf[k:k + 300]
        r = subprocess.run([NODE, JSCHECK] + chunk, capture_output=True, text=True)
        if r.returncode != 0:
            for line in (r.stdout + r.stderr).splitlines():
                if line.startswith('  '):
                    bf = line.strip().split(':')[0]
                    if bf in to_write: bad.add(bf)
    for bf in bad:
        open(bf, 'w', encoding='utf-8').write(to_write[bf][0])
        injected -= 1; restored += 1
        print('SAFETY_JS', bf.split('/tools/')[-1])

print('SCANNED', tot, 'INJECTED', injected, 'SAFETY_PY', safety,
      'SAFETY_JS_RESTORED', restored, 'STATIC_STRING_SKIPPED', static_total)
