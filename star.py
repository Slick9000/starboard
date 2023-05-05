# the non-vps star implementation

import discord
from discord.ext import commands
from io import BytesIO
import os

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix="-", intents=intents, case_insensitive=True)

# webhook info
star_color = 0xffac33

star_icon = "https://discordapp.com/assets/e4d52f4d69d7bba67e5fd70ffe26b70d.svg"

star_emoji = u"\u2B50"

star_topic = u"\U00002b50 1 \U000025CF (Emoji, star count)"

webhook_icon = "https://cdn.discordapp.com/attachments/447786789563006986/494581408661110794/star.png"

webhook_name = "Star"

@bot.event
async def on_ready():

    print(f"\nLogging in as...\n{bot.user}")

    print(f"Connected to { len(bot.guilds) } servers")

@bot.event
async def on_reaction_add(reaction, user):

        webhook = discord.utils.get(await reaction.message.guild.webhooks(), name = webhook_name)

        # user star info
        star_content = reaction.message.clean_content

        star_username = reaction.message.author.name

        star_avatar = reaction.message.author.avatar

        # star topic
        star_topic = webhook.channel.topic

        # star emoji
        star_emoji = star_topic.split()[0]

        # star count
        star_count = int(star_topic.split()[1])

        # disallow bot stars
        if user.bot:

            return
        
        # no starring webhooks
        if reaction.message.webhook_id:

            return
        
        # no restarring
        if reaction.count > star_count:

            return

        # if reaction count and emoji match the ones in the topic
        if reaction.count == star_count and reaction.emoji == star_emoji:

            star_embed = discord.Embed(

                color = star_color,

                timestamp = reaction.message.created_at
            )
            star_embed.add_field(name = "Author", value = reaction.message.author.mention, inline = True)

            star_embed.add_field(name = "Channel", value = reaction.message.channel.mention, inline = True)

            star_embed.set_footer(text = "Starred", icon_url = webhook_icon)

            # can't do over 10 embeds, remove oldest and add newest
            if len(reaction.message.embeds) <= 10:

                star_embeds = list(reaction.message.embeds[:9]) + [star_embed]

            else:

                star_embeds = list(reaction.message.embeds) + [star_embed]

            # no image
            if reaction.message.attachments == []:

                await webhook.send(
                content    = star_content,
                embeds     = star_embeds,
                username   = star_username,
                avatar_url = star_avatar
                )
                
            else:

                fp = BytesIO()

                attachment = reaction.message.attachments[0]

                await attachment.save(fp)
                
                star_file = discord.File(fp = fp, filename = attachment.filename)

                await webhook.send(
                    content    = star_content,
                    embeds     = star_embeds,
                    file       = star_file,
                    username   = star_username,
                    avatar_url = star_avatar
                )

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

        result += "{} Webhook `{}` successfully created.\n\n".format(u"\U00002705", webhook.name)

        if not webhook.channel.topic:

            topic = await ctx.channel.edit(topic = star_topic)

            result += 'u"\U00002705 Topic set.\nIn order to change the emoji and count, use the edit command.'
            '**NOTE:** Due to a Discord API change, you will not be able to use the `edit` or `disable`'
            'commands due to a 10 minute ratelimit. This cannot be circumvented. \n\nYou can however change the'
            'topic manually if you desire to change it without this time frame.'

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

    await ctx.channel.edit(topic = f"{args[0]} {int(args[1])} \U000025CF (Emoji, star count)")

    await ctx.send("Channel topic edited!")

@bot.command()
async def disable(ctx):
    """Disable starboard."""

    webhook = discord.utils.get(await ctx.channel.webhooks(), name = webhook_name)

    if not webhook:

        await ctx.send("Stars aren't set up!")

    else:

        await ctx.channel.edit(topic = None)

        await webhook.delete()

        await ctx.send("Stars successfully disabled.")


if __name__ == '__main__':
    bot.run(os.environ['TOKEN'])
