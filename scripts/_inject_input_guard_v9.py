#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""输入校验前置注入器 v9（治本版）

背景：v8 输出守卫只在结果区把 NaN/Infinity 换成「⚠ 计算结果含无效值，请检查输入是否为
有效正数。」——它遮住了症状，没修根因。根因是页面缺少**语义化输入校验**：
  · 除数为 0（用户把某个输入清空/填 0，而它恰好是分母）
  · 输入为空或非数字（`num()` 之类 helper 静默兜底成 0，把错误藏起来）
结果就是用户只看到一句无信息量的告警，不知道该改哪个框。

本注入器在 calc 入口函数体最前面插入一段校验：
  1. 收集该页所有参与计算的数值/文本输入
  2. 空值/非数字 → 明确指出「请填写 <label>」并在首个出错的输入框加红框
  3. 全零（分母必然为 0）→ 明确提示「分母不能为 0」
校验通过才执行原逻辑，页面公式本身一字不改（不碰已验证的数学）。

用法：
  python3 scripts/_inject_input_guard_v9.py --list <slug清单> [--dry] [--skip <清单>]
  python3 scripts/_inject_input_guard_v9.py --slug <行业/slug> [--dry]
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')

# 校验失败时的提示模板（语义化，替代 v8 的通用告警）
MSG_EMPTY = '<p style="color:var(--danger)">⚠ 请填写「%s」后再计算。</p>'
MSG_ZERO = '<p style="color:var(--danger)">⚠ 输入不能全为 0：至少需要一项非零数值，否则计算无意义。</p>'
MSG_DENOM = '<p style="color:var(--danger)">⚠ 「%s」是本计算的分母，不能为 0。</p>'

# 注入的校验函数名（幂等键）
FN_NAME = '__tbInputGuard'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, s):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)


def skip_string(html, i, n):
    """跳过 JS 字符串字面量（含转义），返回结束后的下标或 None"""
    q = html[i]
    i += 1
    while i < n:
        c = html[i]
        if c == '\\':
            i += 2
            continue
        if c == q:
            return i + 1
        i += 1
    return None


def skip_comment(html, i, n):
    if html.startswith('//', i):
        j = html.find('\n', i)
        return j if j >= 0 else n
    if html.startswith('/*', i):
        j = html.find('*/', i + 2)
        return j + 2 if j >= 0 else n
    return i


def match_brace(html, start, n):
    """start 指向 '{'，返回配对 '}' 之后的下标；跳过字符串与注释、模板串、正则字面量"""
    depth = 0
    i = start
    while i < n:
        i = skip_comment(html, i, n)
        if i >= n:
            return None
        c = html[i]
        if c in '"\'':
            j = skip_string(html, i, n)
            if j is None:
                return None
            i = j
            continue
        if c == '`':
            # 模板串：逐字符扫，跳过 ${ } 内的嵌套
            i += 1
            while i < n:
                if html[i] == '\\':
                    i += 2
                    continue
                if html[i] == '`':
                    i += 1
                    break
                if html[i] == '$' and i + 1 < n and html[i + 1] == '{':
                    e = match_brace(html, i + 1, n)
                    if e is None:
                        return None
                    i = e
                    continue
                i += 1
            continue
        if c == '/' and i + 1 < n and html[i + 1] == '/':
            j = html.find('\n', i)
            i = j if j >= 0 else n
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None


def find_calc_entry(html):
    """返回 (func_name, body_open_brace_idx)；找不到返回 (None, None)

    口径：优先取 onclick 上直接调用的具名函数（按钮「计算」绑定的那个），
    其次取名字里带 calc/compute 的定义。裸 `function calc(` 也要覆盖。
    """
    n = len(html)
    # 1) onclick="xxx(" 且 xxx 名含 calc/计算语义
    best = None
    for m in re.finditer(r'onclick\s*=\s*["\']\s*([A-Za-z_$][\w$]*)\s*\(', html):
        name = m.group(1)
        if re.search(r'calc|compute|calculate|update|result', name, re.I):
            best = name
            break
    if best is None:
        for m in re.finditer(r'onclick\s*=\s*["\']\s*([A-Za-z_$][\w$]*)\s*\(', html):
            best = m.group(1)
            break
    # 2) 定义处取函数体（function 声明 + 箭头函数/函数表达式赋值）
    cands = []
    if best:
        cands.append(best)
    for m in re.finditer(r'function\s+([A-Za-z_$][\w$]*)\s*\(', html):
        nm = m.group(1)
        if nm == FN_NAME:
            continue
        if re.search(r'calc|compute|calculate|update|result', nm, re.I):
            cands.append(nm)
    seen = set()
    for name in cands:
        if name in seen:
            continue
        seen.add(name)
        m = re.search(r'function\s+' + re.escape(name) + r'\s*\(', html)
        if m:
            op = html.find('{', m.end())
        else:
            # window.calc = function(){...} / const calc = () => {...} / const calc = function(){...}
            pats = [
                r'(?:window|globalThis|self)\s*\.\s*' + re.escape(name) + r'\s*=\s*(?:async\s*)?function\s*\([^)]*\)\s*\{',
                r'(?:const|let|var)\s+' + re.escape(name)
                + r'\s*=\s*(?:async\s*)?(?:function\s*)?\([^)]*\)\s*=>\s*\{',
                r'(?:const|let|var)\s+' + re.escape(name)
                + r'\s*=\s*(?:async\s*)?function\s*\([^)]*\)\s*\{',
            ]
            m2 = None
            for pt in pats:
                m2 = re.search(pt, html)
                if m2:
                    break
            if not m2:
                continue
            op = html.find('{', m2.end() - 1)
        if op < 0:
            continue
        cl = match_brace(html, op, n)
        if cl is None:
            continue
        # 校验：函数体里确有除法/算术（避免把纯 UI 函数当计算入口）
        body = html[op:cl]
        if not re.search(r'[-+*/%]|\bMath\.', body):
            continue
        return name, op
    return None, None


def collect_inputs(html, cut, calc_src=''):
    """收集参与计算的输入控件：[(id, label, type, required)]

    required 判定（决定是否做「空值必须填写」校验）：
      · 有 value= 属性 ⇒ 页面给了默认数值，参与计算 ⇒ 必填
      · 只有 placeholder、无 value ⇒ 可选输入（如「时间码」「目标时长(秒)」这类
        二选一的辅助输入），页面自己用 `||0` / `if(==='')` 兜底 ⇒ **不校验空值**
    这一条是必须的：v9 第一版把所有 input 都当必填，把 video-speed 这类
    「主输入 + 可选辅助输入」页面的正常用法误拦成「请填写『时间码』」。
    """
    body = html[:cut] if cut > 0 else html
    out = []
    for m in re.finditer(r'<(input|textarea)\b([^>]*)>', body):
        attrs = dict(re.findall(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"', m.group(2)))
        idv = attrs.get('id')
        if not idv:
            continue
        typ = attrs.get('type', 'text').lower()
        if typ in ('checkbox', 'radio', 'file', 'hidden', 'submit', 'button', 'range', 'color'):
            continue
        lab = label_for(body, idv)
        has_value = 'value' in attrs and attrs.get('value', '') != ''
        is_text = typ not in ('number',)
        # 文本类即使有 value（如 SRT 示例）也允许清空；数值类有 value 才必填
        required = (typ == 'number' and has_value)
        out.append((idv, lab, typ, required))
    return out


def label_for(body, id):
    """取 <label for=id> 的文本；取不到就用 id 本身"""
    m = re.search(r'<label[^>]*\bfor\s*=\s*"' + re.escape(id) + r'"[^>]*>([\s\S]*?)</label>', body)
    if m:
        t = re.sub(r'<[^>]*>', '', m.group(1))
        t = t.replace('*', '').strip()
        t = re.sub(r'\s*[:：]\s*$', '', t).strip()
        if t:
            return t
    # 退而求其次：input 前面最近的 label/文字
    m = re.search(r'<(?:label|div|span|b)[^>]*>\s*([^<>]{1,24}?)\s*(?:</[^>]+>)?\s*<input[^>]*\bid\s*=\s*"'
                  + re.escape(id) + r'"', body)
    if m:
        t = m.group(1).replace('*', '').strip()
        if t:
            return t
    return id


def build_guard_js(inputs, out_id, fname, denoms=None):
    """生成校验函数 + 入口前置调用"""
    ids = [i[0] for i in inputs]
    pairs = ', '.join("'%s'" % i for i in ids)
    labels = ', '.join(json_str(i[1]) for i in inputs)
    # 只有 required 的输入参与「空值」校验；可选输入仅参与「全零/分母」判定
    req_pairs = '[' + ', '.join("'%s'" % i[0] for i in inputs if len(i) > 3 and i[3]) + ']'
    out = json_str(out_id)
    denoms = denoms or []
    dlab = json_str({d['id']: d['label'] for d in denoms})
    denom_tpl = json_str(MSG_DENOM)
    js = f"""
function {FN_NAME}(_ids,_labels){{
  var __TPL='请填写「%s」后再计算。';
  var __TPL2={denom_tpl};
  var _vals=[],_firstBad=-1;
  var _REQ={req_pairs};
  for(var _i=0;_i<_ids.length;_i++){{
    var _e=document.getElementById(_ids[_i]);
    if(!_e) continue;
    var _raw=String(_e.value==null?'':_e.value).trim();
    var _num=parseFloat(_raw);
    var _need=(_REQ.indexOf(_ids[_i])>=0);
    if(_raw===''){{ if(_need&&_firstBad<0)_firstBad=_i; _vals.push(NaN); continue; }}
    if(_e.type==='number'||_e.tagName==='TEXTAREA'){{
      if(_need&&isNaN(_num)){{ if(_firstBad<0)_firstBad=_i; _vals.push(NaN); continue; }}
      _vals.push(_num);
    }} else _vals.push(_raw);
  }}
  if(_firstBad>=0){{
    var _bad=_firstBad;
    var _lbl=(_labels&&_labels[_bad])||_ids[_bad];
    var __msg=__TPL.replace('%s',_lbl);
    var _fe=document.getElementById(_ids[_bad]);
    if(_fe&&_fe.classList&&_fe.classList.add)_fe.classList.add('input-error');
    return __msg;
  }}
  // 分母项：__D 由真浏览器逐项置零探测得出，命中即说明该输入在此页作分母
  var __D={dlab};
  for(var _d=0;_d<_ids.length;_d++){{
    if(!(_ids[_d] in __D)) continue;
    var _de=document.getElementById(_ids[_d]);
    if(!_de) continue;
    if(_de.classList&&_de.classList.remove)_de.classList.remove('input-error');
    if(parseFloat(String(_de.value==null?'':_de.value).trim())===0){{
      if(_de.classList&&_de.classList.add)_de.classList.add('input-error');
      return __TPL2.replace('%s',__D[_ids[_d]]);
    }}
  }}
  // 全零：任何一项作分母都会得到 Infinity/NaN。页面公式本身没错，是输入无意义
  var _nums=[];
  for(var _z=0;_z<_vals.length;_z++){{ if(typeof _vals[_z]==='number'&&!isNaN(_vals[_z])) _nums.push(_vals[_z]); }}
  if(!_nums.length) return '';
  if(_nums.length>0){{
    var _allZero=true;
    for(var _z2=0;_z2<_nums.length;_z2++){{ if(_nums[_z2]!==0){{ _allZero=false; break; }} }}
    if(_allZero) return {json_str(MSG_ZERO)};
  }}
  for(var _k=0;_k<_ids.length;_k++){{
    var _e2=document.getElementById(_ids[_k]);
    if(_e2&&_e2.classList&&_e2.classList.remove)_e2.classList.remove('input-error');
  }}
  return '';
}}
"""
    call = f"  var __ig={FN_NAME}([{pairs}],[{labels}]);if(__ig){{ToolBox.setResult({out},__ig);return;}}\n"
    return js, call


def json_str(s):
    return json.dumps(s, ensure_ascii=False)


def find_out_id(html, cut):
    body = html[:cut] if cut > 0 else html
    for cid in ('result', 'output', 'res', 'resultBox', 'result-box', 'out', 'answer'):
        if re.search(r'id\s*=\s*"' + cid + r'"', body):
            return cid
    return 'result'


def syntax_ok(src):
    """node vm.Script 语法校验：只校验 <script> 块内的 JS（整页 HTML 不是 JS）"""
    blocks = re.findall(r'<script>([\s\S]*?)</script>', src)
    for b in blocks:
        if 'TOOLBOX-API-STUB' in b:
            continue
        js = 'new (require("vm").Script)(%s);' % json.dumps(b)
        p = subprocess.run(['node', '-e', js], capture_output=True, text=True)
        if p.returncode != 0:
            head = [l for l in p.stderr.split('\n') if 'Error' in l or '^' in l]
            return False, (' | '.join(head) or p.stderr)[:300]
    return True, ''


def transform(html, denoms=None):
    if FN_NAME in html:
        return html, 'ALREADY'
    fname, op = find_calc_entry(html)
    if not fname:
        return html, 'NO_CALC'
    cut = html.find('<!-- TOOLBOX-DEEP-DIVE -->')
    inputs = collect_inputs(html, cut)
    if not inputs:
        return html, 'NO_INPUT'
    out_id = find_out_id(html, cut)
    js, call = build_guard_js(inputs, out_id, fname, denoms)
    # 1) 在入口函数体开头（跳过空白与注释）插入校验调用
    k = op + 1
    n0 = len(html)
    while k < n0:
        c = html[k]
        if c in ' \t\r\n':
            k += 1
            continue
        nc = skip_comment(html, k, n0)
        if nc != k:
            k = nc
            continue
        break
    new = html[:k] + call + html[k:]
    # 2) 校验器函数插到 calc 段开头（在 <script> 内、入口定义之前）
    cut2 = new.find('<!-- TOOLBOX-DEEP-DIVE -->')
    m_script = None
    for mm in re.finditer(r'<script>([\s\S]*?)</script>', new):
        body = mm.group(1)
        if re.search(r'function\s+' + re.escape(fname) + r'\s*\(', body) \
           or re.search(r'\.\s*' + re.escape(fname) + r'\s*=\s*(?:async\s*)?function', body) \
           or re.search(r'(?:const|let|var)\s+' + re.escape(fname) + r'\s*=', body):
            if re.search(r'[-+*/%]|\bMath\.', body):
                m_script = mm
                break
    if not m_script:
        m_script = re.search(r'<script>([\s\S]*?)</script>', new)
    if not m_script:
        return html, 'NO_CALC'
    new = new[:m_script.start(1)] + js.lstrip('\n') + '\n' + new[m_script.start(1):]
    return new, 'OK'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list')
    ap.add_argument('--slug', action='append', default=[])
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--skip', default='')
    ap.add_argument('--denoms', help='probe_denoms.js 产出的 JSON，提供分母项')
    a = ap.parse_args()

    slugs = list(a.slug)
    if a.list:
        for line in read(a.list).split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                slugs.append(line)
    skip = {s.strip() for s in a.skip.split(',') if s.strip()}

    dmap = {}
    if a.denoms and os.path.exists(a.denoms):
        raw = json.loads(read(a.denoms))
        if isinstance(raw, dict):
            # {slug: [{id,label}, ...]}
            for slug, ds in raw.items():
                if ds:
                    dmap[slug] = ds
        else:
            # [{slug, denoms:[...]}, ...]
            for rec in raw:
                if isinstance(rec, dict) and rec.get('denoms'):
                    dmap[rec['slug']] = rec['denoms']
    cnt = {'OK': 0, 'ALREADY': 0, 'NO_CALC': 0, 'NO_INPUT': 0, 'FAIL': 0}
    for slug in slugs:
        if slug in skip:
            continue
        p = os.path.join(TOOLS, slug + '.html')
        if not os.path.exists(p):
            print('MISS', slug)
            continue
        src = read(p)
        new, st = transform(src, dmap.get(slug))
        if st == 'OK':
            ok, err = syntax_ok(new)
            if not ok:
                print('SYNTAX-FAIL', slug, err)
                cnt['FAIL'] += 1
                continue
        if st == 'OK' and not a.dry:
            write(p, new)
        cnt[st] = cnt.get(st, 0) + 1
        if st in ('NO_CALC', 'NO_INPUT'):
            print(st, slug)
    print('SUMMARY', cnt, 'dry' if a.dry else 'APPLIED')


if __name__ == '__main__':
    main()
