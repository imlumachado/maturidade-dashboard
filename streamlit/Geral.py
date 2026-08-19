# -*- coding: utf-8 -*-
"""Dashboard de Análise de Maturidade — Página Geral."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Análise de Maturidade",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from common import dados_filtrados, dados_filtrados_op, preparar_dados
from metrics import (
    evolucao,
    faixa_maturidade,
    metricas_geral,
    scores_por_operacao,
    ultimo_ciclo_global,
)
from theme import CORES_FRENTES, VERDE, PRETO, TEXTO_MUTE
from ui import (
    aplicar_css,
    card,
    chip_evolucao,
    chip_faixa,
    empty_state,
    header,
    linha_cards,
    navegacao,
    secao,
    tabela_html,
    titulo_pagina,
)


def _fmt_pct(v):
    return f"{v:.0f}%" if v is not None else "—"


def _fmt_score(v):
    return f"{v:.1f}" if v is not None else "—"


def _fmt_int(v):
    return str(int(v)) if v is not None else "0"


preparar_dados()
doc, ind, tre, qua = dados_filtrados()
doc_op, ind_op, tre_op, qua_op = dados_filtrados_op()
plano = st.session_state.plano

aplicar_css()
navegacao("Geral.py")
header("Visão Geral", "Análise de Maturidade em Processos")
titulo_pagina("Visão Geral", "Análise de Maturidade em Processos")

if doc.empty and ind.empty and tre.empty and qua.empty:
    empty_state("Nenhum dado para os filtros selecionados.")
    st.stop()

geral = metricas_geral(doc, ind, tre, qua)
score_ultimo = ultimo_ciclo_global(doc_op, ind_op, tre_op, qua_op)
faixa = faixa_maturidade(score_ultimo)
metricas_pa = {
    "Vencidas": int(
        ((plano["Prazo"] < pd.Timestamp.today().normalize()) & (plano["Status da Ação"] != "Concluído")).sum()
    )
    if not plano.empty
    else 0
}

secao("Indicadores-chave")
linha_cards(
    [
        {
            "titulo": "Score Final",
            "valor": score_ultimo,
            "sub": faixa or "",
            "cor": VERDE,
            "valor_format": _fmt_score,
            "tooltip": f"Operações avaliadas: <b>{geral['Operações Avaliadas']}</b><br>Ações vencidas: <b>{metricas_pa['Vencidas']}</b>",
        },
    ]
)
st.caption("Passe o cursor sobre o card para ver operações avaliadas e ações vencidas.")

secao("Alertas")
linha_cards(
    [
        {"titulo": "Itens Avaliados Total", "valor": geral["Itens Avaliados Total"], "cor": PRETO, "valor_format": _fmt_int},
        {"titulo": "Graves Total", "valor": geral["Graves Total"], "cor": "#DC2626", "valor_format": _fmt_int},
        {"titulo": "Não Conformes Total", "valor": geral["Não Conformes Total"], "cor": "#F59E0B", "valor_format": _fmt_int},
        {"titulo": "Itens Negativos Total", "valor": geral["Itens Negativos Total"], "cor": "#EAB308", "valor_format": _fmt_int},
    ]
)

secao("Scores por Operação e Frente")
scores = scores_por_operacao(doc, ind, tre, qua)
if not scores.empty:
    fig = go.Figure()
    for frente in ("Documentação", "Indicadores", "Treinamento", "Qualidade"):
        fig.add_trace(
            go.Bar(
                name=frente,
                x=scores["Operação"],
                y=scores[frente].fillna(0),
                marker_color=CORES_FRENTES[frente],
                text=[f"{v:.0f}" if pd.notna(v) else "" for v in scores[frente]],
                textposition="outside",
            )
        )
    fig.add_trace(
        go.Scatter(
            name="Score Final",
            x=scores["Operação"],
            y=scores["Score Final"],
            mode="lines+markers",
            line=dict(color=PRETO, width=3),
        )
    )
    fig.update_layout(
        barmode="group",
        height=380,
        yaxis_title="Score (0–100)",
        yaxis=dict(range=[0, 100], gridcolor="#E2E8F0"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        font=dict(family="Segoe UI", color=TEXTO_MUTE),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=1.12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")
else:
    empty_state()

secao("Ranking das Operações (último ciclo vs anterior)")
evol = evolucao(doc_op, ind_op, tre_op, qua_op)
if not evol.empty:
    evol_display = evol.copy()
    evol_display["Faixa"] = evol_display["Faixa"].map(chip_faixa)
    evol_display["Evolução"] = evol_display["Evolução"].map(chip_evolucao)
    st.markdown(
        tabela_html(
            evol_display[
                [
                    "Operação",
                    "Score Final Último Ciclo",
                    "Faixa",
                    "Score Final Ciclo Anterior",
                    "Variação",
                    "Evolução",
                ]
            ].astype(object).map(lambda v: f"{v:.1f}" if isinstance(v, (int, float)) else v)
        ),
        unsafe_allow_html=True,
    )
else:
    empty_state()