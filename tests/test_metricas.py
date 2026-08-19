# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "streamlit"))

from data_loader import (  # noqa: E402
    _mtime,
    _score_linha,
    carregar_dados,
    fn_atualizacao,
    fn_conformidade,
    fn_sim_nao,
)
from metrics import (  # noqa: E402
    evolucao,
    faixa_maturidade,
    metricas_geral,
    metricas_plano,
    score_final,
    score_frente,
    scores_por_operacao,
    serie_evolucao,
    ultimo_ciclo_global,
)
from theme import cor_score_gradiente  # noqa: E402

FORMULARIO = Path(__file__).resolve().parent.parent / "formulario"


# ---------------------------------------------------------------------------
# Funções de conversão
# ---------------------------------------------------------------------------
def test_fn_sim_nao():
    assert fn_sim_nao("SIM") == 1
    assert fn_sim_nao("Não") == 0
    assert fn_sim_nao("  sim ") == 1
    assert fn_sim_nao("x") is None
    assert fn_sim_nao(None) is None


def test_fn_conformidade():
    assert fn_conformidade("Conformidade") == 1
    assert fn_conformidade("Conformidade Pontual") == 0
    assert fn_conformidade("Não Conformidade") == 0
    assert fn_conformidade("NÃO CONFORMIDADE GRAVE") == -1
    assert fn_conformidade("nada") is None


def test_fn_atualizacao():
    assert fn_atualizacao("Automático") == 1
    assert fn_atualizacao("Manual") == 0.5
    assert fn_atualizacao("Não atualizado") == 0
    assert fn_atualizacao("?") is None


# ---------------------------------------------------------------------------
# ScoreLinha
# ---------------------------------------------------------------------------
def test_score_linha_exemplo_do_guia():
    assert _score_linha([1, 1, 1, -1]) == 50


def test_score_linha_todos_1():
    assert _score_linha([1, 1, 1, 1]) == 100


def test_score_linha_sem_resposta():
    assert _score_linha([None, None]) is None


def test_score_linha_arredondamento():
    assert _score_linha([1, 0, 1]) == 67  # 66.666 -> 67 (AwayFromZero)


# ---------------------------------------------------------------------------
# Faixa de maturidade
# ---------------------------------------------------------------------------
def test_faixas():
    assert faixa_maturidade(25) == "Baixíssima maturidade"
    assert faixa_maturidade(26) == "Baixa maturidade"
    assert faixa_maturidade(36) == "Maturidade intermediária"
    assert faixa_maturidade(76) == "Boa maturidade"
    assert faixa_maturidade(86) == "Excelente maturidade"
    assert faixa_maturidade(None) is None


# ---------------------------------------------------------------------------
# Gradiente de scores
# ---------------------------------------------------------------------------
def test_cor_score_gradiente_extremos():
    assert cor_score_gradiente(0) == "#DC2626"
    assert cor_score_gradiente(100) == "#059669"


def test_cor_score_gradiente_meio():
    assert cor_score_gradiente(50) == "#F59E0B"


def test_cor_score_gradiente_ordem():
    def _canal(h, idx):
        h = h.lstrip("#")
        return int(h[idx * 2 : idx * 2 + 2], 16)

    r_baixo, g_baixo = _canal(cor_score_gradiente(10), 0), _canal(cor_score_gradiente(10), 1)
    r_alto, g_alto = _canal(cor_score_gradiente(90), 0), _canal(cor_score_gradiente(90), 1)
    assert r_baixo > g_baixo  # score baixo -> vermelho predomina
    assert g_alto > r_alto  # score alto -> verde predomina


def test_cor_score_gradiente_none():
    assert cor_score_gradiente(None) == "#94A3B8"


# ---------------------------------------------------------------------------
# Dados sintéticos
# ---------------------------------------------------------------------------
_COLUNAS_FATO = [
    "Operação",
    "Processo avaliado",
    "Frente",
    "Nome_Documento",
    "Data da avaliação",
    "ScoreLinha",
    "Sub Existência",
    "Sub Atualização",
    "Sub Padrão",
    "Sub Conformidade",
    "Plano de Ação",
    "Responsável",
    "Prazo",
    "Status da Ação",
]


def _fato(operacoes, frente="Documentação"):
    linhas = []
    for i, (op, processo, data, respostas) in enumerate(operacoes, start=1):
        linhas.append(
            {
                "Operação": op,
                "Processo avaliado": processo,
                "Frente": frente,
                "Nome_Documento": f"Doc {i}",
                "Data da avaliação": pd.Timestamp(data),
                "ScoreLinha": _score_linha(respostas),
                "Sub Existência": respostas[0] if len(respostas) else None,
                "Sub Atualização": respostas[1] if len(respostas) > 1 else None,
                "Sub Padrão": respostas[2] if len(respostas) > 2 else None,
                "Sub Conformidade": respostas[3] if len(respostas) > 3 else None,
                "Plano de Ação": None,
                "Responsável": None,
                "Prazo": None,
                "Status da Ação": None,
            }
        )
    return pd.DataFrame(linhas, columns=_COLUNAS_FATO)


def _dados_sinteticos():
    doc = _fato(
        [
            ("A", "P1", "2026-08-01", [1, 1, 1, 1]),
            ("A", "P2", "2026-08-01", [1, 1, 1, -1]),
            ("B", "P1", "2026-08-01", [1, 1, 1, 1]),
            ("B", "P1", "2026-07-01", [0, 1, 1, 1]),
        ]
    )
    ind = _fato([("A", "P1", "2026-08-01", [1, 1, 1, 1])], frente="Indicadores")
    tre = _fato([], frente="Treinamento")
    qua = _fato([("A", "P1", "2026-08-01", [1, 1, 1, 1])], frente="Qualidade")
    return doc, ind, tre, qua


def test_score_frente():
    doc, ind, tre, qua = _dados_sinteticos()
    assert score_frente(doc) == pytest.approx(81.25)  # 100, 50, 100, 75 -> 325/4
    assert score_frente(tre) is None


def test_score_final():
    doc, ind, tre, qua = _dados_sinteticos()
    # Doc 81.25 + Ind 100 + Qualidade 100 -> média das frentes avaliadas = 93.75
    assert score_final(doc, ind, tre, qua) == pytest.approx(93.75)


def test_scores_por_operacao():
    doc, ind, tre, qua = _dados_sinteticos()
    df = scores_por_operacao(doc, ind, tre, qua)
    a = df[df["Operação"] == "A"].iloc[0]
    assert a["Documentação"] == pytest.approx(75)  # 100, 50
    assert a["Qualidade"] == pytest.approx(100)
    b = df[df["Operação"] == "B"].iloc[0]
    assert b["Documentação"] == pytest.approx(87.5)  # 100, 75


def test_evolucao():
    doc, ind, tre, qua = _dados_sinteticos()
    df = evolucao(doc, ind, tre, qua)
    b = df[df["Operação"] == "B"].iloc[0]
    assert b["Score Final Último Ciclo"] == pytest.approx(100)
    assert b["Score Final Ciclo Anterior"] == pytest.approx(75)
    assert b["Variação"] == pytest.approx(25)
    assert b["Evolução"] == "▲ Melhorou"


def test_serie_evolucao():
    doc, ind, tre, qua = _dados_sinteticos()
    df = serie_evolucao(doc, ind, tre, qua)
    assert {"2026-07-01", "2026-08-01"} <= set(df["Data"].dt.strftime("%Y-%m-%d"))


def test_ultimo_ciclo_global():
    doc, ind, tre, qua = _dados_sinteticos()
    # ciclo 08/2026: Doc 83.33, Ind 100, Qualidade 100 -> 94.44
    assert ultimo_ciclo_global(doc, ind, tre, qua) == pytest.approx(94.4444, abs=0.01)


def test_metricas_geral():
    doc, ind, tre, qua = _dados_sinteticos()
    m = metricas_geral(doc, ind, tre, qua)
    assert m["Itens Avaliados Total"] == 6
    assert m["Operações Avaliadas"] == 2


def test_metricas_plano():
    pa = pd.DataFrame(
        [
            {"Prazo": pd.Timestamp("2020-01-01"), "Status da Ação": "Aberto"},
            {"Prazo": pd.Timestamp("2026-12-31"), "Status da Ação": "Aberto"},
            {"Prazo": pd.Timestamp("2030-01-01"), "Status da Ação": "Concluído"},
            {"Prazo": None, "Status da Ação": "Em andamento"},
        ]
    )
    m = metricas_plano(pa)
    assert m["Total"] == 4
    assert m["Abertas"] == 2
    assert m["Em Andamento"] == 1
    assert m["Concluídas"] == 1
    assert m["Vencidas"] == 1
    assert m["% Concluídas"] == pytest.approx(25)


# ---------------------------------------------------------------------------
# Carregamento do formulário real (se existir)
# ---------------------------------------------------------------------------
@pytest.mark.skipif(not (FORMULARIO / "F_O_025_Formulario_Maturidade_Planos.xlsx").exists(), reason="formulário ausente")
def test_carregar_dados_real():
    d = carregar_dados(_mtime())
    assert set(d) == {"Documentacao", "Indicadores", "Treinamento", "Qualidade", "PlanoAcao"}
    assert not d["Documentacao"].empty
    assert not (d["Documentacao"]["Operação"] == "Exemplo (apagar)").any()
    assert d["Documentacao"]["ScoreLinha"].between(-100, 100).all()