import streamlit as st
from pages import home, dist, booking, budgeting, about

# Select page
page_info = {
    'Home': home,
    'Airbnb Distributions': dist,
    'Booking': booking,
    'Budgeting': budgeting,
    'About': about,
}

# UI
with st.sidebar:

    st.title('Menu')
    page = st.radio('Navigate to', page_info.keys())

page_info[page]()
