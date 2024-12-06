import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px


st.set_page_config(
    page_title='test',
    page_icon='🦈',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items= None
)


EXCEL_FILE = 'work_orders.xlsx'

# 初始化数据框架
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['工单编号', '执行人', '任务', '开始时间', '结束时间', '花费时间(小时)'])
    df.to_excel(EXCEL_FILE, index=False)
else:
    df = pd.read_excel(EXCEL_FILE)



def add_work_order():
    work_order_df = pd.DataFrame(columns=['工单编号', '执行人', '任务', '开始时间', '结束时间', '花费时间(小时)'])

    work_order = {
        '工单编号': st.text_input('工单编号'),
        '执行人': st.text_input('执行人'),
        '任务': st.text_input('任务'),
        '开始时间': st.date_input('开始时间'),
        '结束时间': st.date_input('结束时间'),
        '花费时间(小时)': st.number_input('花费时间(小时)')
    }

    if st.button('添加'):
        new_order = pd.DataFrame([work_order])
        work_order_df = pd.concat([work_order_df, new_order], ignore_index=True)

        # Save to Excel
        file_path = 'work_orders.xlsx'
        if not work_order_df.empty:
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                work_order_df.to_excel(writer, index=False, sheet_name='工单记录')

        st.success('工单添加成功！')


# Add this function call to your main menu in the main function
# st.sidebar.button('添加工单', on_click=add_work_order)

def show_work_orders():

    file_path = 'work_orders.xlsx'
    if os.path.exists(file_path):
        work_order_df = pd.read_excel(file_path,sheet_name='工单记录')
        st.write('已录入的工单信息:')
        st.dataframe(work_order_df.sort_values(by='开始时间'))
    else:
        st.write('暂无工单信息！')

def show_calendar():
    st.write('日历显示功能（待实现）')


def analyze_work_time():
    file_path = 'work_orders.xlsx'
    if os.path.exists(file_path):
        work_order_df = pd.read_excel(file_path,sheet_name='工单记录')

        # Calculate weekly/monthly totals
        work_order_df['开始时间'] = pd.to_datetime(work_order_df['开始时间'])
        work_order_df['周'] = work_order_df['开始时间'].dt.isocalendar().week
        work_order_df['月'] = work_order_df['开始时间'].dt.month

        weekly_totals = work_order_df.groupby(['执行人', '周'])['花费时间(小时)'].sum().reset_index()
        monthly_totals = work_order_df.groupby(['执行人', '月'])['花费时间(小时)'].sum().reset_index()

        # Display list
        st.write('每周累积工作时间:')
        st.dataframe(weekly_totals)

        # Display pie chart
        fig = px.pie(weekly_totals, values='花费时间(小时)', names='执行人', title='每周累积工作时间分布')
        st.plotly_chart(fig)

        # Similarly, you can display monthly totals
        st.write('每月累积工作时间:')
        st.dataframe(monthly_totals)

        fig = px.pie(monthly_totals, values='花费时间(小时)', names='执行人', title='每月累积工作时间分布')
        st.plotly_chart(fig)
    else:
        st.write('暂无分析数据！')


def main():
    st.title('test')

    menu = ['添加工单', '查看工单列表', '查看日历', '分析工作时间']
    choice = st.sidebar.selectbox('选择菜单', menu)

    if choice == '添加工单':
        add_work_order()
    elif choice == '查看工单列表':
        show_work_orders()
    elif choice == '查看日历':
        show_calendar()  # To be implemented with an actual calendar component
    elif choice == '分析工作时间':
        analyze_work_time()


if __name__ == '__main__':
    main()