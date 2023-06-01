import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from datetime import datetime, timedelta



# Step 2: Load the allocation data from the CSV file and parse the date columns
#df = pd.read_csv("Resource Schedules.csv", names=["ckid", "resource", "rtype", "status", "startdate", "enddate", "actualdate"], parse_dates=["startdate", "enddate", "actualdate"])
df = pd.read_csv("Resource Schedules.csv", names=["ckid", "resource", "rtype", "status", "startdatetime", "enddatetime", "actualdate"])
#df["startdatetime"] = pd.to_datetime(df["startdatetime"], format="%d/%m/%Y %H:%M")
df['start_date_str'] = df['startdatetime'].str[:8]
df['end_date_str'] = df['enddatetime'].str[:8]
df['startdate']=pd.to_datetime(df['start_date_str'], format="%m/%d/%y" )
df['enddate']=pd.to_datetime(df['end_date_str'], format="%m/%d/%y" )
# Step 3: Create a Streamlit sidebar with date input controls
st.sidebar.header("Select date range")

min_date =  datetime.now()-timedelta(weeks=1)
max_date = datetime.now().date()

start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Step 4: Validate the date range
if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

# Step 5: Filter the dataset based on the selected date range
df_filtered = df[(df["startdate"].dt.date >= start_date) & (df["startdate"].dt.date <= end_date)]
resources_filtered = df_filtered.groupby('resource').size().reset_index(name="count")
ckDF = df_filtered.drop_duplicates(subset='ckid', keep='first')
ckDF.loc[:, 'resourceCount'] = df_filtered['ckid'].value_counts().reindex(ckDF['ckid']).values.copy()

ckDF.loc[:,'dow_start'] = ckDF['startdate'].dt.day_name()
ckDF.loc[:,'dow_end'] = ckDF['enddate'].dt.day_name()
ck_per_day_starts = ckDF.groupby('dow_start').size().reset_index(name='start_counts')
ck_per_day_ends = ckDF.groupby('dow_end').size().reset_index(name='end_counts')
resources_per_day_starts = ckDF.groupby('dow_start')['resourceCount'].sum().reset_index(name='resourcesStart')
resources_per_day_ends = ckDF.groupby('dow_end')['resourceCount'].sum().reset_index(name='resourcesEnd')

df_filtered.loc[:,'dow_start'] = df_filtered['startdate'].dt.day_name()
df_filtered.loc[:,'dow_end'] = df_filtered['enddate'].dt.day_name()
resources_per_day_starts = df_filtered.groupby('dow_start').size().reset_index(name='resourcesStart')
resources_per_day_ends = df_filtered.groupby('dow_end').size().reset_index(name='resourcesEnd')

ck_per_day_starts.rename(columns={'dow_start' : 'dow'}, inplace=True)
ck_per_day_ends.rename(columns={'dow_end' : 'dow'}, inplace=True)

resources_per_day_starts.rename(columns={'dow_start' : 'dow'}, inplace=True)
resources_per_day_ends.rename(columns={'dow_end' : 'dow'}, inplace=True)
merged_df = ck_per_day_starts.merge(ck_per_day_ends, on='dow')
merged_df = merged_df.merge(resources_per_day_starts.groupby('dow')['resourcesStart'].sum().reset_index(), on='dow')
merged_df = merged_df.merge(resources_per_day_ends.groupby('dow')['resourcesEnd'].sum().reset_index(), on='dow')
merged_df.fillna(0, inplace=True)

fig, ax = plt.subplots(figsize=(12, 8))

counts_start = merged_df["start_counts"].tolist()
counts_end = merged_df["end_counts"].tolist()

dates = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
merged_df.reindex(dates)
if not merged_df.empty:
    sorted_merged_df = merged_df.set_index('dow').loc[dates].reset_index()
    bar_width = 0.2
    r1 = range(len(dates))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    st.table(sorted_merged_df)

    ax.bar(r1, sorted_merged_df["start_counts"].tolist(), color="b", width=bar_width, label="Checkouts ")

    for i, v in enumerate(sorted_merged_df["start_counts"].tolist()):
        ax.text(r1[i], v, str(v), ha='center', va='bottom')

    ax.bar(r2, sorted_merged_df["end_counts"].tolist(), color="r", width=bar_width, label="Returns")
 
    for i, v in enumerate(sorted_merged_df["end_counts"].tolist()):
        ax.text(r2[i], v, str(v), ha='center', va='bottom')

    ax.plot(r1, sorted_merged_df['resourcesStart'].tolist(), color="brown", marker="o", label="Resources checked out")
 
    for i, v in enumerate(sorted_merged_df['resourcesStart'].tolist()):
        ax.annotate(str(v), (r1[i], v), xytext=(5, 5), textcoords='offset points', ha='center', va='bottom')

    ax.plot(r1, sorted_merged_df['resourcesEnd'].tolist(), color="black", marker="o", label="Resources checked in")

    for i, v in enumerate(sorted_merged_df['resourcesEnd'].tolist()):
        ax.annotate(str(v), (r1[i], v), xytext=(5, 5), textcoords='offset points', ha='center', va='bottom')

# Set labels and title
    ax.set_xlabel("Days of the Week", fontsize=12, fontweight="bold")
    ax.set_ylabel("Counts", fontsize=12, fontweight="bold")
    axis_font_props = fm.FontProperties(size=10)
    ax.set_title(f"Allocation Data ({start_date} to {end_date})", fontsize=14, fontweight="bold")
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=10)

# Set y-axis label size and style
    x_ticks = np.arange(len(dates))  # Create an array of tick positions
    x_ticks=([0, 1, 2, 3, 4])
    ax.tick_params(axis="y", labelsize=12)
    ax.tick_params(axis="x", labelsize=12)
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels([dates[i] for i in x_ticks])  # Use the custom order for tick labels
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)



