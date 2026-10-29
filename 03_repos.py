import requests  # 需要安装requests库
import csv

# 向GitHub公开API发起GET请求（超时时间为10秒），获取用户qiwen-cn的公开仓库列表（返回Response对象，包含状态码、响应头、响应正文等信息）
repos = requests.get("https://api.github.com/users/qiwen-cn/repos", timeout=10)

# 确认请求成功（状态码为200表示成功）
print("状态码:", repos.status_code)
if repos.status_code != 200:
    print("请求失败:", repos.text)
    exit()

# 将响应正文按JSON解析成Python列表，每个元素是一个仓库字典
repo_list = repos.json()

# 将仓库信息写入CSV文件，使用带BOM的UTF-8，禁止Python自动转换换行符
with open("repos.csv", "w", encoding="utf-8-sig", newline="") as f:
    # 创建CSV写入器
    writer = csv.writer(f)
    # 写入表头
    writer.writerow(["仓库名称", "创建时间", "仓库大小(KB)"])

    # 遍历每个仓库字典
    for r in repo_list:
        name = r["name"]  # 仓库名称
        created_at = r["created_at"]  # 仓库创建时间
        size = r["size"]  # 仓库大小

        # 写入每个仓库的信息
        writer.writerow([name, created_at, size])
