from PIL import Image
import numpy as np
import random

def generate_image(seed):
    # 使用输入的seed初始化随机数生成器
    random.seed(int(seed))
    
    # 生成一个随机颜色的数组，形状为256x256，每个像素RGB三通道
    data = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)
    
    # 将数组转换为图像
    image = Image.fromarray(data, 'RGB')
    
    # 构建文件路径
    file_path = f"random_image_{seed}.png"
    
    # 保存图像到磁盘
    image.save(file_path)
    
    # 返回保存的图片文件路径
    return file_path

# 调用函数测试
if __name__ == "__main__":
    seed_input = input("Enter a seed number: ")
    image_path = generate_image(seed_input)
    print(f"Image saved at: {image_path}")  # 打印文件路径
    img = Image.open(image_path)
    img.show()  # 显示生成的图片
