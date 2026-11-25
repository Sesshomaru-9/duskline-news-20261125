#!/usr/bin/env python3
"""Duskline News -- 25 November 2026.

Draws a one-page newspaper front page (1024x1024 PNG) summing up the
world news of Wednesday 25 November 2026, using only Pillow and the
standard library. No network, no randomness, no clock: two runs write
byte-identical output.

The program writes exactly one file, entry.png, into
$MAKEFUN_OUTPUT_DIR (or a fresh temp directory outside this repository
when the variable is unset). It never writes into its own repository:
if the output directory is the repository or inside it, it refuses
and exits 0. It never raises an exception.
"""

import os
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 227)      # warm newsprint cream
INK = (20, 18, 16)          # near-black ink
RED = (176, 32, 32)         # headline accent red
NAVY = (27, 58, 92)         # night-sky blue for the illustration
SKY_DARK = (16, 32, 56)
GOLD = (212, 160, 60)
GREY = (90, 84, 74)
RULE = (120, 110, 95)
TICKER_BG = (24, 24, 22)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font, falling back to Pillow's built-in bitmap font."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill=INK, spacing=4,
                 max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_rocket_scene(canvas, box):
    """Draw the lead illustration: a Long March rocket climbing through
    a starry night sky above the curve of the Earth. The scene is drawn
    on its own layer first, so nothing can spill past the frame."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    layer = Image.new("RGB", (bw, bh), SKY_DARK)
    draw = ImageDraw.Draw(layer)
    # stars: fixed positions, no randomness
    stars = [
        (0.08, 0.10, 2), (0.22, 0.06, 1), (0.35, 0.14, 2), (0.52, 0.05, 1),
        (0.68, 0.12, 2), (0.84, 0.07, 1), (0.93, 0.18, 2), (0.12, 0.28, 1),
        (0.44, 0.24, 1), (0.78, 0.30, 2), (0.60, 0.20, 1), (0.30, 0.34, 1),
        (0.90, 0.40, 1), (0.05, 0.48, 1), (0.70, 0.44, 1),
    ]
    for fx, fy, r in stars:
        cx, cy = fx * bw, fy * bh
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 230, 210))
    # crescent moon
    mx, my, mr = 0.82 * bw, 0.16 * bh, 26
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(240, 235, 205))
    draw.ellipse([mx - mr + 12, my - mr - 4, mx + mr + 12, my + mr - 4],
                 fill=SKY_DARK)
    # Earth curve at the bottom
    earth_y = bh - 34
    draw.ellipse([-190, earth_y, bw + 190, bh + 260], fill=(38, 92, 140))
    draw.ellipse([-150, earth_y + 26, bw + 150, bh + 260],
                 fill=(52, 120, 74))
    # clouds on the Earth curve
    for cx, cy, cw in [(0.18, 0.90, 46), (0.55, 0.94, 60), (0.82, 0.89, 40)]:
        px = cx * bw
        py = cy * bh
        draw.ellipse([px - cw // 2, py - 7, px + cw // 2, py + 7],
                     fill=(225, 232, 238))
    # rocket body (centre, nose up)
    cx = bw // 2
    nose_y = 52
    body_top, body_bot = nose_y + 34, 218
    body_w = 34
    # flame
    flame = [(cx - 12, body_bot), (cx + 12, body_bot),
             (cx + 5, body_bot + 44), (cx, body_bot + 62),
             (cx - 5, body_bot + 44)]
    draw.polygon(flame, fill=(255, 176, 32))
    draw.polygon([(cx - 7, body_bot), (cx + 7, body_bot),
                  (cx + 3, body_bot + 26), (cx, body_bot + 36),
                  (cx - 3, body_bot + 26)], fill=(255, 236, 170))
    # fins
    draw.polygon([(cx - body_w // 2, body_bot - 34), (cx - body_w // 2, body_bot),
                  (cx - body_w // 2 - 22, body_bot + 6)], fill=(200, 40, 40))
    draw.polygon([(cx + body_w // 2, body_bot - 34), (cx + body_w // 2, body_bot),
                  (cx + body_w // 2 + 22, body_bot + 6)], fill=(200, 40, 40))
    # body
    draw.rectangle([cx - body_w // 2, body_top, cx + body_w // 2, body_bot],
                   fill=(238, 236, 228), outline=INK, width=2)
    draw.polygon([(cx - body_w // 2, body_top), (cx + body_w // 2, body_top),
                  (cx, nose_y)], fill=(200, 40, 40), outline=INK)
    draw.rectangle([cx - body_w // 2, body_top + 58, cx + body_w // 2,
                    body_top + 78], fill=RED)
    # window
    draw.ellipse([cx - 8, body_top + 22, cx + 8, body_top + 38],
                 fill=(140, 200, 235), outline=INK, width=2)
    # exhaust smoke puffs
    for sx, sy, sr in [(0.30, 0.86, 14), (0.68, 0.88, 17), (0.50, 0.93, 12)]:
        px = sx * bw
        py = sy * bh
        draw.ellipse([px - sr, py - sr // 2, px + sr, py + sr // 2],
                     fill=(210, 208, 200))
    # caption bar inside the frame
    draw.rectangle([0, bh - 26, bw, bh], fill=(0, 0, 0))
    cap = "SHENZHOU-24 LIFTS OFF FROM JIUQUAN"
    draw.text((10, bh - 21), cap, font=SANS_B(10), fill=(240, 238, 228))
    canvas.paste(layer, (x0, y0))


LEAD_HEAD = "China launches Shenzhou-24 with first Pakistani astronaut aboard"
LEAD_BODY = (
    "A Long March 2F rocket lifted off from Jiuquan at 00:18 UTC, carrying "
    "commander Tang Hongbo, flight engineer Wu Yi and Pakistani payload "
    "specialist Muhammad Zeeshan Ali to the Tiangong space station. Ali, 40, "
    "is the first Pakistani in orbit and the first foreign astronaut ever to "
    "visit Tiangong, where he will run experiments for five to ten days."
)

STORIES = [
    ("GAZA",
     "Israeli strikes kill Hamas security chief; seven dead",
     "Naeem Abu Nahal, who headed Hamas's internal security service, was "
     "killed in Gaza City, medics said, as strikes across the strip left "
     "seven dead despite the ceasefire in place since October."),
    ("INDONESIA",
     "Factory fire toll reaches 26 as police open negligence inquiry",
     "Rescuers recovered 26 body bags from the burnt candy factory in "
     "Serang, Banten. Police questioned 19 witnesses and seized safety "
     "records after finding signs of negligence."),
    ("SPACE DEFENCE",
     "NATO vows to defend space as Russia is reported to ready a nuclear satellite",
     "The alliance pledged to answer threats beyond Earth after reports "
     "that Moscow is preparing a nuclear-armed satellite, possibly for "
     "launch as soon as December."),
    ("TRADE",
     "US set to slap tariffs on China and EU after excess-capacity probe",
     "Washington is preparing new duties on China, the EU and others after "
     "an investigation into excess industrial capacity, a report says."),
    ("TECHNOLOGY",
     "Microsoft declares 'Code Red' after historic outage",
     "Internal memos show the company raised its highest alert after a "
     "major outage, as Asian tech shares slid on weakening confidence in "
     "artificial intelligence."),
    ("CLIMATE",
     "Turkey climate summit ends with no final agreement",
     "More than 190 countries left the Antalya talks without a closing "
     "text, with no deal on fossil fuels as the world stays divided."),
]

TICKER = (
    "SHEIN TO PAY $100M TO SETTLE US SUITS  \u2022  HOSTAGES SEIZED IN CARTAGENA "
    "SUPERMARKET  \u2022  IOWA EVACUATIONS AS ARMY DESTROYS AGEING EXPLOSIVES  "
    "\u2022  SOORYAVANSHI, 15, SMASHES 204 OFF 53 BALLS  \u2022  GUKESH HOLDS "
    "SINDAROV IN WORLD CHESS TITLE MATCH  \u2022  SOUTH KOREA MINISTER RESIGNS  "
    "\u2022  NVIDIA REINSTATES HUANG"
)

FOOTER = (
    "Sources: Reuters  •  Xinhua  •  Associated Press  •  The Hindu  •  NOS  •  "
    "Daily Debrief briefing of 25 November 2026  •  Duskline News sums up the "
    "world news of Wednesday 25 November 2026."
)


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # page margin

    # ---- masthead ----
    d.text((m, 18), "DUSKLINE NEWS", font=SERIF_B(62), fill=INK)
    rule(d, m, 96, W - m, width=3, fill=INK)
    rule(d, m, 102, W - m, width=1, fill=INK)
    d.text((m, 110), "WEDNESDAY, 25 NOVEMBER 2026", font=SANS_B(17), fill=RED)
    right = "THE WORLD IN ONE PAGE  •  No. 329"
    d.text((W - m - d.textlength(right, font=SANS_B(13)), 113), right,
           font=SANS_B(13), fill=GREY)

    # ---- lead story ----
    ly = 146
    d.text((m, ly), "SPACE  •  LEAD STORY", font=SANS_B(14), fill=RED)
    y = draw_wrapped(d, m, ly + 26, LEAD_HEAD, SERIF_B(30), 560,
                     max_lines=3, spacing=2)
    y = draw_wrapped(d, m, y + 8, LEAD_BODY, SERIF(15), 560, spacing=3,
                     max_lines=8)
    # illustration, right of the lead text
    ix0, iy0, ix1, iy1 = 632, ly, W - m, 452
    draw_rocket_scene(img, (ix0, iy0, ix1, iy1))
    d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=2)

    rule(d, m, 470, W - m, width=2, fill=INK)

    # ---- story grid: 2 columns x 3 rows ----
    col_w = (W - 2 * m - 28) // 2
    row_h = 128
    gy = 490
    for i, (kicker, head, body) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = m + col * (col_w + 28)
        y = gy + row * row_h
        d.text((x, y), kicker, font=SANS_B(12), fill=RED)
        y2 = draw_wrapped(d, x, y + 20, head, SERIF_B(17), col_w,
                          max_lines=2, spacing=1)
        draw_wrapped(d, x, y2 + 4, body, SERIF(12), col_w, spacing=2,
                     max_lines=3)
        if col == 0:
            d.line([(x + col_w + 14, y), (x + col_w + 14, y + row_h - 16)],
                   fill=RULE, width=1)
        if row < 2:
            rule(d, x, y + row_h - 8, x + col_w, width=1, fill=RULE)

    # ---- ticker ----
    ty = 878
    d.rectangle([0, ty, W, ty + 62], fill=TICKER_BG)
    d.text((m, ty + 8), "WIRE", font=SANS_B(15), fill=GOLD)
    lines = wrap(d, TICKER, SANS_B(12), W - 2 * m - 62)
    ty_text = ty + 8
    for line in lines[:3]:
        d.text((m + 62, ty_text), line, font=SANS_B(12),
               fill=(238, 236, 228))
        ty_text += 17

    # ---- footer ----
    fy = 952
    rule(d, m, fy, W - m, width=1, fill=RULE)
    draw_wrapped(d, m, fy + 10, FOOTER, SANS(11), W - 2 * m, fill=GREY,
                 spacing=2, max_lines=3)
    return img


def resolve_output_dir():
    """Return the directory to write entry.png into, or None to refuse."""
    repo = Path(__file__).resolve().parent
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if raw:
        out = Path(raw).expanduser()
        try:
            out_resolved = out.resolve()
        except Exception:
            out_resolved = out.absolute()
    else:
        out_resolved = Path(tempfile.mkdtemp(prefix="duskline-news-"))
    try:
        repo_resolved = repo.resolve()
    except Exception:
        repo_resolved = repo.absolute()
    if out_resolved == repo_resolved or repo_resolved in out_resolved.parents:
        return None
    return out_resolved


def main():
    try:
        out_dir = resolve_output_dir()
        if out_dir is None:
            print("refusing: MAKEFUN_OUTPUT_DIR is the repository or "
                  "inside it; nothing written")
            return 0
        out_dir.mkdir(parents=True, exist_ok=True)
        img = build_image()
        target = out_dir / "entry.png"
        img.save(str(target), "PNG")
        print("wrote %s (%dx%d)" % (target, W, H))
        return 0
    except Exception as exc:  # never raise, never crash the harness
        print("error: %s" % (exc,))
        return 0


if __name__ == "__main__":
    sys.exit(main())
