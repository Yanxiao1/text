import base64
import streamlit as st
from PIL import Image
import os
from api.v1.misc import generateFunction,ldm_stable
from src.components.tweaker import st_tweaker
from pages.navigation import make_sidebar
import torch
import datetime
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

make_sidebar()


cols = st.columns([8,6])
with cols[0]:
    st_tweaker.title(
        "MISC", 
        id = "my-elementid7",
        css = "#id { display: flex;  text-align: right; }"
    )
# 检查是否有可用的 GPU，如果有，则将模型和数据移动到 GPU 上
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
ldm_stable = ldm_stable.to(device)
# 如果上传图片的文件夹不存在，则创建
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 上传图片

uploaded_file = st.file_uploader("选择一张图片", type=['jpg', 'png', 'jpeg'])
cols = st.columns([6,6,6])
with cols[0]:
    st.write("上传图片")
    if uploaded_file is None:
        image = Image.open("./uploaded_images/白.png")
        st.image(image,  use_column_width=True)
    if uploaded_file is not None:
    # 显示图片
        image = Image.open(uploaded_file)
        st.image(image, caption='', use_column_width=True)
        st.write(uploaded_file.name)
        # 获取当前时间作为文件名的一部分
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# 上传图片的文件名，加上时间作为唯一标识
        uploaded_image_filename = f"{current_time}_{uploaded_file.name}"
        #image_path = os.path.join(UPLOAD_FOLDER, uploaded_image_filename)
    # 将图片保存到上传文件夹中
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_image_filename)
        with open(image_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

       #st.success('图片已成功保存在 {}'.format(image_path))
with cols[1]:
    st.write("")
    st.write("")
    prompt_1 = st.text_input('私钥private key')
    prompt_2 = st.text_input('公钥public key')
    gen=st.button("运行")
    #step = st.slider('选择迭代次数', 20, 100, 50)
    #st.write(f"迭代次数：{step}次")
    


with cols[2]:
    st.write("生成图片")
    if gen:
        step=50
        generateFunction(image_path,prompt1=prompt_1,prompt2=prompt_2, model=ldm_stable ,num_steps=step,encrypto_flag=False)
        # 在这里调用生成图片的函数，例如 generate_image(prompt1, prompt2)
        # 生成的图片保存在 generated_image_path 变量中
        file_name_without_extension = os.path.splitext(uploaded_file.name)[0]
        generated_image_path = f"./outputs/{file_name_without_extension}_hidden.jpg"  # 替换为实际生成的图片路径
        
        generated_image = Image.open(generated_image_path)
        st.image(generated_image, use_column_width=True)
        with open(f"./outputs/{file_name_without_extension}_hidden.jpg", "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name=f"{file_name_without_extension}_hidden.jpg",
                mime="image/jpg"
            )
    else:
        generated_image = Image.open("./uploaded_images/白2.png")
        st.image(generated_image, use_column_width=True)
    
    
   
    
