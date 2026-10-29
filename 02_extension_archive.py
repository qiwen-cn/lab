from pathlib import Path

# 基础路径
base_path = Path("D:\\workspace\\code\\lab\\test_folder")

# 遍历路径下所有文件或文件夹，使用list()避免迭代器在移动文件时被破坏
for file in list(base_path.iterdir()):

    # 必须是文件，且有后缀名
    if file.is_file() and file.suffix:

        # 获取纯扩展名
        ext_name = file.suffix[1:]

        # 拼接目标文件夹路径
        target_dir = base_path / ext_name

        # 创建文件夹（exist_ok=True如果已存在直接跳过创建）
        target_dir.mkdir(exist_ok=True)

        # 拼接目标文件路径
        target_file = target_dir / file.name

        # 移动文件，如果目标文件夹已存在同名文件则跳过
        if target_file.exists():
            print(f"跳过{file.name}，{ext_name}/里已有同名文件")
        else:
            file.replace(target_file)
            print(f"已将{file.name}移动到{ext_name}/")
