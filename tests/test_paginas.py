# -*- coding: utf-8 -*-
"""Smoke test das páginas Streamlit usando AppTest."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "streamlit"))

from streamlit.testing.v1 import AppTest  # noqa: E402

PAGINAS = [
    "Geral.py",
    "pages/1_Documentação.py",
    "pages/2_Indicadores.py",
    "pages/3_Treinamento.py",
    "pages/4_Evolução.py",
    "pages/5_Plano_de_ação.py",
    "pages/6_Qualidade.py",
]
BASE = Path(__file__).resolve().parent.parent / "streamlit"


def test_paginas_rodam():
    for pagina in PAGINAS:
        at = AppTest.from_file(str(BASE / pagina), default_timeout=30)
        at.run()
        assert not at.exception, f"{pagina} -> {at.exception}"
