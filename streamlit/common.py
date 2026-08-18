# -*- coding: utf-8 -*-
"""Compartilhado entre as páginas: carregamento de dados e filtros globais."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from data_loader import carregar_dados as _carregar
from theme import CINZA_ESCURO, VERDE, BRANCO

_FATOS = ("Documentacao", "Indicadores", "Treinamento")


@st.cache_data(show_spinner="Carregando formulário de maturidade...")
def _carregar_cache() -> dict:
    return _carregar()


def _filtrar_data(df: pd.DataFrame, inicio, fim) -> pd.DataFrame:
    if df.empty or inicio is None or fim is None:
        return df
    datas = pd.to_datetime(df["Data da avaliação"]).dt.date
    return df[(datas >= inicio) & (datas <= fim)]


def preparar_dados() -> None:
    """Carrega os dados e grava as versões filtradas em st.session_state.

    - st.session_state.dados   : tabelas originais
    - st.session_state.filt    : filtradas por operação + data (páginas de análise)
    - st.session_state.filt_op : filtradas apenas por operação (página Evolução)
    - st.session_state.plano   : PlanoAcao filtrado por operação
    """
    dados = _carregar_cache()
    st.session_state.dados = dados

    ops = sorted(
        {o for df in dados.values() if not df.empty for o in df["Operação"].dropna().unique()}
    )

    with st.sidebar:
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] > div:first-child {{ background: #ffffff; }}
            </style>
            <div style="background:{CINZA_ESCURO};border-radius:12px;padding:14px 16px;margin-bottom:14px;">
                <div style="font-weight:800;font-size:1.4rem;color:#fff;">dbm<span style="color:{VERDE}">.</span></div>
                <div style="color:rgba(255,255,255,.7);font-size:.78rem;">Análise de Maturidade</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### Filtros")
        selecao_ops = st.multiselect(
            "Operação",
            ops,
            default=ops,
            help="Selecione uma ou mais operações (vazio = todas).",
        )
        datas_todas = pd.concat(
            [dados[f]["Data da avaliação"] for f in _FATOS]
        ).dropna()
        if datas_todas.empty:
            inicio = fim = None
            st.caption("Nenhuma avaliação registrada ainda.")
        else:
            minimo, maximo = datas_todas.min().date(), datas_todas.max().date()
            try:
                periodo = st.date_input(
                    "Período de avaliação",
                    value=(minimo, maximo),
                    min_value=minimo,
                    max_value=maximo,
                )
            except Exception:
                periodo = (minimo, maximo)
            if isinstance(periodo, tuple):
                inicio, fim = periodo[0], periodo[1] if len(periodo) > 1 else periodo[0]
            else:
                inicio = fim = periodo
        st.caption("Fonte: formulário F_O_025_Formulario_Maturidade_Planos.xlsx")

    if not selecao_ops:
        selecao_ops = set(ops)
    else:
        selecao_ops = set(selecao_ops)

    st.session_state.filt = {}
    st.session_state.filt_op = {}
    for chave in _FATOS:
        df = dados[chave]
        df_op = df[df["Operação"].isin(selecao_ops)]
        st.session_state.filt_op[chave] = df_op
        st.session_state.filt[chave] = _filtrar_data(df_op, inicio, fim)

    plano = dados["PlanoAcao"]
    if not plano.empty:
        plano = plano[plano["Operação"].isin(selecao_ops)]
    st.session_state.plano = plano


def dados_filtrados() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    f = st.session_state.filt
    return f["Documentacao"], f["Indicadores"], f["Treinamento"]


def dados_filtrados_op() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    f = st.session_state.filt_op
    return f["Documentacao"], f["Indicadores"], f["Treinamento"]