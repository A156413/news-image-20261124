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

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("entry.png copy is incomplete")
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
