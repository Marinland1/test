import time
import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta
import datetime
import math
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from streamlit_calendar import calendar as cda
import base64
import requests
#matplotlib中设置中文字体，否则中文不会显示。字体从C:\Windows\Fonts中找。
matplotlib.rcParams['font.sans-serif'] = ['simsun']
matplotlib.rcParams['axes.unicode_minus'] = False
# font_set = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc')
# import plotly.express as px

st.set_page_config(
    page_title='Working Task Management ',
    page_icon='🦈',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items= None
)

#初始化写入的路径
excel_file = 'demo_h.xlsx'
# 初始化数据框架
if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=['Order_ID', 'Applicant', 'Departement', 'Project_id', 'Start date', 'End date','Executor1','Executor2','Hours_spent','Detial'])#这里的名称一定要和写入名称匹配，否则会创建多余的列
    df.to_excel(excel_file, index=False,sheet_name='Hours')
else:
    # df = pd.read_excel(excel_file, parse_dates=(['Start date','End date']), date_format='%Y-%m-%d')
    # # df = pd.read_excel(excel_file, dtype={'Start date':'datetime.date'})
    # # df['Start date'] = pd.to_datetime(df['Start date'], format='%Y-%m-%d', errors='coerce')
    df = pd.read_excel(excel_file)
    df = df.dropna(axis=1, how='all')
    if df.empty:
        df=df
    else:
        df['Start date'] = df['Start date'].dt.date
        df['End date'] = df['End date'].dt.date
    # df = pd.read_excel(excel_file)
# 读取excel。可以设置文件路径，头，和名
def read_excel(list,header,name):
    dfs = pd.read_excel(list,header=header,names=name)
    return dfs



def upload_to_github(file_path, repo, path_in_repo, commit_message, access_token):
    with open(file_path, 'rb') as file:
        content = file.read()
        content_base64 = base64.b64encode(content).decode()

    url = f"https://api.github.com/repos/{repo}/contents/{path_in_repo}"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": commit_message,
        "content": content_base64
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        st.success("文件成功上传到 GitHub")
    else:
        st.error(f"文件上传失败: {response.status_code}")
        st.error(response.json())

    return response.json()



def write_excel(data):
    # for index, row in data.iterrows():
    #     row['Start Date'] = pd.to_datetime(row['Start Date']).strftime('%Y-%m-%d')
    #     row['End Date'] = pd.to_datetime(row['End Date']).strftime('%Y-%m-%d')
    df_new = pd.concat([df,data],axis=0)
    with pd.ExcelWriter('demo_h.xlsx', mode='w') as writer:
        df_new.to_excel(writer, sheet_name='Hours', index=False)

    file_path = 'demo_h.xlsx'  # 本地文件路径
    repo = 'Marinland1/test'  # 仓库名
    path_in_repo = 'demo_h.xlsx'  # 仓库中的路径
    commit_message = 'Update demo_h.xlsx'
    access_token = 'Hjl520hjl###'  # 你的 GitHub 个人访问令牌
    response = upload_to_github(file_path, repo, path_in_repo, commit_message, access_token)
    print(response)




# 找到提交人的姓名列表
df1 = pd.read_excel('name.xlsx',sheet_name = 'app',header=None,names=['name','department'],)
data_name = df1['name']
data_department = df1['department']
# 找到执行人姓名列表
df2= pd.read_excel('name.xlsx',sheet_name = 'exe')
exe_name = df2['name']
#跳过第一行，这是在绘图的时候用的
df3= pd.read_excel('name.xlsx',sheet_name = 'exe',skiprows =[1])
exe_name1 = df3['name']


#calendar css




#利用这个函数，当输入人员的时候直接匹配他们所在行的索引(dataframe)
def feedback_index(applicant):
    index= df1[df1['name'] == applicant].index.tolist()
    return index[0]
###用来在修改函数中进行找寻和匹配
def index_con(i):
    index= df1[df1['name'] == i].index.tolist()
    return index[0]
##用来在修改函数中找到执行人
def index_exe(i1,i2):
    index1 = df2[df2['name'] == i1].index.tolist()
    index2 = df2[df2['name'] == i2].index.tolist()
    return index1[0],index2[0]
def index_exe0(i1):
    index1 = df2[df2['name'] == i1].index.tolist()
    return index1[0],0

##########################以下两个函数是用来计算剩余工时的
def count_weekend_days(start_date, end_date):
    weekend_count = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in [5, 6]:  # weekday()方法返回0 - 4表示周一到周五，5和6表示周六和周日
            weekend_count += 1
        current_date += timedelta(days = 1)
    return weekend_count
def Accumulated_working_hours(st_data,ed_data,excuter):
    start1 = st_data
    end1 = ed_data
    time_work_hours1 = 0
    #是否要考虑更改迭代方式。这里可以考虑用i=len（df）for i in i 的方式进行迭代。因为df.iterrows会把dateframe转换为series进行迭代。
    for index,row in df.iterrows():
        start2 = row['Start date']
        start2 = pd.to_datetime(start2).date()
        end2 = row['End date']
        end2 = pd.to_datetime(end2).date()
        # print(row['name'],row['department'])
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        if overlap_start <= overlap_end:
            overlap_start = overlap_start
            overlap_end = overlap_end
        else:
            continue
        if excuter == row['Executor1'] :
            weekend_count = count_weekend_days(overlap_start, overlap_end)    #重合时间段周末有几天
            coincide_day2 =  (end2- start2).days - count_weekend_days(start2, end2)+1 # 表格中时间段工作日有几天
            coincide_day3 = (overlap_end - overlap_start).days - weekend_count+1   #重合时间段工作日总共有几天
            if pd.notnull(row['Executor1']) and pd.notnull(row['Executor2']):
                l1 = (row['Hours_spent'])
                work_hours_day = l1/coincide_day2*coincide_day3  #在这个重合区间内的总工作时间
                time1 = work_hours_day/2
                time2 = work_hours_day/2
                time_work_hours1 = time_work_hours1 + time1
            elif pd.isnull(row['Executor2']):
                work_hours_day = row['Hours_spent'] / coincide_day2 * coincide_day3  # 在这个重合区间内的总工作时间
                time1 = work_hours_day
                time_work_hours1 = time_work_hours1 + time1
        elif excuter == row['Executor2'] :
            weekend_count = count_weekend_days(overlap_start, overlap_end)    #重合时间段周末有几天

            coincide_day2 =  (end2- start2).days - count_weekend_days(start2, end2)+1 # 表格中时间段工作日有几天
            coincide_day3 = (overlap_end - overlap_start).days - weekend_count+1   #重合时间段工作日总共有几天
            if pd.notnull(row['Executor1']) and pd.notnull(row['Executor2']):
                l1 = (row['Hours_spent'])
                work_hours_day = l1/coincide_day2*coincide_day3  #在这个重合区间内的总工作时间
                time1 = work_hours_day/2
                time2 = work_hours_day/2
                time_work_hours1 = time_work_hours1 + time1
            elif pd.isnull(row['Executor2']):
                work_hours_day = row['Hours_spent'] / coincide_day2 * coincide_day3  # 在这个重合区间内的总工作时间
                time1 = work_hours_day
                time_work_hours1 = time_work_hours1 + time1
    coincide_day1 = (end1 - start1).days - count_weekend_days(start1, end1) + 1  # 输入的时间中工作日有几天
    last_time = coincide_day1*8 - time_work_hours1
    return last_time,time_work_hours1



def add_task():
    st.title('添加工单')
    # 页面布局，两行三列均匀分布
    row1 = st.columns(4)
    row2 = st.columns(2)
    row3 = st.columns(3)
    row4 = st.columns(3)
    row5 = st.columns(1)
    # for col in row1 + row2:
    #     tile = col.container(height=120)
    col01 = row1[0]
    col02 = row1[1]
    col03 = row1[2]
    col04 = row1[3]
    col11 = row2[0]
    col12 = row2[1]

    col21 = row3[0]
    col22 = row3[1]
    col23 = row3[2]
    col31 = row4[0]
    col32 = row4[1]
    col41 = row5[0]
    # 给出用户填入内容的交互框
    work_order_id = col01.text_input('Work Order ID',value='')
    applicant = col02.selectbox('Applicant',data_name,index = 0)
    indexs = feedback_index(applicant)
    applicant_departement = col03.selectbox('Applicant_departement',data_department,index=indexs)
    project = col04.text_input('Project_id', value='')
    start_date = col11.date_input('Start Date')
    end_date = col12.date_input('End Date')
    executor1 = col21.selectbox('Executor1',exe_name,index=0)
    last_time1, time1 = Accumulated_working_hours(start_date,end_date,executor1)
    if type(executor1) != float:
        executor2 = col22.selectbox('Executor2',exe_name)
        col31.write(f':red[该执行人在此时间段剩余工作时长{last_time1}小时]')
        if type(executor2) != float:
            last_time2, time2 = Accumulated_working_hours(start_date, end_date, executor2)
            col32.write(f':red[该执行人在此时间段剩余工作时长{last_time2}小时]')
    else:
        col22.text('先录入执行人1')

    hours_spent = col23.number_input('Hours Spent', min_value=0,value=0)
    detial = col41.text_area('Task Description',value=' ')

    if st.button('添加'):
        if applicant == 'Enter' or applicant_departement == 'Enter' or type(executor1) == float or work_order_id == ' 'or project == ' ':
            st.warning('还有信息没有输入')
        else:
            work_order = pd.DataFrame({
                'Order_ID': [work_order_id],
                'Applicant': [applicant],
                'Departement': [applicant_departement],
                'Project_id': [project],
                'Start date': [start_date],
                'End date': [end_date],
                'Executor1': [executor1],
                'Executor2': [executor2],
                'Hours_spent': [hours_spent],
                'Detial': [detial]
        })
            write_excel(work_order)
            st.success('工单添加成功！')
            time.sleep(0.5)
            st.rerun()


def see_list():
    row1 = st.columns([1, 1, 1, 1, 7])
    row2 = st.columns(2)
    col00 = row1[0]
    col01 = row1[1]
    col02 = row1[2]
    col03 = row1[3]
    col11 = row2[0]
    col12 = row2[1]
    button0 = col00.button("All")
    button1 = col01.button("本年")
    button2 = col02.button("本月")
    button3 = col03.button("本周")
    start_date = datetime.now()
    end_date = datetime.now()
    if button1:
        # 获取本年第一天
        year_start = datetime(datetime.now().year, 1, 1)
        start_date = year_start
        end_date = datetime(datetime.now().year, 12, 31)
    elif button2:
        # 获取本月第一天
        this_month = datetime.now().month
        year = datetime.now().year
        month_start = datetime(year, this_month, 1)
        start_date = month_start
        if this_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            end_date = datetime(year, this_month, 31)
        if this_month == 4 or 6 or 9 or 11:
            end_date = datetime(year, this_month, 30)
        if this_month == 2:
            end_date = datetime(year, this_month, 28)
    elif button3:
        # 获取本周第一天（这里以周一为一周开始）
        today = datetime.now()
        offset = today.weekday()
        week_start = today - timedelta(days=offset)
        start_date = week_start
        end_date = datetime.now()
    start_date1 = col11.date_input('Start Date', value=start_date)
    end_date1 = col12.date_input('End Date', value=end_date)
    filtered_events = df[((df['Start date'] >= start_date1 ) & (df['End date'] <= end_date1)) |
                      ((df['Start date'] < start_date1 ) & (df['End date'] >= start_date1 )) |
                      ((df['Start date'] <= end_date1) & (df['End date'] > end_date1))]
    if button0:
        st.dataframe(df)
    else:
        st.dataframe(filtered_events)

def change_list():
    st.title('修改工单')
    # 页面布局，两行三列均匀分布
    row1 = st.columns(4)
    row2 = st.columns(2)
    row3 = st.columns(3)
    row4 = st.columns(3)
    row5 = st.columns(1)
    # for col in row1 + row2:
    #     tile = col.container(height=120)
    col01 = row1[0]
    col02 = row1[1]
    col03 = row1[2]
    col04 = row1[3]
    col11 = row2[0]
    col12 = row2[1]

    col21 = row3[0]
    col22 = row3[1]
    col23 = row3[2]
    col31 = row4[0]
    col32 = row4[1]
    col41 = row5[0]
    # 给出用户填入内容的交互框
    work_order_id = col01.text_input('Work Order ID', value='')
    dfm = df[df['Order_ID'] == work_order_id]
    st.dataframe(dfm)
    ind = []

    if dfm.empty:
        st.write('错误。表格中没有找到对应的Order ID')
    else :
        matching_rows = df[df['Order_ID'] == work_order_id].index.tolist()
        ind = matching_rows[0]
        index1 = index_con(dfm['Applicant'].item())
        applicant = col02.selectbox('Applicant', data_name,index=index1)
        indexs = feedback_index(applicant)
        applicant_departement = col03.selectbox('Applicant_departement', data_department, index=indexs)
        project = col04.text_input('Project_id', value=dfm['Project_id'].item())
        start_date = col11.date_input('Start Date',value=dfm['Start date'].item())
        end_date = col12.date_input('End Date',value=dfm['End date'].item())
        ####
        if dfm['Executor2'].isnull().any():
            index2,index3 = index_exe0(dfm['Executor1'].item())
        else:
            index2,index3 = index_exe(dfm['Executor1'].item(),dfm['Executor2'].item())

        executor1 = col21.selectbox('Executor1', exe_name, index=index2)
        last_time1, time1 = Accumulated_working_hours(start_date, end_date, executor1)

        if type(executor1) != float:
            executor2 = col22.selectbox('Executor2', exe_name, index=index3)
            col31.write(f':red[该执行人在此时间段剩余工作时长{last_time1}小时]')
            if type(executor2) != float:
                last_time2, time2 = Accumulated_working_hours(start_date, end_date, executor2)
                col32.write(f':red[该执行人在此时间段剩余工作时长{last_time2}小时]')
        else:
            col22.text('先录入执行人1')

        hours_spent = col23.number_input('Hours Spent', min_value=0, value=dfm['Hours_spent'].item())
        detial = col41.text_area('Task Description', value=dfm['Detial'].item())

        if st.button('修改'):
            if applicant == 'Enter' or applicant_departement == 'Enter' or type(
                    executor1) == float or work_order_id == ' ' or project == ' ':
                st.warning('还有信息没有输入')
            else:
                # new_order = pd.DataFrame({
                #     'Order_ID': [work_order_id],
                #     'Applicant': [applicant],
                #     'Departement': [applicant_departement],
                #     'Project_id': [project],
                #     'Start date': [start_date],
                #     'End date': [end_date],
                #     'Executor1': [executor1],
                #     'Executor2': [executor2],
                #     'Hours_spent': [hours_spent],
                #     'Detial': [detial]
                # })
                new_order = [
                    work_order_id,
                    applicant,
                    applicant_departement,
                    project,
                    start_date,
                    end_date,
                    executor1,
                    executor2,
                    hours_spent,
                    detial
                ]

                df.iloc[ind] = new_order
                with pd.ExcelWriter('demo_h.xlsx', mode='w') as writer:
                    df.to_excel(writer, sheet_name='Hours', index=False)
                st.success('工单添加成功！')
                time.sleep(0.5)

def calendar():
    dfc = pd.read_excel('demo_h.xlsx')
    mode = st.selectbox(
        "Calendar Mode:",
        (
            "daygrid",
            # "timegrid",
            "timeline",
            # "resource-daygrid",
            # "resource-timegrid",
            # "resource-timeline",
            "list",
            "multimonth",
        ),
    )
    dfc['department'] = dfc['Departement'].str[:2]
    events = []

    # dataframe转换为list
    for index, row in dfc.iterrows():
        if row['department'] == 'EA':
            event = {
                'title': str(row['Detial']) + str(row['Order_ID']),
                "color": "#FF6C6C",
                'start': row['Start date'].strftime('%Y-%m-%d'),
                'end': row['End date'].strftime('%Y-%m-%d'),
                'resourceId': row['Order_ID']
            }
            events.append(event)
        elif row['department'] == 'EF':
            event = {
                'title': str(row['Order_ID']) + str(row['Detial']),
                "color": "#3D9DF3",
                'start': row['Start date'].strftime('%Y-%m-%d'),
                'end': row['End date'].strftime('%Y-%m-%d'),
                'resourceId': row['Order_ID']
            }
            events.append(event)
        else:
            event = {
                'title': str(row['Detial']) + row['Order_ID'],
                "color": "#FFBD45",
                'start': row['Start date'].strftime('%Y-%m-%d'),
                'end': row['End date'].strftime('%Y-%m-%d'),
                'resourceId': row['Order_ID']
            }
            events.append(event)


    calendar_options = {
        "editable": "false",
        "navLinks": "true",
        # "resources": calendar_resources,
        "selectable": "true",
    }
    if "resource" in mode:
        if mode == "resource-daygrid":
            calendar_options = {
                **calendar_options,
                "initialDate": str(datetime.now().date()),
                "initialView": "resourceDayGridDay",
                "resourceGroupField": "building",
            }
        elif mode == "resource-timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
                },
                "initialDate": "2024-07-01",
                "initialView": "resourceTimelineDay",
                "resourceGroupField": "building",
            }
        elif mode == "resource-timegrid":
            calendar_options = {
                **calendar_options,
                "initialDate": "2024-07-01",
                "initialView": "resourceTimeGridDay",
                "resourceGroupField": "building",
            }
    else:
        if mode == "daygrid":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialDate": str(datetime.now().date()),
                "initialView": "dayGridMonth",
            }
        elif mode == "timegrid":
            calendar_options = {
                **calendar_options,
                "initialView": "timeGridWeek",
            }
        elif mode == "timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "timelineDay,timelineWeek,timelineMonth",
                },
                "initialDate": str(datetime.now().date()),
                "initialView": "timelineMonth",
            }
        elif mode == "list":
            calendar_options = {
                **calendar_options,
                "initialDate": str(datetime.now().date()),
                "initialView": "listMonth",
            }
        elif mode == "multimonth":
            calendar_options = {
                **calendar_options,
                "initialView": "multiMonthYear",
            }

    # state = cda(events=events, options=calendar_options, key="calendar")
    state = cda(
        events=events,
        options=calendar_options,
        custom_css="""
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
        """,
        key=mode,
    )

    # if state.get("eventsSet") is not None:
    #     st.session_state["events"] = state["eventsSet"]

def anay_time():
    menu = ['人员','项目ID','部门','下单人']
    sidebar1 = st.sidebar
    menu_choice1 = sidebar1.selectbox('Choose an option', menu)
    st.title('分析工作时间')
    if menu_choice1 == '人员':
        row1 = st.columns([1,1,1,7])
        row2 = st.columns(2)
        row3 = st.columns([2,4,4])
        col01 = row1[0]
        col02 = row1[1]
        col03 = row1[2]
        col11 = row2[0]
        col12 = row2[1]
        col21 = row3[0]
        col22 = row3[1]
        col23 = row3[2]
        button1 = col01.button("本年")
        button2 = col02.button("本月")
        button3 = col03.button("本周")
        start_date = datetime.now()
        end_date = datetime.now()
        if button1 :
            # 获取本年第一天
            year_start = datetime(datetime.now().year, 1, 1)
            start_date = year_start
            end_date = datetime(datetime.now().year, 12, 31)
        elif button2 :
            # 获取本月第一天
            this_month = datetime.now().month
            year = datetime.now().year
            month_start = datetime(year, this_month, 1)
            start_date = month_start
            if this_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
                end_date = datetime(year, this_month, 31)
            if this_month == 4 or 6 or 9 or 11:
                end_date = datetime(year, this_month, 30)
            if this_month == 2:
                end_date = datetime(year, this_month, 28)
        elif button3 :
            # 获取本周第一天（这里以周一为一周开始）
            today = datetime.now()
            offset = today.weekday()
            week_start = today - timedelta(days=offset)
            start_date = week_start
            end_date = datetime.now()
        start_date1 = col11.date_input('Start Date',value = start_date)
        end_date1 = col12.date_input('End Date', value = end_date)
        if start_date1 > end_date1:
            st.write('Error! end_data need to be the future of the start data')
        else:
            data = []
        #这里用exe_name1是为了跳过第一行的nan
            for i in exe_name1:
                last_time , time = Accumulated_working_hours(start_date1, end_date1, i)
                data.append([i, time])
            df_exe = pd.DataFrame(data, columns=['姓名', '累计工时'])
            col21.dataframe(df_exe)
            st.text('总计工时：')
            st.text(df_exe['累计工时'].sum())
            #画柱状图
            col22.bar_chart(df_exe,x='姓名',y='累计工时')
            #画饼状图
            fig, ax = plt.subplots()
            ax.pie(df_exe['累计工时'], labels=df_exe['姓名'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # 确保饼状图是圆形的
            # 在 Streamlit 中展示图表
            col23.pyplot(fig)
    if menu_choice1 == '项目ID':
        row1 = st.columns([1,1,1,7])
        row2 = st.columns(2)
        row3 = st.columns([2,4,4])
        col01 = row1[0]
        col02 = row1[1]
        col03 = row1[2]
        col11 = row2[0]
        col12 = row2[1]
        col21 = row3[0]
        col22 = row3[1]
        col23 = row3[2]
        button1 = col01.button("本年")
        button2 = col02.button("本月")
        button3 = col03.button("本周")
        start_date = datetime.now()
        end_date = datetime.now()
        if button1:
            # 获取本年第一天
            year_start = datetime(datetime.now().year, 1, 1)
            start_date = year_start
            end_date = datetime(datetime.now().year, 12, 31)
        elif button2:
            # 获取本月第一天
            this_month = datetime.now().month
            year = datetime.now().year
            month_start = datetime(year, this_month, 1)
            start_date = month_start
            if this_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
                end_date = datetime(year, this_month, 31)
            if this_month == 4 or 6 or 9 or 11:
                end_date = datetime(year, this_month, 30)
            if this_month == 2:
                end_date = datetime(year, this_month, 28)
        elif button3:
            # 获取本周第一天（这里以周一为一周开始）
            today = datetime.now()
            offset = today.weekday()
            week_start = today - timedelta(days=offset)
            start_date = week_start
            end_date = datetime.now()
        start_date2 = col11.date_input('Start Date', value=start_date)
        end_date2 = col12.date_input('End Date', value=end_date)
        if start_date2 > end_date2:
            st.write('Error! end_data need to be the future of the start data')
        else:
            dfp = pd.read_excel('demo_h.xlsx')
            dfpp = dfp[(df['Start date'] >= start_date2) & (df['End date'] <= end_date2)]   #根据时间进行筛选
            grouped = dfpp.groupby('Project_id')['Hours_spent'].sum().reset_index()          #grouped 是分组以后的df
            st.text('总计工时：')
            st.text(dfpp['Hours_spent'].sum())
            # 查看分组后的结果
            # print(grouped)
            col21.dataframe(grouped)
            #画柱状图
            col22.bar_chart(grouped,x='Project_id',y='Hours_spent')
            #画饼状图
            fig, ax = plt.subplots()
            ax.pie(grouped['Hours_spent'], labels=grouped['Project_id'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # 确保饼状图是圆形的
            # 在 Streamlit 中展示图表
            col23.pyplot(fig)


    if menu_choice1 == '部门':
        row1 = st.columns([1,1,1,7])
        row2 = st.columns(2)
        row3 = st.columns([2,4,4])
        col01 = row1[0]
        col02 = row1[1]
        col03 = row1[2]
        col11 = row2[0]
        col12 = row2[1]
        col21 = row3[0]
        col22 = row3[1]
        col23 = row3[2]
        button1 = col01.button("本年")
        button2 = col02.button("本月")
        button3 = col03.button("本周")
        start_date = datetime.now()
        end_date = datetime.now()
        if button1:
            # 获取本年第一天
            year_start = datetime(datetime.now().year, 1, 1)
            start_date = year_start
            end_date = datetime(datetime.now().year, 12, 31)
        elif button2:
            # 获取本月第一天
            this_month = datetime.now().month
            year = datetime.now().year
            month_start = datetime(year, this_month, 1)
            start_date = month_start
            if this_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
                end_date = datetime(year, this_month, 31)
            if this_month == 4 or 6 or 9 or 11:
                end_date = datetime(year, this_month, 30)
            if this_month == 2:
                end_date = datetime(year, this_month, 28)
        elif button3:
            # 获取本周第一天（这里以周一为一周开始）
            today = datetime.now()
            offset = today.weekday()
            week_start = today - timedelta(days=offset)
            start_date = week_start
            end_date = datetime.now()
        start_date2 = col11.date_input('Start Date', value=start_date)
        end_date2 = col12.date_input('End Date', value=end_date)
        if start_date2 > end_date2:
            st.write('Error! end_data need to be the future of the start data')
        else :
            dfp = pd.read_excel('demo_h.xlsx')
        # 根据单元格内容前两位进行分组
            dfpf = dfp[(df['Start date'] >= start_date2) & (df['End date'] <= end_date2)]   #根据时间进行筛选
            dfpf['department'] = dfpf['Departement'].str[:2]                                  #只保留departement的前两位
            grouped = dfpf.groupby('department')['Hours_spent'].sum().reset_index()          #grouped 是分组以后的df
            st.text('总计工时：')
            st.text(dfpf['Hours_spent'].sum())
        # 查看分组后的结果
        # print(grouped)
            col21.dataframe(grouped)
        #画柱状图
            col22.bar_chart(grouped,x='department',y='Hours_spent')
        #画饼状图
            fig, ax = plt.subplots()
            ax.pie(grouped['Hours_spent'], labels=grouped['department'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # 确保饼状图是圆形的
        # 在 Streamlit 中展示图表
            col23.pyplot(fig)
    if menu_choice1 == '下单人':
        row1 = st.columns([1,1,1,7])
        row2 = st.columns(2)
        row3 = st.columns([2,4,4])
        col01 = row1[0]
        col02 = row1[1]
        col03 = row1[2]
        col11 = row2[0]
        col12 = row2[1]
        col21 = row3[0]
        col22 = row3[1]
        col23 = row3[2]
        button1 = col01.button("本年")
        button2 = col02.button("本月")
        button3 = col03.button("本周")
        start_date = datetime.now()
        end_date = datetime.now()
        if button1:
            # 获取本年第一天
            year_start = datetime(datetime.now().year, 1, 1)
            start_date = year_start
            end_date = datetime(datetime.now().year, 12, 31)
        elif button2:
            # 获取本月第一天
            this_month = datetime.now().month
            year = datetime.now().year
            month_start = datetime(year, this_month, 1)
            start_date = month_start
            if this_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
                end_date = datetime(year, this_month, 31)
            if this_month == 4 or 6 or 9 or 11:
                end_date = datetime(year, this_month, 30)
            if this_month == 2:
                end_date = datetime(year, this_month, 28)
        elif button3:
            # 获取本周第一天（这里以周一为一周开始）
            today = datetime.now()
            offset = today.weekday()
            week_start = today - timedelta(days=offset)
            start_date = week_start
            end_date = datetime.now()
        start_date2 = col11.date_input('Start Date', value=start_date)
        end_date2 = col12.date_input('End Date', value=end_date)
        if start_date2 > end_date2:
            st.write('Error! end_data need to be the future of the start data')
        else:
            dfp = pd.read_excel('demo_h.xlsx')
        # 根据单元格内容前两位进行分组
            dfpp = dfp[(df['Start date'] >= start_date2) & (df['End date'] <= end_date2)]   #根据时间进行筛选
            grouped = dfpp.groupby('Applicant')['Hours_spent'].sum().reset_index()          #grouped 是分组以后的df
            st.text('总计工时：')
            st.text(dfpp['Hours_spent'].sum())
        # 查看分组后的结果
        # print(grouped)
            col21.dataframe(grouped)
        #画柱状图
            col22.bar_chart(grouped,x='Applicant',y='Hours_spent')
        #画饼状图
            fig, ax = plt.subplots()
            ax.pie(grouped['Hours_spent'], labels=grouped['Applicant'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # 确保饼状图是圆形的
        # 在 Streamlit 中展示图表
            col23.pyplot(fig)


def main():
    menu = ['添加工单', '查看工单', '修改工单','查看日历', '分析工作时间',]
    sidebar = st.sidebar
    menu_choice = sidebar.radio('Choose an option', menu)
    if menu_choice == '添加工单':
        add_task()
    if menu_choice == '查看工单':
        see_list()
    if menu_choice == '修改工单':
        change_list()
    if menu_choice == '查看日历':
        calendar()
    if menu_choice == '分析工作时间':
        anay_time()



if __name__ == '__main__':

    main()