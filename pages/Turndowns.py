import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd

# Read in the data
url = "https://webcheckout.fanshawec.ca/feeds/14months-present-turndown-report-fanshawec-Yd2SKaiN.csv"
turndown_data = pd.read_csv(url)

turndown_data.rename(columns={'TRANSITION-TIME': 'turndowndatetime'}, inplace=True)
turndown_data.rename(columns={'RESOURCE-TYPE.NAME': 'rtype'}, inplace=True)
turndown_data['turndowndatetime'] = pd.to_datetime(turndown_data['turndowndatetime'], errors='coerce')
turndown_data['turndowndatetime'] = turndown_data['turndowndatetime'].dt.date

# Create a date range selector
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Create a list of unique rtypes
unique_rtypes = turndown_data['rtype'].unique()
unique_rtypes = turndown_data.sort_values('rtype')['rtype']

# Select the rtype
selected_rtype = st.sidebar.selectbox("Select an rtype", unique_rtypes)

# Filter the data based on the date range and rtype
filtered_rtype_data = turndown_data[(turndown_data['turndowndatetime'] >= start_date) & (turndown_data['turndowndatetime'] <= end_date) & (turndown_data['rtype'] == selected_rtype)]
filtered_data = turndown_data[(turndown_data['turndowndatetime'] >= start_date) & (turndown_data['turndowndatetime'] <= end_date)]
grouped_selected_data = filtered_rtype_data.groupby("rtype").size().reset_index(name='Counts')
grouped_data = filtered_data.groupby("rtype").size().reset_index(name='Counts')

# Calculate the count of occurances
count = filtered_data.shape[0]

st.markdown(f"<h1 style='text-align: center; color: black;'>Turndowns of selected rtype within date range: </h1>", unsafe_allow_html=True)
hide_table_row_index = """
            <style>
            table {width: 50% !important}
            thead tr th:first-child {display:none}
            thead th {font-weight: bold; color: blue; background-color: rgba(0, 0, 0, 0.10)}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)
grouped_data = grouped_data.rename(columns={'rtype': 'Resource Type'})
grouped_selected_data = grouped_data.rename(columns={'rtype': 'Resource Type'})
st.table(grouped_data[grouped_data['Resource Type'] == selected_rtype])
st.table(grouped_data.nlargest(10, 'Counts').sort_values(by='Counts', ascending=False))

