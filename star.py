# the non-vps star implementation

import discord
from discord.ext import commands
from io import BytesIO
import re

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix="-s ", intents=intents, case_insensitive=True)

bot.remove_command("help")

# webhook info
star_color = 0xffac33

star_icon = "https://cdn.discordapp.com/attachments/1104105181194498058/1104122478453866526/star.png"

star_emoji = u"\u2B50"

star_topic = u"\U00002b50 1 \U000025CF (Emoji, star count)"

webhook_name = "Star"

@bot.event
async def on_ready():

    print(f"\nLogging in as...\n{bot.user}")

    print(f"Connected to { len(bot.guilds) } servers")

    await bot.change_presence(
        activity=discord.Activity(
            name="prefix -s", type=discord.ActivityType.watching
        )
    )

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):

    global star_icon

    if payload.guild_id is None:

        return

    guild = bot.get_guild(payload.guild_id)

    if guild is None:

        return

    channel = guild.get_channel(payload.channel_id) or await guild.fetch_channel(payload.channel_id)

    try:

        message = await channel.fetch_message(payload.message_id)

    except (discord.NotFound, discord.Forbidden):

        return

    user = payload.member or guild.get_member(payload.user_id)

    if user is None:

        try:

            user = await guild.fetch_member(payload.user_id)

        except discord.NotFound:

            return

    if user.bot:

        return

    if message.webhook_id:

        return

    webhook = discord.utils.get(await guild.webhooks(), name=webhook_name)

    if webhook is None:

        return

    star_content = message.clean_content

    star_username = message.author.display_name

    star_avatar = message.author.avatar

    star_topic = webhook.channel.topic

    if not star_topic:

        return

    star_emoji = star_topic.split()[0]

    if star_emoji.startswith("<"):

        emoji_regex = re.findall(r'(?<=\:)(.*?)(?=\:)', star_emoji)[0]

        find_emoji = discord.utils.get(guild.emojis, name=emoji_regex)

        if find_emoji:

            star_icon = find_emoji.url

    star_count = int(star_topic.split()[1])

    # find the matching reaction on the fetched message to get an accurate count
    target = discord.utils.find(lambda r: str(r.emoji) == str(payload.emoji), message.reactions)

    if target is None:

        return

    if user != guild.owner:

        pass

    elif user == message.author:

        return

    if target.count > star_count:

        return

    if target.count == star_count and str(payload.emoji) == str(star_emoji):

        star_embed = discord.Embed(color=star_color, timestamp=message.created_at)

        star_embed.add_field(name="Author", value=message.author.mention, inline=True)

        star_embed.add_field(name="Link", value=message.jump_url, inline=True)

        star_embed.set_footer(text="Starred", icon_url=star_icon)

        if len(message.embeds) <= 10:

            star_embeds = list(message.embeds[:9]) + [star_embed]

        else:

            star_embeds = list(message.embeds) + [star_embed]

        if not message.attachments:
            await webhook.send(
                content=star_content,
                embeds=star_embeds,
                username=star_username,
                avatar_url=star_avatar
            )

        else:

            fp = BytesIO()
            attachment = message.attachments[0]
            await attachment.save(fp)
            fp.seek(0)
            star_file = discord.File(fp=fp, filename=attachment.filename)

            await webhook.send(
                content=star_content,
                embeds=star_embeds,
                file=star_file,
                username=star_username,
                avatar_url=star_avatar
            )

@bot.command()
async def help(ctx):
    """The reddit command."""

    embed = discord.Embed()

    embed.add_field(
        name="Enable",
        value="Enables the starboard by creating a webhook and editing the channel topic. "
        "By default, it sets the emoji to a star and the reaction count to 1."
    )

    embed.add_field(
        name="Disable",
        value="Removes the webhook and resets the channel topic.",
    )

    embed.add_field(
        name="Edit",
        value="Edits the starboard emoji and reaction count. Due to a ratelimit issue, you can only "
        "use this command twice every 10 minutes.\n\nYou can however, manually edit the channel topic to change "
        "the reaction emoji and reaction count required."
    )
    
    embed.add_field(
        name="Starboard",
        value="Starboard using webhooks and channel topics.\n\nLooks nice, works easily. Command prefix **-s**"
    )

    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1104105181194498058/1104122478453866526/star.png"
    )

    await ctx.send(embed=embed)

@bot.command()
async def enable(ctx):
    """Enables and sets up the webhook used for stars."""

    result = ''
    
    webhook = discord.utils.get(await ctx.channel.webhooks(), name = webhook_name)

    if webhook:

        await ctx.send("A starboard already exists!")

        return
    
    else:

        webhook = await ctx.channel.create_webhook(name = webhook_name)

        result += "{} Webhook `{}` successfully created.\n\n".format("\U00002705", webhook.name)

        if not webhook.channel.topic:

            topic = await ctx.channel.edit(topic = star_topic)

            result += '\U00002705 Topic set.\nIn order to change the emoji and count, use the edit command.'
            '**NOTE:** Due to a Discord API change, you will not be able to use the `edit` or `disable`'
            'commands due to a 10 minute ratelimit. This cannot be circumvented. \n\nYou can however change the'
            'topic manually if you desire to change it within this time frame.'

    if result == '':

        await ctx.send("Setup already complete.")

    else:

        await ctx.send(result)

@bot.command()
async def edit(ctx, *args):
    """Edits the star emoji and star count."""

    if len(args) < 1:
        await ctx.send("Please provide an emoji!")
        return

    if len(args) < 2:
        await ctx.send("Please provide an integer!")
        return

    webhook = discord.utils.get(await ctx.guild.webhooks(), name=webhook_name)

    if webhook is None:
        await ctx.send("Stars aren't set up! Run `-s enable` in your starboard channel first.")
        return

    await webhook.channel.edit(topic=f"{args[0]} {int(args[1])} \U000025CF (Emoji, star count)")

    await ctx.send(f"Topic edited in {webhook.channel.mention}!")

@bot.command()
async def disable(ctx):
    """Disable starboard."""

    webhook = discord.utils.get(await ctx.guild.webhooks(), name = webhook_name)

    if not webhook:
        await ctx.send("Stars aren't set up!")
    else:
        await webhook.channel.edit(topic = None)
        await webhook.delete()
        await ctx.send("Stars successfully disabled.")


token = open("token.txt").read()
 
if __name__ == '__main__':

    bot.run(token)
