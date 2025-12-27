from discord.ext import commands

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency: {self.bot.latency * 1000:.2f} ms")

async def setup(bot):
    await bot.add_cog(GeneralCog(bot))
