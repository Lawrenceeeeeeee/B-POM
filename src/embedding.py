from openai import OpenAI
import os
import json
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def embedding(text, model="text-embedding-3-large"):

    response = client.embeddings.create(
        input=text,
        model=model
    )

    return np.array(response.data[0].embedding)

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)
    return dot_product / (norm_a * norm_b)

if __name__ == "__main__":
    text = '''
    这是关于深度学习中神经网络结构的视频。视频中介绍了神经网络的基本结构和如何识别手写数字。通过讲解脑组织和层次之间的关系，帮助观众理解神经网络的运作原理。

    ### 亮点

    - 🧠 脑组织在神经网络中代表数字，不同组织负责不同数字的识别。
    - 🔍 神经网络通过不同层次间的连接解决问题，类似生物脑组织中的信息传递。
    - 🤖 神经元的质量和偏差，以及Sigmoid函数的作用在神经网络中起着重要作用。
    - 📊 手动调整神经网络的权重和偏差，能帮助理解网络如何学习和决策。
    - 📚 通过图栏的方式表达神经网络的权重和连接，简化了复杂的数学运算。
    '''
    text2 = """
    卷积神经网络，擅长图像识别；

长短期记忆网络，擅长语音识别。

神经元:一个装有数字的容器，里面的数字是 激活值 其值越大该神经元激活的程度就越大。最后一层神经元的激活值可以认为是整个神经网络认为是该输出值的可能性，激活值越大，是该值的可能性越大。

隐含层:做数字识别的具体工作。

上一层的激活值影响并决定下一层的激活值，所以神经网络的核心就是一层的激活值通过怎样的运算，算出下一层的激活值。

中间层计算特征，并组合特征然后输出到输出层，用以输出相应的预测值。
    """
    similarity = cosine_similarity(embedding(text), embedding(text2))
    print(similarity)