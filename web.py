import gradio as gr

from simulate import generate_image

def wrapper_function(bv):
    image_path = generate_image(bv)
    return image_path

#/* CSS 更新，添加 Markdown 自定义样式 */#
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

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
    transition: background-color 0.3s; /* 平滑过渡效果 */
}

h1, h2 {
    text-align: center;
    color: #4CAF50;
}

"""

with gr.Blocks(css=css) as web:
    with gr.Row():
        gr.Markdown("## 基于评论情感判断的舆情监测系统")
    with gr.Row():
        gr.Markdown("介绍")
    with gr.Row():
        gr.Markdown("本系统基于用户评论情感判断进行舆情监测，期望营造更好的网络氛围")
    with gr.Row():
        gr.Markdown("包含舆情热度监控、情感变化监控、用户画像等功能")
    with gr.Row():
        gr.Markdown("系统使用爬虫技术获取评论数据，利用文本分析方法进行情感分析")
    with gr.Row():
        gr.Markdown("利用聚类分析等方法绘制简单的用户画像、识别水军")
    with gr.Row():
        gr.Markdown("开发不易，希望大家多多支持！")
    with gr.Column():
        input_bv = gr.Textbox(label="请输入视频的BV值")
        output_image = gr.Image(label="时序图跟踪")
        submit_button = gr.Button("提交")
        submit_button.click(wrapper_function, inputs=input_bv, outputs=output_image)

web.launch()
