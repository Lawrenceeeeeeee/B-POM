from src.word_freq import word_freq
from src.word_cloud import wordcloud

freq = word_freq()
def freq_out():
    a1,_= word_freq.process_text_data()
    return a1
def freq_cloud():
    _,b1= word_freq.process_text_data()
    return b1

cloud = wordcloud()
def cloud_png():
    a2= wordcloud.generate_wordcloud()
    return a2


