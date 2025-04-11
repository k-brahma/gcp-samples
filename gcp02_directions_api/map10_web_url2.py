"""
Google Maps APIを使用して、指定された出発地、目的地、経由地を通る最適化されたルートのGoogle Maps URLを生成するスクリプト。
経由地の順序は、最適化されたルートの順序に合わせて並び替えられます。

必要ライブラリ:
- os: ファイルパスの操作を行うためのPythonの標準ライブラリ
- datetime: 日付と時刻の操作を行うためのPythonの標準ライブラリ
- pathlib: ファイルパスの操作を行うためのPythonの標準ライブラリ
- urllib.parse: URLエンコードを行うためのPythonの標準ライブラリ
- googlemaps: Google Maps APIを使用するためのPythonクライアントライブラリ
- dotenv: .envファイルから環境変数を読み込むためのライブラリ

使い方:
1. GoogleMapsのAPIキーを取得し、.envファイルにGOOGLE_CLOUD_PROJECT_API_KEYとして記載する。
2. googlemapsとpython-dotenvをpipでインストールする。
   pip install googlemaps python-dotenv
3. このスクリプトを実行すると、最適化されたルートのGoogle Maps URLが生成され、出力される。

関数:
- generate_google_maps_url(api_key)
  - 引数:
    - api_key: Google Maps APIキー
  - 機能:
    - 指定された出発地、目的地、経由地を通る最適化されたルートのGoogle Maps URLを生成する。
    - 経由地の順序は、最適化されたルートの順序に合わせて並び替えられる。
    - 生成されたURLを返す。
"""

import os
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import googlemaps
from dotenv import load_dotenv

# .envファイルからAPIキーをロード
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")


def generate_google_maps_url(api_key):
    """Google MapsのURLを生成する関数

    出発地、最終目的地を設定し、経由地を設定する。
    経由地については、最適化された順序を示してくれる。
    """
    gmaps = googlemaps.Client(key=api_key)
    origin = "東京, 日本"  # 出発地
    destination = "浜名湖, 日本"  # 目的地
    waypoints = [
        "修善寺温泉, 静岡",
        "御殿場, 神奈川",
        "伊豆高原, 静岡",
        "下田, 静岡",
    ]  # 経由地のリスト

    # Directions APIを使ってルート情報を取得
    directions_result = gmaps.directions(
        origin,
        destination,
        mode="driving",  # 運転モード
        waypoints=waypoints,
        optimize_waypoints=True,  # 経由地の順序を最適化
        departure_time=datetime.now(),
    )  # 現在時刻を出発時刻として設定

    # 最適化された経由地の順序を取得
    optimized_waypoints = [waypoints[i] for i in directions_result[0]["waypoint_order"]]

    # URLの組み立て
    base_url = "https://www.google.com/maps/dir/"

    # 出発地、経由地、目的地を順番に結合
    locations = [origin] + optimized_waypoints + [destination]
    locations_url = "/".join(
        quote(location.encode("utf-8"), safe=",:/ ") for location in locations
    )  # 各地点をURLエンコードして'/'で連結

    google_maps_url = f"{base_url}{locations_url}"  # URLを組み立て

    return google_maps_url


url = generate_google_maps_url(api_key)  # 最適化されたルートのURLを生成
print(url)  # 生成されたURLを出力
