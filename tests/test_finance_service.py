from decimal import Decimal

from app import storage
from app.finance_service import (
    adicionar_movimentacao,
    calcular_resumo,
    deletar_movimentacao_geral,
)


def configurar_arquivo_temporario(monkeypatch, tmp_path):
    caminho = tmp_path / "movimentacoes.json"
    monkeypatch.setattr(storage, "ARQUIVO_MOVIMENTACOES", caminho)
    return caminho


def test_cadastra_receita(monkeypatch, tmp_path):
    configurar_arquivo_temporario(monkeypatch, tmp_path)

    movimentacao = adicionar_movimentacao(
        "receita",
        "Salario",
        "Renda fixa",
        2500.0,
    )

    assert movimentacao["id"] == 1
    assert movimentacao["tipo"] == "receita"
    assert movimentacao["valor"] == 2500.0


def test_cadastra_despesa(monkeypatch, tmp_path):
    configurar_arquivo_temporario(monkeypatch, tmp_path)

    movimentacao = adicionar_movimentacao(
        "despesa",
        "Supermercado",
        "Alimentacao",
        150.0,
    )

    assert movimentacao["id"] == 1
    assert movimentacao["tipo"] == "despesa"
    assert movimentacao["valor"] == 150.0


def test_calcula_resumo_e_saldo(monkeypatch, tmp_path):
    configurar_arquivo_temporario(monkeypatch, tmp_path)

    adicionar_movimentacao("receita", "Salario", "Renda fixa", 2500.0)
    adicionar_movimentacao("despesa", "Supermercado", "Alimentacao", 150.0)

    resumo = calcular_resumo()

    assert resumo["total_receitas"] == Decimal("2500.0")
    assert resumo["total_despesas"] == Decimal("150.0")
    assert resumo["saldo"] == Decimal("2350.0")


def test_deleta_movimentacao(monkeypatch, tmp_path):
    configurar_arquivo_temporario(monkeypatch, tmp_path)

    movimentacao = adicionar_movimentacao("receita", "Salario", "Renda fixa", 2500.0)

    deletada = deletar_movimentacao_geral(movimentacao["id"])
    resumo = calcular_resumo()

    assert deletada["id"] == movimentacao["id"]
    assert resumo["total_receitas"] == Decimal("0")
    assert resumo["total_despesas"] == Decimal("0")
    assert resumo["saldo"] == Decimal("0")
