# 踩坑笔记

## 2026-10-28 · 文本文件字频统计

### 读中文文件报UnicodeDecodeError

- **现象**：读取文件中的文本时`open("test.txt").read()`报错。`UnicodeDecodeError: 'gbk' codec can't decode byte 0xe7 in position 0: illegal multibyte sequence`gbk解码器在第0个字节（0xe7）这里解析不下去了，它不是合法的GBK序列。
- **原因**：文件是UTF-8编码，Windows中文系统默认拿GBK去解码，两套编码对不上。
- **解决**：打开文件时显式指定编码`open("test.txt", encoding="utf-8").read()`。

### 字典统计字频时，第一次报KeyError

- **现象**：字典`count`里还没有键`ch`时，`count[ch] += 1`报错。`KeyError: '窗'`字典里不存在名为'窗'的键。
- **原因**：Python的字典不会给新键自动初始化。
- **解决**：改成`count[ch] = count.get(ch, 0) + 1`，在键`ch`不存在时用默认值`0`。

### 字频前几名全是标点

- **现象**：程序正常执行，但输出结果前几名是标点符号。
- **原因**：没有过滤标点符号。
- **解决**：只统计字母和数字`if ch.isalnum():`。

### sorted()排序后，原字典没法再按键取值

- **现象**：`count = sorted(count, key=lambda x: count[x], reverse=True)`排序正常，但是之后通过键获取值`count[ch]`时报错。`TypeError: list indices must be integers or slices, not str`列表的下标只能是整数或切片，不能是字符串。
- **原因**：`sorted()`返回的是列表。字典排序后，只保留了键，没保留值。
- **解决**：改成`items = sorted(count.items(), key=lambda x: x[1], reverse=True)`，`count.items()`将字典中的键值对打包成一对一对的元组(键, 值)。