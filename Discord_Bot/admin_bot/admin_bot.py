#admin_bot
import asyncio
from email.policy import default
import os
from unicodedata import category
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


#Bot Commands
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
    
@bot.command(name='role', help='Displays a list of roles and let\'s the user assign himself a role')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)]
    await ctx.send(','.join(dice))


#Creating a new channel
@bot.command(name='cc', help='creates a channel within a category if specified.\n usage: $cc <channel> <category>')
@commands.has_any_role('Normy', 'TTRPG Players')
async def create_channel(ctx, channel_name = commands.parameter(description='the name of the channel'), category_name = commands.parameter(default=None, description='specifies in which category to create the channel (optional)')):
    """
    channel_name: the name of the channel
    category_name: specifies in which category to create the channel (optional)
    Creates a new channel. Optionally can choose a category to create in. If the category
    doesn't exists it will ask the user to create one."""    

    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    user = ctx.author
    print(f'{user.name} is trying to create a new channel ({channel_name})')
    
    if category_name is None:   #Checks if category parameter is empty
            if not existing_channel:
                print(f'{user.name} created a new channel: {channel_name}')
                await guild.create_text_channel(channel_name)
                await ctx.send(f'Channel {discord.utils.get(guild.channels, name=channel_name).mention} created')
            else:
                print(f'{user.name} is trying to create a channel that already exists')
                await ctx.send(f'Channel {existing_channel.mention} already exists')
                
    else:
        existing_category = discord.utils.get(guild.categories, name=category_name)
        if not existing_category:
            print(f'{user.name} is trying to create a new category')
            await ctx.send(f'{category_name} does not exist. Do you want to create it? (y/n)')
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['y','n']
            try:
                msg = await bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send('Sorry, you did not reply in time.')
                return
            
            if msg.content.lower() == 'y':
                existing_category = await guild.create_category(category_name)
                print(f'{user.name} created a new category {category_name}')
            else:
                await ctx.send(f'Operation aborted.')
                return
       
        if not existing_channel:
            print(f'{user.name} created a new channel ({channel_name}) in {category_name}')
            await guild.create_text_channel(channel_name, category=existing_category)
            await ctx.send(f'Channel {discord.utils.get(guild.channels, name=channel_name).mention} created')
        else:
            await ctx.send(f'Channel {existing_channel.mention} already exists')

bot.run(TOKEN)
