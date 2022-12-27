import discord
from discord.ext import commands
from case_group import case_group
import asyncio
import time
from dotenv import load_dotenv
import os 

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

case_group_s = {}

@bot.command()
async def 어시스턴트(ctx):
    await ctx.send('네')

@bot.command()
async def 게임설정(ctx):
    await ctx.send('게임 설정을 시작합니다.')

@bot.command()
async def 사건목록(ctx):
    string = ''
    for key in case_group_s:
        string += str(key) + '\n'
    await ctx.send(case_group_s)

@bot.command()
async def 사건목록열기(ctx, *, arg):
#[function]↓[function]↓[function]↓[function]↓[function]↓[function]↓[function]↓[function]
    def check(msg):
        return True
    
    async def do_msg_countdown(handle, string, max_time):
        
        start = time.time()
        time_passd = 0
        while (time_passd) < max_time:
            time.sleep(1)
            time_passd = time.time() - start
            string += str(round(max_time - time_passd, 1))
            await handle.edit(content = string)
#[function]↑[function]↑[function]↑[function]↑[function]↑[function]↑[function]↑[function]
    max_time = 20
    
    if arg not in case_group_s:
        await ctx.send('없는 사건목록입니다.')
        return
    string = arg + '\n'

    case_group = case_group_s[arg]
    
    for i, member in enumerate(case_group.case):
        string += '>   ' + member + ':  ' + str(case_group.difficulty[i]) + '\n'

    string += '\"확률공개\"  ' + '\"결정\"  ' + '\"나가기\"  '
    msg = await ctx.send(string)

    while True:
        countdown = asyncio.create_task(do_msg_countdown(msg, string, max_time))

        try:
            response = await bot.wait_for("message", check = check, timeout = max_time)
        except asyncio.TimeoutError:
            await ctx.send('시간초과')
            countdown.cancel()
            break

        countdown.cancel()
    
        if response.content == '확률공개':
            await ctx.send(case_group.chance)

        elif response.content == '결정':
            case_group.decide_case()
            await ctx.send(case_group.decided)

        elif response.content == '나가기':
            break

@bot.command()
async def nice(ctx):
    await ctx.send('You, too :)')

@bot.command()
async def 아(ctx):
    await ctx.send('이거 참 ㅈㅗㅣㅅㅗㅇ하네요? ʅcᶿ ωᶿʖʃ')

@bot.command()
async def 자폭(ctx):
    T_minus = 18
    msg = await ctx.send('18.0')

    start = time.time()
    time_passd = 0
    while (time_passd) < T_minus:
        time.sleep(1)
        time_passd = time.time() - start
        string = str(round(T_minus - time_passd, 1))
        await msg.edit(content = string)

@bot.command()
async def 새사건목록(ctx, *args):
#[function]↓[function]↓[function]↓[function]↓[function]↓[function]↓[function]↓[function]
    def check(msg):
        return True

    def do_msg_list(handle, cases):
        string = '>난이도:\n'
        for i, member in enumerate(cases.case):
            string += '>    ' + str(cases.case[i]) + ': '
            if cases.difficulty[i] >= 0:
                string += str(cases.difficulty[i]) + '\n'
            else:
                string += '\n'

        return handle.edit(content = string)

    async def do_msg_countdown(loop, handle, cases, pos, max_time):
        
        start = time.time()
        time_passd = 0
        while (time_passd) < max_time:
            time.sleep(1)
            time_passd = time.time() - start
            string = str(cases.case[pos]) + '부터:      ' + str(round(max_time - time_passd, 1)) + '  \"나가기\"'
            await handle.edit(content = string)
#[function]↑[function]↑[function]↑[function]↑[function]↑[function]↑[function]↑[function]

    max_time = 20 #20 seconds to reply
    new_group = case_group.Case_group(args)
 
    notification_1_handle = await ctx.send('not an empty message')
    notification_2_handle = await ctx.send('not an empty message')

    loop = asyncio.get_event_loop()
    
    while True:
        for i, member in enumerate(new_group.case):
            await do_msg_list(notification_1_handle, new_group)

            countdown = asyncio.create_task(do_msg_countdown(loop, notification_2_handle, new_group, i, max_time))

            try:
                message_in = await bot.wait_for("message", check = check, timeout = max_time)
            except asyncio.TimeoutError:
                await ctx.send('시간초과')
                countdown.cancel()
                break

            countdown.cancel()
            new_group.difficulty[i] = float(message_in.content)
        
        await do_msg_list(notification_1_handle, new_group)
        
        await ctx.send('\"!재설정\" 또는 저장할 이름')
        message_in = await bot.wait_for("message", check = check)
        if message_in.content == "!재설정":
            continue
        else:
            case_group_s.update({message_in.content : new_group})
            await ctx.send('저장완료')
            break
bot.run(TOKEN)
