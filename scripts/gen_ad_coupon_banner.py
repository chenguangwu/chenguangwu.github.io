# -*- coding: utf-8 -*-
"""生成「领券中心」广告素材（assets/images/ads/coupon-center-{pc,m}.webp）。

用途与边界
----------
纯素材生成脚本，**不参与构建**（`_build.py` 不调用它），仅在本机需要更换/微调
广告图时手动运行。依赖 Pillow 与 macOS 自带字体 Hiragino Sans GB：
    pip install pillow
    python3 scripts/gen_ad_coupon_banner.py

为什么是这样设计的
------------------
1. 配色收进站点主色系（AGENTS.md 设计规范）：浅暖橙底 + 橙色图标/CTA + 深色文字，
   与站内卡片广告同族，避免大面积高饱和色块在暖白页面上过于跳。
2. 高度必须与卡片广告严格相等，故页面上用「固定高度 + object-fit:cover」呈现
   （见 css/common.css 的 .coupon-ad-img）：
     容器宽度随视口变化（PC 928→736、手机 406→296），若交给宽高比等比缩放，
     高度会浮动 7~19px，与相邻卡片对不齐。
3. 因此图片按「中央安全区」设计，两侧与上下留出可被裁切的余量：
     PC  版用于 >=768px：最窄容器 736，1920x160 图在高 82 时需宽 984，
         两侧各裁 (984-736)/2=124px 显示像素 = 原图 242px ⇒ 左边距取 260（>242）。
     移动版用于 <=767px：最窄容器 296，702x128 图在高 66 时需宽 362，
         两侧各裁 33px 显示像素 = 原图 64px ⇒ 左边距取 70（>64）。
   ⚠️ 改尺寸或改字号后必须重算安全区，否则窄屏会切到图标/文字。

用法
----
    python3 scripts/gen_ad_coupon_banner.py            # 生成浅色版（当前线上方案）
    python3 scripts/gen_ad_coupon_banner.py --theme orange   # 备选：柔和橙渐变底
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'assets', 'images', 'ads')

FONT = '/System/Library/Fonts/Hiragino Sans GB.ttc'
F_BOLD = lambda s: ImageFont.truetype(FONT, s, index=2)   # W6
F_REG = lambda s: ImageFont.truetype(FONT, s, index=0)    # W3

P_ORANGE = (255, 107, 53)      # --color-primary
P_ORANGE_DEEP = (229, 90, 37)
P_PURPLE = (124, 58, 237)      # --color-secondary
INK = (31, 41, 55)             # --color-text-primary
MUTED = (107, 114, 128)        # --color-text-secondary
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def gradient(size, stops):
    """135° 线性渐变（左上→右下）。stops=[(pos, color), ...]"""
    w, h = size
    img = Image.new('RGB', size)
    px = img.load()
    for y in range(h):
        ty = y / (h - 1)
        for x in range(w):
            t = (x / (w - 1) + ty) / 2.0
            i = 0
            while i < len(stops) - 2 and t > stops[i + 1][0]:
                i += 1
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            k = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
            px[x, y] = lerp(c0, c1, max(0.0, min(1.0, k)))
    return img


def glow(base, cx, cy, r, color, alpha):
    """柔和光斑：多层同心圆叠加，避免出现硬边。"""
    layer = Image.new('RGBA', base.size, color + (0,))
    d = ImageDraw.Draw(layer)
    steps = 36
    for i in range(steps):
        rr = r * (1 - i / steps)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=color + (int(alpha * (i / steps) ** 1.6),))
    return Image.alpha_composite(base.convert('RGBA'), layer)


def ticket(dst, x, y, w, h, color, gap=0.34):
    """票券图标：圆角矩形主体 + 左右各一缺口 + 中间虚线。"""
    cut = max(6, int(h * 0.30))
    m = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=max(4, int(h * 0.18)), fill=255)
    cy = h // 2
    d.ellipse([-cut, cy - cut, cut, cy + cut], fill=0)
    d.ellipse([w - cut, cy - cut, w + cut, cy + cut], fill=0)
    dash = max(2, int(h * 0.08))
    yy = cy - int(h * gap / 2)
    xd = int(w * 0.52)
    while yy < cy + int(h * gap / 2):
        d.rectangle([xd, yy, xd + max(1, w // 34), yy + dash], fill=0)
        yy += dash * 2
    dst.paste(Image.new('RGBA', (w, h), color), (x, y), m)


def text_size(draw, s, font):
    b = draw.textbbox((0, 0), s, font=font)
    return b[2] - b[0], b[3] - b[1]


def banner(W, H, pad_x, sp, theme):
    if theme == 'light':
        img = gradient((W, H), [(0, (255, 245, 238)), (0.40, (255, 238, 221)),
                                (0.78, (255, 226, 200)), (1.0, (254, 236, 222))])
        img = glow(img, W * 0.88, H * -0.1, W * 0.20, P_ORANGE, 30)
        img = glow(img, W * 0.06, H * 1.2, W * 0.15, P_PURPLE, 22)
        fg_title, fg_sub = INK, MUTED
    else:
        img = gradient((W, H), [(0, (247, 156, 118)), (0.55, (240, 124, 74)),
                                (1.0, (216, 92, 54))])
        img = glow(img, W * 0.86, H * -0.15, W * 0.20, WHITE, 42)
        img = glow(img, W * 0.10, H * 1.25, W * 0.16, WHITE, 30)
        fg_title, fg_sub = WHITE, (255, 232, 218)

    d = ImageDraw.Draw(img)
    ic = sp['icon']
    box, r, top = ic['box'], ic['r'], ic['top']

    # 1) 图标：浅色版用橙渐变方块（与站内卡片图标同款），橙底版用半透明白块 + 橙色券
    if theme == 'light':
        sq = gradient((box, box), [(0, P_ORANGE), (1.0, P_ORANGE_DEEP)])
        mask = Image.new('L', (box, box), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, box - 1, box - 1], radius=r, fill=255)
        img.paste(sq, (pad_x, top), mask)
        tk_color = WHITE
    else:
        d.rounded_rectangle([pad_x, top, pad_x + box, top + box], radius=r, fill=WHITE + (52,))
        tk_color = P_ORANGE_DEEP
    tw, th = ic['ticket']
    ticket(img, pad_x + (box - tw) // 2, top + (box - th) // 2, tw, th, tk_color)

    # 2) 标题 + 副标题：整块垂直居中
    tx = pad_x + box + sp['gap']
    f_t, f_s = F_BOLD(sp['title_size']), F_REG(sp['sub_size'])
    _, h_t = text_size(d, sp['title'], f_t)
    _, h_s = text_size(d, sp['sub'], f_s)
    ty = (H - (h_t + sp['line_gap'] + h_s)) // 2
    d.text((tx, ty), sp['title'], font=f_t, fill=fg_title)
    d.text((tx, ty + h_t + sp['line_gap']), sp['sub'], font=f_s, fill=fg_sub)

    # 3) CTA：右侧胶囊
    f_c = F_BOLD(sp['cta_size'])
    w_c, h_c = text_size(d, sp['cta'], f_c)
    cw, ch = w_c + sp['cta_pad'] * 2, h_c + sp['cta_pad_y'] * 2
    cx1, cx0 = W - pad_x, W - pad_x - cw
    cy0 = (H - ch) // 2
    if theme == 'light':
        pg = gradient((cw, ch), [(0, P_ORANGE), (1.0, P_ORANGE_DEEP)])
        pm = Image.new('L', (cw, ch), 0)
        ImageDraw.Draw(pm).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=ch // 2, fill=255)
        img.paste(pg, (cx0, cy0), pm)
        d.text((cx0 + sp['cta_pad'], cy0 + sp['cta_pad_y']), sp['cta'], font=f_c, fill=WHITE)
    else:
        d.rounded_rectangle([cx0, cy0, cx1, cy0 + ch], radius=ch // 2, fill=WHITE)
        d.text((cx0 + sp['cta_pad'], cy0 + sp['cta_pad_y']), sp['cta'], font=f_c, fill=P_ORANGE_DEEP)

    # 4) 浅色版补一圈极细描边，呼应站内卡片的 border
    if theme == 'light':
        d.rounded_rectangle([1, 1, W - 2, H - 2], radius=30,
                            outline=(255, 107, 53, 40), width=2)
    return img


# PC 版：1920x160（2x），页面上显示宽约 928、高 82（与卡片广告等高）
SPEC_PC = dict(icon=dict(box=96, r=24, top=32, ticket=(62, 40)), gap=36,
               title='领券中心', title_size=56,
               sub='抢大额官方补贴 · 先领券再下单更划算', sub_size=27, line_gap=10,
               cta='立即领券', cta_size=30, cta_pad=40, cta_pad_y=18)
# 移动版：702x128（2x），显示宽约 351、高 66
SPEC_M = dict(icon=dict(box=72, r=18, top=28, ticket=(46, 30)), gap=22,
              title='领券中心', title_size=38,
              sub='先领券再下单更划算', sub_size=21, line_gap=6,
              cta='领券', cta_size=22, cta_pad=24, cta_pad_y=12)


def main():
    ap = argparse.ArgumentParser(description='生成领券中心广告素材')
    ap.add_argument('--theme', choices=['light', 'orange'], default='light',
                    help='light=浅暖色卡片风（默认，线上方案）；orange=柔和橙渐变底')
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    jobs = [(1920, 160, 260, SPEC_PC, 'coupon-center-pc.webp'),
            (702, 128, 70, SPEC_M, 'coupon-center-m.webp')]
    for W, H, pad, sp, name in jobs:
        img = banner(W, H, pad, sp, args.theme).convert('RGB')
        path = os.path.join(OUT_DIR, name)
        img.save(path, 'WEBP', quality=90, method=6)
        print('%-26s %dx%d  %.1f KB' % (name, W, H, os.path.getsize(path) / 1024))


if __name__ == '__main__':
    main()
