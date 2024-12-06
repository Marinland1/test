import streamlit as st

# 插入一个图表
data = {
    'x': [1, 2, 3, 4, 5],  # X轴的数据点
    'y': [10, 20, 25, 30, 40]  # Y轴的数据点，与X轴的数据点一一对应
}

# 使用st.line_chart()绘制折线图
st.line_chart(data)

# 设定一个扩张器在图表中
exp = st.expander("See explanation")
#也可以不采用with的方法，直接采用exp.write or exp.image 的方法来写入容器内容。
with exp:
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
    st.image("https://static.streamlit.io/examples/dice.jpg")