import streamlit as st
from pages import home, dist, booking_assistant, booking, budgeting, about

# Config
st.set_page_config(
    page_title="US Airbnb",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Select page
page_info = {
    'Home': home,
    'Airbnb Distributions': dist,
    'Booking Assistant': booking_assistant,
    'Booking': booking,
    'Budgeting': budgeting,
    'About': about,
}

# UI
with st.sidebar:

    st.title('Menu')
    page = st.radio('Navigate to', page_info.keys())

page_info[page]()
