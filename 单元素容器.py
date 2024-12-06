import streamlit as st
import time



emp1 = st.empty()
emp1.write('before')

button = st.button('press this')

if button:
    emp1.write('after')


# with st.empty():
#     for seconds in range(60):
#         st.write(f"⏳ {seconds} seconds have passed")   ##f表示格式化字符。意味着将后续的内容都格式化为字符串形式来进行输出。
#         time.sleep(1)
#     st.write("✔️ 1 minute over!")

#
# placeholder = st.empty()
#
# # 用一些文本替换占位符：
# placeholder.text("Hello")
# time.sleep(1)
# # 用图表替换文本：
# placeholder.line_chart({"data": [1, 5, 2, 6]})
# time.sleep(1)
# # 用几个元素替换图表：
# with placeholder.container():
#     st.write("This is one element")
#     st.write("This is another")
# time.sleep(1)
# # 清除所有这些元素：
# placeholder.empty()


# 创建一个空的容器


# '''
# 利用循环来实现用按钮进入下一个单元素容器内容是不现实的。以下给出了一个很好的利用缓存的方法来使用按钮进行内容切换的方法。
# '''


placeholder = st.empty()


# 定义一个按钮和它的回调函数
# def next_step_callback():
#     # 这里可以放置当点击按钮时要执行的逻辑
#     pass  # 例如，可以设置一个状态变量来指示下一步应该显示什么内容
#
#
# # 创建按钮，注意这里只创建一次
# next_button = st.button('next_step', on_click=next_step_callback)
#
# # 初始化一个状态变量来跟踪当前应该显示的内容
# current_step = st.session_state.get('current_step', 0)
#
# # 根据当前步骤更新占位符的内容
# if current_step == 0:
#     placeholder.text("Hello")
# elif current_step == 1:
#     placeholder.line_chart({"data": [1, 5, 2, 6]})
#     time.sleep(1)  # 注意：在Streamlit应用中通常不推荐使用time.sleep()，因为它会阻塞整个应用的响应
#     # 模拟下一步的转换（在实际应用中，这一步应该在回调函数中处理）
#     st.session_state.current_step += 1  # 这一步在实际应用中应该在回调函数中，且不应该直接修改状态后立刻渲染，因为Streamlit的渲染是异步的
# elif current_step == 2:
#     with placeholder.container():
#         st.write("This is one element")
#         st.write("This is another")
    # 注意：清空容器的操作通常不是必需的，因为你可以通过更新容器的内容来“清空”它
    # 如果你确实需要清空容器，应该考虑在逻辑上如何更好地管理这一点（例如，通过重置状态变量）
    # 而且，直接调用placeholder.empty()在这里是不合适的，因为它会完全移除容器，而不是清空其内容
    # 如果你想清空内容，应该设置状态变量来指示应该显示什么（比如空内容或加载消息）
    # 并在下次渲染时根据这个状态变量来更新UI
    # st.session_state.current_step = 0  # 如果真的需要重置到初始状态，应该在回调函数中处理，并且要注意Streamlit的异步渲染


# # 注意：上面的代码逻辑存在问题，因为streamlit的渲染是异步的，而且time.sleep()会阻塞应用
# # 下面的代码是一个更合理的示例，展示了如何在回调函数中处理步骤的转换
# def update_content():
#     if st.session_state.get('current_step', 0) == 0:
#         placeholder.text("Hello")
#     elif st.session_state['current_step'] == 1:
#         placeholder.line_chart({"data": [1, 5, 2, 6]})
#     elif st.session_state['current_step'] == 2:
#         with placeholder.container():
#             st.write("This is one element")
#             st.write("This is another")
#
#
# # 在按钮回调中更新步骤
# def next_step():
#     current_step = st.session_state.get('current_step', 0) + 1
#     st.session_state['current_step'] = current_step
#     update_content()  # 根据新的步骤更新内容
#
# # 首次加载时调用更新内容的函数
# item = st.session_state.get('current_step', 0)
# update_content()
#
# # 将按钮回调修改为正确的函数
# next_button = st.button('next_step2', on_click=next_step)
#

