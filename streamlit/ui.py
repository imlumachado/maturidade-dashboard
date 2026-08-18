# -*- coding: utf-8 -*-
"""Helpers de interface — visual inspirado no site da dbm.

Header com wordmark "dbm", CSS global, cards minimalistas com acento verde,
chips coloridos e tabelas estilizadas.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from theme import (
    BORDA,
    BRANCO,
    CINZA_ESCURO,
    FUNDO,
    PRETO,
    TEXTO_MUTE,
    VERDE,
    cor_faixa,
    cor_score,
    cor_status,
)

ASSETS = Path(__file__).resolve().parent / "assets"

CSS = f"""
<style>
    /* ===== Globais ===== */
    .stApp {{
        background-color: {FUNDO};
    }}
    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        color: {PRETO} !important;
    }}
    p, span, div, label, .stMarkdown, .stDataFrame {{
        font-family: "Segoe UI", -apple-system, sans-serif !important;
    }}

    /* ===== Header dbm ===== */
    .dbm-header {{
        background: {CINZA_ESCURO};
        border-radius: 14px;
        padding: 18px 28px;
        margin-bottom: 26px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,.10);
    }}
    .dbm-brand {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}
    .dbm-wordmark {{
        font-family: "Segoe UI", sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: .5px;
        color: {BRANCO};
        line-height: 1;
    }}
    .dbm-wordmark span {{
        color: {VERDE};
    }}
    .dbm-brand-divider {{
        width: 1px;
        height: 34px;
        background: rgba(255,255,255,.25);
    }}
    .dbm-title {{
        color: {BRANCO};
        font-size: 1.15rem;
        font-weight: 600;
        line-height: 1.15;
    }}
    .dbm-sub {{
        color: rgba(255,255,255,.7);
        font-size: .82rem;
    }}
    .dbm-tag {{
        background: {VERDE};
        color: {PRETO};
        font-weight: 700;
        font-size: .78rem;
        padding: 6px 14px;
        border-radius: 999px;
        letter-spacing: .04em;
        white-space: nowrap;
    }}

    /* ===== Cabeçalho da página ===== */
    .page-head {{
        margin-bottom: 20px;
    }}
    .page-head h1 {{
        font-size: 1.7rem;
        font-weight: 800;
        margin: 0;
    }}
    .page-head .page-head-sub {{
        color: {TEXTO_MUTE};
        font-size: .95rem;
        margin-top: 2px;
    }}
    .page-head .page-head-rule {{
        height: 4px;
        width: 56px;
        background: {VERDE};
        border-radius: 999px;
        margin-top: 10px;
    }}

    /* ===== Cards KPI ===== */
    .dbm-card {{
        background: {BRANCO};
        border: 1px solid {BORDA};
        border-radius: 14px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 1px 3px rgba(17,17,17,.06);
    }}
    .dbm-card .kpi-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }}
    .dbm-card .kpi-label {{
        color: {TEXTO_MUTE};
        font-size: .72rem;
        text-transform: uppercase;
        letter-spacing: .07em;
        font-weight: 600;
    }}
    .dbm-card .kpi-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: {VERDE};
    }}
    .dbm-card .kpi-value {{
        font-size: 2.0rem;
        font-weight: 800;
        line-height: 1.1;
        color: {PRETO};
    }}
    .dbm-card .kpi-value small {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {TEXTO_MUTE};
    }}
    .dbm-card .kpi-sub {{
        color: {TEXTO_MUTE};
        font-size: .8rem;
        margin-top: 6px;
    }}

    /* ===== Seções ===== */
    .dbm-section {{
        margin-top: 26px;
        margin-bottom: 12px;
    }}
    .dbm-section h4 {{
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 10px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .dbm-section h4::before {{
        content: "";
        width: 10px;
        height: 10px;
        border-radius: 3px;
        background: {VERDE};
    }}

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {{
        background: {BRANCO};
        border-right: 1px solid {BORDA};
    }}
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        color: {PRETO};
    }}

    /* ===== Tabelas HTML ===== */
    .dbm-table {{
        width: 100%;
        border-collapse: collapse;
        background: {BRANCO};
        border-radius: 12px;
        overflow: hidden;
        font-size: .86rem;
        box-shadow: 0 1px 3px rgba(17,17,17,.06);
    }}
    .dbm-table th {{
        background: {CINZA_ESCURO};
        color: {BRANCO};
        text-align: left;
        padding: 10px 12px;
        font-weight: 600;
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .04em;
    }}
    .dbm-table td {{
        padding: 9px 12px;
        border-bottom: 1px solid {BORDA};
        color: {PRETO};
    }}
    .dbm-table tr:hover td {{
        background: #f0fdf7;
    }}
</style>
"""


def aplicar_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def header(pagina: str, subtitulo: str = "") -> None:
    """Header preto estilo dbm com wordmark e tag da página atual."""
    st.markdown(
        f"""
        <div class="dbm-header">
            <div class="dbm-brand">
                <div class="dbm-wordmark">dbm<span>.</span></div>
                <div class="dbm-brand-divider"></div>
                <div>
                    <div class="dbm-title">Análise de Maturidade em Processos</div>
                    <div class="dbm-sub">CX feito por pessoas</div>
                </div>
            </div>
            <div class="dbm-tag">{pagina}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def titulo_pagina(titulo: str, subtitulo: str = "") -> None:
    st.markdown(
        f"""
        <div class="page-head">
            <h1>{titulo}</h1>
            <div class="page-head-sub">{subtitulo}</div>
            <div class="page-head-rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def secao(titulo: str) -> None:
    st.markdown(f'<div class="dbm-section"><h4>{titulo}</h4></div>', unsafe_allow_html=True)


def card(titulo: str, valor, sub: str = "", cor: str = VERDE, valor_format=None):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        texto = "—"
    else:
        texto = str(valor) if valor_format is None else valor_format(valor)
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    st.markdown(
        f"""
        <div class="dbm-card">
            <div class="kpi-top">
                <div class="kpi-label">{titulo}</div>
                <div class="kpi-dot" style="background:{cor}"></div>
            </div>
            <div class="kpi-value">{texto}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def linha_cards(itens, cols: int = 4):
    for i in range(0, len(itens), cols):
        colunas = st.columns(cols)
        for col, item in zip(colunas, itens[i : i + cols]):
            with col:
                card(**item)


def empty_state(mensagem: str = "Sem dados para os filtros selecionados.") -> None:
    st.info(mensagem)


def chip_faixa(faixa: str) -> str:
    if not faixa:
        return "—"
    cor = cor_faixa(faixa)
    return f'<span style="background:{cor};color:#fff;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap">{faixa}</span>'


def chip_evolucao(ev: str) -> str:
    if not ev:
        return "—"
    cor = "#02DE81" if "▲" in ev else ("#E23C3C" if "▼" in ev else "#6b7280")
    return f'<span style="color:{cor};font-weight:700">{ev}</span>'


def chip_status(status: str) -> str:
    if not status:
        return "—"
    cor = cor_status(status)
    return f'<span style="background:{cor};color:#fff;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap">{status}</span>'


def tabela_html(df: pd.DataFrame) -> str:
    """Converte um DataFrame já com chips HTML em tabela estilizada."""
    return f'<table class="dbm-table">{df.to_html(escape=False, index=False)}</table>'
