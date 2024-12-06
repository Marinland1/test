import streamlit as st

# # 用with 进行写入
# with st.popover("Open popover"):
#     st.markdown("Hello World  ")
#     name = st.text_input("What's your name?")
#
# # 不在内部写入
# st.write("Your name:", name)

popover = st.popover("Filter items")

red = popover.checkbox("Show red items.", True, help='you can use this')
blue = popover.checkbox("Show blue items.", True)

if red:
    st.write(":red[This is a red item.]")
if blue:
    st.write(":blue[This is a blue item.]")