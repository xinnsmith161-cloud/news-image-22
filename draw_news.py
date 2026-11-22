#!/usr/bin/env python3
"""Draw 'The World' front page for Sunday, 22 November 2026.

A single 1024x1024 newspaper image summing up the day's verified news:
COP31 climate talks in Antalya, coalition talks in Israel, the ATP Finals
decider in Turin, and a Myanmar earthquake. All stories were checked
against reporting dated 22 November 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247)
INK = (17, 17, 17)
ACCENT = (139, 26, 26)
GREY = (90, 88, 82)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def center(draw, text, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y


def rule(draw, y, x0=40, x1=984, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip + masthead ----
    rule(d, 24, width=3)
    center(d, "S U N D A Y   E D I T I O N", 32, font(SANS_B, 17), GREY)
    center(d, "The World", 50, font(SERIF_B, 88), INK)
    rule(d, 146, width=1)
    center(d, "Sunday, 22 November 2026", 154, font(SERIF, 25), INK)
    center(d, "ANTALYA  •  JERUSALEM  •  TURIN  •  MYANMAR", 186, font(SANS, 15), GREY)
    center(
        d,
        "Climate talks near a deal, Israel opens unity talks, a title decider in Turin.",
        208,
        font(SERIF, 20),
        INK,
    )
    rule(d, 234, width=3)

    # ---- LEAD: COP31 ----
    y = 248
    d.text((40, y), "CLIMATE SUMMIT  •  ANTALYA", font=font(SANS_B, 19), fill=ACCENT)
    y += 26
    f_head = font(SERIF_B, 47)
    y = draw_lines(
        d, wrap(d, "COP31 nears a deal after a night of talks", f_head, 944),
        40, y, f_head, INK, 53,
    )
    y += 4
    f_deck = font(SERIF, 23)
    deck = (
        "A compromise text goes before delegates on Sunday morning after "
        "negotiators worked through the night. The fossil-fuel fight nearly sank it."
    )
    y = draw_lines(d, wrap(d, deck, f_deck, 944), 40, y, f_deck, INK, 28)
    y += 8
    f_body = font(SERIF, 21)
    body = (
        "Delegates had until 03:00 GMT to raise objections, with an approval "
        "session set for 06:00 GMT. An earlier draft stripped every mention of "
        "ending fossil-fuel use after objections from Saudi Arabia and other "
        "producers, and dropped a proposed $120bn-a-year adaptation target for "
        "2035. The text would be the first COP cover decision to acknowledge "
        "warming passing 1.5\u00b0C, calling for any overshoot to be kept small and short."
    )
    y = draw_lines(d, wrap(d, body, f_body, 944), 40, y, f_body, INK, 26)
    y += 10
    rule(d, y, width=2)
    y += 12

    # ---- two columns ----
    col_w = 452
    gutter = 40
    left_x = 40
    right_x = left_x + col_w + gutter
    col_top = y

    f_col_kick = font(SANS_B, 17)
    f_col_head = font(SERIF_B, 30)
    f_col_body = font(SERIF, 19)

    d.text((left_x, col_top), "ISRAEL  •  JERUSALEM", font=f_col_kick, fill=ACCENT)
    ly = col_top + 24
    ly = draw_lines(
        d, wrap(d, "Unity talks open in Israel", f_col_head, col_w),
        left_x, ly, f_col_head, INK, 33,
    )
    ly += 5
    israel = (
        "Gadi Eisenkot, tasked with forming a government, invited Benjamin "
        "Netanyahu\u2019s Likud to intensive coalition talks, meeting first on "
        "Sunday. His bloc holds 48 of the Knesset\u2019s 120 seats to Likud\u2019s "
        "53. His mandate runs to 6 December, extendable by 14 days."
    )
    ly = draw_lines(d, wrap(d, israel, f_col_body, col_w), left_x, ly, f_col_body, INK, 24)

    d.text((right_x, col_top), "SPORT  •  ATP FINALS, TURIN", font=f_col_kick, fill=ACCENT)
    ry = col_top + 24
    ry = draw_lines(
        d, wrap(d, "Zverev v Alcaraz for the title", f_col_head, col_w),
        right_x, ry, f_col_head, INK, 33,
    )
    ry += 5
    atp = (
        "World No. 1 Alexander Zverev meets Carlos Alcaraz in tonight\u2019s "
        "ATP Finals decider in Turin, at 18:00 CET. Zverev, chasing a third "
        "title, has not dropped a set all week. Alcaraz beat Ben Shelton in "
        "Saturday\u2019s semi-final; Zverev beat Daniil Medvedev in the other."
    )
    ry = draw_lines(d, wrap(d, atp, f_col_body, col_w), right_x, ry, f_col_body, INK, 24)

    div_x = left_x + col_w + gutter // 2
    d.line([(div_x, col_top), (div_x, max(ly, ry))], fill=(180, 178, 170), width=1)

    # ---- IN BRIEF: full-width single lines ----
    y = max(ly, ry) + 14
    rule(d, y, width=2)
    y += 8
    d.text((40, y), "IN BRIEF", font=font(SANS_B, 18), fill=ACCENT)
    y += 25
    f_brief = font(SERIF, 18)
    f_brief_b = font(SANS_B, 17)
    briefs = [
        ("MYANMAR", "Magnitude 4.1 earthquake early on Sunday, India\u2019s National Centre for Seismology said."),
        ("ADDIS ABABA", "To host the next climate summit, COP32, in November 2027."),
    ]
    for label, text in briefs:
        d.text((40, y), label + "  ", font=f_brief_b, fill=INK)
        lw = d.textlength(label + "  ", font=f_brief_b)
        d.text((40 + lw, y + 1), text, font=f_brief, fill=INK)
        y += 24

    # ---- footer ----
    rule(d, 988, width=3)
    center(
        d,
        "Reporting: Reuters  •  ANI  •  ATP Tour  —  The World, Sunday, 22 November 2026",
        997,
        font(SANS, 13),
        GREY,
    )

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
