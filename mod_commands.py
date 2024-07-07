import discord
from discord.ext import commands
from discord import app_commands

banword_group = app_commands.Group(name="banword", description="Banning/Unbanning Words")

@banword_group.command(name="add", description="Add a word to the banlist.")
@app_commands.describe(word="What word do you want to ban?")
async def add_banword(interaction: discord.Interaction, word: str):
    with open('banned_words.txt', 'a+') as file:
        file.seek(0)
        banlist = file.read().split(',')
        if word in banlist:
            await interaction.response.send_message(f"{word} is already in the banlist!", ephemeral=True)
        else:
            file.seek(0, 2)
            file.write(f"{word},")
            await interaction.response.send_message(f"{word} has been added to the banlist.", ephemeral=True)

class ModCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author != self.bot.user:
            await self.checkBanlist(msg)
                    
    @commands.Cog.listener()
    async def on_message_edit(self, before, msg):
        await self.checkBanlist(msg)
                
    async def checkBanlist(self, msg):
        try:
            with open('banned_words.txt', 'r') as file:
                banlist = file.read().split(',')
                banlist = banlist[:-1]
                for word in banlist:
                    if word in str(msg.content.lower()):
                        await msg.delete()
                        return
        except FileNotFoundError as e:
            open('banned_words.txt', 'w').close()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot has started!")

async def setup(bot):
    await bot.add_cog(ModCommands(bot))
    bot.tree.add_command(banword_group)
    print("Moderation Commands were loaded!")