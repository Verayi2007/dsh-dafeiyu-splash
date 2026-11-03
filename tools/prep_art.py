"""Prepare the 鲸鱼娘 artwork for the splash: trim, downscale, re-encode as WebP.

Output:
  build/feiyu.webp   (transparent, ~720px on the long side)
  build/art.meta.json
  build/art.b64      (base64 payload used by the build)
"""
import base64
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "build" / "art" / "dsh-feiyu-mood-main" / "assets" / "feiyu.png"
BUILD = ROOT / "build"

im = Image.open(SRC).convert("RGBA")
bbox = im.getbbox()
if bbox:
    im = im.crop(bbox)

target = 760
w, h = im.size
scale = target / max(w, h)
if scale < 1:
    im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)

out = BUILD / "feiyu.webp"
im.save(out, "WEBP", quality=90, method=6, alpha_quality=90)

data = out.read_bytes()
(BUILD / "art.b64").write_text(base64.b64encode(data).decode("ascii"), encoding="utf-8")
(BUILD / "art.meta.json").write_text(
    json.dumps({"size": list(im.size), "bytes": len(data), "b64": len(data) * 4 // 3}, indent=2),
    encoding="utf-8",
)
print(json.dumps({"size": im.size, "webp_bytes": len(data), "png_bytes": SRC.stat().st_size}, indent=2))
