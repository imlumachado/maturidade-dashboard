# -*- coding: utf-8 -*-
"""Página Qualidade."""
import streamlit as st

st.set_page_config(page_title="Qualidade", page_icon="🏅", layout="wide")

from common import dados_filtrados, preparar_dados
from metrics import SUB_QUA
from pagina_frente import renderizar
from theme import CORES_FRENTES

preparar_dados()
_, _, _, qua = dados_filtrados()

renderizar(
    qua,
    titulo="Qualidade",
    subtitulo="Existência, abrangência e conformidade das monitorias de qualidade.",
    subs=SUB_QUA,
    col_item="Processo avaliado",
    cor_frente=CORES_FRENTES["Qualidade"],
    cols_tabela=[
        "Operação",
        "Processo avaliado",
        "ScoreLinha",
        "Sub Existência",
        "Sub Abrangência",
        "Sub Conformidade",
        "Observação",
    ],
)