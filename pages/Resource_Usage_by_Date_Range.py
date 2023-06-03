import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np

df = pd.read_csv("AprilMayAllocsTurndowns.csv", names=['ckid', 'resource', 'rtype', 'status', 'startdatetime', 'enddatetime', 'actualdatetime'])

df['startdatetime'] = pd.to_datetime(df['startdatetime']).dt.date
df['enddatetime'] = pd.to_datetime(df['enddatetime']).dt.date
df['actualdatetime'] = pd.to_datetime(df['actualdatetime']).dt.date

startDate = st.sidebar.date_input("Start Date")
endDate = st.sidebar.date_input("End Date")

uniqueRtypes = sorted(df['rtype'].unique(), key=lambda x: x.lower())
uniqueRtypes.insert(0, "All")

selectedRtype = st.sidebar.selectbox("Select an rtype", uniqueRtypes)

filteredData = df[(df['startdatetime'] >= startDate) & (df['startdatetime'] <= endDate)]
groupedData = filteredData.groupby('rtype').size().reset_index(name='Count')

count = filteredData.shape[0]
st.markdown(f"<h1 style='text-align: center; color: black;'>Occurances of selected Resource Type by Date Range</h1>", unsafe_allow_html=True)
st.markdown(f"**Usage for:** {selectedRtype}")

hide_table_row_index = """
            <style>
            table {width: 50% !important}
            thead tr th:first-child {display:none}
            thead th {font-weight: bold; color: blue; background-color: rgba(0, 0, 0, 0.10)}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)
groupedData = groupedData.rename(columns={'rtype': 'Resource Type'})
if selectedRtype != "All":
    st.table(groupedData[groupedData["Resource Type"] == selectedRtype])
st.markdown(f"**Most frequently used :** ")
sortedData = groupedData[['Resource Type', 'Count']].nlargest(10, 'Count').sort_values(by='Count', ascending=False)
st.table(sortedData)
st.markdown(f"**Least frequenctly used:**")
st.write(f"The total number of resource types with only one checkout is {len(groupedData[groupedData['Count'] == 1])}")
sorted_data = groupedData[['Resource Type', 'Count']].nsmallest(10, 'Count').sort_values(by='Count', ascending=True)
st.table(sorted_data)
