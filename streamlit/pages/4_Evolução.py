# -*- coding: utf-8 -*-
"""Página Evolução."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Evolução", page_icon="📈", layout="wide")

from common import dados_filtrados_op, preparar_dados
from metrics import evolucao, serie_evolucao
from theme import PRETO, TEXTO_MUTE, VERDE
from ui import (
    aplicar_css,
    chip_evolucao,
    chip_faixa,
    empty_state,
    navegacao,
    secao,
    tabela_html,
    titulo_pagina,
)

aplicar_css()
navegacao("pages/4_Evolução.py")

preparar_dados()
doc, ind, tre, qua = dados_filtrados_op()

titulo_pagina(
    "Evolução",
    "Score final ao longo dos ciclos de avaliação (ignora o filtro de período).",
)

if doc.empty and ind.empty and tre.empty and qua.empty:
    empty_state()
    st.stop()

secao("Score Final por Ciclo de Avaliação")
serie = serie_evolucao(doc, ind, tre, qua)
if not serie.empty:
    fig = go.Figure()
    for op, g in serie.groupby("Operação"):
        fig.add_trace(
            go.Scatter(
                name=op,
                x=g["Data"],
                y=g["Score Final"],
                mode="lines+markers",
                line=dict(width=3),
            )
        )
    fig.update_layout(
        height=420,
        yaxis_title="Score (0–100)",
        yaxis=dict(range=[0, 100], gridcolor="#E2E8F0"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        font=dict(family="Segoe UI", color=TEXTO_MUTE),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=1.12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")
else:
    empty_state()

secao("Último Ciclo vs Ciclo Anterior")
evol = evolucao(doc, ind, tre, qua)
if not evol.empty:
    exibir = evol.copy()
    exibir["Faixa"] = exibir["Faixa"].map(chip_faixa)
    exibir["Evolução"] = exibir["Evolução"].map(chip_evolucao)
    st.markdown(
        tabela_html(
            exibir[
                [
                    "Operação",
                    "Data Primeira Avaliação",
                    "Data Última Avaliação",
                    "Score Final Ciclo Anterior",
                    "Score Final Último Ciclo",
                    "Variação",
                    "Faixa",
                    "Evolução",
                ]
            ].astype(object).map(lambda v: f"{v:.1f}" if isinstance(v, (int, float)) else v)
        ),
        unsafe_allow_html=True,
    )
else:
    empty_state()