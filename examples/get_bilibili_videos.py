import requests
import json
import subprocess

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

def get_video_url(bvid, cid, quality=32):
    api_url = 'https://api.bilibili.com/x/player/playurl'
    params = {
        'bvid': bvid,
        'cid': cid,
        'qn': quality,
        'fnval': 1,
        'fnver': 0,
        'fourk': 1
    }
    cookies = {'SESSDATA': SESSDATA}
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(api_url, params=params, cookies=cookies, headers=headers)
    data = response.json()
    return data['data']['durl'][0]['backup_url'][0]

def get_dash_urls(bvid, cid, quality=32):
    api_url = 'https://api.bilibili.com/x/player/playurl'
    params = {
        'bvid': bvid,
        'cid': cid,
        'qn': quality,
        'fnval': 16,  # 使用16表示请求DASH格式
        'fnver': 0,
        'fourk': 1
    }
    cookies = {'SESSDATA': SESSDATA}
    headers = {
        'User-Agent': 'Mozilla/5.0',  # 可以根据需要调整为APP端User-Agent
        'Referer': 'https://www.bilibili.com'
    }
    response = requests.get(api_url, params=params, cookies=cookies, headers=headers)
    data = response.json()
    video_url = data.get('data', {}).get('dash', {}).get('video', [])[0].get('baseUrl')
    audio_url = data.get('data', {}).get('dash', {}).get('audio', [])[0].get('baseUrl')
    return video_url, audio_url

def download_file(url, output_filename):
    command = ['wget', url, '--referer', 'https://www.bilibili.com', '-O', f"{output_filename}.m4a"]
    # 通过ffmpeg转成wav
    
    subprocess.run(command)
    command = ['ffmpeg', '-i', f"{output_filename}.m4a", '-ar', '16000', output_filename + '.wav']

    subprocess.run(command)

if __name__ == '__main__':
    # 【【官方双语】深度学习之神经网络的结构 Part 1 ver 2.0】 https://www.bilibili.com/video/BV1bx411M7Zx/?share_source=copy_web&vd_source=9e94008dbf76e399a164028430118348
    bvid = 'BV1bx411M7Zx'
    cid = 25368631
    audio_url = get_dash_urls(bvid, cid)[1]
    # print(json.dumps(get_dash_urls(bvid, cid), indent=4))
    # print(json.dumps(get_cid(av=bvid), indent=4))
    download_file(audio_url, bvid)