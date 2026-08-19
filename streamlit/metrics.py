# -*- coding: utf-8 -*-
"""Cálculos usados nas páginas: scores, faixas, evolução e plano de ação."""

from typing import Optional

import pandas as pd

FATOS = ("Documentação", "Indicadores", "Treinamento", "Qualidade")

SUB_DOC = ["Sub Existência", "Sub Atualização", "Sub Padrão", "Sub Conformidade"]
SUB_IND = SUB_DOC
SUB_TRE = ["Sub Coerência", "Sub Aplicação", "Sub Atualização", "Sub Conformidade"]
SUB_QUA = ["Sub Existência", "Sub Abrangência", "Sub Conformidade"]


def score_frente(df: pd.DataFrame) -> Optional[float]:
    if df.empty:
        return None
    s = df["ScoreLinha"].mean()
    return None if pd.isna(s) else round(float(s), 2)


def score_final(
    doc: pd.DataFrame,
    ind: pd.DataFrame,
    tre: pd.DataFrame,
    qua: pd.DataFrame,
) -> Optional[float]:
    scores = [
        s
        for s in (score_frente(doc), score_frente(ind), score_frente(tre), score_frente(qua))
        if s is not None
    ]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 2)


def faixa_maturidade(score: Optional[float]) -> Optional[str]:
    if score is None:
        return None
    if score <= 25:
        return "Baixíssima maturidade"
    if score <= 35:
        return "Baixa maturidade"
    if score <= 75:
        return "Maturidade intermediária"
    if score <= 85:
        return "Boa maturidade"
    if score >= 0:
        return "Excelente maturidade"
    return None


def _conta(df: pd.DataFrame, col: str, valor: float) -> int:
    if df.empty or col not in df.columns:
        return 0
    return int((df[col] == valor).sum())


def metricas_frente(df: pd.DataFrame, subs: list[str]) -> dict:
    total = len(df)
    m = {
        "Total": total,
        "Score": score_frente(df),
        "Itens Negativos": int((df["ScoreLinha"] < 0).sum()) if total else 0,
    }
    for s in subs:
        nome = s.replace("Sub ", "Score ")
        v = df[s].mean()
        m[nome] = 0.0 if pd.isna(v) else round(float(v * 100), 2)
        m["% " + s] = round(_conta(df, s, 1.0) / total * 100, 2) if total else 0.0
    m["Conformes"] = _conta(df, "Sub Conformidade", 1.0)
    m["Não Conformes"] = _conta(df, "Sub Conformidade", 0.0)
    m["Graves"] = _conta(df, "Sub Conformidade", -1.0)
    m["% Graves"] = round(m["Graves"] / total * 100, 2) if total else 0.0
    return m


def metricas_documentacao(df: pd.DataFrame) -> dict:
    return metricas_frente(df, SUB_DOC)


def metricas_indicadores(df: pd.DataFrame) -> dict:
    return metricas_frente(df, SUB_IND)


def metricas_treinamento(df: pd.DataFrame) -> dict:
    return metricas_frente(df, SUB_TRE)


def metricas_geral(
    doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame, qua: pd.DataFrame
) -> dict:
    datas = pd.concat(
        [
            doc["Data da avaliação"],
            ind["Data da avaliação"],
            tre["Data da avaliação"],
            qua["Data da avaliação"],
        ]
    )
    ops = set(doc["Operação"]) | set(ind["Operação"]) | set(tre["Operação"]) | set(qua["Operação"])
    return {
        "Itens Avaliados Total": len(doc) + len(ind) + len(tre) + len(qua),
        "Operações Avaliadas": len(ops),
        "Data Última Avaliação": datas.max().date() if not datas.empty else None,
        "Data Primeira Avaliação": datas.min().date() if not datas.empty else None,
        "Graves Total": (
            _conta(doc, "Sub Conformidade", -1.0)
            + _conta(ind, "Sub Conformidade", -1.0)
            + _conta(tre, "Sub Conformidade", -1.0)
            + _conta(qua, "Sub Conformidade", -1.0)
        ),
        "Não Conformes Total": (
            _conta(doc, "Sub Conformidade", 0.0)
            + _conta(ind, "Sub Conformidade", 0.0)
            + _conta(tre, "Sub Conformidade", 0.0)
            + _conta(qua, "Sub Conformidade", 0.0)
        ),
        "Itens Negativos Total": (
            int((doc["ScoreLinha"] < 0).sum())
            + int((ind["ScoreLinha"] < 0).sum())
            + int((tre["ScoreLinha"] < 0).sum())
            + int((qua["ScoreLinha"] < 0).sum())
        ),
    }


def scores_por_operacao(
    doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame, qua: pd.DataFrame
) -> pd.DataFrame:
    ops = sorted(
        set(doc["Operação"])
        | set(ind["Operação"])
        | set(tre["Operação"])
        | set(qua["Operação"])
    )
    linhas = []
    for op in ops:
        linhas.append(
            {
                "Operação": op,
                "Documentação": score_frente(doc[doc["Operação"] == op]),
                "Indicadores": score_frente(ind[ind["Operação"] == op]),
                "Treinamento": score_frente(tre[tre["Operação"] == op]),
                "Qualidade": score_frente(qua[qua["Operação"] == op]),
                "Score Final": score_final(
                    doc[doc["Operação"] == op],
                    ind[ind["Operação"] == op],
                    tre[tre["Operação"] == op],
                    qua[qua["Operação"] == op],
                ),
            }
        )
    return pd.DataFrame(linhas)


def _datas_unica(fatos: list[pd.DataFrame]) -> list:
    return sorted(
        {
            d
            for df in fatos
            for d in pd.to_datetime(df["Data da avaliação"].dropna()).dt.date.unique()
        }
    )


def _score_em(d: object, fatos: list[pd.DataFrame]) -> Optional[float]:
    """Score final considerando apenas linhas cuja data é igual a `d`."""
    scores = []
    for df in fatos:
        g = df[pd.to_datetime(df["Data da avaliação"]).dt.date == d]
        if not g.empty:
            s = g["ScoreLinha"].mean()
            if not pd.isna(s):
                scores.append(float(s))
    if not scores:
        return None
    return round(sum(scores) / len(scores), 2)


def evolucao(
    doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame, qua: pd.DataFrame
) -> pd.DataFrame:
    fatos = [doc, ind, tre, qua]
    linhas = []
    ops = sorted({o for df in fatos for o in df["Operação"].dropna().unique()})
    for op in ops:
        por_frente = [df[df["Operação"] == op] for df in fatos]
        datas = _datas_unica(por_frente)
        if not datas:
            continue
        ult = datas[-1]
        prev = datas[-2] if len(datas) >= 2 else None
        s_ult = _score_em(ult, por_frente)
        s_prev = _score_em(prev, por_frente) if prev else None
        var = (s_ult - s_prev) if (s_ult is not None and s_prev is not None) else None
        linhas.append(
            {
                "Operação": op,
                "Data Primeira Avaliação": datas[0],
                "Data Última Avaliação": ult,
                "Score Final Último Ciclo": s_ult,
                "Score Final Ciclo Anterior": s_prev,
                "Variação": var,
                "Evolução": (
                    None
                    if var is None
                    else ("▲ Melhorou" if var > 0 else ("▼ Piorou" if var < 0 else "➖ Estável"))
                ),
                "Faixa": faixa_maturidade(s_ult),
            }
        )
    return pd.DataFrame(linhas)


def ultimo_ciclo_global(
    doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame, qua: pd.DataFrame
) -> Optional[float]:
    """Score final do ciclo mais recente (ignora filtro de data)."""
    fatos = [doc, ind, tre, qua]
    datas = _datas_unica(fatos)
    if not datas:
        return 0.0
    return _score_em(datas[-1], fatos)


def serie_evolucao(
    doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame, qua: pd.DataFrame
) -> pd.DataFrame:
    """Score final por data de avaliação (linha do tempo)."""
    fatos = [doc, ind, tre, qua]
    ops = sorted({o for df in fatos for o in df["Operação"].dropna().unique()})
    linhas = []
    for op in ops:
        por_frente = [df[df["Operação"] == op] for df in fatos]
        for d in _datas_unica(por_frente):
            linhas.append(
                {
                    "Operação": op,
                    "Data": pd.Timestamp(d),
                    "Score Final": _score_em(d, por_frente),
                }
            )
    return pd.DataFrame(linhas)


def metricas_plano(pa: pd.DataFrame) -> dict:
    hoje = pd.Timestamp.today().normalize()
    total = len(pa)

    def conta(cond: pd.Series) -> int:
        return int(cond.fillna(False).sum())

    abertas = conta(pa["Status da Ação"] == "Aberto")
    em_andamento = conta(pa["Status da Ação"] == "Em andamento")
    concluidas = conta(pa["Status da Ação"] == "Concluído")
    com_prazo = pa["Prazo"].notna()
    vencidas = conta(com_prazo & (pa["Prazo"] < hoje) & (pa["Status da Ação"] != "Concluído"))
    a_vencer = conta(
        com_prazo
        & (pa["Prazo"] >= hoje)
        & (pa["Prazo"] <= hoje + pd.Timedelta(days=30))
        & (pa["Status da Ação"] != "Concluído")
    )
    return {
        "Total": total,
        "Abertas": abertas,
        "Em Andamento": em_andamento,
        "Concluídas": concluidas,
        "Vencidas": vencidas,
        "A Vencer (30 dias)": a_vencer,
        "% Concluídas": round(concluidas / total * 100, 2) if total else 0.0,
    }


