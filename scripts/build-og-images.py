"""Generate 1200x630 Open Graph images for each page.

Run from repo root:  python3 scripts/build-og-images.py
Outputs to: assets/images/og/<slug>.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "images", "og")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1200, 630
ORANGE = (231, 91, 42)
CORAL = (244, 136, 74)
PEACH = (255, 184, 123)
CHARCOAL = (26, 26, 26)
BEIGE = (246, 230, 210)
WHITE = (255, 255, 255)
WARM_BG = (250, 247, 242)
DEEP_BROWN = (74, 55, 37)


def load_font(size, weight="bold"):
    # Try common system fonts; fall back to default.
    paths = [
        # macOS
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


FONT_HEAD = load_font(76)
FONT_HEAD_SM = load_font(62)
FONT_SUB = load_font(30)
FONT_BRAND = load_font(36)
FONT_EYEBROW = load_font(22)
FONT_FOOT = load_font(22)


def gradient_bg(w, h):
    """Diagonal sunset gradient: orange → coral → peach with a soft charcoal at top-right."""
    img = Image.new("RGB", (w, h), WARM_BG)
    px = img.load()
    for y in range(h):
        for x in range(w):
            # 0..1 along the diagonal
            t = (x / w * 0.55) + (y / h * 0.45)
            t = max(0.0, min(1.0, t))
            if t < 0.5:
                # warm bg → coral
                k = t / 0.5
                r = int(WARM_BG[0] + (CORAL[0] - WARM_BG[0]) * k)
                g = int(WARM_BG[1] + (CORAL[1] - WARM_BG[1]) * k)
                b = int(WARM_BG[2] + (CORAL[2] - WARM_BG[2]) * k)
            else:
                k = (t - 0.5) / 0.5
                r = int(CORAL[0] + (ORANGE[0] - CORAL[0]) * k)
                g = int(CORAL[1] + (ORANGE[1] - CORAL[1]) * k)
                b = int(CORAL[2] + (ORANGE[2] - CORAL[2]) * k)
            px[x, y] = (r, g, b)
    return img


def soft_circle(img, cx, cy, r, color, alpha=120):
    """Paint a soft radial blob on the image."""
    blob = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob)
    bd.ellipse((0, 0, r * 2, r * 2), fill=(*color, alpha))
    blob = blob.filter(ImageFilter.GaussianBlur(r // 3))
    img.paste(blob, (cx - r, cy - r), blob)


def rounded_rect(draw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def wrap_text(draw, text, font, max_width):
    """Naive wrap by measuring word widths."""
    words = text.split()
    lines = []
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        bb = draw.textbbox((0, 0), trial, font=font)
        if bb[2] - bb[0] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_og(slug, eyebrow, headline, subline):
    base = gradient_bg(W, H).convert("RGBA")
    # Soft brand glow blobs
    soft_circle(base, 1100, 60, 280, ORANGE, alpha=110)
    soft_circle(base, 90, 560, 320, DEEP_BROWN, alpha=80)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Inner card frame (subtle glass)
    rounded_rect(d, (40, 40, W - 40, H - 40), radius=42, fill=(255, 255, 255, 18))

    # Top brand row
    brand_text = "AIDAN"
    brand_sub = "GROUP OF COMPANIES"
    d.text((80, 70), brand_text, font=FONT_BRAND, fill=WHITE)
    d.text((82, 116), brand_sub, font=FONT_EYEBROW, fill=(255, 255, 255, 220))

    # Eyebrow pill
    if eyebrow:
        ex, ey = 80, 200
        bb = d.textbbox((0, 0), eyebrow.upper(), font=FONT_EYEBROW)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad_x, pad_y = 18, 10
        rounded_rect(
            d,
            (ex, ey, ex + tw + pad_x * 2, ey + th + pad_y * 2),
            radius=24,
            fill=(255, 255, 255, 60),
        )
        d.text((ex + pad_x, ey + pad_y - 2), eyebrow.upper(), font=FONT_EYEBROW, fill=WHITE)

    # Headline
    head_y = 270
    head_font = FONT_HEAD if len(headline) <= 38 else FONT_HEAD_SM
    lines = wrap_text(d, headline, head_font, W - 200)
    for i, ln in enumerate(lines):
        d.text((80, head_y + i * (head_font.size + 6)), ln, font=head_font, fill=WHITE)
    head_bottom = head_y + len(lines) * (head_font.size + 6)

    # Sub
    if subline:
        sub_lines = wrap_text(d, subline, FONT_SUB, W - 200)
        for i, ln in enumerate(sub_lines[:2]):
            d.text(
                (80, head_bottom + 16 + i * (FONT_SUB.size + 6)),
                ln,
                font=FONT_SUB,
                fill=(255, 255, 255, 235),
            )

    # Footer URL + accent line
    d.line([(80, H - 90), (W - 80, H - 90)], fill=(255, 255, 255, 80), width=1)
    d.text((80, H - 70), "aidan.com.my", font=FONT_FOOT, fill=(255, 255, 255, 235))
    d.text(
        (W - 80 - 220, H - 70),
        "Building tomorrow, together",
        font=FONT_FOOT,
        fill=(255, 255, 255, 200),
    )

    out = Image.alpha_composite(base, overlay).convert("RGB")
    path = os.path.join(OUT_DIR, f"{slug}.png")
    out.save(path, "PNG", optimize=True)
    print(f"  wrote {path}")
    return path


PAGES = [
    {
        "slug": "default",
        "eyebrow": "Aidan Group",
        "headline": "Building the future with confidence.",
        "subline": "A strategic group in Technology, Education, and Marketing — locally and internationally.",
    },
    {
        "slug": "home",
        "eyebrow": "Home",
        "headline": "Building the future with confidence.",
        "subline": "A strategic group in Technology, Education, and Marketing — locally and internationally.",
    },
    {
        "slug": "group",
        "eyebrow": "The Group",
        "headline": "One strategic group. Three industries.",
        "subline": "Technology, Education, and Marketing — built on quality, improvement, and trust.",
    },
    {
        "slug": "ventures",
        "eyebrow": "Portfolio",
        "headline": "The ventures that power the group.",
        "subline": "From custom software for government to international olympiads for students.",
    },
    {
        "slug": "culture",
        "eyebrow": "Team Culture",
        "headline": "Part who we are. Part who we aspire to be.",
        "subline": "Give A Damn · Empathy · Mastery · Superior — our four core values.",
    },
    {
        "slug": "career",
        "eyebrow": "Open Roles",
        "headline": "Help us build the company we always dreamed of.",
        "subline": "Roles across technology, education, design, sales, and marketing.",
    },
    {
        "slug": "contact",
        "eyebrow": "Get In Touch",
        "headline": "Let's build something together.",
        "subline": "Kuala Lumpur, Malaysia · +603 4143 0572 · contact@aidan.com.my",
    },
]


def main():
    print(f"Generating OG images into {OUT_DIR}")
    for p in PAGES:
        draw_og(p["slug"], p["eyebrow"], p["headline"], p["subline"])
    print("Done.")


if __name__ == "__main__":
    main()
