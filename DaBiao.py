import pandas as pd

def get_valid_input(prompt, valid_range):
    """ 获取并验证用户输入，确保它在有效范围内 """
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            else:
                print("输入值不在有效范围内，请重新输入！")
        except ValueError:
            print("无效输入，请输入一个整数！")

def main():
    # 用户输入CSV文件名
    filename = input("请输入需要打标的CSV文件名（包括.csv扩展名）: ")
    progress_file = filename + '_progress.txt'  # 进度跟踪文件名
    updated_filename = filename.split('.csv')[0] + '_updated.csv'  # 生成的新文件名

    # 尝试加载进度文件来找到上次的索引
    try:
        with open(progress_file, 'r') as f:
            start_index = int(f.read().strip())
            print(f"上次打标进度在第 {start_index} 行，继续打标...")
    except FileNotFoundError:
        start_index = 0
        print("未找到进度文件，从头开始...")

    # 读取 CSV 文件
    df = pd.read_csv(filename)
    # 确保输出列存在
    new_columns = ['index_qingxu', 'index_manyi', 'bool_tiwen', 'bool_taolun', 'bool_wangeng']
    for col in new_columns:
        if col not in df.columns:
            df[col] = None  # 初始化新列

    # 处理每一行数据
    for index, row in df.iloc[start_index:].iterrows():
        print(f"内容: {row['content']}")
        df.at[index, 'index_qingxu'] = get_valid_input("请输入情绪分类指标 (1消极, 2中立, 3积极): ", [1, 2, 3])
        df.at[index, 'index_manyi'] = get_valid_input("请输入观众满意指标 (1不满, 2不在意, 3满意): ", [1, 2, 3])
        df.at[index, 'bool_tiwen'] = get_valid_input("这是否为提问贴 (1不属于, 2属于): ", [1, 2])
        df.at[index, 'bool_taolun'] = get_valid_input("这是否为讨论帖 (1不属于, 2属于): ", [1, 2])
        df.at[index, 'bool_wangeng'] = get_valid_input("这是否为玩梗帖 (1不属于, 2属于): ", [1, 2])
        
        # 保存当前进度和数据
        with open(progress_file, 'w') as f:
            f.write(str(index))
        df.to_csv(updated_filename, index=False)  # 实时保存更新的数据到新文件
    
    print("打标完成，所有数据已更新。")

if __name__ == "__main__":
    main()
