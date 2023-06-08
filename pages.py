import pandas as pd
from components import display_result, emptylines, header, input_prediction

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

    # UI
    header('Booking')
    emptylines(3)
    display_result()

def budgeting():
    '''Budgeting Page'''

    # UI
    header('Budgeting')
    input_prediction()
