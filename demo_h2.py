import streamlit as st
import pandas as pd


excel_file = 'C:\demo\demo_h.xlsx'

df = pd.read_excel(excel_file)

st.dataframe(df)