import streamlit as st
from PIL import Image

def header(s: str):

    st.title(s)
    st.markdown('---')

def emptylines(n: int) -> None:
    '''Create n empty lines'''

    for _ in range(n): 
        st.write('')

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
            col2.markdown('''Price: ${}  
                          Minimum Nights Required: {}  
                          Host ID: {}
                          '''.format(row['price'], row['minimum_nights'], row['host_id']))
            if col2.button('Book', key=f'book{i}'): print('book')
            else: st.empty()