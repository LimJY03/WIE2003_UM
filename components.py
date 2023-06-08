import streamlit as st
from PIL import Image
from model import predict

def header(s: str):

    st.title(s)
    st.markdown('---')

def emptylines(n: int) -> None:
    '''Create n empty lines'''

    for _ in range(n): 
        st.write('')

def get_state():
    '''Create state widget'''

    states_dict = {
        'Asheville':'NC',
        'Austin':'TX',
        'Boston':'MA',
        'Broward County':'FL',
        'Cambridge':'MA',
        'Chicago':'IL',
        'Clark County':'NV',
        'Columbus':'OH',
        'Denver':'CO',
        'Hawaii':'HI',
        'Jersey City':'NJ',    
        'Los Angeles':'SC',
        'Nashville':'TN',
        'New Orleans':'MS',
        'New York City':'NY',
        'Oakland':'CA',
        'Pacific Grove':'CA',
        'Portland':'OR',
        'Rhode Island':'RI',
        'Salem':'MA',
        'San Clara Country':'CA',
        'Santa Cruz County':'CA',
        'San Diego':'CA',
        'San Francisco':'CA',
        'San Mateo County':'CA',
        'Seattle':'WA',
        'Twin Cities MSA':'MN',
        'Washington D.C.':'DC',
    }

    city = st.selectbox('Select city:', ['Asheville', 'Austin', 'Boston', 'Broward County', 'Cambridge', 
                                         'Chicago', 'Clark County', 'Columbus', 'Denver', 'Hawaii', 'Jersey City',
                                         'Los Angeles', 'Nashville', 'New Orleans', 'New York City', 'Oakland',
                                         'Pacific Grove', 'Portland', 'Rhode Island', 'Salem', 'San Clara Country',
                                         'Santa Cruz County', 'San Diego', 'San Francisco', 'San Mateo County',
                                         'Seattle', 'Twin Cities MSA', 'Washington D.C.']
    return states_dict[city]


def searchbar() -> st.container():
    '''Create a search bar'''

    with st.container():

        col1, col2 = st.columns([6, 2])
        search_bar = col1.text_input('Search a keyword:', placeholder='Search')
        filter_by = col2.selectbox('Sort by:', ['Most Popular', 
                                                'Price (Descending)', 'Price (Ascending)', 
                                                'Nights (Descending)', 'Nights (Ascending)'])

        sort_by = {'by': ['price' if 'Price' in filter_by else \
                          'minimum_nights' if 'Nights' in filter_by else 'number_of_reviews'], 
                   'ascending': 'Ascending' in filter_by}

    with st.container():

        col1, col2 - st.columns{2}
        
        with col1: city = get_state()

    return search_bar, sort_by

def display_result(query_result, initial=0, max_per_page=10):
    '''Display query result in formatted layout'''

    upper_bound = min(initial + max_per_page, len(query_result))

    st.write(f'Search result (Showing {initial + 1} - {upper_bound}) of {len(query_result)}')

    for i in range(initial, min(initial + max_per_page, len(query_result))):

        row = query_result.iloc[i]

        with st.container():
            
            col1, col2 = st.columns([1, 2])
            col1.image(Image.open('./assets/img_placeholder.jpg'))
            col2.markdown('### {}'.format(row['name_of_listing']))
            col2.markdown(f'''Price: ${row['price']}  
                          Minimum Nights Required: {row['minimum_nights']}  
                          Host ID: {row['host_id']}
                          ''')
            if col2.button('Book', key=f'book{i}'): print('book')
            else: st.empty()

def input_prediction():
    '''Get user input for prediction'''

    feature_col = ['predictions', 'number_of_reviews', 'CA', 'CO', 'DC', 'FL', 'HI', 'IL', 'MA', 'MN',
                   'MS', 'NC', 'NJ','NV', 'NY', 'OH', 'OR', 'RI', 'SC', 'TN', 'TX',
                   'Entire home/apt', 'Hotel room', 'Private room']

    user_input_arr = ['cozy'] + [0] * 23
    
    col1, col2, col3 = st.columns([1, 2, 2])

    user_input_arr[0] = st.text_input('Keyword in Airbnb:', placeholder='Enter a keyword')
    user_input_arr[1] = col1.number_input('Number of reviews', min_value=0, value=1)
    
    with col2: city = get_state()

    room = col3.selectbox('Select room type:', ['Shared room', 'Entire home/apt', 'Hotel room', 'Private room'])

    if city != 'WA': user_input_arr[feature_col.index(city)] = 1
    if room != 'Shared room': user_input_arr[feature_col.index(room)] = 1

    if st.button('Predict'): 
        result = predict(user_input_arr)
        emptylines(3)
        st.write(f'The airbnb price of the configuration above is about')
        st.title(f'${round(result, 2)}')
