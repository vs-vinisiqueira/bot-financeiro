import json
import requests
from datetime import datetime
from pathlib import Path

ARQUIVO_MOVIMENTACOES = Path(__file__).with_name("movimentacoes.json")
#Cria o caminho do arquivo onde as movimentações serão salvas.

movimentacoes = []
#Cria uma lista vazia para armazenar as movimentações

def carregar_movimentacoes():
    """Carrega as movimentações salvas no arquivo JSON."""
    global movimentacoes

    try:
        with open(ARQUIVO_MOVIMENTACOES, "r", encoding="utf-8") as arquivo:
            #Abre o arquivo movimentacoes.json em modo leitura.
            dados = json.load(arquivo)
            #Lê o conteúdo do arquivo JSON e converte para uma estrutura Python

        if isinstance(dados, list):
            movimentacoes = dados
        else:
            print("Arquivo de movimentações inválido. Iniciando com lista vazia.")
            movimentacoes = []
    except FileNotFoundError:
        #Captura o erro que acontece quando o arquivo movimentacoes.json ainda não existe.
        movimentacoes = []
        #Se o arquivo não existir, o sistema começa com uma lista vazia.
    except json.JSONDecodeError:
        #Captura erro de leitura do JSON.
        print("Erro ao ler o arquivo de movimentações. Iniciando com lista vazia.")
        movimentacoes = []
        #Inicia o sistema com a lista vazia para evitar travamento.

def salvar_movimentacoes():
    """Salva as movimentações em um arquivo JSON."""
    with open(ARQUIVO_MOVIMENTACOES, "w", encoding="utf-8") as arquivo:
        json.dump(movimentacoes, arquivo, ensure_ascii=False, indent=4)
        #Converte dados Python para JSON e grava no arquivo.

def mostrar_menu():
    """Exibe o menu principal do sistema."""
    print("\n===== SISTEMA DE GESTÃO FINANCEIRA =====")
    print("1 - Adicionar receita")
    print("2 - Adicionar despesa")
    print("3 - Listar movimentações")
    print("4 - Ver resumo financeiro")
    print("5 - Converter dólar para real")
    print("6 - Sair")
   
def ler_valor(mensagem):
    """Lê e valida um valor monetário digitado pelo usuário."""
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            #permite usuário digitar o valor usando vírgula ou ponto como separador decimal
            if valor <= 0:
                print("O valor precisa ser maior que zero.")
            else:
                return valor
        except ValueError:
            print("Digite um valor válido. Exemplo: 150.50")

def ler_texto_obrigatorio(mensagem):
    """Lê um texto obrigatório digitado pelo usuário."""
    while True:
        texto = input(mensagem).strip()

        if texto:
            return texto

        print("Este campo não pode ficar vazio.")

def adicionar_movimentacao(tipo):
    """Adiciona uma receita ou despesa na lista de movimentações."""
    descricao = ler_texto_obrigatorio("Descrição: ")
    categoria = ler_texto_obrigatorio("Categoria: ")
    valor = ler_valor("Valor: R$ ")
    
    movimentacao = {
    #Cria um dicionário chamado movimentacao.
        "tipo": tipo,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        #Adiciona a data e hora atual formatada como dia/mês/ano hora:minuto.
    }

    movimentacoes.append(movimentacao)
    #Adiciona a nova movimentação dentro da lista movimentacoes.
    salvar_movimentacoes()
    #Salva a lista atualizada de movimentações no arquivo JSON.
    print(f"{tipo.capitalize()} cadastrada com sucesso!")
    #Exibe uma mensagem de confirmação informando o tipo de movimentação cadastrada (receita ou despesa).

def listar_movimentacoes():
    """Lista todas as movimentações cadastradas."""
    if len(movimentacoes) == 0:
        print("Nenhuma movimentação cadastrada.")
        return
    
    print("\n===== MOVIMENTAÇÕES =====")

    for indice, item in enumerate(movimentacoes, start=1):
        #Percorre a lista de movimentações usando enumerate para obter o índice e o item. O índice começa em 1.
        print(f"\n{indice}. {item['tipo'].upper()}")
        print(f"Descrição: {item['descricao']}")
        print(f"Categoria: {item['categoria']}")
        print(f"Valor: R$ {item['valor']:.2f}")
        print(f"Data: {item['data']}")

def mostrar_resumo():
    """Calcula e exibe o resumo financeiro."""
    total_receitas = 0
    total_despesas = 0

    for item in movimentacoes:
        if item["tipo"] == "receita":
            total_receitas += item["valor"]
        elif item["tipo"] == "despesa":
            total_despesas += item["valor"]
    
    saldo = total_receitas - total_despesas

    print("\n===== RESUMO FINANCEIRO =====")
    print(f"Total de receitas: R$ {total_receitas:.2f}")
    print(f"total de despesas: R$ {total_despesas:.2f}")
    print(f"Saldo final: R$ {saldo:.2f}")
    if saldo < 0:
        print("Alerta: você está gastando mais do que recebe.")
    elif saldo == 0:
        print("Atenção: suas receitas e despesas estão equilibradas.")
    else:
        print("Boa! Você está com saldo positivo!")

def converter_dolar_para_real():
    """Consulta uma API de câmbio e converte dólar para real."""
    try:
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        #Cria uma variável chamada url com o endereço da API.
        resposta = requests.get(url, timeout=10)
        #Faz uma requisição GET para a API usando a biblioteca requests.
        resposta.raise_for_status()
        #Verifica se a resposta HTTP teve erro.
        dados = resposta.json()
        #Converte a resposta da API para um dicionário Python usando o método json() da resposta.

        cotacao = float(dados["USDBRL"]["bid"])

        valor_dolar = ler_valor("Digite o valor em dólar: US$ ")
        valor_real = valor_dolar * cotacao

        print("\n===== CONVERSÃO DE CÂMBIO =====")
        print(f"Cotação atual do dólar: R$ {cotacao:.2f}")
        print(f"Valor convertido: R$ {valor_real:.2f}")
    
    except requests.exceptions.JSONDecodeError:
        #Captura erro de interpretação do JSON retornado pela API.
        print("Erro ao interpretar a resposta da API.")
    except requests.exceptions.HTTPError:
        #Captura erros HTTP, como 404 ou 500, que indicam que a resposta da API não foi bem-sucedida.
        print("Erro na resposta da API de câmbio.")
    except requests.exceptions.RequestException:
        #Captura erros relacionados à requisição, como problemas de conexão, tempo limite ou outros erros de rede.
        print("Erro de conexão ao consultar a API.")
    except KeyError:
        #Captura erro de acesso a chaves do dicionário, caso a estrutura da resposta da API seja diferente do esperado.
        print("Erro ao interpretar os dados recebidos da API.")
    except ValueError:
        #Captura erro de conversão de string para float, caso o valor da cotação não seja um número válido.
        print("Erro ao converter os dados da cotação.")

def main():
    """Função principal do sistema."""
    carregar_movimentacoes()
    sistema_ativo = True
    #Cria uma variável booleana para controlar o loop principal do sistema. Enquanto for True, o sistema continuará rodando.
    while sistema_ativo:
        #Exibe o menu principal do sistema e aguarda a escolha do usuário.
        mostrar_menu()

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            #Captura o erro de conversão de string para inteiro, caso o usuário digite algo que não seja um número.
            print("Digite apenas números de 1 a 6.")
            continue

        if opcao == 1:
            adicionar_movimentacao("receita")

        elif opcao == 2:
            adicionar_movimentacao("despesa")

        elif opcao == 3:
            listar_movimentacoes()

        elif opcao == 4:
            mostrar_resumo()

        elif opcao == 5:
            converter_dolar_para_real()

        elif opcao == 6:
            print("Encerrando o sistema...")
            sistema_ativo = False

        else:
            print("Opção inválida. Escolha uma opção de 1 a 6.")


main()

