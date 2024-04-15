import requests
import os
import bvav
import json
import time

app_key = "27eb53fc9058f8c3"
app_sec = "c2ed53a74eeefe3cf99fbd01d8c9c375"




bv = "BV1jt42177xt"
av = bvav.bv2av(bv)


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
        # Print the content of the response (body)
        res = json.loads(response.text)
        comments = [item['content']['message'] for item in res['data']['replies']] if res['data']['replies'] else []
        
        # print(json.dumps(res, indent=4))
        # print(response.text)
        # print(comments)
        return comments
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None
        
page = 1
comment_list = []
while True:
    res = get_comments('1', av, 0, 0, 20, page)
    if not res:
        break
    comment_list += res
    page += 1
    # time.sleep(1)
    
print(comment_list)
print(len(comment_list))


# print(get_comments('1', av, 0, 0, 20, 1))
