# -*- coding: utf-8 -*-

from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache
from pathlib import Path

import pandas as pd

FORMULARIO = (
    Path(__file__).resolve().parent
    / "formulario"
    / "F.O.091.GOCO Analise de Maturidade em Processos.xlsx"
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
    if t in ("CONFORMIDADE PONTUAL", "OBSERVAÇÃO"):
        return 0.5
    if t in ("NÃO CONFORMIDADE", "NÃO CONFORMIDADE GRAVE"):
        return 0.0
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
    """Aba Qualidade já traz valores numéricos. Converte e normaliza para [0, 1]."""
    if v is None or pd.isna(v):
        return None
    try:
        val = float(v)
        if val < 0:
            return 0.0
        return val
    except (TypeError, ValueError):
        return None


def _fn_na(v):
    """Critério N/A — inaplicabilidade registrada e validada."""
    return None


def _arredondar(v):
    return int(Decimal(str(v)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _score_linha(subs):
    vals = [s for s in subs if s is not None and not pd.isna(s)]
    if not vals:
        return None
    return _arredondar(sum(vals) / len(vals) * 100)


_SIM_NAO = lambda v: (1 if str(v).strip().upper() == "SIM" else (0 if str(v).strip().upper() in ("NÃO",) else None)) if v is not None else None
_CONF_EXCEL = lambda v: (1 if str(v).strip() == "Conformidade" else (-1 if "grave" in str(v).lower() else (0 if "onformidade" in str(v).lower() else None))) if v is not None else None

_CONFIG = {
    "Documentos": {
        "frente": "Documentação",
        "col_item": "Frente avaliada",
        "col_processo": "Frente avaliada",
        "excel_raw": {
            "Existe?": _CONF_EXCEL,
            "Aplicação?": _CONF_EXCEL,
            "Está atualizado?": _CONF_EXCEL,
            "Padronizado?": _CONF_EXCEL,
            "Conforme?": _CONF_EXCEL,
        },
        "subs": [
            ("Sub Existência", "Existe?", fn_conformidade),
            ("Sub Aplicação", "Aplicação?", fn_conformidade),
            ("Sub Atualização", "Está atualizado?", fn_conformidade),
            ("Sub Padrão", "Padronizado?", fn_conformidade),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
        ],
    },
    "Indicadores": {
        "frente": "Indicadores",
        "col_item": "Frente avaliada",
        "col_processo": "Frente avaliada",
        "excel_raw": {
            "Existe indicador?": _CONF_EXCEL,
            "Aplicação": _CONF_EXCEL,
            "No padrão?": _CONF_EXCEL,
            "Conforme?": _CONF_EXCEL,
            "Atualização": _CONF_EXCEL,
        },
        "subs": [
            ("Sub Existência", "Existe indicador?", fn_conformidade),
            ("Sub Aplicação", "Aplicação", fn_conformidade),
            ("Sub Padrão", "No padrão?", fn_conformidade),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
            ("Sub Atualização", "Atualização", fn_conformidade),
        ],
    },
    "Treinamento": {
        "frente": "Treinamento",
        "col_item": "Item avaliado",
        "col_processo": "Frente avaliada",
        "excel_raw": {
            "Existe?": _CONF_EXCEL,
            "Está atualizado?": _CONF_EXCEL,
            "Padronizado?": _CONF_EXCEL,
            "Conforme?": _CONF_EXCEL,
        },
        "subs": [
            ("Sub Existência", "Existe?", fn_conformidade),
            ("Sub Aplicação", None, _fn_na),
            ("Sub Padrão", "Padronizado?", fn_conformidade),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
            ("Sub Atualização", "Está atualizado?", fn_conformidade),
        ],
    },
    "Qualidade": {
        "frente": "Qualidade",
        "col_item": "Frente avaliada",
        "col_processo": "Frente avaliada",
        "excel_raw": {
            "Existe?": _CONF_EXCEL,
            "Aplicação": _CONF_EXCEL,
            "Está atualizado?": _CONF_EXCEL,
            "Padronizado?": _CONF_EXCEL,
            "Conforme?": _CONF_EXCEL,
        },
        "subs": [
            ("Sub Existência", "Existe?", fn_conformidade),
            ("Sub Aplicação", "Aplicação", fn_conformidade),
            ("Sub Atualização", "Está atualizado?", fn_conformidade),
            ("Sub Padrão", "Padronizado?", fn_conformidade),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
        ],
    },
}


def _fato(aba: str, cfg: dict) -> pd.DataFrame:
    df = pd.read_excel(FORMULARIO, sheet_name=aba)
    df = df[df["Data da avaliação"].notna()].copy()
    df["Operação"] = df["Operação"].astype(str).str.strip()
    col_proc = cfg.get("col_processo", "Processo avaliado")
    if col_proc in df.columns:
        df[col_proc] = df[col_proc].astype(str).str.strip()
        if col_proc != "Processo avaliado":
            df["Processo avaliado"] = df[col_proc]
    df = df[df["Operação"].ne("") & df["Operação"].ne("Exemplo (apagar)")]
    df["Frente"] = cfg["frente"]

    # Compute sub-scores for display
    for nome, col, fn in cfg["subs"]:
        if col is None:
            df[nome] = None
        else:
            df[nome] = df[col].map(fn)

    subs = [nome for nome, _, _ in cfg["subs"]]
    df["ScoreLinha"] = df[subs].apply(lambda r: _score_linha(r.tolist()), axis=1)

    # Compute Geral replicating Excel formulas exactly
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(FORMULARIO))
        ws = wb[aba]
        excel_raw = cfg.get("excel_raw", {})
        geral_col = score_col = None
        for c in range(1, ws.max_column + 1):
            h = ws.cell(row=1, column=c).value
            if h and h.strip() == "Geral":
                geral_col = c
            if h and h.strip() in ("Documentação", "Score Indicadores", "Score Treinamento", "Score"):
                score_col = c

        # Get raw column indices
        raw_cols = {}
        for c in range(1, ws.max_column + 1):
            h = ws.cell(row=1, column=c).value
            if h:
                raw_cols[h.strip()] = c

        def excel_sim_nao(val):
            if val is None:
                return None
            t = str(val).strip().upper()
            if t == "SIM":
                return 1
            if t in ("NÃO", "NÃO"):
                return 0
            return None

        def excel_conformidade(val):
            if val is None:
                return None
            t = str(val).strip()
            if t == "Conformidade":
                return 1
            if "Não conformidade grave" in t:
                return -1
            if "onformidade" in t:
                return 0
            return None

        n_rows = len(df)
        score_vals = []
        for row in range(2, n_rows + 2):
            sub_vals = []
            for raw_col_name, fn in excel_raw.items():
                col_idx = raw_cols.get(raw_col_name)
                if col_idx:
                    raw_val = ws.cell(row=row, column=col_idx).value
                    sub_vals.append(fn(raw_val))
                else:
                    sub_vals.append(None)
            valid = [v for v in sub_vals if v is not None]
            if valid:
                score = round(sum(valid) / len(valid) * 100, 0)
                score_vals.append(score)
            else:
                score_vals.append(None)
        wb.close()

        valid_scores = [s for s in score_vals if s is not None]
        geral_val = sum(valid_scores) / len(valid_scores) if valid_scores else None
        df["Geral"] = geral_val
    except Exception:
        df["Geral"] = df["ScoreLinha"].mean()

    cols = ["Frente", cfg["col_item"], "ScoreLinha", "Geral"] + subs + _COLS_BASE
    cols = list(dict.fromkeys(c for c in cols if c in df.columns))
    df = df[cols]
    return df.reset_index(drop=True)


def _plano_acao(doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame) -> pd.DataFrame:
    def preparar(df, col_item):
        col_proc = "Frente avaliada" if "Frente avaliada" in df.columns else "Processo avaliado"
        item_col = col_item if col_item in df.columns else col_proc
        cols = ["Operação", col_proc, "Frente", item_col, "Plano de Ação", "Responsável", "Prazo", "Status da Ação"]
        cols = list(dict.fromkeys(cols))
        d = df[cols].copy()
        rename = {item_col: "Item"}
        if col_proc in d.columns and col_proc != "Item":
            rename[col_proc] = "Processo avaliado"
        return d.rename(columns=rename)

    pa = pd.concat(
        [preparar(doc, "Frente avaliada"), preparar(ind, "Frente avaliada"), preparar(tre, "Frente avaliada")],
        ignore_index=True,
    )
    pa = pa[pa["Plano de Ação"].notna() & pa["Plano de Ação"].astype(str).str.strip().ne("")]
    pa["Prazo"] = pd.to_datetime(pa["Prazo"], errors="coerce")
    cols = [c for c in COLUNAS_PLANO if c in pa.columns]
    return pa[cols].reset_index(drop=True)


def _mtime() -> float:
    return FORMULARIO.stat().st_mtime if FORMULARIO.exists() else 0.0


@lru_cache(maxsize=1)
def carregar_dados(mtime: float = 0.0) -> dict[str, pd.DataFrame]:
    del mtime
    doc = _fato("Documentos", _CONFIG["Documentos"])
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
