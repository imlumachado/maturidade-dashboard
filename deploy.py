#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de preparação para deploy no Streamlit Community Cloud."""

import os
import shutil
from pathlib import Path

def preparar_deploy():
    """Preparar arquivos para deploy no Streamlit Cloud."""
    
    print("=== PREPARAÇÃO PARA DEPLOY ===")
    
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = [
        "app.py",
        "requirements.txt",
        "formulario/F.O.091.GOCO - Analise de Maturidade em Processos.xlsx",
        "formulario/F.O.091.GOCO - Analise de Maturidade em Processos - Mobilize.xlsx",
        ".streamlit/config.toml"
    ]
    
    print("\n1. Verificando arquivos necessários...")
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"  [OK] {arquivo}")
        else:
            print(f"  [ERRO] {arquivo} - ARQUIVO AUSENTE!")
            return False
    
    # Verificar se o requirements.txt está completo
    print("\n2. Verificando dependências...")
    with open("requirements.txt", "r") as f:
        dependencias = f.read()
    
    dependencias_necessarias = [
        "streamlit",
        "pandas",
        "plotly",
        "openpyxl"
    ]
    
    for dep in dependencias_necessarias:
        if dep in dependencias:
            print(f"  [OK] {dep}")
        else:
            print(f"  [ERRO] {dep} - DEPENDÊNCIA AUSENTE!")
            return False
    
    # Criar arquivo de instruções para deploy
    print("\n3. Criando instruções de deploy...")
    instrucoes = """# Instruções para Deploy no Streamlit Community Cloud

## Pré-requisitos
1. Conta no GitHub
2. Repositório público no GitHub com este código
3. Conta no Streamlit Community Cloud (https://streamlit.io/cloud)

## Passos para Deploy

### 1. Preparar o Repositório
```bash
# Inicializar repositório Git (se ainda não inicializado)
git init

# Adicionar todos os arquivos
git add .

# Commitar as alterações
git commit -m "Preparar para deploy no Streamlit Cloud"

# Adicionar repositório remoto (substitua pelo seu)
git remote add origin https://github.com/SEU_USUARIO/maturidade-dashboard.git

# Enviar para o GitHub
git push -u origin main
```

### 2. Configurar no Streamlit Cloud
1. Acesse https://streamlit.io/cloud
2. Clique em "New app"
3. Conecte seu repositório GitHub
4. Configure:
   - **Repository**: maturidade-dashboard
   - **Branch**: main
   - **Main file path**: app.py
5. Clique em "Deploy"

### 3. Configurações Adicionais (opcional)
- Se precisar de variáveis de ambiente, configure em "Advanced settings"
- O app será acessível via URL pública do Streamlit

## Arquivos Importantes
- `app.py`: Arquivo principal do dashboard
- `formulario/`: Pasta com os formulários Excel (fontes de dados)
- `requirements.txt`: Dependências do projeto
- `.streamlit/config.toml`: Configurações do Streamlit

## Notas
- Os arquivos Excel na pasta `formulario/` serão carregados automaticamente
- O dashboard suporta múltiplos formulários de avaliação
- Para atualizar dados, basta enviar novos arquivos Excel para a pasta `formulario/`
"""
    
    with open("DEPLOY_INSTRUCOES.md", "w", encoding="utf-8") as f:
        f.write(instrucoes)
    
    print("  [OK] DEPLOY_INSTRUCOES.md criado")
    
    # Verificar se há arquivos grandes que não devem ser enviados
    print("\n4. Verificando arquivos grandes...")
    arquivos_grandes = []
    for root, dirs, files in os.walk("."):
        # Ignorar pasta .venv e __pycache__
        dirs[:] = [d for d in dirs if d not in [".venv", "__pycache__", ".git", ".pytest_cache"]]
        
        for file in files:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)
            if size > 10 * 1024 * 1024:  # 10MB
                arquivos_grandes.append((filepath, size / (1024 * 1024)))
    
    if arquivos_grandes:
        print("  [AVISO] Arquivos grandes encontrados:")
        for filepath, size_mb in arquivos_grandes:
            print(f"    - {filepath}: {size_mb:.2f} MB")
    else:
        print("  [OK] Nenhum arquivo maior que 10MB encontrado")
    
    print("\n=== PREPARAÇÃO CONCLUÍDA ===")
    print("\nPróximos passos:")
    print("1. Verifique se todos os arquivos estão no repositório Git")
    print("2. Siga as instruções em DEPLOY_INSTRUCOES.md")
    print("3. Acesse https://streamlit.io/cloud para fazer o deploy")
    
    return True

if __name__ == "__main__":
    preparar_deploy()