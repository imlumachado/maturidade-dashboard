#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Limpar formulário mantendo apenas dados da operação Mobilize."""

import pandas as pd
from pathlib import Path
from openpyxl import load_workbook

# Caminhos
form_principal = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

print("=== LIMPEZA DO FORMULÁRIO - APENAS MOBILIZE ===\n")

# ============================================================
# 1. LER E FILTRAR DADOS
# ============================================================
print("1. Lendo e filtrando dados da Mobilize...")

# Ler todas as abas
xls = pd.ExcelFile(form_principal)
dados_filtrados = {}

for sheet_name in xls.sheet_names:
    if sheet_name in ['Avaliação', 'Indicadores', 'Treinamento', 'Qualidade']:
        df = pd.read_excel(form_principal, sheet_name=sheet_name)
        
        # Filtrar apenas operação Mobilize
        df_filtrado = df[df['Operação'] == 'Mobilize'].copy()
        
        dados_filtrados[sheet_name] = df_filtrado
        print(f"  -> {sheet_name}: {len(df)} registros -> {len(df_filtrado)} registros (Mobilize)")
    else:
        # Manter abas de referência inalteradas
        df = pd.read_excel(form_principal, sheet_name=sheet_name)
        dados_filtrados[sheet_name] = df
        print(f"  -> {sheet_name}: {len(df)} registros (mantido)")

# ============================================================
# 2. SALVAR FORMULÁRIO LIMPO
# ============================================================
print("\n2. Salvando formulário limpo...")

# Criar backup
import shutil
backup_path = form_principal + ".backup2"
shutil.copy2(form_principal, backup_path)
print(f"  -> Backup criado: {backup_path}")

# Salvar dados filtrados
with pd.ExcelWriter(form_principal, engine="openpyxl") as writer:
    for sheet_name, df in dados_filtrados.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"  -> Formulário salvo com apenas dados da Mobilize")

# ============================================================
# 3. VERIFICAR RESULTADO
# ============================================================
print("\n3. Verificando resultado...")

# Recarregar dados
xls = pd.ExcelFile(form_principal)
for sheet_name in ['Avaliação', 'Indicadores', 'Treinamento', 'Qualidade']:
    df = pd.read_excel(form_principal, sheet_name=sheet_name)
    operacoes = df['Operação'].unique() if 'Operação' in df.columns else []
    print(f"  -> {sheet_name}: {len(df)} registros | Operações: {operacoes}")

print("\n=== LIMPEZA CONCLUÍDA ===")