// ============================================================================
//  MODELO DE DADOS — ANÁLISE DE MATURIDADE EM POWER BI
//  Fase 1 (ETL / Modelagem) — Power Query M
// ----------------------------------------------------------------------------
//  COMO APLICAR NO POWER BI DESKTOP:
//  1. Abra o Power BI Desktop > "Obter Dados" > "Consulta em branco".
//  2. No "Editor Avançado", apague tudo e cole UMA das consultas abaixo.
//  3. Renomeie a consulta com o nome indicado no comentário de cada bloco.
//  4. Repita para cada bloco (as funções fn_* primeiro).
//  5. Em "Modelo", crie os relacionamentos (diagrama no rodapé deste arquivo).
//
//  FONTE DE DADOS: o formulário gerado por
//  formulario/adicionar_plano_acao.py (F_O_025_Formulario_Maturidade_Planos.xlsx).
// ============================================================================



// ============================================================================
// Consulta: fn_SimNao
// Converte SIM/NÃO em 1/0. Qualquer outro valor vira nulo (não pontua).
// ============================================================================
(v) =>
    let t = Text.Upper(Text.Trim(Text.From(v)))
    in if t = "SIM" then 1 else if t = "NÃO" then 0 else null



// ============================================================================
// Consulta: fn_Conformidade
// Conformidade = 1 | Conformidade Pontual / Não Conformidade = 0
// Não Conformidade Grave = -1 (DEBITA pontos) | demais valores = nulo
// ============================================================================
(v) =>
    let t = Text.Upper(Text.Trim(Text.From(v)))
    in if t = "CONFORMIDADE" then 1
       else if t = "CONFORMIDADE PONTUAL" then 0
       else if t = "NÃO CONFORMIDADE" then 0
       else if t = "NÃO CONFORMIDADE GRAVE" then -1
       else null



// ============================================================================
// Consulta: fn_AtualizacaoIndicador
// Automático = 1 | Manual = 0.5 | Não atualizado = 0
// ============================================================================
(v) =>
    let t = Text.Upper(Text.Trim(Text.From(v)))
    in if t = "AUTOMÁTICO" then 1
       else if t = "MANUAL" then 0.5
       else if t = "NÃO ATUALIZADO" then 0
       else null



// ============================================================================
// Consulta: Documentacao
// Aba "Avaliação" do formulário. Score por linha = MÉDIA(sub-scores) x 100.
// ============================================================================
let
    Caminho = "C:\\Users\\User\\maturidade-dashboard\\formulario\\F_O_025_Formulario_Maturidade_Planos.xlsx",
    Fonte = Excel.Workbook(File.Contents(Caminho), true),
    Aba = Fonte{[Name = "Avaliação"]}[Data],
    Tipos = Table.TransformColumnTypes(Aba, {
        {"Data da avaliação", type date},
        {"Quantidade", Int64.Type},
        {"Última atualização", type date},
        {"Prazo", type date}
    }),
    Filtro = Table.SelectRows(Tipos, each [Data da avaliação] <> null),
    Operacao = Table.TransformColumns(Filtro, {{"Operação", each Text.Trim(Text.From(_)), type text}}),
    Processo = Table.TransformColumns(Operacao, {{"Processo avaliado", each Text.Trim(Text.From(_)), type text}}),
    Limpeza = Table.SelectRows(Processo, each [Operação] <> "" and [Operação] <> "Exemplo (apagar)"),
    Frente = Table.AddColumn(Limpeza, "Frente", each "Documentação", type text),
    S1 = Table.AddColumn(Frente, "Sub Existência", each fn_SimNao([Existe?]), type number),
    S2 = Table.AddColumn(S1, "Sub Atualização", each fn_SimNao([Está atualizado?]), type number),
    S3 = Table.AddColumn(S2, "Sub Padrão", each fn_SimNao([Padronizado?]), type number),
    S4 = Table.AddColumn(S3, "Sub Conformidade", each fn_Conformidade([Coforme?]), type number),
    Score = Table.AddColumn(S4, "ScoreLinha", each
        let vals = List.RemoveNulls({[Sub Existência], [Sub Atualização], [Sub Padrão], [Sub Conformidade]})
        in if List.IsEmpty(vals) then null else Number.Round(List.Average(vals) * 100, 0, RoundingMode.AwayFromZero),
        type number),
    Sel = Table.SelectColumns(Score, {
        "ID Avaliação", "Data da avaliação", "Operação", "Processo avaliado",
        "Nome_Documento", "Quantidade", "Última atualização",
        "Existe?", "Está atualizado?", "Padronizado?", "Coforme?",
        "Observação",
        "Sub Existência", "Sub Atualização", "Sub Padrão", "Sub Conformidade", "ScoreLinha",
        "Plano de Ação", "Responsável", "Prazo", "Status da Ação"
    }),
    Renomear = Table.RenameColumns(Sel, {{"Coforme?", "Conforme?"}})
in
    Renomear



// ============================================================================
// Consulta: Indicadores
// Aba "Indicadores". Atualização usa escala Automático/Manual/Não atualizado.
// ============================================================================
let
    Caminho = "C:\\Users\\User\\maturidade-dashboard\\formulario\\F_O_025_Formulario_Maturidade_Planos.xlsx",
    Fonte = Excel.Workbook(File.Contents(Caminho), true),
    Aba = Fonte{[Name = "Indicadores"]}[Data],
    Tipos = Table.TransformColumnTypes(Aba, {
        {"Data da avaliação", type date},
        {"Quantidade", Int64.Type},
        {"Prazo", type date}
    }),
    Filtro = Table.SelectRows(Tipos, each [Data da avaliação] <> null),
    Operacao = Table.TransformColumns(Filtro, {{"Operação", each Text.Trim(Text.From(_)), type text}}),
    Processo = Table.TransformColumns(Operacao, {{"Processo avaliado", each Text.Trim(Text.From(_)), type text}}),
    Limpeza = Table.SelectRows(Processo, each [Operação] <> "" and [Operação] <> "Exemplo (apagar)"),
    Frente = Table.AddColumn(Limpeza, "Frente", each "Indicadores", type text),
    S1 = Table.AddColumn(Frente, "Sub Existência", each fn_SimNao([Existe indicador?]), type number),
    S2 = Table.AddColumn(S1, "Sub Atualização", each fn_AtualizacaoIndicador([Como é atualizado?]), type number),
    S3 = Table.AddColumn(S2, "Sub Padrão", each fn_SimNao([No padrão?]), type number),
    S4 = Table.AddColumn(S3, "Sub Conformidade", each fn_Conformidade([Conforme?]), type number),
    Score = Table.AddColumn(S4, "ScoreLinha", each
        let vals = List.RemoveNulls({[Sub Existência], [Sub Atualização], [Sub Padrão], [Sub Conformidade]})
        in if List.IsEmpty(vals) then null else Number.Round(List.Average(vals) * 100, 0, RoundingMode.AwayFromZero),
        type number),
    Sel = Table.SelectColumns(Score, {
        "ID Avaliação", "Data da avaliação", "Operação", "Processo avaliado",
        "Nome_Indicador", "Quantidade",
        "Existe indicador?", "Como é atualizado?", "No padrão?", "Conforme?",
        "Observação",
        "Sub Existência", "Sub Atualização", "Sub Padrão", "Sub Conformidade", "ScoreLinha",
        "Plano de Ação", "Responsável", "Prazo", "Status da Ação"
    })
in
    Sel



// ============================================================================
// Consulta: Treinamento
// Aba "Treinamento". Sub-scores: Coerência, Aplicação, Atualização, Conformidade.
// ============================================================================
let
    Caminho = "C:\\Users\\User\\maturidade-dashboard\\formulario\\F_O_025_Formulario_Maturidade_Planos.xlsx",
    Fonte = Excel.Workbook(File.Contents(Caminho), true),
    Aba = Fonte{[Name = "Treinamento"]}[Data],
    Tipos = Table.TransformColumnTypes(Aba, {
        {"Data da avaliação", type date},
        {"Quantidade", Int64.Type},
        {"Prazo", type date}
    }),
    Filtro = Table.SelectRows(Tipos, each [Data da avaliação] <> null),
    Operacao = Table.TransformColumns(Filtro, {{"Operação", each Text.Trim(Text.From(_)), type text}}),
    Processo = Table.TransformColumns(Operacao, {{"Processo avaliado", each Text.Trim(Text.From(_)), type text}}),
    Limpeza = Table.SelectRows(Processo, each [Operação] <> "" and [Operação] <> "Exemplo (apagar)"),
    Frente = Table.AddColumn(Limpeza, "Frente", each "Treinamento", type text),
    S1 = Table.AddColumn(Frente, "Sub Coerência", each fn_SimNao([Treinamento está coerente aos documentos?]), type number),
    S2 = Table.AddColumn(S1, "Sub Aplicação", each fn_SimNao([Treinamento foi aplicado?]), type number),
    S3 = Table.AddColumn(S2, "Sub Atualização", each fn_SimNao([Houve atualização?]), type number),
    S4 = Table.AddColumn(S3, "Sub Conformidade", each fn_Conformidade([Conforme?]), type number),
    Score = Table.AddColumn(S4, "ScoreLinha", each
        let vals = List.RemoveNulls({[Sub Coerência], [Sub Aplicação], [Sub Atualização], [Sub Conformidade]})
        in if List.IsEmpty(vals) then null else Number.Round(List.Average(vals) * 100, 0, RoundingMode.AwayFromZero),
        type number),
    Sel = Table.SelectColumns(Score, {
        "ID Avaliação", "Data da avaliação", "Operação", "Processo avaliado",
        "Nome_Treinamento", "Quantidade",
        "Treinamento está coerente aos documentos?", "Treinamento foi aplicado?", "Houve atualização?", "Conforme?",
        "Observação",
        "Sub Coerência", "Sub Aplicação", "Sub Atualização", "Sub Conformidade", "ScoreLinha",
        "Plano de Ação", "Responsável", "Prazo", "Status da Ação"
    })
in
    Sel



// ============================================================================
// Consulta: Operacao  (dimensão — lista única de operações)
// ============================================================================
let
    Fonte = Table.Combine({
        Table.SelectColumns(Documentacao, {"Operação"}),
        Table.SelectColumns(Indicadores, {"Operação"}),
        Table.SelectColumns(Treinamento, {"Operação"})
    }),
    Distintos = Table.Distinct(Fonte),
    Ordem = Table.AddIndexColumn(Distintos, "ID Operação", 1, 1, Int64.Type)
in
    Ordem



// ============================================================================
// Consulta: Processo  (dimensão — combinação Operação + Processo)
// ============================================================================
let
    Fonte = Table.Combine({
        Table.SelectColumns(Documentacao, {"Operação", "Processo avaliado"}),
        Table.SelectColumns(Indicadores, {"Operação", "Processo avaliado"}),
        Table.SelectColumns(Treinamento, {"Operação", "Processo avaliado"})
    }),
    Distintos = Table.Distinct(Fonte),
    Chave = Table.AddColumn(Distintos, "ID Processo", each [Operação] & " | " & [Processo avaliado], type text)
in
    Chave



// ============================================================================
// Consulta: Calendario  (tabela de datas — ajuste os anos se necessário)
// ============================================================================
let
    Inicio = #date(2015, 1, 1),
    Fim = #date(2040, 12, 31),
    QuantidadeDias = Duration.Days(Fim - Inicio) + 1,
    Datas = List.Dates(Inicio, QuantidadeDias, #duration(1, 0, 0, 0)),
    Tabela = Table.FromList(Datas, Splitter.SplitByNothing(), {"Data"}, null, ExtraValues.Error),
    Tipos = Table.TransformColumnTypes(Tabela, {{"Data", type date}}),
    Ano = Table.AddColumn(Tipos, "Ano", each Date.Year([Data]), Int64.Type),
    Mes = Table.AddColumn(Ano, "Mês", each Date.Month([Data]), Int64.Type),
    Dia = Table.AddColumn(Mes, "Dia", each Date.Day([Data]), Int64.Type),
    MesNome = Table.AddColumn(Dia, "Mês Nome", each Date.MonthName([Data]), type text),
    Trimestre = Table.AddColumn(MesNome, "Trimestre", each Date.QuarterOfYear([Data]), Int64.Type),
    AnoMes = Table.AddColumn(Trimestre, "Ano-Mês", each Text.PadStart(Text.From([Ano]), 4, "0") & "-" & Text.PadStart(Text.From([Mês]), 2, "0"), type text)
in
    AnoMes



// ============================================================================
// Consulta: FaixasMaturidade  (tabela de faixas para classificação do score)
// ============================================================================
let
    Fonte = #table(
        {"Score Início", "Score Fim", "Classificação"},
        {
            {0, 25, "Baixíssima maturidade"},
            {26, 35, "Baixa maturidade"},
            {36, 75, "Maturidade intermediária"},
            {76, 85, "Boa maturidade"},
            {86, 100, "Excelente maturidade"}
        }
    ),
    Tipos = Table.TransformColumnTypes(Fonte, {
        {"Score Início", Int64.Type},
        {"Score Fim", Int64.Type},
        {"Classificação", type text}
    })
in
    Tipos



// ============================================================================
// Consulta: PlanoAcao
// Linhas das 3 frentes que possuem "Plano de Ação" preenchido.
// ============================================================================
let
    Doc = Table.AddColumn(
        Table.SelectColumns(Documentacao, {"Operação", "Processo avaliado", "Frente", "Nome_Documento", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"}),
        "Item", each [Nome_Documento], type text),
    Ind = Table.AddColumn(
        Table.SelectColumns(Indicadores, {"Operação", "Processo avaliado", "Frente", "Nome_Indicador", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"}),
        "Item", each [Nome_Indicador], type text),
    Tre = Table.AddColumn(
        Table.SelectColumns(Treinamento, {"Operação", "Processo avaliado", "Frente", "Nome_Treinamento", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"}),
        "Item", each [Nome_Treinamento], type text),
    Colunas = {"Operação", "Processo avaliado", "Frente", "Item", "Plano de Ação", "Responsável", "Prazo", "Status da Ação"},
    Uniao = Table.Combine({
        Table.SelectColumns(Doc, Colunas),
        Table.SelectColumns(Ind, Colunas),
        Table.SelectColumns(Tre, Colunas)
    }),
    Filtro = Table.SelectRows(Uniao, each [Plano de Ação] <> null and Text.Trim(Text.From([Plano de Ação])) <> ""),
    Tipos = Table.TransformColumnTypes(Filtro, {{"Prazo", type date}})
in
    Tipos



// ============================================================================
//  RELACIONAMENTOS A CRIAR NO MODELO (aba Modelo):
//
//  Calendario[Data]        1:N  Documentacao[Data da avaliação]
//  Calendario[Data]        1:N  Indicadores[Data da avaliação]
//  Calendario[Data]        1:N  Treinamento[Data da avaliação]
//  Operacao[Operação]      1:N  Documentacao[Operação]
//  Operacao[Operação]      1:N  Indicadores[Operação]
//  Operacao[Operação]      1:N  Treinamento[Operação]
//  Processo[ID Processo]   1:N  Documentacao[ID Processo]   (criar coluna na tabela)
//  Processo[ID Processo]   1:N  Indicadores[ID Processo]    (criar coluna na tabela)
//  Processo[ID Processo]   1:N  Treinamento[ID Processo]    (criar coluna na tabela)
//
//  Dica: as tabelas fato não precisam de relação entre si — as medidas
//  de score final agregam as 3 frentes via dimensões Operacao/Calendario.
// ============================================================================