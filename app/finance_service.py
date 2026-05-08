from datetime import datetime
from decimal import Decimal, InvalidOperation

from app.storage import atualizar_movimentacoes, carregar_movimentacoes


USUARIO_TERMINAL_ID = "terminal"
USUARIO_TERMINAL_NOME = "Terminal"
GUILD_TERMINAL_ID = "terminal"
GUILD_TERMINAL_NOME = "Terminal"


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


def valor_para_decimal(valor):
    try:
        valor_decimal = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        return None

    if not valor_decimal.is_finite():
        return None

    return valor_decimal


def mesma_guild(movimentacao, guild_id):
    """Confere a guild sem misturar movimentacoes antigas sem guild_id."""
    return "guild_id" in movimentacao and movimentacao.get("guild_id") == guild_id


def mesma_pessoa(movimentacao, user_id, guild_id):
    """Confere usuario e guild sem trazer dados antigos sem identificacao."""
    return (
        "user_id" in movimentacao
        and "guild_id" in movimentacao
        and movimentacao.get("user_id") == user_id
        and movimentacao.get("guild_id") == guild_id
    )


def calcular_resumo_movimentacoes(movimentacoes):
    """Calcula receitas, despesas e saldo de uma lista de movimentacoes."""
    total_receitas = Decimal("0")
    total_despesas = Decimal("0")

    for movimentacao in movimentacoes:
        valor = valor_para_decimal(movimentacao.get("valor", 0))
        if valor is None:
            continue

        if movimentacao.get("tipo") == "receita":
            total_receitas += valor
        elif movimentacao.get("tipo") == "despesa":
            total_despesas += valor

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": total_receitas - total_despesas,
    }


def adicionar_movimentacao(
    tipo,
    descricao,
    categoria,
    valor,
    user_id=USUARIO_TERMINAL_ID,
    user_name=USUARIO_TERMINAL_NOME,
    guild_id=GUILD_TERMINAL_ID,
    guild_name=GUILD_TERMINAL_NOME,
    interaction_id=None,
):
    """Adiciona uma receita ou despesa e salva no JSON."""
    if tipo not in ["receita", "despesa"]:
        raise ValueError("Tipo deve ser receita ou despesa.")

    valor_decimal = valor_para_decimal(valor)
    if valor_decimal is None:
        raise ValueError("Valor invalido.")

    if valor_decimal <= 0:
        raise ValueError("Valor deve ser maior que zero.")

    descricao = str(descricao).strip()
    categoria = str(categoria).strip()

    if not descricao:
        raise ValueError("Descricao nao pode ficar vazia.")

    if not categoria:
        raise ValueError("Categoria nao pode ficar vazia.")

    def alterar(movimentacoes):
        id_interacao = str(interaction_id) if interaction_id is not None else None

        if id_interacao is not None:
            for movimentacao in movimentacoes:
                if movimentacao.get("interaction_id") == id_interacao:
                    return movimentacao

        nova_movimentacao = {
            "id": gerar_proximo_id(movimentacoes),
            "tipo": tipo,
            "descricao": descricao,
            "categoria": categoria,
            "valor": float(valor_decimal),
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "user_id": user_id,
            "user_name": user_name,
            "guild_id": guild_id,
            "guild_name": guild_name,
            "interaction_id": id_interacao,
        }

        movimentacoes.append(nova_movimentacao)
        return nova_movimentacao

    return atualizar_movimentacoes(alterar)


def listar_movimentacoes():
    """Retorna todas as movimentacoes cadastradas."""
    return carregar_movimentacoes()


def calcular_resumo():
    """Calcula receitas, despesas e saldo."""
    movimentacoes = carregar_movimentacoes()
    return calcular_resumo_movimentacoes(movimentacoes)


def listar_movimentacoes_usuario(user_id, guild_id):
    """Retorna as movimentacoes de um usuario dentro de uma guild."""
    movimentacoes = carregar_movimentacoes()

    return [
        movimentacao
        for movimentacao in movimentacoes
        if mesma_pessoa(movimentacao, user_id, guild_id)
    ]


def calcular_resumo_usuario(user_id, guild_id):
    """Calcula o resumo de um usuario dentro de uma guild."""
    movimentacoes = listar_movimentacoes_usuario(user_id, guild_id)
    return calcular_resumo_movimentacoes(movimentacoes)


def listar_por_categoria_usuario(categoria, user_id, guild_id):
    """Lista movimentacoes de uma categoria para um usuario."""
    movimentacoes = listar_movimentacoes_usuario(user_id, guild_id)
    categoria_normalizada = categoria.strip().lower()

    return [
        movimentacao
        for movimentacao in movimentacoes
        if str(movimentacao.get("categoria", "")).lower() == categoria_normalizada
    ]


def deletar_movimentacao(id_movimentacao, user_id, guild_id):
    """Remove uma movimentacao se ela pertencer ao usuario na guild."""
    def alterar(movimentacoes):
        for indice, movimentacao in enumerate(movimentacoes):
            if movimentacao.get("id") == id_movimentacao and mesma_pessoa(
                movimentacao, user_id, guild_id
            ):
                return movimentacoes.pop(indice)

        return None

    return atualizar_movimentacoes(alterar)


def deletar_movimentacao_geral(id_movimentacao):
    """Remove uma movimentacao pelo id, sem filtro de usuario ou guild."""
    def alterar(movimentacoes):
        for indice, movimentacao in enumerate(movimentacoes):
            if movimentacao.get("id") == id_movimentacao:
                return movimentacoes.pop(indice)

        return None

    return atualizar_movimentacoes(alterar)


def calcular_resumo_geral(guild_id):
    """Calcula o resumo geral de uma guild."""
    movimentacoes = listar_movimentacoes_geral(guild_id)
    return calcular_resumo_movimentacoes(movimentacoes)


def listar_movimentacoes_geral(guild_id):
    """Retorna todas as movimentacoes de uma guild."""
    movimentacoes = carregar_movimentacoes()

    return [
        movimentacao
        for movimentacao in movimentacoes
        if mesma_guild(movimentacao, guild_id)
    ]


def listar_por_categoria(categoria):
    """Lista movimentacoes de uma categoria, ignorando maiusculas e minusculas."""
    movimentacoes = carregar_movimentacoes()
    categoria_normalizada = categoria.strip().lower()

    return [
        movimentacao
        for movimentacao in movimentacoes
        if str(movimentacao.get("categoria", "")).lower() == categoria_normalizada
    ]
