import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

def create_heatmap_plotly():
    # 加载数据
    data = pd.read_csv('tag_data/comments.csv')
    data['datetime'] = pd.to_datetime(data['timestamp'], unit='s')
    data['hour'] = data['datetime'].dt.strftime('%Y-%m-%d %H')
    
    # 创建相关性分组
    bins = np.linspace(data['correlation_score'].min(), data['correlation_score'].max(), 11)
    data['correlation_group'] = pd.cut(data['correlation_score'], bins=bins, labels=np.arange(10).astype(str))
    pivot_table = data.pivot_table(index='hour', columns='correlation_group', aggfunc='size', fill_value=0)
    
    # 计算频率
    row_sums = pivot_table.sum(axis=1)  # 每个小时的总频数
    frequency_table = pivot_table.div(row_sums, axis=0)  # 计算频率

    # 准备插值的坐标和值
    y = np.arange(len(frequency_table.index))
    x = np.arange(len(frequency_table.columns))
    X, Y = np.meshgrid(x, y)
    Z = frequency_table.values

    # 插值
    x_new = np.linspace(0, len(x) - 1, 300)  # 更密集的x坐标
    y_new = np.linspace(0, len(y) - 1, 300)  # 更密集的y坐标
    X_new, Y_new = np.meshgrid(x_new, y_new)
    Z_new = griddata((X.flatten(), Y.flatten()), Z.flatten(), (X_new, Y_new), method='cubic')

    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=Z_new,
        x=frequency_table.index,
        y=frequency_table.columns.astype(str),  # 使用字符串类型的列名
        colorscale='Viridis'
    ))

    # 更新布局以清楚显示坐标轴
    fig.update_layout(
        title='Heatmap of Correlation Scores by Hour',
        xaxis_title='Date and Hour',
        yaxis_title='Correlation Group',
        autosize=True,
        width=800,
        height=600
    )

    return fig

