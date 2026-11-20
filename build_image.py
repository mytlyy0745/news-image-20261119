#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Facts verified against live reporting on 20 Nov 2026 (Reuters, WSJ,
AP via USA Today, The Independent, Dow Jones/Morningstar, JMIC):
- Trump-Xi-Putin trilateral, Shenzhen, APEC, 19 Nov: first-ever meeting,
  ~90 minutes at Kylin Villa; four-point declaration, "a nuclear war
  cannot be won and must never be fought"; no breakthrough on Ukraine/Iran.
- Ukraine hits the Kerch (Crimean) Bridge a third time in a week (Neptune
  missiles, rail tracks damaged, trains halted, no injuries per Russia);
  Putin rules out a Black Sea / energy truce and vows retaliation.
- US sends USS Theodore Roosevelt, a third carrier, to the Gulf; tankers
  hit mines in the Strait of Hormuz (JMIC: four vessel attacks in 96h).
- Anthropic IPO: priced $83, $81bn raised, largest IPO ever; opened
  $111.50 (+34%), closed +17%; Dow fell 1,101 points the same day.
- Coalition of the Willing meets in Berlin with Zelenskyy, hours after
  Shenzhen. Also: Kyiv drone attack kills one, damages Dutch and Austrian
  embassies; House Democrats nominate Hakeem Jeffries for Speaker;
  Brent crude $92.87.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
DARK = (28, 34, 48)
GREY = (90, 88, 80)
GREEN = (24, 120, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.32)
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    for i in range(7):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=(178, 34, 34) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(24, 62, 120))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    draw.ellipse([x + w * 0.12, y + h * 0.18, x + w * 0.30, y + h * 0.55], fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.15), (0.68, 0.30), (0.68, 0.55), (0.55, 0.68)]:
        draw.ellipse([x + w * sx, y + h * sy, x + w * sx + 5, y + h * sy + 5], fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c, outline=INK, width=1)


def skyline(draw, x, y, w, h, color):
    rnd = random.Random(7)
    cx = x
    while cx < x + w - 10:
        bw = min(rnd.randint(18, 46), x + w - cx)
        bh = rnd.randint(int(h * 0.3), h)
        draw.rectangle([cx, y + h - bh, cx + bw, y + h], fill=color)
        if rnd.random() < 0.3:
            draw.polygon([(cx + bw * 0.3, y + h - bh), (cx + bw * 0.7, y + h - bh),
                          (cx + bw * 0.5, y + h - bh - 22)], fill=color)
        cx += bw + 4


def panel_frame(draw, px, py, pw, ph):
    draw.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)


def panel_text(draw, px, py, pw, kicker, body):
    # image band occupies py+2 .. py+86; title at py+94; body at py+118
    draw.text((px + 12, py + 94), kicker, font=font(SANS_B, 17), fill=RED)
    para(draw, px + 12, py + 118, body, font(SERIF_R, 18), pw - 24, leading=23)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30
    R = W - M

    # ---- Masthead ----
    f_mast = font(SERIF, 62)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 18), title, font=f_mast, fill=INK)
    rule(d, M, 96, R, 3)
    f_date = font(SERIF, 30)
    date = "THURSDAY  ·  19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 106), date, font=f_date, fill=RED)
    f_kick = font(SANS_B, 16)
    kick = "SHENZHEN   —   KYIV   —   THE GULF   —   WALL STREET   —   BERLIN"
    d.text(((W - d.textlength(kick, font=f_kick)) / 2, 146), kick, font=f_kick, fill=GREY)
    rule(d, M, 172, R, 2)

    # ---- Lead story: 186 .. 496 ----
    ly = 186
    ix0, iy0, ix1, iy1 = M, ly, 470, 496
    d.rectangle([ix0, iy0, ix1, iy1], fill=(214, 226, 240), outline=INK, width=2)
    d.rectangle([ix0 + 2, iy0 + 2, ix1 - 2, iy0 + 118], fill=(58, 84, 130))
    skyline(d, ix0 + 8, iy0 + 52, ix1 - ix0 - 16, 66, (38, 52, 84))
    d.ellipse([ix1 - 78, iy0 + 22, ix1 - 38, iy0 + 62], fill=(245, 222, 160))
    # round table
    d.ellipse([ix0 + 55, iy0 + 208, ix1 - 55, iy0 + 262], fill=(122, 74, 40), outline=INK, width=2)
    d.ellipse([ix0 + 95, iy0 + 222, ix1 - 95, iy0 + 250], fill=(146, 96, 56))
    # three flags on poles rising from the table
    for fx, fl in [(ix0 + 78, flag_cn), (ix0 + 205, flag_us), (ix1 - 118, flag_ru)]:
        d.line([(fx + 20, iy0 + 150), (fx + 20, iy0 + 210)], fill=INK, width=3)
        fl(d, fx, iy0 + 150, 40, 26)
    d.text((ix0 + 14, iy1 - 36), "Kylin Villa, Shenzhen — the first-ever", font=font(SANS, 15), fill=GREY)
    d.text((ix0 + 14, iy1 - 18), "meeting of the three nuclear powers.", font=font(SANS, 15), fill=GREY)

    tx = 492
    d.text((tx, ly + 2), "THE SUMMIT  ·  SHENZHEN", font=font(SANS_B, 17), fill=RED)
    y = para(d, tx, ly + 30, "THREE NUCLEAR POWERS, ONE TABLE",
             font(SERIF, 38), R - tx, leading=46)
    y = para(d, tx, y + 10,
             "Trump, Xi and Putin meet for the first time ever — about 90 "
             "minutes at Kylin Villa on the sidelines of APEC.",
             font(SERIF_R, 20), R - tx, leading=26)
    para(d, tx, y + 8,
         "Their four-point declaration: \u201ca nuclear war cannot be won "
         "and must never be fought.\u201d No breakthrough on Ukraine or Iran.",
         font(SERIF_R, 20), R - tx, leading=26)

    rule(d, M, 508, R, 2)

    # ---- Middle row: 520 .. 710 ----
    my, mh = 520, 190
    pw = (R - M - 24) // 2
    # Panel A: Crimean Bridge
    px, py = M, my
    panel_frame(d, px, py, pw, mh)
    d.rectangle([px + 2, py + 2, px + pw - 2, py + 86], fill=(196, 216, 232))
    d.rectangle([px + 2, py + 68, px + pw - 2, py + 86], fill=(90, 130, 170))
    d.line([(px + 8, py + 58), (px + pw // 2 - 28, py + 58)], fill=INK, width=5)
    d.line([(px + pw // 2 + 28, py + 58), (px + pw - 8, py + 58)], fill=INK, width=5)
    for bx in (px + 60, px + pw - 90):
        d.line([(bx, py + 26), (bx, py + 58)], fill=INK, width=4)
    cx, cy = px + pw // 2, py + 46
    for ang in range(0, 360, 30):
        r1, r2 = 7, 22
        d.line([(cx + r1 * math.cos(math.radians(ang)), cy + r1 * math.sin(math.radians(ang))),
                (cx + r2 * math.cos(math.radians(ang)), cy + r2 * math.sin(math.radians(ang)))],
               fill=(230, 120, 20), width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(230, 120, 20))
    panel_text(d, px, py, pw, "UKRAINE  ·  THE BRIDGE HIT AGAIN",
               "Ukraine strikes the Kerch bridge a third time in a week; "
               "trains halted. Putin rules out a Black Sea and energy truce "
               "and vows retaliation.")

    # Panel B: Gulf
    px = M + pw + 24
    panel_frame(d, px, py, pw, mh)
    d.rectangle([px + 2, py + 2, px + pw - 2, py + 86], fill=(214, 226, 240))
    d.rectangle([px + 2, py + 66, px + pw - 2, py + 86], fill=(90, 130, 170))
    d.rectangle([px + 30, py + 52, px + pw - 60, py + 64], fill=DARK)
    d.rectangle([px + pw - 110, py + 34, px + pw - 84, py + 52], fill=DARK)
    d.line([(px + pw - 97, py + 24), (px + pw - 97, py + 34)], fill=DARK, width=3)
    d.rectangle([px + 40, py + 74, px + 150, py + 83], fill=(120, 40, 40))
    d.polygon([(px + 118, py + 74), (px + 128, py + 58), (px + 138, py + 74)], fill=(240, 140, 20))
    panel_text(d, px, py, pw, "THE GULF  ·  THIRD CARRIER SAILS IN",
               "The USS Theodore Roosevelt joins two US carriers as tankers "
               "hit mines in the Strait of Hormuz — four ships attacked in "
               "four days.")

    rule(d, M, 722, R, 2)

    # ---- Bottom row: 734 .. 924 ----
    by, bh = 734, 190
    # Panel C: Anthropic IPO
    px, py = M, by
    panel_frame(d, px, py, pw, bh)
    d.rectangle([px + 2, py + 2, px + pw - 2, py + 86], fill=(238, 240, 234))
    d.line([(px + 20, py + 76), (px + pw - 20, py + 76)], fill=GREY, width=2)
    d.line([(px + 20, py + 76), (px + 20, py + 12)], fill=GREY, width=2)
    pts = [(px + 30, py + 68), (px + 110, py + 60), (px + 190, py + 63),
           (px + 270, py + 40), (px + 350, py + 28), (px + pw - 34, py + 16)]
    d.line(pts, fill=GREEN, width=5)
    d.polygon([(px + pw - 34, py + 16), (px + pw - 52, py + 14), (px + pw - 38, py + 30)],
              fill=GREEN)
    d.text((px + 30, py + 14), "$83", font=font(SANS_B, 20), fill=GREEN)
    d.text((px + 170, py + 14), "+34% at open", font=font(SANS_B, 18), fill=GREEN)
    panel_text(d, px, py, pw, "WALL STREET  ·  BIGGEST IPO EVER",
               "Anthropic lists on Nasdaq at $83, raising $81bn — the "
               "largest IPO in history. Shares jump 34% at the open; the "
               "Dow still falls 1,100 points.")

    # Panel D: Berlin
    px = M + pw + 24
    panel_frame(d, px, py, pw, bh)
    d.rectangle([px + 2, py + 2, px + pw - 2, py + 86], fill=(226, 228, 236))
    gx, gy = px + 130, py + 16
    for i in range(6):
        d.rectangle([gx + i * 34, gy + 16, gx + i * 34 + 16, gy + 66], fill=(70, 76, 92))
    d.rectangle([gx - 10, gy, gx + 5 * 34 + 26, gy + 16], fill=(70, 76, 92))
    d.rectangle([gx - 10, gy + 66, gx + 5 * 34 + 26, gy + 72], fill=(70, 76, 92))
    panel_text(d, px, py, pw, "BERLIN  ·  EUROPE ANSWERS",
               "After Shenzhen, the \u201cCoalition of the Willing\u201d — Germany, "
               "France, Britain, Poland, Italy and NATO — meets Zelenskyy "
               "in Berlin.")

    # ---- Also today strip ----
    sy = 936
    rule(d, M, sy, R, 2)
    d.text((M, sy + 8), "ALSO TODAY", font=font(SANS_B, 16), fill=RED)
    para(d, M, sy + 30,
         "Kyiv drone attack kills one and damages the Dutch and Austrian "
         "embassies  ·  House Democrats nominate Hakeem Jeffries for "
         "Speaker  ·  Brent crude $92.87 a barrel",
         font(SERIF_R, 16), R - M, leading=20)
    f_f = font(SANS, 12)
    foot = "Sources: Reuters · The Wall Street Journal · The Independent · Dow Jones · JMIC — 19 November 2026"
    d.text(((W - d.textlength(foot, font=f_f)) / 2, H - 16), foot, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
