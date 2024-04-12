import streamlit as st


from src.components.tweaker import st_tweaker  

st.set_page_config(layout="wide")

cols = st.columns([9,2,2,4])


with cols[0]:
    st_tweaker.title(
        "中午", 
        id = "my-elementid6",
        css = "#id { display: flex;  text-align: right; }"
    )

with cols[1]:
    st_tweaker.button("🖤未收藏",
        id="button-submit2", css="""#id > div {
        display: flex;
        justify-content: flex-end;
        margin-top: 25px;
    }""")

with cols[2]:
    st_tweaker.button("○未标记",
        id="button-submit3", css="""#id > div {
        margin-top: 25px;
    }""")

cols = st.columns([7,2,2,2,2,7])
with cols[1]:
    st.date_input("开始时间")

with cols[2]:
    from datetime import datetime, timedelta
    def generate_time_options(interval=15):
        times = []
        for i in range(0, 24 * 60, interval):
            hour, minute = divmod(i, 60)
            times.append(datetime(2000, 1, 1, hour, minute).time())
        return times

    time_options = generate_time_options(interval=15)  # 15分钟间隔
    selected_time = st.selectbox("Select a time", options=time_options)
    st.write("Selected time:", selected_time)
    
with cols[3]:
    st.date_input("结束时间",key="stop_time")
    st.write(st.session_state.stop_time)

with cols[4]:
    selected_time = st.time_input('Select a time', key='time_selector')
    
with cols[5]:
    # from streamlit_datetime_range_picker import datetime_range_picker
    button = st_tweaker.button("按钮", id="button-submit13", css="""#id > div {
        margin-top: 30px;
    }""")
    # st.write(button.get_width())

    s = '''display: flex;
        align-items: center; /* 垂直居中 */
        height: 10vh; /* 设置容器的高度，可以根据实际情况进行调整 */
    '''

st.write("这是一个微博")