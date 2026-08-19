# -*- coding: utf-8 -*-
"""Identidade visual — verde sóbrio sobre base da marca dbm.

Paleta da marca: verde profundo #065F46, acento #059669, fundo claro
#F8FAFC, textos grafite #0F172A. Estilo corporativo/analítico, minimalista,
sem serifas, cards limpos com acento verde.
"""

# Cores da marca
VERDE = "#059669"            # verde (acento principal)
VERDE_ESCURO = "#065F46"     # verde profundo (header, títulos)
VERDE_CLARO = "#ECFDF5"      # fundo de destaque / hover
PRETO = "#0F172A"            # textos principais (grafite)
CINZA_ESCURO = "#065F46"     # superfícies escuras (header) — verde profundo
FUNDO = "#F8FAFC"            # fundo geral (branco-azulado)
BRANCO = "#FFFFFF"
TEXTO = "#1E293B"
TEXTO_MUTE = "#64748B"
BORDA = "#E2E8F0"

# Cores das faixas de maturidade (verdes sóbrios, vermelho/âmbar para alerta)
CORES_FAIXA = {
    "Baixíssima maturidade": "#DC2626",
    "Baixa maturidade": "#F59E0B",
    "Maturidade intermediária": "#EAB308",
    "Boa maturidade": "#10B981",
    "Excelente maturidade": "#065F46",
}

# Status do plano de ação
CORES_STATUS = {
    "Aberto": "#DC2626",
    "Em andamento": "#F59E0B",
    "Concluído": "#059669",
}

# Frentes avaliadas (verdes em escala)
CORES_FRENTES = {
    "Documentação": "#065F46",
    "Indicadores": "#059669",
    "Treinamento": "#10B981",
    "Qualidade": "#1E293B",
}


def cor_faixa(faixa):
    return CORES_FAIXA.get(faixa, "#94A3B8")


def cor_status(status):
    return CORES_STATUS.get(status, "#94A3B8")


def cor_score(score):
    if score is None:
        return "#94A3B8"
    if score <= 35:
        return "#DC2626"
    if score <= 75:
        return "#F59E0B"
    return "#059669"