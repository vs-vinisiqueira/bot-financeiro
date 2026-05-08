def formatar_moeda(valor):
    """Formata um numero como moeda brasileira."""
    try:
        valor_formatado = f"{float(valor):,.2f}"
    except (TypeError, ValueError):
        return "R$ valor invalido"

    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"
