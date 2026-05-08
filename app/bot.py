import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from app.finance_service import (
    adicionar_movimentacao,
    calcular_resumo_geral,
    calcular_resumo_usuario,
    deletar_movimentacao,
    listar_movimentacoes_geral,
    listar_movimentacoes_usuario,
    listar_por_categoria_usuario,
)
from app.formatters import formatar_moeda


load_dotenv()
LIMITE_MENSAGEM_DISCORD = 1900


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


def obter_contexto(interaction):
    user_id = interaction.user.id
    user_name = interaction.user.name

    if interaction.guild:
        guild_id = interaction.guild.id
        guild_name = interaction.guild.name
    else:
        guild_id = None
        guild_name = "DM"

    return user_id, user_name, guild_id, guild_name


def formatar_movimentacao(movimentacao):
    id_movimentacao = movimentacao.get("id", "sem id")
    tipo = movimentacao.get("tipo", "").upper()
    descricao = movimentacao.get("descricao", "")
    categoria = movimentacao.get("categoria", "")
    valor = formatar_moeda(movimentacao.get("valor", 0))
    data = movimentacao.get("data", "")
    user_name = movimentacao.get("user_name")

    usuario = ""
    if user_name:
        usuario = f"\nUsuario: {user_name}"

    return (
        f"ID: {id_movimentacao} | {tipo}\n"
        f"Descricao: {descricao}\n"
        f"Categoria: {categoria}\n"
        f"Valor: {valor}\n"
        f"Data: {data}"
        f"{usuario}"
    )


async def enviar_mensagem(interaction, mensagem):
    partes = quebrar_mensagem(mensagem)

    for parte in partes:
        await interaction.followup.send(parte)


def quebrar_mensagem(mensagem, limite=LIMITE_MENSAGEM_DISCORD):
    if len(mensagem) <= limite:
        return [mensagem]

    partes = []
    parte_atual = ""

    for bloco in mensagem.split("\n\n"):
        separador = "\n\n" if parte_atual else ""
        candidato = f"{parte_atual}{separador}{bloco}"

        if len(candidato) <= limite:
            parte_atual = candidato
            continue

        if parte_atual:
            partes.append(parte_atual)
            parte_atual = ""

        while len(bloco) > limite:
            partes.append(bloco[:limite])
            bloco = bloco[limite:]

        parte_atual = bloco

    if parte_atual:
        partes.append(parte_atual)

    return partes


def esta_em_dm(guild_id):
    return guild_id is None


async def enviar_erro(interaction, acao, erro):
    await interaction.followup.send(f"Erro ao {acao}: {erro}")


@bot.tree.command(name="receita", description="Cadastra uma receita")
async def receita(interaction: discord.Interaction, descricao: str, categoria: str, valor: float):
    await interaction.response.defer()
    user_id, user_name, guild_id, guild_name = obter_contexto(interaction)

    try:
        movimentacao = adicionar_movimentacao(
            "receita",
            descricao,
            categoria,
            valor,
            user_id,
            user_name,
            guild_id,
            guild_name,
            interaction.id,
        )
    except ValueError as erro:
        await interaction.followup.send(f"Erro ao cadastrar receita: {erro}")
        return

    await enviar_mensagem(
        interaction,
        "Receita cadastrada com sucesso!\n\n" + formatar_movimentacao(movimentacao)
    )


@bot.tree.command(name="despesa", description="Cadastra uma despesa")
async def despesa(interaction: discord.Interaction, descricao: str, categoria: str, valor: float):
    await interaction.response.defer()
    user_id, user_name, guild_id, guild_name = obter_contexto(interaction)

    try:
        movimentacao = adicionar_movimentacao(
            "despesa",
            descricao,
            categoria,
            valor,
            user_id,
            user_name,
            guild_id,
            guild_name,
            interaction.id,
        )
    except ValueError as erro:
        await interaction.followup.send(f"Erro ao cadastrar despesa: {erro}")
        return

    await enviar_mensagem(
        interaction,
        "Despesa cadastrada com sucesso!\n\n" + formatar_movimentacao(movimentacao)
    )


@bot.tree.command(name="resumo", description="Mostra o resumo financeiro")
async def resumo(interaction: discord.Interaction):
    await interaction.response.defer()
    user_id, _, guild_id, _ = obter_contexto(interaction)

    try:
        dados = calcular_resumo_usuario(user_id, guild_id)
    except ValueError as erro:
        await enviar_erro(interaction, "calcular resumo", erro)
        return

    mensagem = (
        "Seu resumo financeiro\n\n"
        f"Receitas: {formatar_moeda(dados['total_receitas'])}\n"
        f"Despesas: {formatar_moeda(dados['total_despesas'])}\n"
        f"Saldo: {formatar_moeda(dados['saldo'])}"
    )

    await enviar_mensagem(interaction, mensagem)


@bot.tree.command(name="listar", description="Lista as ultimas 10 movimentacoes")
async def listar(interaction: discord.Interaction):
    await interaction.response.defer()
    user_id, _, guild_id, _ = obter_contexto(interaction)

    try:
        movimentacoes = listar_movimentacoes_usuario(user_id, guild_id)
    except ValueError as erro:
        await enviar_erro(interaction, "listar movimentacoes", erro)
        return

    if not movimentacoes:
        await interaction.followup.send("Voce nao tem movimentacoes cadastradas aqui.")
        return

    ultimas_movimentacoes = movimentacoes[-10:]
    linhas = [formatar_movimentacao(item) for item in ultimas_movimentacoes]
    await enviar_mensagem(interaction, "Ultimas movimentacoes:\n\n" + "\n\n".join(linhas))


@bot.tree.command(name="deletar", description="Deleta uma movimentacao pelo id")
async def deletar(interaction: discord.Interaction, id_movimentacao: int):
    await interaction.response.defer()
    user_id, _, guild_id, _ = obter_contexto(interaction)

    try:
        movimentacao = deletar_movimentacao(id_movimentacao, user_id, guild_id)
    except ValueError as erro:
        await enviar_erro(interaction, "deletar movimentacao", erro)
        return

    if movimentacao is None:
        await interaction.followup.send(
            "Movimentacao nao encontrada entre os seus lancamentos neste servidor."
        )
        return

    await enviar_mensagem(
        interaction,
        "Movimentacao deletada com sucesso!\n\n" + formatar_movimentacao(movimentacao)
    )


@bot.tree.command(name="categoria", description="Lista movimentacoes de uma categoria")
async def categoria(interaction: discord.Interaction, categoria: str):
    await interaction.response.defer()
    user_id, _, guild_id, _ = obter_contexto(interaction)

    try:
        movimentacoes = listar_por_categoria_usuario(categoria, user_id, guild_id)
    except ValueError as erro:
        await enviar_erro(interaction, "listar categoria", erro)
        return

    if not movimentacoes:
        await interaction.followup.send("Voce nao tem movimentacoes nessa categoria aqui.")
        return

    resultados = movimentacoes[-10:]
    linhas = [formatar_movimentacao(item) for item in resultados]
    await enviar_mensagem(
        interaction,
        "Movimentacoes encontradas:\n\n" + "\n\n".join(linhas),
    )


@bot.tree.command(name="resumo_geral", description="Mostra o resumo geral do servidor")
async def resumo_geral(interaction: discord.Interaction):
    await interaction.response.defer()
    _, _, guild_id, guild_name = obter_contexto(interaction)

    if esta_em_dm(guild_id):
        await interaction.followup.send("Este comando geral so pode ser usado em servidor.")
        return

    try:
        dados = calcular_resumo_geral(guild_id)
    except ValueError as erro:
        await enviar_erro(interaction, "calcular resumo geral", erro)
        return

    mensagem = (
        f"Resumo geral - {guild_name}\n\n"
        f"Receitas: {formatar_moeda(dados['total_receitas'])}\n"
        f"Despesas: {formatar_moeda(dados['total_despesas'])}\n"
        f"Saldo: {formatar_moeda(dados['saldo'])}"
    )

    await enviar_mensagem(interaction, mensagem)


@bot.tree.command(name="listar_geral", description="Lista as ultimas 10 movimentacoes do servidor")
async def listar_geral(interaction: discord.Interaction):
    await interaction.response.defer()
    _, _, guild_id, guild_name = obter_contexto(interaction)

    if esta_em_dm(guild_id):
        await interaction.followup.send("Este comando geral so pode ser usado em servidor.")
        return

    try:
        movimentacoes = listar_movimentacoes_geral(guild_id)
    except ValueError as erro:
        await enviar_erro(interaction, "listar movimentacoes gerais", erro)
        return

    if not movimentacoes:
        await interaction.followup.send("Nao ha movimentacoes cadastradas neste servidor.")
        return

    ultimas_movimentacoes = movimentacoes[-10:]
    linhas = [formatar_movimentacao(item) for item in ultimas_movimentacoes]
    await enviar_mensagem(
        interaction,
        f"Ultimas movimentacoes - {guild_name}:\n\n" + "\n\n".join(linhas)
    )


def main():
    discord_token = os.getenv("DISCORD_TOKEN")

    if not discord_token:
        raise ValueError("Crie um arquivo .env com DISCORD_TOKEN=seu_token_do_discord.")

    bot.run(discord_token)


if __name__ == "__main__":
    main()
