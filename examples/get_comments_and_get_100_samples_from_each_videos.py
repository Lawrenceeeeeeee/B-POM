import sys
sys.path.append('/Users/lawrence/Desktop/CUFE/大二下/大数据与金融/NLP/')

from src import get_comments as gc
from src import videos


for video in videos.video_list:
    gc.get_full_comments(1, video, sample_size=100)
    print("Got 100 samples from video " + video + ".")