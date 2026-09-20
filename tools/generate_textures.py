#!/usr/bin/env python3
"""Draws every texture the Planets mod needs, as 16x16 PNGs."""
import os, struct, zlib, random

ROOT = "/Users/elduinnunn/GitHub/planets-mod/src/main/resources/assets/planets/textures"

def write_png(path, px):
    """px: list of 16 rows, each 16 (r,g,b,a) tuples."""
    h = len(px); w = len(px[0])
    raw = b"".join(b"\x00" + b"".join(bytes(p) for p in row) for row in px)
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

def hx(s):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)

def shade(c, d):
    return (max(0, min(255, c[0] + d)), max(0, min(255, c[1] + d)), max(0, min(255, c[2] + d)), c[3])

NONE = (0, 0, 0, 0)

# ---------------------------------------------------------------- block stone
def stone_tex(base, seed, rough=18, speck=None, speck_n=0):
    rnd = random.Random(seed)
    b = hx(base)
    px = [[shade(b, rnd.randint(-rough, rough)) for _ in range(16)] for _ in range(16)]
    # a few darker pits so it does not read as flat noise
    for _ in range(10):
        x, y = rnd.randrange(16), rnd.randrange(16)
        px[y][x] = shade(b, -rough - 14)
    for _ in range(8):
        x, y = rnd.randrange(16), rnd.randrange(16)
        px[y][x] = shade(b, rough + 12)
    if speck:
        s = hx(speck)
        for _ in range(speck_n):
            x, y = rnd.randrange(16), rnd.randrange(16)
            px[y][x] = shade(s, rnd.randint(-10, 10))
    return px

def dust_tex(base, seed):
    """Softer, finer grain — reads as dust/sand/snow."""
    rnd = random.Random(seed)
    b = hx(base)
    px = [[shade(b, rnd.randint(-9, 9)) for _ in range(16)] for _ in range(16)]
    for _ in range(14):
        x, y = rnd.randrange(16), rnd.randrange(16)
        px[y][x] = shade(b, -16)
    return px

# craters for the moon: a few ring shapes
def crater_tex(base, seed):
    rnd = random.Random(seed)
    b = hx(base)
    px = [[shade(b, rnd.randint(-8, 8)) for _ in range(16)] for _ in range(16)]
    for _ in range(3):
        cx, cy, r = rnd.randrange(3, 13), rnd.randrange(3, 13), rnd.choice([2, 2, 3])
        for y in range(16):
            for x in range(16):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if r - 0.7 <= d <= r + 0.4:
                    px[y][x] = shade(b, -26)
                elif d < r - 0.7:
                    px[y][x] = shade(b, 10)
    return px

# ---------------------------------------------------------------- ore overlay
ORE_BLOBS = [
    (3, 3), (4, 3), (3, 4),
    (10, 5), (11, 5), (11, 6), (10, 6),
    (6, 9), (7, 9), (6, 10),
    (12, 11), (13, 11),
    (4, 12), (5, 12), (4, 13),
]

def ore_tex(stone_px, gem, seed):
    rnd = random.Random(seed)
    g = hx(gem)
    px = [row[:] for row in stone_px]
    for (x, y) in ORE_BLOBS:
        px[y][x] = shade(g, rnd.randint(-8, 14))
        # soft dark edge below-right so the blob has depth
        if y + 1 < 16:
            px[y + 1][x] = shade(g, -46)
    return px

# ---------------------------------------------------------------- pixel art
def from_map(rows, key):
    px = []
    for r in rows:
        row = []
        for ch in r:
            row.append(NONE if ch == "." else hx(key[ch]))
        px.append(row)
    return px

GEM = [
    "................",
    "................",
    ".......AA.......",
    "......ABBA......",
    ".....ABBBBA.....",
    "....ABBCCBBA....",
    "...ABBCCCCBBA...",
    "...ABBCCCCBBA...",
    "...ABBBCCBBBA...",
    "....ABBBBBBA....",
    ".....ABBBBA.....",
    "......ABBA......",
    ".......AA.......",
    "................",
    "................",
    "................",
]

SHARD = [
    "................",
    "..........A.....",
    ".........ABA....",
    "........ABBA....",
    ".......ABBCA....",
    "......ABBCCA....",
    ".....ABBCCA.....",
    ".....ABBCA......",
    "....ABBCA.......",
    "....ABCA........",
    "...ABCA.........",
    "...ABA..........",
    "..ABA...........",
    "..AA............",
    "................",
    "................",
]

LUMP = [
    "................",
    "................",
    "................",
    "......AAA.......",
    ".....ABBBA......",
    "....ABBCBBA.....",
    "...ABBCCCBBA....",
    "...ABCCCCCBA....",
    "..ABBCCCCCBBA...",
    "..ABBCCCCBBBA...",
    "...ABBBBBBBA....",
    "....ABBBBBA.....",
    ".....AAAAA......",
    "................",
    "................",
    "................",
]

TANK = [
    "................",
    "......DDD.......",
    ".....DEEED......",
    "......DDD.......",
    "......CCC.......",
    ".....ABBBA......",
    "....ABBBBBA.....",
    "....ABBCBBA.....",
    "....ABBCBBA.....",
    "....ABBCBBA.....",
    "....ABBBBBA.....",
    "....ABBBBBA.....",
    "....ABBBBBA.....",
    "....ABBBBBA.....",
    ".....AAAAA......",
    "................",
]

ROCKET_ITEM = [
    "................",
    ".......AA.......",
    "......ABBA......",
    "......ABBA......",
    ".....ABBBBA.....",
    ".....ACCCCA.....",
    ".....ACCCCA.....",
    "....AACCCCAA....",
    "...ABACCCCABA...",
    "...ABBACCABBA...",
    "...ABBAACCABBA..",
    "...ABBA.ABBA....",
    "....AA...AA.....",
    "......DD........",
    ".....DEED.......",
    "......DD........",
]

# ---------------------------------------------------------------- write it all
def main():
    b = os.path.join(ROOT, "block")
    i = os.path.join(ROOT, "item")

    planets = {
        "moon":  dict(rock="#8d8d8d", soil="#c6c2b8", gem="#dff6ff",
                      ore="moonstone_ore", item="moonstone", art=GEM,
                      gk={"A": "#3c4a52", "B": "#9fd6ea", "C": "#eafbff"}),
        "mars":  dict(rock="#7e3b24", soil="#b5603a", gem="#ff5fd0",
                      ore="mars_crystal_ore", item="mars_crystal", art=SHARD,
                      gk={"A": "#4a1038", "B": "#e04ab4", "C": "#ffc2f0"}),
        "venus": dict(rock="#5f4c23", soil="#d4b13c", gem="#ffe94a",
                      ore="sulfur_ore", item="sulfur", art=LUMP,
                      gk={"A": "#6b5107", "B": "#e8c52b", "C": "#fff07a"}),
        "pluto": dict(rock="#a8dcec", soil="#edf7fb", gem="#2a5bd7",
                      ore="frost_ore", item="frost_shard", art=SHARD,
                      gk={"A": "#10245e", "B": "#3f74e8", "C": "#a9c8ff"}),
    }

    # moon is craters, the rest are ordinary rock
    write_png(os.path.join(b, "moon_rock.png"), crater_tex(planets["moon"]["rock"], 11))
    write_png(os.path.join(b, "moon_dust.png"), dust_tex(planets["moon"]["soil"], 12))

    write_png(os.path.join(b, "mars_rock.png"), stone_tex(planets["mars"]["rock"], 21))
    write_png(os.path.join(b, "mars_sand.png"), dust_tex(planets["mars"]["soil"], 22))

    write_png(os.path.join(b, "venus_rock.png"), stone_tex(planets["venus"]["rock"], 31, speck="#8a6a10", speck_n=10))
    write_png(os.path.join(b, "venus_ash.png"), dust_tex(planets["venus"]["soil"], 32))

    write_png(os.path.join(b, "pluto_ice.png"), stone_tex(planets["pluto"]["rock"], 41, rough=11))
    write_png(os.path.join(b, "pluto_snow.png"), dust_tex(planets["pluto"]["soil"], 42))

    # ores sit in their own planet's rock
    hosts = {
        "moon": crater_tex(planets["moon"]["rock"], 11),
        "mars": stone_tex(planets["mars"]["rock"], 21),
        "venus": stone_tex(planets["venus"]["rock"], 31, speck="#8a6a10", speck_n=10),
        "pluto": stone_tex(planets["pluto"]["rock"], 41, rough=11),
    }
    for n, p in planets.items():
        write_png(os.path.join(b, p["ore"] + ".png"), ore_tex(hosts[n], p["gem"], hash(n) & 0xFFFF))
        write_png(os.path.join(i, p["item"] + ".png"), from_map(p["art"], p["gk"]))

    # rocket block skin
    rnd = random.Random(7)
    body = [[shade(hx("#e6e9ee"), rnd.randint(-6, 6)) for _ in range(16)] for _ in range(16)]
    for y in range(16):
        body[y][0] = shade(hx("#9aa3ad"), 0)
        body[y][15] = shade(hx("#9aa3ad"), 0)
    for x in range(16):
        body[6][x] = hx("#d8232a")
        body[7][x] = hx("#b81c22")
    for (x, y) in [(3, 2), (12, 2), (3, 12), (12, 12)]:
        body[y][x] = hx("#7d868f")
    write_png(os.path.join(b, "rocket.png"), body)

    nose = [[hx("#d8232a") for _ in range(16)] for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if (x + y) % 7 == 0:
                nose[y][x] = hx("#ef4a50")
            if x == 0 or x == 15:
                nose[y][x] = hx("#9c1218")
    write_png(os.path.join(b, "rocket_nose.png"), nose)

    write_png(os.path.join(i, "oxygen_tank.png"),
              from_map(TANK, {"A": "#2b3a45", "B": "#4fb6d8", "C": "#bff0ff",
                              "D": "#6a7580", "E": "#c9d2da"}))
    write_png(os.path.join(i, "rocket_part.png"),
              from_map(ROCKET_ITEM, {"A": "#8b949e", "B": "#e6e9ee", "C": "#d8232a",
                                     "D": "#ff8a1f", "E": "#ffd84a"}))
    print("textures written")

main()
