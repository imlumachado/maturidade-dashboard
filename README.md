# Análise de Maturidade em Processos

Dashboard interativo para avaliação de maturidade organizacional, construído com Streamlit.

## Visão Geral

O dashboard acompanha quatro frentes de avaliação:

- **Documentação** — existência, atualização, padronização e conformidade de documentos
- **Indicadores** — existência, padrão e conformidade de indicadores
- **Treinamento** — coerência, aplicação, atualização e conformidade de treinamentos
- **Qualidade** — monitorias de qualidade

Cada frente gera um score de 0 a 100 por operação. O **Score Final** é a média das frentes avaliadas, classificado em faixas de maturidade (Baixíssima a Excelente).

## Estrutura

```
app.py                  # Página principal (Visão Geral)
common.py               # Filtros e carga de dados
data_loader.py          # ETL — leitura do Excel
metrics.py              # Cálculos e indicadores
theme.py                # Paleta de cores
ui.py                   # Componentes de interface
pagina_frente.py        # Layout reutilizável por frente
pages/
  1_Documentação.py
  2_Indicadores.py
  3_Treinamento.py
  4_Evolução.py
  5_Plano_de_ação.py
  6_Qualidade.py
formulario/
  F_O_025_...xlsx       # Fonte de dados
tests/
  test_metricas.py
  test_filtros.py
  test_paginas.py
```

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Stack

- Python 3.11+
- Streamlit 1.61
- Pandas 3.0
- Plotly 6.9
- openpyxl 3.1
