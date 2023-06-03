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

dateRangeResourcesDF = df[(df["startDate"].dt.date >= start_date) & (df["startDate"].dt.date <= end_date)].copy()
dateRangeResourcesDF['dowStart'] = dateRangeResourcesDF['startDate'].dt.day_name()
dateRangeResourcesDF['dowEnd'] = dateRangeResourcesDF['endDate'].dt.day_name()
resourcesPickupsDF = dateRangeResourcesDF.groupby('dowStart').size().reset_index(name='startCount')
resourcesReturnsDF = dateRangeResourcesDF.groupby('dowEnd').size().reset_index(name='endCount')
dateRangeAllocsDF = dateRangeResourcesDF.drop_duplicates(subset='ckid', keep='first')
allocsPickupsDF = dateRangeAllocsDF.groupby('dowStart').size().reset_index(name='startCount')
allocsReturnsDF = dateRangeAllocsDF.groupby('dowEnd').size().reset_index(name='endCount')

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
existing_days = resourcesPickupsDF['dowStart']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dowStart': list(missing_days), 'startCount': 0})
resourcesPickupsDF = pd.concat([resourcesPickupsDF, missing_df], ignore_index=True)
existing_days = resourcesReturnsDF['dowEnd']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dowEnd': list(missing_days), 'endCount': 0})
resourcesReturnsDF = pd.concat([resourcesReturnsDF, missing_df], ignore_index=True)
existing_days = allocsPickupsDF['dowStart']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dowStart': list(missing_days), 'startCount': 0})
allocsPickupsDF = pd.concat([allocsPickupsDF, missing_df], ignore_index=True)
existing_days = allocsReturnsDF['dowEnd']
missing_days = set(days_of_week) - set(existing_days)
missing_df = pd.DataFrame({'dowEnd': list(missing_days), 'endCount': 0})
allocsReturnsDF = pd.concat([allocsReturnsDF, missing_df], ignore_index=True)

if (resourcesPickupsDF['startCount'] == 0).all():
    st.write("No data to display within the date range.")
else:
    custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
 #   resourcesPickupsDF['dowStart'] = pd.Categorical(resourcesPickupsDF['dowStart'], categories=custom_order, ordered=True)
 #   resourcesPickupsDF['dowStart'] = resourcesPickupsDF['dowStart'].cat.reorder_categories(custom_order)
 #   resourcesReturnsDF['dowEnd'] = pd.Categorical(resourcesReturnsDF['dowEnd'], categories=custom_order, ordered=True)
 #   resourcesReturnsDF['dowEnd'] = resourcesReturnsDF['dowEnd'].cat.reorder_categories(custom_order)
 #   allocsPickupsDF['dowStart'] = pd.Categorical(allocsPickupsDF['dowStart'], categories=custom_order, ordered=True)
 #   allocsPickupsDF['dowStart'] = allocsPickupsDF['dowStart'].cat.reorder_categories(custom_order)
 #   allocsReturnsDF['dowEnd'] = pd.Categorical(allocsReturnsDF['dowEnd'], categories=custom_order, ordered=True)
 #   allocsReturnsDF['dowEnd'] = allocsReturnsDF['dowEnd'].cat.reorder_categories(custom_order)
    fig, ax = plt.subplots(figsize=(11, 7))
    bar_width = 0.3
    space_between_bars = 0.05  
    r1 = range(len(resourcesPickupsDF['dowStart']))
    r2 = [x + bar_width + space_between_bars for x in r1]

    offset = 2.0
    ax.bar(r1, allocsPickupsDF['startCount'].tolist(), color="b", width=bar_width, label="Checkouts")
    for i, v in enumerate(allocsPickupsDF['startCount'].tolist()):
        ax.text(r1[i], v, str(v), ha='center', va='bottom')
    ax.bar(r2, allocsReturnsDF['endCount'].tolist(), color="r", width=bar_width, label="Returns")
    for i, v in enumerate(allocsReturnsDF['endCount'].tolist()):
        ax.text(r2[i], v, str(v), ha='center', va='bottom')
    ax.plot(r1, resourcesPickupsDF["startCount"].tolist(), color="b", label="Resources Checked Out", marker="o")
    for i, v in enumerate(resourcesPickupsDF['startCount'].tolist()):
        ax.text(r1[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))
    ax.plot(r2, resourcesReturnsDF["endCount"].tolist(), color="r", label="Resources Checked In", marker="o")
    for i, v in enumerate(resourcesReturnsDF['endCount'].tolist()):
        ax.text(r2[i], v+offset, str(v), ha='center', va='bottom', fontsize=9, color='white', bbox=dict(facecolor='black', edgecolor='none', pad=0.3))

    ax.set_xticks(range(len(custom_order)))
    ax.set_xticklabels(custom_order, rotation=45, ha="right")

    ax.set_title('Pickups and Returns by Day of the Week', fontsize=18, fontweight="bold")
    ax.legend(loc='upper right')

    st.pyplot(fig, use_container_width=True)

