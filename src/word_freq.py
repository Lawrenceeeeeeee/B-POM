import os
import pandas as pd
import jieba
from collections import Counter
import plotly.express as px

class word_freq:
    def __init__(self, bvid, comments, data_dir='data'):
        self.bvid = bvid
        self.comments = comments
        self.crawler_dir = os.path.join(data_dir, 'crawler')
        self.freq_dir = os.path.join(data_dir, 'word_frequencies')
        self.plot_dir = os.path.join(data_dir, 'frequency_plots')
        os.makedirs(self.freq_dir, exist_ok=True)
        os.makedirs(self.plot_dir, exist_ok=True)

        self.stopwords_path = os.path.join(data_dir, 'resources/cn_stopwords.txt')

    def process_text_data(self):
        df = self.comments
        with open(self.stopwords_path, 'r', encoding='utf-8') as file:
            stopwords = set(file.read().splitlines())
        
        df['content_cleaned'] = df['content'].apply(lambda x: x.replace(" ", "").replace("\t", "").replace("\n", ""))
        df['words'] = df['content_cleaned'].apply(lambda x: list(jieba.cut(x)))
        df['words_filtered'] = df['words'].apply(lambda x: [word for word in x if word not in stopwords])
        all_words = [word for sublist in df['words_filtered'] for word in sublist]
        word_freq = Counter(all_words)

        df_word_freq = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
        df_word_freq.sort_values('Frequency', ascending=False, inplace=True)

        # Generate frequency plot with Plotly
        fig = px.bar(df_word_freq.head(10), x='Word', y='Frequency',
                     title='Top 10 Words Frequency', text='Frequency',
                     labels={'Word': '词语', 'Frequency': '频次'})
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        plt_path = os.path.join(self.plot_dir, f'{self.bvid}_freq_plot.html')
        fig.write_html(plt_path)
        return df_word_freq, plt_path