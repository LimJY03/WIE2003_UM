import pickle as pkl
import streamlit as st
import tensorflow as tf
import pandas as pd
from PIL import Image
from components import searchbar, header, emptylines, display_result

MAX_PER_PAGE = 10

# Loading dataset
df = pd.read_csv('./data/airbnb_data_clean.csv').iloc[:, 1:]

# Loading models
# nlp_model = 
reg_model = pkl.load(open('./model/model.pkl', 'rb'))

# Create pages
def home():
    header('Home')

def about():
    header('About')

def booking():

    header('Booking')

    search, sort_by = searchbar()

    query_result = df[df.apply(lambda row: search in row['name_of_listing'], axis=1)].sort_values(**sort_by)

    emptylines(3)
    display_result(query_result)

def budgeting():

    header('Budgeting')



# UI
with st.sidebar:

    st.title('Menu')
    page = st.radio('Navigate to', ['Home', 'About', 'Booking', 'Budgeting'])

# Select page
if page == 'Home': home()
elif page == 'About': about()
elif page == 'Booking': booking()
elif page == 'Budgeting': budgeting()
# else: home()
