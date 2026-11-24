"""Draw the 24 November 2026 world-news poster.

The layout is the front page proven in the 23 November edition
(v4: a tall lead banner, four tight story cards, six footer
briefs in a 2x3 grid); every story is new, gathered for Tuesday
24 November 2026 and cross-checked across wire and broadsheet
reporting of the day:

- Lead: Nvidia's board restores founder Jensen Huang as CEO
  after 11 days; markets cheer, the S&P 500 leaps 4.7% on the
  day (SCMP, AP via Manila Times, One Turn, Horizon close).
- Libya: the UN seeks a probe after Ukrainian sea drones sank
  the Russian corvette Merkury at Benghazi (CNN, WSJ, Al
  Jazeera, IQMia).
- Europe: the EU drafts a 22nd Russia sanctions package,
  reaching banks, soldiers and flags at sports events (SCMP,
  Saudi Gazette, One Turn).
- Myanmar: the UK sanctions Myanmar's military leaders after
  the ICJ's Rohingya genocide ruling (SCMP, Saudi Gazette).
- Nepal: a magnitude 5.6 earthquake strikes Koshi province
  near the Tibet border; no deaths reported (PTI wires).
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (245, 240, 230)
INK = (22, 22, 22)
RED = (168, 32, 24)
GREY = (92, 86, 78)
DECK_GREY = (70, 66, 60)
CARD = (252, 249, 243)
LINE = (196, 60, 46)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SANS_B, 66)
F_DATE = font(SANS_B, 40)
F_KICKER = font(SANS_B, 25)
F_HEAD = font(SANS_B, 43)
F_DECK = font(SANS, 27)
F_LEAD_DECK = font(SANS, 28)
F_BRIEF = font(SANS, 22)
F_LABEL = font(SANS_B, 20)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- pictograms, drawn in an (x, y, s) box, s = box side ---------

def icon_chip(d, x, y, s):
    # a microchip: square body, inner square, pins on all sides
    bx0, by0 = x + s * 0.24, y + s * 0.24
    bx1, by1 = x + s * 0.76, y + s * 0.76
    for t in (0.32, 0.5, 0.68):
        d.line([x + s * t, y + s * 0.06, x + s * t, y + s * 0.24],
               fill=INK, width=6)
        d.line([x + s * t, y + s * 0.76, x + s * t, y + s * 0.94],
               fill=INK, width=6)
        d.line([x + s * 0.06, y + s * t, x + s * 0.24, y + s * t],
               fill=INK, width=6)
        d.line([x + s * 0.76, y + s * t, x + s * 0.94, y + s * t],
               fill=INK, width=6)
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=7)
    d.rectangle([x + s * 0.40, y + s * 0.40, x + s * 0.60, y + s * 0.60],
                fill=RED)


def icon_ship(d, x, y, s):
    hull = [(x + 8, y + s * 0.52), (x + s - 8, y + s * 0.52),
            (x + s - 22, y + s * 0.74), (x + 22, y + s * 0.74)]
    d.polygon(hull, fill=INK)
    d.rectangle([x + s * 0.42, y + s * 0.22, x + s * 0.58, y + s * 0.52],
                fill=RED)
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.22],
           fill=INK, width=5)
    for i in range(3):
        yy = y + s * (0.84 + 0.0)
        xx = x + 6 + i * (s - 12) / 3
        d.arc([xx, yy - 7, xx + (s - 12) / 3, yy + 7], 0, 180, fill=RED,
              width=5)


def icon_ban(d, x, y, s):
    # a prohibition sign: ring and diagonal slash
    d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=RED, width=9)
    import math
    off = (s - 12) / 2 * (1 - math.sqrt(0.5))
    d.line([x + 6 + off, y + s - 6 - off, x + s - 6 - off, y + 6 + off],
           fill=RED, width=9)


def icon_quake(d, x, y, s):
    # a seismograph trace: flat, one sharp spike, flat again
    mid = y + s * 0.52
    pts = [(x + 4, mid), (x + s * 0.3, mid), (x + s * 0.42, y + s * 0.1),
           (x + s * 0.54, y + s * 0.92), (x + s * 0.64, mid),
           (x + s - 4, mid)]
    d.line(pts, fill=RED, width=7, joint="curve")


def icon_badge(d, x, y, s):
    shield = [(x + s * 0.5, y + 4), (x + s - 8, y + s * 0.16),
              (x + s - 8, y + s * 0.52), (x + s * 0.5, y + s - 4),
              (x + 8, y + s * 0.52), (x + 8, y + s * 0.16)]
    d.polygon(shield, outline=INK, width=6)
    cx, cy = x + s / 2, y + s * 0.42
    d.polygon([(cx, cy - 13), (cx + 4, cy - 4), (cx + 13, cy - 4),
               (cx + 6, cy + 3), (cx + 8, cy + 12), (cx, cy + 6),
               (cx - 8, cy + 12), (cx - 6, cy + 3), (cx - 13, cy - 4),
               (cx - 4, cy - 4)], fill=RED)


LEAD = ("01 · TECH & MARKETS — THE DAY'S LEAD STORY", icon_chip,
        "Huang returns to lead Nvidia",
        "Board reverses course; the S&P 500 leaps 4.7%.")

STORIES = [
    ("02 · LIBYA", icon_ship,
     "UN seeks probe of Libya strike",
     "Sea drones sank the Merkury."),
    ("03 · EUROPE", icon_ban,
     "EU drafts 22nd Russia sanctions",
     "Banks, troops, sports flags."),
    ("04 · MYANMAR", icon_badge,
     "UK sanctions Myanmar junta",
     "The ICJ called it genocide."),
    ("05 · NEPAL", icon_quake,
     "Quake of 5.6 shakes Nepal",
     "No deaths reported so far."),
]

# The six footer briefs, laid out as row pairs in the grid:
# (Space, US law), (Armenia, Landmines), (Colombia, Bangladesh).
BRIEFS = [
    "Space: Pakistani Zeeshan Ali to fly to Tiangong",
    "US states sue Musk firms over Grok images",
    "Armenia drafts charter, drops Karabakh claims",
    "Landmine casualties hit 5-year high: 7,000",
    "Colombia: car bomb hits Villavicencio offices",
    "Bangladesh: ex-PM Hasina plans Dec 16 return",
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((48, 26), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.text((48, 106), "Tuesday, 24 November 2026", font=F_DATE, fill=RED)
    d.line([48, 158, W - 48, 158], fill=LINE, width=5)
    d.line([48, 166, W - 48, 166], fill=LINE, width=2)

    # the lead banner: 186px tall, headline at 46px on one
    # measured line; the pictogram sits lower right, its top
    # clearing the headline's foot, and the deck runs under
    # a red rule
    lead_y, lead_h = 180, 186
    kicker, icon, head, deck = LEAD
    d.rounded_rectangle([48, lead_y, W - 48, lead_y + lead_h], 14,
                        fill=CARD, outline=(216, 208, 192), width=2)
    d.text((70, lead_y + 14), kicker, font=F_KICKER, fill=RED)
    F_LEAD = font(SANS_B, 46)
    head_lines = wrap(d, head, F_LEAD, W - 96 - 44)
    assert len(head_lines) == 1, "lead headline must stay on one line"
    d.text((70, lead_y + 46), head_lines[0], font=F_LEAD, fill=INK)
    icon(d, W - 48 - 22 - 96, lead_y + 84, 96)
    d.line([70, lead_y + 118, W - 48 - 22 - 96 - 18, lead_y + 118],
           fill=LINE, width=3)
    deck_lines = wrap(d, deck, F_LEAD_DECK,
                      W - 48 - 22 - 96 - 18 - 70)
    assert len(deck_lines) == 1, "lead deck must stay on one line"
    d.text((70, lead_y + 132), deck_lines[0], font=F_LEAD_DECK,
           fill=DECK_GREY)

    # story cards, 2 columns x 2 rows, 224px tall; the
    # headline starts right under the pictogram row so the
    # type fills the card
    F_CARD = font(SANS_B, 43)
    top, card_h, gap = lead_y + lead_h + 12, 224, 12
    col_w = (W - 96 - gap) // 2
    for i, (kicker, icon, head, deck) in enumerate(STORIES):
        cx = 48 + (i % 2) * (col_w + gap)
        cy = top + (i // 2) * (card_h + gap)
        d.rounded_rectangle([cx, cy, cx + col_w, cy + card_h], 14,
                            fill=CARD, outline=(216, 208, 192), width=2)
        d.text((cx + 22, cy + 14), kicker, font=F_KICKER, fill=RED)
        icon(d, cx + col_w - 22 - 80, cy + 4, 80)
        lines = wrap(d, head, F_CARD, col_w - 44)
        assert len(lines) <= 2, f"headline wraps past 2 lines: {head!r}"
        yy = cy + 84
        for ln in lines:
            d.text((cx + 22, yy), ln, font=F_CARD, fill=INK)
            yy += 50
        deck_lines = wrap(d, deck, F_DECK, col_w - 44)
        assert len(deck_lines) == 1, f"deck wraps past 1 line: {deck!r}"
        d.text((cx + 22, cy + card_h - 34), deck_lines[0], font=F_DECK,
               fill=DECK_GREY)

    # footer briefs: "ALSO TODAY" as a red label on the divider,
    # then the six briefs in a 2 x 3 grid at 24px, each wrapped
    # to its column and at most two lines, bottom margin kept
    div_y = top + 2 * card_h + gap + 12
    d.text((48, div_y - 10), "ALSO TODAY", font=F_LABEL, fill=RED)
    d.line([216, div_y, W - 48, div_y], fill=LINE, width=3)
    col_x = [48, 524]
    col_w_b = 452
    yy = div_y + 12
    for r in range(3):
        row = []
        for c in range(2):
            lines = wrap(d, BRIEFS[r * 2 + c], F_BRIEF, col_w_b)
            assert len(lines) <= 2, f"brief wraps past 2 lines: {BRIEFS[r * 2 + c]!r}"
            row.append(lines)
        for c in range(2):
            for j, ln in enumerate(row[c]):
                d.text((col_x[c], yy + j * 23), ln, font=F_BRIEF,
                       fill=INK)
        yy += max(len(row[0]), len(row[1])) * 23
    assert yy <= H - 16, "briefs crowd the bottom margin"

    import os
    here = os.path.dirname(os.path.abspath(__file__))
    img.save(os.path.join(here, "entry.png"), optimize=True)
    img.save("/tmp/news-20261124.png", optimize=True)
    print("saved entry.png and /tmp/news-20261124.png")


if __name__ == "__main__":
    main()
