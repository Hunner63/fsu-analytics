import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Load the allocation data from the CSV file
df = pd.read_csv("AprilMayAllocsTurndowns.csv")
df.columns = ["ckid", "resources", "rtype", "status", "startdatetime", "enddatetime", "actualdatetime"]

# Convert datetime columns to datetime format
df["startdatetime"] = pd.to_datetime(df["startdatetime"])
df["enddatetime"] = pd.to_datetime(df["enddatetime"])
df["actualdatetime"] = pd.to_datetime(df["actualdatetime"])

# Filter to unique ckid
temp_df = df.drop_duplicates(subset='ckid', keep='first')

# Create a Streamlit sidebar for date range selection
st.sidebar.header("Date Range Selector")

# Set default date range values (one week before today and today)
default_end_date = pd.Timestamp.now().normalize()
default_start_date = default_end_date - pd.DateOffset(weeks=1)

# Select start and end dates
start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", default_end_date)

# Validate the date range
if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

# Filter the DataFrame based on the selected date range
filtered_df = temp_df[(temp_df["startdatetime"].dt.date >= start_date) & (temp_df["startdatetime"].dt.date <= end_date)]
# Display "No data within selected date range" if there is no data in the date range
if filtered_df.empty:
    st.write("No data within selected date range.")
else:
    # Group the DataFrame by ckid and hour for startdatetime, enddatetime, and actualdatetime
    filtered_df['starthour'] = filtered_df["startdatetime"].dt.hour
    filtered_df['endhour'] = filtered_df["enddatetime"].dt.hour
    filtered_df['actualhour'] = filtered_df["actualdatetime"].dt.hour
    grouped_start = filtered_df.groupby('starthour').size().reset_index(name="start_counts")
    grouped_start.rename(columns={'starthour':'hour'}, inplace=True)
    grouped_end = filtered_df.groupby('endhour').size().reset_index(name="end_counts")
    grouped_end.rename(columns={'endhour':'hour'}, inplace=True)
    grouped_actual = filtered_df.groupby('actualhour').size().reset_index(name="actual_counts")
    grouped_actual.rename(columns={'actualhour':'hour'}, inplace=True)
    # Combine the grouped dataframes into a single dataframe
    comb_data = pd.merge(grouped_start, grouped_end, on='hour', how='outer')
    comb_data = pd.merge(comb_data, grouped_actual, on='hour', how='outer')
  
    if comb_data.empty:
        st.write("No data in comb_data")
    else:
        comb_data = comb_data.sort_values('hour')
        #  comb_data['hour'] = pd.to_datetime(comb_data['hour'], format='%H')
        # Create the figure and axes for the combo bar graph
        comb_data['hour']= comb_data['hour'].astype(str) + ":00"
        fig, ax = plt.subplots(figsize=(12, 6))

        # Set the width of each bar
        bar_width = 0.2

        # Set the positions for the bars
        r1 = range(len(comb_data['hour']))
        r2 = [x + bar_width for x in r1]
        r3 = [x + bar_width for x in r2]

        # Plot the bars for start counts, end counts, and actual counts
        ax.bar(r1, comb_data['start_counts'], color='b', width=bar_width, label='Scheduled checkout times')
        ax.bar(r2, comb_data['end_counts'], color='r', width=bar_width, label='Scheduled return times')
        ax.bar(r3, comb_data['actual_counts'], color='g', width=bar_width, label='Actual return time')

        # Set the x-axis tick positions and labels
        ax.set_xticks([r + bar_width for r in range(len(comb_data['hour']))])
        ax.set_xticklabels(comb_data['hour'], rotation=45, ha="right", fontsize=14)

        # Set the y-axis label
        ax.set_ylabel('Counts')
        ax.set_xlabel('Hours')

        #date_formatter = mdates.DateFormatter('%I:00 %p')  # Format as "HH:00 AM/PM"
        #ax.xaxis.set_major_formatter(date_formatter)


        # Set the title and legend
        ax.set_title('Allocation Counts by Hour of the Day')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Display the combo bar graph
        st.pyplot(fig)