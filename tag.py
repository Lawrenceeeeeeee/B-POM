import csv

def validate_input(prompt, range_start, range_end):
    while True:
        user_input = input(prompt)
        if user_input.isdigit() and range_start <= int(user_input) <= range_end:
            return user_input
        else:
            print(f"输入错误，请输入一个{range_start}-{range_end}之间的整数。")

def update_csv_with_tags(input_filename, output_filename):
    progress_filename = input_filename.replace('.csv', '_progress.txt')  # 为每个输入文件设置一个进度文件
    start_row = 0
    # 尝试读取进度文件
    try:
        with open(progress_filename, 'r') as f:
            start_row = int(f.read())
    except FileNotFoundError:
        pass  # 如果文件不存在从头开始

    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader, None)  # 获取列名
        if headers:
            content_index = headers.index('content')  # 获取"content"列的索引
            headers.extend(['emotion', 'satisfaction', 'is_query', 'is_discussion', 'is_meme'])  # 添加新的列标题
        else:
            print("警告：CSV文件没有列名。")
            return

        with open(output_filename, mode='a' if start_row > 0 else 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            if start_row == 0:  # 如果从头开始，写入列标题
                writer.writerow(headers)
            
            for i, row in enumerate(reader, start=1):
                if i <= start_row:  # 跳过已经处理过的行
                    continue
                if not row or all(field.strip() == '' for field in row):  # 检查是否为空行
                    break  # 遇到空行则终止循环
                if len(row) <= content_index:
                    print("警告：发现数据不完整的行，将跳过此行。")
                    continue
                
                print(row[content_index])  # 打印出"content"列的内容
                emotion = validate_input("请输入情绪分类（1消极、2中立、3积极）: ", 1, 3)
                satisfaction = validate_input("请输入观众满意指标（1不满、2不在意、3满意）: ", 1, 3)
                is_query = validate_input("这是否为提问帖（1不是、2是）: ", 1, 2)
                is_discussion = validate_input("这是否为讨论帖（1不是、2是）: ", 1, 2)
                is_meme = validate_input("这是否为玩梗帖（1不是、2是）: ", 1, 2)
                row.extend([emotion, satisfaction, is_query, is_discussion, is_meme])
                writer.writerow(row)
                with open(progress_filename, 'w') as f:
                    f.write(str(i))

# 调用函数，需要指定输入文件、输出文件的路径
input_filename = 'data/BV1aC411G7jT.csv'
output_filename = input_filename.replace('.csv', '_updated.csv')
update_csv_with_tags(input_filename, output_filename)
