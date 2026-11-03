"""Split the artwork into two layers so the head can move on its own.

  assets/rig/body.webp  the whole figure
  assets/rig/head.webp  everything above the fur collar, seam feathered inside the fur

Nothing is painted: both layers are the same pixels, so a small head motion only ever
reveals a sliver of identical image — never a hole, never a patch.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "feiyu.webp"
OUT = ROOT / "assets" / "rig"
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGBA")
W, H = img.size
arr = np.array(img).astype(np.float32)

TOP, BOT = 616, 676                       # feather band, inside the fur collar
ys = np.arange(H, dtype=np.float32)
t = np.clip((ys - TOP) / (BOT - TOP), 0.0, 1.0)
a = 255.0 * (1.0 - t) ** 1.5
alpha = np.repeat(a[:, None], W, axis=1) / 255.0

head = arr.copy()
head[:, :, 3] = head[:, :, 3] * alpha
Image.fromarray(head.astype(np.uint8)).save(OUT / "head.webp", "WEBP", quality=92, method=6)
img.save(OUT / "body.webp", "WEBP", quality=92, method=6)

for stale in ("eye-l.webp", "eye-r.webp", "head-open.webp", "head-closed.webp"):
    p = OUT / stale
    if p.exists():
        p.unlink()

meta = {
    "canvas": [W, H],
    "seam": [TOP, BOT],
    "sizes": {p.name: p.stat().st_size for p in OUT.glob("*.webp")},
}
(OUT / "rig.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
print(json.dumps(meta, indent=2))
