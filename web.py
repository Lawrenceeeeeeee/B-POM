import gradio as gr
import webbrowser
import os
import pandas as pd
from src.qingxu_plot import generate_emotion_chart
from src.count_plot  import generate_comment_count_chart
from src.corr_plot import create_heatmap_plotly
from bpom import bpom

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


def bpom_start(bvid):
    client = bpom(bvid)
    print('start run')
    client.run()
    
    return client.freq_plot, client.word_cloud_plot, client.correlation_plot(), client.Count_plot(), client.emotion_plot(), client.Manyi_plot(), client.Factor_plot(), client.Cluster_plot()
    

with gr.Blocks(theme=gr.themes.Soft()) as web:
    
    with gr.Column():
        gr.Markdown("<!-- 这是一个空行 -->")
        gr.Markdown("# 基于评论情感判断的舆情监测系统")
    gr.Markdown("<!-- 这是一个空行 -->")
    gr.Markdown("<!-- 这是一个空行 -->")
    with gr.Column():
        
        with gr.Column():
            output1 = gr.Plot(label="word_freq")
            output2 = gr.Image(label="word_cloud")
            output3 = gr.Plot(label="corr")
            output4 = gr.Plot(label="count")
            output5 = gr.Plot(label="emotion")
            output6 = gr.Plot(label="content")
            output7 = gr.Image(label="factor_choose_plot")
            output8 = gr.Image(label="cluster")
            
        with gr.Row():
            input_bv = gr.Textbox(label="请输入视频的BV号")
            recom_button1 = gr.Button(value="项目介绍")
            recom_button1.click(open_readme_in_github)
            recom_button2 = gr.Button(value="开始爬取")
            recom_button2.click(fn=bpom_start, inputs=input_bv, outputs=[output1, output2, output3, output4, output5, output6, output7, output8])

        
    crawl_result = gr.Textbox(label="爬取结果", interactive=False)
 
web.launch(server_port=6006)