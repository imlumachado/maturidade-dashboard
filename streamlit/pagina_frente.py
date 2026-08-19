# -*- coding: utf-8 -*-
"""Helper para as páginas de frente (Documentação, Indicadores, Treinamento)."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from metrics import metricas_frente
from theme import TEXTO_MUTE, VERDE
from ui import (
    aplicar_css,
    empty_state,
    header,
    linha_cards,
    navegacao,
    secao,
    titulo_pagina,
)


def _fmt_pct(v):
    return f"{v:.0f}%" if v is not None else "—"


def _fmt_score(v):
    return f"{v:.1f}" if v is not None else "—"


def _fmt_int(v):
    return str(int(v)) if v is not None else "0"


def _layout_fig(height=320):
    return dict(
        height=height,
        yaxis_title="Score (0–100)",
        yaxis=dict(range=[0, 100], gridcolor="#E2E8F0"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        font=dict(family="Segoe UI", color=TEXTO_MUTE),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=1.12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )


def renderizar(
    df: pd.DataFrame,
    titulo: str,
    subtitulo: str,
    subs: list[str],
    col_item: str,
    cor_frente: str,
    cols_tabela: list[str],
    arquivo: str = "",
):
    aplicar_css()
    navegacao(arquivo)
    header(titulo)
    titulo_pagina(titulo, subtitulo)

    if df.empty:
        empty_state()
        return

    m = metricas_frente(df, subs)
    if "Sub Coerência" in subs:
        labels = [
            ("Coerência", "Sub Coerência"),
            ("Aplicação", "Sub Aplicação"),
            ("Atualização", "Sub Atualização"),
            ("Conformidade", "Sub Conformidade"),
        ]
    elif "Sub Abrangência" in subs:
        labels = [
            ("Existência", "Sub Existência"),
            ("Abrangência", "Sub Abrangência"),
            ("Conformidade", "Sub Conformidade"),
        ]
    else:
        labels = [
            ("Existência", "Sub Existência"),
            ("Atualização", "Sub Atualização"),
            ("Padrão", "Sub Padrão"),
            ("Conformidade", "Sub Conformidade"),
        ]

    secao("Indicadores-chave")
    cards = [
        {"titulo": f"{titulo} Avaliados", "valor": m["Total"], "cor": cor_frente, "valor_format": _fmt_int},
    ]
    for rotulo, sub in labels:
        cards.append(
            {
                "titulo": f"% {rotulo}",
                "valor": m.get("% " + sub),
                "cor": cor_frente,
                "valor_format": _fmt_pct,
            }
        )
    cards.append({"titulo": f"Score {titulo}", "valor": m["Score"], "cor": cor_frente, "valor_format": _fmt_score})
    cards.append({"titulo": f"Graves ({titulo})", "valor": m["Graves"], "cor": "#DC2626", "valor_format": _fmt_int})
    linha_cards(cards)

    secao(f"Score {titulo} por Operação")
    por_op = df.groupby("Operação")["ScoreLinha"].mean().sort_values(ascending=False).reset_index()
    fig = go.Figure(
        go.Bar(
            x=por_op["Operação"],
            y=por_op["ScoreLinha"],
            marker_color=cor_frente,
            text=[f"{v:.0f}" for v in por_op["ScoreLinha"]],
            textposition="outside",
        )
    )
    fig.update_layout(**_layout_fig())
    st.plotly_chart(fig, width="stretch")

    secao("Sub-scores por Operação")
    fig2 = go.Figure()
    for rotulo, sub in labels:
        serie = df.groupby("Operação")[sub].mean() * 100
        fig2.add_trace(
            go.Scatter(
                name=rotulo,
                x=serie.index,
                y=serie.values,
                mode="lines+markers",
            )
        )
    fig2.update_layout(**_layout_fig())
    st.plotly_chart(fig2, width="stretch")

    secao("Detalhe")
    visiveis = [c for c in cols_tabela if c in df.columns]
    st.dataframe(
        df[visiveis],
        hide_index=True,
        width="stretch",
        column_config={
            "ScoreLinha": st.column_config.ProgressColumn(
                "ScoreLinha", min_value=-100, max_value=100, format="%.0f"
            )
        },
    )