# -*- coding: utf-8 -*-
"""清理 baking 分类 5 个 formula-desc 套话，替换为真实计算原理说明。"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "baking")

FD_RE = re.compile(r'<p class="formula-desc"[^>]*>.*?</p>', re.S)

REAL = {
    "recipe-scaler":
        "配方缩放采用比例换算：每种原料新用量 = 原用量 ×（目标份数 ÷ 原份数），所有原料同步缩放以保持配比。计算在浏览器本地完成，不上传数据。",
    "oven-temp":
        "温度换算采用标准公式：摄氏度 =（华氏度 − 32）× 5 ÷ 9，华氏度 = 摄氏度 × 9 ÷ 5 + 32。对流（风炉）烤箱因热风加速传热，通常比平炉低 10–20°C 或缩短 10–15% 时间，结果区会给出补偿建议。",
    "convert-28":
        "烘焙百分比以面粉重量为 100% 基准：某配料百分比 = 该配料重量 ÷ 面粉重量 × 100%。输入面粉量即可得出水、糖、酵母等各料用量，便于配方缩放与配比核对。",
    "mold":
        "模具容积按几何公式计算：圆柱 V = π × r² × h，长方体 V = 长 × 宽 × 高，中空模按圆环柱 V = π ×（R² − r²）× h。填充量在容积基础上按品类建议比例（如戚风 7–8 分满）取值。",
    "convert-temp":
        "温度换算采用标准公式：摄氏度 =（华氏度 − 32）× 5 ÷ 9，华氏度 = 摄氏度 × 9 ÷ 5 + 32。风炉（对流）对平炉（传统上下火）需下调 10–20°C 或缩短 10–15% 时间，结果区给出补偿值。",
}

def main():
    changed = 0
    for base, real in REAL.items():
        f = os.path.join(TOOLS_DIR, base + ".html")
        if not os.path.exists(f):
            print("SKIP missing:", base)
            continue
        s = open(f, encoding="utf-8").read()
        new_fd = '<p class="formula-desc">%s</p>' % real
        s2, n = FD_RE.subn(new_fd, s, count=1)
        if n == 0:
            print("NO FD found:", base)
            continue
        open(f, "w", encoding="utf-8").write(s2)
        changed += 1
        print("OK cleaned:", base)
    print("baking formula-desc cleaned:", changed)

if __name__ == "__main__":
    main()
