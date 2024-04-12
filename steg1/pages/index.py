import base64
import streamlit as st
from pages.navigation  import make_sidebar
from src.components.tweaker import st_tweaker
#from dao.mysql import getAllEvent 
make_sidebar()

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

cols = st.columns([7,4])
with cols[0]:
    st_tweaker.title(
        "研究背景", 
        id = "my-elementid7",
        css = "#id { display: flex;  text-align: right; }"
    )

st.markdown('''
    <style>
    .background-gray {
        background-color: #f0f0f0; /* 设置灰色背景 */
        padding: 10px; /* 可选：添加一些内边距以增加内容与背景之间的间距 */
    }
    </style>
   <main>   
        <p class="center-text background-gray" style="font-size: 20px;" 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;随着信息技术的飞速发展，多媒体数据的存储、处理和传输变得越来越便捷，这也使得信息的安全性和隐私保护变得越来越重要。</p> 
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;传统的信息安全技术主要围绕加密技术及体系来完成，但进入移动互联网、大数据时代，传统的加密技术暴露出不足，容易被攻击者通过分析异常数据来发现目标。</p>
        <p class="center-text background-gray" style="font-size: 20px;"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;网络攻击者可能会窃取、篡改或破坏网络中的信息，给个人和企业带来巨大的损失。因此，信息隐藏技术在网络安全领域的应用也变得越来越重要。</b></p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在古代，人们就已经开始利用隐写术来传递秘密信息。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;例如，古希腊战争时期，奴隶主将秘密信息写在奴隶的光头上，等奴隶的头发长起来后再去另一个部落，从而实现了部落之间的秘密通信。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在中国古代也有很多关于稳写术的记载, “头诗”是其中比较著名的方法其将秘密信息写在诗句的特定位置以实现隐蔽通信。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;当前，微信、抖音、微博等网络社交平台是人们进行信息传递和交流的主要途径，具有效率高、范围广、速度快等特点。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;基于这些特点，社交网络也成为了传递加密信息的主流平台之一。同时，通过网络晒图等途径进行秘密信息传播的需求也在不断增大。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>但是随着各种图像信息爬取和解密技术的发展，使得隐藏图像信息传递的安全性遭受到了很大的挑战。</b></p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;近两年来，研究高效、简便的，面向社交网络的图像信息隐写方法成为了热门的研究方向之一。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>生成式信息隐藏的基本原理是通过训练一个生成模型来生成载体数据，并将秘密信息隐藏在生成的载体数据中。</b></p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;在信息传递过程中不会引起信道中第三方的注意，达到证实载体信息所有权、数据完整性或隐蔽通信的目的。</p>
        <p class="center-text background-gray" style="font-size: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;而扩散概率模型作为生成模型领域一个新的概念，在生成载体数据方面等诸多领域展现出不俗的表现。</p>
    </main>  
            ''',
            unsafe_allow_html=True
)