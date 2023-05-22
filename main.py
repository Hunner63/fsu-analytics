import streamlit as st
from PIL import Image

# Load the image
image = Image.open("fanshawe.png")

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
st.markdown("<h1 style='text-align: center; font-size: 24px; font-weight: bold;'>Circulation Analytics</h1>", unsafe_allow_html=True)

# Display the prompt "Select a report on the left" in 14pt
st.markdown("<p style='text-align: center; font-size: 14px;'>Select a report on the left</p>", unsafe_allow_html=True)
