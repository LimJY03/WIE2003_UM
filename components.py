import pandas as pd
import streamlit as st
import pydeck as pdk
from PIL import Image
from model import predict

@st.cache_data
def get_data():
    '''Load data into dataframe'''

    dataframe = pd.read_csv('./data/airbnb_data_clean.csv').iloc[:, 1:]
    return dataframe

def header(heading: str):
    '''Format page header'''

    st.title(heading)
    st.markdown('---')

def emptylines(num_of_lines: int) -> None:
    '''Create n empty lines'''

    for _ in range(num_of_lines):
        st.write('')

def show_3d_map():
    '''Display 3D Map'''

    map_data = pd.DataFrame()
    map_data[['lat', 'lon']] = get_data()[['latitude', 'longitude']]

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.0902,
            longitude=95.7129,
            zoom=3,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=map_data,
                get_position='[lon, lat]',
                radius=2000,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=2000,
            ),
        ],
    ))

def get_state() -> str:
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
                                         'Seattle', 'Twin Cities MSA', 'Washington D.C.'])
    return states_dict[city]

def get_roomtype() -> str:
    '''Create room selection widget'''

    room = st.selectbox('Select room type:', ['Shared room', 'Entire home/apt', 'Hotel room', 'Private room'])
    return room

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

        col1, col2 = st.columns(2)
        
        with col1: city = get_state()
        with col2: room = get_roomtype()

    return search_bar, sort_by, city, room

def display_result():
    '''Display query result in formatted layout'''
    
    df = get_data()
    max_per_page=10

    search, sort_by, city, room = searchbar()

    query_result = df[df.apply(lambda row: search in row['name_of_listing'], axis=1)].sort_values(**sort_by)
    query_result = query_result[(query_result['city'] == city) & (query_result['room_type'] == room)]

    no_result = len(query_result) == 0

    upper_bound = min(max_per_page, len(query_result))

    emptylines(3)
    st.write(f'Search result (Showing {0 if no_result else 1} - {upper_bound}) of {len(query_result)}')

    if no_result: st.markdown('### No result')
    else: 
        for i in range(min(max_per_page, len(query_result))):

            row = query_result.iloc[i]

            with st.container():
                
                col1, col2 = st.columns([1, 2])
                col1.image(Image.open('./assets/img_placeholder.jpg'))
                col2.markdown(f'''### {row['name_of_listing']}''')
                col2.markdown(f'''Price: ${row['price']}  
                            Minimum Nights Required: {row['minimum_nights']}  
                            Host ID: {row['host_id']}
                            ''')
                col2.button('Book', key=f'book{i}')

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
    with col3: room = get_roomtype()

    if city != 'WA': user_input_arr[feature_col.index(city)] = 1
    if room != 'Shared room': user_input_arr[feature_col.index(room)] = 1

    if st.button('Predict'): 
        result = predict(user_input_arr)
        emptylines(3)
        st.write('The airbnb price of the configuration above is about')
        st.title(f'${round(result, 2)}')
