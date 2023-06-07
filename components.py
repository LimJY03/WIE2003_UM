import streamlit as st
from PIL import Image

def header(s: str):

    st.title(s)
    st.markdown('---')

def emptylines(n: int) -> None:

    for _ in range(n): st.write('')

def searchbar():

    with st.container():
        
        col1, col2 = st.columns([6, 2])
        search_bar = col1.text_input('Search a keyword:', placeholder='Search')
        filter_by = col2.selectbox('Sort by:', ['Most Popular', 'Price (Descending)', 'Price (Ascending)', 
                                                'Nights (Descending)', 'Nights (Ascending)'])

        sort_by = {'by': ['number_of_reviews'], 'ascending': False} if filter_by == 'Most Popular' else \
                  {'by': ['price'], 'ascending': False} if filter_by == 'Price (Descending)' else \
                  {'by': ['price']} if filter_by == 'Price (Ascending)' else \
                  {'by': ['minimum_nights'], 'ascending': False} if filter_by == 'Nights (Descending)' else \
                  {'by': ['minimum_nights']}

    return search_bar, sort_by

def display_result(query_result, initial=0, MAX_PER_PAGE=10):

    upper_bound = min(initial + MAX_PER_PAGE, len(query_result))

    st.write(f'Search result (Showing {initial + 1} - {upper_bound}) of {len(query_result)}')

    for i in range(initial, min(initial + MAX_PER_PAGE, len(query_result))):

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