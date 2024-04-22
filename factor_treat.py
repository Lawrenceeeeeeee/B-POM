import pandas as pd
import numpy as np
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

# 加载数据
data = pd.read_csv('comments.csv')

# 选择用于因子分析的列
columns_to_analyze = ['correlation_score', 'qingxu_score', 'manyi_score', 'taolun_score', 'tiwen_score', 'wangeng_score']

# 标准化数据
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[columns_to_analyze])

# 创建因子分析对象，指定提取2个因子
fa = FactorAnalysis(n_components=2)
fa.fit(data_scaled)

# 获取因子载荷矩阵
loadings = fa.components_.T  # 转置矩阵，使其更易读

# 创建载荷矩阵的DataFrame，以便更好的展示和理解
loadings_df = pd.DataFrame(loadings, index=columns_to_analyze, columns=['Factor 1', 'Factor 2'])

# 打印因子载荷矩阵
print("Factor Loadings:\n", loadings_df)
