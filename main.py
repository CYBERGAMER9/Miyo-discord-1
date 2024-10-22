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

@bot.tree.command(name='mute', description='Mute a user')
async def mute(interaction: discord.Interaction, user: discord.Member):
    # Here you would implement the mute logic (e.g., adding a mute role)
    await interaction.response.send_message(f'{user} has been muted.', ephemeral=True)

@bot.tree.command(name='unmute', description='Unmute a user')
async def unmute(interaction: discord.Interaction, user: discord.Member):
    # Here you would implement the unmute logic
    await interaction.response.send_message(f'{user} has been unmuted.', ephemeral=True)

# Help command to display all commands with descriptions
@bot.tree.command(name='help', description='Display help information for all commands')
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Help - Bot Commands", color=discord.Color.blue())
    embed.add_field(name="!ban", value="Ban a user from the server.", inline=False)
    embed.add_field(name="!unban <user_id>", value="Unban a user by their ID.", inline=False)
    embed.add_field(name="!kick", value="Kick a user from the server.", inline=False)
    embed.add_field(name="!mute", value="Mute a user.", inline=False)
    embed.add_field(name="!unmute", value="Unmute a user.", inline=False)
    embed.set_footer(text="Use the commands with proper permissions.")

    await interaction.response.send_message(embed=embed, ephemeral=True)

# Prefix-based owner-only command to reload slash commands
@bot.command(name='reload_slash')
async def reload_slash(ctx):
    # Check if the command issuer is the bot owner
    if ctx.author.id == 1169487822344962060:  # Replace with your bot owner's ID
        await bot.tree.sync()  # Reload all slash commands
        await ctx.send('Slash commands reloaded successfully!')
    else:
        await ctx.send('You do not have permission to use this command.', ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    await bot.tree.sync()

# Function to run Flask app
def run_flask():
    app.run(host='0.0.0.0', port=3000)  # Replit uses port 3000

# Start Flask app in a separate thread
Thread(target=run_flask).start()

# Run the Discord bot
bot.run(TOKEN)