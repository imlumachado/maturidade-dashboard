# -*- coding: utf-8 -*-
"""Smoke test das páginas Streamlit usando AppTest."""
from pathlib import Path

from streamlit.testing.v1 import AppTest  # noqa: E402

PAGINAS = [
    "app.py",
    "pages/1_Documentação.py",
    "pages/2_Indicadores.py",
    "pages/3_Treinamento.py",
    "pages/4_Evolução.py",
    "pages/5_Plano_de_ação.py",
    "pages/Monitoria.py",
]
BASE = Path(__file__).resolve().parent.parent


def test_paginas_rodam():
    for pagina in PAGINAS:
        at = AppTest.from_file(str(BASE / pagina), default_timeout=30)
        at.run()
        assert not at.exception, f"{pagina} -> {at.exception}"
