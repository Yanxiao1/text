import base64
import time
import os
from PIL import Image
import streamlit as st
import datetime
from controlnet_util.synthtext import text_image
from predict import process_image
from src.components.tweaker import st_tweaker
from pages.navigation import make_sidebar
make_sidebar()
cor_xy = (50, 50, 200, 100)  # 文本所在位置的左上角和右下角坐标
image_size = (512, 512)  # 图像大小
font_path = './resources/Arial.ttf'  # 字体文件路径
font_size = 16  # 字体大小
background_color = 'white'  # 背景颜色
text_color = 'black'  # 文本颜色
    
def main_bg(main_bg):
    main_bg_ext = "jpg"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
 
#调用
main_bg('./resources/background.jpg')
current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
cols = st.columns([7,4])
with cols[0]:
    st_tweaker.title(
        "刷新文字", 
        id = "my-elementid7",
        css = "#id { display: flex;  text-align: right; }"
    )
# 手动设置所需参数
cols = st.columns([6,4,6])       
with cols[0]:
    st.write("输入文本")
    text = st.text_input("logo")  # 文本内容
    prompt = st.text_input("prompt")
    with open('prompts.txt', 'w', encoding='utf-8') as f:  
         f.write(prompt)
    st.write("")
    click=st.button("刷新文字")
with cols[2]:
    if click: 
        text_img = text_image(text, cor_xy, image_size, font_path, font_size, background_color, text_color)
        text_text= text_image(text, cor_xy, image_size, font_path, font_size, background_color, text_color)
        text_img.save(f"./text_result/{prompt}.png")
        process_image(
        input_image_path = f"C:/shuiyin/steg1/text_result/{prompt}.png",
        pretrained_model_path = "C:/shuiyin/steg1/checkpoints/stable-diffusion-v1-5",#sd
        control_net_path = "C:/shuiyin/steg1/checkpoints/sd-controlnet-canny",#canny
        output_dir = "./output_images/",
        canny = {'low_threshold': 50, 'high_threshold': 150},
        inference = {'prompts_path': "prompts.txt", 'width': 200, 'height': 200, 'additional_prompt': "additional prompt", 
             'negative_prompt': "negative prompt", 'num_step': 100, 'num_image_per_prompt': 1, 'controlnet_conditioning_scale': 1.0,
             'classifer_free_guidance_scale': 1.0, 'image_guidance_scale': 1.0, 'bbx_guidance_scale': 1.0},
        device = "cuda:0",
        seed = 42,
        ddim_inv = {'SDEdit_strength': 1.0},
        extra = {'word_list': [''], 'bbx_num': 0},#加载图片
    )
    
    #with open(f"./output_images/{current_time}", "rb") as file:
            #btn = st.download_button(
                #label="Download image",
                #data=file,
                #file_name=f"./text_result/{current_time}.png",
                #mime="image/png"
           # )



    




