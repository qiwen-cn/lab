# 读取 test.txt 文件的全部内容，以 utf-8 编码打开，返回字符串
text = open("test.txt", encoding="utf-8").read()

# 初始化一个空字典，用于统计每个字符出现的次数
count = {}

# 遍历文本中的每一个字符
for ch in text:
    # 判断该字符是否为字母或数字（过滤掉空格、标点、换行等）
    if ch.isalnum():
        # 该字符计数 +1；若字典中不存在则默认为 0 再 +1
        count[ch] = count.get(ch, 0) + 1

# 将字典的键值对转为列表，并按出现次数（x[1]）降序排序
items = sorted(count.items(), key=lambda x: x[1], reverse=True)

# 遍历出现次数最多的前 10 个字符
for ch, n in items[:10]:
    # 打印字符及其出现次数
    print(ch, n)