import pandas as pd
import numpy as np
import streamlit as st
from matplotlib import pyplot



# st.title('Uber pickups in NYC')
# st.write('first test')

# 设置全局属性
st.set_page_config(
    page_title='test',
    page_icon='🦈',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items= None
)
# col1, col2, col3 = st.columns(3)



import streamlit as st
#设置行列
row1 = st.columns(3)
row2 = st.columns(3)
#遍历行列，并设置每一个容器的高度信息，宽度信息没有设定
# for col in row1 + row2:
#     tile = col.container(height=120)
col1 = row1[0]
col2 = row1[1]
col3 = row1[2]
col4 = row2[0]
col5 = row2[1]
col6 = row2[2]
#插入一个表情
tile = col1.container(height=120)
tile.title(":balloon:")
tile = col2.container(height=120)
tile.title("1")
tile = col3.container(height=120)
tile.title("2")
tile = col4.container(height=120)
tile.title("3")
tile = col5.container(height=120)
tile.title("4")
col6.write('this is 6')


##对容器进行设定，这个就是用with，
with st.container():
    st.write("This is inside the container")

    # 可用于接受 "类文件 "对象的任何地方：
    # s=np.random.randn(100, 3)
    # st.bar_chart(s)  #(生成一个50*3的数组，即50行三列)
    # chart_data = pd.DataFrame({"col1": list(range(20)), "col2": np.random.randn(20), "col3": np.random.randn(20)}) #使用 x 和 y 参数指定了x轴和y轴的数据列，并通过 color 参数为不同的数据点着色。
    # st.bar_chart(chart_data, x="col1", y="col2", color="col3",width=100,height=200)   #(通过x和y的参数来指定行列，但是已经行成的二维数组应该不可以这样操作)(宽度100为极限，高度500为沾满页面（1080P）)
# 对容器进行设定，这个就是用with，
# c1=st.container(height=300,border=False,key=True)
#
# with c1:
#     for i in range (0,10):
#         st.write("This is inside the container")
#
#     # 可用于接受 "类文件 "对象的任何地方：
#     st.bar_chart(np.random.randn(50, 3))
#
# st.write("This is outside the container")
# c1.write("This is inside the container the second time!")
# st.write("This is outside the container")