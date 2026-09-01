# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st

from data_loader import _mtime, carregar_dados as _carregar

_FATOS = ("Documentacao", "Indicadores", "Treinamento", "Qualidade")


@st.cache_data(show_spinner="Carregando formulário de maturidade...")
def _carregar_cache() -> dict:
    return _carregar(_mtime())


def _filtrar_data(df: pd.DataFrame, inicio, fim) -> pd.DataFrame:
    if df.empty or inicio is None or fim is None:
        return df
    datas = pd.to_datetime(df["Data da avaliação"]).dt.date
    return df[(datas >= inicio) & (datas <= fim)]


def preparar_dados() -> None:
    """Carrega os dados e guarda as versões filtradas no session_state."""
    dados = _carregar_cache()
    st.session_state.dados = dados

    ops = sorted(
        {o for df in dados.values() if not df.empty for o in df["Operação"].dropna().unique()}
    )

    datas_todas = pd.concat(
        [dados[f]["Data da avaliação"] for f in _FATOS]
    ).dropna()
    if datas_todas.empty:
        inicio = fim = None
    else:
        minimo, maximo = datas_todas.min().date(), datas_todas.max().date()

    ops_todas = set(ops)

    if "ops_sel" not in st.session_state:
        st.session_state.ops_sel = ops_todas

    st.markdown('<div style="height:120px"></div>', unsafe_allow_html=True)

    _, col_filtros = st.columns([2, 1])
    with col_filtros:
        col_op, col_periodo = st.columns(2)
        with col_op:
            st.markdown("**Operações**")

            if st.button("Todas", use_container_width=True, key="btn_todas_ops"):
                st.session_state.ops_sel = ops_todas
                for op in ops:
                    st.session_state[f"op_{op}"] = True
                st.rerun()

            n_sel = len(st.session_state.ops_sel)
            n_total = len(ops)
            label = f"{n_sel}/{n_total} selecionadas"

            with st.expander(label, expanded=False):
                for op in ops:
                    marcado = op in st.session_state.ops_sel
                    if st.checkbox(op, value=marcado, key=f"op_{op}"):
                        st.session_state.ops_sel.add(op)
                    else:
                        st.session_state.ops_sel.discard(op)

            selecao_ops = sorted(st.session_state.ops_sel)

        with col_periodo:
            st.markdown("**Período**")
            if datas_todas.empty:
                st.caption("Nenhuma avaliação registrada.")
                inicio = fim = None
            else:
                try:
                    periodo = st.date_input(
                        "Período",
                        value=(minimo, maximo),
                        min_value=minimo,
                        max_value=maximo,
                        format="DD/MM/YYYY",
                        key="periodo_ui",
                        label_visibility="collapsed",
                    )
                except Exception:
                    periodo = (minimo, maximo)
                if isinstance(periodo, tuple):
                    inicio, fim = periodo[0], periodo[1] if len(periodo) > 1 else periodo[0]
                else:
                    inicio = fim = periodo

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


def dados_filtrados() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    f = st.session_state.filt
    return f["Documentacao"], f["Indicadores"], f["Treinamento"], f["Qualidade"]


def dados_filtrados_op() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    f = st.session_state.filt_op
    return f["Documentacao"], f["Indicadores"], f["Treinamento"], f["Qualidade"]