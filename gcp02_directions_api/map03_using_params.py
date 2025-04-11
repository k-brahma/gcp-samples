"""
2地点間（デフォルトでは東京から福島）のGoogle Maps URLを生成し、デフォルトのWebブラウザで開くサンプルスクリプト。

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
3. このスクリプトを実行すると、東京から福島までのGoogle MapsのURLが生成され、デフォルトのWebブラウザで開かれる。

関数:
- create_google_maps_url(origin, destination, travel_mode="driving")
  - 引数:
    - origin: 出発地 (str)
    - destination: 目的地 (str)
    - travel_mode: 移動手段 (str, デフォルトは"driving")
  - 戻り値:
    - Google Maps URL (str)
"""

import os
import urllib.parse
import webbrowser

from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")


def create_google_maps_url(origin, destination, travel_mode="driving"):
    """
    2地点間のGoogle Maps URLを生成する関数。

    引数:
    - origin: 出発地 (str)
    - destination: 目的地 (str)
    - travel_mode: 移動手段 (str, デフォルトは"driving")

    戻り値:
    - Google Maps URL (str)
    """
    base_url = "https://www.google.com/maps/dir/?api=1"
    params = {"origin": origin, "destination": destination, "travelmode": travel_mode}
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}&{query_string}"
    return url


# 使用例：東京から福島へのルート
origin = "東京"
destination = "福島"
url = create_google_maps_url(origin, destination)

# 生成したURLをデフォルトのWebブラウザで開く
webbrowser.open(url)
