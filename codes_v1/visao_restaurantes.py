#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

#necessary libraries 
import pandas as pd 
import numpy as np
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


st.header('Marketplace - Restaurants View')

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
#st.dataframe( df1 )


#=======================================
#STREAMLIT LAYOUT
#=======================================
tab1, tab2, tab3 = st.tabs( ['Managerial Vision', '_', '_'] )

with tab1:
    with st.container():
        st.title( 'Overall Metrics' )

        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = df['Delivery_person_ID'].nunique()
            col1.metric ('unique delivery person', delivery_unique )
            
        with col2:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude','Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x:
                               haversine(
                                     (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                     (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )
            avg_distance = np.round (df1['distance'].mean(), 2 )
            col2.metric('Average delivery distance', avg_distance )

                 
        with col3:
           cols = ['Time_taken(min)', 'Festival']
           df_aux = ( df1.loc[:, cols].groupby( ['Festival'] ).agg( {'Time_taken(min)': ['mean', 'std']} ) )

           df_aux.columns = ['avg_time', 'std_time']
           df_aux = df_aux.reset_index()
           df_aux = np.round (df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'], 2 )
           
           col3.metric( 'Avg. delivery time', df_aux )


        with col4:
           cols = ['Time_taken(min)', 'Festival']
           df_aux = ( df1.loc[:, cols].groupby( ['Festival'] ).agg( {'Time_taken(min)': ['mean', 'std']} ) )

           df_aux.columns = ['avg_time', 'std_time']
           df_aux = df_aux.reset_index()
           df_aux = np.round (df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'], 2 )
           
           col4.metric( 'STD delivery', df_aux )
            
        with col5:
           cols = ['Time_taken(min)', 'Festival']
           df_aux = ( df1.loc[:, cols].groupby( ['Festival'] ).agg( {'Time_taken(min)': ['mean', 'std']} ) )

           df_aux.columns = ['avg_time', 'std_time']
           df_aux = df_aux.reset_index()
           df_aux = np.round (df_aux.loc[df_aux['Festival'] == 'No', 'std_time'], 2 )
           
           col5.metric( 'STD delivery NO festival', df_aux )
            
        with col6:
           cols = ['Time_taken(min)', 'Festival']
           df_aux = ( df1.loc[:, cols].groupby( ['Festival'] ).agg( {'Time_taken(min)': ['mean', 'std']} ) )

           df_aux.columns = ['avg_time', 'std_time']
           df_aux = df_aux.reset_index()
           df_aux = np.round (df_aux.loc[df_aux['Festival'] == 'No', 'std_time'], 2 )
           
           col6.metric( 'STD delivery on festival', df_aux )

    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns ( 2 )
        
        with col1:  
           st.title( 'Average time delivery by city' )
           cols = ['City', 'Time_taken(min)']
           df_aux = df1.loc[:, cols].groupby('City').agg( {'Time_taken(min)': ['mean', 'std']} )
           df_aux.columns = ['avg_time', 'std_time']
           df_aux = df_aux.reset_index()

           fig = go.Figure()
           fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'],
                      error_y=dict( type='data', array=df_aux['std_time'])))
           fig.update_layout(barmode='group')
           st.plotly_chart ( fig )

        with col2:
            st.title( 'Distance Distribuition' )
            
            cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
            df_aux =( df1.loc[:, cols]
                         .groupby( ['City','Road_traffic_density'] )
                         .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']

            df_aux = df_aux.reset_index() 

            st.dataframe ( df_aux )
  
        
    with st.container():
         st.markdown("""---""")
         st.title( 'Time Distribuition' )

         col1, col2 = st.columns( 2 )
         with col1:
           cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
           df1['Distance'] = df1.loc[:, cols].apply( lambda x:
                                        haversine(  (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ),axis=1 )

           avg_distance = df1.loc[:, ['City', 'distance']].groupby( 'City' ).mean().reset_index()
           fig = go.Figure( data=[ go.Pie(  labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
           st.plotly_chart( fig )
        
            
         with col2:
            cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
            df_aux =( df1.loc[:, cols]
                         .groupby( ['City','Road_traffic_density'] )
                         .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']

            df_aux = df_aux.reset_index()   

            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                              color='std_time', color_continuous_scale='RdBu',
                              color_continuous_midpoint=np.average(df_aux['std_time']))
            st.plotly_chart( fig )
       

      






