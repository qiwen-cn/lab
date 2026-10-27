text = open("test.txt", encoding="utf-8").read()

count = {}
for ch in text:
    if ch.strip():          # 跳过空格和换行
        count[ch] = count.get(ch,0)+1     # 让这个字在字典里的计数 +1

items = sorted(count.items(), key=lambda x: x[1], reverse=True)

for ch, n in items[:10]:
    print(ch, n)