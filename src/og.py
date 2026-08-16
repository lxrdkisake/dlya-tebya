"""Рисует og.png — картинку-превью, которая подтягивается при отправке ссылки в мессенджер.

Запуск:  python src/og.py
Шрифты берутся из src/ttf/ (Unbounded, PressStart2P, Onest — Google Fonts, OFL).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF = os.path.join(ROOT, "src", "ttf")
CATS = os.path.join(ROOT, "assets", "cats")
OUT = os.path.join(ROOT, "og.png")

W, H = 1200, 630
INK = (22, 17, 28)
CREAM = (255, 238, 223)
CORAL = (255, 84, 112)
GOLD = (255, 194, 75)
MINT = (95, 227, 192)
VIOLET = (167, 123, 255)

NAME = "Алиса"
NAME_GEN = "Алисы"   # имя в родительном падеже: «только для ...»


def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(TTF, name), size)
    if wght is not None:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    return f


img = Image.new("RGB", (W, H), INK)

# --- тёплые пятна света, как на самой странице ---
glow = Image.new("RGB", (W, H), INK)
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -240, 560, 380], fill=(96, 34, 52))
gd.ellipse([700, -220, 1420, 320], fill=(84, 62, 26))
gd.ellipse([240, 380, 1160, 1020], fill=(58, 40, 92))
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.blend(img, glow, 0.85)
d = ImageDraw.Draw(img)


def paste_gif(path, box_w, angle=0, frame=0, card=False):
    """Кадр из GIF с прозрачностью, увеличенный до box_w, опционально в «фотокарточке»."""
    im = Image.open(path)
    im.seek(frame)
    im = im.convert("RGBA")
    k = box_w / im.width
    im = im.resize((box_w, max(1, int(im.height * k))), Image.LANCZOS)
    if card:
        pad = 14
        bg = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), CREAM + (255,))
        ImageDraw.Draw(bg).rectangle([0, 0, bg.width - 1, bg.height - 1], outline=CREAM + (255,), width=4)
        bg.alpha_composite(im, (pad, pad))
        im = bg
    if angle:
        im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    return im


def paste_sprite(path, tile_x, tile_y, scale, angle=0):
    """32×32 тайл из спрайт-листа oneko, увеличенный без сглаживания."""
    sheet = Image.open(path).convert("RGBA")
    im = sheet.crop((tile_x * 32, tile_y * 32, tile_x * 32 + 32, tile_y * 32 + 32))
    im = im.resize((32 * scale, 32 * scale), Image.NEAREST)
    if angle:
        im = im.rotate(angle, expand=True, resample=Image.NEAREST)
    return im


layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

# --- коты справа, наклеены как фотокарточки ---
# (у стикеров дно обрезано ровной линией — на карточке это читается как край наклейки)
cat_love = paste_gif(os.path.join(CATS, "cat-love.gif"), 210, angle=-7, card=True)
layer.alpha_composite(cat_love, (858, 140))
cat_happy = paste_gif(os.path.join(CATS, "cat-happy.gif"), 168, angle=6, card=True)
layer.alpha_composite(cat_happy, (790, 372))
# пиксельный кот из oneko (тайл «сидит и смотрит»)
neko = paste_sprite(os.path.join(CATS, "oneko.gif"), 3, 3, 4)
layer.alpha_composite(neko, (688, 468))

img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
d = ImageDraw.Draw(img)

# --- рамка ---
d.rectangle([24, 24, W - 25, H - 25], outline=CREAM, width=4)

# --- верхняя бегущая строка ---
d.rectangle([0, 0, W, 62], fill=CORAL)
d.line([(0, 62), (W, 62)], fill=CREAM, width=4)
f_tick = font("PressStart2P.ttf", 16)
tick = "ПРИГЛАШЕНИЕ ♥ ТОЛЬКО ДЛЯ " + NAME_GEN.upper() + " ♥ КОТИКИ ВКЛЮЧЕНЫ ♥ "
x = 16
while x < W:
    d.text((x, 22), tick, font=f_tick, fill=INK)
    x += d.textlength(tick, font=f_tick)

# --- левый текстовый блок ---
LEFT = 74

# золотой чип
f_chip = font("PressStart2P.ttf", 14)
chip = "ПЕРСОНАЛЬНОЕ ПРИГЛАШЕНИЕ"
cw = d.textlength(chip, font=f_chip)
d.rectangle([LEFT, 138, LEFT + cw + 32, 138 + 46], outline=CREAM, width=3)
d.text((LEFT + 16, 152), chip, font=f_chip, fill=GOLD)

# заголовок с жёсткой коралловой тенью
f_h = font("Unbounded.ttf", 74, 900)
lines = ["ПОЙДЁШЬ", "СО МНОЙ НА", "СВИДАНИЕ?"]
y = 214
for ln in lines:
    d.text((LEFT + 6, y + 6), ln, font=f_h, fill=CORAL)
    d.text((LEFT, y), ln, font=f_h, fill=CREAM)
    y += 88

# мятный чип с программой вечера
f_sub = font("PressStart2P.ttf", 15)
sub = "ХАЧАПУРИ + СОТНЯ КОТОВ"
sw = d.textlength(sub, font=f_sub)
d.rectangle([LEFT, 494, LEFT + sw + 34, 494 + 52], fill=MINT, outline=CREAM, width=3)
d.text((LEFT + 17, 512), sub, font=f_sub, fill=INK)

# --- пиксельные звёздочки-искры ---
for cx, cy, s, col in ((640, 150, 9, GOLD), (676, 470, 7, VIOLET), (1120, 150, 8, MINT),
                       (44, 470, 7, CORAL), (1150, 560, 9, GOLD)):
    d.rectangle([cx - s // 3, cy - s, cx + s // 3, cy + s], fill=col)
    d.rectangle([cx - s, cy - s // 3, cx + s, cy + s // 3], fill=col)

img.save(OUT, "PNG", optimize=True)
print("OK", OUT, os.path.getsize(OUT) // 1024, "KB")
