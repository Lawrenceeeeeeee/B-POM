import requests
import json
SESSDATA = 'f7d22332%2C1728481618%2Cf242a%2A41CjBLPbnBWSHKva1n24Wnxt-G4dxI7CA89KIX2tcS7zVz6VFvUVwj-hvU96ZCR68-kFESVjlsc0NOMi10ZUNpRGFNRnJyNXNHTEpLbzMzaTJSeV93aGpKRFRLUk5wRFpLdzFvcjFRZFZ6alAzLUJkZkVIUTFVMVh2WjVJV1p6eXhrVUhqelVIc3lRIIEC'

def get_cid(bv=None, av=None):
    
    api_url = 'https://api.bilibili.com/x/player/pagelist'
    if bv:
        params = {
            'bvid': bv
        }
    elif av:
        params = {
            'aid': av[2:]
        }
    else:
        raise "BV号和AV号必须至少输入一个"
    cookies = {'SESSDATA': SESSDATA}
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(api_url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        data = response.json()
        res = [item['cid'] for item in data['data']]
        return res
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None

def get_video_url(bvid, cid, quality=112):
    api_url = 'https://api.bilibili.com/x/player/playurl'
    params = {
        'bvid': bvid,
        'cid': cid,
        'qn': quality,
        'fnval': 0,
        'fnver': 0,
        'fourk': 1
    }
    cookies = {'SESSDATA': SESSDATA}
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(api_url, params=params, cookies=cookies, headers=headers)
    data = response.json()
    return data

if __name__ == '__main__':
    # 【【官方双语】深度学习之神经网络的结构 Part 1 ver 2.0】 https://www.bilibili.com/video/BV1bx411M7Zx/?share_source=copy_web&vd_source=9e94008dbf76e399a164028430118348
    bvid = 'BV1bx411M7Zx'
    cid = 25368631
    print(json.dumps(get_video_url(bvid, cid), indent=2))
    # print(json.dumps(get_cid(av=bvid), indent=4))