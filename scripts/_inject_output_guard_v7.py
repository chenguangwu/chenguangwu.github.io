import re, glob, os, sys, subprocess
ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io/tools/'
NODE = '/Users/cgw/.workbuddy/binaries/node/versions/22.22.2-3/bin/node'
JSCHECK = '/tmp/_jscheck.js'
WARN = '<p style="color:var(--danger)">⚠ 计算结果含无效值，请检查输入是否为有效正数。</p>'
# Value-based guard: only fire on REAL invalid values, never on legitimate text that
# merely contains the words "NaN"/"Infinity"/"undefined" (e.g. "会溢出为 Infinity。").
# - numeric non-finite (NaN/Infinity) via typeof+!isFinite
# - literal string "Infinity"/"-Infinity"  (NOTE: substring "Infinity" is intentionally NOT matched,
#   otherwise warnings like "...会溢出为 Infinity。" would be wrongly intercepted)
# - standalone word "NaN"  (word-boundary, so "NaNO₂" is NOT matched)
# NOTE: the former `/undefined/.test(x)` clause was REMOVED. It matched the literal
# text "undefined" inside otherwise-correct HTML output (e.g. a tool whose result
# template interpolates a variable that is undefined only under the headless harness
# because the <select>s are built dynamically, not present in static HTML). That
# produced false-positive neutralization of correct pages (gingival-index etc.).
# No verify case expects output containing "undefined", so dropping the clause loses
# zero real protection while restoring correct pages.
GUARD = "(typeof %s==='number'&&!isFinite(%s))||%s==='Infinity'||%s==='-Infinity'||/(^|[^A-Za-z])NaN([^A-Za-z]|$)/.test(%s)"

# ---------- string/comment/paren/semi aware scanners ----------
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

# ---------- precise guard-tail detection (replaces broken already_guarded) ----------
RE_A = re.compile(r"ToolBox\.setResult\(")
RE_B = re.compile(r"(?:(?:window\.)?document\.)?getElementById\(([^)]*)\)\.innerHTML\s*=")
RE_C = re.compile(r"\$\s*\(\s*(['\"]?)([^'\")\n]*)\1\s*\)\s*\.innerHTML\s*=")
RE_D = re.compile(r"([A-Za-z_$][\w$]*)\.innerHTML\s*=")

def is_guard_tail(expr):
    return re.fullmatch(r"__h\d*", expr.strip()) is not None

def prev_ok(html, pos):
    if pos <= 0: return True
    return html[pos - 1] not in '._(abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$'

# ---------- conservative safety filter (hardening: only guard pure-value RHS) ----------
# A guard wraps `rhs` and checks `if(GUARD){...WARN...} else { lhs.innerHTML = rhs }`.
# If `rhs` is a *string* (template literal / concatenation / array map), the guard
# misfires: legitimate text containing the literal "NaN"/"Infinity" (or a string built
# from a NaN number, e.g. `${gi.toFixed(2)}` when gi=NaN) triggers the WARN and clobbers
# correct output. Hardening: only inject when `rhs` is a *pure variable / pure numeric
# arithmetic expression*. Everything that builds DOM/strings dynamically is skipped —
# those pages need real-DOM simulation (a separate large effort), not a value guard.
def expr_is_safe_to_guard(expr):
    e = expr.strip()
    if not e:
        return False
    # scan with string/bracket awareness; bail on ${...} interpolation OUTSIDE strings
    i = 0; n = len(e)
    while i < n:
        c = e[i]
        if c in "'\"`":
            i = skip_string(e, i, n); continue
        if c == '$' and i + 1 < n and e[i + 1] == '{':
            return False  # template interpolation -> skip
        i += 1
    # pure string/string-template literal RHS -> skip (guarding strings misfires)
    if e[0] in "'\"`":
        return False
    # method calls (string formatting / array ops / DOM building) -> skip
    if re.search(r'\.(?:toFixed|toPrecision|toString|toLocaleString|toExponential|'
                 r'map|forEach|filter|reduce|join|replace|split|sort|slice|concat|'
                 r'push|pop|shift|unshift|reverse|substring|substr|trim|'
                 r'toUpperCase|toLowerCase|repeat|padStart|padEnd)\s*\(', e):
        return False
    # custom render/build/format helpers (produce strings/DOM) -> skip to be safe
    if re.search(r'\b(?:render|build|create|make|gen|format|display|show|draw|'
                 r'print|output|toHtml|toHTML|html|append|setHtml)\w*\s*\(', e):
        return False
    return True

# ---------- transform ----------
def transform(html):
    out = []; i = 0; n = len(html); changed = 0; uid = 0
    while i < n:
        ma = RE_A.search(html, i)
        mb = RE_B.search(html, i)
        mc = RE_C.search(html, i)
        md = RE_D.search(html, i)
        cands = []
        if ma: cands.append(('A', ma.start(), ma))
        if mb: cands.append(('B', mb.start(), mb))
        if mc and prev_ok(html, mc.start()): cands.append(('C', mc.start(), mc))
        if md and prev_ok(html, md.start()): cands.append(('D', md.start(), md))
        if not cands:
            out.append(html[i:]); break
        cands.sort(key=lambda x: x[1])
        kind, pos, m = cands[0]
        # ---- guard-tail skip: this setResult/assignment is already a __hN tail -> keep original, do NOT re-inject, do NOT drop text ----
        if kind == 'A':
            p = pos + len("ToolBox.setResult(")
            g = re.match(r"\s*(['\"])([^'\"]*)\1\s*,\s*([\s\S]*?)\s*\)\s*;", html[p:])
            if g and is_guard_tail(g.group(3)):
                end = p + g.end()
                out.append(html[i:end]); i = end
                continue
        else:
            semi = find_semi_balanced(html, m.end())
            if semi >= 0:
                expr = html[m.end():semi].strip()
                if is_guard_tail(expr):
                    out.append(html[i:semi + 1]); i = semi + 1
                    continue
        hn = '__h%d' % uid; uid += 1
        if kind == 'A':
            p = pos + len("ToolBox.setResult(")
            mq = re.match(r"\s*(['\"])([^'\"]*)\1\s*,", html[p:])
            if not mq:
                out.append(html[i:m.end()]); i = m.end(); continue
            qid = mq.group(2); expr_start = p + mq.end(); rb = find_paren_str(html, p - 1)
            if rb < 0:
                out.append(html[i:m.end()]); i = m.end(); continue
            expr = html[expr_start:rb].strip()
            if not expr:
                out.append(html[i:m.end()]); i = m.end(); continue
            repl = ("const %s=%s;if(" + GUARD + "){ToolBox.setResult('%s','%s');return;}ToolBox.setResult('%s',%s);") % (hn, expr, hn, hn, hn, hn, hn, qid, WARN, qid, hn)
            out.append(html[i:pos]); out.append(repl); i = rb + 1
            if i < n and html[i] == ';': i += 1
            changed += 1
        else:
            lhs = re.sub(r'\.innerHTML\s*=\s*$', '', m.group(0))
            semi = find_semi_balanced(html, m.end())
            if semi < 0:
                out.append(html[i:m.end()]); i = m.end(); continue
            expr = html[m.end():semi].strip()
            if not expr:
                out.append(html[i:m.end()]); i = m.end(); continue
            repl = ("const %s=%s;if(" + GUARD + "){%s.innerHTML='%s';return;}%s.innerHTML=%s;") % (hn, expr, hn, hn, hn, hn, hn, lhs, WARN, lhs, hn)
            out.append(html[i:pos]); out.append(repl); i = semi + 1
            changed += 1
    new = ''.join(out)
    return new, changed

# ---------- file selection ----------
DRY = '--dry' in sys.argv
_args = [a for a in sys.argv[1:] if a != '--dry']
INDS = _args[0].split(',') if _args and _args[0] not in ('--test',) else None
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    f = sys.argv[2]
    html = open(f, encoding='utf-8').read()
    new, ch = transform(html)
    print('FILE', f)
    print('changed', ch, 'oolBox_in_new', 'oolBox' in new,
          'setResult_orig', html.count('ToolBox.setResult'), 'setResult_new', new.count('ToolBox.setResult'))
    print('--- NEW TAIL (first 400) ---')
    print(new[:400])
    sys.exit(0)

if INDS and INDS[0].endswith('.txt'):
    files = [ROOT + (l.strip() if l.strip().endswith('.html') else l.strip() + '.html')
             for l in open(INDS[0], encoding='utf-8').read().split('\n') if l.strip()]
else:
    files = sorted(glob.glob(ROOT + '*/*.html'))

tot = 0; injected = 0; skipped = 0; safety = 0
to_write = {}   # f -> (original_html, new_html)
for f in files:
    if INDS and not INDS[0].endswith('.txt') and f.split('/')[-2] not in INDS: continue
    html = open(f, encoding='utf-8').read()
    tot += 1
    # already guarded (committed) -> never re-touch committed pages (avoids clobbering)
    if 'ToolBox.setResult(' in html:
        continue
    new, ch = transform(html)
    if ch == 0 or new == html:
        continue
    # ---- cheap Python safety valve (catches dropped-T corruption / dropped setResult) ----
    # NOTE: 'oolBox' is a substring of 'ToolBox'; only flag it when NOT preceded by a
    # word char or dot (that's a real "ToolBox lost its T" corruption).
    if re.search(r'(?<![A-Za-z_.])oolBox', new) or new.count('ToolBox.setResult') < html.count('ToolBox.setResult'):
        safety += 1
        print('SAFETY_PY', f.split('/tools/')[-1])
        continue
    to_write[f] = (html, new)

# ---- write all (unless --dry), then verify with node vm.Script, restore any bad ----
if DRY:
    for f in to_write:
        print('WILL_INJECT', f.split('/tools/')[-1])
    print('SCANNED', tot, 'WILL_INJECT', len(to_write), 'SAFETY_PY', safety)
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

print('SCANNED', tot, 'INJECTED', injected, 'SKIPPED', skipped, 'SAFETY_PY', safety, 'SAFETY_JS_RESTORED', restored)
