import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# Step 2: Load the allocation data from the CSV file and parse the date columns
df = pd.read_csv("AprilMayAllocsTurndowns.csv", names=["ckid", "resource", "rtype", "status", "startdate", "enddate", "actualdate"], parse_dates=["startdate", "enddate", "actualdate"])

# Step 3: Create a Streamlit sidebar with date input controls
st.sidebar.header("Select date range")
min_date = df["startdate"].min().date()
max_date = df["enddate"].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Step 4: Validate the date range
if start_date > end_date:
    st.sidebar.error("Invalid date range.")
    st.stop()

# Step 5: Filter the dataset based on the selected date range
df_filtered = df[(df["startdate"].dt.date >= start_date) & (df["enddate"].dt.date <= end_date)]
resources_filtered = df_filtered

deduped_df = df_filtered.drop_duplicates(subset='ckid', keep='first')
# Step 6: Group the filtered data by day and count occurrences for each date column
df_grouped = deduped_df.groupby(pd.Grouper(key="startdate", freq="D")).size().reset_index(name="counts_start")
df_grouped["counts_end"] = deduped_df.groupby(pd.Grouper(key="enddate", freq="D")).size().reset_index(drop=True)
df_grouped["counts_actual"] = deduped_df.groupby(pd.Grouper(key="actualdate", freq="D")).size().reset_index(drop=True)
df_grouped["resources_start_count"] = resources_filtered.groupby(pd.Grouper(key="startdate", freq="D")).size().reset_index(drop=True)
df_grouped["resources_end_count"] = resources_filtered.groupby(pd.Grouper(key="enddate", freq="D")).size().reset_index(drop=True)
# Step 7: Merge the grouped dataframes and fill missing values with zero
df_grouped.fillna(0, inplace=True)
# Step 8: Create a bar chart to visualize the counts of allocations for each date column
fig, ax = plt.subplots(figsize=(12, 8))

dates = df_grouped["startdate"].dt.strftime("%Y-%m-%d").tolist()
counts_start = df_grouped["counts_start"].tolist()
counts_end = df_grouped["counts_end"].tolist()
counts_actual = df_grouped["counts_actual"].tolist()
resource_counts_start = df_grouped['resources_start_count'].tolist()
resource_counts_end = df_grouped['resources_end_count'].tolist()

bar_width = 0.2
r1 = range(len(dates))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

ax.bar(r1, counts_start, color="b", width=bar_width, label="Checkouts ")
ax.bar(r2, counts_end, color="r", width=bar_width, label="Returns")
ax.bar(r3, counts_actual, color="g", width=bar_width, label="Reservations")
ax.plot(r1, resource_counts_start, label="Resources Checked Out")
ax.plot(r1, resource_counts_end, label="Resources Returned")

# Set labels and title
ax.set_xlabel("Date Range", fontsize=12, fontweight="bold")
ax.set_ylabel("Counts", fontsize=12, fontweight="bold")
axis_font_props = fm.FontProperties(size=10)
ax.set_title(f"Allocation Data ({start_date} to {end_date})", fontsize=14, fontweight="bold")

# Set x-axis tick labels
ax.set_xticks([r + bar_width for r in range(len(dates))])
ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=10)

# Set y-axis label size and style
ax.tick_params(axis="y", labelsize=12)
ax.tick_params(axis="x", labelsize=12)

# Display legend
ax.legend()

# Adjust spacing
plt.tight_layout()

# Step 9: Display the chart in the Streamlit app
st.pyplot(fig, use_container_width=True)
