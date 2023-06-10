from components import header, homepage_content, recommendation_form, show_3d_map, searchbooking, input_prediction, aboutpage_content

def home():
    '''Home Page'''

    # UI
    header('🏡 Home')
    homepage_content()


def dist():
    '''Show airbnb distribution by city'''
    
    # UI
    header('🌏 Airbnb Distribution')
    show_3d_map()

def booking_assistant():
    '''Recommendation Page'''

    # UI
    header('🤵🏻 Booking Assistant')
    recommendation_form()

def booking():
    '''Booking Page'''

    # UI
    header('📆 Booking')
    searchbooking()

def budgeting():
    '''Budgeting Page'''

    # UI
    header('💵 Budgeting')
    input_prediction()


def about():
    '''About Page'''

    # UI
    header('📋 About')
    aboutpage_content()
