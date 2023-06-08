import pandas as pd
from components import *

def home():
    '''Home Page'''

    # UI
    header('Home')

def about():
    '''About Page'''

    # UI
    header('About')

def booking():
    '''Booking Page'''

    df = pd.read_csv('./data/airbnb_data_clean.csv').iloc[:, 1:]

    # UI
    header('Booking')

    search, sort_by = searchbar()
   
    query_result = df[df.apply(lambda row: search in row['name_of_listing'], axis=1)].sort_values(**sort_by)

    emptylines(3)

    display_result(query_result)

def budgeting():
    '''Budgeting Page'''

    # UI
    header('Budgeting')
    input_prediction()
