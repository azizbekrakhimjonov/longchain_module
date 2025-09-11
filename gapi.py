import requests
import json
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ==== 1. GEMINI bilan rasm tahlili ====
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": "AIzaSyC3QY7iDVkJnHN28fP3L1DJVHsPVpJGzzE"   # <-- API kalitingizni qo'ying
}

with open("img_1.png", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

data = {
    "contents": [
        {
            "parts": [
                {"text": "Rasmni tahlil qil va undagi mahsulot nomini yoz"},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": image_base64
                    }
                }
            ]
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    result = response.json()
    product_name = result["candidates"][0]["content"]["parts"][0]["text"]
    print("Aniqlangan mahsulot:", product_name)
else:
    print("Xatolik:", response.status_code, response.text)
    exit()

# ==== 2. OLX’dan narx topish (oddiy qidiruv) ====
search_url = f"https://www.olx.uz/api/v1/offers/?q={product_name}"
olx_resp = requests.get(search_url)
if olx_resp.status_code == 200:
    try:
        offers = olx_resp.json()["data"]
        if offers:
            price = offers[0]["attributes"][0]["value"]["value"]
            print("Topilgan narx:", price)
        else:
            price = "Narx topilmadi"
    except:
        price = "Narx topilmadi"
else:
    price = "Narx topilmadi"

# ==== 3. Poster yaratish ====
original = Image.open("car1.jpg")
draw = ImageDraw.Draw(original)

# Font sozlash (sizning kompyuteringizdagi TTF faylni ko‘rsatish kerak)
font = ImageFont.truetype("arial.ttf", 40)

# Matn qo'shish
text = f"{product_name}\nNarxi: {price}"
draw.text((50, 50), text, fill="red", font=font)

# Yangi posterni saqlash
original.save("poster.jpg")
print("Poster tayyor: poster.jpg")
