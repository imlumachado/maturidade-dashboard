#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrair e estruturar dados da Mobilize para formulário limpo."""

import json
import pandas as pd
from datetime import datetime

# Carregar dados do DOCX extraído
docx_path = r"C:\Users\User\maturidade-dashboard\mobilize_content.json"

with open(docx_path, "r", encoding="utf-8") as f:
    docx_data = json.load(f)

print("=== EXTRAÇÃO DE DADOS DA MOBILIZE ===\n")

# Informações gerais
data_avaliacao = "18/09/2026"
operacao = "Mobilize"

# Extrair não conformidades
tables = docx_data["tables"]
nao_conformidades = tables[4]["data"]  # Tabela 5: Não conformidades

print("Não conformidades encontradas:")
for nc in nao_conformidades[1:]:  # Pular cabeçalho
    print(f"  {nc[0]}: {nc[3]}")

# Extrair informações de treinamento
treinamento_info = tables[3]["data"]  # Tabela 4: Avaliação por área
print("\nInformações de treinamento:")
for item in treinamento_info[1:]:  # Pular cabeçalho
    if item[0] == "Treinamento":
        print(f"  {item[3]}")

# Extrair informações de qualidade/monitorias
print("\nInformações de monitorias:")
print("  - Portal da Qualidade: Amostral, Conformidade")
print("  - Cessão de Direitos: Amostral, Conformidade (nota 100)")
print("  - Clube FIQ: Não realizada, Não Conformidade Grave")

# Extrair indicadores mencionados
print("\nIndicadores mencionados:")
indicadores = ["NS", "PCA", "TMA", "TME", "CSAT", "FCR", "SLA", "HC", "ABS", "TO"]
for ind in indicadores:
    print(f"  - {ind}")

print("\n=== EXTRAÇÃO CONCLUÍDA ===")