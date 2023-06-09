# starboard
non-vps discord starboard implementation using webhooks and channel topics.

## what is this
most starboard use a database/vps to store the data for being enabled/disabled as well as the reaction count of a message. i wanted to be different (as i did not have access to a db at the time) and use channel topics to perform this task.

i also decided to use webhooks to emulate the look of a regular user for the starboard, similar to my other bot, [reminisce](https://github.com/Slick9000/reminisce).

## invite
it runs through the same bot as [r3ddit](https://github.com/Slick9000/r3dd1t), so you can invite it if you want [here](https://discord.com/oauth2/authorize?client_id=459552609108230158&scope=bot&permissions=8)

## ☕ donations

while completely optional, it would be highly appreciated if you could donate if you like this bot! it can be of any amount.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/irbee246)

## usage
**enable:** enables the starboard and sets the channel topic. by default, the channel topic will be a star emoji (⭐) and the number 1

⭐ 1

the emoji set determines what emoji reaction will trigger the starboard, and the number is how many of these reactions it will take for the comment to be starred.

**edit:** changes the emoji and reaction count. it can be changed manually by changing the channel topic.

**NOTE:** a discord api change (for no reason) has now made it that there is a 10 minute rate limit on changing channel topics. i cannot avoid this or circumvent this, so if you wish to change the channel topic within a 10 minute time frame, you will have to manually change the channel topic yourself. we love discordapp.

**disable:** disables the starboard (deleting the webhook and setting the channel topic to be blank)

## why did i make this
i just thought the idea would be cool. other starboards use databases to store data for each guild, and i wanted to be different and push the limits by using just what is available within discord.

also, by using webhooks, it makes the starred posts repost with the user's profile picture and name, which i thought was a pretty cool idea.
