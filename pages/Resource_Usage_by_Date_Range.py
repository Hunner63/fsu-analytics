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
filtered_data = data[(data['startdatetime'] >= start_date) & (data['startdatetime'] <= end_date) & (data['rtype'] == selected_rtype)]

# Calculate the count of occurances
count = filtered_data.shape[0]

st.markdown(f"<h1 style='text-align: center; color: black;'>The number of occurances of the selected rtype within the selected date range is: {count}</h1>", unsafe_allow_html=True)

st.table(filtered_data[['ckid', 'startdatetime']])