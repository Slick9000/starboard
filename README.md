starboard
my non-vps discord starboard implementation using webhooks and channel topics.

## usage
**enable:** enables the starboard and sets the channel topic. by default, the channel topic will be a star emoji (⭐) and the number 1

⭐ 1

the emoji set determines what emoji reaction will trigger the starboard, and the number is how many of these reactions it will take for the comment to be starred.

this can be changed using the **edit** command, or it can be changed manually by changing the channel topic.

**NOTE:** a discord api change has now made it that there is a 10 minute rate limit on changing channel topics. i cannot avoid this or circumvent this, so if you wish to change the channel topic within this 10 minute time frame, you will have to manually change the channel topic yourself.

**disable:** disables the starboard (deleting the webhook and setting the channel topic to be blank)

## why did i make this
i just thought the idea would be cool. other starboards use servers to store data for each guild, and i wanted to be different and push the limits by using just what is available within discord.

also, by using webhooks, it makes the starred posts repost with the user's profile picture and name, which i thought was a pretty cool idea. in the future, i want to create a server mirroring service doing this same thing (it has been done before, but i want to do it better)
