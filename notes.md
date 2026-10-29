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

## 2026-10-30 · 调用GitHub API及CSV保存

### 网络不佳导致请求无限期卡死

- **现象**：程序运行时如果网络不佳或服务器无响应，`requests.get()`会无限期卡住，程序一直处于等待状态，不报错也不退出。
- **原因**：`requests.get()`默认没有超时限制，会一直等待服务器响应。
- **解决**：在请求中加上超时参数`timeout=10`，超过10秒未响应就抛出异常，防止卡死。

### 请求失败导致json()报错或后续获取数据时不符合预期

- **现象**：如果请求失败（比如被GitHub限流返回403），执行`repos.json()`可能会报错或后续获取数据时不符合预期。
- **原因**：`requests.get()`请求失败时不会抛异常，照样返回一个Response。
- **解决**：先检查状态码`if repos.status_code != 200:`，再处理响应正文。

### Windows环境下CSV文件用Excel打开中文乱码

- **现象**：用`encoding="utf-8"`编码写入`repos.csv`，在Windows环境下用Excel打开，导致中文乱码。
- **原因**：Windows下的Excel不会自动识别UTF-8编码文件，会按本地系统编码（如GBK）去解析。
- **解决**：写入文件时改用`encoding="utf-8-sig"`，它会自动在文件开头加上BOM标识（告诉软件这是什么编码），让Excel正确识别UTF-8中文。

### 手动拼接字符串写入CSV可能导致列错位

- **现象**：`f.write(f"{name},{created_at},{size}\n")`写入CSV文件时看似正常，但如果某个字符串包含英文逗号，可能导致列错位。
- **原因**：简单字符串拼接无法自动处理特殊字符（如逗号、双引号、换行符）的转义。
- **解决**：引入Python内置的csv模块，使用`csv.writer(f).writerow([name, created_at, size])`写入，它会自动处理转义和加引号。

### 写入CSV文件时每行之间多出空行

- **现象**：`writer.writerow([name, created_at, size])`使用csv写入器写一行时，可能会导致每行之间多出空行。
- **原因**：`writerow()`写完一行会在末尾加上一个标准的`\r\n`（回车+换行），而`open()`默认会把`\n`转换成当前操作系统（Windows）的`\r\n`，两者叠加变成了`\r\r\n`（某些系统或编辑器中独立的`\r`会被当成换行）。
- **解决**：在`open()`中加上参数`newline=""`。让Python不要自动转换换行符，把控制权交给csv模块。

### 字典取值[]和get()的区别

- **现象**：从接口拿到的仓库字典，可以直接`r["name"]`，也可以`r.get("name")`，但推荐前者。
- **原因**：两者的区别不在语法，在字段缺失时的行为。`[]`缺失时抛`KeyError`，程序立刻停下；`.get()`缺失时返回`None`（或指定默认值），程序继续执行。
- **解决**：按“如果这个字段没了，这条数据还有意义吗”判断。没意义用`[]`，还有意义用`get()`。