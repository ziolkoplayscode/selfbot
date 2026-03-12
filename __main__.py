import discord
import selfcord
import config
import asyncio
import os
import sys
import logging.handlers
import coloredlogs
from discord.ext import commands
from selfcord.ext import commands as usercommands
from types import SimpleNamespace




if not os.path.exists("logs"):
    os.makedirs("logs")

log_format = logging.Formatter(
    "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
)

logging.addLevelName(21, "USER")
logging.addLevelName(22, "BOT")

def userlog(self, message, *args, **kwargs):
    if self.isEnabledFor(21):
        self._log(21, message, args, **kwargs)
    
def botlog(self, message, *args, **kwargs):
    if self.isEnabledFor(22):
        self._log(22, message, args, **kwargs)

logging.Logger.user = userlog
logging.Logger.bot = botlog


level_styles ={
    'user': {'color':'cyan'},
    'bot': {'color':'magenta'}
}



stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)
logfile_handler = logging.FileHandler("logs/latest.log", mode="w")
logfile_handler.setFormatter(log_format)
log = logging.getLogger("discord")
log.setLevel(logging.INFO)
log.addHandler(stdout_handler)
log.addHandler(logfile_handler)
coloredlogs.install(logger=log, level=logging.INFO, level_styles=level_styles, fmt="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")


user = usercommands.Bot(
    command_prefix=config.prefix,
    self_bot=True
)

bot = commands.Bot(
    command_prefix=config.prefix,
    intents=discord.Intents.all(),
)

def __init__(self, user, bot):
    self.user = user
    self.bot = bot

bot.help_command = None
bot.config = config
bot.log = log
user.help_command = None
user.config = config
user.log = log

@user.event
async def on_ready():
    log.user(f"\nLogged in as: {user.user.name} - {user.user.id}")

@bot.event
async def on_ready():
    log.bot(f"\nLogged in as: {bot.user.name} - {bot.user.id}")

@user.event
async def on_command(ctx):
    log_text = (
        f"{ctx.message.author} ({ctx.message.author.id}): " f'"{ctx.message.content}" '
    )
    if ctx.guild:
        log_text += (
            f'in "{ctx.channel.name}" ({ctx.channel.id}) '
            f'on "{ctx.guild.name}" ({ctx.guild.id})'
        )
    else:
        log_text += f"in DMs ({ctx.channel.id})"
    log.user(log_text)


@user.event
async def on_message(message):
    await user.wait_until_ready()
    if user.user != message.author:
        return
    ctx = await user.get_context(message)
    await user.invoke(ctx)

async def sync():
    log.bot("Syncing..")
    #await bot.tree.clear_commands()
    guild = bot.get_guild(1377274564282679457)
    #await bot.tree.sync(guild=guild)
    await bot.tree.sync()
    for cmd in bot.tree.get_commands():
        log.bot(cmd.name)

async def execute_from_interaction(msg, interaction):
    ctx = await user.get_context(msg)
    # force context to behave like the selfbot
    ctx.author = user.user
    ctx.me = user.user

    # swap channel so sending uses selfbot HTTP client
    ctx.channel = user.get_channel(ctx.channel.id)

    # command name from slash command
    command_name = interaction.command.name

    cmd = user.get_command(command_name)
    if not cmd:
        return

    # collect slash command arguments automatically
    args = []
    args = list(interaction.namespace.__dict__.values())

    await cmd(ctx, *args)

bot.sync = sync
user.execute_interaction = execute_from_interaction

async def main():
    async with user, bot:
        for cog in [
            "usercogs." + f[:-3]
            for f in os.listdir("usercogs/")
            if os.path.isfile("usercogs/" + f) and f[-3:] == ".py"
        ]:
            print("Loading:", cog)
            try:
                await user.load_extension(cog)
            except:
                log.exception(f"Failed to load user cog {cog}.")

        for cog in [
            "botcogs." + f[:-3]
            for f in os.listdir("botcogs/")
            if os.path.isfile("botcogs/" + f) and f[-3:] == ".py"
        ]:
            print("Loading:", cog)
            try:
                await bot.load_extension(cog)
            except:
                log.exception(f"Failed to load bot cog {cog}.")

        await asyncio.gather(
            user.start(config.user_token),
            bot.start(config.bot_token)
        )

if __name__ == "__main__":
    asyncio.run(main())