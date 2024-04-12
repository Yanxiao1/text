import streamlit as st
from time import sleep
#from dao.mysql import *

def loginFuction(username,passwd):
    if username=='admin' and passwd=='admin':
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/index.py")
    else:
        st.error("用户名或密码错误！请重试。")
def logout_Function():
    st.session_state.logged_in = False
    st.info("您已注销")
    sleep(0.5)
    st.switch_page("app.py")