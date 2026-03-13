from discord.ext.commands import Cog
from discord import app_commands
from __main__ import user
from discord.ext import commands
import discord

class Basic(Cog):
    def __init__(self, bot, user):
        self.bot = bot
        self.user = user
    
    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="petpet", description="Pets a user")
    async def petpet(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message("_ _", ephemeral=True)
        msg = await interaction.original_response()
        await self.user.execute_interaction(msg, interaction)
        await interaction.delete_original_response()

    @app_commands.allowed_installs(users=True, guilds=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.command(name="colors", description="Mixes colors and shows them")
    @app_commands.choices(mix_mode=['Additive', 'Subtractive', 'Average'])
    async def colors(self, interaction: discord.Interaction, color_1: str, color_2: Optional[str], color_3: Optional[str], mix_mode: Optional[app_commands.Choice[str]]):
        await interaction.response.send_message("_ _", ephemeral=True)
        msg = await interaction.original_response()
        await self.user.execute_interaction(msg, interaction)
        await interaction.delete_original_response()

async def setup(bot):
    await bot.add_cog(Basic(bot, user))