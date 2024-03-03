# bot.py

import discord
from discord.ext import commands, tasks
import googleapiclient.discovery
from decouple import config
import random
import json
import datetime
import asyncio
from youtube_util import get_youtube_link
from keep_alive import keep_alive

# Load environment variables from .env file
DISCORD_BOT_TOKEN = config('YOUR_DISCORD_BOT_TOKEN')
YOUTUBE_API_KEY = config('YOUR_YOUTUBE_API_KEY')
CHANNEL_ID_POST_YOUTUBE = config('CHANNEL_ID_POST_YOUTUBE')
CHANNEL_ID_ADMIN = config('CHANNEL_ID_ADMIN')

# 必要なIntentを有効化
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容に関連するインテントを有効化

# Discord Botの設定
bot = commands.Bot(command_prefix='/', intents=intents)

# YouTube Data API v3のクライアントを作成
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# JSONファイルからキーワードを読み込む
with open('keywords.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

keywords = data.get('keywords', [])  # 'keywords' キーが存在しない場合は空リストをデフォルトとする

# 定期的なタスクの作成
@tasks.loop(seconds=60)  # 60秒ごとにタスクを実行
async def send_daily_link():
    now = datetime.datetime.now().time()

    # 指定した時刻になったらリンクを送信
    if now.hour == target_time.hour and now.minute == target_time.minute:
        channel_id = int(CHANNEL_ID_POST_YOUTUBE)  # 送信先のチャンネルIDを指定
        channel = bot.get_channel(channel_id)

        if channel:
            youtube_link = get_youtube_link(youtube, keywords)

            if youtube_link:
                # Discordチャンネルに動画のリンクを送信
                await channel.send(f'Today\'s Video: {youtube_link}')

#コマンドでリンクを送信してほしいときに使用
@bot.command(name='post_youtube_link')
async def post_youtube_link(ctx):
    # YouTube APIを使用して動画のリンクを取得
    youtube_link_command = get_youtube_link(youtube, keywords)

    if youtube_link_command:
        # Discordチャンネルに動画のリンクを送信
        await ctx.send(f'Here is a YouTube video for you: {youtube_link_command}')

# コマンドで実行タイミングを変更するためのコマンド追加
@bot.command(name='set_time')
async def set_time(ctx, hours: int, minutes: int):
    global target_time
    target_time = datetime.time(hours, minutes)
    await ctx.send(f'Next video will be sent at {target_time}')

#現在の変数設定を表示
@bot.command(name='show_variables')
async def show_variables(ctx):
    #現在の変数の設定を表示します。
    if target_time:
        response = (
            f"target_time: {target_time}\n"
        )
        await ctx.send(response)

# Botの起動時にタスクを開始
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')   

    # 指定した時刻に実行するための時間設定
    global target_time
    target_time = datetime.time(11, 00)  # 20:00

    # Discordチャンネルに実行時刻を送信
    channel_id = int(CHANNEL_ID_ADMIN)  # 送信先のチャンネルIDを指定
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(f'The daily link task is scheduled to run at {target_time}')
    
    send_daily_link.start()

    '''
    # 最初の実行時刻を計算
    now = datetime.datetime.now()
    next_run = datetime.datetime(now.year, now.month, now.day, target_time.hour, target_time.minute)

    # 次回の実行時間を設定
    if now > next_run:
        next_run += datetime.timedelta(days=1)  # 今日の指定時刻を過ぎていたら翌日の同時刻に設定

    delay_seconds = (next_run - now).total_seconds()
    send_daily_link.start()
    await asyncio.sleep(delay_seconds)
    '''

# Web サーバの立ち上げ
keep_alive()

# Discord Botを実行
bot.run(DISCORD_BOT_TOKEN)
