import os
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager

class wordcloud:
    def __init__(self, data_dir='data/wordclouds'):
        # 创建词云图保存的目录
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        # 获取系统中可用的中文字体路径
        self.font = self.get_chinese_font()

    def get_chinese_font(self):
        """识别并返回系统中可用的最佳中文字体路径。"""
        for font in FontManager().ttflist:
            if 'Heiti' in font.name or 'Song' in font.name or 'PingFang' in font.name:
                return font.fname  # 返回字体文件的完整路径
        # 如果未找到上述字体，返回一个默认的中文字体路径
        return '/System/Library/Fonts/PingFang.ttc'

    def generate_wordcloud(self, frequency_csv, image_file='wordcloud.png'):
        # 从指定路径读取词频数据文件
        freq_path = os.path.join('data/word_frequencies', frequency_csv)
        freq_data = pd.read_csv(freq_path)
        # 将词频数据转换为字典格式，用于生成词云
        word_freq = dict(zip(freq_data['Word'], freq_data['Frequency']))

        # 创建WordCloud对象，指定字体路径、宽高和背景颜色
        wordcloud = WordCloud(width=800, height=600, font_path=self.font, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # 不显示坐标轴
        
        # 保存生成的词云图像到指定路径
        image_path = os.path.join(self.data_dir, image_file)
        plt.savefig(image_path)
        plt.close()
        return image_path



