# Guia de Montagem — Dashboard de Análise de Maturidade (Power BI)

Guia completo para implementar o dashboard **Análise de Maturidade em Processos** no Power BI Desktop, substituindo a versão em Looker Studio.

**Estrutura da pasta do projeto:**
```
maturidade-dashboard/
├── formulario/
│   ├── adicionar_plano_acao.py        # Gera o formulário com colunas de Plano de Ação
│   └── F_O_025_Formulario_Maturidade_Planos.xlsx   # FONTE DE DADOS oficial
├── powerquery/
│   └── modelo_dados.m                 # 11 consultas Power Query (Fase 1)
├── daex/
│   └── medidas.dax                    # Medidas DAX (Fase 2)
└── GUIA_MONTAGEM.md                   # Este arquivo
```

---

## 1. Visão geral do modelo

- **3 frentes de maturidade:** Documentação, Indicadores e Treinamento.
- Cada linha do formulário (documento/indicador/treinamento) recebe um **Score de 0 a 100**.
- Perguntas SIM/NÃO → **1/0** · Conformidade → **1** · Conformidade Pontual / Não Conformidade → **0** · Não Conformidade Grave → **−1 (debita pontos)**.
- **Score da operação por frente = MÉDIA das linhas** da operação.
- **Score Final da Operação = MÉDIA dos 3 scores** das frentes avaliadas (nunca passa de 100; frente sem avaliação não entra).
- **Faixas de maturidade:** 0–25 Baixíssima · 26–35 Baixa · 36–75 Intermediária · 76–85 Boa · 86–100 Excelente.
- **Plano de Ação:** colunas dentro do próprio formulário (`Plano de Ação`, `Responsável`, `Prazo`, `Status da Ação`), com o objetivo de calibrar a operação na próxima análise.

---

## 2. Fase 1 — ETL e modelagem (Power Query)

### 2.1 Preparar o formulário (uma vez)
Execute o script para gerar a cópia do formulário com as colunas de Plano de Ação:
```
python "C:\Users\User\maturidade-dashboard\formulario\adicionar_plano_acao.py"
```
Gera `formulario\F_O_025_Formulario_Maturidade_Planos.xlsx` (a fonte de dados). Execute novamente se o formulário original mudar.

### 2.2 Carregar as consultas

#### Ordem obrigatória
As consultas dependem umas das outras. Crie na exata ordem abaixo; se criar na ordem errada, a consulta exibirá erro `The name 'fn_SimNao' wasn't recognized` (ou similar) até as dependências existirem:

1. **Funções:** `fn_SimNao`, `fn_Conformidade`, `fn_AtualizacaoIndicador`
2. **Fatos:** `Documentacao`, `Indicadores`, `Treinamento`
3. **Dimensões e PlanoAcao:** `Operacao`, `Processo`, `Calendario`, `FaixasMaturidade`, `PlanoAcao`

> `Calendario` e `FaixasMaturidade` são independentes — podem ser criadas a qualquer momento.

#### Passo a passo (repita para cada consulta)
1. **Início > Obter Dados > Consulta em branco** — o **Editor do Power Query** abre já com uma consulta em branco selecionada.
2. Clique com o botão direito na consulta (ex.: `Query1`) > **Editor Avançado**.
3. Apague **todo** o conteúdo e cole **apenas um** bloco do arquivo `powerquery\modelo_dados.m` — do comentário `// Consulta: Xxx` até a linha `in`. Não cole os blocos vizinhos (o comentário do bloco pode ser colado junto como referência, sem problema).
4. Clique em **Concluído**. O Power BI valida a sintaxe; se houver erro, confira se copiou o bloco inteiro e apenas um.
5. **Renomeie** a consulta: no painel **Consultas** (à esquerda), botão direito > **Renomear** (ou edite o campo **Nome** em **Configurações de Consulta**). O nome deve ser **exatamente** o da tabela abaixo (ex.: `fn_SimNao`, não `fn_SimNao_2`).
6. Confirme o resultado: funções aparecem com ícone `fx`; tabelas com ícone de tabela, no painel Consultas.
7. Repita até criar as 11 consultas.

#### Dicas importantes
- **Funções primeiro, sempre.** `Documentacao`, `Indicadores` e `Treinamento` chamam `fn_SimNao`, `fn_Conformidade` e `fn_AtualizacaoIndicador` — se a função não existir com o nome exato, a consulta retorna erro de "nome não reconhecido".
- **O formulário deve existir no caminho exato** da variável `Caminho` (primeira linha de cada consulta de fato). Se o arquivo for movido/renomeado, ajuste `Caminho` em `Documentacao`, `Indicadores` e `Treinamento`.
- Ao criar `Documentacao`/`Indicadores`/`Treinamento`, o Power BI pode pedir a localização da **fonte de dados** e exibir o aviso de **firewall de privacidade** — em ambiente local é aceitável escolher "Ignorar níveis de privacidade".
- **Funções não carregam para o modelo**: ficam apenas no editor, com ícone `fx`. Não é preciso desmarcar "Habilitar carregamento".
- **Dimensões dependem dos nomes exatos** das consultas `Documentacao`, `Indicadores` e `Treinamento` — não as renomeie depois de criar `Operacao`/`Processo`/`PlanoAcao`.
- Ao final, clique em **Fechar e Aplicar**. As tabelas carregadas aparecem em **Dados**. Depois, vá à aba **Modelo** e crie os relacionamentos (seção 2.3).

#### Consultas (nomes exatos)
| Consulta | Tipo | Depende de | Criação |
|---|---|---|---|
| `fn_SimNao` | função | — | 1ª |
| `fn_Conformidade` | função | — | 1ª |
| `fn_AtualizacaoIndicador` | função | — | 1ª |
| `Documentacao` | fato | formulário (aba Avaliação) + 3 funções | 2ª |
| `Indicadores` | fato | formulário (aba Indicadores) + 3 funções | 2ª |
| `Treinamento` | fato | formulário (aba Treinamento) + 3 funções | 2ª |
| `Operacao` | dimensão | `Documentacao`, `Indicadores`, `Treinamento` | 3ª |
| `Processo` | dimensão | `Documentacao`, `Indicadores`, `Treinamento` | 3ª |
| `Calendario` | dimensão | — | a qualquer momento |
| `FaixasMaturidade` | dimensão | — | a qualquer momento |
| `PlanoAcao` | fato | `Documentacao`, `Indicadores`, `Treinamento` | 3ª |

> Se mover o formulário, ajuste a variável `Caminho` em cada consulta de fato.

### 2.3 Relacionamentos (aba Modelo)
Criar:
- `Calendario[Data]` → `Documentacao[Data da avaliação]` (1:N)
- `Calendario[Data]` → `Indicadores[Data da avaliação]` (1:N)
- `Calendario[Data]` → `Treinamento[Data da avaliação]` (1:N)
- `Operacao[Operação]` → `Documentacao[Operação]` (1:N)
- `Operacao[Operação]` → `Indicadores[Operação]` (1:N)
- `Operacao[Operação]` → `Treinamento[Operação]` (1:N)
- `Processo[ID Processo]` → `Documentacao[ID Processo]` (1:N, criar coluna `ID Processo = [Operação] & " | " & [Processo avaliado]` nas fatos)
- `Processo[ID Processo]` → `Indicadores[ID Processo]` (1:N)
- `Processo[ID Processo]` → `Treinamento[ID Processo]` (1:N)

---

## 3. Fase 2 — Medidas DAX

Criar as medidas do arquivo `daex\medidas.dax` (Modelo > Nova medida). Recomendado: criar uma tabela vazia chamada `Medidas` (`ROW("Controle", 1)`, ocultar) e depositar as medidas lá.

### Resumo das medidas
| Grupo | Medidas |
|---|---|
| **Scores** | `Score Documentação`, `Score Indicadores`, `Score Treinamento` |
| **Final** | `Score Final Operação` (MÉDIA dos 3, ≤100), `Faixa de Maturidade`, `Classificação da Operação` |
| **Contadores** | `Documentos/Indicadores/Treinamentos Avaliados` e variantes (Existentes, Atualizados, Padrão, Conformes) + `%` de cada |
| **Sub-scores** | `Score Existência/Atualização/Padrão/Conformidade (Doc/Ind)` e `Score Coerência/Aplicação/Atualização/Conformidade (Tre)` — **identificam fraquezas** |
| **Fraquezas** | `Graves`, `Não Conformes`, `Conformes`, `Itens Negativos`, `% Graves` por frente |
| **Evolução** | `Data Última/Primeira Avaliação`, `Dias desde a Última Avaliação`, `Score Final Último Ciclo`, `Score Final Ciclo Anterior`, `Variação vs Ciclo Anterior`, `Evolução` |
| **Plano de Ação** | `Ações de Plano de Ação`, `Abertas`, `Em Andamento`, `Concluídas`, `Vencidas`, `A Vencer (30 dias)`, `% Concluídas` |
| **Visão Geral** | `Itens Avaliados Total`, `Operações Avaliadas`, `Graves Total`, `Não Conformes Total`, `Itens Negativos Total` |

> Importante: `Score Final Último Ciclo` ignora filtros de data (usa o ciclo mais recente de cada operação). Para ver a evolução no tempo, use `Score Final Operação` com `Calendario[Data]` no eixo.

---

## 4. Fase 3 — Visuais e layout

### 4.1 Identidade visual
- Verde DBM `#02DE81` · Preto `#212121` · Cinza de fundo `#F2F2F2`.
- Cores das faixas (cards e formatação condicional):
  - Baixíssima `#E23C3C` · Baixa `#F59E0B` · Intermediária `#FACC15` · Boa `#34D399` · Excelente `#02DE81`.

### 4.2 Slicers globais
- **Operação** (lista suspensa) · **Data da avaliação** (intervalo). Usar o filtro de data para análises de um ciclo específico.

### 4.3 Páginas e visuais

#### Página 1 — Visão Geral
| Visual | Campos |
|---|---|
| Cards KPI | `Score Final Último Ciclo` (com `Faixa de Maturidade` abaixo), `Operações Avaliadas`, `Ações Vencidas` |
| Cards de alerta | `Itens Avaliados Total`, `Graves Total`, `Não Conformes Total`, `Itens Negativos Total` |
| Colunas agrupadas | Eixo = `Operacao[Operação]` · Valores = `Score Documentação`, `Score Indicadores`, `Score Treinamento` |
| Gauge | `Score Final Último Ciclo` (máx. 100) com bandas por faixa |
| Tabela | `Operação`, `Score Final Último Ciclo`, `Faixa de Maturidade`, `Variação vs Ciclo Anterior`, `Evolução` |

#### Página 2 — Documentação
| Visual | Campos |
|---|---|
| Cards KPI | `Documentos Avaliados`, `% Existência Doc`, `% Atualização Doc`, `% Padrão Doc`, `% Conformidade Doc`, `Graves (Documentação)` |
| Matriz (drill) | Linha = `Operacao[Operação]` → drill `Processo avaliado` · Valor = `Score Documentação` |
| Colunas | `Operação` × `Score Documentação` (decrescente) |
| Linha | `Operação` × `Score Existência/Atualização/Padrão/Conformidade (Doc)` |
| Tabela detalhe | `Nome_Documento`, `Operação`, `Processo avaliado`, `Existe?`, `Está atualizado?`, `Padronizado?`, `Conforme?`, `ScoreLinha`, `Observação` |

#### Página 3 — Indicadores
- KPIs: `Indicadores Avaliados`, `% Existência Ind`, `% Padrão Ind`, `% Conformidade Ind`, `% Graves (Indicadores)`
- Colunas `Operação` × `Score Indicadores` · Linha sub-scores `(Ind)` · Tabela detalhe (`Nome_Indicador`, `Existe indicador?`, `Como é atualizado?`, `No padrão?`, `Conforme?`, `ScoreLinha`)

#### Página 4 — Treinamento
- KPIs: `Treinamentos Avaliados`, `% Coerência Tre`, `% Aplicação Tre`, `% Atualização Tre`, `% Conformidade Tre`, `% Graves (Treinamento)`
- Colunas `Operação` × `Score Treinamento` · Linha sub-scores `(Tre)` · Tabela detalhe (`Nome_Treinamento`, coerência/aplicação/atualização, `Conforme?`, `ScoreLinha`)

#### Página 5 — Evolução
| Visual | Campos |
|---|---|
| Linha | Eixo = `Calendario[Data]` · Valor = `Score Final Operação` · Legenda = `Operação` |
| Matriz | Linha = `Operação` · Colunas = `Score Final Ciclo Anterior` \| `Score Final Último Ciclo` \| `Variação vs Ciclo Anterior` \| `Evolução` |
| Área | `Calendario[Data]` × `Score Final Último Ciclo` |

#### Página 6 — Plano de Ação
| Visual | Campos |
|---|---|
| Cards KPI | `Ações de Plano de Ação`, `Ações Abertas`, `Ações Em Andamento`, `Ações Concluídas`, `Ações Vencidas`, `% Ações Concluídas` |
| Tabela | `Operação`, `Frente`, `Item`, `Plano de Ação`, `Responsável`, `Prazo`, `Status da Ação` |
| Colunas | `Status da Ação` × `Ações de Plano de Ação` |
| Anel | `Frente` × `Ações de Plano de Ação` |
| Slicers | `Status da Ação`, `Responsável` |

### 4.4 Formatação condicional
- **Scores em matriz/tabela:** gradiente `#02DE81` (alto) → `#FACC15` (médio) → `#E23C3C` (baixo/negativo).
- **Evolução:** ▲ = verde, ▼ = vermelho, ➖ = cinza.
- **Plano de Ação:** `Prazo` vencido = vermelho; `Status` Concluído = verde, Aberto = vermelho, Em andamento = amarelo.

---

## 5. Fase 4 — Validação (checklist)

1. Conferir os scores do Power BI contra a aba **Resumo** do formulário (fonte de verdade).
2. Validar o cálculo do score de uma linha conhecida manualmente (ex.: 1,1,1,−1 → 50).
3. Conferir score por operação (MÉDIA das linhas) e score final (MÉDIA das frentes avaliadas).
4. Testar filtros de Operação e Data em todas as páginas.
5. Testar drill-down de Operação → Processo.
6. Confirmar que linhas de exemplo (`Exemplo (apagar)`) não aparecem.

---

## 6. Manutenção e publicação

- **Alimentação:** preencher o formulário `F_O_025_Formulario_Maturidade_Planos.xlsx` gradualmente (1 linha por documento/indicador/treinamento). Preencher `Plano de Ação`, `Responsável`, `Prazo`, `Status da Ação` para os itens que precisam de ação.
- **Atualização no Power BI:** botão **Atualizar** (ou refresh agendado no Power BI Service). Se o arquivo for local, instalar/usar o **Gateway**.
- **Publicação:** Publicar no Power BI Service e criar um App para o time. Se houver necessidade de segregação por operação, configurar **RLS**.
- **Novo ciclo:** ao fazer uma nova análise (nova data de avaliação), o Power BI passa a mostrar automaticamente a evolução entre ciclos na Página 5.