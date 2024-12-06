import streamlit as st
import numpy as np
# 设定三个tab 这个相当于三个界面
st.set_page_config(
    page_title='test',
    page_icon='🦈',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items= None
)

co1,co2 = st.columns([3,1])


with co1:
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with co2:
# 三个tab的设定
    tab4, tab5 = st.tabs(["Chart", "Data"])

# 设定一个随机数列
    data = np.random.randn(10, 1)

# 设定第一个tab
    tab4.subheader("A tab with a chart")
    tab4.line_chart(data)
# 设定第二个tab
    tab5.subheader("A tab with the data")
    tab5.write(data)

