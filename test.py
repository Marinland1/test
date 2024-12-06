import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot



# st.title('Uber pickups in NYC')
# st.write('first test')

# 设置全局属性
st.set_page_config(
    page_title='页面标题',
    page_icon='☆☆☆ ',
    layout='wide'
)

# 正文
# st.title('hello world')
# st.markdown('> Streamlit 支持通过 st.markdown 直接渲染 markdown')

# 设定3列
col1, col2, col3 = st.columns([100,1,1])

# 设定不同的列标题和展示的内容
with col1:
    st.header("A cat")
    # st.image("https://static.streamlit.io/examples/cat.jpg")
    st.write('first test')

with col2:
    st.header("A dog")
    # st.image("https://static.streamlit.io/examples/dog.jpg")
    st.write('first test')
with col3:
    st.header("An owl")
    # st.image("https://static.streamlit.io/examples/owl.jpg")
    st.write('first test')
