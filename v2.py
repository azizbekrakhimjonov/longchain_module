# import requests
# import json
#
# url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
#
# headers = {
#     "Content-Type": "application/json",
#     "X-goog-api-key": "AIzaSyC3QY7iDVkJnHN28fP3L1DJVHsPVpJGzzE"
# }
#
# data = {
#     "contents": [
#         {
#             "parts": [
#                 {"text": "salom menga sher yoz9b ber sevgi haqida"}
#             ]
#         }
#     ]
# }
#
# response = requests.post(url, headers=headers, data=json.dumps(data))
#
# if response.status_code == 200:
#     result = response.json()
#     # Modeldan chiqgan matnni olish
#     try:
#         text_output = result["candidates"][0]["content"]["parts"][0]["text"]
#         print("Model javobi:", text_output)
#     except Exception as e:
#         print("JSON tuzilmasini o‘qishda xato:", e)
#         print(json.dumps(result, indent=2))
# else:
#     print("Xatolik:", response.status_code)
#     print(response.text)


import requests
import json
import base64

# API manzili
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": "AIzaSyC3QY7iDVkJnHN28fP3L1DJVHsPVpJGzzE"
}

# Rasmni o'qib base64 ga o'tkazish
with open("car1.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

data = {
    "contents": [
        {
            "parts": [
                {"text": "shu rasmda nima bor?"},
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
    try:
        text_output = result["candidates"][0]["content"]["parts"][0]["text"]
        print("Model javobi:", text_output)
    except Exception as e:
        print("JSON tuzilmasini o‘qishda xato:", e)
        print(json.dumps(result, indent=2))
else:
    print("Xatolik:", response.status_code)
    print(response.text)
