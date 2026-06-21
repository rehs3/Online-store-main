from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('media/product_image/product_photo', exist_ok=True)

specs = {
    'oculos_1.jpg': ('Óculos', (30, 144, 255)),
    'oculos_2.jpg': ('Óculos', (70, 130, 180)),
    'joias_1.jpg': ('Joias', (218, 112, 214)),
    'joias_2.jpg': ('Joias', (199, 21, 133)),
    'roupas_1.jpg': ('Roupas', (60, 179, 113)),
    'roupas_2.jpg': ('Roupas', (34, 139, 34)),
}

for fname, (label, color) in specs.items():
    path = os.path.join('media', 'product_image', 'product_photo', fname)
    if os.path.exists(path):
        continue
    img = Image.new('RGB', (800, 600), color)
    d = ImageDraw.Draw(img)
    try:
        fnt = ImageFont.truetype('arial.ttf', 48)
    except Exception:
        fnt = None
    text = label
    w, h = d.textsize(text, font=fnt)
    d.text(((800-w)/2, (600-h)/2), text, fill=(255,255,255), font=fnt)
    img.save(path, 'JPEG')

print('Placeholders gerados em media/product_image/product_photo')
