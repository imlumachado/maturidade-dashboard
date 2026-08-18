# -*- coding: utf-8 -*-
"""Página Evolução."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Evolução", page_icon="📈", layout="wide")

from common import dados_filtrados_op, preparar_dados
from metrics import evolucao, serie_evolucao
from theme import cor_score
from ui import chip_evolucao, chip_faixa, empty_state, titulo_pagina

preparar_dados()
doc, ind, tre = dados_filtrados_op()

titulo_pagina(
    "Evolução",
    "Score final ao longo dos ciclos de avaliação (ignora o filtro de período).",
)

if doc.empty and ind.empty and tre.empty:
    empty_state()
    st.stop()

st.markdown("##### Score Final por Ciclo de Avaliação")
serie = serie_evolucao(doc, ind, tre)
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
        yaxis=dict(range=[0, 100]),
        xaxis_title="Data da avaliação",
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=1.12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    empty_state()

st.markdown("##### Último Ciclo vs Ciclo Anterior")
evol = evolucao(doc, ind, tre)
if not evol.empty:
    exibir = evol.copy()
    exibir["Faixa"] = exibir["Faixa"].map(chip_faixa)
    exibir["Evolução"] = exibir["Evolução"].map(chip_evolucao)
    st.markdown(
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
        ].to_html(
            escape=False,
            index=False,
            float_format=lambda v: f"{v:.1f}",
        ),
        unsafe_allow_html=True,
    )
else:
    empty_state()