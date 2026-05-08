# Bot Financeiro

Projeto simples de controle financeiro em Python com duas interfaces:

- bot para Discord com slash commands;
- menu no terminal.

Os dados ficam salvos localmente no arquivo `movimentacoes.json`. Ainda nao ha banco de dados, FastAPI ou Google Sheets.

O bot suporta multiplos usuarios no mesmo servidor. Cada nova movimentacao salva pelo Discord recebe `user_id`, `user_name`, `guild_id` e `guild_name`, permitindo separar os lancamentos de cada pessoa.

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
- `/resumo`: mostra apenas as suas receitas, despesas e saldo no servidor atual.
- `/listar`: lista apenas as suas ultimas 10 movimentacoes no servidor atual.
- `/deletar`: deleta uma movimentacao sua pelo ID no servidor atual.
- `/categoria`: lista apenas as suas movimentacoes de uma categoria no servidor atual.
- `/resumo_geral`: mostra o resumo geral do servidor atual.
- `/listar_geral`: lista as ultimas 10 movimentacoes do servidor atual.

## Comandos pessoais e gerais

Os comandos pessoais (`/resumo`, `/listar`, `/categoria` e `/deletar`) usam o usuario que executou o comando e o servidor atual como filtro. Assim, um usuario nao ve nem apaga movimentacoes de outro usuario.

Os comandos gerais (`/resumo_geral` e `/listar_geral`) mostram dados agregados do servidor atual, filtrando por `guild_id`. Eles sao bloqueados em mensagem direta para nao misturar dados de usuarios diferentes.

Se o bot for usado por mensagem direta, o servidor fica registrado como `DM`.

## Armazenamento

O arquivo `movimentacoes.json` e a fonte dos dados do projeto. Se ele ja tiver dados, eles devem ser preservados. Movimentacoes antigas sem `user_id` ou `guild_id` continuam no arquivo, mas os comandos pessoais do Discord usam apenas movimentacoes novas que tenham identificacao de usuario e servidor.

Se o JSON estiver invalido, o sistema interrompe a leitura/gravacao e pede correcao do arquivo em vez de salvar por cima do historico. As gravacoes tambem sao feitas por arquivo temporario para reduzir risco de corromper dados.

O terminal funciona como ferramenta local/admin: lista, resume e deleta movimentacoes globais do arquivo.
