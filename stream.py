import pandas as pd
import streamlit as st
import plotly.express as px

path = 'Tabela4.csv'

tabela = pd.read_csv(path, sep=";", encoding='latin-1')

tabela_tratada = tabela.iloc[0:27, :].copy()
tabela_tratada.columns = tabela_tratada.iloc[0]

tabela_tratada1 = tabela_tratada.iloc[1:].reset_index(drop=True)
tabela_tratada1 = tabela_tratada1.iloc[[0, 4, 9, 10, 13], :].copy()

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
)

idh_longo["idh"] = pd.to_numeric(
    idh_longo["idh"],
    errors="coerce"
)

df_final = idh_longo.loc[
    idh_longo["ano"] >= 2000
].copy()

st.set_page_config(
    page_title="IDH",
    page_icon="📊",
    layout="wide"
)

st.title("Análise de IDH para Estados 📊")

st.sidebar.title("FILTRO 🔍")

visualizacao = st.sidebar.selectbox(
    "Escolha uma opção de visualização 📊",
    ["Tabela", "Gráfico"]
)

st.sidebar.divider()

noticias_estados = st.sidebar.radio(
    "Selecione o Estado",
    [
        "Acre",
        "Bahia",
        "Maranhão",
        "Minas Gerais",
        "Pará",
        "Nenhum"
    ]
)

st.sidebar.divider()

dados_estados = st.sidebar.multiselect(
    "Selecione os Estados para análise",
    [
        "Acre",
        "Bahia",
        "Maranhão",
        "Minas Gerais",
        "Pará"
    ]
)

st.sidebar.caption(
    "Jorge, Pedro, Mateus, Nina, Maria Cecília"
)


def grafico(dados):

    if dados.empty:
        st.warning("Não existem dados para apresentar.")
        return

    col1, col2 = st.columns(2)

    with col1:

        ultimo_ano = dados["ano"].max()

        dados_ano = dados.loc[
            dados["ano"] == ultimo_ano
        ]

        fig1 = px.line_polar(
            dados_ano,
            r="idh",
            theta="Estado",
            line_close=False,
            markers=True,
            range_r=[0, 1],
            title=f"Comparação do IDH entre os estados ({ultimo_ano})"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        st.caption(
            "Comparação dos índices de desenvolvimento humano "
            "dos estados no último ano disponível."
        )

    with col2:

        fig = px.scatter(
            dados,
            x="ano",
            y="idh",
            color="Estado",
            title="Relação entre Ano e IDH por estado",
            labels={
                "ano": "Ano",
                "idh": "IDH",
                "Estado": "Estado"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption(
            "Evolução do IDH dos estados ao longo dos anos."
        )


if dados_estados:

    dados_filtrados = df_final.loc[
        df_final["Estado"].isin(dados_estados)
    ].copy()

else:

    dados_filtrados = df_final.copy()


if visualizacao == "Tabela":

    st.subheader("Tabela de dados do IDH")

    st.dataframe(
        dados_filtrados,
        use_container_width=True
    )

elif visualizacao == "Gráfico":

    st.subheader("Gráficos de análise do IDH")

    grafico(dados_filtrados)


st.divider()

st.title("Média do IDH por Estado 📊")

estado_media = st.radio(
    "Selecione um estado para visualizar a média do IDH:",
    ["Acre", "Bahia", "Maranhão", "Minas Gerais", "Pará"],
    horizontal=True
)

dados_media = df_final.loc[
    df_final["Estado"] == estado_media
]

media_idh = dados_media["idh"].mean()

st.metric(
    label=f"Média do IDH - {estado_media}",
    value=f"{media_idh:.3f}"
)


imagens_estados = {
    "Acre": "idhAcre.png",
    "Bahia": "idhBahia.png",
    "Maranhão": "idhMaranhao.png",
    "Minas Gerais": "idhMinas.png",
    "Pará": "idhpara.png"
}

if noticias_estados != "Nenhum":

    st.divider()

    st.title(noticias_estados)

    st.image(
        imagens_estados[noticias_estados],
        use_container_width=True
    )
