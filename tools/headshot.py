#!/usr/bin/env python3
"""Turn a real photo into the pixel-art headshot the site expects.

    python3 tools/headshot.py ~/Desktop/headshot.jpg

Centre-crops to a square, biased upward so a portrait keeps its head, and
writes assets/img/me.png at 480x480 — twice the 240px frame, so it stays
sharp on retina screens.
"""
import os, sys
from PIL import Image

OUT_PX = 480      # 2x the 240px frame, for retina sharpness
ZOOM = 0.96       # <1 crops in tighter so the face fills the frame
HEAD_BIAS = 0.24  # 0.5 = dead centre; lower keeps more headroom

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = os.path.expanduser(sys.argv[1])
    if not os.path.exists(src):
        sys.exit(f"no such file: {src}")

    out = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img", "me.png"))

    im = Image.open(src)
    im = im.convert("RGB")

    # square crop, weighted toward the top of the frame
    w, h = im.size
    side = int(min(w, h) * ZOOM)
    left = (w - side) // 2
    top = int((h - side) * HEAD_BIAS)
    im = im.crop((left, top, left + side, top + side))

    im = im.resize((OUT_PX, OUT_PX), Image.LANCZOS)

    im.save(out)
    print(f"wrote {out}  {OUT_PX}x{OUT_PX}  (from a {side}x{side} crop)")
    print("preview it, then: git add -A && git commit && git push")

if __name__ == "__main__":
    main()
