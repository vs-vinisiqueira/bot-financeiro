# Bot Financeiro

Projeto simples de controle financeiro em Python com duas interfaces:

- bot para Discord com slash commands;
- menu no terminal.

Os dados ficam salvos localmente no arquivo `movimentacoes.json`. Ainda nao ha banco de dados, FastAPI ou Google Sheets.

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configurar o token do Discord

Crie um arquivo chamado `.env` na raiz do projeto e adicione:

```env
DISCORD_TOKEN=seu_token_real_do_discord
```

Use o arquivo `.env.example` como modelo. Nunca coloque o token real no codigo.

## Rodar o bot do Discord

```bash
python bot.py
```

## Rodar a versao terminal

```bash
python main.py
```

## Comandos do Discord

- `/receita`: cadastra uma receita.
- `/despesa`: cadastra uma despesa.
- `/resumo`: mostra receitas, despesas e saldo.
- `/listar`: lista as ultimas 10 movimentacoes.
- `/deletar`: deleta uma movimentacao pelo ID.
- `/categoria`: lista movimentacoes de uma categoria.

## Armazenamento

O arquivo `movimentacoes.json` e a fonte dos dados do projeto. Se ele ja tiver dados, eles devem ser preservados.
