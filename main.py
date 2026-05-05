from finance_service import (
    adicionar_movimentacao,
    calcular_resumo,
    deletar_movimentacao,
    listar_movimentacoes,
)
from formatters import formatar_moeda


def mostrar_menu():
    print("\n===== BOT FINANCEIRO - TERMINAL =====")
    print("1 - Adicionar receita")
    print("2 - Adicionar despesa")
    print("3 - Listar movimentacoes")
    print("4 - Ver resumo")
    print("5 - Deletar movimentacao")
    print("0 - Sair")


def ler_texto_obrigatorio(mensagem):
    while True:
        texto = input(mensagem).strip()

        if texto:
            return texto

        print("Este campo nao pode ficar vazio.")


def ler_valor(mensagem):
    while True:
        texto = input(mensagem).replace(",", ".").strip()

        try:
            valor = float(texto)
            if valor <= 0:
                print("O valor precisa ser maior que zero.")
                continue

            return valor
        except ValueError:
            print("Digite um valor valido. Exemplo: 150,50")


def cadastrar_movimentacao(tipo):
    descricao = ler_texto_obrigatorio("Descricao: ")
    categoria = ler_texto_obrigatorio("Categoria: ")
    valor = ler_valor("Valor: R$ ")

    try:
        movimentacao = adicionar_movimentacao(tipo, descricao, categoria, valor)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    print(f"{tipo.capitalize()} cadastrada com sucesso!")
    print(f"ID: {movimentacao['id']}")


def mostrar_movimentacoes():
    movimentacoes = listar_movimentacoes()

    if not movimentacoes:
        print("Nenhuma movimentacao cadastrada.")
        return

    print("\n===== MOVIMENTACOES =====")

    for movimentacao in movimentacoes:
        id_movimentacao = movimentacao.get("id", "sem id")
        print(f"\nID: {id_movimentacao}")
        print(f"Tipo: {movimentacao.get('tipo', '').upper()}")
        print(f"Descricao: {movimentacao.get('descricao', '')}")
        print(f"Categoria: {movimentacao.get('categoria', '')}")
        print(f"Valor: {formatar_moeda(movimentacao.get('valor', 0))}")
        print(f"Data: {movimentacao.get('data', '')}")


def mostrar_resumo():
    resumo = calcular_resumo()

    print("\n===== RESUMO FINANCEIRO =====")
    print(f"Total de receitas: {formatar_moeda(resumo['total_receitas'])}")
    print(f"Total de despesas: {formatar_moeda(resumo['total_despesas'])}")
    print(f"Saldo: {formatar_moeda(resumo['saldo'])}")


def apagar_movimentacao():
    try:
        id_movimentacao = int(input("ID da movimentacao: "))
    except ValueError:
        print("Digite um ID valido.")
        return

    movimentacao = deletar_movimentacao(id_movimentacao)

    if movimentacao is None:
        print("Movimentacao nao encontrada.")
        return

    print("Movimentacao deletada com sucesso!")


def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_movimentacao("receita")
        elif opcao == "2":
            cadastrar_movimentacao("despesa")
        elif opcao == "3":
            mostrar_movimentacoes()
        elif opcao == "4":
            mostrar_resumo()
        elif opcao == "5":
            apagar_movimentacao()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
