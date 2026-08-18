# -*- coding: utf-8 -*-
"""Helpers de interface: cards, formatação de tabelas e mensagens."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from theme import cor_faixa, cor_score, cor_status, VERDE, PRETO


def card(titulo: str, valor, sub: str = "", cor: str = VERDE, valor_format=None):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        texto = "—"
    else:
        texto = str(valor) if valor_format is None else valor_format(valor)
    sub_html = f'<div style="font-size:.85rem;color:#6b7280;margin-top:2px">{sub}</div>' if sub else ""
    html = f"""
    <div style="background:#fff;border-radius:12px;padding:18px 20px;
                border-left:6px solid {cor};box-shadow:0 1px 4px rgba(0,0,0,.08);height:100%">
      <div style="font-size:.75rem;color:#6b7280;text-transform:uppercase;
                  letter-spacing:.06em;font-weight:600">{titulo}</div>
      <div style="font-size:1.9rem;font-weight:800;color:{cor};line-height:1.2">{texto}</div>
      {sub_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def linha_cards(itens, cols: int = 4):
    """Exibe uma linha de cards. `itens` = lista de dicts {titulo, valor, sub, cor, valor_format}."""
    for i in range(0, len(itens), cols):
        with st.container():
            colunas = st.columns(cols)
            for col, item in zip(colunas, itens[i : i + cols]):
                with col:
                    card(**item)


def tabela_scores(df: pd.DataFrame, cols_mostrar: list[str], col_score: str) -> None:
    """Tabela com o score em barra de progresso colorida."""
    config = {"score": None}
    for c in cols_mostrar:
        config[c] = None
    config[col_score] = st.column_config.ProgressColumn(
        col_score,
        min_value=-100,
        max_value=100,
        format="%.0f",
        help="Score de 0 a 100",
    )
    st.dataframe(df[cols_mostrar + [col_score]], hide_index=True, use_container_width=True, column_config=config)


def legenda(status: str) -> str:
    cor = cor_status(status)
    return f'<span style="color:{cor};font-weight:700">● {status}</span>'


def empty_state(mensagem: str = "Sem dados para os filtros selecionados.") -> None:
    st.info(mensagem)


def titulo_pagina(titulo: str, subtitulo: str = "") -> None:
    st.markdown(
        f"<h1 style='color:{PRETO};margin-bottom:0'>{titulo}</h1>"
        f"<p style='color:#6b7280;margin-top:0'>{subtitulo}</p>",
        unsafe_allow_html=True,
    )


def chip_faixa(faixa: str) -> str:
    if not faixa:
        return "—"
    cor = cor_faixa(faixa)
    return f'<span style="background:{cor};color:#fff;padding:2px 10px;border-radius:999px;font-size:.8rem;font-weight:600">{faixa}</span>'


def chip_evolucao(ev: str) -> str:
    if not ev:
        return "—"
    cor = "#02DE81" if "▲" in ev else ("#E23C3C" if "▼" in ev else "#6b7280")
    return f'<span style="color:{cor};font-weight:700">{ev}</span>'


def chip_status(status: str) -> str:
    if not status:
        return "—"
    cor = cor_status(status)
    return f'<span style="background:{cor};color:#fff;padding:2px 10px;border-radius:999px;font-size:.8rem;font-weight:600">{status}</span>'