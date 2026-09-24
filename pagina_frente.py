# -*- coding: utf-8 -*-
"""Layout padrão das páginas de frente (Documentação, Indicadores, Treinamento, Qualidade)."""

import pandas as pd
import streamlit as st

from metrics import metricas_frente
from theme import TEXTO_MUTE, cor_score_gradiente, fmt_num
from ui import (
    aplicar_css,
    empty_state,
    linha_cards,
    secao,
    titulo_pagina,
)


def _fmt_pct(v):
    return f"{fmt_num(v)}%" if v is not None else "0%"


def _fmt_score(v):
    return fmt_num(v) if v is not None else "—"


def _fmt_int(v):
    return str(int(v)) if v is not None else "0"


def _layout_fig(height=320):
    return dict(
        height=height,
        yaxis_title="Score (0–100)",
        yaxis=dict(range=[0, 100], gridcolor="#E2E8F0"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        font=dict(family="Stack Sans Text, Segoe UI", color=TEXTO_MUTE),
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
    titulo_pagina(titulo, subtitulo)

    if df.empty:
        empty_state()
        return

    m = metricas_frente(df, subs)
    labels = [
        ("Existência", "Sub Existência"),
        ("Aplicação", "Sub Aplicação"),
        ("Padrão", "Sub Padrão"),
        ("Conformidade", "Sub Conformidade"),
        ("Atualização", "Sub Atualização"),
    ]

    rotulo_total = {
        "Documentação": "Documentos avaliados",
        "Qualidade": "Monitorias avaliadas",
    }.get(titulo, f"{titulo} Avaliados")
    secao("Indicadores-chave")
    cards = [
        {"titulo": f"Score {titulo}", "valor": m["Score"], "cor": cor_score_gradiente(m["Score"]), "valor_format": _fmt_score},
        {"titulo": rotulo_total, "valor": m["Total"], "cor": cor_frente, "valor_format": _fmt_int},
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
    cards.append({"titulo": f"Parciais ({titulo})", "valor": m["Parciais"], "cor": "#F59E0B", "valor_format": _fmt_int})
    linha_cards(cards)
