import pandas as pd 
import streamlit as st
import plotly.express as px

path = 'Tabela4.csv'

tabela = pd.read_csv(path, sep=";", encoding='latin-1')

tabela_tratada = tabela.iloc[0:27, 0:].copy()
tabela_tratada.columns = tabela_tratada.iloc[0]
tabela_tratada1 = tabela_tratada.iloc[1:].reset_index(drop=True)
tabela_tratada1 = tabela_tratada1.iloc[[0,4,9,10,13], 0:].copy()


anos = [c for c in tabela_tratada1.columns if str(c).isdigit()]

idh_longo = tabela_tratada1.melt(
    id_vars=["Sigla", "Código", "Estado"],
    value_vars=anos,
    var_name="ano",
    value_name="idh"
)

idh_longo["ano"] = pd.to_numeric(idh_longo["ano"])

idh_longo["idh"] = (
    idh_longo["idh"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)


df_final = idh_longo.loc[(idh_longo['ano']  >= 2000)].copy()


st.set_page_config(page_title="IDH", page_icon="📊", layout="wide")
st.title("Análise de IDH para Estados📊")
st.sidebar.space("xxlarge")


st.sidebar.title(
    "FILTRO🔍"
)
add_selectbox = st.sidebar.selectbox(
    "Escolha uma opção de visualização📊",
    ["Tabela", "Gráfico"]
)
st.sidebar.caption(
    "Jorge, Pedro, Mateus, Nina, Maria Cecília"
)

if add_selectbox == 'Tabela':
    st.write(idh_longo)
else:
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line_polar( 
            df_final,
            r='idh',
            theta='Estado', 
            line_close=True, 
            markers=True, 
            range_r=[0, 1],

            title="Relação entre IDH por estado"
    ) 
    
        st.plotly_chart(fig1, use_container_width=True)

        st.caption('Minas Gerais é o Estado que demonstra ter mais desenvolvimento')

    with col2:
        fig = px.scatter(
        df_final, 
        x="ano", 
        y="idh", 
        color="Estado",
        size_max=12,
        
        title="Relação entre Ano e IDH por estado"
    )

        st.plotly_chart(fig, use_container_width=True)

        st.caption('Minas Gerais é o Estado que demonstra ter mais desenvolvimento ao longo de todos os anos. Já o Maranhão tem em média menos desenvolvimento')