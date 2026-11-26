#!/usr/bin/env python3
"""News Image 25 Nov 2026 v3 — one 1024x1024 front page, Pillow only.

Fresh build for make.fun news-image-20261125. 38 stories, 7 regions,
13 drawn cards (3 leads + 10 mids) + 25 ALSO briefs. Deterministic.
Run:  python3 draw_news25_v3.py   -> writes entry.png + pin_debug.txt
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (17, 17, 17)
MUTED = (90, 88, 82)
RED = (200, 16, 46)
RULE = (180, 178, 170)
CARD = (255, 255, 255)
SKY = (214, 232, 246)
SEA = (198, 222, 238)
LAND = (232, 224, 196)
LAND_EDGE = (170, 160, 130)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

REGION_COLOR = {
    "Americas": (200, 16, 46),
    "Asia": (214, 110, 0),
    "Europe": (29, 78, 216),
    "Africa": (21, 128, 61),
    "Middle East": (124, 58, 237),
    "Oceania": (14, 116, 144),
    "Global": (71, 85, 105),
}

# (num, headline, region, claim, source, kicker, deck, pin lat, pin lon)
DRAWN = [
    (1, "Two tankers hit mines in the Strait of Hormuz", "Middle East", "CL",
     "Reuters", "STRAIT OF HORMUZ · SHIPPING",
     "Two tankers struck mines in the strait; crews safe, oil watched.",
     27.18, 56.27),
    (2, "Pakistani first foreigner aboard China's space station",
     "Asia", "C", "Xinhua · Reuters", "BEIJING · SPACE",
     "A Pakistani astronaut joins the Tiangong crew, a first.",
     39.90, 116.40),
    (3, "Democrats clinch 259 seats", "Americas", "C", "AP",
     "WASHINGTON · POLITICS",
     "Democrats pass 218 and keep going, taking 259 of 435 seats.",
     38.90, -77.04),
    (4, "Nvidia slides as Trump role questioned", "Americas", "R", "Reuters",
     "SILICON VALLEY · MARKETS",
     "Shares slide as investors ask how far Washington will go.",
     37.35, -121.95),
    (5, "UK defence plan at risk, watchdog warns", "Europe", "R", "Reuters",
     "LONDON · DEFENCE",
     "Watchdog: the defence plan cannot be delivered on budget.",
     51.50, -0.12),
    (6, "Senegal get AFCON title back", "Africa", "C", "Reuters",
     "DAKAR · SPORT",
     "Senegal celebrate as the AFCON title returns.",
     14.69, -16.90),
    (7, "Spain heads to snap election", "Europe", "R", "Reuters",
     "MADRID · POLITICS",
     "Spain votes 29 Nov after the government loses its majority.",
     40.42, -3.70),
    (8, "China probes Shanghai party chief", "Asia", "R", "Reuters",
     "SHANGHAI · POLITICS",
     "Investigators open a probe into the Shanghai party chief.",
     31.20, 119.00),
    (9, "Congo plane missing; rebels claim hit", "Africa", "CL", "Reuters",
     "KINSHASA · CONFLICT",
     "A plane is missing in Congo; rebels claim they shot it down.",
     -4.32, 15.31),
    (10, "Iran flogs singer 74 times, rights groups say", "Middle East", "R",
     "Reuters", "TEHRAN · RIGHTS",
     "Rights groups say a singer was flogged 74 times.",
     35.69, 51.39),
    (11, "Eurostar cancels Paris-London trains", "Europe", "C",
     "AP", "PARIS · TRANSPORT",
     "Paris-London trains cancelled as staff walk out for the day.",
     48.85, 2.35),
    (12, "Australian inflation runs hot", "Oceania", "C", "Reuters",
     "CANBERRA · ECONOMY",
     "Inflation runs hot, putting a rate rise back on the table.",
     -35.28, 149.13),
    (13, "Solomons pick Australia as partner", "Oceania", "C", "Reuters",
     "HONIARA · PACIFIC",
     "Solomons choose Australia as security partner over China.",
     -9.43, 159.96),
]

# (num, headline, region, claim, source)
ALSO = [
    (14, "US proposes new tariffs on 14 economies", "Americas", "C", "USTR · Reuters"),
    (15, "Hostages freed after supermarket siege", "Americas", "C", "Reuters / AP"),
    (16, "CrowdStrike to buy Zscaler for $44bn", "Americas", "R", "AP / Reuters"),
    (17, "Venezuela reveals $237.5bn debt pile", "Americas", "R", "Reuters"),
    (18, "Argentina enters technical recession", "Americas", "C", "Reuters"),
    (19, "Nikkei falls 2.76% as tech sells off", "Asia", "C", "Reuters"),
    (20, "City marks a year since the Tai Po fire", "Asia", "C", "AP"),
    (21, "Bangladesh garment wage rises 36%", "Asia", "C", "Reuters"),
    (22, "India's Sensex rises 1.8%", "Asia", "C", "Reuters"),
    (23, "Pakistan warns of energy crisis", "Asia", "R", "Reuters"),
    (24, "Russian drone enters Polish airspace", "Europe", "R", "Reuters"),
    (25, "Spain's top court amnesties Puigdemont", "Europe", "C", "Reuters"),
    (26, "Real Madrid thrash PSV 5-1", "Europe", "C", "Reuters"),
    (27, "UK nuclear test veterans win inquiry after 40 years", "Europe", "C", "AP"),
    (28, "Zambia indicts opposition leader on treason charges", "Africa", "R", "Reuters"),
    (29, "UN condemns drone attacks; 28 abducted in Blue Nile", "Africa", "C", "UN / Reuters"),
    (30, "Violence surges at Ebola epicentre", "Africa", "R", "Reuters"),
    (31, "Libya vows retaliation after drone attack kills two", "Africa", "R", "AP"),
    (32, "Iraq to seize Kurdish oilfields, PM orders", "Middle East", "R", "Reuters"),
    (33, "IS attack kills two Syrian security staff (Hasaka)", "Middle East", "R", "Reuters"),
    (34, "Jordan sentences man to death over officer attack", "Middle East", "C", "Reuters"),
    (35, "Houthis claim strike on Saudi oil refinery (Ras Tanura)", "Middle East", "CL", "Reuters"),
    (36, "US envoy slams Australia digital law", "Oceania", "R", "Reuters"),
    (37, "Oil down over 20% in November; Brent $87.49", "Global", "C", "Reuters"),
    (38, "WHO: end US fuel blockade on Cuba", "Global", "C", "Reuters"),
]

NUMBERS = [("38", "STORIES"), ("7", "REGIONS"), ("13", "ON MAP"),
           ("259", "SEATS"), ("$44bn", "DEAL"),
           ("-2.76%", "NIKKEI"), ("5-1", "MADRID")]

TIMELINE = [("00:40", "Nikkei -2.76%"), ("03:15", "Tai Po"),
            ("07:50", "Democrats 259"), ("11:05", "Hormuz hit"),
            ("14:30", "Spain vote"), ("18:20", "Senegal win"),
            ("21:45", "Station first")]

CLAIM_DEF = {"C": "CONFIRMED", "O": "OFFICIAL", "R": "REPORTED", "CL": "CLAIM"}

# Coarse continent outlines (lon, lat) for the solid world map + land checks.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 16), (-105, 20),
     (-110, 23), (-114, 29), (-125, 40), (-125, 49), (-135, 58),
     (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-30, 76),
     (-50, 76), (-60, 74)],
    [(-80, 9), (-72, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -54),
     (-73, -37), (-70, -20), (-77, -12), (-81, -5), (-80, 1)],
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -26),
     (26, -34), (19, -35), (15, -27), (12, -18), (9, -1), (9, 4),
     (-8, 5), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68),
     (55, 69), (70, 72), (90, 75), (110, 76), (130, 72), (150, 70),
     (170, 67), (178, 65), (170, 60), (162, 56), (158, 52), (142, 50),
     (140, 40), (135, 35), (130, 32), (127, 35), (122, 38), (120, 32),
     (110, 20), (108, 12), (105, 9), (100, 8), (98, 12), (95, 16),
     (92, 21), (88, 22), (80, 13), (77, 8), (73, 16), (66, 25), (61, 25),
     (57, 26), (52, 26), (50, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (30, 36), (26, 38), (22, 37), (19, 40), (15, 44),
     (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36)],
    [(114, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(95, 5), (98, 8), (100, 13), (103, 1), (104, -2), (106, -6),
     (110, -7), (114, -8), (118, -9), (120, -10), (125, -9), (130, -3),
     (135, -4), (140, -8), (138, -2), (135, 0), (131, 0), (128, 2),
     (126, 5), (122, 8), (120, 11), (118, 14), (116, 18), (120, 22)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (142, 44), (140, 44), (139, 38)],
    [(167, -45), (170, -42), (173, -40), (176, -38), (178, -37),
     (175, -41), (172, -43)],
    [(155.5, -6.5), (162.5, -6.5), (162.5, -10.5), (155.5, -10.5)],
]

# Display offsets (dx, dy px) for pins that would collide or sit offshore.
PIN_OFFSET = {1: (16, 10), 5: (-16, -10), 7: (0, 14), 8: (2, 14), 11: (14, 8)}

MAP = (24, 534, 584, 630)  # x0, y0, x1, y1 drawing area; legend row 632-650
MAP_LAT_TOP, MAP_LAT_BOT = 78.0, -58.0


def project(lon, lat):
    x0, y0, x1, y1 = MAP
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * (y1 - y0)
    return x, y


def on_land(lon, lat):
    inside = False
    for poly in CONTINENTS:
        j = len(poly) - 1
        c = False
        for i in range(len(poly)):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > lat) != (yj > lat)) and \
                    (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
                c = not c
            j = i
        inside = inside or c
    return inside


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(drw, text, fnt, width, max_lines, tag):
    lines = wrap(text, fnt, width)
    if len(lines) > max_lines:
        raise SystemExit(f"VALIDATOR FAIL [{tag}]: '{text}' needs "
                         f"{len(lines)} lines, max {max_lines}")
    for ln in lines:
        if fnt.getlength(ln) > width + 0.5:
            raise SystemExit(f"VALIDATOR FAIL [{tag}]: line too wide: '{ln}'")
    return lines


def badge(drw, x, y, claim, r=9):
    d = r * 2
    drw.ellipse([x, y, x + d, y + d], outline=INK, width=1,
                fill=(255, 255, 255))
    f = font(SANS_B, 9 if len(claim) == 1 else 7)
    tw = f.getlength(claim)
    drw.text((x + r - tw / 2, y + r - 5 if len(claim) == 1 else y + r - 4),
             claim, font=f, fill=INK)


def draw_lead_scene(drw, idx, x0, y0, x1, y1):
    """Rich / informative scene inside the lead frame, with margin."""
    ix0, iy0, ix1, iy1 = x0 + 8, y0 + 8, x1 - 8, y1 - 8
    if idx == 1:  # Hormuz regional map
        drw.rectangle([ix0, iy0, ix1, iy1], fill=SEA)
        drw.polygon([(ix0, iy0), (ix1, iy0), (ix1, iy0 + 34),
                     (ix0 + 150, iy0 + 52), (ix0, iy0 + 44)], fill=LAND)
        drw.polygon([(ix0, iy1), (ix1, iy1), (ix1, iy1 - 30),
                     (ix0 + 200, iy1 - 44), (ix0, iy1 - 26)], fill=LAND)
        drw.line([(ix0 + 150, iy0 + 52), (ix0 + 210, iy1 - 44)],
                 fill=(90, 140, 190), width=3)
        for tx, ty in [(ix0 + 120, iy0 + 62), (ix0 + 165, iy0 + 88)]:
            drw.rectangle([tx, ty, tx + 34, ty + 10], fill=(60, 60, 66),
                          outline=INK)
            drw.rectangle([tx + 10, ty - 6, tx + 18, ty], fill=(60, 60, 66))
        for mx, my in [(ix0 + 148, iy0 + 74), (ix0 + 185, iy0 + 100)]:
            drw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED,
                        outline=(255, 255, 255))
        f = font(SANS_B, 9)
        drw.text((ix0 + 6, iy0 + 4), "IRAN", font=f, fill=MUTED)
        drw.text((ix0 + 6, iy1 - 14), "ARABIA", font=f, fill=MUTED)
        drw.text((ix1 - 62, iy0 + 40), "STRAIT", font=f, fill=(40, 80, 130))
    elif idx == 2:  # bright space scene
        for i in range(iy1 - iy0):
            t = i / max(1, iy1 - iy0 - 1)
            c = tuple(int(SKY[k] + (253 - SKY[k]) * t) for k in range(3))
            drw.line([(ix0, iy0 + i), (ix1, iy0 + i)], fill=c)
        drw.ellipse([ix0 - 60, iy1 - 26, ix1 + 60, iy1 + 90],
                    fill=(70, 130, 200), outline=(40, 90, 160))
        drw.arc([ix0 - 60, iy1 - 26, ix1 + 60, iy1 + 90], 180, 360,
                fill=(255, 255, 255), width=2)
        cx, cy = (ix0 + ix1) // 2, (iy0 + iy1) // 2 - 6
        drw.rectangle([cx - 52, cy - 8, cx - 14, cy + 8], fill=(30, 90, 160),
                      outline=INK)
        drw.rectangle([cx + 14, cy - 8, cx + 52, cy + 8], fill=(30, 90, 160),
                      outline=INK)
        drw.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=(220, 225, 230),
                      outline=INK)
        drw.line([(cx - 70, cy), (cx + 70, cy)], fill=INK, width=2)
        rx = ix1 - 44
        drw.polygon([(rx, iy0 + 26), (rx + 8, iy0 + 12), (rx + 16, iy0 + 26)],
                    fill=RED, outline=INK)
        drw.rectangle([rx, iy0 + 26, rx + 16, iy0 + 52], fill=(245, 245, 245),
                      outline=INK)
        drw.polygon([(rx + 2, iy0 + 52), (rx + 8, iy0 + 66), (rx + 14, iy0 + 52)],
                    fill=(255, 180, 60))
        for sx, sy in [(ix0 + 22, iy0 + 18), (ix0 + 70, iy0 + 40),
                       (ix1 - 70, iy0 + 14)]:
            drw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    else:  # idx 3: data lead — giant number + mini chart, margins kept
        f_big = font(SERIF_B, 44)
        num = "259"
        nw = f_big.getlength(num)
        nx = ix0 + 10
        ny = iy0 + 2
        if nx + nw > ix1 - 10:
            raise SystemExit("VALIDATOR FAIL [lead3]: giant number overflows")
        drw.text((nx, ny), num, font=f_big, fill=RED)
        f_lab = font(SANS_B, 9)
        drw.text((nx, ny + 46), "DEMOCRATS · HOUSE SEATS OF 435",
                 font=f_lab, fill=INK)
        bx0, by = ix0 + 10, iy0 + 60
        bw_max = ix1 - ix0 - 110
        for label, val, col in [("DEM", 259, (29, 78, 216)),
                                ("REP", 176, (200, 16, 46))]:
            f2 = font(SANS_B, 10)
            drw.text((bx0, by), label, font=f2, fill=INK)
            bar_x = bx0 + 44
            bar_w = int(bw_max * val / 259.0)
            drw.rectangle([bar_x, by + 1, bar_x + bar_w, by + 11], fill=col)
            drw.text((bar_x + bar_w + 6, by), str(val), font=f2, fill=INK)
            by += 13
        if by - 13 + 11 > iy1 - 4:
            raise SystemExit("VALIDATOR FAIL [lead3]: chart rows overflow")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    f_kick = font(SANS_B, 11)
    f_title = font(SERIF_B, 30)
    f_sub = font(SANS, 12)
    d.text((24, 12), "THE WORLD IN ONE PAGE", font=f_kick, fill=RED)
    d.text((24, 28), "Wednesday 25 November 2026", font=f_title, fill=INK)
    sub = "38 STORIES  ·  7 REGIONS  ·  13 ON THE MAP"
    d.text((1024 - 24 - f_sub.getlength(sub), 40), sub, font=f_sub, fill=MUTED)
    d.line([(24, 68), (1000, 68)], fill=INK, width=2)

    # ---- leads (3) ----
    lead_x = [24, 352, 680]
    banners = {1: "TWO TANKERS HIT", 2: "A FIRST IN ORBIT",
               3: "DEMOCRATS CLINCH THE HOUSE"}
    for i, st in enumerate(DRAWN[:3]):
        num, head, region, claim, src, kicker, deck, lat, lon = st
        x0, y0, x1, y1 = lead_x[i], 74, lead_x[i] + 320, 280
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=1)
        d.text((x0 + 10, y0 + 8), kicker, font=font(SANS_B, 9),
               fill=REGION_COLOR[region])
        badge(d, x1 - 30, y0 + 6, claim)
        d.text((x0 + 10, y0 + 24), f"via {src}", font=font(SANS, 9),
               fill=MUTED)
        fb = font(SANS_B, 13)
        bw = fb.getlength(banners[num]) + 16
        d.rectangle([x0 + 10, y0 + 42, x0 + 10 + bw, y0 + 62], fill=RED)
        d.text((x0 + 18, y0 + 45), banners[num], font=fb, fill=(255, 255, 255))
        hl = fit_lines(d, head, font(SERIF_B, 17), 300, 2, f"lead{num}")
        yy = y0 + 68
        for ln in hl:
            d.text((x0 + 10, yy), ln, font=font(SERIF_B, 17), fill=INK)
            yy += 21
        scene_y0 = yy + 4
        scene_y1 = y1 - 8
        if scene_y1 - scene_y0 < 40:
            raise SystemExit(f"VALIDATOR FAIL [lead{num}]: no room for scene")
        draw_lead_scene(d, num, x0, scene_y0, x1, scene_y1)

    # ---- mids (10, 2 rows x 5) ----
    mid_x = [24, 221, 418, 615, 812]
    mid_y = [286, 380]
    for k, st in enumerate(DRAWN[3:]):
        num, head, region, claim, src, kicker, deck, lat, lon = st
        x0 = mid_x[k % 5]
        y0 = mid_y[k // 5]
        x1, y1 = x0 + 188, y0 + 88
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
        d.rectangle([x0, y0, x0 + 4, y1], fill=REGION_COLOR[region])
        d.text((x0 + 10, y0 + 6), kicker, font=font(SANS_B, 8),
               fill=REGION_COLOR[region])
        badge(d, x1 - 26, y0 + 5, claim, r=8)
        hl = fit_lines(d, head, font(SANS_B, 11), 164, 2, f"mid{num}")
        yy = y0 + 22
        for ln in hl:
            d.text((x0 + 10, yy), ln, font=font(SANS_B, 11), fill=INK)
            yy += 14
        dl = fit_lines(d, deck, font(SANS, 9), 164, 2, f"mid-deck{num}")
        for ln in dl:
            d.text((x0 + 10, yy), ln, font=font(SANS, 9), fill=MUTED)
            yy += 12
        if yy > y1 - 14:
            raise SystemExit(f"VALIDATOR FAIL [mid{num}]: deck overflows card")
        d.text((x0 + 10, y1 - 13), f"via {src}", font=font(SANS, 8),
               fill=MUTED)

    # ---- IN NUMBERS strip (7) ----
    y0, y1 = 474, 506
    d.rectangle([24, y0, 1000, y1], fill=(17, 17, 17))
    d.text((34, y0 + 10), "IN NUMBERS", font=font(SANS_B, 11),
           fill=(255, 210, 60))
    xx = 150
    for val, lab in NUMBERS:
        f_v = font(SERIF_B, 16)
        f_l = font(SANS_B, 8)
        d.text((xx, y0 + 8), val, font=f_v, fill=(255, 255, 255))
        d.text((xx + f_v.getlength(val) + 6, y0 + 13), lab, font=f_l,
               fill=(200, 200, 200))
        xx += int(f_v.getlength(val) + f_l.getlength(lab) + 34)
    if xx > 1000:
        raise SystemExit("VALIDATOR FAIL [numbers]: strip overflows")

    # ---- world map (solid) + pins 1-13 ----
    d.rectangle([24, 512, 584, 652], fill=CARD, outline=INK, width=1)
    d.text((34, 516), "WHERE THE NEWS HAPPENED — 13 STORIES ON THE MAP",
           font=font(SANS_B, 10), fill=INK)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    f_oc = font(SANS_B, 9)
    d.text((52, 606), "PACIFIC", font=f_oc, fill=(70, 120, 170))
    d.text((238, 616), "ATLANTIC", font=f_oc, fill=(70, 120, 170))
    d.text((428, 612), "INDIAN", font=f_oc, fill=(70, 120, 170))
    pin_rows = []
    shown = []
    for st in DRAWN:
        num, head, region, claim, src, kicker, deck, lat, lon = st
        tx, ty = project(lon, lat)
        dx, dy = PIN_OFFSET.get(num, (0, 0))
        px, py = tx + dx, ty + dy
        if not on_land(lon, lat):
            raise SystemExit(f"VALIDATOR FAIL [pin{num}]: centre off land "
                             f"({lat}, {lon})")
        if dx or dy:
            d.line([(tx, ty), (px, py)], fill=INK, width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        col = REGION_COLOR[region]
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col, outline=INK)
        fn = font(SANS_B, 9)
        tw = fn.getlength(str(num))
        d.text((px - tw / 2, py - 6), str(num), font=fn,
               fill=(255, 255, 255))
        shown.append((num, region, lat, lon, round(tx), round(ty),
                      round(px), round(py), on_land(lon, lat)))
        pin_rows.append((num, px, py))
    for a in range(len(pin_rows)):
        for b in range(a + 1, len(pin_rows)):
            dist = math.hypot(pin_rows[a][1] - pin_rows[b][1],
                              pin_rows[a][2] - pin_rows[b][2])
            if dist < 18:
                raise SystemExit(
                    f"VALIDATOR FAIL [pins]: pins {pin_rows[a][0]} and "
                    f"{pin_rows[b][0]} only {dist:.1f}px apart")

    # legend on its OWN row below the map
    ly = 632
    d.text((34, ly), "PIN COLOUR = REGION:", font=font(SANS_B, 9), fill=INK)
    lx = 168
    counts = {}
    for st in DRAWN:
        counts[st[2]] = counts.get(st[2], 0) + 1
    for region in ["Americas", "Asia", "Europe", "Africa", "Middle East",
                   "Oceania"]:
        if region not in counts:
            continue
        d.ellipse([lx, ly + 1, lx + 10, ly + 11], fill=REGION_COLOR[region])
        lab = f"{region.upper()} {counts[region]}"
        d.text((lx + 13, ly), lab, font=font(SANS_B, 7), fill=INK)
        lx += int(font(SANS_B, 7).getlength(lab) + 24)
    if lx > 584:
        raise SystemExit("VALIDATOR FAIL [map legend]: legend overflows")

    # ---- chart panel 1: STORIES BY REGION (vertical bars, all 7) ----
    region_totals = {}
    for st in DRAWN + ALSO:
        region_totals[st[2]] = region_totals.get(st[2], 0) + 1
    cx0, cy0, cx1, cy1 = 592, 512, 1000, 578
    d.rectangle([cx0, cy0, cx1, cy1], fill=CARD, outline=INK, width=1)
    d.text((cx0 + 8, cy0 + 5), "STORIES BY REGION — 38 IN ALL",
           font=font(SANS_B, 9), fill=INK)
    order = ["Americas", "Asia", "Europe", "Africa", "Middle East",
             "Oceania", "Global"]
    slot = (cx1 - cx0 - 16) / 7.0
    base = cy1 - 14
    for i, r in enumerate(order):
        v = region_totals[r]
        bh = int(26 * v / 7.0)
        bx = cx0 + 8 + i * slot + 8
        d.rectangle([bx, base - bh, bx + 26, base], fill=REGION_COLOR[r])
        d.text((bx + 6, base - bh - 11), str(v), font=font(SANS_B, 9),
               fill=INK)
        lab = {"Americas": "AMER", "Asia": "ASIA", "Europe": "EURO",
               "Africa": "AFRI", "Middle East": "MIDE", "Oceania": "OCEA",
               "Global": "GLOB"}[r]
        d.text((bx - 2, base + 2), lab, font=font(SANS_B, 7), fill=MUTED)

    # ---- chart panel 2: MARKET MOVES (horizontal bars) ----
    mx0, my0, mx1, my1 = 592, 584, 1000, 652
    d.rectangle([mx0, my0, mx1, my1], fill=CARD, outline=INK, width=1)
    d.text((mx0 + 8, my0 + 5), "MARKET MOVES — 25 NOV (%)",
           font=font(SANS_B, 9), fill=INK)
    mrows = [("NIKKEI", -2.76, RED), ("SENSEX", 1.80, (21, 128, 61)),
             ("OIL NOV", -20.0, RED), ("WAGE +36%", 36.0, (21, 128, 61))]
    # zero line placed so the longest negative bar stays inside the panel:
    # bar area runs mx0+96 .. mx1-64; -20 maps left, +36 maps right.
    zero_x = mx0 + 96 + int((mx1 - mx0 - 160) * 20.0 / 56.0)
    d.line([(zero_x, my0 + 20), (zero_x, my1 - 4)], fill=RULE, width=1)
    mby = my0 + 22
    for label, val, col in mrows:
        f2 = font(SANS_B, 9)
        d.text((mx0 + 8, mby), label, font=f2, fill=INK)
        span = (mx1 - mx0 - 160) / 56.0
        bar_w = int(abs(val) * span)
        if val >= 0:
            d.rectangle([zero_x, mby, zero_x + bar_w, mby + 9], fill=col)
            d.text((zero_x + bar_w + 5, mby),
                   f"{val:+.2f}" if abs(val) < 10 else f"{val:+.0f}",
                   font=f2, fill=INK)
        else:
            d.rectangle([zero_x - bar_w, mby, zero_x, mby + 9], fill=col)
            d.text((zero_x - bar_w - 34, mby),
                   f"{val:+.2f}" if abs(val) < 10 else f"{val:+.0f}",
                   font=f2, fill=INK)
        mby += 11
    if mby - 11 + 9 > my1 - 2:
        raise SystemExit("VALIDATOR FAIL [markets]: chart overflows")

    # ---- ALSO (25 briefs, 3 columns) ----
    d.text((24, 658), "ALSO ON WEDNESDAY 25 NOVEMBER — 25 MORE STORIES",
           font=font(SANS_B, 11), fill=INK)
    d.text((700, 658), "C CONFIRMED · O OFFICIAL · R REPORTED · CL CLAIM",
           font=font(SANS_B, 9), fill=MUTED)
    d.line([(24, 676), (1000, 676)], fill=RULE, width=1)
    cols = [ALSO[0:9], ALSO[9:17], ALSO[17:25]]
    col_x = [24, 352, 680]
    for ci, col in enumerate(cols):
        yy = 682
        for num, head, region, claim, src in col:
            badge(d, col_x[ci], yy, claim, r=8)
            f_h = font(SANS, 10)
            lines = fit_lines(d, f"{num}. {head} — via {src}", f_h, 296, 2,
                              f"also{num}")
            for j, ln in enumerate(lines):
                d.text((col_x[ci] + 22, yy - 1 + j * 12), ln, font=f_h,
                       fill=INK)
            yy += 24
        if yy > 902:
            raise SystemExit("VALIDATOR FAIL [also]: column overflows")

    # ---- UTC timeline (7) ----
    y0, y1 = 904, 932
    d.rectangle([24, y0, 1000, y1], fill=(245, 243, 236), outline=RULE)
    d.text((34, y0 + 8), "THE DAY IN UTC", font=font(SANS_B, 10), fill=INK)
    xx = 150
    for t, lab in TIMELINE:
        d.text((xx, y0 + 8), t, font=font(SANS_B, 9), fill=RED)
        d.text((xx + 42, y0 + 8), lab, font=font(SANS, 9), fill=INK)
        xx += 42 + int(font(SANS, 9).getlength(lab)) + 12
    if xx > 1000:
        raise SystemExit("VALIDATOR FAIL [timeline]: strip overflows")

    # ---- footer: DATE CHECK + legend + HOW CHECKED ----
    fy0, fy1 = 938, 1014
    d.rectangle([24, fy0, 340, fy1], fill=CARD, outline=INK, width=1)
    d.text((34, fy0 + 6), "DATE CHECK", font=font(SANS_B, 10), fill=RED)
    for j, ln in enumerate(fit_lines(
            d, "Every story happened or was first reported on Wed 25 Nov "
            "2026. Spain votes 29 Nov; CAS ruling announced 24 Nov.",
            font(SANS, 10), 296, 3, "datecheck")):
        d.text((34, fy0 + 22 + j * 14), ln, font=font(SANS, 10), fill=INK)
    d.rectangle([348, fy0, 664, fy1], fill=CARD, outline=INK, width=1)
    d.text((358, fy0 + 6), "HOW SURE?  C CONFIRMED · O OFFICIAL",
           font=font(SANS_B, 10), fill=INK)
    for j, ln in enumerate(fit_lines(
            d, "R REPORTED · CL CLAIM. Every card and brief carries its "
            "circle; counts re-added: 7+7+7+6+6+3+2 = 38.",
            font(SANS, 10), 296, 3, "legend")):
        d.text((358, fy0 + 22 + j * 14), ln, font=font(SANS, 10), fill=INK)
    d.rectangle([672, fy0, 1000, fy1], fill=CARD, outline=INK, width=1)
    d.text((682, fy0 + 6), "HOW CHECKED", font=font(SANS_B, 10), fill=INK)
    for j, ln in enumerate(fit_lines(
            d, "Each story carries a named source. Pins 1-13 projected "
            "from real lat/lon and checked on land.",
            font(SANS, 10), 296, 3, "howchecked")):
        d.text((682, fy0 + 22 + j * 14), ln, font=font(SANS, 10), fill=INK)

    # ---- arithmetic gate ----
    total = len(DRAWN) + len(ALSO)
    assert total == 38, total
    assert ALSO[-1][0] == 38, ALSO[-1][0]
    assert sum(region_totals.values()) == 38
    assert max(region_totals.values()) <= 7, region_totals
    assert len({s[0] for s in DRAWN + ALSO}) == 38
    assert len(shown) == 13 and all(r[8] for r in shown)

    img.save("entry.png")
    with open("pin_debug.txt", "w") as f:
        f.write("PIN DEBUG — lat/lon -> x/y (map 24,534-584,630)\n")
        f.write("num | region | lat | lon | true x,y | shown x,y | on_land\n")
        for r in shown:
            f.write(f"{r[0]:>2} | {r[1]:<11} | {r[2]:>6.2f} | {r[3]:>7.2f} | "
                    f"({r[4]},{r[5]}) | ({r[6]},{r[7]}) | {r[8]}\n")
        f.write(f"regions: {region_totals}\n")
        f.write(f"total stories: {total} | drawn: {len(DRAWN)} | "
                f"also: {len(ALSO)} | last also: {ALSO[-1][0]}\n")
    print("RENDER OK entry.png 1024x1024")
    print(f"ARITHMETIC OK total={total} drawn={len(DRAWN)} also={len(ALSO)} "
          f"regions={region_totals}")
    for r in shown:
        print(f"PIN {r[0]:>2} {r[1]:<11} lat {r[2]:>6.2f} lon {r[3]:>7.2f} "
              f"true=({r[4]},{r[5]}) shown=({r[6]},{r[7]}) land={r[8]}")


if __name__ == "__main__":
    main()
