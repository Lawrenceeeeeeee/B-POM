import csv

def validate_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit() and 1 <= int(user_input) <= 5:
            return user_input
        else:
            print("输入错误，请输入一个1-5之间的整数。")

def update_csv_with_emotions(input_filename, output_filename):
    with open(input_filename, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader, None)
        with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                # 检查行是否有至少两个元素
                if len(row) < 7:
                    print("警告：发现数据不完整的行，将跳过此行。")
                    continue
                # 打印出每一行的文本内容（第二列）
                print(row[6])
                positive_negative = validate_input("请输入一个1-5之间的整数表示正面或负面情感: ")
                rational_irrational = validate_input("请输入一个1-5之间的整数表示理性或非理性情感: ")
                row.extend([positive_negative, rational_irrational])
                writer.writerow(row)
# 调用函数，需要指定输入文件和输出文件的路径
input_filename = 'BV1bc411f7fK.csv'
output_filename = input_filename.replace('.csv', '_updated.csv')
update_csv_with_emotions(input_filename, output_filename)

