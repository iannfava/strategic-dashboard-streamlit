import streamlit as st
from PIL import Image

image = Image.open('images/cury.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown('### Cury Company')
st.sidebar.markdown('## A entrega mais rápida da cidade')
st.sidebar.markdown("""---""")

st.write( "# Cury Company - Growth Dashboard" )

st.markdown(
    """
    Dashboard criado para acompanhar os principais indicadores de um marketplace de delivery, sob três visões: empresa, entregadores e restaurantes.

    ### Como usar este dashboard

    **Visão Empresa**
    - Gerencial: pedidos por dia, participação de cada tipo de trânsito e pedidos por cidade e trânsito.
    - Tática: pedidos por semana e média de pedidos por entregador por semana.
    - Geográfica: mapa das cidades por tipo de trânsito.

    **Visão Entregadores**
    - Idade dos entregadores e condição dos veículos.
    - Avaliações médias por entregador, por trânsito e por clima.
    - Entregadores mais rápidos e mais lentos por cidade.

    **Visão Restaurantes**
    - Entregadores únicos e distância média das entregas.
    - Tempo de entrega com e sem festival.
    - Tempo de entrega por cidade e trânsito, e distância média por cidade.

    ### Contato

    - **LinkedIn:** [linkedin.com/in/iannfava](https://linkedin.com/in/iannfava)
    - **GitHub:** [github.com/iannfava](https://github.com/iannfava)
    - **E-mail:** iannfava@gmail.com
    """ )