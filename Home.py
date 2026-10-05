import streamlit as st

st.set_page_config( page_title='Cury Company', layout='wide' )

pg = st.navigation( [
    st.Page( 'views/inicio.py', title='Início', icon='🎯', default=True ),
    st.Page( 'views/1_company_view.py', title='Visão Empresa', icon='📈', url_path='visao-empresa' ),
    st.Page( 'views/2_delivers_view.py', title='Visão Entregadores', icon='🚚', url_path='visao-entregadores' ),
    st.Page( 'views/3_restaurants_view.py', title='Visão Restaurantes', icon='🍽️', url_path='visao-restaurantes' ),
] )

pg.run()