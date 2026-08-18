# -*- coding: utf-8 -*-
"""Página Documentação."""
import streamlit as st

st.set_page_config(page_title="Documentação", page_icon="📄", layout="wide")

from common import dados_filtrados, preparar_dados
from metrics import SUB_DOC
from pagina_frente import renderizar
from theme import CORES_FRENTES

preparar_dados()
doc, _, _ = dados_filtrados()

renderizar(
    doc,
    titulo="Documentação",
    subtitulo="Existência, atualização, padrão e conformidade dos documentos.",
    subs=SUB_DOC,
    col_item="Nome_Documento",
    cor_frente=CORES_FRENTES["Documentação"],
    cols_tabela=[
        "Operação",
        "Processo avaliado",
        "Nome_Documento",
        "ScoreLinha",
        "Sub Existência",
        "Sub Atualização",
        "Sub Padrão",
        "Sub Conformidade",
        "Observação",
    ],
)