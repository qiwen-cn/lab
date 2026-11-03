import requests

with open("test.txt", "r", encoding="utf-8") as f:
    text = f.read()

r = requests.post(
    "http://127.0.0.1:8000/summarize",
    json={"text": text},
    timeout=90,
)
print(r.status_code)
print(r.text)
