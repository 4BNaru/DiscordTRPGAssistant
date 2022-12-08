import discord
from discord.ext import commands
from case_group import case_group
import asyncio
import time
import threading

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
async def 새사건프리셋(ctx, *, args):
#[function]↓[function]↓[function]↓[function]
    def check(msg):
        return True

    def notification_1(handle, cases):
        str = ' : 난이도\n'
        for i in enumerate(cases):
            str += cases.cases[i] + ': '
            if cases.difficalty[i] >= 0:
                str += cases.difficalty[i] + '\n'
            else:
                str += '\n'

        handle.edit(content = str)

    def notification_2(handle, cases, pos, max_time, stop_flag):
        
        start = time.time()
        time_passd = 0
        while (time_passd) < max_time:
            str = cases.cases[pos] + '부터:      ' + time +'  \"나가기\"'
            handle.edit(content = str)
            if stop_flag:
                break
            time_passd = time.time() - start
#[function]↑[function]↑[function]↑[function]

    max_time = 20 #20 seconds to reply
    new_group = case_group(args)

    notification_1_handle = await ctx.send('')
    notification_2_handle = await ctx.send('')

    v = 0
    stop_flag = False
    countdown_thread = threading.thread(target = notification_2, args = (notification_2_handle, new_group, v, max_time, stop_flag))
    
    while True:
        for i in enumerate(args):
            await notification_1(notification_1_handle, new_group)

            v = i
            countdown_thread.start()

            try:
                message_in = await bot.wait_for("message", check = check, timeout = max_time)
            except asyncio.TimeoutError:
                await ctx.send('시간초과')
                break

            stop_flag = True
            new_group.difficulty[i] = float(message_in.content)
        
        await ctx.send('\"!재설정\" 또는 저장할 이름')
        message_in = await bot.wait_for("message", check = check)
        if message_in.content == "!재설정":
            continue
        else:
            case_group_s.update({message_in.content : new_group})
            break


bot.run('MTA1MDA0MDMwNDcwMDQ4OTc0OA.GWEj08.QVUODXc9XeA2mMOB7dqCncBilGMiRVEXXEOQFo')
