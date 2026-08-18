# -*- coding: utf-8 -*-
"""Identidade visual do dashboard."""

VERDE = "#02DE81"
PRETO = "#212121"
CINZA = "#F2F2F2"
BRANCO = "#FFFFFF"

CORES_FAIXA = {
    "Baixíssima maturidade": "#E23C3C",
    "Baixa maturidade": "#F59E0B",
    "Maturidade intermediária": "#FACC15",
    "Boa maturidade": "#34D399",
    "Excelente maturidade": "#02DE81",
}

CORES_STATUS = {
    "Aberto": "#E23C3C",
    "Em andamento": "#F59E0B",
    "Concluído": "#02DE81",
}

CORES_FRENTES = {
    "Documentação": "#02DE81",
    "Indicadores": "#34D399",
    "Treinamento": "#FACC15",
}


def cor_faixa(faixa):
    return CORES_FAIXA.get(faixa, "#9CA3AF")


def cor_status(status):
    return CORES_STATUS.get(status, "#9CA3AF")


def cor_score(score):
    if score is None:
        return "#9CA3AF"
    if score <= 35:
        return "#E23C3C"
    if score <= 75:
        return "#F59E0B"
    return "#02DE81"