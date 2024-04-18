import os
import pandas as pd

def merge_csv_files(directory_path, output_filename):
    """合并目录下的所有CSV文件到一个新的CSV文件中，保留第一个文件的列标题。"""
    files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
    combined_df = pd.DataFrame()

    for index, file in enumerate(files):
        file_path = os.path.join(directory_path, file)
        df = pd.read_csv(file_path)

        # 如果是第一个文件，初始化combined_df数据帧以包含列标题
        if index == 0:
            combined_df = df
        else:
            # 忽略后续文件的列标题
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # 保存到新的CSV文件
    combined_df.to_csv(output_filename, index=False)
    print(f"All CSV files have been merged into {output_filename}")

if __name__ == "__main__":
    directory_path = input("请输入包含CSV文件的文件夹路径: ")
    output_filename = input("请输入输出CSV文件的完整路径: ")
    merge_csv_files(directory_path, output_filename)
