import pandas as pd
from colorama import Fore, Style
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def gpt_tagger(text):
    system_prompt = """
    你现在是一个机器学习助手。我们小组希望对视频评论进行分类，打Tag。Tag的规则如下
    第一类：情绪分类指标（1-3）【1是消极、2是中立、3是积极】

        其中，这个指标只基于评论自己的情感色彩，与视频内容无关；提问帖讨论帖这些无明显情感倾向的均为中立。

    第二类：观众满意指标（1-3）【1是不满、2是不在意、3是满意】

        其中，出现玩梗、刷沙发这类的评论，一律按照不在意考虑。

    第三类：是否为提问贴（1，2）【1是不属于，2是属于】

    第四类：是否为讨论帖（1，2）【1是不属于，2是属于】

    第五类：是否为玩梗帖（1，2）【1是不属于，2是属于】
    
    -------------------
    用户会提供一条评论，你需要根据这条评论的内容，按照上面的类别顺序输出json格式的列表(只输出json的list！不要输出任何不相关的文字内容），格式如下：
    ```
    [2, 3, 1, 2, 1]
    ```
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "我也心动了，计划中"},
            {"role": "assistant", "content": "[3, 3, 1, 1, 1]"},
            {"role": "user", "content": "已经被游戏官方骗麻了，幽默下载就送60抽，预约抽卡上线即活动结束，一堆人之前抽半天，结果后面没领上，看后续官方怎么说，大不了还是玩端游，手游很多地方又卡又糊，操作体验也不行，要不是奔着IP来，都不可能看官方后续再决"},
            {"role": "assistant", "content": "[1, 1, 1, 1, 1]"},
            {"role": "user", "content": "偷偷说一嘴，虽然做的依旧很好看！！但是一直盯着长镜头难免会觉得有点疲劳..印象中已经连续看到三个长镜头视频了，只是建议！！"},
            {"role": "assistant", "content": "[2, 1, 1, 2, 1]"},
            {"role": "user", "content": text},
        ]
    )
    res = response.choices[0].message.content
    print(res)
    res = json.loads(res)
    return res

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
        print(Fore.GREEN + f"{index} 内容" + Fore.RESET + f": {row['content']}")
        res = gpt_tagger(row['content'])
        print(res)
        df.at[index, 'index_qingxu'] = res[0]
        df.at[index, 'index_manyi'] = res[1]
        df.at[index, 'bool_tiwen'] = res[2]
        df.at[index, 'bool_taolun'] = res[3]
        df.at[index, 'bool_wangeng'] = res[4]
        
        # 保存当前进度和数据
        with open(progress_file, 'w') as f:
            f.write(str(index))
        df.to_csv(updated_filename, index=False)  # 实时保存更新的数据到新文件
    
    print("打标完成，所有数据已更新。")

if __name__ == "__main__":
    main()
    # result = gpt_tagger("夜间牙齿自发疼那是急性牙髓炎啊，别拖了，治牙去吧[doge]")
    # print(result)
    # print(type(result))
