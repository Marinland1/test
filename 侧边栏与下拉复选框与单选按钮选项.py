import streamlit as st

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    [1,2,3,4,5,6,7]
) #参数add_selectbox接收到的值是option选项的结果。实时热更新。
if add_selectbox == 1:
    st.write(":red[This is a red item.]")
if add_selectbox == 2:
    st.write(":blue[This is a blue item.]")





# 假设我们有一个选项列表，其中每个选项都是一个字典的键
options = {'apple': 'An edible fruit', 'banana': 'A long, curved fruit', 'carrot': 'A long, orange vegetable'}


# 定义一个函数来格式化选项的显示
def format_option(option):
    # 使用字典来获取与选项关联的描述，并返回这个描述作为显示文本
    return options[option]
# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    selected_option = st.selectbox('Choose a fruit or vegetable:', list(options.keys()), format_func=format_option)

    # 显示用户选择的选项及其描述
st.write('You selected:', selected_option, 'which is', options[selected_option])




# 使用 st.selectbox() 并传递 format_func 参数
