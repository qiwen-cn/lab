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

### 字典使用切片报KeyError

- **现象**：字典使用切片时`print(count[:10])`报错。`KeyError: slice(None, 10, None)`，字典报错：找不到名为`[:10]`的键。
- **原因**：字典不支持切片，只认键（Key）。在底层，`[:10]`会被转换成`slice(None, 10, None)`这个对象，字典把它当成了一个普通的键去查找，因为字典里没有这个键，所以抛出`KeyError`。
- **解决**：先转成列表再切片。可以通过`sorted()`排序，排序后拿到的是列表。

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

## 2026-10-30 · 调用GitHub API并CSV保存

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

## 2026-10-31 · 读取CSV数据统计并排序

### 读取CSV表头多出隐藏字符

- **现象**：读取时第一列表头前面多出个`\ufeff`。
- **原因**：文件开头有BOM标识时，如果读取不加`sig`，Python就会把BOM当成真实的文本内容读出来。
- **解决**：读写CSV时统一使用`encoding="utf-8-sig"`。写时防Excel乱码，读时自动剥离BOM。

### 使用sum()报TypeError

- **现象**：使用`sum(data, key=lambda r: int(r[2]))`累计求和时报错。`TypeError: sum() got an unexpected keyword argument 'key'`，`sum()`收到了一个意外的关键字参数`'key'`。
- **原因**：`sorted()`、`max()`、`min()`都有`key`参数，而`sum()`不支持`key`参数。
- **解决**：使用生成器表达式`sum(int(r[2]) for r in data)`。

### CSV文件数据计算总和时报错

- **现象**：`sum(r[2] for r in data)`将CSV文件数据累计求和时报错。`TypeError: unsupported operand type(s) for +: 'int' and 'str'`不能把“数字”和“文字”直接相加。
- **原因**：从CSV文件读取出来的数据，默认全部都是字符串类型，不能直接和整数0相加（`sum()`从0开始累加）。
- **解决**：累计求和前显式进行类型转换`sum(int(r[2]) for r in data)`。

### CSV写入做了转义，读取却没做（对称性）

- **现象**：写CSV时用了`csv.writer`，因为它会自动处理字段里的逗号、引号。读取时却用`line.split(",")`手工切分，如果某个字符串包含英文逗号，可能导致列错位。
- **原因**：CSV的引号转义是一对成对的行为。写入时，含逗号的字段会被加上引号，如`"a,b",123`；读取时必须按同样规则把引号去掉、还原成一个字段。只在一端转义、另一端手工切分，含逗号的字段会直接错列，而且不报错。
- **解决**：读写用同一套工具。写用`csv.writer`，读就用`csv.reader`。

### 文件对象本身就是可迭代的

- **现象**：逐行读文件，不需要`while True:`+`f.readline()`。
- **原因**：文件对象本身就是可迭代的，迭代时每次产出一行。Python中凡是“能一行一行遍历”的东西，都支持for循环遍历它。
- **解决**：直接for循环遍历文件对象即可`for line in f:`。