from datetime import datetime

from storage import carregar_movimentacoes, salvar_movimentacoes


def gerar_proximo_id(movimentacoes):
    """Gera o proximo id, ignorando movimentacoes antigas sem id."""
    ids = []

    for movimentacao in movimentacoes:
        id_movimentacao = movimentacao.get("id")

        if isinstance(id_movimentacao, int):
            ids.append(id_movimentacao)

    if not ids:
        return 1

    return max(ids) + 1


def adicionar_movimentacao(tipo, descricao, categoria, valor):
    """Adiciona uma receita ou despesa e salva no JSON."""
    if tipo not in ["receita", "despesa"]:
        raise ValueError("Tipo deve ser receita ou despesa.")

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        raise ValueError("Valor invalido.")

    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero.")

    movimentacoes = carregar_movimentacoes()

    nova_movimentacao = {
        "id": gerar_proximo_id(movimentacoes),
        "tipo": tipo,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }

    movimentacoes.append(nova_movimentacao)
    salvar_movimentacoes(movimentacoes)

    return nova_movimentacao


def listar_movimentacoes():
    """Retorna todas as movimentacoes cadastradas."""
    return carregar_movimentacoes()


def calcular_resumo():
    """Calcula receitas, despesas e saldo."""
    movimentacoes = carregar_movimentacoes()
    total_receitas = 0
    total_despesas = 0

    for movimentacao in movimentacoes:
        valor = float(movimentacao.get("valor", 0))

        if movimentacao.get("tipo") == "receita":
            total_receitas += valor
        elif movimentacao.get("tipo") == "despesa":
            total_despesas += valor

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": total_receitas - total_despesas,
    }


def deletar_movimentacao(id_movimentacao):
    """Remove uma movimentacao pelo id."""
    movimentacoes = carregar_movimentacoes()

    for movimentacao in movimentacoes:
        if movimentacao.get("id") == id_movimentacao:
            movimentacoes.remove(movimentacao)
            salvar_movimentacoes(movimentacoes)
            return movimentacao

    return None


def listar_por_categoria(categoria):
    """Lista movimentacoes de uma categoria, ignorando maiusculas e minusculas."""
    movimentacoes = carregar_movimentacoes()
    categoria_normalizada = categoria.strip().lower()

    return [
        movimentacao
        for movimentacao in movimentacoes
        if str(movimentacao.get("categoria", "")).lower() == categoria_normalizada
    ]
