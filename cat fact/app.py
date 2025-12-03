from flask import Flask, send_file, send_from_directory
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
from io import BytesIO

app = Flask(__name__, static_folder="static")

FACTS_DIR = "facts"
FONT_PATH = os.path.join("fonts", "arial.ttf")   # ← your font

shuffle_queue = []


# -----------------------------------
# LOAD AVAILABLE FACTS
# -----------------------------------
def get_fact_folders():
    return sorted([
        int(name)
        for name in os.listdir(FACTS_DIR)
        if name.isdigit() and os.path.isdir(os.path.join(FACTS_DIR, name))
    ])


# -----------------------------------
# SHUFFLE PLAY QUEUE
# -----------------------------------
def refill_shuffle_queue():
    global shuffle_queue
    folders = get_fact_folders()
    shuffle_queue = folders.copy()
    random.shuffle(shuffle_queue)
    print("🔄 Shuffle queue rebuilt:", shuffle_queue)


def get_next_fact():
    global shuffle_queue

    if not shuffle_queue:
        refill_shuffle_queue()

    return shuffle_queue.pop(0)


# -----------------------------------
# LOAD TEXT + IMAGE
# -----------------------------------
def load_fact(folder_number):
    folder = os.path.join(FACTS_DIR, str(folder_number))

    with open(os.path.join(folder, "text.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()

    img = Image.open(os.path.join(folder, "image.jpg")).convert("RGB")
    return text, img


# -----------------------------------
# IMAGE EDIT FUNCTIONS
# -----------------------------------
def upscale_background(img, w=1920, h=1080):
    bg = img.copy().resize((w, h), Image.LANCZOS)
    return bg.filter(ImageFilter.GaussianBlur(40))


def fit_center(img, max_w=1600, max_h=900):
    iw, ih = img.size
    scale = min(max_w / iw, max_h / ih)
    new_size = (int(iw * scale), int(ih * scale))
    return img.resize(new_size, Image.LANCZOS)


# -----------------------------------
# DRAW TEXT ON IMAGE
# -----------------------------------
def draw_text(image, text):
    draw = ImageDraw.Draw(image)

    # Load your custom font
    try:
        font = ImageFont.truetype(FONT_PATH, 58)   # ← BIGGER 58px FONT
    except Exception as e:
        print("Font error:", e)
        font = ImageFont.load_default()

    words = text.split()
    lines, current = [], ""
    max_width = image.width - 100

    for w in words:
        test_line = (current + " " + w).strip()
        if draw.textlength(test_line, font=font) <= max_width:
            current = test_line
        else:
            lines.append(current)
            current = w

    if current:
        lines.append(current)

    line_height = draw.textbbox((0, 0), "A", font=font)[3]
    total_height = line_height * len(lines) + 40

    bottom = image.height - total_height
    draw.rectangle([(0, bottom), (image.width, image.height)], fill=(0, 0, 0, 170))

    y = bottom + 20
    for line in lines:
        w = draw.textlength(line, font=font)
        x = (image.width - w) // 2

        # shadow
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            draw.text((x + dx, y + dy), line, font=font, fill="black")

        draw.text((x, y), line, font=font, fill="white")
        y += line_height + 6

    out = BytesIO()
    image.save(out, "PNG")
    out.seek(0)
    return out


# -----------------------------------
# FRONTEND
# -----------------------------------
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# -----------------------------------
# API ENDPOINT
# -----------------------------------
@app.get("/cat")
def cat():
    folder = get_next_fact()

    text, img = load_fact(folder)

    bg = upscale_background(img)
    main = fit_center(img)

    bg.paste(
        main,
        (
            (bg.width - main.width) // 2,
            (bg.height - main.height) // 2
        )
    )

    result = draw_text(bg, text)

    return send_file(result, mimetype="image/png")


# -----------------------------------
# VERCEL: INIT SHUFFLE
# -----------------------------------
refill_shuffle_queue()


# DO NOT RUN SERVER HERE (Vercel will run automatically)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
