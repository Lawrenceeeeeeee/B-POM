import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

def create_heatmap_plotly(comments):
    # 加载数据并处理时间
    data = comments
    data['datetime'] = pd.to_datetime(data['timestamp'], unit='s')
    data['hour'] = data['datetime'].dt.strftime('%Y-%m-%d %H:00')
    
    # 创建相关性分组
    bins = np.linspace(data['correlation_score'].min(), data['correlation_score'].max(), 11)
    data['correlation_group'] = pd.cut(data['correlation_score'], bins=bins, labels=np.arange(10).astype(str))
    
    # 构建数据透视表
    pivot_table = data.pivot_table(index='correlation_group', columns='hour', aggfunc='size', fill_value=0)

    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,  # 使用原始数据
        x=pivot_table.columns,  # 时间作为x轴
        y=pivot_table.index.astype(str),  # 相关性分组作为y轴
        colorscale='Viridis',  # 使用Viridis颜色渐变方案
        zsmooth='best'  # 平滑处理
    ))

    # 更新图表布局
    fig.update_layout(
        title='相关性得分时序热力图',
        xaxis_title='日期和小时',
        yaxis_title='相关性分组',
        autosize=True,
        width=800,
        height=600
    )

    return fig

