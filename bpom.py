from src import get_bilibili_videos, get_comments

class bpom: 
    def __init__(self, bvid):
        self.bvid = bvid
        self.summary = get_bilibili_videos.get_video_summary(self.bvid)
        
    def fetch_comments(self, sort=0, nohot=0, ps=20):
        """获取视频全部评论，存到csv，文件名为{bvid}.csv

        Args:
            sort (int, optional): _description_. Defaults to 0.
            nohot (int, optional): _description_. Defaults to 0.
            ps (int, optional): _description_. Defaults to 20.
        """
        get_comments.get_full_comments(type, self.bvid, sort, nohot, ps, sample_size=None)
        
    def correlation_score(self, comment):
        """计算单个评论与视频内容的相关性指数

        Args:
            comment (_type_): _description_

        Returns:
            _type_: _description_
        """
        parts_sum = self.summary['parts']
        return get_bilibili_videos.comment_correlation(comment, parts_sum)
    
if __name__ == "__main__":
    bvid = "BV1fz421z7x9"
    bpom = bpom(bvid)
    print(bpom.summary)
    # print(bpom.correlation_score("这个视频讲的太好了！"))