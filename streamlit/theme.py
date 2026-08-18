# -*- coding: utf-8 -*-
"""Identidade visual — inspirada no site da dbm (www.dbm.com.br).

Paleta da marca: verde #02DE81, preto, branco e cinza claro.
Estilo: minimalista, sem serifas, cards limpos com acento verde.
"""

# Cores da marca
VERDE = "#02DE81"          # verde dbm (primária)
VERDE_ESCURO = "#00C46E"   # hover / variação do verde
PRETO = "#111111"          # textos e header
CINZA_ESCURO = "#2B2B2B"   # superfícies escuras (header)
FUNDO = "#F5F5F5"          # fundo geral (cinza claro)
BRANCO = "#FFFFFF"
TEXTO = "#1A1A1A"
TEXTO_MUTE = "#6B7280"
BORDA = "#E5E7EB"

# Cores das faixas de maturidade
CORES_FAIXA = {
    "Baixíssima maturidade": "#E23C3C",
    "Baixa maturidade": "#F59E0B",
    "Maturidade intermediária": "#FACC15",
    "Boa maturidade": "#34D399",
    "Excelente maturidade": "#02DE81",
}

# Status do plano de ação
CORES_STATUS = {
    "Aberto": "#E23C3C",
    "Em andamento": "#F59E0B",
    "Concluído": "#02DE81",
}

# Frentes avaliadas
CORES_FRENTES = {
    "Documentação": "#02DE81",
    "Indicadores": "#00C46E",
    "Treinamento": "#34D399",
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
