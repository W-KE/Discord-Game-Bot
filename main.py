import discord
from discord.ext import commands

import undercover

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
poll_id = ""


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def start(ctx, name="谁是卧底"):
    global owner, preparing, players, game, min_players, poll_id, playing
    if not preparing and not playing:
        preparing = True
        playing = False
        game = None
        poll_id = ""
        if name == "":
            await bot.say("用法\n$start 谁是卧底")
            return
        owner = ctx.message.author
        preparing = True
        players = [owner]
        if name == "谁是卧底":
            min_players = 2
        await bot.say(
            "{} 想要开始游戏，输入 $join 加入，玩家加入后 {} 输入 $start 开始".format(ctx.message.author.mention, ctx.message.author.mention))
    elif preparing and not playing:
        if ctx.message.author != owner:
            await bot.say("只有主持人可以开始游戏")
            return
        if len(players) >= min_players:
            if len(players) < 7:
                game = undercover.Game(players, 2)
            else:
                game = undercover.Game(players, 3)
            preparing = False
            playing = True
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


@bot.command()
async def poll(question="谁是卧底?", *options: str):
    global poll_id
    if len(options) == 0:
        options = [i.user.mention for i in game.players if not i.out]
    if len(options) <= 1:
        await bot.say("至少需要两人开始投票")
        return
    if len(options) > 10:
        await bot.say("最多十人参加投票")
        return
    reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
    description = []
    for x, option in enumerate(options):
        description += '\n{} {}'.format(reactions[x], option)
    embed = discord.Embed(title=question, description="".join(description))
    react_message = await bot.say(embed=embed)
    for reaction in reactions[:len(options)]:
        await bot.add_reaction(react_message, reaction)
    poll_id = react_message.id
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await bot.edit_message(react_message, embed=embed)


@bot.command(pass_context=True)
async def tally(ctx):
    poll_message = await bot.get_message(ctx.message.channel, poll_id)
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

    output = '"{}"投票结果:\n'.format(embed['title'])
    max_player = 0
    max_poll = 0
    max_count = 0
    for key in tally.keys():
        if tally[key] > max_poll:
            max_poll = tally[key]
            max_count = 1
            max_player = key
        elif tally[key] == max_poll:
            max_count += 1
        output += "\n{}: {}".format(opt_dict[key], tally[key])
    await bot.say(output)
    if max_count > 1:
        await bot.say("投票相同，待定")
    else:
        for i in game.players:
            if not i.out:
                if i.user.mention == opt_dict[max_player]:
                    i.out = True
                    if i.uc:
                        await bot.say("卧底 {} 被淘汰\n卧底词：{}\n平民词：{}\n平民获胜".format(opt_dict[max_player], game.undercover, game.normal))
                        return
        await bot.say("{} 被淘汰".format(opt_dict[max_player]))
    alive = [i.user.mention for i in game.players if not i.out]
    if len(alive) <= game.win:
        for i in alive:
            if i.uc:

                await bot.say("卧底词：{}\n平民词：{}\n卧底 {} 获胜".format(game.undercover, game.normal, i.user.mention))


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
