import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from finance_service import (
    adicionar_movimentacao,
    calcular_resumo,
    deletar_movimentacao,
    listar_movimentacoes,
    listar_por_categoria,
)
from formatters import formatar_moeda


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("Crie um arquivo .env com DISCORD_TOKEN=seu_token_do_discord.")


class FinanceBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"Bot conectado como {self.user}")


bot = FinanceBot()


def formatar_movimentacao(movimentacao):
    id_movimentacao = movimentacao.get("id", "sem id")
    tipo = movimentacao.get("tipo", "").upper()
    descricao = movimentacao.get("descricao", "")
    categoria = movimentacao.get("categoria", "")
    valor = formatar_moeda(movimentacao.get("valor", 0))
    data = movimentacao.get("data", "")

    return (
        f"ID: {id_movimentacao} | {tipo}\n"
        f"Descricao: {descricao}\n"
        f"Categoria: {categoria}\n"
        f"Valor: {valor}\n"
        f"Data: {data}"
    )


@bot.tree.command(name="receita", description="Cadastra uma receita")
async def receita(interaction: discord.Interaction, descricao: str, categoria: str, valor: float):
    try:
        movimentacao = adicionar_movimentacao("receita", descricao, categoria, valor)
    except ValueError as erro:
        await interaction.response.send_message(f"Erro ao cadastrar receita: {erro}")
        return

    await interaction.response.send_message(
        "Receita cadastrada com sucesso!\n\n" + formatar_movimentacao(movimentacao)
    )


@bot.tree.command(name="despesa", description="Cadastra uma despesa")
async def despesa(interaction: discord.Interaction, descricao: str, categoria: str, valor: float):
    try:
        movimentacao = adicionar_movimentacao("despesa", descricao, categoria, valor)
    except ValueError as erro:
        await interaction.response.send_message(f"Erro ao cadastrar despesa: {erro}")
        return

    await interaction.response.send_message(
        "Despesa cadastrada com sucesso!\n\n" + formatar_movimentacao(movimentacao)
    )


@bot.tree.command(name="resumo", description="Mostra o resumo financeiro")
async def resumo(interaction: discord.Interaction):
    dados = calcular_resumo()

    mensagem = (
        "Resumo financeiro\n\n"
        f"Receitas: {formatar_moeda(dados['total_receitas'])}\n"
        f"Despesas: {formatar_moeda(dados['total_despesas'])}\n"
        f"Saldo: {formatar_moeda(dados['saldo'])}"
    )

    await interaction.response.send_message(mensagem)


@bot.tree.command(name="listar", description="Lista as ultimas 10 movimentacoes")
async def listar(interaction: discord.Interaction):
    movimentacoes = listar_movimentacoes()

    if not movimentacoes:
        await interaction.response.send_message("Nao ha movimentacoes cadastradas.")
        return

    ultimas_movimentacoes = movimentacoes[-10:]
    linhas = [formatar_movimentacao(item) for item in ultimas_movimentacoes]
    await interaction.response.send_message("Ultimas movimentacoes:\n\n" + "\n\n".join(linhas))


@bot.tree.command(name="deletar", description="Deleta uma movimentacao pelo id")
async def deletar(interaction: discord.Interaction, id_movimentacao: int):
    movimentacao = deletar_movimentacao(id_movimentacao)

    if movimentacao is None:
        await interaction.response.send_message("Movimentacao nao encontrada.")
        return

    await interaction.response.send_message(
        "Movimentacao deletada com sucesso!\n\n" + formatar_movimentacao(movimentacao)
    )


@bot.tree.command(name="categoria", description="Lista movimentacoes de uma categoria")
async def categoria(interaction: discord.Interaction, categoria: str):
    movimentacoes = listar_por_categoria(categoria)

    if not movimentacoes:
        await interaction.response.send_message("Nao ha movimentacoes nessa categoria.")
        return

    resultados = movimentacoes[-10:]
    linhas = [formatar_movimentacao(item) for item in resultados]
    await interaction.response.send_message("Movimentacoes encontradas:\n\n" + "\n\n".join(linhas))


bot.run(DISCORD_TOKEN)
