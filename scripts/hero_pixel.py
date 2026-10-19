"""Render the original, four-scene pixel-art profile banner.

Run with Pillow: python scripts/hero_pixel.py
No game sprites, screenshots, or third-party artwork are used.
"""

from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
W, H, SCALE = 320, 96, 4
FRAMES_PER_SCENE = 17

INK = (7, 15, 31)
WHITE = (233, 245, 241)
MUTED = (127, 160, 168)
TEAL = (57, 208, 184)
GOLD = (242, 192, 103)
BLUE = (91, 157, 236)
MINT = (112, 226, 160)

SCENES = [
    ("CODE", "BUILD THE SYSTEM", TEAL),
    ("BUSINESS", "MODEL THE OPERATION", GOLD),
    ("BANKING + RISK", "DESIGN THE CONTROLS", BLUE),
    ("PRIVATE EQUITY", "INTEREST: VALUE + DILIGENCE", MINT),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "consolab.ttf" if bold else "consola.ttf"
    candidates = [Path("C:/Windows/Fonts") / name,
                  Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F7 = font(7, True)
F8 = font(8, True)
F10 = font(10, True)
F17 = font(17, True)


def rect(d, box, fill, outline=None, width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)


def line(d, xy, fill, width=1):
    d.line(xy, fill=fill, width=width)


def skyline(d, scene: int, tick: int):
    for y in range(0, 82):
        k = y / 82
        shade = (7 + int(k * 5), 15 + int(k * 10), 31 + int(k * 14))
        line(d, (0, y, 319, y), shade)
    for i, (x, top, width) in enumerate([(169, 43, 13), (183, 34, 16), (204, 48, 10),
                                         (218, 27, 18), (241, 41, 12), (256, 22, 15),
                                         (277, 35, 14), (296, 28, 17)]):
        rect(d, (x, top, x + width, 82), (13, 30, 47) if i % 2 else (11, 27, 45))
        for yy in range(top + 7, 78, 8):
            for xx in range(x + 3, x + width - 1, 6):
                if (xx + yy + i + scene) % 4:
                    rect(d, (xx, yy, xx + 1, yy + 2), (36, 78, 86))
    for i in range(20):
        x = 166 + (i * 37) % 149
        y = 5 + (i * 29) % 37
        color = (66, 131, 140) if (i + tick // 4) % 5 else GOLD
        d.point((x, y), fill=color)
    line(d, (0, 81, 319, 81), (47, 82, 91), 2)
    rect(d, (0, 83, 319, 95), (19, 43, 50))
    for x in range(0, 321, 16):
        line(d, (x, 84, x, 95), (26, 58, 61))
        line(d, (x, 89, x + 15, 89), (26, 58, 61))
        if x % 32 == 0:
            rect(d, (x + 3, 86, x + 5, 87), (50, 105, 100))


def code_lab(d, tick: int):
    # Server stack, terminal and bright program-flow links.
    rect(d, (211, 44, 227, 80), (29, 51, 66), (71, 117, 128))
    for y in (49, 59, 69):
        rect(d, (214, y, 224, y + 6), (9, 27, 39), (38, 105, 109))
        d.point((216, y + 3), fill=TEAL if tick % 4 < 2 else GOLD)
        line(d, (219, y + 3, 222, y + 3), (67, 113, 120))
    rect(d, (235, 35, 304, 73), (42, 84, 92), (91, 151, 151), 2)
    rect(d, (238, 38, 301, 70), (7, 22, 35))
    for j, y in enumerate((43, 48, 53, 58, 63)):
        color = [TEAL, BLUE, GOLD][j % 3]
        line(d, (244 + (j % 2) * 4, y, 266 + j * 3, y), color, 1)
        line(d, (269 + j, y, 278 + j * 3, y), (45, 93, 102), 1)
    rect(d, (261, 74, 278, 76), (74, 120, 122))
    line(d, (270, 72, 270, 74), (74, 120, 122))
    rect(d, (239, 78, 307, 81), (48, 73, 78))
    rect(d, (275, 76, 292, 78), (19, 49, 53))
    # Cursor and little terminal-status sparkle.
    if tick % 4 < 2:
        rect(d, (280, 63, 282, 65), TEAL)


def business_floor(d, tick: int):
    # Fulfilment shelves, live-business inventory and forecasting display.
    rect(d, (217, 32, 241, 81), (61, 69, 63), (114, 121, 101))
    for y in (42, 59, 76):
        line(d, (219, y, 239, y), GOLD, 2)
    for x, y in ((221, 36), (231, 36), (220, 49), (229, 51), (221, 66), (232, 65)):
        rect(d, (x, y, x + 7, y + 6), (139, 99, 58), (196, 150, 83))
        line(d, (x + 3, y, x + 3, y + 6), (98, 75, 55))
    rect(d, (250, 34, 307, 73), (40, 78, 81), (101, 151, 143), 2)
    rect(d, (253, 37, 304, 70), (8, 27, 37))
    vals = (8, 13, 11, 18, 20, 25)
    for i, h in enumerate(vals):
        x = 258 + i * 7
        rect(d, (x, 65 - h, x + 3, 65), TEAL if i < 4 else GOLD)
    line(d, (257, 65, 300, 65), (66, 106, 104))
    rect(d, (245, 78, 309, 81), (64, 82, 77))
    rect(d, (286 + tick % 3, 73, 292 + tick % 3, 77), (159, 115, 67))


def banking_hall(d, tick: int):
    # Risk decision network in front of a stylized bank facade.
    rect(d, (228, 35, 307, 80), (31, 53, 72), (80, 121, 151))
    d.polygon([(226, 35), (267, 22), (309, 35)], fill=(48, 75, 95), outline=(105, 147, 171))
    for x in (236, 255, 274, 293):
        rect(d, (x, 38, x + 7, 76), (81, 112, 127), (135, 160, 166))
        rect(d, (x - 2, 36, x + 9, 39), (99, 131, 142))
    rect(d, (224, 76, 311, 81), (87, 121, 136))
    rect(d, (244, 46, 288, 69), (8, 29, 43), (70, 125, 146))
    # Three explicit decision branches, inspired by the user's risk engine.
    for i, color in enumerate((MINT, GOLD, (242, 107, 105))):
        y = 52 + i * 6
        line(d, (250, y, 272, y), color)
        rect(d, (275, y - 2, 282, y + 2), color if (tick + i) % 4 < 2 else (36, 74, 90))
    for x, y in ((212, 41), (217, 49), (215, 60)):
        line(d, (x, y, 241, 57), (59, 123, 151))
        rect(d, (x - 1, y - 1, x + 1, y + 1), BLUE)


def investing_room(d, tick: int):
    # Due diligence board, operating-company cards and value bridge.
    rect(d, (218, 31, 307, 76), (48, 69, 76), (112, 150, 151), 2)
    rect(d, (221, 34, 304, 73), (9, 28, 39))
    for i, x in enumerate((226, 250, 274)):
        rect(d, (x, 40, x + 18, 58), (24, 57, 65), (71, 130, 127))
        for bx, hh in ((x + 4, 6), (x + 9, 9), (x + 14, 5 + (i % 2) * 4)):
            rect(d, (bx, 55 - hh, bx + 2, 55), MINT if i != 1 else GOLD)
        line(d, (x + 2, 62, x + 15, 62), (65, 115, 116))
        line(d, (x + 2, 65, x + 11, 65), (49, 87, 93))
    line(d, (227, 69, 238, 69, 251, 65, 265, 64, 278, 57, 296, 47), GOLD, 2)
    d.polygon([(296, 47), (290, 47), (296, 42)], fill=GOLD)
    rect(d, (229, 77, 304, 81), (63, 91, 87))
    d.ellipse((303 - tick % 3, 34, 306 - tick % 3, 37), fill=MINT)


DETAIL = [code_lab, business_floor, banking_hall, investing_room]


def sprite(d, scene: int, tick: int):
    x = min(184 + tick * 2, 204)
    walk = tick < 12
    bob = (tick % 4 == 1) if walk else (tick % 7 == 0)
    y = 61 - int(bob)
    # Shadow, legs, jacket, head and expressive task-specific hand motion.
    d.ellipse((x - 2, 80, x + 12, 83), fill=(5, 19, 25))
    leg = 2 if walk and tick % 2 else -1
    line(d, (x + 2, y + 13, x + 2 + leg, 81), (50, 105, 125), 2)
    line(d, (x + 7, y + 13, x + 7 - leg, 81), (50, 105, 125), 2)
    rect(d, (x + 1, y + 6, x + 9, y + 14), (42, 133, 139), (101, 213, 193))
    line(d, (x + 2, y + 8, x - 1, y + 12), (210, 157, 112), 2)
    hand_y = y + (8 if tick % 4 < 2 else 10)
    line(d, (x + 9, y + 8, x + 13, hand_y), (210, 157, 112), 2)
    rect(d, (x + 2, y - 1, x + 9, y + 6), (206, 154, 109), (73, 51, 46))
    rect(d, (x + 1, y - 3, x + 9, y), (34, 38, 51))
    rect(d, (x + 8, y + 2, x + 9, y + 2), (13, 27, 34))
    # Prop changes with the level: laptop glow, clipboard, risk tile, model sheet.
    if scene == 0:
        rect(d, (x + 12, y + 10, x + 18, y + 13), TEAL)
    elif scene == 1:
        rect(d, (x + 11, y + 8, x + 16, y + 14), (173, 143, 91), GOLD)
    elif scene == 2:
        rect(d, (x + 11, y + 8, x + 17, y + 14), BLUE)
        line(d, (x + 13, y + 11, x + 15, y + 11), WHITE)
    else:
        rect(d, (x + 11, y + 9, x + 17, y + 14), WHITE)
        line(d, (x + 12, y + 12, x + 16, y + 12), MINT)


def hud(d, scene: int, tick: int):
    label, subtitle, accent = SCENES[scene]
    # Opaque left panel guarantees readable type across all levels.
    rect(d, (0, 0, 163, 81), INK)
    for x in range(163, 180):
        shade = max(0, 25 - (x - 163) * 2)
        line(d, (x, 0, x, 80), (7, 15 + shade // 4, 31 + shade // 3))
    rect(d, (13, 10, 17, 13), accent)
    d.text((22, 8), "PLAYER / JME", font=F7, fill=MUTED)
    d.text((12, 20), "JOHN MARWIN", font=F17, fill=WHITE)
    d.text((12, 36), "EBONA", font=F17, fill=WHITE)
    line(d, (13, 56, 149, 56), (51, 85, 94))
    d.text((13, 60), label, font=F10, fill=accent)
    d.text((13, 73), subtitle, font=F7, fill=WHITE)
    # Level indicator and tiny loading rail give it a game UI language.
    rect(d, (270, 8, 308, 21), (12, 32, 45), (63, 105, 113))
    d.text((276, 9), f"0{scene + 1}/04", font=F8, fill=WHITE)
    for i in range(4):
        rect(d, (266 + i * 10, 26, 272 + i * 10, 28), accent if i == scene else (45, 75, 82))
    if tick < 12:
        for i in range(3):
            x = 167 + ((tick * 3 - i * 5) % 32)
            d.point((x, 77 - i * 2), fill=(65, 129, 134))


def scene_frame(scene: int, tick: int) -> Image.Image:
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    skyline(d, scene, tick)
    DETAIL[scene](d, tick)
    sprite(d, scene, tick)
    hud(d, scene, tick)
    return img


def main():
    OUT.mkdir(exist_ok=True)
    frames = []
    for scene in range(4):
        for tick in range(FRAMES_PER_SCENE):
            current = scene_frame(scene, tick)
            if tick >= FRAMES_PER_SCENE - 3:
                next_frame = scene_frame((scene + 1) % 4, 0)
                # Crisp tile-column wipe, preserving the pixel-art edges.
                coverage = (tick - (FRAMES_PER_SCENE - 4)) / 4
                cut = int(W * (1 - coverage))
                current.paste(next_frame.crop((cut, 0, W, H)), (cut, 0))
            frames.append(current)

    # A shared palette prevents color shifts between animated frames.
    palette_source = Image.new("RGB", (W * 4, H))
    for i in range(4):
        palette_source.paste(scene_frame(i, 12), (W * i, 0))
    palette = palette_source.quantize(colors=128, method=Image.Quantize.FASTOCTREE,
                                      dither=Image.Dither.NONE)
    hires = [f.quantize(palette=palette, dither=Image.Dither.NONE).resize(
        (W * SCALE, H * SCALE), Image.Resampling.NEAREST) for f in frames]
    hires[0].convert("RGB").save(OUT / "hero-pixel.png", optimize=True)
    hires[0].save(OUT / "hero-pixel.gif", save_all=True, append_images=hires[1:],
                  duration=105, loop=0, optimize=True, disposal=2)
    print(f"Created {OUT / 'hero-pixel.gif'} ({len(hires)} frames)")


if __name__ == "__main__":
    main()
