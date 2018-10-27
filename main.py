import discord
from discord.ext import commands
import os, sys, traceback

initial_extensions = ["stars"]

bot = commands.Bot(command_prefix="-", case_insensitive=True)
bot.remove_command(help)

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Failed to load extension {e}.", file=sys.stderr)
        traceback.print_exc()


@bot.event
async def on_ready():
    print(f"Logging in as...\n{bot.user}")
    print(f"Connected to { len(bot.guilds) } servers")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"{len(bot.guilds)} servers"))


if __name__ == '__main__':
    bot.run(os.environ['TOKEN'])
