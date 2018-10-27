# the non-vps star implementation

import discord
from discord.ext import commands
from io import BytesIO

class Stars:
    def __init__(self, bot):
        self.bot = bot

        # webhook info
        self.star_color = 0xffac33
        self.star_icon = "https://discordapp.com/assets/e4d52f4d69d7bba67e5fd70ffe26b70d.svg"
        self.star_emoji = u"\u2B50"
        self.star_topic = u"\U00002b50 1 \U000025CF (Emoji, star count)"
        self.webhook_icon = "https://cdn.discordapp.com/attachments/447786789563006986/494581408661110794/star.png"

        self.webhook_name = "Star"

    async def on_reaction_add(self, reaction, user):
        webhook = discord.utils.get(await reaction.message.guild.webhooks(), name = self.webhook_name)

        # user star info
        star_content = reaction.message.clean_content
        star_username = reaction.message.author.name
        star_avatar = reaction.message.author.avatar_url_as(format = "png")

        # star topic
        star_topic = webhook.channel.topic
        # star emoji
        star_emoji = star_topic.split()[0]
        # star count
        star_count = int(star_topic.split()[1])

        # if guild owner: can self star
        if user == reaction.message.guild.owner:
            pass
        # disallow bot stars
        elif user.bot:
            return
        # no selfstars for anyone else
        elif user == reaction.message.author:
            return
        # no starring webhooks
        elif reaction.message.webhook_id:
            return
        # no restarring
        elif reaction.count > star_count:
            return

        # if reaction count and emoji match the ones in the topic
        if reaction.count == star_count and reaction.emoji == star_emoji:
            star_embed = discord.Embed(
                color = self.star_color,
                timestamp = reaction.message.created_at
            )
            star_embed.add_field(name = "Author", value = reaction.message.author.mention, inline = True)
            star_embed.add_field(name = "Channel", value = reaction.message.channel.mention, inline = True)
            star_embed.set_footer(text = "Starred", icon_url = self.webhook_icon)

            # can't do over 10 embeds, remove oldest and add newest
            if len(reaction.message.embeds) <= 10:
                star_embeds = list(reaction.message.embeds[:9]) + [star_embed]
            else:
                star_embeds = list(reaction.message.embeds) + [star_embed]

            # no image
            if len(reaction.message.attachments) == 0:
                star_file = None
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

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        "Simple lazy help command."
        embed = discord.Embed(title = "Starboard Help", url = "https://github.com/Slick9000/emilia-stars", color = 0xFFFFFF)
        embed.add_field(name = "Setup", value = "Sets up the webhook used for stars.", inline = True)
        embed.add_field(name = "Edit", value = "Edits the star emoji and star count.", inline = True)
        embed.add_field(name = "Unsetup", value = "Unsetup the starboard.", inline = True)                     
        embed.set_author(name = self.bot.username)
                              
    @help.command()
    async def setup(self, ctx):
        await ctx.send("Sets up the starboard.\n"
                       "**Usage:** -starboard setup"
                      )
                              
    @help.command()
    async def edit(self, ctx):
        await ctx.send("Edits the star emoji and star count."
                       "**Usage:** -starboard edit {emoji} {star count}"
                      )
                              
    @help.command()
    async def unsetup(self, ctx):
        await ctx.send("Unsetup the starboard."
                       "**Usage:** -starboard unsetup"
                      )
            
    @commands.group(invoke_without_command=True)
    async def starboard(self, ctx):
        """Emilia's starboard"""

    @starboard.command()
    async def setup(self, ctx):
        """Sets up the webhook used for stars."""

        result = ''
        webhook = discord.utils.get(await ctx.channel.webhooks(), name = self.webhook_name)

        if webhook:
            await ctx.send("A starboard already exists!")
            return
        else:
            webhook = await ctx.channel.create_webhook(name = self.webhook_name)
            result += "{} Webhook `{}` successfully created.\n\n".format(u"\U00002705", webhook.name)
            if not webhook.channel.topic:
            	topic = await ctx.channel.edit(topic = self.star_topic)
            	result += u"\U00002705 Topic set.\nIn order to change the emoji and count, use the edit command.\nIt can also be manually changed."

        if result == '':
            await ctx.send("Setup already complete.")
        else:
            await ctx.send(result)

    @starboard.command()
    async def edit(self, ctx, emoji: str, count: int):
        """Edits the star emoji and star count."""

        await ctx.channel.edit(topic = f"{emoji} {count} \U000025CF (Emoji, star count)")

    @starboard.command()
    async def unsetup(self, ctx):
        """Unsetup the entire thing."""
        webhook = discord.utils.get(await ctx.channel.webhooks(), name = self.webhook_name)

        if webhook:
            await webhook.delete()
            await ctx.channel.edit(topic = None)
            await ctx.send("Stars successfully unsetup.")
        else:
            await ctx.send("Stars aren't even setup!")


def setup(bot):
    bot.add_cog(Stars(bot))
