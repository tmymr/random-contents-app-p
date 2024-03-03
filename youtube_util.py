# youtube_util.py

import googleapiclient.discovery
import random
import json

def get_random_region_code():
    # JSON ファイルから地域コードのリストを読み込む
    with open('region_codes.json', 'r') as file:
        region_codes = json.load(file)
    
    # ランダムに地域コードを選択
    return random.choice(region_codes)

def get_random_video_id(search_response):
    # 検索結果から上位10件の動画IDを取得
    video_ids = [item['id']['videoId'] for item in search_response['items'][:10]]

    # ランダムに動画IDを選択
    return random.choice(video_ids)

def get_youtube_link(youtube, keywords):
    # ランダムなキーワードを選択
    search_keyword = random.choice(keywords)

    # ランダムな地域コードを取得
    region_code = get_random_region_code()

    # YouTube APIを使用して動画を検索
    search_response = youtube.search().list(q=search_keyword, part='id', type='video', regionCode=region_code).execute()

    # ランダムに動画IDを取得
    video_id = get_random_video_id(search_response)

    # 動画のURLを生成
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    return video_url