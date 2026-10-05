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
from streamlit_folium import st_folium

st.set_page_config( page_title='Visão Empresa', page_icon='📈', layout='wide')

# Uma cor fixa para cada tipo de trânsito, usada em todos os gráficos
TRAFFIC_COLORS = {'Baixo': '#83c9ff', 'Médio': '#0068c9', 'Alto': '#ffabab', 'Congestionado': '#ff2b2b'}
TRAFFIC_ORDER = ['Baixo', 'Médio', 'Alto', 'Congestionado']

#FUNCTIONS
#---------------------------------

def country_maps( df1 ):
    df_aux =( df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                .groupby(['City', 'Road_traffic_density'])
                .median()
                .reset_index() )

    if df_aux.empty:
        st.info( 'Sem dados para os filtros selecionados.' )
        return

    center = [ df_aux['Delivery_location_latitude'].mean(), df_aux['Delivery_location_longitude'].mean() ]
    map = folium.Map( location=center, zoom_start=6 )

    for index, location_info in df_aux.iterrows():
        folium.CircleMarker( [location_info['Delivery_location_latitude'],
                              location_info['Delivery_location_longitude']],
                              radius=8, color='#1f77b4', fill=True, fill_opacity=0.8,
                              popup=f"{location_info['City']} - trânsito {location_info['Road_traffic_density']}" ).add_to( map )

    st_folium( map, width=1024, height=600, returned_objects=[] )

def order_share_by_week( df1 ):
    df_aux01 = df1.loc[: ,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 =( df1.loc[: ,['Delivery_person_ID', 'week_of_year']]
                 .groupby('week_of_year' )
                 .nunique()
                 .reset_index() )
    
    df_aux = pd.merge (df_aux01, df_aux02, how='inner' )
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    
    fig = px.line( df_aux, x='week_of_year', y='order_by_deliver',
                   labels={'week_of_year': 'Semana do ano', 'order_by_deliver': 'Pedidos por entregador'} )
    
    return fig

def order_by_week( df1 ):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
    df_aux = df1.loc[: ,['ID', 'week_of_year']].groupby('week_of_year' ).count().reset_index()
    fig = px.line( df_aux, x='week_of_year', y='ID',
                   labels={'week_of_year': 'Semana do ano', 'ID': 'Quantidade de pedidos'} )
   
    return fig

def traffic_order_city( df1 ):     
    df_aux = ( df1.loc[: , ['ID','City','Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .count()
                  .reset_index() )
                                 
    fig = px.bar( df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group',
                  text='ID', color_discrete_map=TRAFFIC_COLORS,
                  category_orders={'Road_traffic_density': TRAFFIC_ORDER},
                  labels={'City': 'Cidade', 'Road_traffic_density': 'Trânsito', 'ID': 'Pedidos'} )
    
    return fig

def traffic_order_share( df1 ):
    df_aux = ( df1.loc[:, ['ID', 'Road_traffic_density']]
                 .groupby( 'Road_traffic_density' )
                 .count() 
                 .reset_index() )
    
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :]
    df_aux['delivery_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    
    fig = px.pie(df_aux, values='delivery_perc', names='Road_traffic_density',
        color='Road_traffic_density', color_discrete_map=TRAFFIC_COLORS,
        category_orders={'Road_traffic_density': TRAFFIC_ORDER},
        labels={'Road_traffic_density': 'Trânsito', 'delivery_perc': 'Participação'} )
    
    return fig 

def order_metric ( df1 ):
    cols = ["ID", "Order_Date"]
    # rows selection
    df_aux = df1.loc[:, cols].groupby("Order_Date").count().reset_index()

    # drawn the bar chart
    fig = px.bar(df_aux, x="Order_Date", y="ID",
                 labels={'Order_Date': 'Data do pedido', 'ID': 'Quantidade de pedidos'} )
    fig.update_xaxes( tickformat='%d/%m' )

    return fig

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

#--------------------------------------
#import dataset
#-------------------------------------
df = pd.read_csv ('dataset/train.csv')

#-------------------------------------
#Cleanig data 
#-------------------------------------
df1 = clean_code( df )

#-------------------------------------
# Traduz para português os valores que aparecem na tela (cidades e trânsito)
#-------------------------------------
df1['City'] = df1['City'].replace( {'Metropolitian': 'Metropolitana', 'Urban': 'Urbana', 'Semi-Urban': 'Semiurbana'} )
df1['Road_traffic_density'] = df1['Road_traffic_density'].replace( {'Low': 'Baixo', 'Medium': 'Médio', 'High': 'Alto', 'Jam': 'Congestionado'} )
    

#=======================================
#SIDEBAR
#=======================================


st.header('Marketplace - Visão Empresa')

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

#Date filter
rows_selected = df1['Order_Date'] < date_slider
df1 = df1.loc[rows_selected, :]

# Traffic filter
rows_selected = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[rows_selected, :]
#st.dataframe( df1 )

#=======================================
#STREAMLIT LAYOUT
#=======================================

tab1, tab2, tab3 = st.tabs ( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    with st.container():
        #Order metric 
        fig = order_metric( df1 )    
        st.markdown( '# Pedidos por dia' ) 
        st.plotly_chart( fig, width='stretch' )  
                                                    
    with st.container():
        col1, col2 = st.columns ( 2 )
        
        with col1:
            fig = traffic_order_share( df1 ) 
            st.header( 'Participação dos pedidos por trânsito' )
            st.plotly_chart( fig, width='stretch' )
                
        with col2:
            st.header( 'Pedidos por cidade e trânsito' )
            fig = traffic_order_city( df1 )
            st.plotly_chart( fig, width='stretch' )
                       
with tab2:    
    with st.container():        
        st.markdown( "# Pedidos por semana" )
        fig = order_by_week( df1 )
        st.plotly_chart( fig, width='stretch' )
    
    with st.container():
        st.markdown( "# Pedidos por entregador por semana" )
        fig = order_share_by_week( df1 )
        st.plotly_chart( fig, width='stretch' )
         
with tab3:
    st.markdown( "# Mapa das entregas" )
    st.caption( 'Cada marcador é a localização mediana das entregas de um tipo de cidade com um tipo de trânsito.' )
    country_maps( df1 )