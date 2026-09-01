# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import pandas as pd  # noqa: E402
from streamlit.testing.v1 import AppTest

BASE = Path(__file__).resolve().parent.parent


def _set_ops(at, selecionar: list[str], ops_todas: list[str]):
    """Seleciona apenas as operações desejadas usando checkboxes."""
    for op in ops_todas:
        key = f"op_{op}"
        if key in at.session_state:
            if op in selecionar:
                at.session_state[key] = True
            else:
                at.session_state[key] = False
        else:
            at.session_state[key] = op in selecionar
    at.session_state.ops_sel = set(selecionar)
    at.run()


def test_filtro_operacao_limita_dados():
    at = AppTest.from_file(str(BASE / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception

    d = at.session_state.dados
    ops = sorted({o for df in d.values() if not df.empty for o in df["Operação"].dropna().unique()})
    assert len(ops) >= 2

    selecionar = [ops[0]]
    _set_ops(at, selecionar, ops)
    assert not at.exception

    filt = at.session_state.filt
    for chave, df in filt.items():
        if not df.empty:
            assert set(df["Operação"].unique()) <= set(selecionar), chave
    plano = at.session_state.plano
    if not plano.empty:
        assert set(plano["Operação"].unique()) <= set(selecionar)


def test_filtro_data_limita_periodo():
    at = AppTest.from_file(str(BASE / "app.py"), default_timeout=30)
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
    ops_todas = None
    for pagina in ("pages/1_Documentação.py", "pages/2_Indicadores.py", "pages/3_Treinamento.py",
                   "pages/4_Evolução.py", "pages/5_Plano_de_ação.py", "pages/Monitoria.py"):
        at = AppTest.from_file(str(BASE / pagina), default_timeout=30)
        at.run()
        assert not at.exception, pagina
        if ops_todas is None:
            d = at.session_state.dados
            ops_todas = sorted({o for df in d.values() if not df.empty for o in df["Operação"].dropna().unique()})
        selecionar = [ops_todas[0]] if ops_todas else []
        _set_ops(at, selecionar, ops_todas)
        assert not at.exception, f"{pagina} com filtro"


if __name__ == "__main__":
    test_filtro_operacao_limita_dados()
    test_filtro_data_limita_periodo()
    test_paginas_rodam_com_filtro_operacao()
    print("OK")