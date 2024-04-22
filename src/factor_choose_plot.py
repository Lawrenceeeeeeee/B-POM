import numpy as np
import pandas as pd
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from scipy.linalg import eigh

def perform_factor_analysis_and_plot_scree(bvid, comments):
    """
    Perform factor analysis on specified columns of a dataset and plot a scree plot of the eigenvalues.
    
    Parameters:
        data_path (str): Path to the CSV file containing the data.
        columns_to_analyze (list): List of column names to include in the factor analysis.
    """
    # 加载数据
    data = comments

    columns_to_analyze = ['correlation_score', 'qingxu_score', 'manyi_score', 'taolun_score', 'tiwen_score', 'wangeng_score']
    # 数据标准化
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[columns_to_analyze])

    # 计算协方差矩阵的特征值
    cov_matrix = np.cov(data_scaled, rowvar=False)
    eigenvalues, _ = eigh(cov_matrix)

    # 绘制碎石图
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, len(eigenvalues) + 1), eigenvalues[::-1], 'o-')
    plt.title('Scree Plot')
    plt.xlabel('Factor Number')
    plt.ylabel('Eigenvalue')
    plt.grid(True)
    plot_path = f'data/{bvid}_factor_choose_plot.png'
    plt.savefig(plot_path)
    plt.close()  # 关闭图形，防止内存占用过高
    return plot_path
# # 示例用法
# data_path = 'comments.csv'
# columns_to_analyze = ['correlation_score', 'qingxu_score', 'manyi_score', 'taolun_score', 'tiwen_score', 'wangeng_score']
# perform_factor_analysis_and_plot_scree(data_path, columns_to_analyze)
