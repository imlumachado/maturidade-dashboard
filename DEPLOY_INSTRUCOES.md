# Instruções para Deploy no Streamlit Community Cloud

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
