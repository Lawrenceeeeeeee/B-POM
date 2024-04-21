import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager

class word_cloud:
    def __init__(self, bvid, word_freq, data_dir='data/wordclouds'):
        self.bvid = bvid
        self.word_freq = word_freq
        # 创建词云图保存的目录
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        # 获取系统中可用的中文字体路径
        # self.font = self.get_chinese_font()
        self.font = "/root/autodl-tmp/BERT/data/fonts/STHeiti_Light.ttc"
        # print(os.path.exists(self.font)) 

    def generate_wordcloud(self):
        # 从指定路径读取词频数据文件
        # freq_path = os.path.join('data/word_frequencies', frequency_csv)
        freq_data = self.word_freq
        # 将词频数据转换为字典格式，用于生成词云
        word_freq = dict(zip(freq_data['Word'], freq_data['Frequency']))

        # 创建WordCloud对象，指定字体路径、宽高和背景颜色
        wordcloud = WordCloud(width=800, height=600, font_path=self.font, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # 不显示坐标轴
        
        # 保存生成的词云图像到指定路径
        image_path = os.path.join(self.data_dir, f'{self.bvid}_wordcloud.png')
        plt.savefig(image_path)
        plt.close()
        return image_path



