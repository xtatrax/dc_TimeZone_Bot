import argparse
import datetime
import time
import os

import discord
from discord.ext import tasks

version = '1.0.0'
pyname = os.path.basename(__file__)

parser = argparse.ArgumentParser(description='時間表示BOT',add_help = True)
parser.add_argument('--version', action='version', version='%(prog)s ' + version) # version
parser.add_argument('-t', '--token',required=True, help='Discord-BOTのトークン') # 絶対
parser.add_argument('-z', '--zone',type=int, required=True, help='タイムゾーン+-数値') # 絶対
args = parser.parse_args()

TOKEN = args.token
client = discord.Client()
@tasks.loop(seconds=1)
async def setTime(zone):
    dt_now_jst_aware = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=zone))
    )
    now = dt_now_jst_aware.strftime('%H:%M:%S')
    await client.change_presence(activity=discord.Game(name=now, type=1))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="starting", type=1))
    setTime.start(args.zone)

client.run(TOKEN)



