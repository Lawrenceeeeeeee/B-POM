import requests
import os
import bvav
import json
import time
import pandas as pd

app_key = "27eb53fc9058f8c3"
app_sec = "c2ed53a74eeefe3cf99fbd01d8c9c375"




bv = "BV1bc411f7fK"
av = bvav.bv2av(bv)

columns = ['timestamp', 'uid', 'uname', 'content', 'likes', 'replies']

def get_comments(type, oid, sort=0, nohot=0, ps=20, pn=1):
    
    """获取b站视频评论

    Args:
        type (_type_): _description_
        oid (_type_): _description_
        sort (int, optional): _description_. Defaults to 0.
        nohot (int, optional): _description_. Defaults to 0.
        ps (int, optional): _description_. Defaults to 20.
        pn (int, optional): _description_. Defaults to 1.
    """
    
    url = "https://api.bilibili.com/x/v2/reply"
    SESSDATA = 'f7d22332%2C1728481618%2Cf242a%2A41CjBLPbnBWSHKva1n24Wnxt-G4dxI7CA89KIX2tcS7zVz6VFvUVwj-hvU96ZCR68-kFESVjlsc0NOMi10ZUNpRGFNRnJyNXNHTEpLbzMzaTJSeV93aGpKRFRLUk5wRFpLdzFvcjFRZFZ6alAzLUJkZkVIUTFVMVh2WjVJV1p6eXhrVUhqelVIc3lRIIEC'
    
    params = {
        "type": type,
        "oid": oid,
        "sort": sort,
        "nohot": nohot,
        "ps": ps,
        "pn": pn,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": f"https://www.bilibili.com/video/av{oid}",
    }
    cookies = {
        "SESSDATA": SESSDATA,
    }
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    
    # Check if the request was successful
    if response.status_code == 200:
        df = pd.DataFrame(columns=columns)
        # Print the content of the response (body)
        results = json.loads(response.text)
        for result in results['data']['replies']:
            new_row = {
                'timestamp': result['ctime'],
                'uid': result['mid'],
                'uname': result['member']['uname'],
                'content': result['content']['message'],
                'likes': result['like'],
                'replies': result['count'],
            }
            new_row = pd.DataFrame(new_row, index=[0])
            df = pd.concat([df, new_row], ignore_index=True)
            
        # comments = [item['content']['message'] for item in res['data']['replies']] if res['data']['replies'] else []
        
        # print(json.dumps(res, indent=4))
        # with open('output.txt', 'a') as f:
        #     f.write(json.dumps(res, indent=4))
        # print(response.text)
        # print(comments)
        return df
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None
        
def get_full_comments(type, oid, sort=0, nohot=0, ps=20):
    """获取指定b站视频所有评论

    Args:
        type (_type_): 评论区类型代码
        oid (_type_): 视频av号
        sort (int, optional): 排序方式，默认为0。0：按时间；1：按点赞数；2：按回复数.
        nohot (int, optional): 是否不显示热评. 默认为0.
        ps (int, optional): 每页项数（1-20）. Defaults to 20.

    Returns:
        _type_: _description_
    
    ## 评论区类型代码
        
    （PS：以下部分内容来源不明，有待验证）

    | 代码 | 评论区类型              | oid 的意义  |
    | ---- | ----------------------- | ----------- |
    | 1    | 视频稿件                | 稿件 avid   |
    | 2    | 话题                    | 话题 id     |
    | 4    | 活动                    | 活动 id     |
    | 5    | 小视频                  | 小视频 id   |
    | 6    | 小黑屋封禁信息          | 封禁公示 id |
    | 7    | 公告信息                | 公告 id     |
    | 8    | 直播活动                | 直播间 id   |
    | 9    | 活动稿件                | (?)         |
    | 10   | 直播公告                | (?)         |
    | 11   | 相簿（图片动态）        | 相簿 id     |
    | 12   | 专栏                    | 专栏 cvid   |
    | 13   | 票务                    | (?)         |
    | 14   | 音频                    | 音频 auid   |
    | 15   | 风纪委员会              | 众裁项目 id |
    | 16   | 点评                    | (?)         |
    | 17   | 动态（纯文字动态&分享） | 动态 id     |
    | 18   | 播单                    | (?)         |
    | 19   | 音乐播单                | (?)         |
    | 20   | 漫画                    | (?)         |
    | 21   | 漫画                    | (?)         |
    | 22   | 漫画                    | 漫画 mcid   |
    | 33   | 课程                    | 课程 epid   |
    """
    page = 1
    # comment_list = []
    # 时间戳、用户id、用户名、评论内容、点赞数、回复数
    df = pd.DataFrame(columns=columns)
    
    while True:
        res = get_comments(type, oid, sort, nohot, ps, page)
        if res.empty:
            break
        df = pd.concat([df, res], ignore_index=True)
        page += 1
        # time.sleep(1) # 如果被ban了就取消这个注释
    
    with open('BV1bc411f7fK.csv', 'a') as f:
        df.to_csv(f, header=True, encoding='utf-8')
        
        
    return df



    
print(get_full_comments('1', av, 0, 0, 20).head())
# print(len(comment_list))


# print(get_comments('1', av, 0, 0, 20, 1))
