import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from datetime import datetime, timedelta

df = pd.read_csv("Resource Schedules.csv", names=["ckid", "resource", "rtype", "status", "startdatetime", "enddatetime", "actualdate"])
df['start_date_str'] = df['startdatetime'].str[:8]
df['end_date_str'] = df['enddatetime'].str[:8]
df['startDate']=pd.to_datetime(df['start_date_str'], format="%m/%d/%y" )
df['endDate']=pd.to_datetime(df['end_date_str'], format="%m/%d/%y" )

st.sidebar.header("Select date range")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

dateRangeResourcesDF = df[ ((df["startDate"].dt.date >= start_date) & (df["startDate"].dt.date <= end_date)) | ((df["endDate"].dt.date >= start_date) & (df["endDate"].dt.date <= end_date)) ].copy()
dateRangeResourcesDF['dowStart'] = dateRangeResourcesDF['startDate'].dt.day_name()
dateRangeResourcesDF['dowEnd'] = dateRangeResourcesDF['endDate'].dt.day_name()
st.table(dateRangeResourcesDF.reset_index(drop=True))
resourcesPickupsDF = dateRangeResourcesDF.groupby('dowStart').size().reset_index(name='rStarts')
resourcesPickupsDF.rename(columns={'dowStart': 'dow'}, inplace=True)
resourcesReturnsDF = dateRangeResourcesDF.groupby('dowEnd').size().reset_index(name='rEnds')
resourcesReturnsDF.rename(columns={'dowEnd': 'dow'}, inplace=True)
dateRangeAllocsDF = dateRangeResourcesDF.drop_duplicates(subset='ckid', keep='first').copy()
allocsPickupsDF = dateRangeAllocsDF.groupby('dowStart').size().reset_index(name='aStarts')
allocsPickupsDF.rename(columns={'dowStart': 'dow'}, inplace=True)
allocsReturnsDF = dateRangeAllocsDF.groupby('dowEnd').size().reset_index(name='aEnds')
allocsReturnsDF.rename(columns={'dowEnd': 'dow'}, inplace=True)

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
existing_days = resourcesPickupsDF['dow']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dow': list(missing_days), 'rStarts': 0})
resourcesPickupsDF = pd.concat([resourcesPickupsDF, missing_df], ignore_index=True)
existing_days = resourcesReturnsDF['dow']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dow': list(missing_days), 'rEnds': 0})
resourcesReturnsDF = pd.concat([resourcesReturnsDF, missing_df], ignore_index=True)
existing_days = allocsPickupsDF['dow']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dow': list(missing_days), 'aStarts': 0})
allocsPickupsDF = pd.concat([allocsPickupsDF, missing_df], ignore_index=True)
existing_days = allocsReturnsDF['dow']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dow': list(missing_days), 'aEnds': 0})
allocsReturnsDF = pd.concat([allocsReturnsDF, missing_df], ignore_index=True)
mergedDF = pd.merge(resourcesPickupsDF, resourcesReturnsDF, on='dow', how='outer')
mergedDF = pd.merge(mergedDF, allocsPickupsDF, on='dow', how='outer')
mergedDF = pd.merge(mergedDF, allocsReturnsDF, on='dow', how='outer')
print("pre re-index", mergedDF)
desired_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
mergedDF = mergedDF.set_index('dow').loc[desired_order].reset_index()
print("post", mergedDF)

if (resourcesPickupsDF['rStarts'] == 0).all():
    st.write("No data to display within the date range.")
else:
    fig, ax = plt.subplots(figsize=(11, 7))
    bar_width = 0.3
    space_between_bars = 0.05
    r1 = np.arange(len(days_of_week))
    r2 = [x + bar_width + space_between_bars for x in r1]
    offset = 1.0
    ax.bar(r1, mergedDF['aStarts'].tolist(), color="b", width=bar_width, label="Checkouts")
    for i, v in enumerate(mergedDF['aStarts'].tolist()):
        ax.text(r1[i], v+offset, str(v), ha='center', va='bottom')
    ax.bar(r2, mergedDF['aEnds'].tolist(), color="r", width=bar_width, label="Returns")
    for i, v in enumerate(mergedDF['aEnds'].tolist()):
        ax.text(r2[i], v+offset, str(v), ha='center', va='bottom')
    ax.plot(r1, mergedDF["rStarts"].tolist(), color="b", label="Resources Checked Out", marker="o")
    for i, v in enumerate(mergedDF['rStarts'].tolist()):
        ax.text(r1[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))
    ax.plot(r2, mergedDF["rEnds"].tolist(), color="r", label="Resources Checked In", marker="o")
    for i, v in enumerate(mergedDF['rEnds'].tolist()):
        ax.text(r2[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))

    ax.set_xticks([x + bar_width / 2 for x in r1])
    ax.set_xticklabels(days_of_week, rotation=0, ha="center")

    ax.set_title('Pickups and Returns by Day of the Week', fontsize=18, fontweight="bold")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.035), fancybox=True, shadow=True, ncol=5)
    
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
