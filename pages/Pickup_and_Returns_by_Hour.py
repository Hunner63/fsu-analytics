import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
from datetime import date

url = "https://webcheckout.fanshawec.ca/feeds/14months-present-rs-schedules-fanshawec-FtwDpq7N.csv"
df = pd.read_csv(url)
#df.columns = ["ckid", "resources", "rtype", "status", "startdatetime_str", "enddatetime_str"]
# Convert datetime columns to datetime format
#df['REAL-START-TIME'] = pd.to_datetime(df['REAL-START-TIME'], format="%m/%d/%Y %I:%M %p")
#df['REAL-END-TIME'] = pd.to_datetime(df['REAL-END-TIME'], format="%m/%d/%Y %I:%M %p")
#Construct string of hours
#df['realStartStr'] = pd.to_datetime(df['REAL-START-TIME'].astype(str), format="%Y-%m-%d %H:%M:%S")
#df['realStartStr'] = df['REAL-START-TIME'].dt.strftime("%Y-%m-%d %I:%M:%S %p")
df["realStartStr"] = df['REAL-START-TIME'].str[11:]
df['startHour'] = df['realStartStr'].str.split(":").str[0]+":00 " +df['realStartStr'].str[-2:]
#df.dropna(subset=['startHour'], inplace=True)
#statement below contains meridian
#df['startHour'] = df['realStartStr'].str.split(":").str[0]+":00 "+df['realStartStr'].str[-2:]
#df['realEndStr'] = df['REAL-END-TIME'].dt.strftime("%Y-%m-%d %I:%M:%S %p")
df["realEndStr"] = df['REAL-END-TIME'].str[11:]
df['endHour'] = df['realEndStr'].str.split(":").str[0]+":00 " +df['realEndStr'].str[-2:]

#df["REAL-END-TIME"] = df["REAL-END-TIME"].str[9:]
#df['endHour'] = df['REAL-END-TIME'].str.split(":").str[0]+":00 "+df['end_time_str'].str[-2:]
#breakpoint()
st.sidebar.header("Date Range Selector")

# Set default date range values (one week before today and today)
default_end_date = pd.Timestamp.now().normalize()
default_start_date = default_end_date - pd.DateOffset(weeks=1)
start_date = st.sidebar.date_input("Start Date", value=datetime.today().date())
end_date = st.sidebar.date_input("End Date", value=datetime.today().date())

if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

resourcesFilteredDF = df[(pd.to_datetime(df["REAL-START-TIME"]) >= pd.to_datetime(start_date)) & (pd.to_datetime(df["REAL-START-TIME"]) <= pd.to_datetime(end_date)) | (pd.to_datetime(df["REAL-END-TIME"]) >= pd.to_datetime(start_date)) & (pd.to_datetime(df["REAL-END-TIME"]) <= pd.to_datetime(end_date))].copy()

if resourcesFilteredDF.empty:
    st.write("No data within selected date range.")
else:
    resourcesStartGrouped = resourcesFilteredDF.groupby('startHour').size().reset_index(name="startCount")
    resourcesEndGrouped = resourcesFilteredDF.groupby('endHour').size().reset_index(name="endCount")
    allocsFilteredDF = resourcesFilteredDF.drop_duplicates(subset='ALLOCATION.NAME', keep='first').copy()
    allocsStartGrouped = allocsFilteredDF.groupby('startHour').size().reset_index(name="startCount")
    allocsEndGrouped = allocsFilteredDF.groupby('endHour').size().reset_index(name="endCount")
   
    if (resourcesStartGrouped['startCount'] == 0).all():
        st.write("No data within selected date range")
    else:
        desiredHours=['7:00 AM', '8:00 AM','9:00 AM', '10:00 AM','11:00 AM', '12:00 PM','1:00 PM', '2:00 PM','3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM']
        missing_values = set(desiredHours) - set(resourcesStartGrouped['startHour'])
        if missing_values:
            missing_rows = pd.DataFrame({'startHour': list(missing_values), 'startCount': 0})
            resourcesStartGrouped = pd.concat([resourcesStartGrouped, missing_rows]).sort_values(by='startHour', key=lambda x: pd.Categorical(x, categories=desiredHours))
     
        missing_values = set(desiredHours) - set(resourcesEndGrouped['endHour'])
        if missing_values:
            missing_rows = pd.DataFrame({'endHour': list(missing_values), 'endCount': 0})
            resourcesEndGrouped = pd.concat([resourcesEndGrouped, missing_rows]).sort_values(by='endHour', key=lambda x: pd.Categorical(x, categories=desiredHours))

        missing_values = set(desiredHours) - set(allocsStartGrouped['startHour'])
        if missing_values:
            missing_rows = pd.DataFrame({'startHour': list(missing_values), 'startCount': 0})
            allocsStartGrouped = pd.concat([allocsStartGrouped, missing_rows]).sort_values(by='startHour', key=lambda x: pd.Categorical(x, categories=desiredHours))

        missing_values = set(desiredHours) - set(allocsEndGrouped['endHour'])
        if missing_values:
            missing_rows = pd.DataFrame({'endHour': list(missing_values), 'endCount': 0})
            allocsEndGrouped = pd.concat([allocsEndGrouped, missing_rows]).sort_values(by='endHour', key=lambda x: pd.Categorical(x, categories=desiredHours))
    
        fig, ax = plt.subplots(figsize=(12, 6))
        bar_width = 0.3
        space_between_bars = 0.05
        offset = 1.0
        r1 = np.arange(len(list(desiredHours)))
        r2 = r1 + bar_width + space_between_bars
 
        ax.plot(r1, resourcesStartGrouped['startCount'].to_list(), color='r', label='Checked out Resources', marker="o")
        for i, v in enumerate(resourcesStartGrouped['startCount'].tolist()):
            ax.text(r1[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))
        ax.plot(r2, resourcesEndGrouped['endCount'].to_list(), color='b', label='Returned Resources')
        for i, v in enumerate(resourcesEndGrouped['endCount'].tolist()):
            ax.text(r2[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))
        ax.bar(r1, allocsStartGrouped['startCount'].to_list(), color='r', width=bar_width, label='Allocations going out')
        for i, v in enumerate(allocsStartGrouped['startCount'].tolist()):
            ax.text(r1[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))
        ax.bar(r2, allocsEndGrouped['endCount'].to_list(), color='b', width=bar_width, label='Allocations returned')
        for i, v in enumerate(allocsEndGrouped['endCount'].tolist()):
            ax.text(r2[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))

        ax.set_xticks(range(len(desiredHours)))
        ax.set_xticklabels(desiredHours, rotation=45, ha='right')
        ax.set_title('Pickups and Returns by Hour of the Day', fontsize=18, fontweight="bold")
        ax.legend(loc='upper right')

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)


    #     # Plot the bars for start counts and end counts

    #     offset=2.0
    #     # Add text annotations for start counts and end counts
    #     for i, v in enumerate(comb_resources_data["alloc_start_counts"].tolist()):
    #         ax.text(r1[i], v+offset, str(int(v)), ha='center', va='bottom')

    #     for i, v in enumerate(comb_resources_data["alloc_end_counts"].tolist()):
    #         ax.text(r2[i], v+offset, str(int(v)), ha='center', va='bottom')

    #     for i, v in enumerate(comb_resources_data["resources_start_counts"].tolist()):
    #         ax.text(r1[i], v+offset, str(int(v)), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))

    #     for i, v in enumerate(comb_resources_data["resources_end_counts"].tolist()):
    #         ax.text(r2[i], v+offset, str(int(v)), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))

    #     # Set the x-axis tick positions and labels
    #     ax.set_xticks(r1 + bar_width / 2)
    #     ax.set_xticklabels(comb_resources_data['hour'], rotation=45, ha="right", fontsize=9)

    #     # Set the y-axis label
    #     ax.set_ylabel('Counts', fontsize=10, fontweight="bold")
    #     ax.set_xlabel('Hours', fontsize=10, fontweight="bold")

    #     # Set the title and legend
    #     ax.set_title('Allocation Counts by Hour of the Day', fontsize=18, fontweight="bold")
    #     ax.legend(loc='upper right')

