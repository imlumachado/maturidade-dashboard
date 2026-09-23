#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analisar estrutura detalhada do formulário original."""

import pandas as pd
import json

# Caminhos
form_original = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

def analisar_aba(sheet_name):
    """Analisar detalhes de uma aba específica."""
    print(f"\n{'='*60}")
    print(f"ABA: {sheet_name}")
    print('='*60)
    
    df = pd.read_excel(form_original, sheet_name=sheet_name, header=None)
    print(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
    
    # Primeira linha (cabeçalho)
    print("\nColunas (cabeçalho - linha 0):")
    for j in range(min(25, df.shape[1])):
        valor = df.iloc[0, j]
        if pd.notna(valor):
            print(f"  Col {j}: {valor}")
    
    # Amostra de dados
    print("\nPrimeiras 3 linhas de dados:")
    for i in range(1, min(4, df.shape[0])):
        print(f"\n  Linha {i}:")
        for j in range(min(15, df.shape[1])):
            valor = df.iloc[i, j]
            if pd.notna(valor):
                print(f"    Col {j}: {valor}")
    
    return df

if __name__ == "__main__":
    # Analisar todas as abas
    xls = pd.ExcelFile(form_original)
    
    for sheet_name in xls.sheet_names:
        analisar_aba(sheet_name)
    
    print("\n" + "="*60)
    print("ANÁLISE CONCLUÍDA")
    print("="*60)