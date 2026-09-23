#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para enviar alterações para o GitHub."""

import subprocess
import sys

def executar_comando(comando):
    """Executar um comando e retornar o resultado."""
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

def main():
    """Enviar alterações para o GitHub."""
    
    print("=== ENVIO PARA O GITHUB ===")
    
    # Verificar se há alterações para enviar
    sucesso, stdout, stderr = executar_comando("git status")
    if not sucesso:
        print("Erro ao verificar status do Git")
        return False
    
    if "nothing to commit" in stdout and "working tree clean" in stdout:
        print("Nenhuma alteração pendente para enviar")
        print("Verificando se há commits para enviar...")
        
        sucesso, stdout, stderr = executar_comando("git log origin/main..HEAD --oneline")
        if sucesso and stdout.strip():
            print(f"Commits para enviar:\n{stdout}")
        else:
            print("Todos os commits já foram enviados")
            return True
    
    # Enviar para o GitHub
    print("\nEnviando alterações para o GitHub...")
    sucesso, stdout, stderr = executar_comando("git push origin main")
    
    if sucesso:
        print("[OK] Alterações enviadas com sucesso!")
        print(stdout)
        return True
    else:
        print("[ERRO] Falha ao enviar alterações:")
        print(stderr)
        
        # Tentar fazer pull primeiro
        print("\nTentando fazer pull das alterações remotas...")
        sucesso_pull, stdout_pull, stderr_pull = executar_comando("git pull origin main --rebase")
        
        if sucesso_pull:
            print("[OK] Pull realizado com sucesso")
            print(stdout_pull)
            
            # Tentar enviar novamente
            print("\nTentando enviar novamente...")
            sucesso2, stdout2, stderr2 = executar_comando("git push origin main")
            
            if sucesso2:
                print("[OK] Alterações enviadas com sucesso!")
                print(stdout2)
                return True
            else:
                print("[ERRO] Falha ao enviar após pull:")
                print(stderr2)
        else:
            print("[ERRO] Falha ao fazer pull:")
            print(stderr_pull)
        
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)