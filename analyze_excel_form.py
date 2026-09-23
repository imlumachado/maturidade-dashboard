#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analisar a estrutura do formulário Excel existente."""

import pandas as pd
import json
import os

# Caminhos
form_path = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

def analyze_excel_structure(excel_path):
    """Analisar a estrutura de todas as abas do Excel."""
    print(f"Analisando: {excel_path}")
    
    # Ler todas as abas
    xls = pd.ExcelFile(excel_path)
    sheet_names = xls.sheet_names
    
    print(f"\nTotal de abas: {len(sheet_names)}")
    print(f"Abas encontradas: {sheet_names}")
    
    sheets_info = {}
    
    for sheet_name in sheet_names:
        print(f"\n=== ABA: {sheet_name} ===")
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
        
        print(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Mostrar primeiras linhas
        print("Primeiras 5 linhas:")
        for i in range(min(5, df.shape[0])):
            row_data = []
            for j in range(min(10, df.shape[1])):
                val = df.iloc[i, j]
                if pd.notna(val):
                    row_data.append(f"[{j}]={str(val)[:50]}")
            if row_data:
                print(f"  Linha {i}: {', '.join(row_data)}")
        
        # Salvar informações
        sheets_info[sheet_name] = {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "sample_data": df.head(10).values.tolist()
        }
    
    return sheets_info

if __name__ == "__main__":
    info = analyze_excel_structure(form_path)
    
    # Salvar análise
    output_path = r"C:\Users\User\maturidade-dashboard\excel_structure.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\nAnálise salva em: {output_path}")