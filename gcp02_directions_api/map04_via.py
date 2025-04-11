"""
2地点間（デフォルトでは東京から修善寺）のGoogle Maps URLを生成し、デフォルトのWebブラウザで開くサンプルスクリプト。
経由地（小田原、伊豆高原、下田）を指定しています。

環境変数からAPIキーを読み込むために、dotenvライブラリを使用しています。
APIキーは、親ディレクトリにある.envファイルに記載されている前提です。

必要ライブラリ:
- webbrowser: URLをデフォルトのWebブラウザで開くためのPythonの標準ライブラリ
- urllib.parse: URLエンコードを行うためのPythonの標準ライブラリ
- python-dotenv: .envファイルから環境変数を読み込むためのライブラリ

使い方:
1. GoogleMapsのAPIキーを取得し、.envファイルにGOOGLE_CLOUD_PROJECT_API_KEYとして記載する。
2. python-dotenvをpipでインストールする。
   pip install python-dotenv
3. このスクリプトを実行すると、東京から修善寺までのGoogle MapsのURL（小田原、伊豆高原、下田を経由地として設定）が生成され、デフォルトのWebブラウザで開かれる。

関数:
- create_google_maps_url(origin, destination, waypoints=None, travel_mode="driving")
  - 引数:
    - origin: 出発地 (str)
    - destination: 目的地 (str)
    - waypoints: 経由地のリスト (list, デフォルトはNone)
    - travel_mode: 移動手段 (str, デフォルトは"driving")
  - 戻り値:
    - Google Maps URL (str)
"""

import os
import urllib.parse
import webbrowser
from pathlib import Path

from dotenv import load_dotenv



# .envファイルを読み込む
load_dotenv()

api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")


def create_google_maps_url(origin, destination, waypoints=None, travel_mode="driving"):
    """
    2地点間のGoogle Maps URLを生成する関数。経由地を指定することもできます。

    引数:
    - origin: 出発地 (str)
    - destination: 目的地 (str)
    - waypoints: 経由地のリスト (list, デフォルトはNone)
    - travel_mode: 移動手段 (str, デフォルトは"driving")

    戻り値:
    - Google Maps URL (str)
    """
    base_url = "https://www.google.com/maps/dir/?api=1"

    params = {"origin": origin, "destination": destination, "travelmode": travel_mode}

    if waypoints:
        params["waypoints"] = "|".join(waypoints)

    query_string = urllib.parse.urlencode(params, safe="|")

    url = f"{base_url}&{query_string}"
    return url


# 使用例：東京から修善寺まで、小田原、伊豆高原、下田を経由
origin = "Tokyo, Japan"
destination = "修善寺温泉"
waypoints = ["小田原城", "伊豆高原", "下田"]
url = create_google_maps_url(origin, destination, waypoints)

# 生成したURLをデフォルトのWebブラウザで開く
webbrowser.open(url)
