#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migrar dados do novo formulário para o formulário principal."""

import pandas as pd
import json
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Caminhos
form_novo = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO Analise de Maturidade em Processos.xlsx"
form_principal = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

print("=== MIGRAÇÃO DE DADOS DO NOVO FORMULÁRIO ===\n")

# ============================================================
# 1. LER DADOS DO NOVO FORMULÁRIO
# ============================================================
print("1. Lendo dados do novo formulário...")

# Ler aba de Documentos e filtrar linhas com dados válidos
df_documentos = pd.read_excel(form_novo, sheet_name="Documentos")
df_documentos = df_documentos.dropna(subset=["Data da avaliação", "Operação", "Nome_Documento"])
print(f"  -> Documentos: {len(df_documentos)} registros válidos")

# Ler aba de Indicadores e filtrar linhas com dados válidos
df_indicadores = pd.read_excel(form_novo, sheet_name="Indicadores")
df_indicadores = df_indicadores.dropna(subset=["Data da avaliação", "Operação", "Nome_Indicador"])
print(f"  -> Indicadores: {len(df_indicadores)} registros válidos")

# Ler aba de Treinamento e filtrar linhas com dados válidos
df_treinamento = pd.read_excel(form_novo, sheet_name="Treinamento")
df_treinamento = df_treinamento.dropna(subset=["Data da avaliação", "Operação", "Nome_Treinamento"])
print(f"  -> Treinamento: {len(df_treinamento)} registros válidos")

# Ler aba de Qualidade e filtrar linhas com dados válidos
df_qualidade = pd.read_excel(form_novo, sheet_name="Qualidade")
df_qualidade = df_qualidade.dropna(subset=["Data da avaliação", "Operação", "Processo Monitorado"])
print(f"  -> Qualidade: {len(df_qualidade)} registros válidos")

# ============================================================
# 2. MAPEAR COLUNAS PARA ESTRUTURA DO DASHBOARD
# ============================================================
print("\n2. Mapeando colunas para estrutura do dashboard...")

# Mapear colunas de Documentos
colunas_documentos = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Processo avaliado": "Processo avaliado",
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

# Renomear colunas
df_documentos_mapeado = df_documentos.rename(columns=colunas_documentos)

# Adicionar colunas faltantes
colunas_faltantes_doc = ["Documentação", "Geral"]
for col in colunas_faltantes_doc:
    if col not in df_documentos_mapeado.columns:
        df_documentos_mapeado[col] = 0

# Mapear colunas de Indicadores
colunas_indicadores = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Processo avaliado": "Processo avaliado",
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

df_indicadores_mapeado = df_indicadores.rename(columns=colunas_indicadores)

# Adicionar colunas faltantes
colunas_faltantes_ind = ["Score Indicadores", "Geral"]
for col in colunas_faltantes_ind:
    if col not in df_indicadores_mapeado.columns:
        df_indicadores_mapeado[col] = 0

# Mapear colunas de Treinamento
colunas_treinamento = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Processo avaliado": "Processo avaliado",
    "Nome_Treinamento": "Nome_Treinamento",
    "Quantidade": "Quantidade",
    "Treinamento está coerente aos documentos?": "Treinamento está coerente aos documentos?",
    "Treinamento foi aplicado?": "Treinamento foi aplicado?",
    "Houve atualização?": "Houve atualização?",
    "Conforme?": "Conforme?",
    "Coerência": "Coerência",
    "Aplicação": "Aplicação",
    "Atualização": "Atualização",
    "Conformidade": "Conformidade",
    "Observação": "Observação",
    "Plano de Ação": "Plano de Ação",
    "Responsável": "Responsável",
    "Prazo": "Prazo",
    "Status da Ação": "Status da Ação"
}

df_treinamento_mapeado = df_treinamento.rename(columns=colunas_treinamento)

# Adicionar colunas faltantes
colunas_faltantes_tre = ["Score Treinamento", "Geral"]
for col in colunas_faltantes_tre:
    if col not in df_treinamento_mapeado.columns:
        df_treinamento_mapeado[col] = 0

# Mapear colunas de Qualidade
colunas_qualidade = {
    "ID Avaliação": "ID Avaliação",
    "Data da avaliação": "Data da avaliação",
    "Operação": "Operação",
    "Processo avaliado": "Processo avaliado",
    "Processo Monitorado": "Processo Monitorado",
    "Quantidade": "Quantidade",
    "Foram feitas monitorias de qualidade?": "Foram feitas monitorias de qualidade?",
    "Como são feitas as monitorias?": "Como são feitas as monitorias?",
    "Conforme?": "Conforme?",
    "Existência": "Existência",
    "Abrangência": "Abrangência",
    "Conformidade": "Conformidade",
    "Observação": "Observação"
}

df_qualidade_mapeado = df_qualidade.rename(columns=colunas_qualidade)

# Adicionar colunas faltantes
colunas_faltantes_qua = ["Score Qualidade", "Geral"]
for col in colunas_faltantes_qua:
    if col not in df_qualidade_mapeado.columns:
        df_qualidade_mapeado[col] = 0

print("  -> Colunas mapeadas com sucesso")

# ============================================================
# 3. SALVAR NO FORMULÁRIO PRINCIPAL
# ============================================================
print("\n3. Salvando dados no formulário principal...")

# Criar backup do formulário atual
import shutil
backup_path = form_principal + ".backup"
shutil.copy2(form_principal, backup_path)
print(f"  -> Backup criado: {backup_path}")

# Salvar dados mapeados
with pd.ExcelWriter(form_principal, engine="openpyxl") as writer:
    df_documentos_mapeado.to_excel(writer, sheet_name="Avaliação", index=False)
    df_indicadores_mapeado.to_excel(writer, sheet_name="Indicadores", index=False)
    df_treinamento_mapeado.to_excel(writer, sheet_name="Treinamento", index=False)
    df_qualidade_mapeado.to_excel(writer, sheet_name="Qualidade", index=False)

print(f"  -> Dados salvos no formulário principal")

# ============================================================
# 4. ATUALIZAR ABA RESUMO
# ============================================================
print("\n4. Atualizando aba Resumo...")

# Calcular métricas
total_docs = len(df_documentos_mapeado)
docs_existentes = len(df_documentos_mapeado[df_documentos_mapeado["Existe?"] == "SIM"])
docs_atualizados = len(df_documentos_mapeado[df_documentos_mapeado["Está atualizado?"] == "SIM"])

total_indicadores = len(df_indicadores_mapeado)
indicadores_existentes = len(df_indicadores_mapeado[df_indicadores_mapeado["Existe indicador?"] == "SIM"])

total_treinamentos = len(df_treinamento_mapeado)
treinamentos_aplicados = len(df_treinamento_mapeado[df_treinamento_mapeado["Treinamento foi aplicado?"] == "SIM"])

total_monitorias = len(df_qualidade_mapeado)
monitorias_realizadas = len(df_qualidade_mapeado[df_qualidade_mapeado["Foram feitas monitorias de qualidade?"] == "SIM"])

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
wb = load_workbook(form_principal)
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

wb.save(form_principal)
print(f"  -> Aba Resumo atualizada")

# ============================================================
# 5. ADICIONAR ABAS DE REFERÊNCIA
# ============================================================
print("\n5. Adicionando abas de referência...")

# Adicionar aba Critérios
criteria_data = [
    ["CRITÉRIOS E REGRAS DE PREENCHIMENTO"],
    [""],
    ["Campo", "O que registrar", "Tipo", "Obrigatório?", "Regra", "Exemplo"],
    ["Data da avaliação", "Data em que a análise foi realizada.", "Data", "Sim", "Usar dd/mm/aaaa.", "18/09/2026"],
    ["Operação", "Nome da operação analisada.", "Texto", "Sim", "Padronizar nomenclatura.", "Mobilize"],
    ["Processo avaliado", "Processo ou área avaliada.", "Texto", "Sim", "Usar nomenclatura do DOCX.", "Documentação"],
    ["Nome_Documento", "Nome ou código do documento.", "Texto", "Sim", "Incluir código se houver.", "D.C.231.EXTE"],
    ["Existe?", "Se o documento existe.", "SIM/NÃO", "Sim", "SIM ou NÃO.", "SIM"],
    ["Está atualizado?", "Se está versão vigente.", "SIM/NÃO", "Sim", "SIM ou NÃO.", "NÃO"],
    ["Padronizado?", "Se segue padrão definido.", "SIM/NÃO", "Sim", "SIM ou NÃO.", "NÃO"],
    ["Coforme?", "Nível de conformidade.", "Texto", "Sim", "Conformidade/Parcial/Não Conformidade.", "Não Conformidade"],
]

ws_criteria = wb.create_sheet("Critérios")
for i, row in enumerate(criteria_data, start=1):
    for j, value in enumerate(row, start=1):
        ws_criteria.cell(row=i, column=j, value=value)

ws_criteria["A1"].font = Font(bold=True, size=14)
ws_criteria["A3"].font = Font(bold=True)

# Adicionar aba Modelo de Score
score_data = [
    ["MODELO DE SCORE - BASE PARA EVOLUÇÃO DA MATURIDADE"],
    [""],
    ["Dimensão", "Indicador", "Pontuação atual", "Peso sugerido", "Score ponderado", "Fonte", "Observação"],
    ["Existência", "Existe documentação?", "1 = SIM / 0 = NÃO", 0.3333, 0.27775, "Avaliação", "Pode ser refinado para medir cobertura do processo"],
    ["Atualização", "Está atualizado?", "1 = SIM / 0 = NÃO", 0.3333, 0.27775, "Avaliação", "Pode incorporar faixas por idade da revisão"],
    ["Padrão", "Está padronizado?", "1 = SIM / 0 = NÃO", 0.3333, 0.27775, "Avaliação", "Pode ser refinado para medir aderência a模板"],
    ["Conformidade", "É conforme?", "1 = Conformidade / 0 = Parcial / -1 = Não conformidade", 1.0, 0.1665, "Avaliação", "Pode ser ponderado por gravidade"],
]

ws_score = wb.create_sheet("Modelo de Score")
for i, row in enumerate(score_data, start=1):
    for j, value in enumerate(row, start=1):
        ws_score.cell(row=i, column=j, value=value)

ws_score["A1"].font = Font(bold=True, size=14)
ws_score["A3"].font = Font(bold=True)

# Adicionar aba Como usar
como_usar_data = [
    ["COMO UTILIZAR O FORMULÁRIO"],
    [""],
    ["1", "Defina a operação", "Informe a operação que será avaliada."],
    ["2", "Liste os processos", "Registre cada processo que será objeto da análise."],
    ["3", "Registre as documentações", "Para cada documento, use uma nova linha."],
    ["4", "Avalie cada critério", "Marque SIM ou NÃO para cada critério."],
    ["5", "Registre não conformidades", "Descreva objetivamente a não conformidade."],
    ["6", "Crie plano de ação", "Para cada NC, defina ação, responsável e prazo."],
    ["7", "Atualize o resumo", "Calcule os indicadores na aba Resumo."],
]

ws_como_usar = wb.create_sheet("Como usar")
for i, row in enumerate(como_usar_data, start=1):
    for j, value in enumerate(row, start=1):
        ws_como_usar.cell(row=i, column=j, value=value)

ws_como_usar["A1"].font = Font(bold=True, size=14)

wb.save(form_principal)
print(f"  -> Abas de referência adicionadas")

# ============================================================
# 6. VERIFICAR RESULTADO
# ============================================================
print("\n6. Verificando resultado...")

# Recarregar dados
xls = pd.ExcelFile(form_principal)
print(f"  -> Abas no formulário: {xls.sheet_names}")

# Contar registros
for sheet_name in ["Avaliação", "Indicadores", "Treinamento", "Qualidade"]:
    df = pd.read_excel(form_principal, sheet_name=sheet_name)
    print(f"  -> {sheet_name}: {len(df)} registros")

print("\n=== MIGRAÇÃO CONCLUÍDA COM SUCESSO ===")
print(f"\nFormulário principal atualizado: {form_principal}")
print(f"Backup criado: {backup_path}")