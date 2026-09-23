#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Preencher dashboard com dados do formulário correto."""

import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font

# Caminhos
form_novo = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO Analise de Maturidade em Processos.xlsx"
output_path = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

print("=== PREENCHIMENTO DO DASHBOARD COM FORMULÁRIO CORRETO ===\n")

# ============================================================
# 1. LER E MAPEAR DADOS DE DOCUMENTOS
# ============================================================
print("1. Lendo e mapeando dados de Documentos...")

df_doc = pd.read_excel(form_novo, sheet_name="Documentos")
df_doc = df_doc[df_doc['Operação'] == 'Mobilize'].copy()

# Mapear colunas para estrutura do dashboard
colunas_doc = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Frente avaliada": "Processo avaliado",
    "Nome_Documento": "Nome_Documento",
    "Quantidade": "Quantidade",
    "Existe?": "Existe?",
    "Está atualizado?": "Está atualizado?",
    "Última atualização": "Última atualização",
    "Padronizado?": "Padronizado?",
    "Conforme?": "Coforme?",
    "Existência": "Existência",
    "Atualização": "Atualização",
    "Padrão": "Padrão",
    "Conformidade": "Conformidade",
    "Observação": "Observação",
    "Plano de Ação": "Plano de Ação",
    "Responsável": "Responsável",
    "Prazo": "Prazo",
    "Status da Ação": "Status da Ação"
}

df_doc_mapeado = df_doc.rename(columns=colunas_doc)

# Adicionar colunas faltantes
colunas_faltantes = ["Documentação", "Geral"]
for col in colunas_faltantes:
    if col not in df_doc_mapeado.columns:
        df_doc_mapeado[col] = 0

print(f"  -> Documentos: {len(df_doc_mapeado)} registros mapeados")

# ============================================================
# 2. LER E MAPEAR DADOS DE INDICADORES
# ============================================================
print("\n2. Lendo e mapeando dados de Indicadores...")

df_ind = pd.read_excel(form_novo, sheet_name="Indicadores")
df_ind = df_ind[df_ind['Operação'] == 'Mobilize'].copy()

# Mapear colunas
colunas_ind = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Frente avaliada": "Processo avaliado",
    "Nome_Indicador": "Nome_Indicador",
    "Quantidade": "Quantidade",
    "Existe indicador?": "Existe indicador?",
    "Como é atualizado?": "Como é atualizado?",
    "No padrão?": "No padrão?",
    "Conforme?": "Conforme?",
    "Existência": "Existência",
    "Atualização": "Atualização",
    "Padrão": "Padrão",
    "Conformidade": "Conformidade",
    "Observação": "Observação",
    "Plano de Ação": "Plano de Ação",
    "Responsável": "Responsável",
    "Prazo": "Prazo",
    "Status da Ação": "Status da Ação"
}

df_ind_mapeado = df_ind.rename(columns=colunas_ind)

# Adicionar colunas faltantes
colunas_faltantes = ["Score Indicadores", "Geral"]
for col in colunas_faltantes:
    if col not in df_ind_mapeado.columns:
        df_ind_mapeado[col] = 0

print(f"  -> Indicadores: {len(df_ind_mapeado)} registros mapeados")

# ============================================================
# 3. LER E MAPEAR DADOS DE TREINAMENTO
# ============================================================
print("\n3. Lendo e mapeando dados de Treinamento...")

df_tre = pd.read_excel(form_novo, sheet_name="Treinamento")
df_tre = df_tre[df_tre['Operação'] == 'Mobilize'].copy()

# Mapear colunas - verificar nomes das colunas primeiro
print(f"  Colunas originais: {list(df_tre.columns)}")

# O formulário pode ter colunas diferentes, vamos adaptar
colunas_tre = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Frente avaliada": "Processo avaliado",
    "Item avaliado": "Nome_Treinamento",
    "Quantidade": "Quantidade",
    "Existe?": "Treinamento está coerente aos documentos?",
    "Está atualizado?": "Treinamento foi aplicado?",
    "Última atualização": "Houve atualização?",
    "Padronizado?": "Conforme?",
    "Conforme?": "Conforme?"
}

df_tre_mapeado = df_tre.rename(columns=colunas_tre)

# Adicionar colunas faltantes
colunas_faltantes_tre = ["Coerência", "Aplicação", "Atualização", "Conformidade", "Score Treinamento", "Geral"]
for col in colunas_faltantes_tre:
    if col not in df_tre_mapeado.columns:
        df_tre_mapeado[col] = 0

print(f"  -> Treinamento: {len(df_tre_mapeado)} registros mapeados")

# ============================================================
# 4. LER E MAPEAR DADOS DE QUALIDADE
# ============================================================
print("\n4. Lendo e mapeando dados de Qualidade...")

df_qua = pd.read_excel(form_novo, sheet_name="Qualidade")
df_qua = df_qua[df_qua['Operação'] == 'Mobilize'].copy()

# Mapear colunas
colunas_qua = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Frente avaliada": "Processo avaliado",
    "Item avaliado": "Processo Monitorado",
    "Quantidade": "Quantidade",
    "Existe?": "Foram feitas monitorias de qualidade?",
    "Está atualizado?": "Como são feitas as monitorias?",
    "Última atualização": "Conforme?",
    "Padronizado?": "Conforme?"
}

df_qua_mapeado = df_qua.rename(columns=colunas_qua)

# Adicionar colunas faltantes
colunas_faltantes_qua = ["Existência", "Abrangência", "Conformidade", "Score Qualidade", "Geral"]
for col in colunas_faltantes_qua:
    if col not in df_qua_mapeado.columns:
        df_qua_mapeado[col] = 0

print(f"  -> Qualidade: {len(df_qua_mapeado)} registros mapeados")

# ============================================================
# 5. SALVAR NO FORMULÁRIO PRINCIPAL
# ============================================================
print("\n5. Salvando dados no formulário principal...")

# Salvar dados mapeados
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df_doc_mapeado.to_excel(writer, sheet_name="Avaliação", index=False)
    df_ind_mapeado.to_excel(writer, sheet_name="Indicadores", index=False)
    df_tre_mapeado.to_excel(writer, sheet_name="Treinamento", index=False)
    df_qua_mapeado.to_excel(writer, sheet_name="Qualidade", index=False)

print(f"  -> Dados salvos no formulário principal")

# ============================================================
# 6. ATUALIZAR ABA RESUMO
# ============================================================
print("\n6. Atualizando aba Resumo...")

# Calcular métricas
total_docs = len(df_doc_mapeado)
docs_existentes = len(df_doc_mapeado[df_doc_mapeado["Existe?"] == "SIM"])
docs_atualizados = len(df_doc_mapeado[df_doc_mapeado["Está atualizado?"] == "SIM"])

total_indicadores = len(df_ind_mapeado)
indicadores_existentes = len(df_ind_mapeado[df_ind_mapeado["Existe indicador?"] == "SIM"])

total_treinamentos = len(df_tre_mapeado)
treinamentos_aplicados = len(df_tre_mapeado[df_tre_mapeado["Treinamento foi aplicado?"] == "SIM"]) if "Treinamento foi aplicado?" in df_tre_mapeado.columns else 0

total_monitorias = len(df_qua_mapeado)
monitorias_realizadas = len(df_qua_mapeado[df_qua_mapeado["Foram feitas monitorias de qualidade?"] == "SIM"]) if "Foram feitas monitorias de qualidade?" in df_qua_mapeado.columns else 0

# Criar dados de resumo
resumo_data = [
    ["RESUMO DA AVALIAÇÃO MOBILIZE"],
    [""],
    ["Indicador", "Resultado", "", "Faixa do Score", "Interpretação"],
    ["Documentações avaliadas", total_docs, "", "0-25", "Baixíssima maturidade documental"],
    ["Documentações existentes", docs_existentes, "", "26-35", "Baixa maturidade documental"],
    ["Documentações atualizadas", docs_atualizados, "", "0-25", "Baixíssima maturidade documental"],
    ["Indicadores avaliados", total_indicadores, "", "26-35", "Baixa maturidade de indicadores"],
    ["Indicadores existentes", indicadores_existentes, "", "26-35", "Baixa maturidade de indicadores"],
    ["Treinamentos avaliados", total_treinamentos, "", "26-35", "Baixa maturidade de treinamento"],
    ["Treinamentos aplicados", treinamentos_aplicados, "", "26-35", "Baixa maturidade de treinamento"],
    ["Monitorias avaliadas", total_monitorias, "", "26-35", "Baixa maturidade de qualidade"],
    ["Monitorias realizadas", monitorias_realizadas, "", "26-35", "Baixa maturidade de qualidade"],
]

# Adicionar aba Resumo ao Excel
wb = load_workbook(output_path)

# Remover aba Resumo existente se houver
if "Resumo" in wb.sheetnames:
    del wb["Resumo"]

ws = wb.create_sheet("Resumo")

for i, row in enumerate(resumo_data, start=1):
    for j, value in enumerate(row, start=1):
        ws.cell(row=i, column=j, value=value)

# Formatar cabeçalho
ws["A1"].font = Font(bold=True, size=14)
ws["A3"].font = Font(bold=True)
ws["B3"].font = Font(bold=True)
ws["D3"].font = Font(bold=True)
ws["E3"].font = Font(bold=True)

wb.save(output_path)
print(f"  -> Aba Resumo atualizada")

# ============================================================
# 7. VERIFICAR RESULTADO FINAL
# ============================================================
print("\n7. Verificando resultado final...")

xls = pd.ExcelFile(output_path)
for sheet_name in ['Avaliação', 'Indicadores', 'Treinamento', 'Qualidade']:
    df = pd.read_excel(output_path, sheet_name=sheet_name)
    operacoes = df['Operação'].unique() if 'Operação' in df.columns else []
    print(f"  -> {sheet_name}: {len(df)} registros | Operações: {operacoes}")

print("\n=== PREENCHIMENTO CONCLUÍDO COM SUCESSO ===")