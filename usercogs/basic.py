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
    async def petpet(self, ctx, user: selfcord.User):
        channel = self.user.get_channel(ctx.channel.id)
        await channel.send(f'https://tt7homa.eu.pythonanywhere.com/petpet.gif?image={user.avatar.url}')

    @commands.command()
    async def colors(self, ctx, color1, color2=None, color3=None, mixmode='Average'):
        channel = self.user.get_channel(ctx.channel.id)
        coloramount = 3 if color2 and color3 else 2 if color2 or color3 else 1
        color1rgb = color1.lstrip('#')
        if len(color1) == 3:
            color1rgb = "".join([c*2 for c in color1rgb])
        color1rgb = tuple(int(color1rgb[i:i+2], 16) for i in (0, 2, 4))
        if color2:
            color2rgb = color2.lstrip('#')
            if len(color2) == 3:
                color1rgb = "".join([c*2 for c in color1rgb])
            color2rgb = tuple(int(color2rgb[i:i+2], 16) for i in (0, 2, 4))
        else color2rgb = (0,0,0)
        if color3:
            color3rgb = color3.lstrip('#')
            if len(color3) == 3:
                color3rgb = "".join([c*2 for c in color3rgb])
            color3rgb = tuple(int(color3rgb[i:i+2], 16) for i in (0, 2, 4))
        else: 
            color3rgb = (0,0,0)
        
        if mixmode == 'Average':
            colorresult = ((color1rgb[0]+color2rgb[0]+color3rgb[0])/coloramount, (color1rgb[1]+color2rgb[1]+color3rgb[1])/coloramount, (color1rgb[2]+color2rgb[2]+color3rgb[2])/coloramount)
        elif mixmode == 'Additive':
            maxcolor = max(color1rgb[0]+color2rgb[0]+color3rgb[0], color1rgb[1]+color2rgb[1]+color3rgb[1], color1rgb[2]+color2rgb[2]+color3rgb[2], 255)
            colorresult = (((color1rgb[0]+color2rgb[0]+color3rgb[0])/maxcolor)*255,((color1rgb[1]+color2rgb[1]+color3rgb[1])/maxcolor)*255,((color1rgb[2]+color2rgb[2]+color3rgb[2])/maxcolor)*255)
        elif mixmode == 'Subtractive':
            maxcolor = max((255-color1rgb[0])+(255-color2rgb[0])+(255-color3rgb[0]), (255-color1rgb[1])+(255-color2rgb[1])+(255-color3rgb[1]), (255-color1rgb[2])+(255-color2rgb[2])+(255-color3rgb[2]))
            colorresult = (255-(((255-color1rgb[0])+(255-color2rgb[0])+(255-color3rgb[0])/maxcolor)*255),255-(((255-color1rgb[1])+(255-color2rgb[1])+(255-color3rgb[1])/maxcolor)*255),255-(((255-color1rgb[2])+(255-color2rgb[2])+(255-color3rgb[2])/maxcolor)*255))

        hexcode = "#{:02x}{:02x}{:02x}".format(*colorresult)
        channel.send(f"https://singlecolorimage.com/get/{hexcode}/100x100")
async def setup(user):
    await user.add_cog(Basic(user, bot))
    