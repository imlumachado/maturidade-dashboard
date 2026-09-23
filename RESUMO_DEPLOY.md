# Resumo para Deploy no Streamlit Cloud

## Status Atual
- **Repositório Git**: Configurado e atualizado
- **Commit realizado**: "Preparar para deploy no Streamlit Cloud - Dados Mobilize"
- **Dados Mobilize**: Formulário preenchido e pronto para uso

## Arquivos Preparados para Deploy
1. **app.py** - Aplicação principal do Streamlit
2. **data_loader.py** - Carregamento de dados (atualizado para múltiplos formulários)
3. **formulario/** - Pasta com os formulários Excel:
   - `F.O.091.GOCO - Analise de Maturidade em Processos.xlsx` (original)
   - `F.O.091.GOCO - Analise de Maturidade em Processos - Mobilize.xlsx` (novo)
4. **requirements.txt** - Dependências do projeto
5. **.streamlit/config.toml** - Configurações do Streamlit

## Passos para Deploy

### 1. Enviar para o GitHub
```bash
cd C:\Users\User\maturidade-dashboard
git push origin main
```

### 2. Configurar no Streamlit Cloud
1. Acesse https://streamlit.io/cloud
2. Clique em "New app"
3. Conecte o repositório GitHub: `imlumachado/maturidade-dashboard`
4. Configure:
   - **Repository**: maturidade-dashboard
   - **Branch**: main
   - **Main file path**: app.py
5. Clique em "Deploy"

### 3. Acessar o Dashboard
Após o deploy, o dashboard estará acessível via URL pública do Streamlit Cloud.

## Funcionalidades do Dashboard
- **Visão Geral**: Score final, métricas por operação
- **Documentação**: Avaliação de documentos
- **Indicadores**: Análise de indicadores
- **Treinamento**: Avaliação de treinamentos
- **Qualidade**: Monitorias de qualidade
- **Evolução**: Comparativo entre ciclos
- **Plano de Ação**: Ações corretivas

## Dados da Mobilize
O formulário da Mobilize inclui:
- **15 documentos** avaliados
- **10 indicadores** (NS, PCA, TMA, TME, CSAT, FCR, SLA, HC, ABS, TO)
- **3 treinamentos** (Banco N1, Locadora N1, BackOffice N2)
- **3 monitorias** (Portal da Qualidade, Cessão de Direitos, Clube FIQ)

## Notas Importantes
- O dashboard suporta múltiplos formulários de avaliação
- Para adicionar novas avaliações, basta enviar novos arquivos Excel para a pasta `formulario/`
- Os dados são carregados automaticamente ao iniciar o dashboard