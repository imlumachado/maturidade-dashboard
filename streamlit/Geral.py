# -*- coding: utf-8 -*-
"""Visão Geral do dashboard de maturidade."""
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
from theme import CORES_FRENTES, PRETO, TEXTO_MUTE, cor_score_gradiente, fmt_num
from ui import (
    aplicar_css,
    card,
    chip_evolucao,
    chip_faixa,
    chip_score,
    empty_state,
    linha_cards,
    navegacao,
    secao,
    tabela_html,
    titulo_pagina,
)


def _fmt_pct(v):
    return f"{fmt_num(v)}%" if v is not None else "0%"


def _fmt_score(v):
    return fmt_num(v) if v is not None else "—"


def _fmt_int(v):
    return str(int(v)) if v is not None else "0"


aplicar_css()
navegacao("Geral.py")

preparar_dados()
doc, ind, tre, qua = dados_filtrados()
doc_op, ind_op, tre_op, qua_op = dados_filtrados_op()
plano = st.session_state.plano

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
            "cor": cor_score_gradiente(score_ultimo),
            "valor_format": _fmt_score,
            "tooltip": f"Operações avaliadas: <b>{geral['Operações Avaliadas']}</b><br>Ações vencidas: <b>{metricas_pa['Vencidas']}</b>",
        },
    ]
)

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
                text=[fmt_num(v) if pd.notna(v) else "" for v in scores[frente]],
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
        font=dict(family="Stack Sans Text, Segoe UI", color=TEXTO_MUTE),
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
    for col in ("Score Final Último Ciclo", "Score Final Ciclo Anterior"):
        evol_display[col] = evol_display[col].map(chip_score)
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
            ].astype(object).map(lambda v: fmt_num(v) if isinstance(v, (int, float)) else v)
        ),
        unsafe_allow_html=True,
    )
else:
    empty_state()
