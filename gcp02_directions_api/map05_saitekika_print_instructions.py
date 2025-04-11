"""
Google Maps APIを使用して、指定された出発地、目的地、経由地を通る最適化されたルートを計算し、各区間の情報を出力するスクリプト。

必要ライブラリ:
- googlemaps: Google Maps APIを使用するためのPythonクライアントライブラリ
- datetime: 日付と時刻の操作を行うためのPythonの標準ライブラリ
- os: 環境変数を読み込むためのPythonの標準ライブラリ
- dotenv: .envファイルから環境変数を読み込むためのライブラリ
- pathlib: ファイルパスの操作を行うためのPythonの標準ライブラリ

使い方:
1. GoogleMapsのAPIキーを取得し、.envファイルにGOOGLE_CLOUD_PROJECT_API_KEYとして記載する。
2. googlemapsとpython-dotenvをpipでインストールする。
   pip install googlemaps python-dotenv
3. このスクリプトを実行すると、東京から熱海までの最適化されたルートが計算され、各区間の情報が出力される。

出力情報:
- 各区間の開始地点と終了地点のアドレス
- 各区間の所要時間
- 各区間の詳細な道順と距離
"""

import os
from datetime import datetime
from pathlib import Path

import googlemaps
from dotenv import load_dotenv

# .envファイルからAPIキーをロード
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

# Google Mapsクライアントを初期化
gmaps = googlemaps.Client(key=api_key)

# ルート計算の設定
origin = "東京, 日本"
destination = "熱海, 日本"
waypoints = ["修善寺温泉, 静岡", "小田原城, 神奈川", "伊豆高原, 静岡", "下田, 静岡"]

# 最適化されたルート計算（optimize_waypointsをTrueに設定）
directions_result = gmaps.directions(
    origin,
    destination,
    mode="driving",
    waypoints=waypoints,
    optimize_waypoints=True,
    departure_time=datetime.now(),
)

# 結果を出力
for leg in directions_result[0]["legs"]:
    print(f"Start: {leg['start_address']}")
    print(f"End: {leg['end_address']}")
    print(f"Duration: {leg['duration']['text']}")
    for step in leg["steps"]:
        print(f"Instruction: {step['html_instructions']} Distance: {step['distance']['text']}")
    print("\n")
