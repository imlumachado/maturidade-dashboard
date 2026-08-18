# Plano de Trabalho — Dashboard de Maturidade em Streamlit

Replicar o dashboard "Análise de Maturidade em Processos" (hoje previsto no Power BI) como um app **Streamlit**, usando o mesmo formulário Excel como fonte de dados. O objetivo é ter uma versão navegável para **apresentação** antes de finalizar a montagem no Power BI.

---

## 1. Objetivo e escopo

- Ler `formulario\F_O_025_Formulario_Maturidade_Planos.xlsx` (abas `Avaliação`, `Indicadores`, `Treinamento`).
- Replicar em Python/pandas as transformações das consultas Power Query (`powerquery\modelo_dados.m`).
- Replicar em Python os cálculos das medidas DAX (`daex\medidas.dax`).
- Entregar 6 páginas equivalentes às do Power BI: **Visão Geral, Documentação, Indicadores, Treinamento, Evolução, Plano de Ação**.
- Filtros globais: **Operação** e **Data da avaliação** (sidebar).
- Identidade visual do guia (verde `#02DE81`, preto `#212121`, cinza `#F2F2F2`, cores das faixas).

Fora do escopo desta 1ª versão: aba `Qualidade` do formulário, RLS/autenticação, edição de dados pelo app (somente leitura).

---

## 2. Stack e pré-requisitos

| Item | Versão sugerida |
|---|---|
| Python | 3.11+ (ambiente local tem 3.13) |
| streamlit | >= 1.40 |
| pandas | >= 2.2 |
| plotly | >= 5.24 (gráficos interativos) |
| openpyxl | >= 3.1 (leitura do xlsx) |

**Ambiente:**
```
python -m venv .venv
.venv\Scripts\activate
pip install streamlit pandas plotly openpyxl
streamlit run streamlit/app.py
```

---

## 3. Fases de desenvolvimento

### Fase 0 — Estrutura e preparação
- Criar `streamlit/` com módulos separados (abaixo) e `requirements.txt`.
- Criar venv e instalar dependências.
- **Critério de aceite:** `streamlit run` abre o app sem erros.

### Fase 1 — Camada de dados (ETL em pandas) → `data_loader.py`
Replicar as 3 funções de conversão e as 3 tabelas fato do Power Query:

| Função | Regra |
|---|---|
| `fn_sim_nao(v)` | SIM → 1 · NÃO → 0 · resto → NaN |
| `fn_conformidade(v)` | Conformidade → 1 · Pontual/Não conforme → 0 · Grave → −1 · resto → NaN |
| `fn_atualizacao(v)` | Automático → 1 · Manual → 0.5 · Não atualizado → 0 · resto → NaN |

Por aba (tabelas `Documentacao`, `Indicadores`, `Treinamento`):
- Ler Excel; descartar linhas sem `Data da avaliação`; limpar `Operação`/`Processo avaliado` (trim) e excluir `""` e `Exemplo (apagar)`.
- Criar colunas `Frente`, `Sub Existência/Atualização/Padrão/Conformidade` (nomes por frente) e **`ScoreLinha`** = média dos sub-scores não nulos × 100, arredondado (`1,1,1,−1 → 50`).
- `PlanoAcao` = linhas das 3 frentes com `Plano de Ação` não vazio (colunas: Operação, Processo, Frente, Item, Plano de Ação, Responsável, Prazo, Status).

- **Critério de aceite:** teste rápido confere `ScoreLinha` manual (ex. `1,1,1,−1 → 50`) e totais por aba.

### Fase 2 — Camada de cálculo (medidas) → `metrics.py`
Funções puras que recebem os DataFrames + filtros (operação, data) e devolvem valores. Replicam o DAX:

- **Scores por frente:** média de `ScoreLinha` de `Documentacao`/`Indicadores`/`Treinamento`.
- **Score Final Operação:** média das 3 frentes avaliadas (frente sem dados não entra).
- **Faixa de Maturidade:** 0–25 Baixíssima · 26–35 Baixa · 36–75 Intermediária · 76–85 Boa · 86–100 Excelente.
- **Contadores e %:** avaliados/existentes/atualizados/padrão/conformes por frente e os `%` correspondentes.
- **Sub-scores:** média de cada sub-score × 100 (para achar fraquezas).
- **Fraquezas:** Graves (Sub Conformidade = −1), Não Conformes (= 0), Conformes (= 1), Itens Negativos (ScoreLinha < 0), `% Graves`.
- **Evolução (por operação):** Data última avaliação, Data primeira, `Score Final Último Ciclo` (só linhas da data mais recente), `Score Final Ciclo Anterior`, `Variação`, `Evolução` (▲ Melhorou / ▼ Piorou / ➖ Estável).
- **Plano de Ação:** total, Abertas, Em Andamento, Concluídas, **Vencidas** (Prazo < hoje e ≠ Concluído), **A Vencer (30 dias)**, `% Concluídas`.
- **Visão geral:** Itens Avaliados Total, Operações Avaliadas, Graves/Não Conformes/Itens Negativos Total.

- **Critério de aceite:** uma bateria de testes (`tests/test_metricas.py`) valida cada grupo contra valores calculados à mão e contra a aba `Resumo` do formulário.

### Fase 3 — Interface (páginas) → `app.py` + `pages/`
- `app.py`: sidebar com filtros de **Operação** (multiselect) e **Data** (date_input range) + navegação; aplica filtros nos DataFrames antes de calcular.
- Páginas equivalentes ao guia (4.3):
  1. **Visão Geral** — cards KPI (Score Final Último Ciclo + Faixa, Operações Avaliadas, Ações Vencidas), cards de alerta (Itens/Graves/Não Conformes/Negativos), barras agrupadas por operação (3 frentes), tabela de ranking com variação/evolução.
  2. **Documentação** — KPIs e % (existência/atualização/padrão/conformidade), barras por operação, linha de sub-scores, tabela detalhe.
  3. **Indicadores** — idem com campos da aba Indicadores.
  4. **Treinamento** — idem com campos da aba Treinamento.
  5. **Evolução** — linha `Score Final Operação` ao longo das datas por operação; tabela Último Ciclo × Ciclo Anterior × Variação × Evolução.
  6. **Plano de Ação** — cards, tabela detalhe, barras por status, anel por frente, filtros de Status/Responsável.
- Reuso de um módulo `ui.py` com helpers de card e gráfico (cores padronizadas).

### Fase 4 — Identidade visual e formatação
- Paleta única em `theme.py`; cores das faixas para cards/formatação.
- Formatação condicional: scores em gradiente verde→amarelo→vermelho; plano de ação (Prazo vencido vermelho; status coloridos).

### Fase 5 — Validação (checklist)
1. Scores do app conferem com a aba **Resumo** do formulário.
2. Linha conhecida manualmente (ex. `1,1,1,−1 → 50`).
3. Score por operação (média das linhas) e final (média das frentes).
4. Filtros de Operação e Data funcionam em todas as páginas.
5. Linhas `Exemplo (apagar)` não aparecem.
6. Plano de ação: vencidas/a vencer calculadas contra a data de hoje.

### Fase 6 — Apresentação
- Executar local: `streamlit run streamlit/app.py` (opcional `--server.headless true`).
- (Opcional) publicar no **Streamlit Community Cloud** conectando o repositório Git e subindo o xlsx junto (o arquivo já é fonte fixa no repositório).

---

## 4. Estrutura de arquivos (alvo)

```
maturidade-dashboard/
├── formulario/
│   └── F_O_025_Formulario_Maturidade_Planos.xlsx   # fonte de dados
├── streamlit/
│   ├── app.py                  # entrada: filtros globais + navegação
│   ├── data_loader.py          # leitura do Excel + ETL (Fase 1)
│   ├── metrics.py              # cálculos/medidas (Fase 2)
│   ├── ui.py                   # helpers de cards/gráficos/cores
│   ├── theme.py                # paleta e estilos
│   └── pages/
│       ├── visao_geral.py
│       ├── documentacao.py
│       ├── indicadores.py
│       ├── treinamento.py
│       ├── evolucao.py
│       └── plano_acao.py
├── tests/
│   └── test_metricas.py        # validação das medidas
└── requirements.txt
```

---

## 5. Ordem de execução e entregáveis

| # | Fase | Entregável | Ordem |
|---|---|---|---|
| 1 | Fase 0 | ambiente rodando | 1ª |
| 2 | Fase 1 | `data_loader.py` + 3 tabelas + PlanoAcao | 2ª |
| 3 | Fase 2 | `metrics.py` + testes | 3ª |
| 4 | Fase 3 | 6 páginas navegáveis | 4ª |
| 5 | Fase 4 | visual/cores/formatação | 5ª |
| 6 | Fase 5 | checklist validado | 6ª |
| 7 | Fase 6 | app pronto para apresentação | 7ª |

> Decisão a confirmar: publicar no **Streamlit Community Cloud** (requer conta e repositório Git) ou apresentar **localmente** apenas.
