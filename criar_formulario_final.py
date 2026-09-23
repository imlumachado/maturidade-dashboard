#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Criar formulário final apenas com dados da Mobilize."""

import pandas as pd
import json
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font

# Caminhos
form_novo = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO Analise de Maturidade em Processos.xlsx"
docx_path = r"C:\Users\User\maturidade-dashboard\mobilize_content.json"
output_path = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

print("=== CRIAÇÃO DO FORMULÁRIO FINAL - APENAS MOBILIZE ===\n")

# Carregar dados do DOCX
with open(docx_path, "r", encoding="utf-8") as f:
    docx_data = json.load(f)

# ============================================================
# 1. LER DADOS DO FORMULÁRIO NOVO (INDICADORES)
# ============================================================
print("1. Lendo dados de Indicadores do formulário novo...")

df_indicadores = pd.read_excel(form_novo, sheet_name="Indicadores")
df_indicadores = df_indicadores[df_indicadores['Operação'] == 'Mobilize'].copy()
print(f"  -> Indicadores Mobilize: {len(df_indicadores)} registros")

# ============================================================
# 2. CRIAR DADOS DE DOCUMENTOS (BASEADO NO DOCX)
# ============================================================
print("\n2. Criando dados de Documentos baseado no relatório...")

# Não conformidades do DOCX
nao_conformidades = docx_data["tables"][4]["data"]

documentos_data = []
id_counter = 1

# Documentos das não conformidades
docs_nc = [
    ("D.C.231.EXTE", "Documentação", "Divergências de versão e datas"),
    ("D.C.232.EXTE", "Documentação", "Divergências de versão e datas"),
    ("D.C.1504.EXTE", "Documentação", "Datas duplicadas"),
    ("D.C.2480.EXTE", "Documentação", "Atualizado sem controle de versão"),
    ("D.C.1517.EXTE", "Documentação", "Controles de versão duplicados"),
    ("D.C.136.EXTE", "Documentação", "Fluxograma descrito como orientação"),
]

for doc, area, obs in docs_nc:
    documentos_data.append({
        "ID Avaliação": id_counter,
        "Data da avaliação": "2026-09-18",
        "Operação": "Mobilize",
        "Processo avaliado": area,
        "Nome_Documento": doc,
        "Quantidade": 1,
        "Existe?": "SIM",
        "Está atualizado?": "NÃO",
        "Última atualização": "",
        "Padronizado?": "NÃO",
        "Coforme?": "Não Conformidade",
        "Existência": 1,
        "Atualização": 0,
        "Padrão": 0,
        "Conformidade": 0,
        "Observação": obs,
        "Plano de Ação": f"Corrigir {doc}",
        "Responsável": "Responsáveis documentais",
        "Prazo": "",
        "Status da Ação": "Aguardando ação"
    })
    id_counter += 1

# Documentos mencionados nas observações do DOCX
docs_observacoes = [
    ("Política da Informação Documentada", "Documentação", "Política"),
    ("Procedimento Operacional", "Documentação", "Procedimento"),
]

for doc, area, processo in docs_observacoes:
    documentos_data.append({
        "ID Avaliação": id_counter,
        "Data da avaliação": "2026-09-18",
        "Operação": "Mobilize",
        "Processo avaliado": processo,
        "Nome_Documento": doc,
        "Quantidade": 1,
        "Existe?": "SIM",
        "Está atualizado?": "SIM",
        "Última atualização": "2025-01-25",
        "Padronizado?": "SIM",
        "Coforme?": "Conformidade",
        "Existência": 1,
        "Atualização": 1,
        "Padrão": 1,
        "Conformidade": 1,
        "Observação": f"{doc} - {area}",
        "Plano de Ação": "",
        "Responsável": "",
        "Prazo": "",
        "Status da Ação": ""
    })
    id_counter += 1

df_documentos = pd.DataFrame(documentos_data)
print(f"  -> Documentos criados: {len(df_documentos)} registros")

# ============================================================
# 3. CRIAR DADOS DE TREINAMENTO (BASEADO NO DOCX)
# ============================================================
print("\n3. Criando dados de Treinamento baseado no relatório...")

treinamento_info = [
    ("Treinamento - Banco N1", "Treinamento", "Material sem controle de versão", "NÃO", "SIM", "NÃO", "Não Conformidade"),
    ("Treinamento - Locadora N1", "Treinamento", "Faltou rastreabilidade da evidência", "SIM", "SIM", "NÃO", "Não Conformidade"),
    ("Treinamento - BackOffice N2", "Treinamento", "Estrutura compatível", "SIM", "SIM", "SIM", "Conformidade"),
    ("Integração de Novos Colaboradores", "Treinamento", "Processo de integração", "SIM", "SIM", "SIM", "Conformidade"),
    ("Gestão de Incidentes", "Treinamento", "Treinamento de gestão de incidentes", "SIM", "SIM", "SIM", "Conformidade"),
]

treinamento_data = []
for i, (nome, area, obs, coerencia, aplicacao, atualizacao, conforme) in enumerate(treinamento_info, start=1):
    treinamento_data.append({
        "ID Avaliação": i,
        "Data da avaliação": "2026-09-18",
        "Operação": "Mobilize",
        "Processo avaliado": area,
        "Nome_Treinamento": nome,
        "Quantidade": 1,
        "Treinamento está coerente aos documentos?": coerencia,
        "Treinamento foi aplicado?": aplicacao,
        "Houve atualização?": atualizacao,
        "Conforme?": conforme,
        "Coerência": 1 if coerencia == "SIM" else 0,
        "Aplicação": 1 if aplicacao == "SIM" else 0,
        "Atualização": 1 if atualizacao == "SIM" else 0,
        "Conformidade": 1 if conforme == "Conformidade" else (0 if conforme == "Não Conformidade" else -1),
        "Observação": obs,
        "Plano de Ação": f"Versionar {nome}" if conforme != "Conformidade" else "",
        "Responsável": "Daniel da Silva" if conforme != "Conformidade" else "",
        "Prazo": "",
        "Status da Ação": "Aguardando ação" if conforme != "Conformidade" else ""
    })

df_treinamento = pd.DataFrame(treinamento_data)
print(f"  -> Treinamento criado: {len(df_treinamento)} registros")

# ============================================================
# 4. CRIAR DADOS DE QUALIDADE (BASEADO NO DOCX)
# ============================================================
print("\n4. Criando dados de Qualidade baseado no relatório...")

qualidade_info = [
    ("Portal da Qualidade", "Qualidade", "Amostral", "Conformidade", 1, 0.5, 1),
    ("Cessão de Direitos", "Qualidade", "Amostral", "Conformidade", 1, 0.5, 1),
    ("Clube FIQ", "Qualidade", "Não realizada", "Não Conformidade Grave", 0, 0, -1),
]

qualidade_data = []
for i, (nome, area, metodo, conforme, existencia, abrangencia, conformidade) in enumerate(qualidade_info, start=1):
    qualidade_data.append({
        "ID Avaliação": i,
        "Data da avaliação": "2026-09-18",
        "Operação": "Mobilize",
        "Processo avaliado": area,
        "Processo Monitorado": nome,
        "Quantidade": 1,
        "Foram feitas monitorias de qualidade?": "SIM" if "Não realizada" not in metodo else "NÃO",
        "Como são feitas as monitorias?": metodo,
        "Conforme?": conforme,
        "Existência": existencia,
        "Abrangência": abrangencia,
        "Conformidade": conformidade,
        "Observação": f"Monitoria {nome}: {metodo}"
    })

df_qualidade = pd.DataFrame(qualidade_data)
print(f"  -> Qualidade criada: {len(df_qualidade)} registros")

# ============================================================
# 5. SALVAR FORMULÁRIO FINAL
# ============================================================
print("\n5. Salvando formulário final...")

# Criar backup
import shutil
backup_path = output_path + ".backup_final"
shutil.copy2(output_path, backup_path)
print(f"  -> Backup criado: {backup_path}")

# Salvar dados
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df_documentos.to_excel(writer, sheet_name="Avaliação", index=False)
    df_indicadores.to_excel(writer, sheet_name="Indicadores", index=False)
    df_treinamento.to_excel(writer, sheet_name="Treinamento", index=False)
    df_qualidade.to_excel(writer, sheet_name="Qualidade", index=False)

print(f"  -> Formulário salvo")

# ============================================================
# 6. ATUALIZAR ABA RESUMO
# ============================================================
print("\n6. Atualizando aba Resumo...")

# Calcular métricas
total_docs = len(df_documentos)
docs_existentes = len(df_documentos[df_documentos["Existe?"] == "SIM"])
docs_atualizados = len(df_documentos[df_documentos["Está atualizado?"] == "SIM"])

total_indicadores = len(df_indicadores)
indicadores_existentes = len(df_indicadores[df_indicadores["Existe indicador?"] == "SIM"])

total_treinamentos = len(df_treinamento)
treinamentos_aplicados = len(df_treinamento[df_treinamento["Treinamento foi aplicado?"] == "SIM"])

total_monitorias = len(df_qualidade)
monitorias_realizadas = len(df_qualidade[df_qualidade["Foram feitas monitorias de qualidade?"] == "SIM"])

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

print("\n=== FORMULÁRIO FINAL CRIADO COM SUCESSO ===")