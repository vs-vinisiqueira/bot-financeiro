import json
import tempfile
import threading
from pathlib import Path


ARQUIVO_MOVIMENTACOES = Path(__file__).with_name("movimentacoes.json")
_LOCK = threading.RLock()


class ErroArquivoMovimentacoes(ValueError):
    """Indica que o arquivo de movimentacoes nao pode ser usado com seguranca."""


def carregar_movimentacoes():
    """Carrega as movimentacoes salvas no arquivo JSON."""
    with _LOCK:
        return _carregar_movimentacoes_sem_lock()


def _carregar_movimentacoes_sem_lock():
    if not ARQUIVO_MOVIMENTACOES.exists():
        return []

    conteudo = ARQUIVO_MOVIMENTACOES.read_text(encoding="utf-8").strip()
    if not conteudo:
        return []

    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as erro:
        raise ErroArquivoMovimentacoes(
            f"O arquivo {ARQUIVO_MOVIMENTACOES.name} esta com JSON invalido. "
            "Corrija ou restaure o arquivo antes de salvar novas movimentacoes."
        ) from erro

    if isinstance(dados, list):
        return dados

    raise ErroArquivoMovimentacoes(
        f"O arquivo {ARQUIVO_MOVIMENTACOES.name} precisa conter uma lista de movimentacoes."
    )


def salvar_movimentacoes(movimentacoes):
    """Salva as movimentacoes no arquivo JSON."""
    with _LOCK:
        _salvar_movimentacoes_sem_lock(movimentacoes)


def _salvar_movimentacoes_sem_lock(movimentacoes):
    conteudo = json.dumps(movimentacoes, indent=4, ensure_ascii=False)
    ARQUIVO_MOVIMENTACOES.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=ARQUIVO_MOVIMENTACOES.parent,
        delete=False,
    ) as arquivo_temporario:
        arquivo_temporario.write(conteudo)
        arquivo_temporario.write("\n")
        caminho_temporario = Path(arquivo_temporario.name)

    caminho_temporario.replace(ARQUIVO_MOVIMENTACOES)


def atualizar_movimentacoes(funcao):
    """Executa uma alteracao atomica em memoria e salva o resultado no JSON."""
    with _LOCK:
        movimentacoes = _carregar_movimentacoes_sem_lock()
        resultado = funcao(movimentacoes)
        _salvar_movimentacoes_sem_lock(movimentacoes)
        return resultado
