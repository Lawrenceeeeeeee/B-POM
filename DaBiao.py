import csv

def validate_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit() and 1 <= int(user_input) <= 5:
            return user_input
        else:
            print("输入错误，请输入一个1-5之间的整数。")

def update_csv_with_emotions(input_filename, output_filename):
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
        else:
            print("警告：CSV文件没有列名。")
            return
        with open(output_filename, mode='a' if start_row > 0 else 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for i, row in enumerate(reader, start=1):
                if i <= start_row:  # 跳过已经处理过的行
                    continue
                # 检查行是否有至少两个元素
                if len(row) <= content_index:
                    print("警告：发现数据不完整的行，将跳过此行。")
                    continue
                # 打印出"content"列的内容
                print(row[content_index])
                positive_negative = validate_input("请输入一个1-5之间的整数表示正面或负面情感: ")
                rational_irrational = validate_input("请输入一个1-5之间的整数表示理性或非理性情感: ")
                row.extend([positive_negative, rational_irrational])
                writer.writerow(row)
                # 保存进度
                with open(progress_filename, 'w') as f:
                    f.write(str(i))

# 调用函数，需要指定输入文件、输出文件的路径
input_filename = 'BV1bc411f7fK.csv'
output_filename = input_filename.replace('.csv', '_updated.csv')
update_csv_with_emotions(input_filename, output_filename)
