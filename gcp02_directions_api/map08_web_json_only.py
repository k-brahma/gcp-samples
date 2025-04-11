"""
Google Maps APIを使用して、指定された出発地、目的地、経由地を通る最適化されたルートを計算し、結果をJSON形式で整理してファイルに保存するスクリプト。

必要ライブラリ:
- json: JSONデータの操作を行うためのPythonの標準ライブラリ
- os: ファイルパスの操作を行うためのPythonの標準ライブラリ
- datetime: 日付と時刻の操作を行うためのPythonの標準ライブラリ
- pathlib: ファイルパスの操作を行うためのPythonの標準ライブラリ
- googlemaps: Google Maps APIを使用するためのPythonクライアントライブラリ
- dotenv: .envファイルから環境変数を読み込むためのライブラリ

使い方:
1. GoogleMapsのAPIキーを取得し、.envファイルにGOOGLE_CLOUD_PROJECT_API_KEYとして記載する。
2. googlemapsとpython-dotenvをpipでインストールする。
   pip install googlemaps python-dotenv
3. このスクリプトを実行すると、最適化されたルートが計算され、結果がJSON形式で整理されてresults/route_data.jsonファイルに保存される。

関数:
- calculate_optimal_route(api_key)
  - 引数:
    - api_key: Google Maps APIキー
  - 機能:
    - 指定された出発地、目的地、経由地を通る最適化されたルートを計算する。
    - 結果をJSON形式で整理して返す。
"""

import json
import os
from datetime import datetime
from pathlib import Path

import googlemaps
from dotenv import load_dotenv

# .envファイルからAPIキーをロード
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")


def calculate_optimal_route(api_key):
    """
    指定された出発地、目的地、経由地を通る最適化されたルートを計算し、結果をJSON形式で整理して返す関数。

    引数:
    - api_key: Google Maps APIキー

    返り値:
    - route_data: 最適化されたルートのJSONデータ
    """
    gmaps = googlemaps.Client(key=api_key)
    origin = "東京, 日本"  # 出発地
    destination = "熱海, 日本"  # 目的地
    waypoints = [
        "修善寺温泉, 静岡",
        "小田原城, 神奈川",
        "伊豆高原, 静岡",
        "下田, 静岡",
    ]  # 経由地のリスト

    directions_result = gmaps.directions(
        origin,
        destination,
        mode="driving",  # 運転モード
        waypoints=waypoints,
        optimize_waypoints=True,  # 経由地の順序を最適化
        departure_time=datetime.now(),
    )  # 現在時刻を出発時刻として設定

    # データをJSON形式で整理
    route_data = json.dumps(directions_result, ensure_ascii=False, indent=2)
    return route_data


route_data = calculate_optimal_route(api_key)  # 最適化されたルートを計算
print(route_data)  # 結果を出力

# resultsディレクトリが存在しない場合は作成
if not os.path.exists("results"):
    os.makedirs("results")

# ルート情報をファイルに保存
output_path = "results/route_data.json"
with open(output_path, "w", encoding="utf8") as file:
    file.write(route_data)
print(f"ルート情報を{output_path}に保存しました。")
