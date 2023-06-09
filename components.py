import math
import random
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
from PIL import Image
from model import predict

@st.cache_data
def get_data():
    '''Load data into dataframe'''

    dataframe = pd.read_csv('./data/airbnb_data_clean.csv').iloc[:, 1:]
    return dataframe


def get_states_dict() -> dict:
    '''Map each city to state'''

    return {
        'Asheville': 'NC',
        'Austin': 'TX',
        'Boston': 'MA',
        'Broward County': 'FL',
        'Cambridge': 'MA',
        'Chicago': 'IL',
        'Clark County': 'NV',
        'Columbus': 'OH',
        'Denver': 'CO',
        'Hawaii': 'HI',
        'Jersey City': 'NJ',
        'Los Angeles': 'SC',
        'Nashville': 'TN',
        'New Orleans': 'MS',
        'New York City': 'NY',
        'Oakland': 'CA',
        'Pacific Grove': 'CA',
        'Portland': 'OR',
        'Rhode Island': 'RI',
        'Salem': 'MA',
        'San Clara Country': 'CA',
        'Santa Cruz County': 'CA',
        'San Diego': 'CA',
        'San Francisco': 'CA',
        'San Mateo County': 'CA',
        'Seattle': 'WA',
        'Twin Cities MSA': 'MN',
        'Washington D.C.': 'DC',
    }


def get_lat_lon(city: str) -> tuple[float, float]:
    '''Generate coordinate for each city'''

    coordinate_dict = {
        'Asheville': (35.5951, -82.5515),
        'Austin': (30.2711, -97.7437),
        'Boston': (42.3601, -71.0589),
        'Broward County': (26.1901, -80.3659),
        'Cambridge': (42.3736, -71.1097),
        'Chicago': (41.8781, -87.6298),
        'Clark County': (36.214, -115.013),
        'Columbus': (39.9623, -83.0007),
        'Denver': (39.7392, -104.9903),
        'Hawaii': (20.7984, -156.3319),
        'Jersey City': (40.7282, -74.0776),
        'Los Angeles': (34.0522, -118.2437),
        'Nashville': (36.1627, -86.7816),
        'New Orleans': (29.9511, -90.0715),
        'New York City': (40.7128, -74.006),
        'Oakland': (37.8044, -122.2711),
        'Pacific Grove': (36.6177, -121.9166),
        'Portland': (45.5202, -122.6742),
        'Rhode Island': (41.5801, -71.4774),
        'Salem': (42.5195, -70.8967),
        'San Clara Country': (37.3541, -121.9552),
        'Santa Cruz County': (37.0454, -121.957),
        'San Diego': (32.7157, -117.1611),
        'San Francisco': (37.7749, -122.4194),
        'San Mateo County': (37.4969, -122.3331),
        'Seattle': (47.6062, -122.3321),
        'Twin Cities MSA': (44.9778, -93.265),
        'Washington D.C.': (38.9072, -77.0379)
    }
    return coordinate_dict[city]


def header(heading: str):
    '''Format page header'''

    st.title(heading)
    st.markdown('---')


def h3(heading: str):
    '''Heading 3 format'''

    st.markdown(f'### {heading}')


def emptylines(num_of_lines: int) -> None:
    '''Create n empty lines'''

    for _ in range(num_of_lines):
        st.write('')


def show_3d_map() -> None:
    '''Display 3D Map'''

    col1, col2 = st.columns([1, 4])

    with col1:

        with st.form('airbnb_dist'):

            city = st.selectbox('Select a city', get_states_dict().keys())
            room = []
            
            if st.checkbox('Shared Room', value=True): room.append('Shared room')
            if st.checkbox('Entire Home/Apt', value=True): room.append('Entire home/apt')
            if st.checkbox('Hotel Room', value=True): room.append('Hotel room')
            if st.checkbox('Private Room', value=True): room.append('Private room')
            
            st.form_submit_button('Display', use_container_width=True)

    map_data = get_data()
    coords = map_data[(map_data['city'] == get_states_dict()[city]) & 
                      (map_data['room_type'].isin(room))][['latitude', 'longitude']]

    latitude, longitude = get_lat_lon(city)

    with col2:

        st.info('Height of bar represents the number of airbnb in that area')

        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=coords,
                    get_position='[longitude, latitude]',
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=coords,
                    get_position='[longitude, latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))


def get_state() -> str:
    '''Create state widget'''

    states_dict = get_states_dict()

    city = st.selectbox('Select city:', list(states_dict.keys()))
    return states_dict[city]


def get_roomtype() -> str:
    '''Create room selection widget'''

    room = st.selectbox('Select room type:', [
                        'Shared room', 'Entire home/apt', 'Hotel room', 'Private room'])
    return room


def recommendation_form():
    '''Create a form to recommend airbnb'''

    states_dict = get_states_dict()

    with st.form(key='recommendation_box'):

        city = st.selectbox('Select a city', states_dict.keys())
        budget = st.number_input('Enter your budget', min_value=1.0, value=80.1, step=1.0)
        submit = st.form_submit_button('Show Recommendation', use_container_width=True)

    if submit:

        data = get_data()
        data = data[data['city'] == states_dict[city]]
        values = data['price'].tolist() + [budget]
        
        width = math.ceil((max(values) - min(values)) / 50)

        col1, col2 = st.columns([1, 2])
        
        with col1:
            
            fig, ax = plt.subplots()
            _, _, patches = ax.hist(values, bins=50)

            patches[int((budget - min(values) - (1 if budget != min(values) else 0)) // width)].set_fc('r')

            st.write(f'Your budget in {city}\'s airbnb price range')
            st.pyplot(fig)

        with col2:

            choice = data[data['price'] <= budget].index

            st.write('Recommended Airbnbs')

            if len(choice) > 0:

                selected = random.sample(range(len(choice)), min(len(choice), 10))

                for i in selected:

                    print(i)
                    row = data.loc[choice[i]]

                    with st.container():

                        col1, col2 = st.columns([1, 2])
                        col1.image(Image.open('./assets/img_placeholder.jpg'))
                        col2.markdown(f'''### {row['name_of_listing']}''')
                        col2.markdown(f'''Price: ${row['price']}  
                                    Minimum Nights Required: {row['minimum_nights']}  
                                    Host ID: {row['host_id']}
                                    ''')
                        col2.button('Book', key=i)

            else:

                h3('No result')


def searchbooking() -> None:
    '''Create a search bar'''

    with st.form('booking'):

        col1, col2, col3, col4 = st.columns([6, 2, 2, 2])
        search_bar = col1.text_input('Search a keyword:', placeholder='Search')
        filter_by = col2.selectbox('Sort by:', ['Most Popular',
                                                'Price (Descending)', 'Price (Ascending)',
                                                'Nights (Descending)', 'Nights (Ascending)'])

        sort_by = {'by': ['price' if 'Price' in filter_by else
                          'minimum_nights' if 'Nights' in filter_by else 'number_of_reviews'],
                   'ascending': 'Ascending' in filter_by}

        with col3:
            city = get_state()
        with col4:
            room = get_roomtype()

        search = st.form_submit_button('Search')

    if search:

        display_result(search_bar, sort_by, city, room)


def display_result(search, sort_by, city, room):
    '''Display query result in formatted layout'''

    data = get_data()
    max_per_page = 10

    query_result = data[
        data.apply(lambda row: search in row['name_of_listing'], axis=1)
    ].sort_values(**sort_by)

    query_result = query_result[
        (query_result['city'] == city) & (query_result['room_type'] == room)
    ]

    no_result = len(query_result) == 0

    upper_bound = min(max_per_page, len(query_result))

    emptylines(3)
    st.write(f'Search result (Showing {0 if no_result else 1} - {upper_bound}) of {len(query_result)}')

    if no_result:
        h3('No result')
    else:
        for i in range(min(max_per_page, len(query_result))):

            row = query_result.iloc[i]

            with st.form(f'airbnb{i}'):

                col1, col2 = st.columns([1, 5])
                col1.image(Image.open('./assets/img_placeholder.jpg'))
                col2.markdown(f'''### {row['name_of_listing']}''')
                col2.markdown(f'''**Price:** ${row['price']}  
                            **Minimum Nights Required:** {row['minimum_nights']}  
                            **Host ID:** {row['host_id']}
                            ''')
                col2.form_submit_button('Book')


def input_prediction():
    '''Get user input for prediction'''

    feature_col = ['predictions', 'number_of_reviews', 'CA', 'CO', 'DC', 'FL', 'HI', 'IL', 'MA',
                   'MN', 'MS', 'NC', 'NJ', 'NV', 'NY', 'OH', 'OR', 'RI', 'SC', 'TN', 'TX',
                   'Entire home/apt', 'Hotel room', 'Private room']

    user_input_arr = ['cozy'] + [0] * 23

    with st.form(key='prediction'):

        col1, col2, col3 = st.columns([1, 2, 2])

        user_input_arr[0] = st.text_input('Keyword in Airbnb:', placeholder='Enter a keyword')
        user_input_arr[1] = col1.number_input('Number of reviews', min_value=0, value=1)

        with col2:
            city = get_state()
        with col3:
            room = get_roomtype()

        make_prediction = st.form_submit_button('Predict', use_container_width=True)

    if city != 'WA':
        user_input_arr[feature_col.index(city)] = 1
    if room != 'Shared room':
        user_input_arr[feature_col.index(room)] = 1

    if make_prediction:
        result = predict(user_input_arr)
        emptylines(3)
        st.write('The airbnb price of the configuration above is about')
        st.title(f'${round(result, 2)}')


def homepage_content() -> None:
    '''Show content on Home Page'''

    h3('Project Background')
    st.markdown('Since its founding in 2008, Airbnb has grown rapidly through its value creation using the sharing economy business model. Citizens from **over 220 nations** use it and there are 4 million hosts worldwide. According to [Airbnb Statistics [2023]: User & Market Growth Data (2022, August 3)](https://ipropertymanagement.com/research/airbnb-statistics), over 1 billion stays have been booked by more than 150 million users worldwide.There are **21 nights reserved** for the typical Airbnb property in the U.S. each month. In 2021, the average Airbnb occupancy rate in the U.S. was **48%**.')
    st.markdown('Based on [Hati, S. R. H., Balqiah, T. E., Hananto, A., & Yuliati, E. (2021)](https://doi.org/10.1016/j.heliyon.2021.e08222), accommodations on Airbnb are **frequently less expensive than conventional accommodations** like a hotel. Additionally, Airbnb provides customers with the chance to **experience local authenticity** by letting them stay in a listed flat or private room and live like a local. With Airbnb, property owners can get the most out of their underutilised properties and increase their revenue.')
    st.markdown('As we know, the sharing economy business model has a **significant impact** on the travel industry. This dynamic creates a workable substitute for conventional services, enabling travellers to **personalise their journeys** and **enrich their experiences**. ')
    st.markdown('Hence, our team has come up with a project that **aids in Airbnb pricing prediction** and **suggests** the most affordable accommodations for consumers. The analysis findings may be used by Airbnb hosts to **refine their listings** and **increase their revenue**. Additionally, this may be advantageous to tourists looking for **high-calibre**, **reasonably-priced** Airbnb listings.')
    emptylines(3)
    h3('Project Objectives')
    st.markdown('''
    1. To **identify opportunities** for hosts based on the insights  
    2. To **analyse and predict** Airbnb prices to understand its market  
    3. To **recommend** the most suitable Airbnb accommodation at the optimum price''')


def aboutpage_content() -> None:
    '''Shows content on About Page'''

    col1, _, col2 = st.columns([6, 1, 2])

    with col1:

        h3('About Our Team')
        st.markdown('We are a group of undergraduate students taking the WIE2003 **Introduction to Data Science** course in the Faculty of Computer Science and Information Technology, Universiti Malaya.')
        st.markdown('**Low Hui Yi** is our team leader as well as the project manager. She checks and ensures that all progresses are following the planned timeline.')
        st.markdown('**Lim Jun Yi** is the main developer for the Machine Learning Models and this Streamlit App.')
        st.markdown('**Oon Yee Sem, Tessa and Wong Yi Fei** are the main data scientist in cleaning, processing and analyzing the data to discover insights and prepare the data for Model Training.')
        emptylines(3)
        h3('About This Product')

    with col2:

        h3('Contributors')
        st.markdown('''
        * Lim Jun Yi ([linktree](https://linktr.ee/limjy03))  
        * Tessa Shalini Pradeep ()  
        * Low Hui Yi ()  
        * Wong Yi Fei ()  
        * Oon Yee Sem ()''')
