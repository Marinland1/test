import streamlit as st


# 先设定一个标题
@st.dialog("Cast your vote")
def vote(item):
    # 写入问题，
    st.write(f"Why is {item} your favorite?")
    co1 , co2 = st.columns(2)
    with co1:
        reason1 = st.text_input("Because1...")
    with co2:
        reason2 = st.text_input("Because2...")
    # 这里如果点击发送就会展示
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason1": reason1}
        st.rerun()



# 这里定义初始界面，进行分析
if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
# 这里我们将结果输入出你选的内容，并通过输入的的原因展示出来
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"


# 定义一个投票系统

