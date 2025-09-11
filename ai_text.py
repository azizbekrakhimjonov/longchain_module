import requests
import json

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": "AIzaSyC3QY7iDVkJnHN28fP3L1DJVHsPVpJGzzE"
}

data = {
    "contents": [
        {
            "parts": [
                {"text": "salom menga sher yoz9b ber sevgi haqida"}
            ]
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    # Modeldan chiqgan matnni olish
    try:
        text_output = result["candidates"][0]["content"]["parts"][0]["text"]
        print("Model javobi:", text_output)
    except Exception as e:
        print("JSON tuzilmasini o‘qishda xato:", e)
        print(json.dumps(result, indent=2))
else:
    print("Xatolik:", response.status_code)
    print(response.text)