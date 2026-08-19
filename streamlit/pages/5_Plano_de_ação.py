# -*- coding: utf-8 -*-
"""Página Plano de Ação."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Plano de Ação", page_icon="✅", layout="wide")

from common import preparar_dados
from metrics import metricas_plano
from theme import CORES_STATUS, PRETO, TEXTO_MUTE
from ui import (
    aplicar_css,
    chip_status,
    empty_state,
    linha_cards,
    navegacao,
    secao,
    tabela_html,
    titulo_pagina,
)

aplicar_css()
navegacao("pages/5_Plano_de_ação.py")

preparar_dados()
pa = st.session_state.plano

titulo_pagina(
    "Plano de Ação",
    "Ações para calibrar a maturidade das operações na próxima análise.",
)

if pa.empty:
    empty_state("Nenhuma ação de plano de ação preenchida no formulário.")
    st.stop()

m = metricas_plano(pa)


def _fmt_int(v):
    return str(int(v)) if v is not None else "0"


def _fmt_pct(v):
    return f"{v:.2f}%" if v is not None else "0.00%"


secao("Indicadores-chave")
linha_cards(
    [
        {"titulo": "Ações de Plano de Ação", "valor": m["Total"], "cor": PRETO, "valor_format": _fmt_int},
        {"titulo": "Ações Abertas", "valor": m["Abertas"], "cor": CORES_STATUS["Aberto"], "valor_format": _fmt_int},
        {"titulo": "Em Andamento", "valor": m["Em Andamento"], "cor": CORES_STATUS["Em andamento"], "valor_format": _fmt_int},
        {"titulo": "Concluídas", "valor": m["Concluídas"], "cor": CORES_STATUS["Concluído"], "valor_format": _fmt_int},
        {"titulo": "Vencidas", "valor": m["Vencidas"], "cor": "#DC2626", "valor_format": _fmt_int},
        {"titulo": "A Vencer (30 dias)", "valor": m["A Vencer (30 dias)"], "cor": "#F59E0B", "valor_format": _fmt_int},
        {"titulo": "% Concluídas", "valor": m["% Concluídas"], "cor": "#059669", "valor_format": _fmt_pct},
    ]
)

with st.expander("Filtros do Plano de Ação", expanded=False):
    status_opcoes = sorted(pa["Status da Ação"].dropna().unique().tolist())
    status_sel = st.multiselect("Status da Ação", status_opcoes, default=status_opcoes)
    resp_opcoes = sorted(pa["Responsável"].dropna().astype(str).unique().tolist())
    resp_sel = st.multiselect("Responsável", resp_opcoes, default=resp_opcoes)

if status_sel:
    pa = pa[pa["Status da Ação"].isin(status_sel)]
if resp_sel:
    pa = pa[pa["Responsável"].astype(str).isin(resp_sel)]

c1, c2 = st.columns(2)
with c1:
    secao("Ações por Status")
    status_counts = pa["Status da Ação"].fillna("—").value_counts().reindex(
        ["Aberto", "Em andamento", "Concluído"], fill_value=0
    )
    fig = go.Figure(
        go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            marker_color=[CORES_STATUS.get(s, "#94A3B8") for s in status_counts.index],
            text=status_counts.values,
            textposition="outside",
        )
    )
    fig.update_layout(
        height=320,
        font=dict(family="Stack Sans Text, Segoe UI", color=TEXTO_MUTE),
        yaxis=dict(gridcolor="#E2E8F0"),
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")

with c2:
    secao("Ações por Frente")
    frente_counts = pa["Frente"].value_counts()
    fig2 = go.Figure(
        go.Pie(
            labels=frente_counts.index,
            values=frente_counts.values,
            hole=0.5,
            marker=dict(colors=["#059669", "#059669", "#10B981"][: len(frente_counts)]),
        )
    )
    fig2.update_layout(
        height=320,
        font=dict(family="Stack Sans Text, Segoe UI", color=TEXTO_MUTE),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig2, width="stretch")

secao("Detalhe das Ações")
exibir = pa.copy()
exibir["Status da Ação"] = exibir["Status da Ação"].map(chip_status)
hoje = pd.Timestamp.today().normalize()
exibir["Prazo"] = exibir["Prazo"].map(lambda d: d.strftime("%d/%m/%Y") if pd.notna(d) else "—")
vencida = pa["Prazo"].notna() & (pa["Prazo"] < hoje) & (pa["Status da Ação"] != "Concluído")
exibir.loc[vencida.values, "Prazo"] = exibir.loc[vencida.values, "Prazo"].map(
    lambda d: f"<span style='color:#DC2626;font-weight:700'>⚠️ {d}</span>"
)
st.markdown(
    tabela_html(
        exibir[
            ["Operação", "Frente", "Item", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"]
        ]
    ),
    unsafe_allow_html=True,
)
