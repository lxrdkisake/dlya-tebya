import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TTF = r"C:/Users/kenji/AppData/Local/Temp/claude/H--OSPanel-domains-untitled23/95fdaabf-657d-4dfe-9263-7ec0ba0e42ac/scratchpad/ttf"
OUT = r"H:/OSPanel/domains/untitled23/og.png"
W, H = 1200, 630

CREAM = (255, 247, 242)
ROSE = (232, 87, 124)
ROSE_DEEP = (184, 57, 94)
PLUM = (59, 36, 48)
GOLD = (184, 134, 43)

def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(TTF, name), size)
    if wght is not None:
        try:
            f.set_variation_by_axes([wght])
        except Exception as e:
            print("var axes failed:", e)
    return f

img = Image.new("RGB", (W, H), CREAM)

# --- мягкие цветовые пятна ---
glow = Image.new("RGB", (W, H), CREAM)
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -300, 620, 380], fill=(255, 228, 238))
gd.ellipse([700, -260, 1500, 340], fill=(255, 239, 224))
gd.ellipse([180, 380, 1080, 1000], fill=(251, 216, 230))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.blend(img, glow, 0.92)

d = ImageDraw.Draw(img)

# --- рамка ---
d.rounded_rectangle([30, 30, W - 30, H - 30], radius=26, outline=(226, 186, 197), width=2)
d.rounded_rectangle([40, 40, W - 40, H - 40], radius=20, outline=(232, 205, 168), width=1)


def heart(dr, cx, cy, scale, fill):
    pts = []
    for i in range(361):
        t = math.radians(i)
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * scale, cy - y * scale))
    dr.polygon(pts, fill=fill)


# --- сердце: мягкое свечение + сама фигура ---
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
heart(ImageDraw.Draw(sh), 600, 180, 3.35, (232, 87, 124, 60))
sh = sh.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
d = ImageDraw.Draw(img)
heart(d, 600, 172, 3.0, ROSE)

# --- мелкие сердечки по углам (подальше от текста) ---
for cx, cy, s, a in ((132, 128, 1.15, 62), (1068, 128, 1.15, 62),
                     (108, 500, .95, 44), (1092, 500, .95, 44),
                     (232, 556, .7, 34), (968, 556, .7, 34)):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    heart(ImageDraw.Draw(layer), cx, cy, s, (232, 87, 124, a))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
d = ImageDraw.Draw(img)


def center(text, f, y, fill, tracking=0):
    if tracking:
        widths = [d.textlength(ch, font=f) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = (W - total) / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=f, fill=fill)
            x += w + tracking
        return
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


f_eyebrow = font("Nunito.ttf", 24, 800)
f_title = font("Cormorant.ttf", 82, 600)
f_script = font("MarckScript.ttf", 46)
f_small = font("Nunito.ttf", 25, 600)

center("ПЕРСОНАЛЬНОЕ ПРИГЛАШЕНИЕ", f_eyebrow, 292, GOLD, tracking=6)

# декоративная линия с ромбом по центру
d.line([(432, 342), (576, 342)], fill=(224, 186, 198), width=2)
d.line([(624, 342), (768, 342)], fill=(224, 186, 198), width=2)
d.polygon([(600, 333), (608, 342), (600, 351), (592, 342)], fill=GOLD)

center("Пойдёшь со мной на свидание?", f_title, 366, PLUM)
center("нажми, чтобы открыть", f_script, 480, ROSE_DEEP)

img.save(OUT, "PNG", optimize=True)
print("OK", OUT, os.path.getsize(OUT) // 1024, "KB")
