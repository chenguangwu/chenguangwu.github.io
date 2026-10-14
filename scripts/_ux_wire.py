#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UX-Q4 薄弱页补线生成器（零侵入、复用页面自身计算逻辑）。

只对「已引 tool-kit.js 但未接线组件」的薄弱计算器页生效：
  - 抽取 calcTool 的 输入读取 + 计算赋值 + dataGrid 结果数组
  - 在结果区后插入 速查表 / 与上比 / 历史 三个容器
  - 在输入区后插入 预设条容器；在工具栏加 导出按钮
  - 注入 __xxExtras / __xxPresets / __xxExport + calcTool 包装器 + __xxBoot
  - 把静态新增的「导出明细 CSV」写入该页 EN 字典

特性：
  - 复用页面自身计算代码（extras 内重跑同一段赋值），结果零误差
  - 动态内容（matrix 行/头、预设 label）走 JS 字面量，EN 静态探针不扫，免翻译
  - 仅 HTML 内新增的中文按钮「导出明细 CSV」需入 EN 字典（标准条目 Export detail CSV）
  - 跳过已含 TBKit.matrix.table 的页（防重复接线）

用法：
  python3 scripts/_ux_wire.py --cat robotics            # dry 预览 + 统计
  python3 scripts/_ux_wire.py --cat robotics --apply    # 实际写入
  python3 scripts/_ux_wire.py --cat robotics --apply --page belt-linear-speed
"""
import os, re, sys, json, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

# 非 JS 脚本块（JSON-LD 等）：浏览器不执行，注入其中=死代码+污染结构化数据
def _is_nonjs_type(attrs):
    tm = re.search(r'type\s*=\s*["\']([^"\']*)["\']', attrs, re.I)
    if not tm:
        return False
    v = tm.group(1).strip().lower()
    return v != '' and 'javascript' not in v

def last_js_script_close(s):
    """返回最后一个「真 JS 内联块」的 </script> 索引；跳过 src 外链与
    application/ld+json 等非 JS 块（曾因注入进 FAQ JSON-LD 致 141 页接线成
    死代码 + JSON-LD 污染，2026-10-14 修复）。无则返回 -1。"""
    best = -1
    for m in re.finditer(r'<script\b([^>]*)>', s, re.I):
        attrs = m.group(1)
        if re.search(r'\bsrc\s*=', attrs, re.I):
            continue
        if _is_nonjs_type(attrs):
            continue
        close = s.find('</script>', m.end())
        if close == -1:
            continue
        if close > best:
            best = close
    return best

def bracket_match(s, start):
    """从 s[start]（应为 '['）起，匹配最外层 [...] 返回 (内容, 结束索引)"""
    assert s[start] == '['
    depth = 0
    i = start
    while i < len(s):
        c = s[i]
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return s[start+1:i], i+1
        i += 1
    return None, i

def bracket_depth(s):
    """粗略括号深度：{[+( 计数减 }]) 计数（不考虑字符串，全角括号不影响）。
    用于判断一行续行归属：>0 表示该行括号未闭合，后续闭合行必须拼回。"""
    return s.count('{') + s.count('[') + s.count('(') - s.count('}') - s.count(']') - s.count(')')

def find_datagrid_array(body):
    idx = body.find('dataGrid(')
    if idx < 0:
        return None
    j = body.find('[', idx)
    if j < 0:
        return None
    arr, _ = bracket_match(body, j)
    return arr

def calc_body(s):
    """括号匹配提取完整 calcTool 函数体（支持 calcTool() / calcTool(force) / 含嵌套块）。
    返回函数体字符串；找不到返回 None。"""
    m = re.search(r'function calcTool\s*\([^)]*\)\s*\{', s)
    if not m:
        return None
    start = m.end() - 1  # 指向 '{'
    depth = 0
    i = start
    while i < len(s):
        c = s[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[start+1:i]
        i += 1
    return None

def extract(page):
    """返回 dict: inputs, compute(赋值段), dg_rows([ [valExpr, label], ... ]), primary(var)"""
    s = open(page, encoding='utf-8').read()
    body = calc_body(s)
    if body is None:
        return None
    # 输入 id：优先从 num('x')；再补 __tbInputGuard(['x',...])
    inputs = re.findall(r"num\('([^']+)'\)", body)
    if not inputs:
        g = re.search(r"__tbInputGuard\(\s*\[([^\]]*)\]", body)
        if g:
            inputs = re.findall(r"'([^']+)'", g.group(1))
    num_ids = list(inputs)
    # 补：calc 内直读 getElementById('id').value/.checked 的控件——num() 只覆盖数值输入，
    # select/checkbox/列表粘贴输入直读曾致漏识别（记录缺列、历史缺字段、restore 丢状态，
    # 如 drinking-water-plan 的 act/stage、free-space-impedance 的 x）
    # .value/.checked 后不得紧跟 =（resetForm 的赋值形态，曾把 dummy 占位输入误纳）
    for m in re.finditer(r"getElementById\('([\w-]+)'\)\.(?:value|checked)(?![^;]{0,4}=)", body):
        iid = m.group(1)
        if iid not in inputs and re.search(r'<(?:input|select|textarea)\b[^>]*\bid="%s"' % re.escape(iid), s):
            inputs.append(iid)
    # dataGrid 数组
    dg = find_datagrid_array(body)
    if dg is None:
        return None
    # dg_rows: 解析 [[valExpr, 'label'], ...]
    # 用括号匹配逐对提取
    rows = []
    i = 0
    while i < len(dg):
        if dg[i] == '[':
            inner, end = bracket_match(dg, i)
            # inner 形如 "valExpr, 'label'"
            # 找最后一个逗号分隔的 'label'（带引号）
            mm = re.search(r",\s*('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")\s*$", inner)
            if mm:
                label = mm.group(1)[1:-1]
                val = inner[:mm.start()].rstrip().rstrip(',').strip()
                rows.append([val, label])
            i = end
        else:
            i += 1
    # compute 段：切到「含 dataGrid( 的整行」之前（避免把 `let x=dataGrid(` 同行的 `let x=` 悬空成语法错）
    gi = body.find('dataGrid(')
    line_start = body.rfind('\n', 0, gi) + 1
    pre = body[:line_start]
    # 含 for/while 循环累加的计算（如债券久期/凸性）无法用扁平赋值复现 → 跳过，避免产出 NaN 表
    if re.search(r'\b(for|while)\s*\(', pre):
        return None
    # 去掉 __ig 守卫整体
    pre = re.sub(r"var __ig=.*?return;\s*\}", "", pre, flags=re.S)
    # 去掉悬挂 const __gN=
    # 同行函数声明（前一段以 } 或 ; 结尾）拆到独立行：否则 st 不以 function 开头，
    # 会被当成上一行的续行拼接进 keep，产出坏块（convert-power 真案例）。
    pre = re.sub(r'([;}])\s*(function\s+\w+\s*\()', r'\\1\n\\2', pre)
    pre = re.sub(r"const\s+__g\d*\s*=\s*$", "", pre)
    # 语句级过滤：保留 ① const/var/let 赋值 ② 完整括号平衡的 if/else 链（花括号/无花括号均可）
    # 整块丢弃 for/while/switch/try/function（花括号须平衡，防悬挂）；含 for/while/dataGrid 的
    # if 链也丢。曾因整段删除花括号 if/else 致 `var Ea;`/`let I,W,desc;` 悬空 → 表行
    # Ea.toFixed TypeError 被 try/catch 吞掉、明细表静默死亡（active-earth-rankine 真案例）；
    # 也曾因丢弃无花括号 if 链致 `var perDay;` 悬空（diaper-usage 真案例）。
    # 孤立 else（其 if 已被丢弃）必须一并丢弃，否则语法错。
    def _brace_delta(t):
        return t.count('{') - t.count('}')
    keep = []
    fn_blocks = []   # 原样保留的嵌套辅助函数（primary 提取需跳过，防取到函数体内局部变量）
    lines = pre.splitlines()
    i = 0
    while i < len(lines):
        st = lines[i].strip()
        i += 1
        if not st:
            continue
        if re.match(r"^(const|var|let)\b", st) and "setResult" not in st and "__tbInputGuard" not in st and "__ig" not in st:
            keep.append(st)
        elif re.match(r"^(if|else)\b", st):
            # 收集完整 if/else-if/else 语句（花括号平衡为止）
            stmt = [st]
            depth = _brace_delta(st)
            while depth > 0 and i < len(lines):
                nxt = lines[i]
                if not nxt.strip().startswith('//'):
                    stmt.append(nxt.strip())  # 纯注释行跳过：拼行会把后续代码吞进注释
                depth += _brace_delta(nxt)
                i += 1
            text = " ".join(x for x in stmt if x)
            if re.match(r"^else\b", st) and not (keep and re.match(r"^(if|else)\b", keep[-1])):
                continue  # 孤立 else：配对的 if 已丢弃 → 丢 else 防语法错
            if re.search(r'\b(for|while)\s*\(|dataGrid\(', text):
                continue  # 循环/表格生成无法安全内联 → 丢
            if "setResult" in text or re.search(r'\breturn\b', text):
                continue  # Extras 重跑段不能 setResult（覆写结果区/双弹提示）也不能提前 return（跳过记录与挂载）
            keep.append(text)
        elif re.match(r"^function\s+\w+\s*\(", st):
            # 嵌套辅助函数（fmt/erf/isPrime 等）：原样整块保留（多行也原样，不用空格拼接）。
            # 旧逻辑整块丢弃 → compute 内调用该函数时 ReferenceError 被 try/catch 吞掉，
            # 明细表/历史/预设静默全死（比不接线更隐蔽）。原样保留即与页面内语义等价
            # （函数声明提升、同一声明顺序）。
            blk = [st]
            depth = _brace_delta(st)
            while depth > 0 and i < len(lines):
                nxt = lines[i]
                if not nxt.strip().startswith('//'):
                    blk.append(nxt)   # 纯注释行跳过：拼块会把后续代码吞进注释
                depth += _brace_delta(nxt)
                i += 1
            if depth > 0:
                return None          # 括号无法闭合 → 放弃该页，防产出坏块
            text = "\n".join(blk)
            # 会二次渲染结果区 / 直接写 DOM 的辅助函数不可保留 → 放弃该页（保守）
            if re.search(r'dataGrid\(|setResult|innerHTML|getElementById\(\s*[\'"]res', text):
                return None
            fn_blocks.append(text)
            keep.append(text)
            continue
        elif re.match(r"^(for|while|switch|try)\b", st):
            # 整块丢弃（消费到花括号平衡）
            depth = _brace_delta(st)
            while depth > 0 and i < len(lines):
                depth += _brace_delta(lines[i])
                i += 1
        elif keep and not re.match(r"^(const|var|let|if|for|while|switch|function|return|else|do|try|catch|throw|break|continue)\b", st):
            # 续行拼接：以 } ] ) 开头的闭合行，在上一行括号未闭合时（多行对象/数组字面量）必须拼回，
            # 否则会丢闭合括号产生语法错（如 const info={...} 跨行、闭合行独立成 `};`）。
            # 上一行已闭合（函数体闭合等）才丢弃。
            if st[0] in '}])' and bracket_depth(keep[-1]) <= 0:
                continue
            keep[-1] += " " + st
        # 其余（控制流/孤立续行）丢弃
    pre = "\n".join(keep)
    # 末尾修剪：dataGrid 切分线（line_start）可能拦腰斩断「块体含 dataGrid 的 if/else」，
    # 使 pre 末尾留下未闭合块头（如 `if (v2sq < 0) {`）→ extras 花括号不平衡 SyntaxError、
    # 整块接线死（bernoulli-velocity / slope-line / quadratic-solver 真案例）。
    # 正向扫描，只保留到最后一个「花括号深度归零」的行为止。
    tl = pre.splitlines()
    depth = 0
    last_ok = -1
    for idx, ln in enumerate(tl):
        if depth == 0 and not ln.strip():
            last_ok = idx
            continue
        depth += _brace_delta(ln)
        if depth <= 0:
            depth = 0
            last_ok = idx
    pre = "\n".join(tl[:last_ok + 1])
    # primary 结果变量：第一个非输入的 const/var 赋值（compute 内联时块级 const/let
    # 已全部提升为 var——函数作用域，Extras 顶层可达；dilution-c1v1 真案例：
    # `if(...){ const V=...; }` 曾致 record 的 V:V ReferenceError）
    # 逐条 keep 扫描（跳过嵌套函数块内部），顺序与旧版在 "\n".join(keep) 上搜索一致
    primary = None
    for stmt in keep:
        if re.match(r"^function\b", stmt):
            continue
        for mm in re.finditer(r"(?:const|var|let)\s+(\w+)\s*=", stmt):
            v = mm.group(1)
            if v not in inputs and v not in ('__g1','__g2','__ig'):
                primary = v
                break
        if primary:
            break
    return {"inputs": inputs, "num_ids": num_ids, "compute": pre, "dg_rows": rows, "primary": primary}

def find_tag_close(s, open_idx):
    """open_idx 指向 '<tagname'；返回该元素闭合标签结束索引（自闭合返回开标签结束）。
    属性值含 '>' 时可能失配，调用方须 try 包裹。"""
    m = re.match(r'<(\w+)', s[open_idx:])
    if not m:
        return None
    tag = m.group(1)
    pat = re.compile(r'<(/?)%s\b[^>]*?(/?)>' % tag, re.I)
    depth = 0
    i = open_idx
    while True:
        mm = pat.search(s, i)
        if not mm:
            return None
        if mm.group(1) == '/':
            depth -= 1
            if depth == 0:
                return mm.end()
        elif mm.group(2) == '/':
            if depth == 0:
                return mm.end()
        else:
            depth += 1
        i = mm.end()


RESULT_IDS = ("result", "res", "output")
# 次级容器：搜索/筛选型「可检索参考列表」页（rock-identify / cloud-identify /
# pottery-typology / 64-gua / plant-care 等）用 render()/filterList() 渲染到列表容器，
# 无 result/res/output。仅在无主容器时退化使用，避免误伤导航列表页。
# 只放**已核验**的结果列表容器。曾用通配 `(?:List|Grid|Results)$` 兜底，实测把
# historyList / statGrid / presetsGrid / slidesList / recList 等控件面板当成结果区，
# 表格插错位置 → 改为显式名单，宁可少接也不错接。
RESULT_IDS2 = ("resultList", "result-list", "countryList", "guaList", "plantList",
               "cardList", "itemList", "listBox", "list", "listDiv", "rodList",
               "formulaList", "herbList", "recipeList", "results", "detail",
               "grid", "tableWrap", "tableArea")
RESULT_CLASSES = ("result-box", "result-display")
# 末级兜底：按 id 名的**词边界**猜结果容器（resultBox / cssOutput / breakdown / …）。
# 必须词边界而非子串——"res" 是 "presets" 的子串、"list" 会命中 "presetGrid"/"hiveList"
# 等控件区，实测把表格插进预设面板。命不中就放弃该页（宁可不接也不接到错误容器）。
RESULT_HINT_RE = re.compile(
    r'(?:^|[\-_])(?:result|res|output|outcome|breakdown|answer|summary)(?:$|[\-_])'
    r'|(?:Result|Output|Outcome|Breakdown|Answer|Summary)')

def find_result_container(s):
    """定位结果容器：主 id（result/res/output）→ 次级列表 id → class → id 名子串兜底。
    返回 ('id', val) / ('class', val) / None。新架构页（leather/pet 等）用 id="res"，
    部分页只有 class="result-box" 无 id。"""
    for rid in RESULT_IDS:
        if re.search(r'id="%s"' % re.escape(rid), s):
            return ("id", rid)
    for rid in RESULT_IDS2:
        if re.search(r'id="%s"' % re.escape(rid), s):
            return ("id", rid)
    for rc in RESULT_CLASSES:
        if re.search(r'class="[^"]*\b%s\b' % re.escape(rc), s):
            return ("class", rc)
    for mm in re.finditer(r'id="([\w-]+)"', s):
        if RESULT_HINT_RE.search(mm.group(1)):
            return ("id", mm.group(1))
    return None

def extract_custom(page):
    """新架构手工页模式：顶层 function <fn> + 结果容器（id/res/output 或 result-box 类）
    + 输入控件（无 calcTool/dataGrid）。返回 dict(fn, inputs, defaults, container) 或 None。
    fn 取按钮/输入事件回调中的顶层函数，优先 calc/compute/solve/count/estimate/eval 系命名。"""
    s = open(page, encoding='utf-8').read()
    if 'TBKit.matrix.table' in s:
        return None
    container = find_result_container(s)
    if container is None:
        return None
    cands = []
    for mm in re.finditer(r'on(?:click|input|change)="(\w+)\(', s):
        c = mm.group(1)
        if c not in cands:
            cands.append(c)
    # 计算型函数名：只包这些语义的函数。旧逻辑「任意顶层函数」会把 UI 动作
    # （copyCode/switchTab/addHive/togglePlay/openAddVeh/useEyeDropper）当成计算入口，
    # 包裹后表格/历史只在用户点那个具体控件时才渲染 → 接线形同虚设且位置错乱。
    FN_OK = r'^(?:calc|calculate|compute|solve|count|estimate|eval|evaluate|convert|generate|analyze|analyse|render|filter|search|doSearch|lookup|update|apply)\w*$'
    def _declared(c):
        if re.search(r'(?:^|[;}])\s*function\s+%s\s*\(' % re.escape(c), s, re.M):
            return True
        # var / window. 赋值式声明可安全重包；const/let 不可（运行时 TypeError）
        return bool(re.search(r'(?:var\s+%s\s*=\s*function|window\.%s\s*=\s*function)'
                              % (re.escape(c), re.escape(c)), s))
    fn = None
    for c in cands:
        if re.match(FN_OK, c, re.I) and _declared(c):
            fn = c
            break
    if fn is None:
        return None
    # 输入控件 id（input/select/textarea），去重保序，上限 12 防表过宽
    ids = []
    for mm in re.finditer(r'<(?:input|select|textarea)\b[^>]*\bid="([\w-]+)"', s):
        iid = mm.group(1)
        # 只排除站点搜索/安全字段。旧规则排除任何含 search 的 id → 把工具自身的
        # 关键词过滤框（travel-adapter-guide / herb-processing 的 id="search"）误杀，
        # 输入集合为空 → 该页直接放弃接线。
        if re.search(r'(?:token|csrf|nonce)', iid, re.I):
            continue
        if re.match(r'(?:q|query)$', iid, re.I):
            continue
        if re.search(r'(?:site|nav|header|global|top)[-_]?search', iid, re.I):
            continue
        if iid not in ids:
            ids.append(iid)
    inputs = ids[:12]
    if not inputs:
        return None
    defaults = {}
    for iid in inputs:
        m = re.search(r'<(?:input|select|textarea)\b[^>]*\bid="%s"[^>]*\bvalue="([^"]*)"' % re.escape(iid), s)
        if m:
            defaults[iid] = m.group(1)
        else:
            m2 = re.search(r'<select\b[^>]*\bid="%s"[^>]*>\s*<option[^>]*value="([^"]*)"' % re.escape(iid), s)
            defaults[iid] = m2.group(1) if m2 else ''
    return {"fn": fn, "inputs": inputs, "defaults": defaults, "container": container}


def gen_script(name, info):
    p = name  # 前缀
    inputs = info["inputs"]
    compute = info["compute"]
    rows = info["dg_rows"]
    primary = info["primary"]
    # matrix 行：[label, valExpr]
    matrix_rows = ",\n".join("            [%r, %s]" % (lbl, val) for val, lbl in rows)
    # history.record 字段：所有输入
    rec = ", ".join("%s:__n('%s')" % (i, i) for i in inputs)
    # mount 回填
    restore = " ".join("if(rec.%s!=null)document.getElementById('%s').value=rec.%s;" % (i, i, i) for i in inputs)
    # 预设：默认 + 2× + 0.5×（基于输入默认值，需从 HTML 取，这里先留占位，外部补）
    return inputs, compute, matrix_rows, rec, restore, primary

def _strip_js_line_comment(line):
    """去除 JS 行内 // 注释（引号感知），保留字符串与 :// URL 内的 //。

    extract() 把多行 if/else 拼成单行后，行内 // 注释会吞掉后续代码（含收尾 }），
    致 Extras 块花括号不闭合（desk-dimensions 真案例）。重放 compute 前剥注释消除该隐患。"""
    out = []
    i = 0
    n = len(line)
    in_s = in_d = False
    while i < n:
        c = line[i]
        if c == "'" and not in_d:
            in_s = not in_s
        elif c == '"' and not in_s:
            in_d = not in_d
        elif c == '/' and not in_s and not in_d and i + 1 < n and line[i + 1] == '/' and (i == 0 or line[i - 1] != ':'):
            break  # 行注释开始，丢弃余下
        out.append(c)
        i += 1
    return "".join(out).rstrip()


def gen_classic_extras(p, inputs, compute, rows, primary, num_ids=None, diff_fields=None):
    """生成经典模式 __xExtras 函数文本（行列表）。apply_page() 与历史缺陷修复脚本共用，
    保证「重生成」与「新生成」同源。函数自包含（Raw/Restore 均为局部声明），
    修复脚本可单独替换整个 Extras 块。"""
    num_ids = set(num_ids or [])
    js = []
    js.append("function __%sExtras(){" % p)
    # 原始值读取（select/checkbox/列表粘贴输入用；parseFloat 会丢列表与文本）
    js.append("    function __%sRaw(id){var e=document.getElementById(id);if(!e)return '';var t=(e.type||'').toLowerCase();if(t==='checkbox'||t==='radio')return e.checked?(e.value||'1'):'';return e.value==null?'':e.value;}" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    # 重跑计算（复用页面赋值段）；const/let 转 var 避免重复声明（如同名系数数组与输入）
    for line in compute.splitlines():
        line = line.strip()
        if line:
            line = re.sub(r'^(const|let)\b', 'var', line)
            # 行内 if/else 块中的 const/let → var：块级声明在 Extras 顶层不可达
            # （dilution-c1v1 真案例：`if(...){ const V=...; }` 致 record 的 V:V
            #  ReferenceError → 整表+记录死）。要求后跟 `标识符=` 防误伤对象属性。
            line = re.sub(r'([{,]\s*)(const|let)\s+(\w+\s*=)', r'\1var \3', line)
            # 剥行内 // 注释：避免 // 吞掉同行后续代码（含收尾 }）致花括号不闭合
            line = _strip_js_line_comment(line)
            js.append("    " + line)
    # 守卫：数值输入 NaN 跳过；非数值输入（select/checkbox/列表）空值跳过
    if inputs:
        gp = []
        for i in inputs:
            if i in num_ids:
                gp.append("!isFinite(__%sNum('%s'))" % (p, i))
            else:
                gp.append("!__%sRaw('%s')" % (p, i))
        js.append("    if (%s) return;" % " || ".join(gp))
    js.append("    var en=TBKit.util.isEn();")
    # matrix 表
    js.append("    TBKit.matrix.table('#%sTable',{" % p)
    js.append("        head: en?['Item','Value']:['项目','数值'],")
    js.append("        rows: [")
    for val, lbl in rows:
        js.append("            [%r, %s]," % (lbl, val))
    js.append("        ]")
    js.append("    });")
    # history（输入字段 + 主结果；无输入页 rec 仅含主结果，避免前导逗号语法错误）
    rec_parts = ["%s:__%sRaw('%s')" % (i, p, i) for i in inputs]
    if primary:
        rec_parts.append("%s:%s" % (primary, primary))
    js.append("    TBKit.history.record({%s});" % ", ".join(rec_parts))
    # 回填：checkbox/radio 按勾选态还原（设 .value 不生效，曾致 restore 后状态丢失、
    # 重算结果与历史记录不符）；其余控件按值回填
    js.append("    function __%sRestore(rec){for(var k in rec){var e=document.getElementById(k);if(!e)continue;var t=(e.type||'').toLowerCase();if(t==='checkbox'||t==='radio'){e.checked=(String(e.value)===String(rec[k])||rec[k]==='1'||rec[k]===true);}else{e.value=rec[k];}}}" % p)
    js.append("    TBKit.history.mount('#%sHist',function(rec){ __%sRestore(rec); calcTool(); });" % (p, p))
    # diffBox：优先保留原页已有的对比字段（可能是派生量，如 __g0/dx），避免有损重生成丢
    # compare 特征（实测 quadratic-solver/slope-line 原 diff 在派生量上，primary 提取为 None
    # 致整行消失 → 基线 compare 掉分）。diff_fields 为空且 primary 存在时用 primary。
    _diff = diff_fields if diff_fields else ([primary] if primary else None)
    if _diff:
        js.append("    TBKit.util.diffBox('#%sDiff',[%s]);" % (p, ",".join("'%s'" % f for f in _diff)))
    js.append("}")
    return js

def _unsafe_nested_fn(cb):
    """compute 段（dataGrid 之前的赋值段）内的嵌套函数是否不可接线。

    旧规则对整个 calc 体做 `function \\w+(` 存在性检查 → 两处误杀：
      ① dataGrid 之后才定义函数的页（circular-permutation / multinomial-coefficient）
         本可安全接线却被跳过；
      ② 纯计算辅助函数（fmt / isPrime / npv / erf / 格式解析器）被一刀切跳过，
         页内 compute 调用它们 → 若丢弃则 ReferenceError 被 try/catch 吞掉、表静默死。
    新规则：只检查 compute 段，且只有会二次渲染结果区的函数（dataGrid/setResult/
    innerHTML/写 #res）才判不安全；其余由 extract() 原样保留。"""
    gi = cb.find('dataGrid(')
    region = cb[:cb.rfind('\n', 0, gi) + 1] if gi >= 0 else cb
    for m in re.finditer(r'^function\s+\w+\s*\(', region, re.M):
        i = region.find('{', m.start())
        if i < 0:
            return True
        depth, j = 1, i + 1
        while j < len(region) and depth > 0:
            if region[j] == '{':
                depth += 1
            elif region[j] == '}':
                depth -= 1
            j += 1
        if depth > 0:
            return True          # 括号无法闭合 → 放弃
        blk = region[m.start():j]
        if re.search(r'dataGrid\(|setResult|innerHTML|getElementById\(\s*[\'"]res', blk):
            return True
    return False


def apply_page(page, dry=False):
    # 含嵌套函数定义的页：仅当该函数会二次渲染结果区才跳过（见 _unsafe_nested_fn）
    s0 = open(page, encoding='utf-8').read()
    cb = calc_body(s0)
    if cb and _unsafe_nested_fn(cb):
        return "skip:complex-nested-functions"
    info = extract(page)
    if info is None:
        # 经典模式（calcTool+dataGrid）不适用 → 尝试新架构手工页模式（calc+#result）
        r = apply_custom(page, dry=dry)
        if r:
            return r
        return "skip:no-calcTool/datagrid"
    # 已接线则跳过
    s0 = open(page, encoding='utf-8').read()
    if 'TBKit.matrix.table' in s0:
        return "skip:already-wired"
    name = os.path.splitext(os.path.basename(page))[0]
    p = name.replace('-', '_')   # JS 标识符安全前缀（DOM id 仍可用原名）
    pid = name
    inputs = info["inputs"]
    compute = info["compute"]
    rows = info["dg_rows"]
    primary = info["primary"]

    # 取输入默认值
    defaults = {}
    for iid in inputs:
        m = re.search(r'<(?:input|select|textarea)[^>]*\bid="%s"[^>]*\bvalue="([^"]*)"' % re.escape(iid), s0)
        defaults[iid] = m.group(1) if m else ""
    # 预设值变体（数值缩放）
    def scale(v, f):
        try:
            return str(round(float(v)*f, 4)).rstrip('0').rstrip('.')
        except:
            return v
    presets = []
    presets.append({"label": "默认", "labelEn": "Default",
                    "values": {i: defaults[i] for i in inputs}})
    presets.append({"label": "示例 2×", "labelEn": "Example 2×",
                    "values": {i: scale(defaults[i], 2) for i in inputs}})
    presets.append({"label": "示例 0.5×", "labelEn": "Example 0.5×",
                    "values": {i: scale(defaults[i], 0.5) for i in inputs}})

    js = []
    js.append("function __%sNum(id){var e=document.getElementById(id);var v=e?parseFloat(e.value):NaN;return isFinite(v)?v:NaN;}" % p)
    js.extend(gen_classic_extras(p, inputs, compute, rows, primary, info.get("num_ids")))
    # export
    js.append("function __%sExport(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    js.append("    try { TBKit.util.exportTable('#%sTable','%s.csv'); } catch(e){}" % (p, name))
    js.append("}")
    # presets
    js.append("function __%sPresets(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    js.append("    TBKit.preset.bar('#%sPresets',[" % p)
    for pr in presets:
        vals = ", ".join("%s:'%s'" % (k, v) for k, v in pr["values"].items())
        js.append("        {label:%r,labelEn:%r,values:{%s}}," % (pr["label"], pr["labelEn"], vals))
    js.append("    ],function(){ calcTool(); });")
    js.append("}")
    # wrapper + boot
    js.append("var __tb_fn0 = calcTool;")
    js.append("calcTool = function(){ __tb_fn0(); try{ __%sExtras(); }catch(e){} };" % p)
    js.append("function __%sBoot(){ try{ __%sPresets(); }catch(e){} try{ calcTool(); }catch(e){} }" % (p, p))
    js.append("if (document.readyState && document.readyState !== 'loading') __%sBoot();" % p)
    js.append("else document.addEventListener('DOMContentLoaded', __%sBoot);" % p)
    js_code = "\n".join(js)

    # HTML 注入
    s = s0
    # 1) 导出按钮：在 重置 按钮后
    s = s.replace('<button class="btn" onclick="resetForm()">重置</button>',
                  '<button class="btn" onclick="resetForm()">重置</button>\n      <button class="btn" onclick="__%sExport()">导出明细 CSV</button>' % p, 1)
    # 2) 预设容器：在 <div class="toolbar"> 前
    s = s.replace('<div class="toolbar">', '<div id="%sPresets"></div>\n\n    <div class="toolbar">' % p, 1)
    # 3) 结果容器：在 result-box 后
    s = s.replace('<div class="result-box" id="result"></div>',
                  '<div class="result-box" id="result"></div>\n    <div id="%sTable"></div>\n    <div id="%sDiff"></div>\n    <div id="%sHist"></div>' % (p, p, p), 1)
    # 4) 脚本注入：在最后一个「真 JS 内联块」的 </script> 前
    #    必须跳过 application/ld+json 等非 JS 块（注进去浏览器不执行=死代码）
    pos = last_js_script_close(s)
    if pos == -1:
        return "skip:no-js-script"
    s = s[:pos] + "\n" + js_code + "\n" + s[pos:]

    if dry:
        return "DRY ok: inputs=%s primary=%s rows=%d" % (inputs, primary, len(rows))
    open(page, 'w', encoding='utf-8').write(s)
    # EN 字典补 导出明细 CSV
    en_path = page.replace('/tools/', '/i18n/tools/en/').replace('.html', '.json')
    if os.path.isfile(en_path):
        try:
            d = json.load(open(en_path, encoding='utf-8'))
            mp = d.get("map", {})
            if "导出明细 CSV" not in mp:
                mp["导出明细 CSV"] = "Export detail CSV"
                d["map"] = mp
                json.dump(d, open(en_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        except Exception as e:
            return "written-but-en-json-err:%s" % e
    return "applied"

def gen_custom_render(p, fn):
    """生成 custom 模式 __pRender 函数文本（行列表）。apply_custom() 与历史缺陷修复脚本
    共用。回填对 checkbox/radio 按勾选态还原（设 .value 不生效，曾致 restore 后状态
    丢失、重算结果与历史记录不符）。"""
    js = []
    js.append("function __%sRender(keys,rk,en){" % p)
    js.append("    try{")
    js.append("        var arr=TBKit.history.list().slice(0,10);")
    js.append("        var head=[en?'Time':'时间'].concat(keys).concat([rk]);")
    js.append("        var rows=arr.map(function(it){")
    js.append("            var row=[__%sTime(it.t)];" % p)
    js.append("            for(var i=0;i<keys.length;i++){var v=it.d[keys[i]];row.push(v==null?'':v);}")
    js.append("            var r=it.d[rk];row.push(r==null?'':r);")
    js.append("            return row;")
    js.append("        });")
    js.append("        TBKit.matrix.table('#%sTable',{head:head,rows:rows});" % p)
    js.append("        TBKit.util.diffBox('#%sDiff');" % p)
    js.append("        TBKit.history.mount('#%sHist',function(rec){" % p)
    js.append("            __%s_skip=true;" % p)
    js.append("            try{")
    js.append("                for(var k in rec){")
    js.append("                    if(k===rk) continue;")
    js.append("                    var e=document.getElementById(k);")
    js.append("                    if(!e) continue;")
    js.append("                    var t=(e.type||'').toLowerCase();")
    js.append("                    if(t==='checkbox'||t==='radio'){e.checked=(String(e.value)===String(rec[k])||rec[k]==='1'||rec[k]===true);}")
    js.append("                    else{e.value=rec[k];}")
    js.append("                }")
    js.append("                %s();" % fn)
    js.append("            }catch(e2){}")
    js.append("            __%s_skip=false;" % p)
    js.append("        });")
    js.append("        var nums=[],labels=[];")
    js.append("        for(var j=arr.length-1;j>=0;j--){")
    js.append("            var v=parseFloat(arr[j].d[rk]);")
    js.append("            if(isFinite(v)){nums.push(v);labels.push(__%sTime(arr[j].t));}" % p)
    js.append("        }")
    js.append("        if(nums.length>=2){")
    js.append("            TBKit.chart.line('#%sChart',{labels:labels,series:[{name:en?'Result trend':'结果趋势',data:nums}]});" % p)
    js.append("        }")
    js.append("    }catch(e3){}")
    js.append("}")
    return js

def apply_custom(page, dry=False):
    """新架构手工页接线：包装顶层 calc 函数，calc 后快照输入+结果摘要，
    经 TBKit 落 history/matrix/diffBox/chart/preset/export。全部 try 包裹，
    TBKit 缺失时静默跳过，不触碰页面核心计算。"""
    s0 = open(page, encoding='utf-8').read()
    info = extract_custom(page)
    if info is None:
        return None
    name = os.path.splitext(os.path.basename(page))[0]
    p = name.replace('-', '_')
    fn = info["fn"]
    defaults = info["defaults"]
    container = info["container"]

    js = []
    js.append("var __%s_last=0,__%s_skip=false;" % (p, p))
    # 输入快照（checkbox/radio 取勾选态，排除按钮/隐藏域）
    js.append("function __%sSnap(){" % p)
    js.append("    var out={};")
    js.append("    var els=document.querySelectorAll('input[id],select[id],textarea[id]');")
    js.append("    for(var i=0;i<els.length;i++){")
    js.append("        var e=els[i];")
    js.append("        var t=(e.type||'').toLowerCase();")
    js.append("        if(t==='button'||t==='submit'||t==='hidden') continue;")
    js.append("        var v=(t==='checkbox'||t==='radio')?(e.checked?(e.value||'1'):''):e.value;")
    js.append("        if(v!==''&&v!=null) out[e.id]=v;")
    js.append("    }")
    js.append("    return out;")
    js.append("}")
    # 结果摘要文本（结果容器 textContent；占位/报错态返回空 → 不记录）
    js.append("function __%sResText(){" % p)
    if container[0] == "id":
        js.append("    var r=document.getElementById('%s');" % container[1])
    else:
        js.append("    var r=document.querySelector('.%s');" % container[1])
    js.append("    if(!r) return '';")
    js.append("    var t=(r.textContent||'').replace(/\\s+/g,' ').trim();")
    js.append("    if(!t||t==='--'||t==='—'||t==='-') return '';")
    js.append("    if(/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';")
    js.append("    return t.slice(0,80);")
    js.append("}")
    js.append("function __%sTime(t){" % p)
    js.append("    var d=new Date(t);")
    js.append("    function q(x){return (x<10?'0':'')+x;}")
    js.append("    return q(d.getMonth()+1)+'-'+q(d.getDate())+' '+q(d.getHours())+':'+q(d.getMinutes());")
    js.append("}")
    # 渲染：明细表 + 与上次相比 + 历史面板 + 趋势图
    js.extend(gen_custom_render(p, fn))
    # extras：快照 + 记录（1s 防抖 + 同参去重）+ 渲染
    js.append("function __%sExtras(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    js.append("    if (__%s_skip) return;" % p)
    js.append("    var snap=__%sSnap();" % p)
    js.append("    var keys=Object.keys(snap);")
    js.append("    if(!keys.length) return;")
    js.append("    if(keys.length>12) keys=keys.slice(0,12);")
    js.append("    var res=__%sResText();" % p)
    js.append("    if(!res) return;")
    js.append("    var en=TBKit.util.isEn();")
    js.append("    var rk=en?'Result':'结果';")
    js.append("    var now=Date.now();")
    js.append("    if(now-__%s_last<1000) return;" % p)
    js.append("    var last=null;")
    js.append("    try{ last=TBKit.history.last(); }catch(e){}")
    js.append("    if(last){")
    js.append("        var same=true;")
    js.append("        for(var i=0;i<keys.length;i++){")
    js.append("            if(String(last[keys[i]])!==String(snap[keys[i]])){same=false;break;}")
    js.append("        }")
    js.append("        if(same&&String(last[rk])===String(res)) return;")
    js.append("    }")
    js.append("    __%s_last=now;" % p)
    js.append("    var rec={};")
    js.append("    for(var i=0;i<keys.length;i++) rec[keys[i]]=snap[keys[i]];")
    js.append("    rec[rk]=res;")
    js.append("    TBKit.history.record(rec);")
    js.append("    __%sRender(keys,rk,en);" % p)
    js.append("}")
    # 导出
    js.append("function __%sExport(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    js.append("    try { TBKit.util.exportTable('#%sTable','%s.csv'); } catch(e){}" % (p, name))
    js.append("}")
    # 预设（默认参数回填；键一律加引号——输入 id 可含连字符如 temp-slider，裸键会语法错）
    pv = ", ".join("'%s':'%s'" % (k, str(v).replace("'", "").replace("\\", "")[:40]) for k, v in defaults.items() if v != '')
    js.append("function __%sPresets(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    if pv:
        js.append("    TBKit.preset.bar('#%sPresets',[{label:'默认参数',labelEn:'Default',values:{%s}}],function(){ %s(); });" % (p, pv, fn))
    js.append("}")
    # 包装 + boot（typeof 守卫：calc 注入点不可见时不包装，绝不让 ReferenceError 杀死脚本块）
    js.append("var __%s_f0=(typeof %s==='function')?%s:null;" % (p, fn, fn))
    js.append("if(__%s_f0){" % p)
    js.append("    %s=function(){ var __r=__%s_f0.apply(null,arguments); try{ __%sExtras(); }catch(e){} return __r; };" % (fn, p, p))
    js.append("}")
    # boot：只挂预设，**不主动调 calc**——随机输出页（zalgo 等）的 harness 用种子随机数
    # 断言输出序列，Boot 多调一次 calc 会多消耗 RNG 抽数使期望值整体偏移（biz/zalgo-text
    # 139/139 → 2 失败即此因）。历史/表格在用户首次真实计算时自然渲染，无损体验。
    js.append("function __%sBoot(){ try{ __%sPresets(); }catch(e){} }" % (p, p))
    js.append("if (document.readyState && document.readyState !== 'loading') __%sBoot();" % p)
    js.append("else document.addEventListener('DOMContentLoaded', __%sBoot);" % p)
    js_code = "\n".join(js)

    if dry:
        return "DRY ok(custom): fn=%s defaults=%d" % (fn, sum(1 for v in defaults.values() if v))

    s = s0
    # 1) tool-kit.js 缺失则补（紧跟 tool-page-runtime.js）
    if 'tool-kit.js' not in s:
        s = s.replace('<script src="/js/tool-page-runtime.js" defer></script>',
                      '<script src="/js/tool-page-runtime.js" defer></script>\n<script src="/js/tool-kit.js" defer></script>', 1)
    # 2) 主按钮（onclick="fn(...)"）：前插预设容器、后插导出按钮
    m = re.search(r'<button\b[^>]*onclick="%s\([^)]*\)"[^>]*>.*?</button>' % re.escape(fn), s, re.S)
    if m:
        s = s[:m.start()] + '<div id="%sPresets"></div>' % p + s[m.start():]
        m2 = re.search(r'<button\b[^>]*onclick="%s\([^)]*\)"[^>]*>.*?</button>' % re.escape(fn), s, re.S)
        s = s[:m2.end()] + '<button class="btn" type="button" onclick="__%sExport()">导出明细 CSV</button>' % p + s[m2.end():]
    else:
        # 无主按钮（纯输入事件触发）：在结果容器前插独立导出行
        if container[0] == "id":
            rp = s.find('id="%s"' % container[1])
            op = s.rfind('<', 0, rp)
        else:
            cm = re.search(r'<\w+\b[^>]*class="[^"]*\b%s\b' % re.escape(container[1]), s)
            if not cm:
                return "skip:custom-result-class-not-found"
            op = cm.start()
        s = s[:op] + '<div class="toolbar" style="margin:8px 0;"><button class="btn" type="button" onclick="__%sExport()">导出明细 CSV</button></div>' % p + s[op:]
    # 3) 结果容器：在结果元素闭合后
    if container[0] == "id":
        rp = s.find('id="%s"' % container[1])
        op = s.rfind('<', 0, rp)
    else:
        cm = re.search(r'<\w+\b[^>]*class="[^"]*\b%s\b' % re.escape(container[1]), s)
        if not cm:
            return "skip:custom-result-class-not-found"
        op = cm.start()
    close_idx = find_tag_close(s, op)
    if close_idx is None:
        return "skip:custom-result-tag-unmatched"
    containers = '<div id="%sTable"></div> <div id="%sDiff"></div> <div id="%sChart"></div> <div id="%sHist"></div>' % (p, p, p, p)
    s = s[:close_idx] + ' ' + containers + s[close_idx:]
    # 4) 脚本注入：在最后一个「真 JS 内联块」的 </script> 前
    #    必须跳过 application/ld+json 等非 JS 块（注进去浏览器不执行=死代码）
    pos = last_js_script_close(s)
    if pos == -1:
        return "skip:custom-no-js-script"
    s = s[:pos] + "\n" + js_code + "\n" + s[pos:]

    open(page, 'w', encoding='utf-8').write(s)
    # EN 字典补 导出明细 CSV
    en_path = page.replace('/tools/', '/i18n/tools/en/').replace('.html', '.json')
    if os.path.isfile(en_path):
        try:
            d = json.load(open(en_path, encoding='utf-8'))
            mp = d.get("map", {})
            if "导出明细 CSV" not in mp:
                mp["导出明细 CSV"] = "Export detail CSV"
                d["map"] = mp
                json.dump(d, open(en_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        except Exception as e:
            return "written-but-en-json-err:%s" % e
    return "applied(custom)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cat', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--page', default=None)
    args = ap.parse_args()
    d = os.path.join(TOOLS, args.cat)
    if not os.path.isdir(d):
        print("no such cat", d); sys.exit(1)
    files = sorted(f for f in os.listdir(d) if f.endswith('.html') and f != 'index.html')
    stats = {"applied":0,"skip":0,"fail":0}
    for fn in files:
        if args.page and fn != args.page + '.html':
            continue
        page = os.path.join(d, fn)
        try:
            r = apply_page(page, dry=not args.apply)
        except Exception as e:
            stats["fail"] += 1
            print("FAIL %s: %s" % (fn, e))
            continue
        if r.startswith("applied") or r.startswith("DRY"):
            stats["applied"] += 1
            print(("APPLY " if args.apply else "DRY  ") + fn + " -> " + r)
        else:
            stats["skip"] += 1
            print("SKIP " + fn + " -> " + r)
    print("STATS", stats)

if __name__ == "__main__":
    main()
