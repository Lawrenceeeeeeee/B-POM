import requests
import json
import subprocess
import os
import transcribe as tr
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

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
    command = ['wget', url, '--referer', 'https://www.bilibili.com', '-O', f"temp/{output_filename}.m4a"]
    # 通过ffmpeg转成wav
    
    subprocess.run(command)
    command = ['ffmpeg', '-i', f"./temp/{output_filename}.m4a", '-ar', '16000', f'./temp/{output_filename}.wav']
    

    subprocess.run(command)
    os.remove(f"temp/{output_filename}.m4a")
    
def summarize(text, model="gpt-4-turbo"):
    system_prompt = """
    你现在是一个AI总结概括小助手，专门对视频的内容进行总结。用户会传入视频的自动生成字幕的内容（包含每个字幕的时间戳，每一行字幕结构为："[timestamp] subtitle"），你要做的任务是：
     - 先对整个视频的主要内容进行概括，将字数控制在100字以内
     - 然后根据视频内容，将视频划分成几个大部分（如果视频太短就不需要分太多），并对每一个部分进行简要概括，每一个部分的概括不超过50字
     
     输出参考如下：
     ```
     {
            "summary": "这是一段科普视频，讲解了……（100字以内）",
            "parts": [
                "这是第一部分……（50字以内）",
                "这是第二部分……（50字以内）",
                "这是结尾……（50字以内）",
                ……
            ]
     }
     ```
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
    )
    res = response.choices[0].message.content
    return res

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    original_cwd = os.getcwd()
    # 更改工作目录到函数所在文件目录
    os.chdir(current_dir)
    
    
    bvid = 'BV11c411z7PL'
    cid = get_cid(bvid)[0]
    audio_url = get_dash_urls(bvid, cid)[1]
    # print(json.dumps(get_dash_urls(bvid, cid), indent=4))
    # print(json.dumps(get_cid(av=bvid), indent=4))
    download_file(audio_url, bvid)
    content = tr.transcribe(f"temp/{bvid}.wav")
    # print(content)
    os.remove(f"temp/{bvid}.wav")
    res = summarize(content)
    print(res)
    
    os.chdir(original_cwd)
    