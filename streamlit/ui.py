# -*- coding: utf-8 -*-
"""Helpers de interface — visual corporativo refinado.

Header limpo, navegação superior com fade na troca de página, cards
minimalistas com acento verde, chips coloridos e tabelas estilizadas.
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
    VERDE_CLARO,
    VERDE_ESCURO,
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
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        animation: pageFade .55s cubic-bezier(.25,.1,.25,1) both;
    }}
    @keyframes pageFade {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        color: {PRETO} !important;
        letter-spacing: -0.01em;
    }}
    p, span, div, label, .stMarkdown, .stDataFrame {{
        font-family: "Segoe UI", -apple-system, sans-serif !important;
    }}

    /* ===== Header ===== */
    .app-header {{
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 18px;
        padding-bottom: 14px;
        border-bottom: 1px solid {BORDA};
    }}
    .app-header h1 {{
        font-size: 1.65rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }}
    .app-header .app-header-sub {{
        color: {TEXTO_MUTE};
        font-size: .92rem;
        margin-top: 2px;
    }}

    /* ===== Navegação (sidebar) ===== */
    .dbm-nav {{
        margin-bottom: 18px;
    }}
    .dbm-nav .stButton {{
        margin-bottom: 4px;
    }}
    .dbm-nav .stButton > button {{
        width: 100%;
        text-align: left;
        background: transparent;
        color: {TEXTO_MUTE};
        font-size: .86rem;
        font-weight: 600;
        padding: 9px 14px;
        border-radius: 9px;
        border: 1px solid transparent;
        transition: background-color .3s ease, color .3s ease, transform .2s ease, box-shadow .3s ease;
        white-space: nowrap;
    }}
    .dbm-nav .stButton > button:hover {{
        background: {VERDE_CLARO};
        color: {VERDE_ESCURO};
        transform: translateX(2px);
    }}
    .dbm-nav .stButton > button:focus {{
        box-shadow: none;
    }}
    .dbm-nav-item {{
        width: 100%;
        text-align: left;
        background: {VERDE};
        color: {BRANCO};
        font-size: .86rem;
        font-weight: 700;
        padding: 10px 14px;
        border-radius: 9px;
        box-shadow: 0 2px 6px rgba(5,150,105,.35);
        white-space: nowrap;
        margin-bottom: 4px;
    }}

    /* ===== Cabeçalho da página ===== */
    .page-head {{
        margin-bottom: 20px;
    }}
    .page-head h1 {{
        font-size: 1.55rem;
        font-weight: 800;
        margin: 0;
    }}
    .page-head .page-head-sub {{
        color: {TEXTO_MUTE};
        font-size: .92rem;
        margin-top: 2px;
    }}
    .page-head .page-head-rule {{
        height: 3px;
        width: 52px;
        background: {VERDE};
        border-radius: 999px;
        margin-top: 10px;
    }}

    /* ===== Cards KPI ===== */
    .dbm-card {{
        position: relative;
        background: {BRANCO};
        border: 1px solid {BORDA};
        border-radius: 14px;
        padding: 20px 22px;
        height: 100%;
        box-shadow: 0 1px 4px rgba(15,23,42,.05);
        transition: box-shadow .25s ease, transform .25s ease, border-color .25s ease;
    }}
    .dbm-card:hover {{
        box-shadow: 0 6px 20px rgba(15,23,42,.09);
        transform: translateY(-2px);
        border-color: #BFDBFE;
    }}
    .dbm-card .kpi-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}
    .dbm-card .kpi-label {{
        color: {TEXTO_MUTE};
        font-size: .70rem;
        text-transform: uppercase;
        letter-spacing: .09em;
        font-weight: 600;
    }}
    .dbm-card .kpi-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {VERDE};
    }}
    .dbm-card .kpi-value {{
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.05;
        color: {PRETO};
        letter-spacing: -0.02em;
    }}
    .dbm-card .kpi-value small {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {TEXTO_MUTE};
    }}
    .dbm-card .kpi-sub {{
        color: {TEXTO_MUTE};
        font-size: .8rem;
        margin-top: 8px;
    }}

    /* ===== Tooltip no card ===== */
    .dbm-tooltip-wrap {{
        max-height: 0;
        overflow: hidden;
        transition: max-height .2s ease, padding .2s ease;
        padding: 0;
    }}
    .dbm-tooltip {{
        background: {PRETO};
        color: {BRANCO};
        padding: 9px 12px;
        border-radius: 8px;
        font-size: .78rem;
        font-weight: 500;
        line-height: 1.5;
        white-space: normal;
        text-align: center;
        margin-top: 8px;
        box-shadow: 0 4px 12px rgba(15,23,42,.25);
        display: inline-block;
    }}
    .dbm-card:hover .dbm-tooltip-wrap {{
        max-height: 120px;
        padding-bottom: 4px;
    }}

    /* ===== Seções ===== */
    .dbm-section {{
        margin-top: 28px;
        margin-bottom: 12px;
    }}
    .dbm-section h4 {{
        font-size: 1.02rem;
        font-weight: 700;
        margin: 0 0 12px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .dbm-section h4::before {{
        content: "";
        width: 4px;
        height: 16px;
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
    [data-testid="stSidebarCollapseButton"] span {{
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        font-size: 0 !important;
        visibility: hidden;
    }}
    [data-testid="stSidebarCollapseButton"] span::after {{
        content: "‹";
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        font-size: 18px !important;
        font-weight: 700;
        color: {TEXTO_MUTE};
        visibility: visible;
        line-height: 1;
    }}
    [data-testid="stSidebarControlButton"] span {{
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        font-size: 0 !important;
        visibility: hidden;
    }}
    [data-testid="stSidebarControlButton"] span::after {{
        content: "›";
        font-family: "Segoe UI", -apple-system, sans-serif !important;
        font-size: 18px !important;
        font-weight: 700;
        color: {TEXTO_MUTE};
        visibility: visible;
        line-height: 1;
    }}

    /* ===== Tabelas HTML ===== */
    .dbm-table {{
        width: 100%;
        border-collapse: collapse;
        background: {BRANCO};
        border-radius: 12px;
        overflow: hidden;
        font-size: .86rem;
        box-shadow: 0 1px 4px rgba(15,23,42,.05);
    }}
    .dbm-table th {{
        background: {CINZA_ESCURO};
        color: {BRANCO};
        text-align: left;
        padding: 11px 14px;
        font-weight: 600;
        font-size: .76rem;
        text-transform: uppercase;
        letter-spacing: .05em;
    }}
    .dbm-table td {{
        padding: 10px 14px;
        border-bottom: 1px solid {BORDA};
        color: {PRETO};
    }}
    .dbm-table tr:hover td {{
        background: {VERDE_CLARO};
    }}

    /* ===== Botões ===== */
    .stButton > button {{
        border-radius: 10px;
        border: 1px solid {BORDA};
        font-weight: 600;
        transition: all .2s ease;
    }}
    .stButton > button:hover {{
        border-color: {VERDE};
        color: {VERDE_ESCURO};
        transform: translateY(-1px);
    }}
</style>
"""

NAV_ITENS = [
    ("Geral.py", "Visão Geral"),
    ("pages/1_Documentação.py", "Documentação"),
    ("pages/2_Indicadores.py", "Indicadores"),
    ("pages/3_Treinamento.py", "Treinamento"),
    ("pages/6_Qualidade.py", "Qualidade"),
    ("pages/4_Evolução.py", "Evolução"),
    ("pages/5_Plano_de_ação.py", "Plano de Ação"),
]


def aplicar_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def navegacao(atual: str = "") -> None:
    """Navegação vertical na sidebar. O item ativo fica destacado em verde e
    os botões desvanecem (fade) ao trocar de página (animação de entrada)."""
    with st.sidebar:
        st.markdown(
            '<div class="dbm-nav"><div class="dbm-nav-item" style="margin-bottom:10px;background:#EDF9F3;color:#065F46;box-shadow:none;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;">Navegação</div></div>',
            unsafe_allow_html=True,
        )
        for arquivo, nome in NAV_ITENS:
            if arquivo == atual:
                st.markdown(f'<div class="dbm-nav-item">{nome}</div>', unsafe_allow_html=True)
            else:
                if st.button(nome, key=f"nav_{arquivo}", use_container_width=True):
                    st.switch_page(arquivo)


def header(pagina: str, subtitulo: str = "") -> None:
    """Cabeçalho limpo com título e subtítulo, sem marca institucional."""
    st.markdown(
        f"""
        <div class="app-header">
            <div>
                <h1>{pagina}</h1>
                <div class="app-header-sub">{subtitulo}</div>
            </div>
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


def card(titulo: str, valor, sub: str = "", cor: str = VERDE, valor_format=None, tooltip: str = ""):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        texto = "—"
    else:
        texto = str(valor) if valor_format is None else valor_format(valor)
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    tooltip_html = (
        f'<div class="dbm-tooltip-wrap"><div class="dbm-tooltip">{tooltip}</div></div>' if tooltip else ""
    )
    st.markdown(
        f"""
        <div class="dbm-card">
            <div class="kpi-top">
                <div class="kpi-label">{titulo}</div>
                <div class="kpi-dot" style="background:{cor}"></div>
            </div>
            <div class="kpi-value">{texto}</div>
            {sub_html}
            {tooltip_html}
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
    cor = VERDE if "▲" in ev else ("#DC2626" if "▼" in ev else TEXTO_MUTE)
    return f'<span style="color:{cor};font-weight:700">{ev}</span>'


def chip_status(status: str) -> str:
    if not status:
        return "—"
    cor = cor_status(status)
    return f'<span style="background:{cor};color:#fff;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap">{status}</span>'


def tabela_html(df: pd.DataFrame) -> str:
    """Converte um DataFrame já com chips HTML em tabela estilizada."""
    return f'<table class="dbm-table">{df.to_html(escape=False, index=False)}</table>'