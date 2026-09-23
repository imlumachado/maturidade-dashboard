#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Criar formulário limpo apenas com dados da Mobilize."""

import pandas as pd
import json
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Caminhos
docx_path = r"C:\Users\User\maturidade-dashboard\mobilize_content.json"
output_path = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

# Carregar dados do DOCX
with open(docx_path, "r", encoding="utf-8") as f:
    docx_data = json.load(f)

print("=== CRIAÇÃO DE FORMULÁRIO LIMPO - MOBILIZE ===\n")

# Dados da avaliação
data_avaliacao = "18/09/2026"
operacao = "Mobilize"

# ============================================================
# 1. ABA AVALIAÇÃO (DOCUMENTAÇÃO)
# ============================================================
print("1. Criando aba Avaliação (Documentação)...")

# Não conformidades do DOCX
nao_conformidades = docx_data["tables"][4]["data"]

# Documentos mencionados nas observações
docs_mencionados = [
    ("D.C.231.EXTE", "Documentação", "Divergências de versão e datas"),
    ("D.C.232.EXTE", "Documentação", "Divergências de versão e datas"),
    ("D.C.1504.EXTE", "Documentação", "Datas de criação, modificação e aprovação duplicadas"),
    ("D.C.2480.EXTE", "Documentação", "Atualizado sem alteração do controle de versão"),
    ("D.C.1517.EXTE", "Documentação", "Controles de versão duplicados"),
    ("D.C.136.EXTE", "Documentação", "Denominado fluxograma, mas descrito como material de orientação"),
]

# Criar dados para aba Avaliação
avaliacao_data = []
id_counter = 1

# Adicionar documentos das não conformidades
for nc in nao_conformidades[1:]:  # Pular cabeçalho
    if len(nc) >= 4:
        id_nc, area, requisito, descricao = nc[0], nc[1], nc[2], nc[3]
        
        # Determinar se existe baseado na descrição
        existe = "NÃO" if "ausência" in descricao.lower() or "sem" in descricao.lower() else "SIM"
        atualizado = "NÃO"  # Maioria não está atualizada
        padronizado = "NÃO"  # Maioria não está padronizada
        conforme = "Não Conformidade Grave" if "grave" in descricao.lower() or "divergências" in descricao.lower() else "Não Conformidade"
        
        avaliacao_data.append({
            "ID Avaliação": id_counter,
            "Data da avaliação": data_avaliacao,
            "Operação": operacao,
            "Processo avaliado": area,
            "Nome_Documento": f"Documento {id_nc}",
            "Quantidade": 1,
            "Existe?": existe,
            "Está atualizado?": atualizado,
            "Última atualização": "",
            "Padronizado?": padronizado,
            "Coforme?": conforme,
            "Existência": 1 if existe == "SIM" else 0,
            "Atualização": 1 if atualizado == "SIM" else 0,
            "Padrão": 1 if padronizado == "SIM" else 0,
            "Conformidade": -1 if "Grave" in conforme else (0 if "Não" in conforme else 1),
            "Documentação": 0,
            "Geral": 0,
            "Observação": descricao,
            "Plano de Ação": f"Corrigir {id_nc.lower()}",
            "Responsável": "Responsáveis documentais",
            "Prazo": "",
            "Status da Ação": "Aguardando ação"
        })
        id_counter += 1

# Adicionar documentos mencionados nas observações
for doc, area, obs in docs_mencionados:
    avaliacao_data.append({
        "ID Avaliação": id_counter,
        "Data da avaliação": data_avaliacao,
        "Operação": operacao,
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
        "Documentação": 0,
        "Geral": 0,
        "Observação": obs,
        "Plano de Ação": f"Atualizar {doc}",
        "Responsável": "Responsáveis documentais",
        "Prazo": "",
        "Status da Ação": "Aguardando ação"
    })
    id_counter += 1

df_avaliacao = pd.DataFrame(avaliacao_data)
print(f"  -> {len(df_avaliacao)} registros criados")

# ============================================================
# 2. ABA INDICADORES
# ============================================================
print("2. Criando aba Indicadores...")

# Indicadores mencionados no DOCX
indicadores_info = [
    ("NS", "Nível de Serviço", "Manual", "NÃO", "Não Conformidade"),
    ("PCA", "Programa de Controle de Absenteísmo", "Manual", "NÃO", "Não Conformidade"),
    ("TMA", "Tempo Médio de Atendimento", "Automático", "SIM", "Conformidade"),
    ("TME", "Tempo Médio de Espera", "Automático", "SIM", "Conformidade"),
    ("CSAT", "Customer Satisfaction", "Automático", "SIM", "Conformidade"),
    ("FCR", "First Call Resolution", "Automático", "SIM", "Conformidade"),
    ("SLA", "Service Level Agreement", "Automático", "SIM", "Conformidade"),
    ("HC", "Headcount", "Manual", "NÃO", "Não Conformidade"),
    ("ABS", "Absenteísmo", "Manual", "NÃO", "Não Conformidade"),
    ("TO", "Turnover", "Manual", "NÃO", "Não Conformidade"),
]

indicadores_data = []
for i, (sigla, nome, atualizacao, padrao, conforme) in enumerate(indicadores_info, start=1):
    existe = "SIM"
    indicadores_data.append({
        "ID Avaliação": i,
        "Data da avaliação": data_avaliacao,
        "Operação": operacao,
        "Processo avaliado": "Indicadores",
        "Nome_Indicador": f"{sigla} - {nome}",
        "Quantidade": 1,
        "Existe indicador?": existe,
        "Como é atualizado?": atualizacao,
        "No padrão?": padrao,
        "Conforme?": conforme,
        "Existência": 1,
        "Atualização": 1 if atualizacao == "Automático" else 0.5,
        "Padrão": 1 if padrao == "SIM" else 0,
        "Conformidade": 1 if conforme == "Conformidade" else 0,
        "Score Indicadores": 100 if conforme == "Conformidade" else 0,
        "Geral": 0,
        "Observação": f"Indicador {sigla} - {nome}",
        "Plano de Ação": f"Formalizar histórico de metas para {sigla}" if conforme != "Conformidade" else "",
        "Responsável": "Wesley Soares e supervisores" if conforme != "Conformidade" else "",
        "Prazo": "",
        "Status da Ação": "Aguardando ação" if conforme != "Conformidade" else ""
    })

df_indicadores = pd.DataFrame(indicadores_data)
print(f"  -> {len(df_indicadores)} registros criados")

# ============================================================
# 3. ABA TREINAMENTO
# ============================================================
print("3. Criando aba Treinamento...")

# Treinamentos mencionados no DOCX
treinamento_info = [
    ("Treinamento - Banco N1", "Material sem controle de versão", "NÃO", "SIM", "NÃO", "Não Conformidade"),
    ("Treinamento - Locadora N1", "Faltou rastreabilidade da evidência individual", "SIM", "SIM", "NÃO", "Não Conformidade"),
    ("Treinamento - BackOffice N2", "Estrutura compatível", "SIM", "SIM", "SIM", "Conformidade"),
]

treinamento_data = []
for i, (nome, obs, coerencia, aplicacao, atualizacao, conforme) in enumerate(treinamento_info, start=1):
    treinamento_data.append({
        "ID Avaliação": i,
        "Data da avaliação": data_avaliacao,
        "Operação": operacao,
        "Processo avaliado": "Treinamento",
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
        "Score Treinamento": 100 if conforme == "Conformidade" else (0 if conforme == "Não Conformidade" else -25),
        "Geral": 0,
        "Observação": obs,
        "Plano de Ação": f"Versionar materiais de {nome}" if conforme != "Conformidade" else "",
        "Responsável": "Daniel da Silva" if conforme != "Conformidade" else "",
        "Prazo": "",
        "Status da Ação": "Aguardando ação" if conforme != "Conformidade" else ""
    })

df_treinamento = pd.DataFrame(treinamento_data)
print(f"  -> {len(df_treinamento)} registros criados")

# ============================================================
# 4. ABA QUALIDADE
# ============================================================
print("4. Criando aba Qualidade...")

# Monitorias mencionadas no DOCX
qualidade_info = [
    ("Portal da Qualidade", "Amostral", "Conformidade", 1, 0.5, 1),
    ("Cessão de Direitos", "Amostral", "Conformidade", 1, 0.5, 1),
    ("Clube FIQ", "Não realizada", "Não Conformidade Grave", 0, 0, -1),
]

qualidade_data = []
for i, (nome, metodo, conforme, existencia, abrangencia, conformidade) in enumerate(qualidade_info, start=1):
    qualidade_data.append({
        "ID Avaliação": i,
        "Data da avaliação": data_avaliacao,
        "Operação": operacao,
        "Processo avaliado": "Qualidade",
        "Processo Monitorado": nome,
        "Quantidade": 1,
        "Foram feitas monitorias de qualidade?": "SIM" if "Não realizada" not in metodo else "NÃO",
        "Como são feitas as monitorias?": metodo,
        "Conforme?": conforme,
        "Existência": existencia,
        "Abrangência": abrangencia,
        "Conformidade": conformidade,
        "Score Qualidade": 83 if conforme == "Conformidade" else (-33 if "Grave" in conforme else 0),
        "Geral": 0,
        "Observação": f"Monitoria {nome}: {metodo}"
    })

df_qualidade = pd.DataFrame(qualidade_data)
print(f"  -> {len(df_qualidade)} registros criados")

# ============================================================
# 5. SALVAR FORMULÁRIO
# ============================================================
print("\n5. Salvando formulário limpo...")

# Criar DataFrame para cada aba
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    df_avaliacao.to_excel(writer, sheet_name="Avaliação", index=False)
    df_indicadores.to_excel(writer, sheet_name="Indicadores", index=False)
    df_treinamento.to_excel(writer, sheet_name="Treinamento", index=False)
    df_qualidade.to_excel(writer, sheet_name="Qualidade", index=False)

print(f"  -> Formulário salvo em: {output_path}")

# ============================================================
# 6. ATUALIZAR ABA RESUMO
# ============================================================
print("6. Atualizando aba Resumo...")

# Calcular métricas
total_docs = len(df_avaliacao)
docs_existentes = len(df_avaliacao[df_avaliacao["Existe?"] == "SIM"])
docs_atualizados = len(df_avaliacao[df_avaliacao["Está atualizado?"] == "SIM"])

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

df_resumo = pd.DataFrame(resumo_data)

# Adicionar aba Resumo ao Excel
from openpyxl import load_workbook
wb = load_workbook(output_path)
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
# 7. ADICIONAR ABAS DE REFERÊNCIA
# ============================================================
print("7. Adicionando abas de referência...")

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

wb.save(output_path)
print(f"  -> Abas de referência adicionadas")

print("\n=== FORMULÁRIO LIMPO CRIADO COM SUCESSO ===")
print(f"\nResumo:")
print(f"  • Avaliação (Documentação): {len(df_avaliacao)} registros")
print(f"  • Indicadores: {len(df_indicadores)} registros")
print(f"  • Treinamento: {len(df_treinamento)} registros")
print(f"  • Qualidade: {len(df_qualidade)} registros")
print(f"  • Arquivo: {output_path}")