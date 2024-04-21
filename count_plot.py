import pandas as pd
import plotly.graph_objects as go

def generate_comment_count_chart():
    # 加载数据
    file_path = 'tag_data/BV1bA4m1c7F1_updated.csv'
    df = pd.read_csv(file_path)

    # 将时间戳转换为可读的日期时间格式
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

    # 对数据按时间戳排序
    df.sort_values('datetime', inplace=True)

    # 按小时进行计数
    comment_counts = df.groupby(df['datetime'].dt.floor('H')).size()

    # 计算累积评论数量
    cumulative_comment_counts = comment_counts.cumsum()

    # 生成图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=cumulative_comment_counts.index,
        y=cumulative_comment_counts.values,
        mode='lines+markers',
        name='累积评论数量',
        line=dict(color='rgba(255, 165, 0, 0.8)', width=3, shape='spline'),
        marker=dict(color='rgba(255, 165, 0, 0.8)', size=6)
    ))
    fig.update_layout(
        xaxis_title='时间',
        yaxis_title='累积评论数量',
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
