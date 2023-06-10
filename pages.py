from components import header, show_3d_map, emptylines, display_result, input_prediction

def home():
    '''Home Page'''

    # UI
    header('Home')

def about():
    '''About Page'''

    # UI
    header('About')
    show_3d_map()
    

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
