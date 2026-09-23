# -*- coding: utf-8 -*-

from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache
from pathlib import Path

import pandas as pd

PASTA_FORMULARIOS = Path(__file__).resolve().parent / "formulario"
FORMULARIO_PRINCIPAL = PASTA_FORMULARIOS / "F.O.091.GOCO - Analise de Maturidade em Processos.xlsx"

# Lista de todos os formulários Excel na pasta
def obter_formularios():
    """Retorna uma lista com todos os arquivos Excel na pasta de formulários."""
    formularios = list(PASTA_FORMULARIOS.glob("*.xlsx"))
    # Filtrar apenas arquivos que começam com "F.O." e contêm "Analise de Maturidade"
    formularios_filtrados = [
        f for f in formularios 
        if f.name.startswith("F.O.") and "Analise de Maturidade" in f.name
    ]
    return formularios_filtrados

# Para compatibilidade, manter a referência ao formulário principal
FORMULARIO = FORMULARIO_PRINCIPAL

COLUNAS_PLANO = [
    "Operação",
    "Processo avaliado",
    "Frente",
    "Item",
    "Plano de Ação",
    "Responsável",
    "Prazo",
    "Status da Ação",
]

_COLS_BASE = [
    "Operação",
    "Processo avaliado",
    "Data da avaliação",
    "Observação",
    "Plano de Ação",
    "Responsável",
    "Prazo",
    "Status da Ação",
]

def _texto(v):
    if v is None or pd.isna(v):
        return None
    return str(v).strip()


def fn_sim_nao(v):
    t = _texto(v)
    if t is None:
        return None
    t = t.upper()
    if t == "SIM":
        return 1.0
    if t == "NÃO":
        return 0.0
    return None


def fn_conformidade(v):
    t = _texto(v)
    if t is None:
        return None
    t = t.upper()
    if t == "CONFORMIDADE":
        return 1.0
    if t == "CONFORMIDADE PONTUAL":
        return 0.5
    if t in ("NÃO CONFORMIDADE", "NÃO CONFORMIDADE GRAVE"):
        return 0.0
    return None


def fn_atualizacao(v):
    t = _texto(v)
    if t is None:
        return None
    t = t.upper()
    if t == "AUTOMÁTICO":
        return 1.0
    if t == "MANUAL":
        return 0.5
    if t == "NÃO ATUALIZADO":
        return 0.0
    return None


def fn_numerico(v):
    """Aba Qualidade já traz valores numéricos. Converte e normaliza para [0, 1]."""
    if v is None or pd.isna(v):
        return None
    try:
        val = float(v)
        if val < 0:
            return 0.0
        return val
    except (TypeError, ValueError):
        return None


def _fn_na(v):
    """Critério N/A — inaplicabilidade registrada e validada."""
    return None


def _arredondar(v):
    return int(Decimal(str(v)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _score_linha(subs):
    vals = [s for s in subs if s is not None and not pd.isna(s)]
    if not vals:
        return None
    return _arredondar(sum(vals) / len(vals) * 100)


_CONFIG = {
    "Avaliação": {
        "frente": "Documentação",
        "col_item": "Nome_Documento",
        "subs": [
            ("Sub Existência", "Existe?", fn_sim_nao),
            ("Sub Aplicação", None, _fn_na),
            ("Sub Padrão", "Padronizado?", fn_sim_nao),
            ("Sub Conformidade", "Coforme?", fn_conformidade),
            ("Sub Atualização", "Está atualizado?", fn_sim_nao),
        ],
    },
    "Indicadores": {
        "frente": "Indicadores",
        "col_item": "Nome_Indicador",
        "subs": [
            ("Sub Existência", "Existe indicador?", fn_sim_nao),
            ("Sub Aplicação", None, _fn_na),
            ("Sub Padrão", "No padrão?", fn_sim_nao),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
            ("Sub Atualização", "Como é atualizado?", fn_atualizacao),
        ],
    },
    "Treinamento": {
        "frente": "Treinamento",
        "col_item": "Nome_Treinamento",
        "subs": [
            ("Sub Existência", "Treinamento está coerente aos documentos?", fn_sim_nao),
            ("Sub Aplicação", "Treinamento foi aplicado?", fn_sim_nao),
            ("Sub Padrão", None, _fn_na),
            ("Sub Conformidade", "Conforme?", fn_conformidade),
            ("Sub Atualização", "Houve atualização?", fn_sim_nao),
        ],
    },
    "Qualidade": {
        "frente": "Qualidade",
        "col_item": "Processo avaliado",
        "subs": [
            ("Sub Existência", "Existência", fn_numerico),
            ("Sub Aplicação", "Abrangência", fn_numerico),
            ("Sub Padrão", None, _fn_na),
            ("Sub Conformidade", "Conformidade", fn_numerico),
            ("Sub Atualização", None, _fn_na),
        ],
    },
}


def _fato(aba: str, cfg: dict) -> pd.DataFrame:
    df = pd.read_excel(FORMULARIO, sheet_name=aba)
    df = df[df["Data da avaliação"].notna()].copy()
    df["Operação"] = df["Operação"].astype(str).str.strip()
    df["Processo avaliado"] = df["Processo avaliado"].astype(str).str.strip()
    df = df[df["Operação"].ne("") & df["Operação"].ne("Exemplo (apagar)")]
    df["Frente"] = cfg["frente"]

    for nome, col, fn in cfg["subs"]:
        if col is None:
            df[nome] = None
        else:
            df[nome] = df[col].map(fn)

    subs = [nome for nome, _, _ in cfg["subs"]]
    df["ScoreLinha"] = df[subs].apply(lambda r: _score_linha(r.tolist()), axis=1)

    cols = ["Frente", cfg["col_item"], "ScoreLinha"] + subs + _COLS_BASE
    cols = list(dict.fromkeys(c for c in cols if c in df.columns))
    df = df[cols]
    return df.reset_index(drop=True)


def _plano_acao(doc: pd.DataFrame, ind: pd.DataFrame, tre: pd.DataFrame) -> pd.DataFrame:
    def preparar(df, col_item):
        d = df[
            [
                "Operação",
                "Processo avaliado",
                "Frente",
                col_item,
                "Plano de Ação",
                "Responsável",
                "Prazo",
                "Status da Ação",
            ]
        ].copy()
        return d.rename(columns={col_item: "Item"})

    pa = pd.concat(
        [preparar(doc, "Nome_Documento"), preparar(ind, "Nome_Indicador"), preparar(tre, "Nome_Treinamento")],
        ignore_index=True,
    )
    pa = pa[pa["Plano de Ação"].notna() & pa["Plano de Ação"].astype(str).str.strip().ne("")]
    pa["Prazo"] = pd.to_datetime(pa["Prazo"], errors="coerce")
    return pa[COLUNAS_PLANO].reset_index(drop=True)


def _mtime() -> float:
    return FORMULARIO.stat().st_mtime if FORMULARIO.exists() else 0.0


def _fato_de_formulario(formulario_path: Path, aba: str, cfg: dict) -> pd.DataFrame:
    """Ler dados de uma aba específica de um formulário Excel."""
    try:
        df = pd.read_excel(formulario_path, sheet_name=aba)
        df = df[df["Data da avaliação"].notna()].copy()
        df["Operação"] = df["Operação"].astype(str).str.strip()
        df["Processo avaliado"] = df["Processo avaliado"].astype(str).str.strip()
        df = df[df["Operação"].ne("") & df["Operação"].ne("Exemplo (apagar)")]
        df["Frente"] = cfg["frente"]
        df["Arquivo"] = formulario_path.name  # Adicionar referência ao arquivo

        for nome, col, fn in cfg["subs"]:
            if col is None:
                df[nome] = None
            else:
                df[nome] = df[col].map(fn)

        subs = [nome for nome, _, _ in cfg["subs"]]
        df["ScoreLinha"] = df[subs].apply(lambda r: _score_linha(r.tolist()), axis=1)

        cols = ["Frente", cfg["col_item"], "ScoreLinha"] + subs + _COLS_BASE + ["Arquivo"]
        cols = list(dict.fromkeys(c for c in cols if c in df.columns))
        df = df[cols]
        return df.reset_index(drop=True)
    except Exception as e:
        print(f"Erro ao ler aba {aba} do formulário {formulario_path.name}: {e}")
        return pd.DataFrame()

@lru_cache(maxsize=1)
def carregar_dados(mtime: float = 0.0) -> dict[str, pd.DataFrame]:
    del mtime
    
    formularios = obter_formularios()
    print(f"Formulários encontrados: {[f.name for f in formularios]}")
    
    # Listas para armazenar dados de todos os formulários
    todos_docs = []
    todos_inds = []
    todos_tres = []
    todos_quas = []
    
    for formulario in formularios:
        print(f"Carregando dados de: {formulario.name}")
        
        doc = _fato_de_formulario(formulario, "Avaliação", _CONFIG["Avaliação"])
        ind = _fato_de_formulario(formulario, "Indicadores", _CONFIG["Indicadores"])
        tre = _fato_de_formulario(formulario, "Treinamento", _CONFIG["Treinamento"])
        qua = _fato_de_formulario(formulario, "Qualidade", _CONFIG["Qualidade"])
        
        if not doc.empty:
            todos_docs.append(doc)
        if not ind.empty:
            todos_inds.append(ind)
        if not tre.empty:
            todos_tres.append(tre)
        if not qua.empty:
            todos_quas.append(qua)
    
    # Concatenar dados de todos os formulários
    doc_final = pd.concat(todos_docs, ignore_index=True) if todos_docs else pd.DataFrame()
    ind_final = pd.concat(todos_inds, ignore_index=True) if todos_inds else pd.DataFrame()
    tre_final = pd.concat(todos_tres, ignore_index=True) if todos_tres else pd.DataFrame()
    qua_final = pd.concat(todos_quas, ignore_index=True) if todos_quas else pd.DataFrame()
    
    print(f"Total de registros carregados:")
    print(f"  Documentação: {len(doc_final)}")
    print(f"  Indicadores: {len(ind_final)}")
    print(f"  Treinamento: {len(tre_final)}")
    print(f"  Qualidade: {len(qua_final)}")
    
    return {
        "Documentacao": doc_final,
        "Indicadores": ind_final,
        "Treinamento": tre_final,
        "Qualidade": qua_final,
        "PlanoAcao": _plano_acao(doc_final, ind_final, tre_final),
    }
