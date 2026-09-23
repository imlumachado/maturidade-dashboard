#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analisar o novo formulário Excel da Mobilize."""

import pandas as pd
import json

# Caminhos
form_novo = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO Analise de Maturidade em Processos.xlsx"

def analisar_formulario():
    """Analisar todas as abas do novo formulário."""
    print("=== ANÁLISE DO NOVO FORMULÁRIO MOBILIZE ===\n")
    
    xls = pd.ExcelFile(form_novo)
    print(f"Total de abas: {len(xls.sheet_names)}")
    print(f"Abas: {xls.sheet_names}\n")
    
    dados_formulario = {}
    
    for sheet_name in xls.sheet_names:
        print(f"\n{'='*60}")
        print(f"ABA: {sheet_name}")
        print('='*60)
        
        df = pd.read_excel(form_novo, sheet_name=sheet_name, header=None)
        print(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # Mostrar cabeçalho (primeira linha)
        print("\nColunas (cabeçalho):")
        colunas = []
        for j in range(min(25, df.shape[1])):
            valor = df.iloc[0, j]
            if pd.notna(valor):
                colunas.append(str(valor))
                print(f"  Col {j}: {valor}")
        
        # Mostrar primeiras linhas de dados
        print("\nPrimeiras 5 linhas de dados:")
        dados_aba = []
        for i in range(1, min(6, df.shape[0])):
            linha = {}
            print(f"\n  Linha {i}:")
            for j in range(min(15, df.shape[1])):
                valor = df.iloc[i, j]
                if pd.notna(valor):
                    linha[df.iloc[0, j]] = valor
                    print(f"    {df.iloc[0, j]}: {valor}")
            dados_aba.append(linha)
        
        dados_formulario[sheet_name] = {
            "colunas": colunas,
            "total_linhas": df.shape[0] - 1,  # Descontar cabeçalho
            "dados_exemplo": dados_aba
        }
    
    return dados_formulario

if __name__ == "__main__":
    dados = analisar_formulario()
    
    # Salvar análise
    output_path = r"C:\Users\User\maturidade-dashboard\analise_novo_formulario.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n\nAnálise salva em: {output_path}")