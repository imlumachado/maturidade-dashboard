# -*- coding: utf-8 -*-
"""Validação dos filtros de Operação e Data nas páginas (Fase 5, item 4)."""
import sys
from pathlib import Path

import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "streamlit"))

from streamlit.testing.v1 import AppTest  # noqa: E402

BASE = Path(__file__).resolve().parent.parent / "streamlit"


def test_filtro_operacao_limita_dados():
    at = AppTest.from_file(str(BASE / "Geral.py"), default_timeout=30)
    at.run()
    assert not at.exception

    # descobrir ops disponíveis
    d = at.session_state.dados
    ops = sorted({o for df in d.values() if not df.empty for o in df["Operação"].dropna().unique()})
    assert len(ops) >= 2

    selecionar = [ops[0]]
    at.multiselect[0].set_value(selecionar).run()
    assert not at.exception

    filt = at.session_state.filt
    for chave, df in filt.items():
        if not df.empty:
            assert set(df["Operação"].unique()) <= set(selecionar), chave
    # plano de ação também filtrado por operação
    plano = at.session_state.plano
    if not plano.empty:
        assert set(plano["Operação"].unique()) <= set(selecionar)


def test_filtro_data_limita_periodo():
    at = AppTest.from_file(str(BASE / "Geral.py"), default_timeout=30)
    at.run()
    assert not at.exception

    d = at.session_state.dados
    datas = []
    for chave, df in d.items():
        if chave == "PlanoAcao" or df.empty:
            continue
        datas.extend(pd.to_datetime(df["Data da avaliação"]).dt.date)
    datas = sorted(set(datas))
    assert len(datas) >= 2

    inicio = datas[0]
    at.date_input[0].set_value((inicio, inicio)).run()
    assert not at.exception

    filt = at.session_state.filt
    for chave, df in filt.items():
        if not df.empty:
            dt = pd.to_datetime(df["Data da avaliação"]).dt.date
            assert (dt >= inicio).all() and (dt <= inicio).all(), chave


def test_paginas_rodam_com_filtro_operacao():
    ops = None
    for pagina in ("pages/1_Documentação.py", "pages/2_Indicadores.py", "pages/3_Treinamento.py",
                   "pages/4_Evolução.py", "pages/5_Plano_de_ação.py", "pages/6_Qualidade.py"):
        at = AppTest.from_file(str(BASE / pagina), default_timeout=30)
        at.run()
        assert not at.exception, pagina
        if ops is None:
            d = at.session_state.dados
            ops = sorted({o for df in d.values() if not df.empty for o in df["Operação"].dropna().unique()})
        selecionar = [ops[0]] if ops else []
        at.multiselect[0].set_value(selecionar).run()
        assert not at.exception, f"{pagina} com filtro"


if __name__ == "__main__":
    test_filtro_operacao_limita_dados()
    test_filtro_data_limita_periodo()
    test_paginas_rodam_com_filtro_operacao()
    print("OK")