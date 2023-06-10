from components import header, recommendation_form, show_3d_map, emptylines, display_result, input_prediction

def home():
    '''Home Page'''

    # UI
    header('Home')


def dist():
    '''Show airbnb distribution by city'''
    
    # UI
    header('Airbnb Distribution')
    show_3d_map()

def booking_assistant():
    '''Recommendation Page'''

    # UI
    header('Booking Assistant')
    recommendation_form()

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


def about():
    '''About Page'''

    # UI
    header('About')
