from selfcord.ext.commands import Cog
from selfcord.ext import commands
from __main__ import bot
import selfcord
import datetime
from __main__ import sync

class Basic(Cog):
    def __init__(self, user, bot):
        self.user = user
        self.bot = bot
    
    @commands.command(aliases=['sync'])
    async def _sync(self, ctx):
        await self.bot.sync()
        await ctx.send("Commands synced! New commands could take up to an hour to show.")


    @commands.command()
    async def time(self, ctx):
        now =  datetime.datetime.now()
        await ctx.send(f"It is {now.strftime('%H:%M')} for me right now.")

    @commands.command()
    async def petpet(self, ctx, user: selfcord.Member):
        channel = self.user.get_channel(ctx.channel.id)
        await channel.send(f'https://tt7homa.eu.pythonanywhere.com/petpet.gif?image={user.avatar.url}')
        

async def setup(user):
    await user.add_cog(Basic(user, bot))
    