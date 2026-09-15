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

#import dataset
df = pd.read_csv ('dataset/train.csv')

# 1.Convertendo a coluna Age de texto para numero
df1 = df.copy()
linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

linhas_selecionadas = (df1['City'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()

df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )


# 2. Convertendo a coluna Ratings de  texto para numero decimal ( float )
df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float)

# 3. Convertendo a coluna order_date de texto para data
df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

# 4. Convertendo multiple_deliveries de texto para numero inteiro ( int )
linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
df1 = df1.loc[linhas_selecionadas, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

##5 . Removendo espaços dentro de strings/texto/objeto
#df1 = df1.reset_index( drop=True )
#for i in range ( len( df1 ) ):
# df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

# 6. Removendo os espaços dentro de strings/texto/object

df1.loc[: , 'ID'] = df1.loc[: ,'ID'].str.strip()
df1.loc[: , 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
df1.loc[: , 'Type_of_order'] =  df1.loc[:, 'Type_of_order'].str.strip()
df1.loc[: , 'Type_of_vehicle'] = df1.loc[: , 'Type_of_vehicle'].str.strip()
df1.loc[: , 'City'] = df1.loc[: , 'City'].str.strip()
df1.loc[: , 'Festival'] = df1.loc[: , 'Festival'].str.strip()

#limpando a coluna de time taken

df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1] )
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)



#=======================================
#SIDEBAR
#=======================================


st.header('Marketplace - Client Vision')

image_path = 'images/cury.png'
image=Image.open( image_path )
st.sidebar.image( image, width=120 )
    
st.sidebar.markdown('### Cury company')
st.sidebar.markdown ('## Fastest Delivery in Town')
st.sidebar.markdown ("""---""")

st.sidebar.markdown('## Select a limit date')   
    
date_slider = st.sidebar.slider(
    'by what date?',
    value=datetime(2022, 4, 13 ),
    min_value=datetime(2022, 2, 11 ),
    max_value=datetime(2022, 4, 2 ),
    format='DD-MM-YYYY' 
)        

st.header( date_slider )
st.sidebar.markdown ("""---""")

           
traffic_options = st.sidebar.multiselect(
    'Whats the traffic like?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown ("""---""")
st.sidebar.markdown ( '### Powered by DS Community' )

#Date filter
rows_selected = df1['Order_Date'] < date_slider
df1 = df1.loc[rows_selected, :]

# Traffic filter
rows_selected = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[rows_selected, :]
st.dataframe( df1 )

#=======================================
#STREAMLIT LAYOUT
#=======================================

tab1, tab2, tab3 = st.tabs ( ['Managerial Vision', 'Tatical Vision', 'Geographical Vision'] )

with tab1:
    with st.container():
      st.markdown( '# Orders by Day' )
      column = ["ID", "Order_Date"]

# rows selection
      df_aux = df1.loc[:, column].groupby("Order_Date").count().reset_index()

# drawn the line chart 
      fig = px.bar(df_aux, x="Order_Date", y="ID")
      st.plotly_chart( fig, use_container_width=True )

    with st.container():
      col1, col2 = st.columns ( 2 )
        
      with col1:
          st.header('Traffic Order Share')
          df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index())
          df_aux = df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :]
          df_aux['delivery_perc'] = df_aux['ID'] / df_aux['ID'].sum()

          fig = px.pie(df_aux, values='delivery_perc', names= 'Road_traffic_density')
          st.plotly_chart( fig, use_container_width=True )
          
      with col2:
          st.header('Traffic Order City')
          df_aux = df1.loc[: , ['ID','City','Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
          df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
          df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

          fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color= 'City')
          st.plotly_chart( fig, use_container_width=True )
          
with tab2:    
      with st.container():
        
           st.markdown( "# Order by Week" )
    
           df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U' )
           df_aux = df1.loc[: ,['ID', 'week_of_year']].groupby('week_of_year' ).count().reset_index()
           fig = px.line( df_aux, x='week_of_year', y='ID')
           st.plotly_chart (fig, use_container_width=True)

      with st.container():

           st.markdown( "# Order Share by Week" )
    
           df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')

           df_aux01 = df1.loc[: ,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
           df_aux02 = df1.loc[: ,['Delivery_person_ID', 'week_of_year']].groupby('week_of_year' ).nunique().reset_index()

           df_aux = pd.merge (df_aux01, df_aux02, how='inner' )

           df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

           fig = px.line( df_aux, x='week_of_year', y='order_by_deliver' )
           st.plotly_chart (fig, use_container_width=True)
           
with tab3:
    st.markdown( "# Country Maps" )
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                   location_info['Delivery_location_longitude']],
                   popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
folium_static( map, width=1024 , height=600 )




























