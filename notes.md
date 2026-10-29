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
- **解决**：改成`items = sorted(count.items(), key=lambda x: x[1], reverse=True)`，`count.items()`将字典中的键值对打包成一对一对的元组(原字典键, 原字典值)。

## 2026-10-29 · 文件按扩展名归档

### 遍历文件夹时移动文件可能导致漏文件或报错

- **现象**：`for file in path.iterdir():`遍历路径下所有文件或文件夹时，如果在遍历过程中改变目录结构（添加、移动、删除、重命名文件等），可能会导致有些文件没被处理到，或者偶尔报FileNotFoundError。
- **原因**：`iterdir()`返回的是个惰性迭代器，依赖操作系统的目录游标，目录结构变化会导致游标错乱。
- **解决**：将遍历结果转化为列表快照再循环`for file in list(path.iterdir()):`。

### pathlib的replace()会让同名文件被静默覆盖

- **现象**：`file.replace(target_file)`将文件移动到目标文件夹时，如果目标文件夹里已存在同名文件，原文件会被悄悄覆盖。
- **原因**：`replace()`底层逻辑就是替换，不会检查目标路径是否已有文件。
- **解决**：移动前加一步判断`if not target_file.exists():`。