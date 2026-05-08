# Bot Financeiro

Bot financeiro em Python para registrar receitas e despesas pelo Discord ou por um menu no terminal. O projeto usa armazenamento local em JSON e foi organizado como pacote Python para facilitar manutenção, testes e publicação no GitHub.

## Tecnologias

- Python
- discord.py
- python-dotenv
- Pytest
- JSON para persistencia local

## Funcionalidades

- Cadastro de receitas e despesas.
- Listagem de movimentacoes.
- Calculo de receitas, despesas e saldo.
- Exclusao de movimentacoes por ID.
- Slash commands no Discord.
- Modo terminal para uso local/admin.
- Separacao de movimentacoes por usuario e servidor no Discord.
- Protecao contra sobrescrita quando o JSON esta invalido.

## Estrutura

```text
bot-financeiro/
├── app/
│   ├── __init__.py
│   ├── bot.py
│   ├── cli.py
│   ├── finance_service.py
│   ├── storage.py
│   └── formatters.py
├── data/
│   └── movimentacoes.example.json
├── tests/
│   └── test_finance_service.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

O arquivo real `data/movimentacoes.json` e criado automaticamente quando a primeira movimentacao e salva. Ele fica fora do Git para evitar publicar dados pessoais.

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configurar ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN=seu_token_real_do_discord
```

Use `.env.example` como referencia. Nunca publique o `.env` nem tokens reais.

## Rodar o bot Discord

```bash
python -m app.bot
```

Comandos disponiveis:

- `/receita`: cadastra uma receita.
- `/despesa`: cadastra uma despesa.
- `/resumo`: mostra o resumo pessoal no servidor atual.
- `/listar`: lista suas ultimas movimentacoes no servidor atual.
- `/deletar`: remove uma movimentacao sua pelo ID.
- `/categoria`: lista suas movimentacoes por categoria.
- `/resumo_geral`: mostra o resumo geral do servidor.
- `/listar_geral`: lista as ultimas movimentacoes do servidor.

## Rodar a versao terminal

```bash
python -m app.cli
```

O terminal funciona como ferramenta local/admin e opera sobre todas as movimentacoes salvas em `data/movimentacoes.json`.

## Rodar testes

```bash
pytest
```

## Armazenamento

- Exemplo publico: `data/movimentacoes.example.json`
- Arquivo real local: `data/movimentacoes.json`

Se `data/movimentacoes.json` nao existir, o sistema inicia com uma lista vazia e cria o arquivo na primeira gravacao. Se o JSON estiver invalido, a aplicacao interrompe a gravacao para preservar o historico.

## Proximas melhorias

- Criar camada de banco de dados.
- Adicionar filtros por periodo.
- Exportar relatorios em CSV.
- Melhorar permissao dos comandos gerais no Discord.
- Adicionar testes para comandos do bot.
