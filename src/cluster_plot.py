import pandas as pd
import numpy as np
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def perform_clustering(bvid, comments, n_factors=2, n_clusters=5, random_state=42):
    """
    Perform factor analysis and clustering on specified columns of data.
    
    Parameters:
        data_path (str): Path to the CSV file containing the data.
        columns_to_analyze (list): List of column names to include in the analysis.
        n_factors (int): Number of factors to extract.
        n_clusters (int): Number of clusters to form.
        random_state (int): Random state for reproducibility.
        
    Returns:
        Displays a scatter plot of the clustering results.
    """
    # 加载数据
    data = comments

    columns_to_analyze = ['correlation_score', 'qingxu_score', 'manyi_score', 'taolun_score', 'tiwen_score', 'wangeng_score']
    # 数据标准化
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data[columns_to_analyze])

    # 因子分析
    fa = FactorAnalysis(n_components=n_factors)
    data_factors = fa.fit_transform(data_scaled)

    # 转换因子分数为DataFrame
    factor_scores = pd.DataFrame(data_factors, columns=['Negative Emotion Factor', 'User Engagement Factor'])

    # 聚类分析
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(factor_scores)
    factor_scores['Cluster'] = clusters

    # 绘制聚类结果的散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Negative Emotion Factor', y='User Engagement Factor', hue='Cluster', data=factor_scores, palette='viridis', style='Cluster')
    plt.title('Clustering Results on Factor Scores')
    plt.xlabel('Negative Emotion Factor')
    plt.ylabel('User Engagement Factor')
    plot_path = f'data/{bvid}_clustering_results.png'
    plt.savefig(plot_path)
    plt.close()  # 关闭图形，防止内存占用过高
    return plot_path

# # 示例用法
# data_path = 'comments.csv'
# columns_to_analyze = ['correlation_score', 'qingxu_score', 'manyi_score', 'taolun_score', 'tiwen_score', 'wangeng_score']
# perform_clustering(data_path, columns_to_analyze)
