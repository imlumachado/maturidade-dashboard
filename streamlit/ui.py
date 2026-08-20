# -*- coding: utf-8 -*-
"""Interface padrão das páginas: estilos, cards, navegação e tabelas."""

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
    cor_score_gradiente,
    cor_status,
    fmt_num,
)

ASSETS = Path(__file__).resolve().parent / "assets"

CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Stack+Sans+Text:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Stack+Sans+Notch:wght@500&display=swap');

    /* ===== Globais ===== */
    .stApp {{
        background-color: {FUNDO};
    }}
    .block-container {{
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        animation: pageFade .55s cubic-bezier(.25,.1,.25,1) backwards;
    }}
    @keyframes pageFade {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: "Stack Sans Text", "Segoe UI", -apple-system, sans-serif !important;
        color: {PRETO} !important;
        letter-spacing: -0.01em;
    }}
p, span, div, label, button, input, textarea, select, .stMarkdown, .stDataFrame {{
        font-family: "Stack Sans Text", "Segoe UI", -apple-system, sans-serif !important;
    }}
    b, strong, .kpi-value, h1, h2, h3, h4, h5, h6 {{
        font-family: "Stack Sans Notch", "Stack Sans Text", "Segoe UI", sans-serif !important;
        font-weight: 500 !important;
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
        transition: background-color .7s cubic-bezier(.25,.1,.25,1), color .7s cubic-bezier(.25,.1,.25,1), transform .5s cubic-bezier(.25,.1,.25,1), box-shadow .7s cubic-bezier(.25,.1,.25,1), border-color .7s cubic-bezier(.25,.1,.25,1);
        white-space: nowrap;
    }}
    .dbm-nav .stButton > button:hover {{
        background: {VERDE_CLARO};
        color: {VERDE_ESCURO};
        transform: translateX(3px);
        border-color: rgba(5,150,105,.25);
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
        animation: navFadeIn .7s cubic-bezier(.25,.1,.25,1) backwards;
        transition: background-color .7s cubic-bezier(.25,.1,.25,1), color .7s cubic-bezier(.25,.1,.25,1), box-shadow .7s cubic-bezier(.25,.1,.25,1);
    }}
    @keyframes navFadeIn {{
        from {{ opacity: 0; transform: translateX(-6px); }}
        to {{ opacity: 1; transform: translateX(0); }}
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
        transition: box-shadow .45s cubic-bezier(.25,.1,.25,1), transform .35s cubic-bezier(.25,.1,.25,1), border-color .45s cubic-bezier(.25,.1,.25,1);
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
        transition: max-height .45s cubic-bezier(.25,.1,.25,1), padding .35s cubic-bezier(.25,.1,.25,1);
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
        transition: transform .7s cubic-bezier(.25,.1,.25,1), min-width .7s cubic-bezier(.25,.1,.25,1), max-width .7s cubic-bezier(.25,.1,.25,1), background-color .5s cubic-bezier(.25,.1,.25,1) !important;
    }}
    section[data-testid="stSidebar"] > div {{
        transition: transform .7s cubic-bezier(.25,.1,.25,1), opacity .6s cubic-bezier(.25,.1,.25,1);
    }}
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stExpandSidebarButton"] {{
        transition: transform .6s cubic-bezier(.25,.1,.25,1), opacity .6s cubic-bezier(.25,.1,.25,1), background-color .6s cubic-bezier(.25,.1,.25,1);
    }}
    [data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="stExpandSidebarButton"]:hover {{
        transform: translateY(-2px);
        background-color: {VERDE_CLARO};
    }}
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        color: {PRETO};
    }}
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stExpandSidebarButton"] span {{
        font-family: "Stack Sans Text", "Segoe UI", -apple-system, sans-serif !important;
        font-size: 0 !important;
        visibility: hidden;
    }}
    [data-testid="stSidebarCollapseButton"] span::after {{
        content: "‹";
        font-family: "Stack Sans Text", "Segoe UI", -apple-system, sans-serif !important;
        font-size: 18px !important;
        font-weight: 700;
        color: {TEXTO_MUTE};
        visibility: visible;
        line-height: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }}
    [data-testid="stExpandSidebarButton"] span::after {{
        content: "›";
        font-family: "Stack Sans Text", "Segoe UI", -apple-system, sans-serif !important;
        font-size: 18px !important;
        font-weight: 700;
        color: {TEXTO_MUTE};
        visibility: visible;
        line-height: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
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
        transition: all .45s cubic-bezier(.25,.1,.25,1);
    }}
.stButton > button:hover {{
        border-color: {VERDE};
        color: {VERDE_ESCURO};
        transform: translateY(-1px);
    }}

    /* ===== Responsividade ===== */
    /* Colunas do Streamlit quebram para uma por linha em telas menores */
    [data-testid="stHorizontalBlock"] {{
        flex-wrap: wrap !important;
    }}
    @media (max-width: 1200px) {{
        section[data-testid="stSidebar"] {{
            max-width: 260px !important;
        }}
        .block-container {{
            max-width: 100%;
        }}
    }}
    @media (max-width: 900px) {{
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
            min-width: min(100%, 240px) !important;
            flex-grow: 1 !important;
        }}
    }}
    @media (max-width: 768px) {{
        section[data-testid="stSidebar"] {{
            max-width: 100% !important;
            min-width: 0 !important;
            width: min(85vw, 320px) !important;
        }}
    }}
    @media (max-width: 768px) {{
        .block-container {{
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        .app-header h1, .page-head h1 {{
            font-size: 1.25rem;
        }}
        .dbm-card {{
            padding: 16px 18px;
        }}
        .dbm-card .kpi-value {{
            font-size: 1.7rem;
        }}
        .dbm-table {{
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }}
        .dbm-card .kpi-value small {{
            font-size: .95rem;
        }}
    }}
    @media (max-width: 480px) {{
        .app-header h1, .page-head h1 {{
            font-size: 1.1rem;
        }}
        .dbm-card .kpi-value {{
            font-size: 1.5rem;
        }}
        .dbm-section h4 {{
            font-size: .95rem;
        }}
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
    """Menu lateral. A página atual fica destacada em verde."""
    with st.sidebar:
        for arquivo, nome in NAV_ITENS:
            if arquivo == atual:
                st.markdown(f'<div class="dbm-nav-item">{nome}</div>', unsafe_allow_html=True)
            else:
                if st.button(nome, key=f"nav_{arquivo}", use_container_width=True):
                    st.switch_page(arquivo)


def header(pagina: str, subtitulo: str = "") -> None:
    """Cabeçalho com título e subtítulo."""
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


def chip_score(valor) -> str:
    """Score com fundo em gradiente verde -> amarelo -> vermelho."""
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return "—"
    cor = cor_score_gradiente(valor)
    return (
        f'<span style="background:{cor};color:#fff;padding:2px 10px;'
        f'border-radius:999px;font-size:.78rem;font-weight:700;white-space:nowrap">'
        f"{fmt_num(valor)}</span>"
    )


def chip_status(status: str) -> str:
    if not status:
        return "—"
    cor = cor_status(status)
    return f'<span style="background:{cor};color:#fff;padding:2px 10px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap">{status}</span>'


def tabela_html(df: pd.DataFrame) -> str:
    """DataFrame (já com chips HTML) como tabela estilizada."""
    return f'<table class="dbm-table">{df.to_html(escape=False, index=False)}</table>'
