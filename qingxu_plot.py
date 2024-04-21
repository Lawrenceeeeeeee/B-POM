import gradio as gr
import pandas as pd
import plotly.graph_objects as go

def generate_emotion_chart():
    # 加载数据
    file_path = 'tag_data/BV151421Z7p9_updated.csv'
    df = pd.read_csv(file_path)

    # 映射情绪指数到 -1, 0, 1
    emotion_mapping = {1: -1, 2: 0, 3: 1}
    df['index_qingxu'] = df['index_qingxu'].map(emotion_mapping)

    # 将时间戳转换为可读的日期时间格式
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    # 对数据按日期时间排序
    df.sort_values('datetime', inplace=True)

    # 计算情绪的累积值
    df['emotion_cumsum'] = df['index_qingxu'].cumsum()

    # 生成图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['datetime'], y=df['emotion_cumsum'],
        mode='lines+markers', name='情绪变化',
        line=dict(color='rgba(30, 144, 255, 0.8)', width=3, shape='spline'),
        marker=dict(color='rgba(30, 144, 255, 0.8)', size=6)  # 标记点颜色
    ))
    fig.update_layout(
        xaxis_title='日期和时间',
        yaxis_title='累积情绪值',
        plot_bgcolor='rgba(245, 245, 245, 1)',  # 轻微灰色的背景色
        font=dict(family="Arial, sans-serif", size=16, color="#333"),
        xaxis=dict(
            showline=True, linecolor='#bdbdbd',  # x轴边框线
            showgrid=True, gridcolor='#bdbdbd'   # x轴网格线
        ),
        yaxis=dict(
            showline=True, linecolor='#bdbdbd',  # y轴边框线
            showgrid=True, gridcolor='#bdbdbd'   # y轴网格线
        )
    )

    return fig

