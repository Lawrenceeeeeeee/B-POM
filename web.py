import gradio as gr
import webbrowser
import os
import pandas as pd
from examples.simulate import generate_image



# 项目介绍文件的函数
def open_readme_in_github():
    # 设置 GitHub 仓库中的 README 文件的 URL
    url = "https://github.com/Lawrenceeeeeeee/big-data-finance-5-nlp/blob/main/README.md"
    
    # 使用默认浏览器打开 URL
    webbrowser.open(url)





# 记录日志的函数
def write_to_csv(bv, record):
    # 定义文件名，包括 BV 号
    filename = f'data/{bv}_records.csv'
    
    # 检查文件是否存在，不存在则创建并初始化列名
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=['BV号', 'Record'])
    else:
        # 加载现有的 CSV 文件
        df = pd.read_csv(filename)
    
    # 添加新的数据行
    df = df.append({'BV号': bv, 'Record': record}, ignore_index=True)
    # 保存更新后的 CSV 文件
    df.to_csv(filename, index=False)
    return f"数据已写入到 {filename}!"
    

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

.button-large {
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
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
            recom_button1.click(open_readme_in_github)
            recom_button2 = gr.Button(value="开始爬取")
            #recom_button2.click(fn=start_crawling, inputs=input_bv, outputs=crawl_result)

        with gr.Column(scale=30):
            input_bv = gr.Textbox(label="请输入视频的BV号")
    crawl_result = gr.Textbox(label="爬取结果", interactive=False)
                

        
    with gr.Column():
        
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("## 词语的统计描述")
        with gr.Row():
            with gr.Column():
                with gr.Column():
                    output_img1 = gr.Image(label="词频统计")
                    submit_button1 = gr.Button("词频分析")
                    #submit_button1.click(fn=frec_out,inputs=[],outputs=output_img1)
            with gr.Column():
                with gr.Column():
                    output_img2 = gr.Image(label="词云统计")
                    submit_button2 = gr.Button("词云展示")
                    #submit_button2.click(fn=frec_plt,inputs=[],outputs=output_img2)
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