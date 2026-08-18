# -*- coding: utf-8 -*-
"""Página Plano de Ação."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Plano de Ação", page_icon="✅", layout="wide")

from common import preparar_dados
from metrics import metricas_plano
from theme import CORES_STATUS
from ui import chip_status, empty_state, linha_cards, titulo_pagina

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
    return f"{v:.0f}%" if v is not None else "—"


linha_cards(
    [
        {"titulo": "Ações de Plano de Ação", "valor": m["Total"], "cor": "#212121", "valor_format": _fmt_int},
        {"titulo": "Ações Abertas", "valor": m["Abertas"], "cor": CORES_STATUS["Aberto"], "valor_format": _fmt_int},
        {"titulo": "Em Andamento", "valor": m["Em Andamento"], "cor": CORES_STATUS["Em andamento"], "valor_format": _fmt_int},
        {"titulo": "Concluídas", "valor": m["Concluídas"], "cor": CORES_STATUS["Concluído"], "valor_format": _fmt_int},
        {"titulo": "Vencidas", "valor": m["Vencidas"], "cor": "#E23C3C", "valor_format": _fmt_int},
        {"titulo": "A Vencer (30 dias)", "valor": m["A Vencer (30 dias)"], "cor": "#F59E0B", "valor_format": _fmt_int},
        {"titulo": "% Concluídas", "valor": m["% Concluídas"], "cor": "#02DE81", "valor_format": _fmt_pct},
    ]
)

with st.sidebar:
    st.markdown("#### Plano de Ação")
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
    st.markdown("##### Ações por Status")
    status_counts = pa["Status da Ação"].fillna("—").value_counts().reindex(
        ["Aberto", "Em andamento", "Concluído"], fill_value=0
    )
    fig = go.Figure(
        go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            marker_color=[CORES_STATUS.get(s, "#9CA3AF") for s in status_counts.index],
            text=status_counts.values,
            textposition="outside",
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("##### Ações por Frente")
    frente_counts = pa["Frente"].value_counts()
    fig2 = go.Figure(
        go.Pie(
            labels=frente_counts.index,
            values=frente_counts.values,
            hole=0.5,
            marker=dict(colors=["#02DE81", "#34D399", "#FACC15"][: len(frente_counts)]),
        )
    )
    fig2.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10), showlegend=True)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("##### Detalhe das Ações")
exibir = pa.copy()
exibir["Status da Ação"] = exibir["Status da Ação"].map(chip_status)
hoje = pd.Timestamp.today().normalize()
vencida = pa["Prazo"].notna() & (pa["Prazo"] < hoje) & (pa["Status da Ação"] != "Concluído")
exibir.loc[vencida.values, "Prazo"] = exibir.loc[vencida.values, "Prazo"].map(
    lambda d: f"<span style='color:#E23C3C;font-weight:700'>⚠️ {d.date()}</span>"
)
st.markdown(
    exibir[
        ["Operação", "Frente", "Item", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"]
    ].to_html(escape=False, index=False),
    unsafe_allow_html=True,
)