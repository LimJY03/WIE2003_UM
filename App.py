import streamlit as st
from pages import home, about, booking, budgeting

# UI
with st.sidebar:

    st.title('Menu')
    page = st.radio('Navigate to', ['Home', 'About', 'Booking', 'Budgeting'])

# Select page
page_info = {
    'Home': home,
    'About': about,
    'Booking': booking,
    'Budgeting': budgeting
}
page_info[page]()
