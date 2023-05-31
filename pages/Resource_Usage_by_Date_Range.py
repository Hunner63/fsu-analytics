import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd

# Read in the data
data = pd.read_csv("AprilMayAllocsTurndowns.csv", names=['ckid', 'resource', 'rtype', 'status', 'startdatetime', 'enddatetime', 'actualdatetime'])

#convert to dates
data['startdatetime'] = pd.to_datetime(data['startdatetime'])
data['startdatetime'] = data['startdatetime'].dt.date
data['enddatetime'] = pd.to_datetime(data['enddatetime'])
data['enddatetime'] = data['enddatetime'].dt.date
data['actualdatetime'] = pd.to_datetime(data['actualdatetime'])
data['actualdatetime'] = data['actualdatetime'].dt.date

# Create a date range selector
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Create a list of unique rtypes
unique_rtypes = data['rtype'].unique()
unique_rtype = data.sort_values('rtype')['rtype']

# Select the rtype
selected_rtype = st.sidebar.selectbox("Select an rtype", unique_rtypes)

# Filter the data based on the date range and rtype
filtered_type_data = data[(data['startdatetime'] >= start_date) & (data['startdatetime'] <= end_date) & (data['rtype'] == selected_rtype)]
filtered_data = data[(data['startdatetime'] >= start_date) & (data['startdatetime'] <= end_date)]
grouped_data = filtered_data.groupby('rtype').size().reset_index(name='Turndowns')

# Calculate the count of occurances
count = filtered_type_data.shape[0]
st.markdown(f"<h1 style='text-align: center; color: black;'>Occurances of selected Resource Type by Date Range</h1>", unsafe_allow_html=True)
#st.table(filtered_type_data[['ckid', 'startdatetime']])
#st.write("Usage for:", selected_rtype)
st.markdown(f"**Usage for:** {selected_rtype}")

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
st.table(grouped_data[grouped_data["Resource Type"] == selected_rtype])
st.markdown(f"**Most used items:** {selected_rtype}")
sorted_data = grouped_data[['Resource Type', 'Turndowns']].nlargest(10, 'Turndowns').sort_values(by='Turndowns', ascending=False)
st.table(sorted_data)
st.markdown(f"**ULeast used items:** {selected_rtype}")
#st.write(sorted_data['rtype'], sorted_data['counts'])
sorted_data = grouped_data[['Resource Type', 'Turndowns']].nsmallest(10, 'Turndowns').sort_values(by='Turndowns', ascending=True)
st.table(sorted_data)
