import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd

# Read in the data
turndown_data = pd.read_csv("Turndowns.csv", names=['rtype', 'turndowndatetime', 'cocenter'])

#convert to dates
turndown_data['turndowndatetime'] = pd.to_datetime(turndown_data['turndowndatetime'])
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
filtered_data = turndown_data[(turndown_data['turndowndatetime'] >= start_date) & (turndown_data['turndowndatetime'] <= end_date) & (turndown_data['rtype'] == selected_rtype)]

# Calculate the count of occurances
count = filtered_data.shape[0]


st.markdown(f"<h1 style='text-align: center; color: black;'>The number of occurances of the selected rtype within the selected date range is: {count}</h1>", unsafe_allow_html=True)

st.table(filtered_data[['rtype', 'turndowndatetime']])