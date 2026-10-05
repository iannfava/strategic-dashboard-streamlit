#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#necessary libraries 
import pandas as pd 
import streamlit as st
from PIL import Image
from datetime import datetime
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregadores', page_icon='🚚', layout='wide')

#---------------------------------
#FUNCTIONS
#---------------------------------


def top_delivers( df1, top_asc):           
    df2 =( df1.loc [:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby(['City', 'Delivery_person_ID'])
              .mean()
              .sort_values(['City', 'Time_taken(min)'], ascending = top_asc )
              .reset_index() )
    
    df_aux01 = df2.loc[df2['City'] == 'Metropolitana', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urbana', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semiurbana', :].head(10)
    
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    df3 = df3.round( 2 )
    df3.columns = ['Cidade', 'ID do entregador', 'Tempo médio (min)']
    
    return df3 

def clean_code( df1 ):
    """this function has the responsability to clean the dataframe
           type of cleaning:
           1. Removing the NaN data
           2. Changing the columns type
           3. Removing the text variables spaces
           4. Formating the column data
           5. Cleaning the time column ( removing the text from the numerical variable )

           Input: Dataframe
           Output: Dataframe
    """
           
    # 1.Converting the Age column from text to number 
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    
    
    # 2. Converting the Ratings column from text to decimal number (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float)
    
    # 3. Converting the order_date column from text to date
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # 4. Converting multiple_deliveries from text to integer (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    
    ##5 . Removing spaces inside strings/text/objects
    #df1 = df1.reset_index( drop=True )
    #for i in range ( len( df1 ) ):
    # df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
    
    # 6. Removing spaces inside strings/text/objects
    
    df1.loc[: , 'ID'] = df1.loc[: ,'ID'].str.strip()
    df1.loc[: , 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[: , 'Type_of_order'] =  df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[: , 'Type_of_vehicle'] = df1.loc[: , 'Type_of_vehicle'].str.strip()
    df1.loc[: , 'City'] = df1.loc[: , 'City'].str.strip()
    df1.loc[: , 'Festival'] = df1.loc[: , 'Festival'].str.strip()
    
    #cleaning up the time taken column
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1
    
#------------------------------------------------------------------------
#---------------------Code Logical Structure-----------------------------
#------------------------------------------------------------------------

#---------------------------------------
#import dataset
#---------------------------------------
df = pd.read_csv ('dataset/train.csv')

#---------------------------------------
#Cleaning Dataset
#---------------------------------------
df1 = clean_code( df )

#---------------------------------------
# Traduz para português os valores que aparecem na tela (cidades, trânsito e clima)
#---------------------------------------
df1['City'] = df1['City'].replace( {'Metropolitian': 'Metropolitana', 'Urban': 'Urbana', 'Semi-Urban': 'Semiurbana'} )
df1['Road_traffic_density'] = df1['Road_traffic_density'].replace( {'Low': 'Baixo', 'Medium': 'Médio', 'High': 'Alto', 'Jam': 'Congestionado'} )
df1['Weatherconditions'] = df1['Weatherconditions'].str.strip().replace( {
    'conditions Cloudy': 'Nublado',
    'conditions Fog': 'Neblina',
    'conditions Sandstorms': 'Tempestade de areia',
    'conditions Stormy': 'Tempestade',
    'conditions Sunny': 'Ensolarado',
    'conditions Windy': 'Ventania' } )


#=======================================
#SIDEBAR
#=======================================


st.header('Marketplace - Visão Entregadores')

image = Image.open('images/cury.png')
st.sidebar.image( image, width=120 )
    
st.sidebar.markdown('### Cury Company')
st.sidebar.markdown ('## A entrega mais rápida da cidade')
st.sidebar.markdown ("""---""")

st.sidebar.markdown('## Selecione uma data limite')   
    
date_slider = st.sidebar.slider(
    'Até qual data?',
    value=datetime(2022, 4, 13 ),
    min_value=datetime(2022, 2, 11 ),
    max_value=datetime(2022, 4, 2 ),
    format='DD-MM-YYYY' 
)        

st.sidebar.markdown ("""---""")

           
traffic_options = st.sidebar.multiselect(
    'Condições de trânsito',
    ['Baixo', 'Médio', 'Alto', 'Congestionado'],
    default=['Baixo', 'Médio', 'Alto', 'Congestionado'] )

st.sidebar.markdown ("""---""")
st.sidebar.markdown ( '### Desenvolvido com a Comunidade DS' )

#---------------------------------------
#Date filter
#---------------------------------------
rows_selected = df1['Order_Date'] < date_slider
df1 = df1.loc[rows_selected, :]

#---------------------------------------
# Traffic filter
#---------------------------------------
rows_selected = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[rows_selected, :]

#=======================================
#STREAMLIT LAYOUT
#=======================================
tab1 = st.tabs( ['Visão Gerencial'] )[0]

with tab1:
    with st.container():
        st.title( 'Métricas Gerais' )

        col1, col2, col3, col4 = st.columns ( 4, gap='large' )
        
        with col1:
            
            Older = df1.loc[: , 'Delivery_person_Age'].max()
            col1.metric( 'Entregador mais velho', f'{Older} anos' )

        with col2:
            
            Younger = df1.loc[: , 'Delivery_person_Age'].min()
            col2.metric( 'Entregador mais novo', f'{Younger} anos' )

        with col3:
            
            better_condition = df1.loc[: , 'Vehicle_condition'].max()
            col3.metric('Condição do veículo (máx.)', better_condition )

        with col4:
       
            worst_condition = df1.loc[: , 'Vehicle_condition'].min()
            col4.metric( 'Condição do veículo (mín.)', worst_condition )

            
    with st.container():
        st.markdown ( "---" ) 
        st.title( 'Avaliações' )

        col1, col2 = st.columns ( 2 )
        with col1:
            st.markdown ( '##### Avaliação média por entregador' )
            df_avg_ratings_per_deliver = (df1.loc[: , ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                            .groupby('Delivery_person_ID')
                                            .mean()
                                            .reset_index() )
            df_avg_ratings_per_deliver = df_avg_ratings_per_deliver.round( 2 )
            df_avg_ratings_per_deliver.columns = ['ID do entregador', 'Avaliação média']
            st.dataframe( df_avg_ratings_per_deliver ) 
            
        with col2:
            st.markdown( '##### Avaliação média por trânsito' )
            df_avg_std_rating_by_traffic = (df1.loc[: , ['Road_traffic_density', 'Delivery_person_Ratings']]
                                               .groupby('Road_traffic_density')
                                               .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            #mudança de nome das colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']

            #reset do index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.round( 2 )
            df_avg_std_rating_by_traffic.columns = ['Trânsito', 'Avaliação média', 'Desvio padrão']

            st.dataframe( df_avg_std_rating_by_traffic )
            
            st.markdown( '##### Avaliação média por clima' )
            df_avg_std_rating_by_Weatherconditions = (df1.loc[: , ['Weatherconditions', 'Delivery_person_Ratings']]
                                                         .groupby('Weatherconditions')
                                                         .agg({'Delivery_person_Ratings': ['mean', 'std']}))

            #mudança das colunas
            df_avg_std_rating_by_Weatherconditions.columns = ['delivery_mean', 'delivery_std']

            #reset do index
            df_avg_std_rating_by_Weatherconditions = df_avg_std_rating_by_Weatherconditions.reset_index()
            df_avg_std_rating_by_Weatherconditions = df_avg_std_rating_by_Weatherconditions.round( 2 )
            df_avg_std_rating_by_Weatherconditions.columns = ['Clima', 'Avaliação média', 'Desvio padrão']
            st.dataframe( df_avg_std_rating_by_Weatherconditions )

    with st.container():
        st.markdown("""---""")
        st.title( 'Velocidade de entrega' )

        col1, col2 = st.columns( 2 )

        with col1:
            st.markdown( '##### Entregadores mais rápidos (top 10 por cidade)' )
            df3 = top_delivers( df1, top_asc=True )
            st.dataframe( df3 )
            
        with col2:
            st.markdown( '##### Entregadores mais lentos (top 10 por cidade)' )
            df3 = top_delivers( df1, top_asc=False )
            st.dataframe( df3 )