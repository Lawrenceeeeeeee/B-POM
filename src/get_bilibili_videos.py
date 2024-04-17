import requests
import json
import subprocess
import os
import transcribe as tr
import embedding as emb
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
    # 获取当前函数所在文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 保存原始工作目录
    original_cwd = os.getcwd()
    # 更改工作目录到函数所在文件目录
    os.chdir(current_dir)
    command = ['wget', url, '--referer', 'https://www.bilibili.com', '-O', f"temp/{output_filename}.m4a"]
    # 通过ffmpeg转成wav
    
    subprocess.run(command)
    command = ['ffmpeg', '-i', f"./temp/{output_filename}.m4a", '-ar', '16000', f'./temp/{output_filename}.wav']
    

    subprocess.run(command)
    os.remove(f"temp/{output_filename}.m4a")
    os.chdir(current_dir)
    
def summarize(text, model="gpt-4-turbo"):
    system_prompt = """
    你现在是一个AI总结概括小助手，专门对视频的内容进行总结。用户会传入视频的自动生成字幕的内容（包含每个字幕的时间戳，每一行字幕结构为："[timestamp] subtitle"），你要做的任务是：
     - 先对整个视频的主要内容进行概括，将字数控制在100字以内
     - 然后根据视频内容，将视频划分成几个大部分（如果视频太短就不需要分太多，主打一个宁少勿多），并对每一个部分进行简要概括，每一个部分的概括不超过50字
     
     输出参考如下：
     {
            "summary": "这是一段科普视频，讲解了……（100字以内）",
            "parts": [
                "介绍了xxx……（50字以内）",
                "阐释了……（50字以内）",
                "呼吁大家……（50字以内）",
                ……
            ]
     }
    请直接输出json格式的dict，不要输出任何不相关的文字内容。即使原视频是其他语言的视频，你概括的时候也要用中文输出。
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

def get_video_summary(bvid):
    # 获取当前函数所在文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 保存原始工作目录
    original_cwd = os.getcwd()
    # 更改工作目录到函数所在文件目录
    os.chdir(current_dir)
    cid = get_cid(bvid)[0]
    audio_url = get_dash_urls(bvid, cid)[1]
    # print(json.dumps(get_dash_urls(bvid, cid), indent=4))
    # print(json.dumps(get_cid(av=bvid), indent=4))
    download_file(audio_url, bvid)
    content = tr.transcribe(f"temp/{bvid}.wav")
    # print(content)
    os.remove(f"temp/{bvid}.wav")
    res = summarize(content)
    res = json.loads(res)
    
    os.chdir(original_cwd)
    return res

def comment_correlation(comment, parts_sum):
    corr = 0
    corr = max([emb.cosine_similarity(emb.embedding(comment), emb.embedding(item)) for item in parts_sum])
    # for item in parts_sum:
    #     corr += emb.cosine_similarity(emb.embedding(comment), emb.embedding(item))
    # corr /= len(parts_sum)
    return corr
    

if __name__ == '__main__':
#     bv = 'BV17i421f7VX'
#     summary = get_video_summary(bv)
    comment = """
    在北京生活二十多年，前几天刚从杭州旅游回来，就谈谈这两个城市的区别吧（纯主观，有不同的观点那就以你为准）
首先说说景点吧，这两个城市的景点其实都是t0级别的了吧，北京人文，杭州自然。
美食就没什么好说的了，主要说说城市给人的感觉吧，北京就是经典的太大了，所以他繁华的地方是真繁华，该破的地方也是真的破。当然这也是所有一线城市的通病了，但是感觉北京尤为明显。杭州依山傍水的看着确实是舒服点，当然这也是一个北方人对南方自带的滤镜罢了（
    """
    summary = {'summary': '这是一段关于个人经历与生活选择的记录，视频主讲述了他从北京搬迁到杭州的决定及原因，展示了收拾搬家的过程，并反思了城市选择对个人生活方式的影响。', 'parts': ['第一部分：视频主介绍自己在北京的生活经历和即将搬迁到杭州的决定。', '第二部分：详细记录搬家过程中的点点滴滴，包括打包物品和处理无用物品。', '第三部分：视频主探讨北京与杭州生活环境的不同，以及这次搬迁对他个人选择的意义。', '结尾部分：思考和分享生活哲学，搬家过程结束，并表达对未来生活的展望和期待。']}
#     print(summary)
    res = comment_correlation(comment, summary['parts'])
    print(res)