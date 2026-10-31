import csv

with open("repos.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)  # 创建CSV读取器
    next(reader)  # 跳过表头
    data = list(reader)  # 将剩余数据读取为列表

    total_repos = len(data)  # 计算仓库总数
    total_size = sum(int(r[2]) for r in data)  # 计算仓库总大小
    sorted_data = sorted(data, key=lambda r: r[1])  # 按创建时间排序

    print(f"共计 {total_repos} 个仓库")
    print(f"总大小 {total_size} KB")
    for r in sorted_data:
        print(f"{r[1]} {r[0]} {r[2]}")
