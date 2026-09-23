#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Preencher o formulário Excel com dados do DOCX da Mobilize."""

import pandas as pd
import json
import os
from datetime import datetime

# Caminhos
docx_json_path = r"C:\Users\User\maturidade-dashboard\mobilize_content.json"
form_path = r"C:\Users\User\maturidade-dashboard\formulario\F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"
output_path = r"C:\Users\User\maturidade-dashboard\F.O.091.GOCO - Analise de Maturidade em Processos - Mobilize.xlsx"

def load_docx_data(json_path):
    """Carregar dados extraídos do DOCX."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_mobilize_data(docx_data):
    """Criar dados estruturados para o formulário Excel baseado no DOCX."""
    
    # Data da avaliação
    data_avaliacao = "18/09/2026"
    operacao = "Mobilize"
    
    # Dados para aba de Avaliação (Documentação)
    avaliacao_data = []
    
    # Extrair informações das tabelas do DOCX
    tables = docx_data["tables"]
    
    # Tabela 1: Informações gerais
    info_geral = tables[0]["data"]
    
    # Tabela 2: Avaliação de requisitos (4.1 a 9.1.2)
    requisitos_avaliacao = tables[1]["data"]
    
    # Tabela 3: Resultados consolidados
    resultados_consolidados = tables[2]["data"]
    
    # Tabela 4: Avaliação por área
    avaliacao_por_area = tables[3]["data"]
    
    # Tabela 5: Não conformidades
    nao_conformidades = tables[4]["data"]
    
    # Tabela 6 e 7: Plano de ações
    plano_acoes = tables[5]["data"]
    
    # Criar linhas para aba de Avaliação (Documentação)
    # Baseado nas não conformidades identificadas
    for i, nc in enumerate(nao_conformidades[1:], start=1):  # Pular cabeçalho
        if len(nc) >= 4:
            id_nc, area, requisito, descricao = nc[0], nc[1], nc[2], nc[3]
            
            avaliacao_data.append({
                "ID Avaliação": i,
                "Data da avaliação": data_avaliacao,
                "Operação": operacao,
                "Processo avaliado": area,
                "Nome_Documento": f"Documento {id_nc}",
                "Quantidade": 1,
                "Existe?": "NÃO" if "Não conforme" in descricao.lower() else "SIM",
                "Está atualizado?": "NÃO",
                "Última atualização": "",
                "Padronizado?": "NÃO"
            })
    
    # Adicionar documentos mencionados nas observações
    docs_mencionados = [
        "D.C.231.EXTE", "D.C.232.EXTE", "D.C.1504.EXTE", 
        "D.C.2480.EXTE", "D.C.1517.EXTE", "D.C.136.EXTE"
    ]
    
    for doc in docs_mencionados:
        avaliacao_data.append({
            "ID Avaliação": len(avaliacao_data) + 1,
            "Data da avaliação": data_avaliacao,
            "Operação": operacao,
            "Processo avaliado": "Documentação",
            "Nome_Documento": doc,
            "Quantidade": 1,
            "Existe?": "SIM",
            "Está atualizado?": "NÃO",
            "Última atualização": "",
            "Padronizado?": "NÃO"
        })
    
    # Dados para aba de Indicadores
    indicadores_data = []
    
    # Extrair indicadores mencionados no DOCX
    indicadores_mencionados = ["NS", "PCA", "TMA", "TME", "CSAT", "FCR", "SLA", "HC", "ABS", "TO"]
    
    for i, indicador in enumerate(indicadores_mencionados, start=1):
        indicadores_data.append({
            "ID Avaliação": i,
            "Data da avaliação": data_avaliacao,
            "Operação": operacao,
            "Processo avaliado": "Indicadores",
            "Nome_Indicador": indicador,
            "Quantidade": 1,
            "Existe indicador?": "SIM",
            "Como é atualizado?": "Manual",
            "No padrão?": "NÃO",
            "Conforme?": "Não Conformidade"
        })
    
    # Dados para aba de Treinamento
    treinamento_data = []
    
    # Extrair informações de treinamento do DOCX
    treinamento_info = [
        ("Treinamento - Banco N1", "Material sem controle de versão"),
        ("Treinamento - Locadora N1", "Faltou rastreabilidade da evidência individual"),
        ("Treinamento - BackOffice N2", "Estrutura compatível")
    ]
    
    for i, (nome, obs) in enumerate(treinamento_info, start=1):
        treinamento_data.append({
            "ID Avaliação": i,
            "Data da avaliação": data_avaliacao,
            "Operação": operacao,
            "Processo avaliado": "Treinamento",
            "Nome_Treinamento": nome,
            "Quantidade": 1,
            "Treinamento está coerente aos documentos?": "SIM" if "compatível" in obs else "NÃO",
            "Treinamento foi aplicado?": "SIM",
            "Houve atualização?": "NÃO",
            "Conforme?": "Conformidade" if "compatível" in obs else "Não Conformidade"
        })
    
    # Dados para aba de Qualidade
    qualidade_data = []
    
    # Extrair informações de qualidade do DOCX
    qualidade_info = [
        ("Monitoria - Portal da Qualidade", "Amostral", "Conformidade"),
        ("Monitoria - Cessão de Direitos", "Amostral", "Conformidade"),
        ("Monitoria - Clube FIQ", "Não realizada", "Não Conformidade Grave")
    ]
    
    for i, (nome, metodo, conformidade) in enumerate(qualidade_info, start=1):
        qualidade_data.append({
            "ID Avaliação": i,
            "Data da avaliação": data_avaliacao,
            "Operação": operacao,
            "Processo avaliado": "Qualidade",
            "Processo Monitorado": nome,
            "Quantidade": 1,
            "Foram feitas monitorias de qualidade?": "SIM" if "Não realizada" not in metodo else "NÃO",
            "Como são feitas as monitorias?": metodo,
            "Conforme?": conformidade,
            "Existência": 1 if "Conformidade" == conformidade else 0
        })
    
    return {
        "avaliacao": avaliacao_data,
        "indicadores": indicadores_data,
        "treinamento": treinamento_data,
        "qualidade": qualidade_data,
        "info_geral": info_geral,
        "nao_conformidades": nao_conformidades,
        "plano_acoes": plano_acoes
    }

def fill_excel_form(data, form_path, output_path):
    """Preencher o formulário Excel com os dados extraídos."""
    
    import shutil
    
    # Copiar o formulário original para o arquivo de saída
    shutil.copy2(form_path, output_path)
    
    # Ler o formulário original para obter as dimensões
    xls = pd.ExcelFile(form_path)
    
    # Atualizar cada aba com os novos dados
    for sheet_name in xls.sheet_names:
        df_original = pd.read_excel(form_path, sheet_name=sheet_name, header=None)
        
        # Determinar quais dados escrever com base no nome da aba
        if sheet_name == "Avaliação" and data["avaliacao"]:
            df_new = pd.DataFrame(data["avaliacao"])
            start_row = df_original.shape[0]
            
            # Usar openpyxl diretamente para escrever
            from openpyxl import load_workbook
            wb = load_workbook(output_path)
            ws = wb[sheet_name]
            
            for i, row in df_new.iterrows():
                for j, value in enumerate(row):
                    ws.cell(row=start_row + i + 1, column=j + 1, value=value)
            
            wb.save(output_path)
            wb.close()
        
        elif sheet_name == "Indicadores" and data["indicadores"]:
            df_new = pd.DataFrame(data["indicadores"])
            start_row = df_original.shape[0]
            
            from openpyxl import load_workbook
            wb = load_workbook(output_path)
            ws = wb[sheet_name]
            
            for i, row in df_new.iterrows():
                for j, value in enumerate(row):
                    ws.cell(row=start_row + i + 1, column=j + 1, value=value)
            
            wb.save(output_path)
            wb.close()
        
        elif sheet_name == "Treinamento" and data["treinamento"]:
            df_new = pd.DataFrame(data["treinamento"])
            start_row = df_original.shape[0]
            
            from openpyxl import load_workbook
            wb = load_workbook(output_path)
            ws = wb[sheet_name]
            
            for i, row in df_new.iterrows():
                for j, value in enumerate(row):
                    ws.cell(row=start_row + i + 1, column=j + 1, value=value)
            
            wb.save(output_path)
            wb.close()
        
        elif sheet_name == "Qualidade" and data["qualidade"]:
            df_new = pd.DataFrame(data["qualidade"])
            start_row = df_original.shape[0]
            
            from openpyxl import load_workbook
            wb = load_workbook(output_path)
            ws = wb[sheet_name]
            
            for i, row in df_new.iterrows():
                for j, value in enumerate(row):
                    ws.cell(row=start_row + i + 1, column=j + 1, value=value)
            
            wb.save(output_path)
            wb.close()
    
    # Atualizar aba de Resumo
    atualizar_resumo(data, output_path)
    
    print(f"Formulário preenchido salvo em: {output_path}")

def atualizar_resumo(data, output_path):
    """Atualizar aba de Resumo com os dados da avaliação."""
    
    # Calcular métricas
    total_docs = len(data["avaliacao"])
    docs_existentes = sum(1 for item in data["avaliacao"] if item.get("Existe?") == "SIM")
    docs_atualizados = sum(1 for item in data["avaliacao"] if item.get("Está atualizado?") == "SIM")
    
    total_indicadores = len(data["indicadores"])
    indicadores_existentes = sum(1 for item in data["indicadores"] if item.get("Existe indicador?") == "SIM")
    
    total_treinamentos = len(data["treinamento"])
    treinamentos_aplicados = sum(1 for item in data["treinamento"] if item.get("Treinamento foi aplicado?") == "SIM")
    
    total_monitorias = len(data["qualidade"])
    monitorias_realizadas = sum(1 for item in data["qualidade"] if item.get("Foram feitas monitorias de qualidade?") == "SIM")
    
    # Criar dados de resumo
    resumo_data = [
        ["Documentações avaliadas", total_docs, "0-25", "Baixíssima maturidade documental"],
        ["Documentações existentes", docs_existentes, "26-35", "Baixa maturidade documental"],
        ["Documentações atualizadas", docs_atualizados, "0-25", "Baixíssima maturidade documental"],
        ["Indicadores avaliados", total_indicadores, "26-35", "Baixa maturidade de indicadores"],
        ["Indicadores existentes", indicadores_existentes, "26-35", "Baixa maturidade de indicadores"],
        ["Treinamentos avaliados", total_treinamentos, "26-35", "Baixa maturidade de treinamento"],
        ["Treinamentos aplicados", treinamentos_aplicados, "26-35", "Baixa maturidade de treinamento"],
        ["Monitorias avaliadas", total_monitorias, "26-35", "Baixa maturidade de qualidade"],
        ["Monitorias realizadas", monitorias_realizadas, "26-35", "Baixa maturidade de qualidade"]
    ]
    
    # Atualizar aba de Resumo usando openpyxl
    from openpyxl import load_workbook
    from openpyxl.styles import Alignment
    
    wb = load_workbook(output_path)
    ws = wb["Resumo"]
    
    # Remover células mescladas na área onde vamos escrever
    merged_cells = list(ws.merged_cells.ranges)
    for merged_range in merged_cells:
        # Verificar se a mesclagem está na área que vamos usar (linhas 6-15)
        if merged_range.min_row >= 6:
            ws.unmerge_cells(str(merged_range))
    
    # Encontrar a primeira linha vazia após o cabeçalho
    start_row = 6  # Começar após o cabeçalho existente
    
    for i, row_data in enumerate(resumo_data):
        for j, value in enumerate(row_data):
            cell = ws.cell(row=start_row + i, column=j + 1, value=value)
            cell.alignment = Alignment(wrap_text=True)
    
    wb.save(output_path)
    wb.close()

if __name__ == "__main__":
    print("Carregando dados do DOCX...")
    docx_data = load_docx_data(docx_json_path)
    
    print("Criando dados estruturados...")
    mobilize_data = create_mobilize_data(docx_data)
    
    print("Preenchendo formulário Excel...")
    fill_excel_form(mobilize_data, form_path, output_path)
    
    print("\n=== RESUMO DO PREENCHIMENTO ===")
    print(f"Documentos cadastrados: {len(mobilize_data['avaliacao'])}")
    print(f"Indicadores cadastrados: {len(mobilize_data['indicadores'])}")
    print(f"Treinamentos cadastrados: {len(mobilize_data['treinamento'])}")
    print(f"Monitorias cadastradas: {len(mobilize_data['qualidade'])}")
    print(f"\nArquivo salvo: {output_path}")