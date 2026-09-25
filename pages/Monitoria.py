# -*- coding: utf-8 -*-
"""Página Monitoria."""
import streamlit as st

st.set_page_config(page_title="Monitoria", page_icon="🏅", layout="wide")

from common import dados_filtrados, preparar_dados
from metrics import SUB_QUA
from pagina_frente import renderizar
from theme import CORES_FRENTES
from ui import aplicar_css, navegacao

aplicar_css()
navegacao("pages/Monitoria.py")

preparar_dados()
_, _, _, qua = dados_filtrados()

renderizar(
    qua,
    titulo="Monitoria",
    subtitulo="Existência, aplicação, padrão, conformidade e atualização das monitorias de qualidade.",
    subs=SUB_QUA,
    col_item="Frente avaliada",
    cor_frente=CORES_FRENTES["Qualidade"],
    arquivo="pages/Monitoria.py",
    cols_tabela=[
        "Operação",
        "Processo avaliado",
        "Frente avaliada",
        "ScoreLinha",
        "Sub Existência",
        "Sub Aplicação",
        "Sub Padrão",
        "Sub Conformidade",
        "Sub Atualização",
        "Observação",
    ],
    mostrar_total=False,
)