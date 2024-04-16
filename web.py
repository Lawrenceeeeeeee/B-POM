import gradio as gr
import webbrowser
import os
import pandas as pd
from examples.simulate import generate_image

# CSV 文件路径
csv_file = 'data.csv'

# 如果文件不存在，创建文件并添加列名
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=['BV', 'Record'])
    df.to_csv(csv_file, index=False)

def write_to_csv(bv, record):
    # 加载现有的 CSV 文件
    df = pd.read_csv(csv_file)
    # 添加新的数据行
    df = df.append({'BV': bv, 'Record': record}, ignore_index=True)
    # 保存更新后的 CSV 文件
    df.to_csv(csv_file, index=False)
    return "数据已写入!"

def wrapper_function(bv):
    image_path = generate_image(bv)
    return image_path

def open_readme_in_browser():
    # 设置 README 文件的名称
    filename = "README.md"
    # 获取当前工作目录的路径
    current_directory = os.getcwd()
    # 构造完整的文件路径
    full_path = os.path.join(current_directory, filename)
    
    # 检查文件是否存在
    if os.path.exists(full_path):
        # 使用默认浏览器打开文件
        webbrowser.open(f"file://{full_path}")
    else:
        pass

    

css = """
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
body {
    font-family: 'Arial', sans-serif;   /* 设置默认字体 */
    background-color: #d3d3d3;          /* 页面背景颜色 */
    color: #333;                        /* 文本颜色 */
    padding: 20px;                      /* 页面内边距 */
}
.markdown, p {
    font-family: 'Pacifico', cursive; /* 更圆润的字体 */
    text-align: center; /* 文本居中 */
    font-size: 16px; /* 字体大小 */
    color: #4CAF50; /* 字体颜色，可以根据需要调整 */
    line-height: 1.4; /* 行间距,1.2 表示行高是字体大小的1.4倍 */
}
input, textarea, button {
    width: 90%; /* 调整宽度以适当居中 */
    margin-bottom: 10px; /* 增加底部边距以分隔组件 */
    text-align: center; /* 文本居中 */
}
.button-small {
    height: 40px;
    font-size: 14px;
    width: 150px;
    background-color: lightblue; /* 示例背景色 */
}
.markdown h1 {  /* 这里假设 Markdown 中使用了一级标题 */
    font-size: 42px;  /* 调整字体大小 */
}
h1, h2 {
    text-align: center;
    color: #4CAF50;
}
"""

with gr.Blocks(css=css,theme=gr.themes.Soft()) as web:
    
    with gr.Column():
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("# 基于评论情感判断的舆情监测系统")
    gr.Markdown("<!-- 这是一个空行 -->")
    gr.Markdown("<!-- 这是一个空行 -->")
    with gr.Row():
        with gr.Column(scale=1):
            recom_button1 = gr.Button(value="项目介绍")
            recom_button1.click(open_readme_in_browser)
            recom_button2 = gr.Button(value="使用说明")
        with gr.Column(scale=30):
            input_bv = gr.Textbox(label="请输入视频的BV值")
        
    with gr.Column():
        
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("## 词语的统计描述")
        with gr.Row():
            with gr.Column():
                with gr.Column():
                    output_img1 = gr.Image(label="词频统计")
                    submit_button1 = gr.Button("词频分析")
                    # submit_button1.click()
            with gr.Column():
                with gr.Column():
                    output_img2 = gr.Image(label="词云统计")
                    submit_button2 = gr.Button("词云展示")
                    # submit_button2.click()
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("## 舆情变化时序统计")
        
        with gr.Column():
            output_img3 = gr.Image(label="评论数量时序分析")
            submit_button3 = gr.Button("分析")
            # submit_button3.click()
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("<!-- 这是一个空行 -->")
        with gr.Column():
            output_img4 = gr.Image(label="评论情感时序分析")
            submit_button4 = gr.Button("分析")
            # submit_button4.click()
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("<!-- 这是一个空行 -->")
        with gr.Column():
            output_img5 = gr.Image(label="评论理智程度时序分析")
            submit_button5 = gr.Button("分析")
            # submit_button5.click()
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("## 用户评论特征")
        
        with gr.Column():
            output_img6 = gr.Image(label="用户评论特征")
            submit_button6 = gr.Button("生成")
            # submit_button6.click()
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("## 记录")
        with gr.Column():
            input_txt = gr.Textbox(label="监测者记录")
            submit_button7 = gr.Button("写入")
            submit_button7.click(write_to_csv, inputs=[input_bv, input_txt], outputs=[])
web.launch()