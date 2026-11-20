#!/usr/bin/env python3
"""Build the front page for Thursday, 19 November 2026.

Draws a newspaper front page (1024x1024 PNG) with PIL only, from
hard-coded, researched facts about that day. No network, no clock,
no randomness: running it twice writes byte-identical output.

Stories (all reported on 19 November 2026):
  1. Trump, Xi and Putin meet in Shenzhen (APEC) - first three-way
     summit, peace declaration, UN reform and oil pledges.
  2. The ICJ rules 9-6 that Myanmar committed genocide against the
     Rohingya in 2017 - the first time the court has found a state
     guilty of genocide; about 10,000 killed; reparations ordered.
  3. Anthropic IPO: $83 a share, $81bn raised, the largest IPO ever;
     about $1.5tn valuation; shares close at $97 after touching $115.
  4. A Houthi missile hits a Public Investment Fund tower in Riyadh.
  5. The US Senate rejects the Iran war-powers resolution, 51-48.
  6. Israeli tanks push into central Gaza beyond the ceasefire line;
     Russia says Ukraine attacked the Crimean Bridge again.
  7. GTA VI launches on PS5 and Xbox Series X|S.
Also today: Denmark approves the Greenland defence deal 109-0;
a migrant boat capsizes off Senegal; record floods in Florida.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (15, 42, 74)
BLUE = (31, 78, 121)
GREY = (96, 92, 84)
LIGHT = (236, 231, 218)
LIGHT_BLUE = (226, 233, 240)
GOLD = (178, 138, 32)
WHITE = (255, 255, 255)

SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
]
SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
]
SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
]
SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]

_FONT_CACHE = {}


def font(paths, size):
    key = (tuple(paths), size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    for path in paths:
        try:
            f = ImageFont.truetype(path, size)
            _FONT_CACHE[key] = f
            return f
        except OSError:
            continue
    f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


def serif_bold(size):
    return font(SERIF_BOLD, size)


def serif(size):
    return font(SERIF, size)


def sans_bold(size):
    return font(SANS_BOLD, size)


def sans(size):
    return font(SANS, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    import math

    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_us(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else WHITE
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=NAVY)
    for row in range(5):
        for col in range(6):
            sx = x + 8 + col * (cw - 14) / 5.0
            sy = y + 6 + row * (ch - 12) / 4.0
            draw.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=WHITE)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(draw, x + w * 0.16, y + h * 0.28, h * 0.20, (255, 222, 0))
    for sx, sy in [(0.34, 0.12), (0.42, 0.26), (0.42, 0.44), (0.34, 0.58)]:
        star(draw, x + w * sx, y + h * sy, h * 0.09, (255, 222, 0))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
        draw.rectangle(
            [x, y + i * h / 3.0, x + w, y + (i + 1) * h / 3.0], fill=c
        )
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def scales(draw, x, y, s, color):
    # Simple scales of justice: post, beam, two pans.
    draw.line([(x + s / 2, y), (x + s / 2, y + s * 0.78)], fill=color, width=3)
    draw.line([(x + 2, y + s * 0.16), (x + s - 2, y + s * 0.16)],
              fill=color, width=3)
    draw.ellipse([x + s / 2 - 4, y - 4, x + s / 2 + 4, y + 4], fill=color)
    for cx in (x + 4, x + s - 4):
        draw.line([(cx, y + s * 0.16), (cx, y + s * 0.48)], fill=color, width=2)
        draw.arc([cx - 13, y + s * 0.42, cx + 13, y + s * 0.72],
                 start=0, end=180, fill=color, width=3)
    draw.line([(x + 6, y + s * 0.82), (x + s - 6, y + s * 0.82)],
              fill=color, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    cw = W - 2 * mx  # 952

    # --- top strip -------------------------------------------------
    f_small = sans_bold(14)
    d.text((mx, 20), "ONE DAY  •  ONE PAGE", font=f_small, fill=GREY)
    right = "No. 323  •  FREE"
    d.text((W - mx - d.textlength(right, font=f_small), 20), right,
           font=f_small, fill=GREY)

    # --- masthead --------------------------------------------------
    f_mast = serif_bold(66)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 40), title,
           font=f_mast, fill=INK)
    d.rectangle([mx, 114, W - mx, 118], fill=RED)

    # --- dateline bar ----------------------------------------------
    d.rectangle([mx, 126, W - mx, 162], fill=INK)
    f_date = sans_bold(23)
    d.text((mx + 16, 134), "THURSDAY, 19 NOVEMBER 2026",
           font=f_date, fill=WHITE)
    f_date_r = sans(17)
    rtext = "SHENZHEN  •  THE HAGUE  •  NEW YORK"
    d.text((W - mx - 16 - d.textlength(rtext, font=f_date_r), 138), rtext,
           font=f_date_r, fill=(210, 210, 205))

    # --- lead story -------------------------------------------------
    y = 174
    d.text((mx, y), "SHENZHEN, CHINA  —  APEC SUMMIT",
           font=sans_bold(17), fill=RED)
    y = 200
    f_head = serif_bold(46)
    d.text((mx, y), "TRUMP, XI AND PUTIN", font=f_head, fill=INK)
    d.text((mx, y + 54), "MEET IN SHENZHEN", font=f_head, fill=INK)
    y = 316
    f_deck = serif(21)
    y = draw_wrapped(
        d, mx, y,
        "First three-way summit ends with a peace declaration \u2014 "
        "pledges to reform the UN and boost oil output. No deal yet "
        "on Ukraine, Iran or nuclear arms.",
        f_deck, cw, INK, 27)

    # flag strip: USA / China / Russia
    fy = 372
    fw, fh = 304, 64
    flags = [
        (flag_us, "UNITED STATES", "Donald Trump"),
        (flag_cn, "CHINA", "Xi Jinping"),
        (flag_ru, "RUSSIA", "Vladimir Putin"),
    ]
    for i, (fn, name, leader) in enumerate(flags):
        fx = mx + i * (fw + 20)
        fn(d, fx, fy, fw, fh)
        d.text((fx + (fw - d.textlength(name, font=sans_bold(15))) / 2,
                fy + fh + 6), name, font=sans_bold(15), fill=INK)
        d.text((fx + (fw - d.textlength(leader, font=sans(13))) / 2,
                fy + fh + 26), leader, font=sans(13), fill=GREY)
    y = fy + fh + 44
    f_bullet = sans(15)
    bullet = ("90-minute talks  •  Ukraine, Iran and nuclear arms on the "
              "table  •  Europe\u2019s leaders meet in Berlin the same day")
    d.text((mx, y), bullet, font=f_bullet, fill=INK)

    # --- rule --------------------------------------------------------
    d.line([(mx, 506), (W - mx, 506)], fill=INK, width=2)

    # --- middle row: two big stories --------------------------------
    my = 518
    box_w = 466
    box_h = 208
    # left: ICJ / Myanmar
    d.rectangle([mx, my, mx + box_w, my + box_h], fill=LIGHT_BLUE)
    d.rectangle([mx, my, mx + box_w, my + box_h], outline=INK, width=1)
    bx = mx + 16
    d.text((bx, my + 12), "THE HAGUE  —  JUSTICE",
           font=sans_bold(15), fill=NAVY)
    scales(d, mx + box_w - 66, my + 10, 52, NAVY)
    f_h2 = serif_bold(28)
    d.text((bx, my + 38), "MYANMAR GUILTY", font=f_h2, fill=INK)
    d.text((bx, my + 72), "OF GENOCIDE", font=f_h2, fill=INK)
    draw_wrapped(
        d, bx, my + 112,
        "The World Court rules 9\u20136: Myanmar committed genocide "
        "against the Rohingya in 2017 \u2014 about 10,000 killed. "
        "A first: no state has been found guilty before. "
        "Reparations ordered.",
        serif(16), box_w - 32, INK, 21)

    # right: Anthropic IPO
    rx = mx + box_w + 20
    d.rectangle([rx, my, rx + box_w, my + box_h], fill=LIGHT)
    d.rectangle([rx, my, rx + box_w, my + box_h], outline=INK, width=1)
    bx = rx + 16
    d.text((bx, my + 12), "NEW YORK  —  MARKETS",
           font=sans_bold(15), fill=NAVY)
    d.text((bx, my + 38), "ANTHROPIC IN RECORD", font=f_h2, fill=INK)
    d.text((bx, my + 72), "$81BN IPO", font=f_h2, fill=INK)
    draw_wrapped(
        d, bx, my + 112,
        "The Claude maker prices at $83 a share \u2014 the largest "
        "IPO ever, valued about $1.5 trillion.",
        serif(16), box_w - 32, INK, 21)
    d.text((bx, my + box_h - 26), "Close $97, after a $115 high.",
           font=sans_bold(13), fill=INK)
    # mini bar chart: $83 IPO, $115 high, $97 close
    chart_y = my + box_h - 8
    bars = [("$83", 20, NAVY), ("$115", 32, RED), ("$97", 26, BLUE)]
    bx0 = rx + box_w - 118
    for i, (lab, bh, col) in enumerate(bars):
        x0 = bx0 + i * 38
        d.rectangle([x0, chart_y - bh, x0 + 24, chart_y], fill=col)
        d.text((x0 - 2, chart_y - bh - 16), lab, font=sans_bold(12),
               fill=INK)

    # --- rule --------------------------------------------------------
    d.line([(mx, 738), (W - mx, 738)], fill=INK, width=2)

    # --- third row: three short stories ------------------------------
    ty = 750
    col_w = 304
    cols = [
        ("RIYADH  —  MISSILE", RED,
         "HOUTHI MISSILE HITS\nRIYADH TOWER",
         "A strike damages a Public Investment Fund tower in the "
         "Saudi capital. Debris is reported; no one has claimed "
         "the attack."),
        ("WASHINGTON  —  CONGRESS", NAVY,
         "SENATE REJECTS IRAN\nWAR VOTE, 51\u201348",
         "Senators vote down a measure to end US hostilities in "
         "Iran. Three Republicans back it; one Democrat votes "
         "against it."),
        ("GAZA  •  UKRAINE  —  WAR", RED,
         "ISRAEL PUSHES INTO\nCENTRAL GAZA",
         "Israeli tanks move beyond the ceasefire line near "
         "Nuseirat; Hamas calls it a violation. Russia says "
         "Ukraine hit the Crimean Bridge again."),
    ]
    for i, (kick, kcol, head, body) in enumerate(cols):
        cx = mx + i * (col_w + 20)
        d.text((cx, ty), kick, font=sans_bold(14), fill=kcol)
        f_h3 = serif_bold(21)
        yy = ty + 22
        for line in head.split("\n"):
            d.text((cx, yy), line, font=f_h3, fill=INK)
            yy += 26
        draw_wrapped(d, cx, yy + 4, body, serif(15), col_w, INK, 20)
        if i < 2:
            d.line([(cx + col_w + 10, ty), (cx + col_w + 10, ty + 148)],
                   fill=(200, 195, 180), width=1)

    # --- rule --------------------------------------------------------
    d.line([(mx, 908), (W - mx, 908)], fill=INK, width=2)

    # --- bottom row ---------------------------------------------------
    by = 920
    # GTA VI
    d.rectangle([mx, by, mx + box_w, by + 76], fill=INK)
    d.text((mx + 16, by + 8), "GTA VI IS HERE",
           font=serif_bold(24), fill=WHITE)
    d.text((mx + 16, by + 40),
           "Rockstar\u2019s game launches on PS5 and Xbox;",
           font=sans(14), fill=(220, 220, 215))
    d.text((mx + 16, by + 58),
           "99 Metascore, $1.65bn in presales.",
           font=sans(14), fill=(220, 220, 215))
    # also today
    ax = mx + box_w + 20
    d.text((ax, by + 2), "ALSO TODAY", font=sans_bold(15), fill=RED)
    draw_wrapped(
        d, ax, by + 24,
        "Denmark approves the Greenland defence deal, 109\u20130  •  "
        "Dozens missing after a migrant boat capsizes off Senegal  •  "
        "Record floods in Florida as the St. Johns River tops 18 feet.",
        serif(15), box_w, INK, 20)

    # --- footer -------------------------------------------------------
    f_foot = sans(12)
    foot = ("THE WORLD TODAY  •  Thursday, 19 November 2026  •  "
            "All stories reported on 19 November 2026  •  Drawn with "
            "Python and PIL")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 1000), foot,
           font=f_foot, fill=GREY)

    return img


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "entry.png"
        probe = out_path
        probe.touch(exist_ok=True)
    except OSError:
        out_dir = Path("out")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "entry.png"
    img = build()
    img.save(out_path, format="PNG")
    print("wrote", out_path, img.size)


if __name__ == "__main__":
    main()
