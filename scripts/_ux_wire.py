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
    # 整块删除 if/for/while/switch(...) {...} 控制流（括号匹配，避免悬挂开括号）
    pre = re.sub(r"\b(if|for|while|switch)\s*\([^()]*\)\s*\{[^}]*\}", "", pre, flags=re.S)
    # 去掉悬挂 const __gN=
    pre = re.sub(r"const\s+__g\d*\s*=\s*$", "", pre)
    # 合并续行 + 仅保留纯赋值行（丢弃残留控制流/return）
    keep = []
    for ln in pre.splitlines():
        st = ln.strip()
        if not st:
            continue
        if re.match(r"^(const|var|let)\b", st) and "setResult" not in st and "__tbInputGuard" not in st and "__ig" not in st:
            keep.append(st)
        elif keep and not re.match(r"^(const|var|let|if|for|while|switch|function|return|else|do|try|catch|throw|break|continue)\b", st):
            # 续行拼接：以 } ] ) 开头的闭合行，在上一行括号未闭合时（多行对象/数组字面量）必须拼回，
            # 否则会丢闭合括号产生语法错（如 const info={...} 跨行、闭合行独立成 `};`）。
            # 上一行已闭合（函数体闭合等）才丢弃。
            if st[0] in '}])' and bracket_depth(keep[-1]) <= 0:
                continue
            keep[-1] += " " + st
        # 其余（控制流/孤立续行）丢弃
    pre = "\n".join(keep)
    # primary 结果变量：第一个非输入的 const/var 赋值
    primary = None
    for mm in re.finditer(r"(?:const|var|let)\s+(\w+)\s*=", pre):
        v = mm.group(1)
        if v not in inputs and v not in ('__g1','__g2','__ig'):
            primary = v
            break
    return {"inputs": inputs, "compute": pre, "dg_rows": rows, "primary": primary}

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


def extract_custom(page):
    """新架构手工页模式：顶层 function <fn> + id="result" + 输入控件（无 calcTool/dataGrid）。
    返回 dict(fn, inputs, defaults) 或 None。fn 取按钮/输入事件回调中的顶层函数，
    优先 calc/compute/solve/count/estimate/eval 系命名。"""
    s = open(page, encoding='utf-8').read()
    if 'TBKit.matrix.table' in s:
        return None
    if not re.search(r'id="result"', s):
        return None
    cands = []
    for mm in re.finditer(r'on(?:click|input|change)="(\w+)\(', s):
        c = mm.group(1)
        if c not in cands:
            cands.append(c)
    fn = None
    for c in cands:
        if re.match(r'^(?:calc|compute|solve|count|estimate|eval|do)\w*$', c) and \
                re.search(r'^function\s+%s\s*\(' % re.escape(c), s, re.M):
            fn = c
            break
    if fn is None:
        for c in cands:
            if re.search(r'^function\s+%s\s*\(' % re.escape(c), s, re.M):
                fn = c
                break
    if fn is None:
        return None
    # 输入控件 id（input/select/textarea），去重保序，上限 12 防表过宽
    ids = []
    for mm in re.finditer(r'<(?:input|select|textarea)\b[^>]*\bid="([\w-]+)"', s):
        iid = mm.group(1)
        if re.search(r'\b(?:search|token|csrf|nonce)\b', iid, re.I):
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
    return {"fn": fn, "inputs": inputs, "defaults": defaults}


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

def apply_page(page, dry=False):
    # 含嵌套函数定义（erf/invNorm 等）的页：提取会打碎函数体、把局部 const 展平到同一作用域，
    # 导致「already been declared」或表格静默失效 → 跳过，留待手动 A 档精做（不破坏核心计算）。
    s0 = open(page, encoding='utf-8').read()
    cb = calc_body(s0)
    if cb and re.search(r'function\s+\w+\s*\(', cb):
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
    js.append("function __%sExtras(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    # 重跑计算（复用页面赋值段）；const/let 转 var 避免重复声明（如同名系数数组与输入）
    for line in compute.splitlines():
        line = line.strip()
        if line:
            line = re.sub(r'^(const|let)\b', 'var', line)
            js.append("    " + line)
    # 守卫：任一输入 NaN 则返回（无输入页跳过守卫，避免 if () 语法错误）
    if inputs:
        guard = " || ".join("!isFinite(__%sNum('%s'))" % (p, i) for i in inputs)
        js.append("    if (%s) return;" % guard)
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
    rec_parts = ["%s:__%sNum('%s')" % (i, p, i) for i in inputs]
    if primary:
        rec_parts.append("%s:%s" % (primary, primary))
    rec = ", ".join(rec_parts)
    js.append("    TBKit.history.record({%s});" % rec)
    restore = " ".join("if(rec.%s!=null)document.getElementById('%s').value=rec.%s;" % (i, i, i) for i in inputs)
    js.append("    TBKit.history.mount('#%sHist',function(rec){ %s calcTool(); });" % (p, restore))
    # diffBox
    if primary:
        js.append("    TBKit.util.diffBox('#%sDiff',['%s']);" % (p, primary))
    js.append("}")
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
    # 4) 脚本注入：在含 calcTool 的 <script> 末尾 </script> 前
    # 找最后一个 </script>（页面内联脚本）
    pos = s.rfind('</script>')
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
    # 结果摘要文本（#result textContent；占位/报错态返回空 → 不记录）
    js.append("function __%sResText(){" % p)
    js.append("    var r=document.getElementById('result');")
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
    js.append("                    if(e) e.value=rec[k];")
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
    # 预设（默认参数回填）
    pv = ", ".join("%s:'%s'" % (k, str(v).replace("'", "").replace("\\", "")[:40]) for k, v in defaults.items() if v != '')
    js.append("function __%sPresets(){" % p)
    js.append("    if (typeof TBKit === 'undefined') return;")
    if pv:
        js.append("    TBKit.preset.bar('#%sPresets',[{label:'默认参数',labelEn:'Default',values:{%s}}],function(){ %s(); });" % (p, pv, fn))
    js.append("}")
    # 包装 + boot（typeof 守卫：calc 注入点不可见时不包装，绝不让 ReferenceError 杀死脚本块）
    js.append("var __%s_f0=(typeof %s==='function')?%s:null;" % (p, fn, fn))
    js.append("if(__%s_f0){" % p)
    js.append("    %s=function(){ __%s_f0.apply(null,arguments); try{ __%sExtras(); }catch(e){} };" % (fn, p, p))
    js.append("}")
    js.append("function __%sBoot(){ try{ __%sPresets(); }catch(e){} try{ %s(); }catch(e){} }" % (p, p, fn))
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
        s = s[:m.start()] + '<div id="%sPresets"></div>\n      ' % p + s[m.start():]
        m2 = re.search(r'<button\b[^>]*onclick="%s\([^)]*\)"[^>]*>.*?</button>' % re.escape(fn), s, re.S)
        s = s[:m2.end()] + '\n      <button class="btn" type="button" onclick="__%sExport()">导出明细 CSV</button>' % p + s[m2.end():]
    else:
        # 无主按钮（纯输入事件触发）：在 #result 前插独立导出行
        rp = s.find('id="result"')
        op = s.rfind('<', 0, rp)
        s = s[:op] + '<div class="toolbar" style="margin:8px 0;"><button class="btn" type="button" onclick="__%sExport()">导出明细 CSV</button></div>\n    ' % p + s[op:]
    # 3) 结果容器：在 #result 元素闭合后
    rp = s.find('id="result"')
    op = s.rfind('<', 0, rp)
    close_idx = find_tag_close(s, op)
    if close_idx is None:
        return "skip:custom-result-tag-unmatched"
    containers = '<div id="%sTable"></div>\n    <div id="%sDiff"></div>\n    <div id="%sChart"></div>\n    <div id="%sHist"></div>' % (p, p, p, p)
    s = s[:close_idx] + '\n    ' + containers + s[close_idx:]
    # 4) 脚本注入：最后一个 </script> 前
    pos = s.rfind('</script>')
    if pos == -1:
        return "skip:custom-no-script"
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
