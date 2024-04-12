import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from api.v1.login import *

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("深藏不露")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/index.py", label="首页", icon="🌍")
            st.page_link("pages/encrypto.py", label="隐写", icon="✍️")
            st.page_link("pages/decrypto.py", label="恢复", icon="🎈")
            st.page_link("pages/textbrush.py",label="刷新文字", icon="📕")

            st.write("")
            st.write("")
            st.divider()
            if st.button("注销"):
                logout_Function()
            st.divider()
            st.write("用户信息")
        
        elif get_current_page_name() != "app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("app.py")



