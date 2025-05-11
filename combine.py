import os
from PIL import Image, ImageDraw
from tqdm import tqdm
from math import ceil

# ПАРАМЕТРЫ
DPI = 365
PAGE_SIZE = "A4"  # варианты: "A4", "A5", "A6"
ORIENTATION = "portrait"  # "portrait" или "landscape"
MARGIN_CM = 0.25
SPACING_CM = 0
OUTPUT_FILE = "output.pdf"

# РАЗМЕРЫ СТРАНИЦ В СМ
PAGE_SIZES_CM = {
    "A4": (21.0, 29.7),
    "A5": (14.8, 21.0),
    "A6": (10.5, 14.8)
}

MARGIN_PX = int(MARGIN_CM * DPI / 2.54)
SPACING_PX = int(SPACING_CM * DPI / 2.54)

page_width_cm, page_height_cm = PAGE_SIZES_CM[PAGE_SIZE]
if ORIENTATION == "landscape":
    page_width_cm, page_height_cm = page_height_cm, page_width_cm

PAGE_WIDTH_PX = int(page_width_cm * DPI / 2.54)
PAGE_HEIGHT_PX = int(page_height_cm * DPI / 2.54)

CONTENT_WIDTH_PX = PAGE_WIDTH_PX - 2 * MARGIN_PX
CONTENT_HEIGHT_PX = PAGE_HEIGHT_PX - 2 * MARGIN_PX

images = []

for file in os.listdir('.'):
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        img = Image.open(file).convert("RGB")
        images.append((file, img))

placed_images = []
current_page = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), "white")
draw = ImageDraw.Draw(current_page)
x, y = MARGIN_PX, MARGIN_PX
row_height = 0
pages = []

for name, img in tqdm(images, desc="Размещение изображений"):
    w, h = img.size
    if x + w > PAGE_WIDTH_PX - MARGIN_PX:
        x = MARGIN_PX
        y += row_height + SPACING_PX
        row_height = 0

    if y + h > PAGE_HEIGHT_PX - MARGIN_PX:
        pages.append(current_page)
        current_page = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), "white")
        draw = ImageDraw.Draw(current_page)
        x, y = MARGIN_PX, MARGIN_PX
        row_height = 0

    current_page.paste(img, (x, y))
    x += w + SPACING_PX
    row_height = max(row_height, h)

pages.append(current_page)

pages[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=pages[1:],
    resolution=DPI,
    quality=95
)

print(f"Сохранено в файл {OUTPUT_FILE}")