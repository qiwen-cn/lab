# 踩坑笔记

## 文本文件字频统计
问题：读取文件中的文本时`open("test.txt").read()`，报Unicode解码错误`UnicodeDecodeError`。
原因：编码不匹配。文件是用UTF-8格式存的，但是Windows系统默认拿GBK字典去翻译它。
解决：设置utf-8编码`open("test.txt", encoding="utf-8").read()`。

问题：在字典`count`中没有键`ch`时，通过`count[ch] += 1`报`KeyError`键错误。
原因：Python的字典不会给新键自动初始化。
解决：改成`count[ch] = count.get(ch, 0) + 1`，在键`ch`不存在时用默认值`0`。

问题：统计字频时，也统计了标点、换行等符号。
原因：没有过滤标点、换行等符号。
解决：只统计字母和数字`if ch.isalnum():`。

问题：字典排序后`count = sorted(count, key=lambda x: count[x], reverse=True)`，无法再通过`count[ch]`获取值。
原因：`sorted()`将原字典排序后转换成了列表。
解决：排序时先将原字典转换成一对一对（元组）的列表`items = sorted(count.items(), key=lambda x: x[1], reverse=True)`。