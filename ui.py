# -*- coding: utf-8 -*-
"""Interface padrão das páginas: estilos, cards, navegação e tabelas."""

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
    .dash-nav {{
        margin-bottom: 18px;
    }}
    .dash-nav .stButton {{
        margin-bottom: 4px;
    }}
.dash-nav .stButton > button {{
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
    .dash-nav .stButton > button:hover {{
        background: {VERDE_CLARO};
        color: {VERDE_ESCURO};
        transform: translateX(3px);
        border-color: rgba(5,150,105,.25);
    }}
    .dash-nav .stButton > button:focus {{
        box-shadow: none;
    }}
    .dash-nav-item {{
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
    .dash-card {{
        position: relative;
        background: {BRANCO};
        border: 1px solid {BORDA};
        border-radius: 14px;
        padding: 20px 22px;
        height: 100%;
        box-shadow: 0 1px 4px rgba(15,23,42,.05);
        transition: box-shadow .45s cubic-bezier(.25,.1,.25,1), transform .35s cubic-bezier(.25,.1,.25,1), border-color .45s cubic-bezier(.25,.1,.25,1);
    }}
    .dash-card:hover {{
        box-shadow: 0 6px 20px rgba(15,23,42,.09);
        transform: translateY(-2px);
        border-color: #BFDBFE;
    }}
    .dash-card .kpi-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}
    .dash-card .kpi-label {{
        color: {TEXTO_MUTE};
        font-size: .70rem;
        text-transform: uppercase;
        letter-spacing: .09em;
        font-weight: 600;
    }}
    .dash-card .kpi-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: {VERDE};
    }}
    .dash-card .kpi-value {{
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.05;
        color: {PRETO};
        letter-spacing: -0.02em;
    }}
    .dash-card .kpi-value small {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {TEXTO_MUTE};
    }}
    .dash-card .kpi-sub {{
        color: {TEXTO_MUTE};
        font-size: .8rem;
        margin-top: 8px;
    }}

    /* ===== Tooltip no card ===== */
    .dash-tooltip-wrap {{
        max-height: 0;
        overflow: hidden;
        transition: max-height .45s cubic-bezier(.25,.1,.25,1), padding .35s cubic-bezier(.25,.1,.25,1);
        padding: 0;
    }}
    .dash-tooltip {{
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
    .dash-card:hover .dash-tooltip-wrap {{
        max-height: 120px;
        padding-bottom: 4px;
    }}

    /* ===== Seções ===== */
    .dash-section {{
        margin-top: 28px;
        margin-bottom: 12px;
    }}
    .dash-section h4 {{
        font-size: 1.02rem;
        font-weight: 700;
        margin: 0 0 12px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .dash-section h4::before {{
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
    .dash-table {{
        width: 100%;
        border-collapse: collapse;
        background: {BRANCO};
        border-radius: 12px;
        overflow: hidden;
        font-size: .86rem;
        box-shadow: 0 1px 4px rgba(15,23,42,.05);
    }}
    .dash-table th {{
        background: {CINZA_ESCURO};
        color: {BRANCO};
        text-align: left;
        padding: 11px 14px;
        font-weight: 600;
        font-size: .76rem;
        text-transform: uppercase;
        letter-spacing: .05em;
    }}
    .dash-table td {{
        padding: 10px 14px;
        border-bottom: 1px solid {BORDA};
        color: {PRETO};
    }}
    .dash-table tr:hover td {{
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
        .dash-card {{
            padding: 16px 18px;
        }}
        .dash-card .kpi-value {{
            font-size: 1.7rem;
        }}
        .dash-table {{
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }}
        .dash-card .kpi-value small {{
            font-size: .95rem;
        }}
    }}
    @media (max-width: 480px) {{
        .app-header h1, .page-head h1 {{
            font-size: 1.1rem;
        }}
        .dash-card .kpi-value {{
            font-size: 1.5rem;
        }}
        .dash-section h4 {{
            font-size: .95rem;
        }}
    }}

    /* ===== Sidebar Nav — oculta a nativa do Streamlit ===== */
    [data-testid="stSidebarNav"] {{ display: none; }}

    /* ===== Expander — ícone de seta ===== */
    [data-testid="stExpander"] summary {{
        list-style: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    [data-testid="stExpander"] summary::marker {{
        display: none;
    }}
    [data-testid="stExpander"] summary::-webkit-details-marker {{
        display: none;
    }}
    [data-testid="stExpander"] summary svg {{
        display: none !important;
    }}
    [data-testid="stExpander"] summary span {{
        font-size: 0 !important;
        visibility: hidden !important;
        line-height: 0 !important;
    }}
    [data-testid="stExpander"] summary p {{
        font-size: 0 !important;
        visibility: hidden !important;
    }}
    [data-testid="stExpander"] summary div {{
        font-size: 0 !important;
        visibility: hidden !important;
    }}
    [data-testid="stExpander"] summary::before {{
        content: "›";
        font-size: 14px;
        font-weight: 700;
        color: #64748B;
        transition: transform .2s ease;
        flex-shrink: 0;
        visibility: visible !important;
    }}
    [data-testid="stExpander"][open] summary::before {{
        content: "↓";
    }}
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        position: sticky;
        top: 20px;
        z-index: 100;
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 12px;
        min-width: 250px;
        max-height: 70vh;
        overflow-y: auto;
    }}

    /* ===== Área de Filtros ===== */
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {{
        min-width: 0;
    }}
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .stButton > button {{
        padding: 4px 8px;
        font-size: .78rem;
        min-height: 0;
        height: auto;
    }}
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .stExpander {{
        margin-top: -4px;
    }}
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .stDateInput {{
        font-size: .85rem;
    }}

    /* ===== Painel de Filtros ===== */
    .filtro-painel {{
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px 18px;
        background: {BRANCO};
        border: 1px solid {BORDA};
        border-left: 3px solid transparent;
        border-radius: 14px;
        padding: 12px 18px;
        box-shadow: 0 1px 4px rgba(15,23,42,.05);
        transition: border-color .45s cubic-bezier(.25,.1,.25,1),
                    box-shadow .45s cubic-bezier(.25,.1,.25,1);
    }}
    .filtro-painel.tem-filtros {{
        border-left-color: {VERDE};
    }}

    .filtro-painel__cabecalho {{
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
    }}
    .filtro-painel__icone {{
        width: 24px;
        height: 24px;
        border-radius: 7px;
        background: {VERDE_CLARO};
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .filtro-painel__icone svg {{
        width: 12px;
        height: 12px;
        fill: {VERDE_ESCURO};
    }}
    .filtro-painel__titulo {{
        font-size: .82rem;
        font-weight: 700;
        color: {PRETO};
        white-space: nowrap;
    }}
    .filtro-painel__contagem {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 18px;
        height: 18px;
        padding: 0 5px;
        border-radius: 9px;
        font-size: .66rem;
        font-weight: 700;
        background: #F1F5F9;
        color: {TEXTO_MUTE};
        transition: background-color .3s, color .3s;
    }}
    .filtro-painel.tem-filtros .filtro-painel__contagem {{
        background: {VERDE};
        color: #fff;
    }}

    .filtro-painel__separador {{
        width: 1px;
        align-self: stretch;
        background: {BORDA};
        flex-shrink: 0;
    }}

    .filtro-painel__chips {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 6px;
        flex: 1;
        min-width: 0;
    }}
    .filtro-chip {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #F8FAFC;
        border: 1px solid #EEF2F6;
        color: #334155;
        font-size: .74rem;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 999px;
        white-space: nowrap;
    }}
    .filtro-chip__dot {{
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: {VERDE};
        flex-shrink: 0;
    }}
    .filtro-chip__rotulo {{
        color: {TEXTO_MUTE};
        font-weight: 600;
    }}
    .filtro-painel__vazio {{
        font-size: .78rem;
        color: {TEXTO_MUTE};
    }}

    /* Botao "Limpar" — renderizado por st.button ao lado do card */
    .filtro-limpar .stButton > button {{
        background: transparent !important;
        border: none !important;
        color: {TEXTO_MUTE} !important;
        font-size: .76rem !important;
        font-weight: 600 !important;
        padding: 4px 2px !important;
        height: auto !important;
        min-height: 0 !important;
        text-decoration: underline;
        text-decoration-color: transparent;
        transition: color .2s, text-decoration-color .2s;
    }}
    .filtro-limpar .stButton > button:hover {{
        color: #DC2626 !important;
        text-decoration-color: #DC2626 !important;
        background: transparent !important;
        transform: none !important;
    }}

    @media (max-width: 768px) {{
        .filtro-painel {{
            padding: 10px 14px;
        }}
        .filtro-painel__separador {{
            display: none;
        }}
    }}
</style>
"""

NAV_ITENS = [
    ("app.py", "Visão Geral"),
    ("pages/1_Documentação.py", "Documentação"),
    ("pages/2_Indicadores.py", "Indicadores"),
    ("pages/3_Treinamento.py", "Treinamento"),
    ("pages/Monitoria.py", "Qualidade"),
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
                st.markdown(f'<div class="dash-nav-item">{nome}</div>', unsafe_allow_html=True)
            else:
                if st.button(nome, key=f"nav_{arquivo}", use_container_width=True):
                    st.switch_page(arquivo)


def barra_filtros(
    titulo: str,
    filtros_ativos: list[tuple[str, str]],
    key: str = "barra_filtros_limpar",
    ao_limpar=None,
) -> None:
    if not filtros_ativos:
        return

    chips_html = "".join(
        f'<span class="filtro-chip">'
        f'<span class="filtro-chip__dot"></span>'
        f'<span class="filtro-chip__rotulo">{rotulo}:</span>&nbsp;{valor}'
        f"</span>"
        for rotulo, valor in filtros_ativos
    )

    st.markdown(
        f"""
        <div class="filtro-painel tem-filtros">
            <div class="filtro-painel__cabecalho">
                <div class="filtro-painel__icone">
                    <svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2 4h16l-6 7v5l-4 2v-7z"/>
                    </svg>
                </div>
                <span class="filtro-painel__titulo">{titulo}</span>
                <span class="filtro-painel__contagem">{len(filtros_ativos)}</span>
            </div>
            <div class="filtro-painel__separador"></div>
            <div class="filtro-painel__chips">{chips_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="filtro-limpar">', unsafe_allow_html=True)
    if st.button("Limpar", key=key, use_container_width=True):
        if ao_limpar:
            ao_limpar()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


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
    st.markdown(f'<div class="dash-section"><h4>{titulo}</h4></div>', unsafe_allow_html=True)


def card(titulo: str, valor, sub: str = "", cor: str = VERDE, valor_format=None, tooltip: str = ""):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        texto = "—"
    else:
        texto = str(valor) if valor_format is None else valor_format(valor)
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    tooltip_html = (
        f'<div class="dash-tooltip-wrap"><div class="dash-tooltip">{tooltip}</div></div>' if tooltip else ""
    )
    st.markdown(
        f"""
        <div class="dash-card">
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
    return f'<table class="dash-table">{df.to_html(escape=False, index=False)}</table>'
