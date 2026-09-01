# -*- coding: utf-8 -*-
"""Página Plano de Ação."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Plano de Ação", page_icon="✅", layout="wide")

from common import preparar_dados
from metrics import metricas_plano
from theme import CORES_STATUS, PRETO, TEXTO_MUTE, fmt_num
from ui import (
    aplicar_css,
    chip_status,
    empty_state,
    linha_cards,
    navegacao,
    secao,
    tabela_html,
    titulo_pagina,
)


@st.cache_data
def get_opcoes(df: pd.DataFrame, coluna: str) -> list:
    if df.empty or coluna not in df.columns:
        return []
    return sorted(df[coluna].dropna().astype(str).unique().tolist())


def _aplicar_filtros(
    pa: pd.DataFrame,
    status_sel: list,
    resp_sel: list,
    frente_sel: list,
    data_inicio,
    data_fim,
) -> pd.DataFrame:
    if not status_sel or not resp_sel or not frente_sel:
        return pa.iloc[0:0]

    filtrado = pa[
        pa["Status da Ação"].isin(status_sel)
        & pa["Responsável"].astype(str).isin(resp_sel)
        & pa["Frente"].astype(str).isin(frente_sel)
    ]

    if data_inicio and data_fim:
        sem_prazo = filtrado["Prazo"].isna()
        dentro_periodo = filtrado["Prazo"].dt.date.between(data_inicio, data_fim)
        filtrado = filtrado[sem_prazo | dentro_periodo]

    return filtrado


def _init_filtros(opcoes: list, key_prefix: str) -> None:
    session_key = f"sel_{key_prefix}"
    if session_key not in st.session_state:
        st.session_state[session_key] = set(opcoes)


def _render_filtro_checkboxes(opcoes: list, key_prefix: str) -> set:
    session_key = f"sel_{key_prefix}"
    selecionados = st.session_state[session_key]

    col_todas, col_nenhuma = st.columns(2)
    with col_todas:
        if st.button("Todas", use_container_width=True, key=f"btn_todas_{key_prefix}"):
            st.session_state[session_key] = set(opcoes)
            st.rerun()
    with col_nenhuma:
        if st.button("Nenhuma", use_container_width=True, key=f"btn_nenhum_{key_prefix}"):
            st.session_state[session_key] = set()
            st.rerun()

    with st.expander(f"{len(selecionados)}/{len(opcoes)} selecionadas", expanded=False):
        for item in opcoes:
            marcado = item in selecionados
            if st.checkbox(item, value=marcado, key=f"chk_{key_prefix}_{item}"):
                st.session_state[session_key].add(item)
            else:
                st.session_state[session_key].discard(item)

    return st.session_state[session_key]


def filtro_plano_acao(pa: pd.DataFrame) -> pd.DataFrame:
    status_opcoes = get_opcoes(pa, "Status da Ação")
    resp_opcoes = get_opcoes(pa, "Responsável")
    frente_opcoes = get_opcoes(pa, "Frente")

    _init_filtros(status_opcoes, "status")
    _init_filtros(resp_opcoes, "resp")
    _init_filtros(frente_opcoes, "frente")

    col_s, col_r, col_f = st.columns(3)
    with col_s:
        st.markdown("#### Status")
        status_sel = _render_filtro_checkboxes(status_opcoes, "status")
    with col_r:
        st.markdown("#### Responsável")
        resp_sel = _render_filtro_checkboxes(resp_opcoes, "resp")
    with col_f:
        st.markdown("#### Frente")
        frente_sel = _render_filtro_checkboxes(frente_opcoes, "frente")

    data_inicio = data_fim = None
    prazos_validos = pa["Prazo"].dropna()
    if not prazos_validos.empty:
        min_data, max_data = prazos_validos.min().date(), prazos_validos.max().date()
        periodo = st.date_input(
            "Período (Prazo)",
            value=(min_data, max_data),
            min_value=min_data,
            max_value=max_data,
        )
        if isinstance(periodo, (tuple, list)) and len(periodo) == 2:
            data_inicio, data_fim = periodo

    status_sel = sorted(status_sel)
    resp_sel = sorted(resp_sel)
    frente_sel = sorted(frente_sel)

    if not status_sel or not resp_sel or not frente_sel:
        st.warning("Selecione ao menos uma opção em cada filtro para ver resultados.")
        return pa.iloc[0:0]

    return _aplicar_filtros(pa, status_sel, resp_sel, frente_sel, data_inicio, data_fim)


aplicar_css()
navegacao("pages/5_Plano_de_ação.py")

preparar_dados()
pa_completo = st.session_state.plano

titulo_pagina(
    "Plano de Ação",
    "Ações para calibrar a maturidade das operações na próxima análise.",
)

if pa_completo.empty:
    empty_state("Nenhuma ação de plano de ação preenchida no formulário.")
    st.stop()

pa = filtro_plano_acao(pa_completo)

if pa.empty:
    empty_state("Nenhuma ação encontrada para os filtros selecionados.")
    st.stop()

m = metricas_plano(pa)


def _fmt_int(v):
    return str(int(v)) if v is not None else "0"


def _fmt_pct(v):
    return f"{fmt_num(v)}%" if v is not None else "0%"


secao("Indicadores-chave")
linha_cards(
    [
        {"titulo": "Ações de Plano de Ação", "valor": m["Total"], "cor": PRETO, "valor_format": _fmt_int},
        {"titulo": "Ações Abertas", "valor": m["Abertas"], "cor": CORES_STATUS["Aberto"], "valor_format": _fmt_int},
        {"titulo": "Em Andamento", "valor": m["Em Andamento"], "cor": CORES_STATUS["Em andamento"], "valor_format": _fmt_int},
        {"titulo": "Concluídas", "valor": m["Concluídas"], "cor": CORES_STATUS["Concluído"], "valor_format": _fmt_int},
        {"titulo": "Vencidas", "valor": m["Vencidas"], "cor": "#DC2626", "valor_format": _fmt_int},
        {"titulo": "A Vencer (30 dias)", "valor": m["A Vencer (30 dias)"], "cor": "#F59E0B", "valor_format": _fmt_int},
        {"titulo": "% Concluídas", "valor": m["% Concluídas"], "cor": "#059669", "valor_format": _fmt_pct},
    ]
)


c1, c2 = st.columns(2)
with c1:
    secao("Ações por Status")
    status_counts = pa["Status da Ação"].fillna("—").value_counts().reindex(
        ["Aberto", "Em andamento", "Concluído"], fill_value=0
    )
    fig = go.Figure(
        go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            marker_color=[CORES_STATUS.get(s, "#94A3B8") for s in status_counts.index],
            text=status_counts.values,
            textposition="outside",
        )
    )
    fig.update_layout(
        height=320,
        font=dict(family="Stack Sans Text, Segoe UI", color=TEXTO_MUTE),
        yaxis=dict(gridcolor="#E2E8F0"),
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")

with c2:
    secao("Ações por Frente")
    frente_counts = pa["Frente"].value_counts()
    fig2 = go.Figure(
        go.Pie(
            labels=frente_counts.index,
            values=frente_counts.values,
            hole=0.5,
            marker=dict(colors=["#059669", "#059669", "#10B981"][: len(frente_counts)]),
        )
    )
    fig2.update_layout(
        height=320,
        font=dict(family="Stack Sans Text, Segoe UI", color=TEXTO_MUTE),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig2, width="stretch")

secao("Detalhe das Ações")
exibir = pa.copy()
exibir["Status da Ação"] = exibir["Status da Ação"].map(chip_status)
hoje = pd.Timestamp.today().normalize()
exibir["Prazo"] = exibir["Prazo"].map(lambda d: d.strftime("%d/%m/%Y") if pd.notna(d) else "—")
vencida = pa["Prazo"].notna() & (pa["Prazo"] < hoje) & (pa["Status da Ação"] != "Concluído")
exibir.loc[vencida.values, "Prazo"] = exibir.loc[vencida.values, "Prazo"].map(
    lambda d: f"<span style='color:#DC2626;font-weight:700'>⚠️ {d}</span>"
)
st.markdown(
    tabela_html(
        exibir[
            ["Operação", "Frente", "Item", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"]
        ]
    ),
    unsafe_allow_html=True,
)