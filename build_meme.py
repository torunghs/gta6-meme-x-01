#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme (1920x1280 PNG) with Python PIL.

Inputs (paths are fixed by the brief; the base image and the official
make.fun ghost mark are used as-is, never redrawn):
  BASE  = ~/workspace/makefun/media-generation-gta6-meme-base-0-56b4a840-539b-45d0-a6d1-efe60eee4d30.png
  GHOST = ~/workspace/makefun/makefun-mark-1024.png (official mark, RGBA 1024x1024)
Output:
  meme.png in this repo + ~/workspace/makefun/gta6-meme-x-01-meme.png

Layout (1920x1280):
  - Top caption, two lines, DejaVu Sans Bold, white with thick black outline,
    over a subtle top gradient so it reads over the bright sky:
        CALLED IN SICK FOR
        GTA 6 LAUNCH DAY
  - Official ghost mark, 480 px tall, standing centre-right on the road
    (centre x=1200, bottom y=1060) with a soft shadow beneath it.
  - Small "make.fun" label under the ghost.
  - Bottom caption, DejaVu Sans Bold, white with black outline, over a
    subtle bottom gradient:
        BOSS: "WE CAN SEE YOU ONLINE"
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HOME = os.path.expanduser("~")
BASE = os.path.join(
    HOME,
    "workspace/makefun/media-generation-gta6-meme-base-0-56b4a840-539b-45d0-a6d1-efe60eee4d30.png",
)
GHOST = os.path.join(HOME, "workspace/makefun/makefun-mark-1024.png")
OUT_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")
OUT_COPY = os.path.join(HOME, "workspace/makefun/gta6-meme-x-01-meme.png")

W, H = 1920, 1280
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD, size)


def outlined_text(draw: ImageDraw.ImageDraw, cx: int, y: int,
                  text: str, fnt: ImageFont.FreeTypeFont,
                  fill=(255, 255, 255), outline=(0, 0, 0),
                  stroke: int = 8) -> int:
    """Draw centred text with a thick outline; return text height."""
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], y - bbox[1]), text, font=fnt,
              fill=fill, stroke_width=stroke, stroke_fill=outline)
    return th


def vertical_gradient(size, top_alpha: int, bottom_alpha: int):
    """Black vertical gradient strip (top_alpha -> bottom_alpha)."""
    w, h = size
    grad = Image.new("L", (1, h))
    for y in range(h):
        a = int(top_alpha + (bottom_alpha - top_alpha) * y / max(h - 1, 1))
        grad.putpixel((0, y), a)
    grad = grad.resize((w, h))
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(grad)
    return black


def main() -> None:
    base = Image.open(BASE).convert("RGBA")
    assert base.size == (W, H), f"base image is {base.size}, expected {(W, H)}"

    # Subtle readability gradients (do not cover the scene, just the captions).
    base.alpha_composite(vertical_gradient((W, 360), 150, 0), (0, 0))
    base.alpha_composite(vertical_gradient((W, 220), 0, 150), (0, H - 220))

    # --- Ghost mark, standing centre-right on the road -------------------
    ghost = Image.open(GHOST).convert("RGBA")
    ghost_h = 480
    ghost_w = int(ghost.width * ghost_h / ghost.height)  # square -> 480
    ghost = ghost.resize((ghost_w, ghost_h), Image.LANCZOS)
    gx = 1200 - ghost_w // 2   # centre x = 1200
    gy = 1060 - ghost_h        # bottom y = 1060 (feet on the road)

    # Soft shadow on the road under the ghost.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([1200 - 230, 1048, 1200 + 230, 1088], fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(shadow)
    base.alpha_composite(ghost, (gx, gy))

    draw = ImageDraw.Draw(base)

    # --- Top caption ------------------------------------------------------
    y = 56
    y += outlined_text(draw, W // 2, y, "CALLED IN SICK FOR", font(118), stroke=10)
    y += 12
    outlined_text(draw, W // 2, y, "GTA 6 LAUNCH DAY", font(118), stroke=10)

    # --- Small make.fun label under the ghost -----------------------------
    outlined_text(draw, 1200, 1072, "make.fun", font(46), stroke=6)

    # --- Bottom caption ---------------------------------------------------
    outlined_text(draw, W // 2, 1178, 'BOSS: "WE CAN SEE YOU ONLINE"',
                  font(62), stroke=7)

    rgb = base.convert("RGB")
    rgb.save(OUT_REPO, "PNG")
    rgb.save(OUT_COPY, "PNG")
    print(f"wrote {OUT_REPO} ({W}x{H})")
    print(f"wrote {OUT_COPY}")


if __name__ == "__main__":
    main()
