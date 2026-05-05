import json
from pathlib import Path


ARQUIVO_MOVIMENTACOES = Path(__file__).with_name("movimentacoes.json")


def carregar_movimentacoes():
    """Carrega as movimentacoes salvas no arquivo JSON."""
    if not ARQUIVO_MOVIMENTACOES.exists():
        return []

    try:
        conteudo = ARQUIVO_MOVIMENTACOES.read_text(encoding="utf-8").strip()
        if not conteudo:
            return []

        dados = json.loads(conteudo)
    except json.JSONDecodeError:
        return []

    if isinstance(dados, list):
        return dados

    return []


def salvar_movimentacoes(movimentacoes):
    """Salva as movimentacoes no arquivo JSON."""
    ARQUIVO_MOVIMENTACOES.write_text(
        json.dumps(movimentacoes, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
