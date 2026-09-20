#!/usr/bin/env python3
"""Draws the mod icon: a rocket, a ringed planet and a little moon.

Authored as a 32x32 pixel grid and scaled 8x with nearest-neighbour, so it
still looks like Minecraft art at 256x256. Colours are lifted straight out of
the mod's own block and item textures.
"""
import os, struct, zlib

# The generated mod manifest points at assets/icon.png, not assets/<modid>/.
OUT = "/Users/elduinnunn/GitHub/planets-mod/src/main/resources/assets/icon.png"
PREVIEW = "/Users/elduinnunn/GitHub/planets-mod/build/icon_preview.png"
SIZE = 32
SCALE = 8


def hx(s):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)


# straight from the mod's textures
SPACE = hx("#080A16")
SPACE_LOW = hx("#11152A")
STAR = hx("#FFFFFF")
STAR_DIM = hx("#9FB6D8")

PLANET_LIGHT = hx("#E08A4A")
PLANET_MID = hx("#C05A2E")
PLANET_DARK = hx("#7E3B24")
RING_LIGHT = hx("#F3CE96")
RING_DARK = hx("#C79A62")

MOON_LIGHT = hx("#C6C2B8")
MOON_DARK = hx("#8D8D8D")

W = hx("#E6E9EE")   # rocket body
G = hx("#8B949E")   # rocket fins
R = hx("#D8232A")   # rocket nose and stripe
F = hx("#FF8A1F")   # flame
Y = hx("#FFD84A")   # flame core

ROCKET = [
    "....R....",
    "...RRR...",
    "...WWW...",
    "..WWWWW..",
    "..WWWWW..",
    "..WRRRW..",
    "..WWWWW..",
    ".GWWWWWG.",
    ".GWWWWWG.",
    "GGWWWWWGG",
    "...FFF...",
    "...FYF...",
    "....F....",
]
ROCKET_KEY = {"W": W, "G": G, "R": R, "F": F, "Y": Y}

STARS = [
    (2, 19, STAR), (5, 27, STAR_DIM), (1, 24, STAR_DIM), (14, 3, STAR),
    (18, 7, STAR_DIM), (21, 2, STAR), (30, 13, STAR_DIM), (28, 18, STAR),
    (13, 9, STAR_DIM), (30, 27, STAR_DIM), (24, 29, STAR), (16, 30, STAR_DIM),
    (9, 20, STAR), (2, 12, STAR_DIM), (23, 12, STAR),
]


def blank():
    """Space, fading very slightly lighter towards the bottom."""
    grid = []
    for y in range(SIZE):
        t = y / (SIZE - 1)
        shade = tuple(round(SPACE[i] + (SPACE_LOW[i] - SPACE[i]) * t) for i in range(3)) + (255,)
        grid.append([shade for _ in range(SIZE)])
    return grid


def disc(grid, cx, cy, r, light, mid, dark):
    for y in range(SIZE):
        for x in range(SIZE):
            dx, dy = x - cx, y - cy
            d = (dx * dx + dy * dy) ** 0.5
            if d > r:
                continue
            # light comes from the upper left
            lit = (-dx - dy) / max(r, 1)
            grid[y][x] = light if lit > 0.45 else (mid if lit > -0.35 else dark)


def ring(grid, cx, cy, rx, ry, only_below=None):
    for y in range(SIZE):
        for x in range(SIZE):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            d = (dx * dx + dy * dy) ** 0.5
            if not (0.78 <= d <= 1.0):
                continue
            if only_below is not None and y < only_below:
                continue
            grid[y][x] = RING_LIGHT if x < cx else RING_DARK


def stamp(grid, art, key, ox, oy):
    for y, row in enumerate(art):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            gx, gy = ox + x, oy + y
            if 0 <= gx < SIZE and 0 <= gy < SIZE:
                grid[gy][gx] = key[ch]


def write_png(path, grid, scale):
    h = len(grid) * scale
    w = len(grid[0]) * scale
    raw = b""
    for row in grid:
        line = b"".join(bytes(p) * scale for p in row)
        raw += (b"\x00" + line) * scale

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


def main():
    grid = blank()
    for x, y, c in STARS:
        grid[y][x] = c

    px, py, pr = 19, 22, 8
    ring(grid, px, py, 13, 4)                 # the half behind the planet
    disc(grid, px, py, pr, PLANET_LIGHT, PLANET_MID, PLANET_DARK)
    ring(grid, px, py, 13, 4, only_below=py + 1)   # and the half in front

    disc(grid, 27, 5, 3, MOON_LIGHT, MOON_DARK, MOON_DARK)
    stamp(grid, ROCKET, ROCKET_KEY, 2, 3)

    write_png(OUT, grid, SCALE)
    write_png(PREVIEW, grid, 2)
    print("icon written to", OUT)


main()
