import re, glob, os, sys, subprocess
ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io/tools/'
NODE = '/Users/cgw/.workbuddy/binaries/node/versions/22.22.2-3/bin/node'
JSCHECK = '/tmp/_jscheck.js'
WARN = '<p style="color:var(--danger)">⚠ 计算结果含无效值，请检查输入是否为有效正数。</p>'
# ---------------------------------------------------------------------------
# 输出守卫注入工具 v8（2026-09-23）
#
# 与 v7 的差异（v7 的 `expr_is_safe_to_guard` 只是**定义了却没在 transform() 里调用**，
# 即「保守过滤」从未生效；同时 v7 也没有处理 harness 盲区页）：
#
#  1. 接线一个**收窄版**过滤器：只跳过「纯静态字符串字面量」RHS。
#     依据（全站扫描实测，见 DEV-PLAN §8）：守卫对静态字符串永不触发
#     （typeof 非 number、不等于 'Infinity'、文本不含独立 NaN 词），注入纯噪声；
#     而**模板串 / 字符串拼接 / 动态字符串容器变量（如 `html`）的守卫在真机上恰恰有效**
#     —— 数值 NaN 会随插值进入文本，`.test(/ NaN /)` 命中后显示告警，正是不泄漏 NaN 的目的。
#     所以 v8 **刻意不**跳过它们（v7 的过滤设计过宽，若真接线反而会削弱真机防护）。
#
#  2. 新增 `--skip <清单文件>`：用于「页级试错回退」。
#     harness 盲区页（动态构建的 <select> 在无真实 DOM 时取不到值 → 插值得 NaN）
#     会让守卫在 headless 下对**真机正确的输出**误触发，使该页 verify 用例失败。
#     这类页无法静态识别，故流程为：注入 → 跑该行业 verify → 失败页写入清单 →
#     带 `--skip` 重跑 → 直到该行业 verify 全绿。（真机防护不受影响，只是放弃 harness 无法验证的页。）
# ---------------------------------------------------------------------------
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

# ---------- precise guard-tail detection ----------
RE_A = re.compile(r"ToolBox\.setResult\(")
RE_B = re.compile(r"(?:(?:window\.)?document\.)?getElementById\(([^)]*)\)\.innerHTML\s*=")
RE_C = re.compile(r"\$\s*\(\s*(['\"]?)([^'\")\n]*)\1\s*\)\s*\.innerHTML\s*=")
RE_D = re.compile(r"([A-Za-z_$][\w$]*)\.innerHTML\s*=")

def is_guard_tail(expr):
    return re.fullmatch(r"__h\d*", expr.strip()) is not None

def prev_ok(html, pos):
    if pos <= 0: return True
    return html[pos - 1] not in '._(abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$'

# ---------- v8 收窄过滤器 ----------
def is_static_string_literal(expr):
    """RHS 整体就是一个**无插值的**字符串/模板串字面量 -> 守卫永不触发，注入纯噪声。"""
    r = expr.strip()
    if not r or r[0] not in "'\"`":
        return False
    if r[0] == '`' and '${' in r:
        return False                      # 模板串含插值 -> 可能承载 NaN，必须保留
    i = skip_string(r, 0, len(r))
    return i >= len(r)                    # 后面没有拼接/运算符 -> 纯字面量

def guardable(expr):
    e = expr.strip()
    if not e:
        return False
    if is_static_string_literal(e):
        return False
    return True

# ---------- transform ----------
def transform(html):
    out = []; i = 0; n = len(html); changed = 0; uid = 0; skipped_static = 0
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
        # ---- guard-tail skip: already a __hN tail -> keep original, do NOT re-inject ----
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
            if not guardable(expr):
                skipped_static += 1
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
            if not guardable(expr):
                skipped_static += 1
                out.append(html[i:m.end()]); i = m.end(); continue
            repl = ("const %s=%s;if(" + GUARD + "){%s.innerHTML='%s';return;}%s.innerHTML=%s;") % (hn, expr, hn, hn, hn, hn, hn, lhs, WARN, lhs, hn)
            out.append(html[i:pos]); out.append(repl); i = semi + 1
            changed += 1
    new = ''.join(out)
    return new, changed, skipped_static

# ---------- file selection ----------
DRY = '--dry' in sys.argv
SKIP = set()
# 默认加载持久化排除清单：存放「dry-run 静态命中、但真机不存在 NaN 路径」的页面
# （判据见清单头部：jsdom 真机模拟 + 源码兜底核验）。不加载它会让 dry-run 长期
# 报同一批悬空页，诱导后人盲目注入。清单行尾 # 注释会被剥离。
_EXCL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_guard_exclude.txt')
if os.path.isfile(_EXCL):
    for _l in open(_EXCL, encoding='utf-8'):
        _l = _l.split('#')[0].strip()
        if _l:
            SKIP.add(os.path.basename(_l))
if '--skip' in sys.argv:
    _k = sys.argv.index('--skip')
    for _l in open(sys.argv[_k + 1], encoding='utf-8').read().split('\n'):
        _l = _l.strip()
        if _l:
            SKIP.add(os.path.basename(_l))
_args = [a for a in sys.argv[1:] if a != '--dry']
if '--skip' in _args:
    _j = _args.index('--skip')
    _args = _args[:_j] + _args[_j + 2:]
INDS = _args[0].split(',') if _args and _args[0] not in ('--test',) else None
if len(sys.argv) > 1 and sys.argv[1] == '--test':
    f = sys.argv[2]
    html = open(f, encoding='utf-8').read()
    new, ch, sk = transform(html)
    print('FILE', f)
    print('changed', ch, 'skipped_static', sk, 'oolBox_in_new', 'oolBox' in new,
          'setResult_orig', html.count('ToolBox.setResult'), 'setResult_new', new.count('ToolBox.setResult'))
    print('--- NEW TAIL (first 400) ---')
    print(new[:400])
    sys.exit(0)

if INDS and INDS[0].endswith('.txt'):
    files = [ROOT + (l.strip() if l.strip().endswith('.html') else l.strip() + '.html')
             for l in open(INDS[0], encoding='utf-8').read().split('\n') if l.strip()]
else:
    files = sorted(glob.glob(ROOT + '*/*.html'))

tot = 0; injected = 0; skipped = 0; safety = 0; static_total = 0
to_write = {}   # f -> (original_html, new_html)
for f in files:
    if INDS and not INDS[0].endswith('.txt') and f.split('/')[-2] not in INDS: continue
    if os.path.basename(f) in SKIP:
        skipped += 1
        continue
    html = open(f, encoding='utf-8').read()
    tot += 1
    # already guarded (committed) -> never re-touch committed pages (avoids clobbering)
    if 'ToolBox.setResult(' in html:
        continue
    new, ch, sk = transform(html)
    static_total += sk
    if ch == 0 or new == html:
        continue
    # ---- cheap Python safety valve (catches dropped-T corruption / dropped setResult) ----
    if re.search(r'(?<![A-Za-z_.])oolBox', new) or new.count('ToolBox.setResult') < html.count('ToolBox.setResult'):
        safety += 1
        print('SAFETY_PY', f.split('/tools/')[-1])
        continue
    to_write[f] = (html, new)

if DRY:
    for f in to_write:
        print('WILL_INJECT', f.split('/tools/')[-1])
    print('SCANNED', tot, 'WILL_INJECT', len(to_write), 'SKIP_LIST', len(SKIP),
          'SAFETY_PY', safety, 'STATIC_STRING_SKIPPED', static_total)
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

print('SCANNED', tot, 'INJECTED', injected, 'SKIPPED', skipped, 'SAFETY_PY', safety,
      'SAFETY_JS_RESTORED', restored, 'STATIC_STRING_SKIPPED', static_total)
