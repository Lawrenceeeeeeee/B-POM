import subprocess
import os

def transcribe(video_path, output_path):
    video_file = os.path.basename(video_path)
    video_name = os.path.splitext(video_file)[0]
    # 获取当前函数所在文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 保存原始工作目录
    original_cwd = os.getcwd()
    # 更改工作目录到函数所在文件目录
    os.chdir(current_dir)
    
    output_path = "temp"
    command = ['../whisper.cpp/main', '-m', '../whisper.cpp/models/ggml-small.bin', '-f', '../' + video_path, '-of', f'temp/{video_name}', '-olrc', 'true']
    # subprocess.call(command, shell=True)
    subprocess.run(command)
    output_path = f'temp/{video_name}.lrc'
    with open(output_path, 'r', encoding='utf-8') as f:
        all_text = f.read()
    os.remove(output_path)
    os.chdir(original_cwd)
    return all_text
    
if __name__ == '__main__':
    video_path = "examples/test.wav"
    output_path = "examples/test"
    res = transcribe(video_path, output_path)
    print(res)