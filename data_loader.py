# -*- coding: utf-8 -*-

from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache
from pathlib import Path

import pandas as pd

FORMULARIO = (
    Path(__file__).resolve().parent
    / "formulario"
    / "F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"
)

COLUNAS_PLANO = [
    "Operação",
    "Processo avaliado",
    "Frente",
    "Item",
    "Plano de Ação",
    "Responsável",
    "Prazo",
    "Status da Ação",
]

_COLS_BASE = [
    "Operação",
    "Processo avaliado",
    "Data da avaliação",
    "Observação",
    "Plano de Ação",
    "Responsável",
    "Prazo",
    "Status da Ação",
]

def _texto(v):
    if v is None or pd.isna(v):
        return None
    return str(v).strip()


def fn_sim_nao(v):
    t = _texto(v)
    if t is None:
        return None
    t = t.upper()
    if t == "SIM":
        return 1.0
    if t == "NÃO":
        return 0.0
    return None


def fn_conformidade(v):
    t = _texto(v)
    if t is None:
        return None
    t = t.upper()
    if t == "CONFORMIDADE":
        return 1.0
    if t in ("CONFORMIDADE PONTUAL", "NÃO CONFORMIDADE"):
        return 0.0
    if t == "NÃO CONFORMIDADE GRAVE":
        return -1.0
    return None


def fn_atualizacao(v):
    t = _texto(v)
    if t is None:
        return None
    t = t.upper()
    if t == "AUTOMÁTICO":
        return 1.0
    if t == "MANUAL":
        return 0.5
    if t == "NÃO ATUALIZADO":
        return 0.0
    return None


def fn_numerico(v):
    """Aba Qualidade já traz valores numéricos (1 / 0.5 / 0 / -1)."""
    if v is None or pd.isna(v):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _arredondar(v):
    return int(Decimal(str(v)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _score_linha(subs):
    vals = [s for s in subs if s is not None and not pd.isna(s)]
    if not vals:
        return None
    return _arredondar(sum(vals) / len(vals) * 100)


_CONFIG = {
    "Avaliação": {
        "frente": "Documentação",
        "col_item": "Nome_Documento",
        "subs": [
            ("Sub Existência", "Existe?", fn_sim_nao),
            ("Sub Atualização", "Está atualizado?", fn_sim_nao),
            ("Sub Padrão", "Padronizado?", fn_sim_nao),
            ("Sub Conformidade", "Coforme?", fn_conformidade),
        ],
    },
    "Indicadores": {
        "frente": "Indicadores",
        "col_item": "Nome_Indicador",
        "subs": [
            ("Sub Existência", "Existe indicador?", fn_sim_nao),
            ("Sub Atualização", "Como é atualizado?", fn_atualizacao),
            ("Sub Padrão", "No padrão?", fn_sim_nao),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
        ],
    },
    "Treinamento": {
        "frente": "Treinamento",
        "col_item": "Nome_Treinamento",
        "subs": [
            ("Sub Coerência", "Treinamento está coerente aos documentos?", fn_sim_nao),
            ("Sub Aplicação", "Treinamento foi aplicado?", fn_sim_nao),
            ("Sub Atualização", "Houve atualização?", fn_sim_nao),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
        ],
    },
    "Qualidade": {
        "frente": "Qualidade",
        "col_item": "Processo avaliado",
        "subs": [
            ("Sub Existência", "Existência", fn_numerico),
            ("Sub Abrangência", "Abrangência", fn_numerico),
            ("Sub Conformidade", "Conformidade", fn_numerico),
        ],
    },
}


def _fato(aba: str, cfg: dict) -> pd.DataFrame:
    df = pd.read_excel(FORMULARIO, sheet_name=aba)
    df = df[df["Data da avaliação"].notna()].copy()
    df["Operação"] = df["Operação"].astype(str).str.strip()
    df["Processo avaliado"] = df["Processo avaliado"].astype(str).str.strip()
    df = df[df["Operação"].ne("") & df["Operação"].ne("Exemplo (apagar)")]
    df["Frente"] = cfg["frente"]

    for nome, col, fn in cfg["subs"]:
        df[nome] = df[col].map(fn)

    subs = [nome for nome, _, _ in cfg["subs"]]
    df["ScoreLinha"] = df[subs].apply(lambda r: _score_linha(r.tolist()), axis=1)

    cols = ["Frente", cfg["col_item"], "ScoreLinha"] + subs + _COLS_BASE
    cols = list(dict.fromkeys(c for c in cols if c in df.columns))
    df = df[cols]
    if "Coforme?" in df.columns:
        df = df.rename(columns={"Coforme?": "Conforme?"})
    return df.reset_index(drop=True)


def _plano_acao(doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame) -> pd.DataFrame:
    def preparar(df, col_item):
        d = df[
            [
                "Operação",
                "Processo avaliado",
                "Frente",
                col_item,
                "Plano de Ação",
                "Responsável",
                "Prazo",
                "Status da Ação",
            ]
        ].copy()
        return d.rename(columns={col_item: "Item"})

    pa = pd.concat(
        [preparar(doc, "Nome_Documento"), preparar(ind, "Nome_Indicador"), preparar(tre, "Nome_Treinamento")],
        ignore_index=True,
    )
    pa = pa[pa["Plano de Ação"].notna() & pa["Plano de Ação"].astype(str).str.strip().ne("")]
    pa["Prazo"] = pd.to_datetime(pa["Prazo"], errors="coerce")
    return pa[COLUNAS_PLANO].reset_index(drop=True)


def _mtime() -> float:
    return FORMULARIO.stat().st_mtime if FORMULARIO.exists() else 0.0


@lru_cache(maxsize=1)
def carregar_dados(mtime: float = 0.0) -> dict[str, pd.DataFrame]:
    del mtime
    doc = _fato("Avaliação", _CONFIG["Avaliação"])
    ind = _fato("Indicadores", _CONFIG["Indicadores"])
    tre = _fato("Treinamento", _CONFIG["Treinamento"])
    qua = _fato("Qualidade", _CONFIG["Qualidade"])
    return {
        "Documentacao": doc,
        "Indicadores": ind,
        "Treinamento": tre,
        "Qualidade": qua,
        "PlanoAcao": _plano_acao(doc, ind, tre),
    }
