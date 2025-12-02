
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestão de Manutenção do Condomínio", layout="wide")

# ----------------------------
# Upload da Planilha
# ----------------------------
st.sidebar.header("📁 Carregar Dados")
arquivo = st.sidebar.file_uploader("Envie a planilha de equipamentos (.xlsx)", type=["xlsx"])

# ----------------------------
# Função para carregar os dados
# ----------------------------
@st.cache_data
def carregar_dados(file):
    return pd.read_excel(file)

# ----------------------------
# Layout com Abas
# ----------------------------
aba1, aba2 = st.tabs(["📋 Lista de Equipamentos", "📊 Dashboard"])

# ----------------------------
# ABA 1 — LISTA DE EQUIPAMENTOS
# ----------------------------
with aba1:

    st.title("📋 Lista de Equipamentos do Condomínio")

    if not arquivo:
        st.warning("Envie a planilha à esquerda para visualizar os equipamentos.")
    else:
        df = carregar_dados(arquivo)
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            local = st.selectbox("Filtrar por Local", ["Todos"] + sorted(df["Local"].unique()))
        with col2:
            categoria = st.selectbox("Filtrar por Categoria", ["Todos"] + sorted(df["Categoria"].unique()))

        df_filt = df.copy()
        if local != "Todos":
            df_filt = df_filt[df_filt["Local"] == local]
        if categoria != "Todos":
            df_filt = df_filt[df_filt["Categoria"] == categoria]

        st.subheader("📌 Equipamentos Filtrados")
        st.dataframe(df_filt, use_container_width=True)

# ----------------------------
# ABA 2 — DASHBOARD
# ----------------------------
with aba2:

    st.title("📊 Dashboard de Manutenção Preventiva")

    if not arquivo:
        st.warning("Envie a planilha à esquerda para gerar o dashboard.")
    else:
        df = carregar_dados(arquivo)

        df["Última Troca"] = pd.to_datetime(df["Última Troca"])
        df["Próxima Troca"] = pd.to_datetime(df["Próxima Troca"])

        st.subheader("⏱️ Próximas Trocas por Equipamento")

        fig = px.bar(
            df,
            x="Equipamento",
            y="Dias para Próxima Troca",
            color="Categoria",
            title="Dias Restantes para a Próxima Manutenção",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📦 Quantidade de Equipamentos por Categoria")

        fig2 = px.pie(
            df,
            names="Categoria",
            title="Distribuição por Categoria",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("🚨 Equipamentos com manutenção urgente (≤ 15 dias)")
        critico = df[df["Dias para Próxima Troca"] <= 15]

        if critico.empty:
            st.success("Nenhum equipamento com manutenção urgente! 🎉")
        else:
            st.error("⚠️ Atenção! Equipamentos próximos do prazo.")
            st.dataframe(critico, use_container_width=True)
