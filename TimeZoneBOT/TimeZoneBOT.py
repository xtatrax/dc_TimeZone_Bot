import argparse
import datetime
import time
import os

import discord
from discord.ext import tasks

version = '1.0.0'
pyname = os.path.basename(__file__)

#引数を定義
parser = argparse.ArgumentParser(description='時間表示BOT',add_help = True)
parser.add_argument('--version', action='version', version='%(prog)s ' + version) # version
parser.add_argument('-t', '--token',required=True, help='Discord-BOTのトークン') # 絶対
parser.add_argument('-z', '--zone',type=int, required=True, help='タイムゾーン+-数値') # 絶対
args = parser.parse_args()

#引数からトークンを取得
TOKEN = args.token

#Clientのインスタンスを作成
client = discord.Client()

#ループタスク作成(１秒)
@tasks.loop(seconds=1)
async def setTime(zone):
    #zoneで指定された、タイムゾーンの現在時刻を取得
    dt_now_jst_aware = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=zone))
    )
    #現在時刻を 時：分：秒として整形
    now = dt_now_jst_aware.strftime('%H:%M:%S')
    #BOTのステータスに書き込み
    await client.change_presence(activity=discord.Game(name=now, type=1))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="starting", type=1))
    setTime.start(args.zone)

client.run(TOKEN)



