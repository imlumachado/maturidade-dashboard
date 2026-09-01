# -*- coding: utf-8 -*-

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


def cor_score_gradiente(score, de="#DC2626", meio="#F59E0B", ate="#059669"):
    """Interpola a cor do score num gradiente vermelho -> amarelo -> verde (0-100)."""
    if score is None:
        return "#94A3B8"
    try:
        score = float(score)
    except (TypeError, ValueError):
        return "#94A3B8"
    score = max(0.0, min(100.0, score))

    def _hex2rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

    def _rgb2hex(c):
        return "#{:02X}{:02X}{:02X}".format(*[round(v) for v in c])

    a, b = (_hex2rgb(de), _hex2rgb(meio)) if score <= 50 else (_hex2rgb(meio), _hex2rgb(ate))
    t = score / 50.0 if score <= 50 else (score - 50.0) / 50.0
    return _rgb2hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


def fmt_num(v, casas=2):
    if v is None:
        return None
    try:
        v = float(v)
    except (TypeError, ValueError):
        return str(v)
    texto = f"{v:.{casas}f}".rstrip("0").rstrip(".")
    return texto