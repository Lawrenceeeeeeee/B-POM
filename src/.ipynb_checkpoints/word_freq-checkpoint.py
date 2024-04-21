import os
import pandas as pd
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontManager

class word_freq:
    def __init__(self, bvid, comments, data_dir='data'):
        self.bvid = bvid
        self.comments = comments
        self.crawler_dir = os.path.join(data_dir, 'crawler')
        self.freq_dir = os.path.join(data_dir, 'word_frequencies')
        self.plot_dir = os.path.join(data_dir, 'frequency_plots')
        os.makedirs(self.freq_dir, exist_ok=True)
        os.makedirs(self.plot_dir, exist_ok=True)
        self.font = self.get_chinese_font()

        self.stopwords_path = os.path.join(data_dir, 'resources/cn_stopwords.txt')

    def get_chinese_font(self):
        """Identify the best available Chinese font."""
        fm = FontManager()
        for font in fm.ttflist:
            if 'Heiti' in font.name or 'Song' in font.name or 'PingFang' in font.name:
                return font.name
        return 'SimHei'  # Default to SimHei if no preferred font is found

    def process_text_data(self):
        # input_path = os.path.join(self.crawler_dir, input_csv)
        # df = pd.read_csv(input_path)
        df = self.comments
        with open(self.stopwords_path, 'r', encoding='utf-8') as file:
            stopwords = set(file.read().splitlines())
        
        df['content_cleaned'] = df['content'].apply(lambda x: x.replace(" ", "").replace("\t", "").replace("\n", ""))
        df['words'] = df['content_cleaned'].apply(lambda x: list(jieba.cut(x)))
        df['words_filtered'] = df['words'].apply(lambda x: [word for word in x if word not in stopwords])
        all_words = [word for sublist in df['words_filtered'] for word in sublist]
        word_freq = Counter(all_words)
        
        # output_path = os.path.join(self.freq_dir, output_csv)
        df_word_freq = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
        df_word_freq.sort_values('Frequency', ascending=False, inplace=True)
        # df_word_freq.to_csv(output_path, index=False)

        # Generate frequency plot
        plt.rcParams['font.sans-serif'] = [self.font]  # Use identified Chinese font
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(dpi=200)
        top_words = df_word_freq.head(10)
        ax.bar(top_words['Word'], top_words['Frequency'])
        ax.set_xlabel('词语')
        ax.set_ylabel('频次')
        ax.set_title('Top 10 Words Frequency')
        plt.xticks(rotation=45)
        plt_path = os.path.join(self.plot_dir, f'{self.bvid}_freq_plot.png')
        plt.savefig(plt_path)
        plt.close()
        return df_word_freq, plt_path



