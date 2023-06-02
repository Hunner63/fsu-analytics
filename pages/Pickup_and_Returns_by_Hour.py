import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
from datetime import date

df = pd.read_csv("Resource Schedules.csv")
df.columns = ["ckid", "resources", "rtype", "status", "startdatetime_str", "enddatetime_str"]
# Convert datetime columns to datetime format
df['startdatetime'] = pd.to_datetime(df['startdatetime_str'], format="%m/%d/%y %I:%M %p")
df['enddatetime'] = pd.to_datetime(df['enddatetime_str'], format="%m/%d/%y %I:%M %p")
#Construct string of hours
df["start_time_str"] = df["startdatetime_str"].str[9:]
df['start_hour_str'] = df['start_time_str'].str.split(":").str[0]+":00 "+df['start_time_str'].str[-2:]
df["end_time_str"] = df["enddatetime_str"].str[9:]
df['end_hour_str'] = df['end_time_str'].str.split(":").str[0]+":00 "+df['end_time_str'].str[-2:]

# Filter to unique ckid
temp_df = df.drop_duplicates(subset='ckid', keep='first')

# Create a Streamlit sidebar for date range selection
st.sidebar.header("Date Range Selector")

# Set default date range values (one week before today and today)
default_end_date = pd.Timestamp.now().normalize()
default_start_date = default_end_date - pd.DateOffset(weeks=1)
start_date = st.sidebar.date_input("Start Date", value=datetime.today().date())
end_date = st.sidebar.date_input("End Date", value=datetime.today().date())

if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

filtered_df = temp_df[(temp_df["startdatetime"] >= pd.to_datetime(start_date)) & (temp_df["startdatetime"] <= pd.to_datetime(end_date))]

if filtered_df.empty:
    st.write("No data within selected date range.")
else:
    dedupedDF = filtered_df.drop_duplicates(subset='ckid', keep='first')
    filtered_df = filtered_df.dropna()
    grouped_resources_start = filtered_df.groupby('start_hour_str').size().reset_index(name="resources_start_counts")
    grouped_resources_start.rename(columns={'start_hour_str':'hour'}, inplace=True)
    grouped_resources_end = filtered_df.groupby('end_hour_str').size().reset_index(name="resources_end_counts")
    grouped_resources_end.rename(columns={'end_hour_str':'hour'}, inplace=True)
 
    grouped_allocs_start = dedupedDF.groupby('start_hour_str').size().reset_index(name="alloc_start_counts")
    grouped_allocs_start.rename(columns={'start_hour_str':'hour'}, inplace=True)
    grouped_allocs_end = dedupedDF.groupby('end_hour_str').size().reset_index(name="alloc_end_counts")
    grouped_allocs_end.rename(columns={'end_hour_str':'hour'}, inplace=True)

    filled_df = pd.DataFrame(columns=["hour"])
    filled_df['hour']=["7:00 AM", "8:00 AM","9:00 AM", "10:00 AM","11:00 AM", "12:00 PM","1:00 PM", "2:00 PM","3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM"]
    comb_resources_data = pd.merge(grouped_resources_start, grouped_resources_end, on='hour', how='outer')
    comb_resources_data = pd.merge(comb_resources_data, filled_df, on="hour", how="outer" )

    comb_resources_data = pd.merge(comb_resources_data, grouped_allocs_start, on="hour", how="outer" )
    comb_resources_data = pd.merge(comb_resources_data, grouped_allocs_end, on="hour", how="outer" )

    comb_resources_data = comb_resources_data.fillna(0)
    if comb_resources_data.empty:
        st.write("No data in comb_data")
    else:
        hours=['7:00 AM', '8:00 AM','9:00 AM', '10:00 AM','11:00 AM', '12:00 PM','1:00 PM', '2:00 PM','3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM']
        comb_resources_data = comb_resources_data.sort_values(by='hour', key=lambda x: pd.Categorical(x, categories=hours))
        fig, ax = plt.subplots(figsize=(12, 6))

        bar_width = 0.3
        space_between_bars = 0.05

        r1 = np.arange(len(comb_resources_data['hour']))
        r2 = r1 + bar_width + space_between_bars

        # Plot the lines for start counts and end counts
        ax.plot(r1, comb_resources_data['alloc_start_counts'], color='r', marker='o', label='Checkouts')
        ax.plot(r1, comb_resources_data['alloc_end_counts'], color='g', marker='o', label='Returns')

        # Plot the bars for start counts and end counts
        ax.bar(r1, comb_resources_data['resources_start_counts'], color='r', width=bar_width, label='Checked Resources')
        ax.bar(r2, comb_resources_data['resources_end_counts'], color='b', width=bar_width, label='Returned Resources')

        # Add text annotations for start counts and end counts
        for i, v in enumerate(comb_resources_data["alloc_start_counts"].tolist()):
            ax.text(r1[i], v, str(int(v)), ha='center', va='bottom')

        for i, v in enumerate(comb_resources_data["alloc_end_counts"].tolist()):
            ax.text(r1[i], v, str(int(v)), ha='center', va='bottom')

        # Add text annotations for resource counts
        for i, v in enumerate(comb_resources_data["resources_start_counts"].tolist()):
            ax.text(r1[i], v, str(int(v)), ha='center', va='bottom')

        for i, v in enumerate(comb_resources_data["resources_end_counts"].tolist()):
            ax.text(r2[i], v, str(int(v)), ha='center', va='bottom')

        # Set the x-axis tick positions and labels
        ax.set_xticks(r1 + bar_width / 2)
        ax.set_xticklabels(comb_resources_data['hour'], rotation=45, ha="right", fontsize=9)

        # Set the y-axis label
        ax.set_ylabel('Counts', fontsize=10, fontweight="bold")
        ax.set_xlabel('Hours', fontsize=10, fontweight="bold")

        # Set the title and legend
        ax.set_title('Allocation Counts by Hour of the Day', fontsize=18, fontweight="bold")
        ax.legend(loc='upper right')

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
