# -*- coding: utf-8 -*-
"""Página Indicadores."""
import streamlit as st

st.set_page_config(page_title="Indicadores", page_icon="📈", layout="wide")

from common import dados_filtrados, preparar_dados
from metrics import SUB_IND
from pagina_frente import renderizar
from theme import CORES_FRENTES

preparar_dados()
_, ind, _, _ = dados_filtrados()

renderizar(
    ind,
    titulo="Indicadores",
    subtitulo="Existência, forma de atualização, padrão e conformidade dos indicadores.",
    subs=SUB_IND,
    col_item="Nome_Indicador",
    cor_frente=CORES_FRENTES["Indicadores"],
    arquivo="pages/2_Indicadores.py",
    cols_tabela=[
        "Operação",
        "Processo avaliado",
        "Nome_Indicador",
        "ScoreLinha",
        "Sub Existência",
        "Sub Atualização",
        "Sub Padrão",
        "Sub Conformidade",
        "Observação",
    ],
)