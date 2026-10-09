# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 23:39:36 2026

@author: Cauan
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Termômetro de Desemprego Real | Brasil",
    page_icon="📈",
    layout="wide"
)

# Estilização CSS personalizada para dar um ar moderno (Executive Dashboard)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Título e Descrição
st.title("📉 Termômetro do Desemprego Real e Subutilização no Brasil")
st.markdown("Uma análise avançada indo **além da taxa oficial de desocupação**, mapeando desalentados e ociosidade oculta por Estado.")
st.markdown("---")

@st.cache_data
def carregar_dados():
    try:
        return pd.read_csv("data/processed/subutilizacao_uf.csv")
    except FileNotFoundError:
        return None

df = carregar_dados()

if df is None:
    st.error("⚠️ Base de dados não encontrada. Execute `python src/extract.py` primeiro.")
else:
    # --- BARRA LATERAL ---
    st.sidebar.header("🗺️ Controles de Filtro")
    estados_disponiveis = sorted(df['uf'].unique())
    
    estado_selecionado = st.sidebar.selectbox(
        "Selecione o Estado:",
        options=estados_disponiveis,
        index=estados_disponiveis.index("São Paulo") if "São Paulo" in estados_disponiveis else 0
    )

    df_filtrado = df[df['uf'] == estado_selecionado].sort_values('trimestre')

    # --- KPIs SUPERIORES ---
    st.subheader(f"Indicadores Principais: {estado_selecionado}")
    
    if not df_filtrado.empty:
        ultima_taxa = df_filtrado.iloc[-1]['taxa_subutilizacao']
        ultimo_trimestre = df_filtrado.iloc[-1]['trimestre']
        media_periodo = df_filtrado['taxa_subutilizacao'].mean()
        primeira_taxa = df_filtrado.iloc[0]['taxa_subutilizacao']
        variacao = ultima_taxa - primeira_taxa

        kpi1, kpi2, kpi3 = st.columns(3)
        
        with kpi1:
            st.metric(label=f"Taxa Recente ({ultimo_trimestre})", value=f"{ultima_taxa:.1f}%")
        with kpi2:
            st.metric(label="Média da Série Histórica", value=f"{media_periodo:.1f}%")
        with kpi3:
            st.metric(label="Variação no Período", value=f"{variacao:+.1f} p.p.")

    st.markdown("---")

    # --- GRÁFICOS ---
    col_g1, col_g2 = st.columns([1.6, 1])
    
    with col_g1:
        st.subheader(f"Evolução Temporal — {estado_selecionado}")
        fig_linha = px.line(
            df_filtrado, 
            x='trimestre', 
            y='taxa_subutilizacao', 
            markers=True,
            labels={'trimestre': 'Trimestre', 'taxa_subutilizacao': 'Subutilização (%)'},
            template='plotly_dark'
        )
        fig_linha.update_traces(line_color='#00d2ff', line_width=3, marker_size=8)
        fig_linha.update_layout(xaxis_type='category', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_linha, width='stretch')

    with col_g2:
        st.subheader("Ranking Atual (Top 10 UFs)")
        ultimo_trimestre_geral = df['trimestre'].max()
        df_recente = df[df['trimestre'] == ultimo_trimestre_geral].sort_values(by='taxa_subutilizacao', ascending=False).head(10)
        
        fig_bar = px.bar(
            df_recente,
            x='taxa_subutilizacao',
            y='uf',
            orientation='h',
            text='taxa_subutilizacao',
            labels={'taxa_subutilizacao': 'Taxa (%)', 'uf': 'Estado'},
            template='plotly_dark'
        )
        fig_bar.update_traces(marker_color='#ff4b4b', texttemplate='%{text:.1f}%', textposition='outside')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=420)
        st.plotly_chart(fig_bar, width='stretch')

    # --- TABELA EXPANSÍVEL ---
    with st.expander("📋 Visualizar base de dados completa filtrada"):
        st.dataframe(df_filtrado, width='stretch')