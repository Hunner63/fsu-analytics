import streamlit as st
from PIL import Image

#import streamlit as st
#rom pickups_date_range.py import pickups_date_range
#from returns_date_range.py import returns_date_range
#from pickups_hour.py import pickups_hour
#from returns_hour.py import returns_hour
#from turndowns.py import turndowns

#PAGES = {
#    "Pickups and Returns by Date Range" : pickups_date_range,
#    "Returns by Date Range" : returns_date_range,
#    "Pickups by Hour of Day": pickups_hour,
#    "Returns by Hour of Day": returns_hour,
#    "Turndowns by date range": turndowns
#}

# Load the image
image = Image.open("fanshawe.png")
wco_logo = Image.open("wco_logo.jpg")

# Center the content
st.markdown(
    """
    <style>
    .reportview-container .main {
        flex: 0;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the image
st.image(image, use_column_width=True)

# Display the title "Circulation Analytics" in 24pt bold
st.markdown("<h1 style='text-align: center; font-size: 24px; font-weight: bold;'>Franshawe Circulation Analytics</h1>", unsafe_allow_html=True)

# Display the prompt "Select a report on the left" in 14pt
st.markdown("<p style='text-align: center; font-size: 16px;'>Select a report on the left</p>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .reportview-container .main {
        flex: 0;
        margin-left: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.image(wco_logo, use_column_width=True)

