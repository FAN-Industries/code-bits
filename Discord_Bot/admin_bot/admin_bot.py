#admin_bot
import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands


#environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


#Custom bot class extends from Client
class CustomBot(commands.Bot):
    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=GUILD)
        print(f'{self.user} is connected to the following guild:\n' f'{guild.name}(id:{guild.id})\n')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
        
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to Adrian\'s server!')

    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command')
            
bot = CustomBot(intents=intents, command_prefix='$')


#Commands
@bot.command(name='99', help='test help')
async def nine_nine(ctx):
    brooklyn_99_quotes = ['I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    (
        'Cool. Cool cool cool cool cool cool cool, '
        'no doubt no doubt no doubt no doubt.'
    ),]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
    
@bot.command(name='roll_dice', help='rolls a number of dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)]
    await ctx.send(','.join(dice))

@bot.command(name='cc', help='creates a channel')
@commands.has_any_role('Normy', 'TTRPG Players')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

bot.run(TOKEN)
