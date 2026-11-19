#!/usr/bin/env python3
"""Deterministic PIL builder for the gta6-meme-x-01 meme.

Concepts brainstormed in-session:
  A) "The Long Wait"  - the make.fun ghost has waited 13 years for GTA 6
     (calendars 2013 -> 2026, bench under a Leonida sunset, controller
     in hand); punchline: his AI agent got paid on make.fun while he
     waited.
  B) "Launch Price"   - GTA 6 costs $79.99, the ghost's wallet is empty,
     but his AI agent earns real money on make.fun, star coin in hand.
  C) "Sick Day"       - the ghost files a launch-day sick note for all of
     Leonida; his agent covers his shift by earning on make.fun.
     (Not rendered: the sick-note prop reads poorly at 480px wide.)

A and B are rendered; A is copied to meme.png as the winner (see bottom).
The ghost is the official press-kit mark, placed centre-scene as the
character itself (its magenta disc doubling as the Leonida sunset sun),
sitting on a bench with a controller, not pasted as a corner sticker.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRESSKIT = os.path.join(HERE, "..", "presskit")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W = H = 1024
BLACK = (10, 10, 14)
WHITE = (255, 255, 255)
MAGENTA = (214, 31, 132)
GOLD = (255, 196, 0)


def font(size):
    return ImageFont.truetype(FONT, size)


def ghost_character(size):
    """Official mark, cropped to its disc.

    The mark's magenta disc doubles as the big Leonida sunset sun the
    ghost is sitting in front of, so the character (sparkle eyes and
    magenta star coin included) stays instantly recognisable at 480px.
    """
    im = Image.open(os.path.join(PRESSKIT, "mark-1024.png")).convert("RGBA")
    im = im.crop(im.getbbox())
    im.thumbnail((size, size), Image.LANCZOS)
    return im


def caption_bar(draw, y0, y1, lines):
    draw.rectangle([0, y0, W, y1], fill=BLACK)
    total = sum(size for _, size, _ in lines)
    gap = 10 * (len(lines) - 1)
    y = y0 + ((y1 - y0) - (total + gap)) // 2
    for text, size, colour in lines:
        f = font(size)
        box = draw.textbbox((0, 0), text, font=f)
        tw = box[2] - box[0]
        draw.text(((W - tw) // 2 - box[0], y - box[1]), text, font=f, fill=colour)
        y += size + gap


def sunset(y0, y1):
    img = Image.new("RGB", (W, y1 - y0))
    d = ImageDraw.Draw(img)
    top = (46, 16, 101)      # deep Vice City purple
    mid = (214, 31, 132)     # magenta
    low = (255, 140, 66)     # sunset orange
    h = y1 - y0
    for i in range(h):
        t = i / h
        if t < 0.5:
            a, b, k = top, mid, t * 2
        else:
            a, b, k = mid, low, (t - 0.5) * 2
        d.line([(0, i), (W, i)], fill=tuple(int(a[j] + (b[j] - a[j]) * k) for j in range(3)))
    return img


def palm(draw, x, y, s, colour=(24, 10, 40)):
    """Simple Leonida palm: curved trunk plus drooping frond polylines."""
    cx, cy = x + 26 * s, y - 168 * s          # crown point
    draw.line([x, y, x + 10 * s, y - 84 * s, cx, cy], fill=colour, width=int(15 * s), joint="curve")
    for dx, lift, drop in ((-120, 52, 44), (-78, 78, 18), (-26, 92, 6), (34, 88, 10), (88, 70, 26), (128, 44, 52)):
        mx, my = cx + dx * 0.55 * s, cy - lift * s
        ex, ey = cx + dx * s, cy - lift * s + drop * s
        draw.line([cx, cy, mx, my, ex, ey], fill=colour, width=int(10 * s), joint="curve")


def calendar(draw, x, y, w, year, crossed):
    draw.rounded_rectangle([x, y, x + w, y + w * 1.08], 14, fill=WHITE, outline=BLACK, width=6)
    draw.rectangle([x, y, x + w, y + w * 0.30], fill=(200, 30, 45))
    f = font(int(w * 0.26))
    box = draw.textbbox((0, 0), year, font=f)
    draw.text((x + (w - (box[2] - box[0])) // 2 - box[0], y + w * 0.02), year, font=f, fill=WHITE)
    for r in range(3):
        for c in range(4):
            cx, cy = x + w * (0.16 + 0.23 * c), y + w * (0.48 + 0.19 * r)
            draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(120, 120, 130))
    if crossed:
        draw.line([x + 8, y + 8, x + w - 8, y + w * 1.08 - 8], fill=(200, 30, 45), width=12)
        draw.line([x + w - 8, y + 8, x + 8, y + w * 1.08 - 8], fill=(200, 30, 45), width=12)


def build_a():
    img = Image.new("RGB", (W, H), BLACK)
    img.paste(sunset(170, 850), (0, 170))
    d = ImageDraw.Draw(img, "RGBA")
    # Leonida palms + floor
    palm(d, 26, 850, 1.0)
    palm(d, 872, 850, 1.0)
    d.rectangle([0, 790, W, 850], fill=(24, 10, 40))
    # Calendars: GTA V's 2013 on the left, GTA 6's 2026 on the right
    calendar(d, 36, 205, 190, "2013", False)
    calendar(d, 798, 205, 190, "2026", False)
    d.polygon([(250, 285), (330, 285), (330, 262), (372, 302), (330, 342), (330, 319), (250, 319)], fill=GOLD, outline=BLACK)
    # Bench
    d.rounded_rectangle([212, 700, 812, 745], 12, fill=(70, 38, 20), outline=BLACK, width=5)
    d.rectangle([232, 745, 262, 800], fill=(40, 22, 12))
    d.rectangle([762, 745, 792, 800], fill=(40, 22, 12))
    # Ghost character, big and central, sitting on the bench
    g = ghost_character(470)
    img.paste(g, ((W - g.width) // 2, 268), g)
    d = ImageDraw.Draw(img, "RGBA")
    # NOTE: a beard, then a moustache, were both tried as age props and
    # both read as clutter (bowl / grey band) at 480px, so the ghost
    # stays clean: the 2013 -> 2026 calendars carry the 13-year joke.
    # Controller in front of the ghost
    d.rounded_rectangle([402, 668, 622, 742], 34, fill=(20, 20, 26), outline=WHITE, width=5)
    d.ellipse([432, 692, 462, 722], fill=MAGENTA)
    d.ellipse([552, 692, 582, 722], fill=GOLD)
    caption_bar(d, 0, 170, [("WAITED 13 YEARS", 76, WHITE), ("FOR GTA 6", 76, WHITE)])
    caption_bar(d, 850, 1024, [("MY AI AGENT GOT PAID ON", 58, WHITE), ("make.fun WHILE I WAITED", 58, MAGENTA)])
    return img


def build_b():
    img = Image.new("RGB", (W, H), BLACK)
    img.paste(sunset(170, 850), (0, 170))
    d = ImageDraw.Draw(img, "RGBA")
    palm(d, 26, 850, 1.0)
    palm(d, 872, 850, 1.0)
    d.rectangle([0, 790, W, 850], fill=(24, 10, 40))
    # Price tag for the game
    d.rounded_rectangle([560, 230, 970, 432], 18, fill=GOLD, outline=BLACK, width=7)
    f = font(64); d.text((592, 252), "GTA 6", font=f, fill=BLACK)
    f = font(76); d.text((592, 330), "$79.99", font=f, fill=BLACK)
    # Empty wallet in front of the ghost
    g = ghost_character(430)
    img.paste(g, (60, 330), g)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([330, 640, 606, 740], 16, fill=(110, 66, 30), outline=BLACK, width=6)
    f = font(40); d.text((350, 670), "WALLET: $0", font=f, fill=WHITE)
    caption_bar(d, 0, 170, [("GTA 6 COSTS $79.99", 72, WHITE), ("MY WALLET: EMPTY", 72, WHITE)])
    caption_bar(d, 850, 1024, [("MY AI AGENT EARNS REAL $ ON", 54, WHITE), ("make.fun - PROBLEM SOLVED", 54, MAGENTA)])
    return img


if __name__ == "__main__":
    a = build_a(); a.save(os.path.join(HERE, "concept-a.png"))
    b = build_b(); b.save(os.path.join(HERE, "concept-b.png"))
    a.save(os.path.join(HERE, "meme.png"))
    print("built concept-a.png, concept-b.png, meme.png (= A)")
