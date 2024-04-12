from PIL import Image, ImageDraw, ImageFont
import numpy as np
from Textgen.gen import datagen
from omegaconf import OmegaConf
from typing import Dict
import os

def text_image(text, cor_xy, image_size, font_path='arial.ttf', font_size=16, background_color='white', text_color='black'):
    left, top, right, bottom = cor_xy
    width = right - left
    height = bottom - top
    
    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)
    font_size = font_size * min(width / text_width, height / text_height)
    font = ImageFont.truetype(font_path, int(font_size))

    draw.text((left, top), text, fill=text_color, font=font)
    return image
    
def main(cfg: Dict):
    data_gen = datagen(cfg)
    cnt = 0
    result_path = cfg.result_path
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    # if cfg.read_from_prompt
    #     assert cfg.prompt_path is not None
    while(cnt < cfg.sample_num):
        try:
            text_image, bbs, text = data_gen.gen_text_image(cnt)
        except:
            continue
        else:
            image_name = f"{cnt}.png"
            text_name = f"{cnt}.txt"
            text_image.save(os.path.join(result_path, image_name))
            with open(os.path.join(result_path, text_name), "w") as f:
                for bb in bbs:
                    line = ",".join(str(x) for x in bb)
                    f.write(line + ',' + text + '\n')
            cnt += 1
    
if __name__ == '__main__':
    # 手动设置所需参数
    text = "Hello, world!"  # 文本内容
    cor_xy = (50, 50, 200, 100)  # 文本所在位置的左上角和右下角坐标
    image_size = (512, 512)  # 图像大小
    font_path = 'arial.ttf'  # 字体文件路径
    font_size = 16  # 字体大小
    background_color = 'white'  # 背景颜色
    text_color = 'black'  # 文本颜色
    
    # 调用text_image函数
    text_img = text_image(text, cor_xy, image_size, font_path, font_size, background_color, text_color)
    
    # 保存生成的图像
    text_img.save("text_image.png")