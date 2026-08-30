# -*- coding: utf-8 -*-
"""共享工具页模板 + 渲染函数。

Batch 6/7/8... 所有「专业公式计算器」生成器统一复用本模块，
保证页面结构、SEO 元数据、ToolBox.setResult 接线、质量门一致。

用法（在各自的 gen_xxx_tools.py 中）:
    from tool_template import main
    TOOLS = [ {...}, ... ]
    if __name__ == "__main__":
        main(TOOLS)
"""
import os

TOOLS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")

CAT_ZH = {
    "civil": "工程建造",
    "engineering": "工程计算",
    "mechanical": "机械工程",
    "electrical": "电气工程",
    "optical": "光学计算",
    "hydraulic": "流体力学",
    "science": "物理科学",
    "meteorology": "气象计算",
    "physics": "物理科学",
    "chemistry": "化学计算",
    "acoustics": "声学计算",
    "thermodynamics": "热力学",
    "signal": "信号与系统",
    "geometry": "几何测量",
    "electromagnetism": "电磁学",
    "structural": "结构工程",
    "astronomy": "天文计算",
    "materials": "材料科学",
    "kinematics": "运动学",
    "math": "数学计算",
    "robotics": "机器人学",
    "quantum": "量子物理",
    "optics": "光学计算",
    "nuclear": "核物理",
    "dynamics": "动力学",
    "fluid": "流体力学",
    "economics": "经济学",
    "banking": "银行学",
    "tax": "税务计算",
    "process": "过程能力",
    "metrology": "计量学",
    "investment": "投资分析",
    "insurance": "保险精算",
    "securities": "证券分析",
    "surveying": "测绘计算",
    "energy": "能源计算",
    "aerospace": "航空航天",
    "automotive": "汽车工程",
    "accounting": "会计计算",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<!-- toolbox-theme-bootstrap -->
<!-- toolbox-sw-register --><script>if("serviceWorker"in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){});});}</script><script>(function(){try{var t=localStorage.getItem("theme");if(!t&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches){t="dark";}if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");}}catch(e){}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=__CAT__,industry=__INDUSTRY__,icon=__ICON__,bg=__BG__">
<title>__TITLE__ - ToolBox</title>
<link rel="canonical" href="https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html">
<meta name="twitter:card" content="summary">
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"},{"@type":"ListItem","position":2,"name":"__CATZH__","item":"https://chenguangwu.github.io/tools/__INDUSTRY__/index.html"},{"@type":"ListItem","position":3,"name":"__TITLE__","item":"https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html"}]}
</script>

<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">
    <meta property="og:type" content="website">
    <meta name="twitter:title" content="__TITLE__">
    <meta name="twitter:description" content="__DESC__">

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"__TITLE__","url":"https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","description":"__TITLE__","image":"https://chenguangwu.github.io/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}
</script>

<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
<!-- TOOLBOX-SECURITY -->

<script src="/js/privacy.js" defer></script>
<!-- TOOLBOX-PRIVACY-SCRIPT -->

<script src="/js/metrics.js" defer></script>
<!-- TOOLBOX-METRICS-SCRIPT -->
</head>
<body>

<h1 class="sr-only">__H1__</h1>

<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ __TITLE__</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>



<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">🔧 __CATZH__</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">__TITLE__ | ToolBox免费在线工具箱</span>
</nav>
<div class="container">
  <div class="card">
    <h2>__H2__</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">__INTRO__</p>

__INPUTS__

    <div class="toolbar">
      <button class="btn primary" onclick="calcTool()">计算</button>
      <button class="btn" onclick="resetForm()">重置</button>
    </div>

    <div class="result-box" id="result"></div>

    <div class="tool-notes">
      <div class="tool-notes-title">📌 计算说明</div>
      <ul>
__NOTES__
      </ul>
    </div>
  </div>
</div>

<script>
function num(id){const v=parseFloat(document.getElementById(id).value);return isNaN(v)?0:v;}
function dataGrid(rows){let h='<div class="data-grid">';for(const r of rows){h+='<div class="data-card"><div class="num">'+r[0]+'</div><div class="label">'+r[1]+'</div></div>';}return h+'</div>';}
function calcTool(){__CALC__}
function resetForm(){__RESET__}
calcTool();
</script>
</body>
</html>
"""


def render_inputs(tool):
    rows = []
    ins = tool["inputs"]
    for i in range(0, len(ins), 3):
        chunk = ins[i:i + 3]
        cells = []
        for f in chunk:
            unit = (" (" + f.get("unit", "") + ")") if f.get("unit") else ""
            minv = f.get("min", "")
            maxv = f.get("max", "")
            extra = ""
            if minv != "":
                extra += ' min="%s"' % minv
            if maxv != "":
                extra += ' max="%s"' % maxv
            cells.append(
                '      <div>\n'
                '        <label for="%s">%s%s</label>\n'
                '        <input type="number" id="%s" value="%s" step="%s"%s>\n'
                '      </div>' % (f["id"], f["label"], unit, f["id"], f["value"], f["step"], extra)
            )
        rows.append('    <div class="input-row">\n' + "\n".join(cells) + '\n    </div>')
    return "\n".join(rows)


def render_reset(tool):
    lines = []
    for f in tool["inputs"]:
        lines.append("document.getElementById('%s').value = %s;" % (f["id"], repr(f["value"])))
    lines.append("calcTool();")
    return "\n      ".join(lines)


def render_notes(tool):
    return "\n".join("        <li>%s</li>" % n for n in tool["notes"])


def render(tool):
    catzh = CAT_ZH.get(tool["industry"], tool["industry"])
    return (TEMPLATE
            .replace("__CAT__", tool["cat"])
            .replace("__INDUSTRY__", tool["industry"])
            .replace("__ICON__", tool["icon"])
            .replace("__BG__", tool["bg"])
            .replace("__SLUG__", tool["slug"])
            .replace("__TITLE__", tool["title"])
            .replace("__H1__", tool["h1"])
            .replace("__H2__", tool["h2"])
            .replace("__INTRO__", tool["intro"])
            .replace("__DESC__", tool["desc"])
            .replace("__CATZH__", catzh)
            .replace("__INPUTS__", render_inputs(tool))
            .replace("__CALC__", tool["calc"])
            .replace("__RESET__", render_reset(tool))
            .replace("__NOTES__", render_notes(tool)))


def main(TOOLS):
    count = 0
    for tool in TOOLS:
        out_dir = os.path.join(TOOLS_DIR, tool["industry"])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, tool["slug"] + ".html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(tool))
        count += 1
        print("  + tools/%s/%s.html" % (tool["industry"], tool["slug"]))
    print("共生成 %d 个工具页" % count)


if __name__ == "__main__":
    raise SystemExit("请通过具体 gen_xxx_tools.py 调用 main(TOOLS)")
