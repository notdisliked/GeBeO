from discord.ext import commands
import discord
from helpers.filecmdhelper import *
import asyncio

class Sounds():
    def __init__(self, bot : commands.Bot):
        print("initializing sounds")
 
        if not os.path.exists("sounds"):
            os.makedirs("sounds")

        self.bot = bot
        self.currentVoiceChan = None

    currentVoiceChan = None

    def after_sound_clip(self, error):
        self.bot.loop.create_task(self.currentVoiceChan.disconnect())
        self.currentVoiceChan = None

    async def soundhandler(self, ctx, filename : str):
        vchan = ctx.message.author.voice.channel
        if vchan == None:
            await ctx.send("You're not in a voice channel!")
        else:
            self.currentVoiceChan = await vchan.connect()
            self.currentVoiceChan.play(discord.FFmpegPCMAudio(filename), after=self.after_sound_clip)

    @commands.command()
    async def slist(self, ctx):
        await filelister(ctx, "sounds")

    @commands.command()
    async def s(self, ctx):
        await ctx.trigger_typing()
        if self.currentVoiceChan != None:
            ctx.send("The bot is in use, wait your turn!")
        else:
            try:
                await filegetter(ctx, "sounds", self.soundhandler)
            except NoNameSpecifiedError:
                await ctx.send("No sound specified! If you are looking for a list of available sounds, run `!slist`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sadd(self, ctx):
        await ctx.trigger_typing()
        await fileadder(ctx, "sounds")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def srm(self, ctx):
        await ctx.trigger_typing()
        await fileremover(ctx, "sounds")

    @commands.command()
    async def sstop(self, ctx):
        for vc in self.bot.voice_clients:
            for m in vc.channel.members:
                if ctx.message.author == m:
                    await vc.disconnect()
                    return
        await ctx.send("You're not in a voice chat that the bot is in!")

    # @commands.command()
    # async def yt(self, ctx):
    #     await asyncio.sleep(0.25)
    #     await ctx.trigger_typing()
    #     vchan = ctx.message.author.voice.voice_channel
    #     if vchan == None:
    #         await self.bot.say("You're not in a voice channel!")
    #     else:
    #         voice = await self.bot.join_voice_channel(vchan)
    #         player = await voice.create_ytdl_player(ctx.arg, after=self.after_sound_clip)
    #         player.vc = voice
    #         player.start()

def setup(bot):
    print("setting up sounds")
    bot.add_cog(Sounds(bot))