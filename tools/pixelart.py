#!/usr/bin/env python3
"""Generate the pixel-art assets for the sage/Win95 theme."""
import zlib, struct, os

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img"))
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- png writer
def write_png(name, px, scale=1):
    h, w = len(px), len(px[0])
    raw = b""
    for row in px:
        line = b"\x00"
        for p in row:
            line += bytes(p) * scale
        raw += line * scale
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    body = (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w * scale, h * scale, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))
    path = os.path.join(OUT, name)
    open(path, "wb").write(body)
    print(f"  {name}  {w*scale}x{h*scale}")

def grid(rows, legend):
    return [[legend[c] for c in row] for row in rows]

# ---------------------------------------------------------------- palette
T  = (0, 0, 0, 0)
DK = (0x3E, 0x52, 0x31, 255)   # dark sage outline
MD = (0x7C, 0x9A, 0x63, 255)   # mid sage fill
LT = (0x9F, 0xB8, 0x86, 255)   # light sage
PL = (0xE2, 0xE9, 0xD1, 255)   # pale
GD = (0xC2, 0x99, 0x4E, 255)   # muted gold
RS = (0xA8, 0x5A, 0x32, 255)   # muted rust

# ---------------------------------------------------------------- cursors
print("cursors")

ARROW = [
    "d...............",
    "dd..............",
    "dmd.............",
    "dmmd............",
    "dmmmd...........",
    "dmmmmd..........",
    "dmmmmmd.........",
    "dmmmmmmd........",
    "dmmmmmmmd.......",
    "dmmmmmmmmd......",
    "dmmmmmddddd.....",
    "dmmdmmd.........",
    "dmd.dmmd........",
    "dd..dmmd........",
    "d....dmmd.......",
    ".....dddd.......",
]

HAND = [
    "......dd........",
    ".....dmmd.......",
    ".....dmmd.......",
    ".....dmmd.......",
    ".....dmmd.......",
    ".....dmmddd.....",
    ".....dmmdmmdd...",
    ".....dmmdmmdmmd.",
    "..dd.dmmdmmdmmd.",
    "..dmmdmmmmmmmmmd",
    "..dmmmmmmmmmmmmd",
    "...dmmmmmmmmmmd.",
    "...dmmmmmmmmmmd.",
    "....dmmmmmmmmmd.",
    "....dmmmmmmmmmd.",
    "....ddddddddddd.",
]

cur_legend = {".": T, "d": DK, "m": MD}
write_png("cursor-arrow.png", grid(ARROW, cur_legend), scale=2)
write_png("cursor-hand.png",  grid(HAND,  cur_legend), scale=2)

# ---------------------------------------------------------------- nav icons
print("icons")

FOLDER = [
    "................",
    "................",
    "..dddd..........",
    ".dllllddddddddd.",
    ".dlllllllllllld.",
    ".dlllllllllllld.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dmmmmmmmmmmmmd.",
    ".dddddddddddddd.",
    "................",
    "................",
    "................",
]

icon_legend = {".": T, "d": DK, "l": LT, "m": MD}
write_png("icon-folder.png", grid(FOLDER, icon_legend), scale=1)

# envelope: box rows 4..12 / cols 1..14, with a V flap meeting at the centre
env = [[T for _ in range(16)] for _ in range(16)]
for x in range(1, 15):
    env[4][x] = env[12][x] = DK
for y in range(5, 12):
    env[y][1] = env[y][14] = DK
    for x in range(2, 14):
        env[y][x] = LT
for i in range(6):                      # the two diagonals of the flap
    env[5 + i][2 + i] = DK
    env[5 + i][13 - i] = DK
write_png("icon-envelope.png", env, scale=1)

# linkedin: solid tile with light "in"
li = [[DK for _ in range(16)] for _ in range(16)]
for y in range(1, 15):
    for x in range(1, 15):
        li[y][x] = MD
def fill(px, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[y][x] = c
fill(li, 3, 3, 4, 4, PL)      # i dot
fill(li, 3, 6, 4, 12, PL)     # i stem
fill(li, 7, 6, 8, 12, PL)     # n stem
fill(li, 9, 6, 10, 7, PL)     # n shoulder
fill(li, 11, 7, 12, 12, PL)   # n leg
write_png("icon-linkedin.png", li, scale=1)

# ---------------------------------------------------------------- wallpaper
print("wallpaper")
W = H = 64
BASE  = (0x7C, 0x94, 0x63, 255)
BASE2 = (0x77, 0x8F, 0x5E, 255)
TUFT  = (0x69, 0x82, 0x51, 255)
TUFT2 = (0x8D, 0xA6, 0x72, 255)

wp = [[BASE for _ in range(W)] for _ in range(H)]

# subtle dither so the field itself reads as pixels
for y in range(H):
    for x in range(W):
        if (x * 7 + y * 13) % 23 == 0:
            wp[y][x] = BASE2

def blit(px, rows, legend, ox, oy):
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == ".":
                continue
            px[(oy + dy) % H][(ox + dx) % W] = legend[ch]

FLOWER = [
    ".p.",
    "pgp",
    ".p.",
]
TUFT_S = [
    "t.t",
    "ttt",
    ".t.",
]
SPRIG = [
    "..t",
    ".t.",
    "tt.",
]

tf_legend = {"t": TUFT, ".": T}

# three flower varieties keep the field from reading as all-green
fl_white = {"p": PL, "g": GD, ".": T}                                   # white petals, gold centre
fl_blue  = {"p": (0x8F, 0xB4, 0xDC, 255), "g": (0x27, 0x3F, 0x6E, 255), ".": T}
fl_pink  = {"p": (0xE8, 0x8B, 0xA3, 255), "g": (0xCE, 0x5A, 0x2E, 255), ".": T}

for (x, y) in [(6, 9), (49, 14), (40, 38), (21, 55), (34, 22)]:
    blit(wp, FLOWER, fl_white, x, y)
for (x, y) in [(27, 4), (14, 33), (57, 46)]:
    blit(wp, FLOWER, fl_blue, x, y)
for (x, y) in [(44, 27), (9, 46)]:
    blit(wp, FLOWER, fl_pink, x, y)
for (x, y) in [(17, 3), (36, 11), (2, 20), (54, 5), (24, 15), (45, 20),
               (11, 27), (30, 31), (59, 33), (5, 38), (50, 41), (20, 44),
               (38, 50), (60, 55), (13, 60), (29, 41), (47, 58)]:
    blit(wp, TUFT_S, tf_legend, x, y)
for (x, y) in [(33, 7), (7, 30), (52, 30), (26, 48), (43, 8), (16, 17)]:
    blit(wp, SPRIG, tf_legend, x, y)
for (x, y) in [(3, 12), (22, 26), (41, 45), (55, 22), (12, 52), (48, 52), (31, 60)]:
    wp[y % H][x % W] = TUFT2

write_png("wallpaper.png", wp, scale=1)

# ---------------------------------------------------------------- me.png
print("headshot placeholder")
S = 40
FIELD    = (0xE8, 0xEE, 0xDA, 255)
OUTLINE  = (0x3E, 0x52, 0x31, 255)
HAIR     = (0x4A, 0x3B, 0x2E, 255)
HAIR_HI  = (0x63, 0x4E, 0x3C, 255)
SKIN     = (0xC9, 0xA5, 0x86, 255)
SKIN_SH  = (0xB1, 0x8C, 0x6E, 255)
SHIRT    = (0x6E, 0x8A, 0x5C, 255)
SHIRT_SH = (0x5A, 0x73, 0x4A, 255)

me = [[FIELD for _ in range(S)] for _ in range(S)]

cx, cy, r = 19.5, 17.0, 8.6

# shoulders
for y in range(27, S):
    half = 7 + (y - 27) * 1.35
    for x in range(S):
        if abs(x - cx) <= half:
            me[y][x] = SHIRT_SH if abs(x - cx) > half - 1.6 else SHIRT
# neck
for y in range(24, 29):
    for x in range(17, 23):
        me[y][x] = SKIN_SH if x >= 21 else SKIN
# head
for y in range(S):
    for x in range(S):
        if ((x - cx) ** 2) / (r ** 2) + ((y - cy) ** 2) / ((r + 1.4) ** 2) <= 1:
            me[y][x] = SKIN_SH if x - cx > r * 0.45 else SKIN
# hair: cap + side lengths
for y in range(S):
    for x in range(S):
        d = ((x - cx) ** 2) / ((r + 1.1) ** 2) + ((y - cy) ** 2) / ((r + 2.4) ** 2)
        if d <= 1 and (y < cy - 2.5 or abs(x - cx) > r - 1.4):
            me[y][x] = HAIR_HI if (y < cy - 5 and x < cx) else HAIR
# hair falling past the jaw
for y in range(int(cy), 30):
    for x in range(S):
        if r - 1.6 < abs(x - cx) <= r + 2.2:
            me[y][x] = HAIR
# eyes + mouth
for x in (16, 17):
    me[17][x] = OUTLINE
for x in (22, 23):
    me[17][x] = OUTLINE
for x in range(18, 22):
    me[21][x] = SKIN_SH

# pixel vignette border
for i in range(S):
    me[0][i] = me[S - 1][i] = OUTLINE
    me[i][0] = me[i][S - 1] = OUTLINE

print("done")

# ---------------------------------------------------------------- project icons
print("project icons")

def blank(n=16):
    return [[T for _ in range(n)] for _ in range(n)]

# trophy
tr = blank()
for y in range(2, 9):                       # cup
    for x in range(4, 12):
        tr[y][x] = LT if y < 6 else MD
for y in range(2, 9):
    tr[y][3] = tr[y][12] = DK
for x in range(3, 13):
    tr[1][x] = DK
for x in range(4, 12):
    tr[9][x] = DK
for y in range(3, 7):                       # handles
    tr[y][1] = tr[y][14] = DK
    tr[y][2] = tr[y][13] = LT
tr[2][2] = tr[2][13] = DK
tr[7][2] = tr[7][13] = DK
for y in range(9, 12):                      # stem
    for x in range(7, 9):
        tr[y][x] = MD
    tr[y][6] = tr[y][9] = DK
for x in range(4, 12):                      # base
    tr[12][x] = tr[13][x] = MD
    tr[14][x] = DK
for y in (12, 13):
    tr[y][3] = tr[y][12] = DK
tr[11][3] = tr[11][12] = DK
for x in range(3, 13):
    tr[11][x] = DK if x in (3, 12) else tr[11][x]
write_png("icon-trophy.png", tr, scale=1)

# shopping cart
ct = blank()
for x in range(1, 4):                       # handle
    ct[3][x] = DK
for y in range(3, 6):
    ct[y][3] = DK
for x in range(4, 14):                      # basket top
    ct[5][x] = DK
for y in range(6, 11):
    ct[y][4 + (y - 6) // 2] = DK
    ct[y][13 - (y - 6) // 2] = DK
    for x in range(5 + (y - 6) // 2, 13 - (y - 6) // 2):
        ct[y][x] = LT if y < 8 else MD
for x in range(6, 12):
    ct[10][x] = DK
for cxw in (6, 12):                         # wheels
    for dy in range(2):
        for dx in range(2):
            ct[12 + dy][cxw + dx] = DK
write_png("icon-cart.png", ct, scale=1)

# globe
gl = blank()
cx = cy = 7.5
for y in range(16):
    for x in range(16):
        d = (x - cx) ** 2 + (y - cy) ** 2
        if d <= 6.6 ** 2:
            gl[y][x] = LT
        if 5.6 ** 2 < d <= 6.6 ** 2:
            gl[y][x] = DK
for y in range(2, 14):                      # meridian
    if gl[y][7] != T: gl[y][7] = DK
    if gl[y][8] != T: gl[y][8] = DK
for x in range(1, 15):                      # equator + parallels
    for y in (7, 8):
        if gl[y][x] != T: gl[y][x] = DK
    for y in (4, 11):
        if gl[y][x] != T and abs(x - cx) < 5.2: gl[y][x] = DK
write_png("icon-globe.png", gl, scale=1)

# headshot placeholder, sized 1:1 for the 240px frame.
# guarded so re-running this script never overwrites a real photo.
if os.path.exists(os.path.join(OUT, "me.png")):
    print("  me.png  exists, left alone")
else:
    write_png("me.png", me, scale=6)
