"""Write the 24 November 2026 world-news image to /output/entry.png
for make.fun's 'news-image-20261124' bounty.

The poster was drawn by draw_poster.py in this repository: a
front page in the layout proven in the 23 November edition —
a tall lead banner, four tight story cards and six footer
briefs in a 2x3 grid. The day's stories: Nvidia restores
founder Jensen Huang as CEO and markets leap; the UN seeks a
probe of the Libya strike that sank Russia's corvette
Merkury; the EU drafts a 22nd Russia sanctions package; the
UK sanctions Myanmar's junta after the ICJ genocide
ruling; and a 5.6 quake shakes Nepal. The program copies
the finished image.
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
POSTER_PIXELS = 1024


def png_dimensions(path):
    # read the IHDR chunk of a PNG with the standard library
    # alone: 8-byte signature, then length, "IHDR", width, height
    with open(path, "rb") as fh:
        head = fh.read(24)
    if head[:8] != PNG_SIGNATURE or head[12:16] != b"IHDR":
        raise RuntimeError(f"{path} is not a PNG with an IHDR")
    return struct.unpack(">II", head[16:24])


def verify_poster(path):
    width, height = png_dimensions(path)
    if (width, height) != (POSTER_PIXELS, POSTER_PIXELS):
        raise RuntimeError(
            f"poster is {width}x{height}, not {POSTER_PIXELS} square")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("entry.png copy is incomplete")
    verify_poster(dst)
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
