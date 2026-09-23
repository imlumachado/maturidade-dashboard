#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para preparar o repositório Git para deploy."""

import subprocess
import os

def executar_comando(comando):
    """Executar um comando Git e retornar o resultado."""
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return resultado.returncode == 0, resultado.stdout, resultado.stderr
    except Exception as e:
        return False, "", str(e)

def preparar_repositorio():
    """Preparar o repositório Git para deploy."""
    
    print("=== PREPARAÇÃO DO REPOSITÓRIO GIT ===")
    
    # Verificar se estamos em um repositório Git
    sucesso, stdout, stderr = executar_comando("git status")
    if not sucesso:
        print("Erro: Não estamos em um repositório Git válido")
        return False
    
    print("\n1. Adicionando arquivos ao staging...")
    comandos_add = [
        "git add app.py",
        "git add data_loader.py",
        "git add requirements.txt",
        "git add .streamlit/",
        "git add formulario/",
        "git add pages/",
        "git add common.py",
        "git add metrics.py",
        "git add theme.py",
        "git add ui.py",
        "git add pagina_frente.py",
        "git add tests/",
        "git add DEPLOY_INSTRUCOES.md",
        "git add deploy.py"
    ]
    
    for comando in comandos_add:
        sucesso, stdout, stderr = executar_comando(comando)
        if sucesso:
            print(f"  [OK] {comando}")
        else:
            print(f"  [AVISO] {comando}: {stderr}")
    
    print("\n2. Verificando status...")
    sucesso, stdout, stderr = executar_comando("git status")
    if sucesso:
        print(stdout)
    
    print("\n3. Criando commit...")
    mensagem_commit = "Preparar para deploy no Streamlit Cloud - Dados Mobilize"
    comando_commit = f'git commit -m "{mensagem_commit}"'
    sucesso, stdout, stderr = executar_comando(comando_commit)
    
    if sucesso:
        print(f"  [OK] Commit realizado: {mensagem_commit}")
        print(stdout)
    else:
        print(f"  [AVISO] Commit: {stderr}")
        # Tentar commit com -a para incluir modificações
        comando_commit_a = f'git commit -a -m "{mensagem_commit}"'
        sucesso, stdout, stderr = executar_comando(comando_commit_a)
        if sucesso:
            print(f"  [OK] Commit realizado com -a: {mensagem_commit}")
        else:
            print(f"  [ERRO] Não foi possível criar commit: {stderr}")
            return False
    
    print("\n4. Verificando repositório remoto...")
    sucesso, stdout, stderr = executar_comando("git remote -v")
    if sucesso and "origin" in stdout:
        print("  [OK] Repositório remoto configurado:")
        print(stdout)
    else:
        print("  [AVISO] Repositório remoto não configurado")
        print("  Para configurar, execute:")
        print("    git remote add origin https://github.com/SEU_USUARIO/maturidade-dashboard.git")
        print("    git push -u origin main")
    
    print("\n=== PREPARAÇÃO CONCLUÍDA ===")
    print("\nPróximos passos:")
    print("1. Verifique se o repositório remoto está configurado")
    print("2. Envie as alterações para o GitHub: git push origin main")
    print("3. Acesse https://streamlit.io/cloud para fazer o deploy")
    
    return True

if __name__ == "__main__":
    preparar_repositorio()