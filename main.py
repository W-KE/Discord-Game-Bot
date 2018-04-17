import discord
from discord.ext import commands

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='$', description=description)
owner = None
preparing = False
playing = False
players = []
min_players = 0
game = None


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def start(ctx, name=""):
    global owner, preparing, players, game, min_players
    if not preparing and not playing:
        if name == "":
            await bot.say("人数不足")
            return
        owner = ctx.message.author
        preparing = True
        players = [owner]
        if name == "谁是卧底":
            min_players = 3
        await bot.say(
            "{} 想要开始游戏，输入 $join 加入，玩家加入后 {} 输入 $go 开始".format(ctx.message.author.mention, ctx.message.author.mention))
    elif preparing and not playing:
        if ctx.message.author != owner:
            await bot.say("只有主持人可以开始游戏")
            return
        if len(players) >= min_players:
            if len(players) < 7:
                game = undercover.Game(players, 2)
            else:
                game = undercover.Game(players, 3)
            await bot.say("本局游戏共有{}人参加".format(len(players)))
        else:
            await bot.say("人数不足")
    else:
        await bot.say("游戏已经开始，等待下一局")


@bot.command(pass_context=True)
async def join(ctx):
    global players
    if playing:
        await bot.say("游戏已经开始，等待下一局")
        return
    if ctx.message.author in players:
        await bot.say("你已经在游戏中了，不要重复加入")
    else:
        if preparing:
            players.append(ctx.message.author)
            await bot.say("{} 加入了游戏".format(ctx.message.author.mention))
        else:
            await bot.say("没有进行中的游戏,输入 $start 开始新游戏")


@bot.command(pass_context=True)
async def move(ctx, option):
    if preparing:
        await bot.say("游戏已经开始，等待下一局")
        return
    if playing:
        if ctx.message.author in players:
            pass
        else:
            await bot.say("你不在游戏中了，等待下一局")
            return


@bot.command(pass_context=True)
async def poll(ctx, question, *options: str):
    emoji = [":dog:", ":cat:", ":mouse:", ":hamster:", ":rabbit:", ":bear:", ":panda_face:", ":koala:", ":tiger:",
             ":lion_face:", ":cow:", ":pig:", ":frog:", ":octopus:", ":chicken:", ":wolf:", ":boar:"]
    if len(options) <= 1:
        await bot.say('You need more than one option to make a poll!')
        return
    if len(options) > 10:
        await bot.say('You cannot make a poll for more than 10 things!')
        return
    reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
    embed = discord.Embed(title=question, description="")
    react_message = await bot.say(embed=embed)
    for reaction in reactions[:len(options)]:
        await bot.add_reaction(react_message, reaction)
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await bot.edit_message(react_message, embed=embed)


@bot.command(pass_context=True)
async def tally(ctx, id):
    poll_message = await bot.get_message(ctx.message.channel, id)
    if not poll_message.embeds:
        return
    embed = poll_message.embeds[0]
    if poll_message.author != ctx.message.server.me:
        return
    if not embed['footer']['text'].startswith('Poll ID:'):
        return
    unformatted_options = [x.strip() for x in embed['description'].split('\n')]
    opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
        else {x[:1]: x[2:] for x in unformatted_options}
    # check if we're using numbers for the poll, or x/checkmark, parse accordingly
    voters = [ctx.message.server.me.id]  # add the bot's ID to the list of voters to exclude it's votes

    tally = {x: 0 for x in opt_dict.keys()}
    for reaction in poll_message.reactions:
        if reaction.emoji in opt_dict.keys():
            reactors = await bot.get_reaction_users(reaction)
            for reactor in reactors:
                if reactor.id not in voters:
                    tally[reaction.emoji] += 1
                    voters.append(reactor.id)

    output = 'Results of the poll for "{}":\n'.format(embed['title']) + \
             '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
    await bot.say(output)


@bot.group(pass_context=True)
async def cool(ctx):
    """
    Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='Poker')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the Poker is cool.')


bot.run('NDM1NjU5MjUwNDcyMzIxMDI0.DbcK0Q.0HLUlvcDpuDXN8a8TZUXF14bH1w')
