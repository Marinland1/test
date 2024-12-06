import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot

# 设置全局属性
st.set_page_config(
    page_title='test',
    page_icon='🦈',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items= None
)
c1=st.container(height=300,border=True,key=True)
# with c1:
#     co1, co2, co3 = st.columns(3)
#
#     with co1:
#         st.write('111')
#     with co2:
#         st.write('222')
#     with co3:
#         st.write('333')

co1, co2, co3 = c1.columns(3)

co1.write('111')

# with co1 :
#     with st.container() as c1 :
#         st.write('111')
# with co2 :
#     with st.container() as c2 :
#         st.write('222')
# with co3 :
#     with st.container() as c3:
#         st.write('333')


# st.write('over')