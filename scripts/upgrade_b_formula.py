# -*- coding: utf-8 -*-
"""P4 增强（补刀）：修复 inject_formula_auto 的提取 bug 后，重新提取被漏抓的 B 级真公式工具并升级为 A 级。

原 bug：inject_formula_auto.extract_eq 使用的 vis_text() 把所有空白压成一行，
导致 EQ 正则 .{2,60} 贪婪吞掉整段可见文本（远超 60 字符）而被拒绝 —— B-OPT7 那次
"268 个注入"严重漏抓。本脚本修正提取（按句/行/分号切分 + 右侧数学算子校验），
并把两类 B 级真公式工具升级为 A 级：

  1) h2 公式工具：页面用 <h2>公式</h2> 展示公式（生成器约定），但缺 .formula-box 组件。
     → 把该 <h2> 原地替换为 <div class="formula-box"><div class="formula-eq">公式</div></div>。
     （不重复新增，仅替换原 h2 显示，避免公式出现两次）

  2) 正文公式工具：公式在可见正文里（非 h2），且属于公式域、有 function calc。
     → 复用 inject_formula_box.inject() 在 intro <p> 之后注入 .formula-box。

幂等：已含 formula-box 则跳过。classify_quality 见 formula-box → A。

用法：
  python3 scripts/upgrade_b_formula.py --dry-run     # 打印全部候选 + 即将注入的公式
  python3 scripts/upgrade_b_formula.py               # 执行注入/替换
"""
import os, re, sys, json, html, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inject_formula_box import inject as inject_fb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")
TOOLS = json.load(open(os.path.join(ROOT, "json", "tools.json"), encoding="utf-8"))

# ---- 提取规则（修复版）----
VAGUE = re.compile(r'(基准值|基准 ?值|指标加权|预测值 = 基准|学习参考|仅供|实际用药|遵医嘱|仅供参考|同时展示差值|稳定性指数综合考虑|留头甩头|复制结果|清空|📋|查询记录|计算历史|计算报告|输入数据|计算评分|输入时请注意|输入时|评分|分级|量表|计算 |总分|平均分)')
EQ = re.compile(
    r'([A-Za-z0-9_.\u4e00-\u9fff\u03b1-\u03c9\u00b2\u00b3\u207f\u221a\u03c0\u03c3\u0394\u2211\u222b\u2202\u03bb\u03bc\u03c1\u03b8\u03b1\u03b2\u03b3\u03c9\u03c6\u03b7\u03c4\u00d7\u00f7\u00b1\u2264\u2265\u2248%]+\s*[=\uff1d\u2248\u2261]\s*.{2,60})')
# 右侧必须含"真实数学结构"：算子（不含裸 /，单位斜杠 mmol/L 会误判）+ 希腊字母 + 上下标。
# 裸 / 排除：避免 "LT=血乳酸...1.0mmol/L 时的心率" 这类单位斜杠被当成除法算子。
RIGHTMATH = re.compile(r'[+\-×÷√\^()\u00b7]|[\u03b1-\u03c9\u0391-\u03a9]|\u00b2|\u00b3')
EXAMPLE = re.compile(r'(→|示例|例如|如：|例如：|算例|举例|假设)')
H2 = re.compile(r'<h2[^>]*>(.*?)</h2>', re.S)
# 尾部中文说明切割点：逗号/分号/全角括号/「或」/闭括号后接中文/空格+中文动词
TRAIL = re.compile(r'[，；;（]\s*[^=]*$|或.*$|[）)]\s*[\u4e00-\u9fff].*$|[ \u3000][\u4e00-\u9fff]?(计算|据此|其中|表示|反映|评估|判定|说明|可选).*$')

# 手动覆盖：提取结果不干净或截断时，用人工核定的标准公式
OVERRIDE = {
    ("optical", "microscope-magnification"): "M = (L/f₀)(D/fₑ)",
    ("optical", "lens-maker"): "f = (n-1)(1/R₁ - 1/R₂)",
    ("science", "variance-calculator"): "σ² = Σ(xᵢ − x̄)² / N",
    ("automotive", "calc-1"): "t ≈ ½·m·v² / (P·η)",
}
# 明确跳过的脏乱页（提取出乱码/非公式）
DENY = {
    ("optical", "checker-stress"),
    ("optical", "frame-pupillary"),
    ("civil", "calc-1"),
}

def vis_text(c):
    c = re.sub(r'<script.*?</script>', '', c, flags=re.S)
    c = re.sub(r'<style.*?</style>', '', c, flags=re.S)
    c = re.sub(r'<[^>]+>', ' ', c)
    return c  # 不折叠空白

def extract_eq(c):
    v = vis_text(c)
    segs = re.split(r'[。！？\n\r；;]', v)
    best = None
    for seg in segs:
        seg = seg.strip()
        if not seg:
            continue
        for m in EQ.finditer(seg):
            s = m.group(1).strip()
            if len(s) < 6 or len(s) > 55:
                continue
            if VAGUE.search(s) or EXAMPLE.search(s):
                continue
            # 切掉尾部中文说明
            s = TRAIL.sub('', s).strip()
            if len(s) < 5:
                continue
            eqpos = re.search(r'[=\uff1d\u2248\u2261]', s)
            if not eqpos:
                continue
            rhs = s[eqpos.end():]
            if not RIGHTMATH.search(rhs):
                continue
            if best is None or len(s) > len(best):
                best = s
    return best

def h2_formula(c):
    """返回页面中第一个含公式的 h2 纯文本（无则 None）。"""
    for m in H2.finditer(c):
        txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if re.search(r'[=\uff1d\u2248\u2261\u2245]', txt) and (RIGHTMATH.search(txt) or re.search(r'[\u03b1-\u03c9\u0391-\u03a9\u00b2\u00b3\u221a\u03c0]', txt)):
            return txt
    return None

FORMULA_DOMAINS = set("""
signal quantum metrology aerospace kinematics nuclear optics optical structural geometry
economics securities banking tax insurance accounting surveying energy meteorology realestate
sports math robotics geology investment science hydraulic fire machinery metalwork fishery
procurement language legal statistics fluid thermodynamics dynamics
electromagnetism materials acoustics chemistry civil automotive electrical ballistics
metallurgy textile process quality packaging paper glass paint cable pipe dailychem chemical
seismology astronomy geophysics hydrology railway maritime
""".split())

def load(t):
    p = t.get('path') or t.get('file')
    fp = os.path.join(TOOLS_DIR, p)
    if not os.path.exists(fp):
        return None
    return open(fp, encoding='utf-8').read()

def candidates():
    """返回 (kind, industry, slug, eq_or_h2text) 列表。kind: 'h2' | 'body'。"""
    out = []
    for t in TOOLS:
        if t.get('quality') != 'B':
            continue
        c = load(t)
        if not c:
            continue
        if 'formula-box' in c or 'TOOLBOX-REDIRECT' in c:
            continue
        ind = t.get('industry')
        slug = t.get('slug') or os.path.basename(t.get('path', '')).replace('.html', '')
        key = (ind, slug)
        if key in DENY:
            continue
        # 1) h2 公式优先（任意域，公式显式展示，高置信）
        h2f = h2_formula(c)
        if h2f:
            out.append(('h2', ind, slug, OVERRIDE.get(key, h2f)))
            continue
        # 2) 正文公式（仅公式域 + 有 function calc）
        if ind not in FORMULA_DOMAINS:
            continue
        if 'function calc' not in c:
            continue
        eq = OVERRIDE.get(key) or extract_eq(c)
        if eq:
            out.append(('body', ind, slug, eq))
    return out

def upgrade_h2(ind, slug, eq):
    fp = os.path.join(TOOLS_DIR, ind, slug + '.html')
    if not os.path.exists(fp):
        return 'missing'
    c = open(fp, encoding='utf-8').read()
    if 'formula-box' in c:
        return 'skip'
    # 替换第一个含公式的 h2
    def repl(m):
        txt = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if re.search(r'[=\uff1d\u2248\u2261\u2245]', txt) and (RIGHTMATH.search(txt) or re.search(r'[\u03b1-\u03c9\u0391-\u03a9\u00b2\u00b3\u221a\u03c0]', txt)):
            fb = ('\n    <div class="formula-box">\n'
                  '      <div class="formula-title">📐 计算公式</div>\n'
                  '      <div class="formula-eq">%s</div>\n'
                  '    </div>' % html.escape(txt))
            return fb
        return m.group(0)
    c2, n = H2.subn(repl, c, count=1)
    if n == 0:
        return 'no-h2'
    open(fp, 'w', encoding='utf-8').write(c2)
    return 'ok'

def upgrade_body_fallback(ind, slug, eq):
    """no-intro 兜底：公式不在标准 intro <p> 内，而是显示于 .formula-display /
    .formula / .info-box 等元素中。改为主动注入：在第一个 <h2> 之后插入
    .formula-box（公式用 candidates() 已提取好的 eq），不依赖正文 <p> 含公式，
    避免漏抓。classify_quality 见 formula-box → A。"""
    fp = os.path.join(TOOLS_DIR, ind, slug + '.html')
    if not os.path.exists(fp):
        return 'missing'
    c = open(fp, encoding='utf-8').read()
    if 'formula-box' in c:
        return 'skip'
    if not eq:
        return 'no-eq'
    H2TAG = re.compile(r'(<h2[^>]*>.*?</h2>)', re.S)
    m = H2TAG.search(c)
    if not m:
        return 'no-h2'
    fb = ('\n    <div class="formula-box">\n'
          '      <div class="formula-title">📐 计算公式</div>\n'
          '      <div class="formula-eq">%s</div>\n'
          '    </div>' % html.escape(eq))
    c2 = c[:m.end()] + fb + c[m.end():]
    open(fp, 'w', encoding='utf-8').write(c2)
    return 'ok-fallback'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    cands = candidates()
    print("候选总数: %d  (h2=%d, body=%d)" % (
        len(cands), sum(1 for x in cands if x[0] == 'h2'), sum(1 for x in cands if x[0] == 'body')))
    if args.dry_run:
        for kind, ind, slug, eq in cands:
            print("  [%s] %s/%s  ::  %s" % (kind, ind, slug, eq))
        return
    stats = {}
    for kind, ind, slug, eq in cands:
        if kind == 'h2':
            r = upgrade_h2(ind, slug, eq)
        else:
            r = inject_fb(ind, slug, eq)
            if r == 'no-intro':
                r = upgrade_body_fallback(ind, slug, eq)
        stats[r] = stats.get(r, 0) + 1
    print("执行结果:", stats)

if __name__ == "__main__":
    main()
