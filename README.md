GEMN

```commandline
AIzaSyC3QY7iDVkJnHffN28fP3L1DJllVHsPVpJGzzE
```

https://aistudio.google.com/apikey


curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: GEMINI_API_KEY' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Explain how AI works in a few words"
          }
        ]
      }
    ]
  }'
