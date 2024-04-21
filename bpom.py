from src import get_bilibili_videos, get_comments, bvav, embedding
from src.BertExecer import ModelInferer
from src.word_freq import word_freq


class bpom: 
    def __init__(self, bvid):
        self.bvid = bvid
        self.oid = str(bvav.bv2av(bvid))
        self.comments = self.fetch_comments()
        
        self.wf = word_freq(self.bvid, self.comments)
        self.comment_word_freq, self.freq_plot = self.wf.process_text_data()

        print("# 词频统计")
        print(self.comment_word_freq.head())

        print("--------------------------")
        print("# 评论示例")
        print(self.comments.head())
        # self.summary = get_bilibili_videos.get_video_summary(self.bvid)
        # self.embedded_summary = [embedding.embedding(item) for item in self.summary['parts']]
        
        
    def fetch_comments(self):
        """获取视频全部评论，存到csv，文件名为{bvid}.csv

        Args:
            sort (int, optional): _description_. Defaults to 0.
            nohot (int, optional): _description_. Defaults to 0.
            ps (int, optional): _description_. Defaults to 20.
        """
        comments = get_comments.get_full_comments('1', self.bvid, sample_size=100)
        return comments
        
    def correlation_score(self, comment):
        """计算单个评论与视频内容的相关性指数

        Args:
            comment (_type_): _description_

        Returns:
            _type_: _description_
        """
        comment_vec = embedding.embedding(comment)
        parts_sum = self.summary['parts']
        return get_bilibili_videos.comment_correlation(comment_vec, self.embedded_summary)
    
    def word_freq(self):
        pass

    def run(self):
        if 'content' in self.comments.columns:
            self.comments['correlation_score'] = self.comments['content'].apply(self.correlation_score)
            inferer = ModelInferer()
            for key in inferer.models.keys():
                self.comments[key + '_score'] = self.comments['content'].apply(lambda x: inferer.predict(x, key))
        else:
            print("Content column is missing in the comments DataFrame.") 
        print(self.comments.head())
        # with open(f"{self.bvid}.csv", "r") as f:
        #     comments = f.readlines()
        
        
    
if __name__ == "__main__":
    bvid = "BV1uz421X7e1"
    b = bpom(bvid)
    print(b.summary)
    print(b.comments)
    # print(bpom.correlation_score("这个视频讲的太好了！"))