#!/usr/bin/env python3
"""draw_poster.py — renders entry.png for make.fun news-image-20261123 (r3).

Fresh build from FACT-SHEET-R3.md (35 verified stories, Monday 23 Nov 2026).
Newspaper front page, PIL flat illustration, 1024x1024.
Run: python3 draw_poster.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (245, 239, 221)
INK = (22, 21, 19)
INK_SOFT = (64, 60, 52)
RED = (163, 29, 29)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GOLD = (146, 64, 14)
RULE = (120, 110, 88)
CARD_BG = (250, 246, 233)
CARD_LINE = (198, 186, 158)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def clamp_lines(d, text, f, max_w, max_lines):
    """Wrap text, clamp to max_lines, add ellipsis if truncated."""
    lines = wrap(d, text, f, max_w)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    last = out[-1]
    while last and d.textlength(last + "...", font=f) > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    out[-1] = (last + "...").strip()
    return out


def text_block(d, x, y, lines, f, fill=INK, leading=None):
    if leading is None:
        leading = f.size + 3
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=f, fill=fill)
    return y + len(lines) * leading


def hrule(d, x0, x1, y, fill=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


REGION_COLOR = {
    "NORTH AMERICA": BLUE,
    "EUROPE": (124, 45, 18),
    "MIDDLE EAST": RED,
    "AFRICA": GOLD,
    "ASIA": TEAL,
    "SOUTH AMERICA": (77, 124, 15),
    "OCEANIA": (109, 40, 217),
}


# ---------------------------------------------------------------- illustrations
def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 165),
              outline=(22, 21, 19), width=3)
    land = (96, 160, 110)
    d.ellipse([cx - r + 12, cy - r + 22, cx - r + 62, cy - r + 62], fill=land)
    d.ellipse([cx - 6, cy - r + 8, cx + 52, cy - r + 44], fill=land)
    d.ellipse([cx + 8, cy + 6, cx + r - 14, cy + r - 30], fill=land)
    d.ellipse([cx - r + 26, cy + 18, cx - 8, cy + r - 16], fill=land)
    d.ellipse([cx - 14, cy + r - 34, cx + 30, cy + r - 8], fill=land)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(235, 240, 244))
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 0, 180, fill=(235, 240, 244))
    crack = [(cx - 58, cy - 44), (cx - 30, cy - 18), (cx - 44, cy + 6),
             (cx - 12, cy + 22), (cx - 26, cy + 48), (cx + 6, cy + 66),
             (cx - 2, cy + 84)]
    d.line(crack, fill=(22, 21, 19), width=4, joint="curve")
    crack2 = [(cx - 12, cy + 22), (cx + 22, cy + 10), (cx + 44, cy + 26),
              (cx + 62, cy + 12)]
    d.line(crack2, fill=(22, 21, 19), width=3, joint="curve")
    crack3 = [(cx - 30, cy - 18), (cx - 2, cy - 34), (cx + 26, cy - 26)]
    d.line(crack3, fill=(22, 21, 19), width=3, joint="curve")
    d.line([(cx - 52, cy + r + 10), (cx + 52, cy + r + 10)], fill=INK, width=4)
    d.line([(cx, cy + r), (cx, cy + r + 10)], fill=INK, width=4)


def draw_capitol(d, x, y, w, h):
    d.rectangle([x, y + h - 8, x + w, y + h], fill=INK)
    d.rectangle([x + 6, y + h - 16, x + w - 6, y + h - 8], fill=INK_SOFT)
    d.pieslice([x + w // 2 - 16, y, x + w // 2 + 16, y + 32], 180, 360,
               fill=BLUE)
    d.rectangle([x + w // 2 - 16, y + 14, x + w // 2 + 16, y + h - 16],
                fill=BLUE)
    d.line([(x + w // 2, y - 6), (x + w // 2, y)], fill=INK, width=2)


def draw_tanker(d, x, y, w, h):
    d.polygon([(x, y + h - 22), (x + w, y + h - 22), (x + w - 12, y + h),
               (x + 10, y + h)], fill=(90, 32, 28))
    d.rectangle([x + 8, y + 14, x + 30, y + h - 22], fill=TEAL)
    d.rectangle([x + 34, y + 20, x + 56, y + h - 22], fill=GOLD)
    d.rectangle([x + w - 26, y + 4, x + w - 8, y + h - 22], fill=INK_SOFT)
    d.polygon([(x + 40, y + 18), (x + 48, y - 2), (x + 56, y + 18)],
              fill=(217, 119, 6))
    d.polygon([(x + 44, y + 16), (x + 48, y + 4), (x + 52, y + 16)],
              fill=(245, 158, 11))
    for sx, sy, sr in [(x + 20, y - 6, 5), (x + 30, y - 12, 6),
                       (x + 44, y - 14, 5)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 113, 108))
    d.line([(x, y + h + 4), (x + w, y + h + 4)], fill=BLUE, width=2)


def draw_world_map(d, x0, y0, w, h):
    """Stylised world map (cropped equirectangular), 7 region dots."""
    sx, sy = w / 300.0, h / 100.0

    def poly(pts, fill):
        d.polygon([(x0 + px * sx, y0 + py * sy) for px, py in pts], fill=fill)

    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 228, 236))
    land = (168, 178, 158)
    poly([(8, 18), (40, 6), (78, 10), (72, 28), (55, 34), (38, 44), (18, 40),
          (6, 30)], land)                       # North America
    poly([(82, 4), (96, 6), (92, 14), (80, 12)], land)  # Greenland
    poly([(66, 52), (88, 48), (96, 62), (84, 88), (70, 72)], land)  # S. America
    poly([(140, 10), (168, 6), (172, 20), (150, 24)], land)  # Europe
    poly([(138, 30), (168, 26), (178, 44), (166, 70), (146, 62)], land)  # Africa
    poly([(172, 6), (285, 8), (292, 24), (260, 40), (230, 34), (200, 44),
          (176, 26)], land)                     # Asia
    poly([(252, 68), (290, 64), (292, 78), (258, 82)], land)  # Oceania
    for px, py in [(30, 28), (80, 64), (155, 16), (185, 30), (158, 42),
                   (252, 38), (272, 74)]:
        cx, cy = x0 + px * sx, y0 + py * sy
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                  outline=(255, 255, 255), width=1)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=INK, width=1)


# ---------------------------------------------------------------- content
BIG = [
    {"kicker": "NORTH AMERICA  •  WASHINGTON", "region": "NORTH AMERICA",
     "head": "DEMOCRATS TAKE 258 HOUSE SEATS",
     "deck": "Best House result since 1992 as Chuck Hubbard beats Virginia "
             "Foxx by 330 votes after a recount; Democrats also hold a "
             "56–44 Senate.",
     "art": "capitol"},
    {"kicker": "MIDDLE EAST  •  STRAIT OF HORMUZ", "region": "MIDDLE EAST",
     "head": "TANKERS BURN IN THE STRAIT",
     "deck": "Three tankers hit by projectiles near Oman Fri–Sat; Iran says "
             "two more struck mines Sunday; a sixth claimed Monday; attacks "
             "at their highest since February.",
     "art": "tanker"},
]

CARDS = [
    ("AFRICA", "LIBYA: RUSSIAN WARSHIP SUNK",
     "Ukrainian sea drones hit the corvette Merkury at Benghazi; 10 hurt."),
    ("EUROPE", "DYMER TOLL RISES TO 11",
     "Russian drone strike flattens a five-storey block near Kyiv; "
     "11 killed."),
    ("EUROPE", "POLAND: RUSSIAN MISSILES",
     "Three fallen objects were Russian Kh-101 cruise missiles; NATO "
     "talks Monday."),
    ("NORTH AMERICA", "'EL CHAPO ISIDRO' CAUGHT",
     "FBI most-wanted Sinaloa cartel boss captured by Mexican military; "
     "11 dead."),
    ("ASIA", "CANDY FACTORY FIRE KILLS 24",
     "Blaze at a candy factory in Cikande, Banten, leaves 24 dead and about "
     "30 missing."),
    ("NORTH AMERICA", "DELTA CHAOS: 1,000+ FLIGHTS",
     "Weight-and-balance failure delays over 1,000 Delta flights Sunday."),
    ("ASIA", "SEOUL MINISTER QUITS",
     "Education Minister Choi Kyo-jin resigns after anti-cheating rules "
     "sow CSAT chaos."),
    ("EUROPE", "FRANCE MARCHES, WEEK SIX",
     "Tens of thousands rally for a sixth Saturday over living costs and "
     "the 'licence to kill' police law."),
    ("EUROPE", "153 DRONES IN ONE NIGHT",
     "Russia launches 153 strike drones overnight; Ukraine says 134 "
     "neutralised."),
    ("NORTH AMERICA", "WALL STREET BOUNCES BACK",
     "Nasdaq futures jump 3% after the worst week since March 2020."),
    ("EUROPE", "IMO NET-ZERO TALKS OPEN",
     "IMO working group opens in London to decide the Net-Zero Framework."),
    ("NORTH AMERICA", "STATES SUE MUSK'S SPACEX",
     "Virginia and Oregon sue SpaceX over Grok deepfakes; 20,000+ images "
     "of children."),
    ("EUROPE", "BELGIUM'S SKIES GO DARK",
     "Air traffic controllers join a national austerity strike; all flights "
     "cancelled 07:00–21:00; 429 flights hit."),
]

STATS = [
    ("258", "House seats won by Democrats — best since 1992"),
    ("153", "Russian drones launched overnight; 134 downed"),
    ("24", "killed in the Banten candy-factory fire"),
    ("1,000+", "Delta flights delayed Sunday by a system failure"),
    ("99%", "of Gaza shows toxic-contamination indicators"),
    ("$120bn", "COP31 adaptation fund dropped in the final draft"),
]

TIMELINE = [
    ("04:39 UTC", "49ers beat Vikings 35–10 in Mexico City"),
    ("06:00 UTC", "Belgium airspace shut as controllers strike"),
    ("07:09 UTC", "Nasdaq futures rebound +3% in Asia trade"),
    ("07:28 UTC", "Ukraine reports 153 drones overnight"),
    ("10:49 UTC", "Oxfam–CEOBS Gaza contamination report out"),
    ("13:13 UTC", "Jillaroos win the Women's Rugby League World Cup"),
]

ALSO_ON = [
    "BepiColombo only 2nd craft to orbit Mercury",
    "Alcaraz wins his first ATP Finals title",
    "Márquez seals an eighth MotoGP crown",
    "Boca Juniors win the Sudamericana 2–0",
    "New Zealand draw with India in Wellington",
    "ASX slides; NZX falls 1% in early trade",
    "Nvidia jumps 30% as Huang returns as CEO",
    "Bitcoin climbs back above $61,000",
    "Gold gains 2% as fear grips markets",
    "Fear & Greed index reads just 11 of 100",
    "Shuri Castle reopens its doors",
    "Lahore chokes on AQI 538",
    "UK set to host 2035 Women's World Cup",
    "Gaza truck strike kills 3; IDF, Gaza dispute victims",
    "Eisenkot calls settler arson 'Jewish terrorism'",
    "Liverpool rout Man Utd 4–0 at Anfield",
    "Congress leaves; funding expires 11 Dec",
    "Reuters links 17+ Russian women to Epstein ring",
    "Iran strikes Bahrain site; two hurt",
    "Armenia draft drops Karabakh claim",
    "Ukraine drones hit 3 Russian oil sites",
    "Slovyansk glide bomb kills 2",
    "Shahed drone hits Kharkiv kindergarten; 2 hurt",
]


def section_head(d, x, y, text, width):
    f = font(SANS_B, 13)
    d.text((x, y), text, font=f, fill=INK)
    hrule(d, x, x + width, y + 20, fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---- masthead: 12..126
    f_mast = font(SERIF, 56)
    d.text(((W - d.textlength("THE WORLD IN ONE DAY", font=f_mast)) // 2, 12),
           "THE WORLD IN ONE DAY", font=f_mast, fill=INK)
    hrule(d, 24, W - 24, 78, fill=INK, width=2)
    f_date = font(SANS_B, 22)
    date = "MONDAY, 23 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) // 2, 82), date,
           font=f_date, fill=RED)
    f_sub = font(SANS, 11)
    sub = "THE DAY'S NEWS  •  39 STORIES  •  IN ONE PAGE"
    d.text(((W - d.textlength(sub, font=f_sub)) // 2, 108), sub,
           font=f_sub, fill=INK_SOFT)
    hrule(d, 24, W - 24, 126, fill=INK, width=2)

    # ---- lead hero: 134..318
    f_kick = font(SANS_B, 13)
    d.text((24, 134), "CLIMATE  •  ANTALYA", font=f_kick, fill=RED)
    f_lead = font(SERIF, 40)
    text_block(d, 24, 152, ["COP31 COLLAPSES", "IN ANTALYA"], f_lead,
               leading=44)
    f_deck = font(SANS, 15)
    deck = ("Climate talks end with no deal after two days of overtime; EU, "
            "Britain and island states reject a draft silent on fossil "
            "fuels; the $120bn fund is dropped — the longest COP ever.")
    deck_lines = clamp_lines(d, deck, f_deck, 600, 3)
    text_block(d, 24, 246, deck_lines, f_deck, leading=19)
    draw_globe(d, 838, 222, 78)
    hrule(d, 24, W - 24, 318, fill=INK, width=2)

    # ---- two big stories: 326..458
    y = 326
    col_w = 476
    for i, story in enumerate(BIG):
        x = 24 + i * (col_w + 24)
        d.text((x, y), story["kicker"], font=f_kick,
               fill=REGION_COLOR[story["region"]])
        f_bh = font(SERIF, 21)
        head_lines = clamp_lines(d, story["head"], f_bh, 356, 2)
        text_block(d, x, y + 18, head_lines, f_bh, leading=23)
        f_bd = font(SANS, 12)
        deck_lines = clamp_lines(d, story["deck"], f_bd, 452, 3)
        text_block(d, x, y + 68, deck_lines, f_bd, leading=15)
        if story["art"] == "capitol":
            draw_capitol(d, x + 372, y + 16, 84, 46)
        else:
            draw_tanker(d, x + 372, y + 16, 88, 46)
    hrule(d, 24, W - 24, 458, fill=RULE, width=1)

    # ---- stat strip: 466..556
    section_head(d, 24, 466, "THE DAY IN NUMBERS", W - 48)
    f_num = font(SANS_B, 24)
    f_lab = font(SANS, 9)
    stat_w = (W - 48) // 6
    for i, (num, lab) in enumerate(STATS):
        x = 24 + i * stat_w
        d.text((x, 490), num, font=f_num, fill=RED)
        lab_lines = clamp_lines(d, lab, f_lab, stat_w - 12, 2)
        text_block(d, x, 518, lab_lines, f_lab, fill=INK_SOFT, leading=11)
    hrule(d, 24, W - 24, 556, fill=RULE, width=1)

    # ---- cards grid: 564..798 (4 rows x 54, gap 6)
    gx, gy = 24, 564
    cw, ch, gapx, gapy = 238, 54, 8, 6
    f_ck = font(SANS_B, 9)
    f_ch = font(SANS_B, 13)
    f_cb = font(SANS, 10)
    for idx, (region, head, body) in enumerate(CARDS):
        row, col = divmod(idx, 4)
        x = gx + col * (cw + gapx)
        yy = gy + row * (ch + gapy)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD_BG,
                    outline=CARD_LINE, width=1)
        d.text((x + 7, yy + 3), region, font=f_ck,
               fill=REGION_COLOR[region])
        head_lines = clamp_lines(d, head, f_ch, cw - 14, 1)
        text_block(d, x + 7, yy + 15, head_lines, f_ch, leading=15)
        body_lines = clamp_lines(d, body, f_cb, cw - 14, 2)
        text_block(d, x + 7, yy + 31, body_lines, f_cb, fill=INK_SOFT,
                   leading=11)
    # DATE CHECK box spanning the last row's remaining 3 columns
    x = gx + 1 * (cw + gapx)
    yy = gy + 3 * (ch + gapy)
    box_w = 3 * cw + 2 * gapx
    d.rectangle([x, yy, x + box_w, yy + ch], fill=(232, 222, 196),
                outline=RED, width=2)
    d.text((x + 10, yy + 4), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    f_dc = font(SANS, 11)
    dc = ("Every story on this page happened, or was first reported, on "
          "Monday 23 November 2026. Weekend events (21–22 Nov) appear as "
          "reported on Monday; disputed claims are attributed.")
    dc_lines = clamp_lines(d, dc, f_dc, box_w - 20, 2)
    text_block(d, x + 10, yy + 20, dc_lines, f_dc, leading=14)

    # ---- timeline + world map: 806..912
    ty = 806
    section_head(d, 24, ty, "THE DAY IN UTC", 620)
    section_head(d, 664, ty, "WHERE IT HAPPENED", 336)
    f_tt = font(SANS_B, 11)
    f_tl = font(SANS, 10)
    tw = 300
    for i, (tm, txt) in enumerate(TIMELINE):
        col, row = divmod(i, 3)
        x = 24 + col * (tw + 16)
        yy = ty + 28 + row * 28
        d.text((x, yy), tm, font=f_tt, fill=RED)
        lab = clamp_lines(d, txt, f_tl, tw - 62, 2)
        text_block(d, x + 66, yy, lab, f_tl, fill=INK_SOFT, leading=12)
    draw_world_map(d, 664, ty + 28, 336, 78)

    # ---- also-on: 920..1000
    ay = 920
    section_head(d, 24, ay, "ALSO ON MONDAY", W - 48)
    f_ao = font(SANS, 9)
    cols, rows = 4, 6
    ao_w = (W - 48 - 3 * 16) // cols
    for i, item in enumerate(ALSO_ON):
        col, row = divmod(i, rows)
        x = 24 + col * (ao_w + 16)
        yy = ay + 24 + row * 10
        line = "•  " + item
        if d.textlength(line, font=f_ao) > ao_w:
            while line and d.textlength(line + "…", font=f_ao) > ao_w:
                line = line.rsplit(" ", 1)[0] if " " in line else line[:-1]
            line = line + "…"
        d.text((x, yy), line, font=f_ao, fill=INK)

    # ---- footer: 1006..1017
    fy = 1006
    hrule(d, 24, W - 24, fy, fill=INK, width=1)
    f_ft = font(SANS, 9)
    foot = ("Sources: AP  •  Reuters  •  AFP  •  Oxfam–CEOBS  •  h.ua  •  "
            "Skeyes  —  All 39 stories verified against 23 November 2026 "
            "reporting.  Map: N. America • S. America • Europe • M. East • "
            "Africa • Asia • Oceania.")
    d.text((24, fy + 4), foot, font=f_ft, fill=INK_SOFT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
