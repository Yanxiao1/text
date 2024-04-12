import base64
import streamlit as st
from pages.navigation import make_sidebar
from api.v1.login import loginFuction
from src.components.tweaker import st_tweaker
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
make_sidebar()
#st.set_page_config(layout="wide")
cols = st.columns([8,2])

with cols[0]:
    st_tweaker.title(
        "深藏不露demo示例", 
        id = "my-elementid6",
        css = "#id { display: flex;  text-align: right;}"
    )
st.write("登陆以继续...")
username = st.text_input("用户名")
password = st.text_input("密码", type="password")

if st.button("Log in", type="primary"):
   loginFuction(username,password)
