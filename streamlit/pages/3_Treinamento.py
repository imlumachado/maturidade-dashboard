# -*- coding: utf-8 -*-
"""Página Treinamento."""
import streamlit as st

st.set_page_config(page_title="Treinamento", page_icon="🎓", layout="wide")

from common import dados_filtrados, preparar_dados
from metrics import SUB_TRE
from pagina_frente import renderizar
from theme import CORES_FRENTES
from ui import aplicar_css, navegacao

aplicar_css()
navegacao("pages/3_Treinamento.py")

preparar_dados()
_, _, tre, _ = dados_filtrados()

renderizar(
    tre,
    titulo="Treinamento",
    subtitulo="Coerência, aplicação, atualização e conformidade dos treinamentos.",
    subs=SUB_TRE,
    col_item="Nome_Treinamento",
    cor_frente=CORES_FRENTES["Treinamento"],
    arquivo="pages/3_Treinamento.py",
    cols_tabela=[
        "Operação",
        "Processo avaliado",
        "Nome_Treinamento",
        "ScoreLinha",
        "Sub Coerência",
        "Sub Aplicação",
        "Sub Atualização",
        "Sub Conformidade",
        "Observação",
    ],
)