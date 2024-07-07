import discord
import bot_main
from discord.ext import commands
from discord import app_commands

embed_group = app_commands.Group(name="embed", description="Embed related commands")
embed_edit_group = app_commands.Group(name="edit", description="Edit an existing embed.", parent=embed_group)

@embed_group.command(name="create", description="Create a simple embed.")
@app_commands.describe(color = "What color should the embed be? Use Hexadecimal, no #.")
@app_commands.describe(title = "What is the title of the embed?")
@app_commands.describe(desc = "What do you want to write in your embed?")
async def embed_create(interaction: discord.Interaction, color: str, title: str, desc: str):
    try:
        newEmbed = discord.Embed(title=title, description=desc, color=int(color, 16))
        print(interaction.user.display_name)
        await interaction.channel.send(embed=newEmbed)
        await interaction.response.send_message("Here is your embed. Use /embed edit to change it.", ephemeral=True)
    except ValueError as e:
        await interaction.response.send_message(f"{color} is not a valid color! Please use Hexadecimal with no #. (ffffff for white)")

@embed_edit_group.command(name="title", description="Edit the title of an existing embed.")
@app_commands.describe(message_id = "The Message ID of the embed you want to edit")
@app_commands.describe(new_title = "The new title you wish to use.")
async def embed_edit_title(interaction: discord.Interaction, message_id: str, new_title: str):
    try:
        message = await interaction.channel.fetch_message(message_id)
        if not message.embeds:
            await interaction.response.send_message("That message isn't an embed!", ephemeral=True)
        else:
            embed = message.embeds[0]
            embed.title = new_title
            
            await message.edit(embed=embed)
            await interaction.response.send_message("Embed title changed!", ephemeral=True)

    except discord.NotFound:
        await interaction.response.send_message("I couldn't find a message with that ID!", ephemeral = True)