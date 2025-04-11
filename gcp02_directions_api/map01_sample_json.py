"""
GoogleMaps APIを使って、2地点間（東京から新潟）のドライビング経路を検索するサンプルスクリプト。

環境変数からAPIキーを読み込むために、dotenvライブラリを使用しています。
APIキーは、親ディレクトリにある.envファイルに記載されている前提です。

必要ライブラリ:
- googlemaps: GoogleMaps APIを使うためのPythonクライアントライブラリ
- python-dotenv: .envファイルから環境変数を読み込むためのライブラリ

使い方:
1. GoogleMapsのAPIキーを取得し、.envファイルにGOOGLE_CLOUD_PROJECT_API_KEYとして記載する。
2. googlemapsとpython-dotenvをpipでインストールする。
   pip install -U googlemaps python-dotenv
3. このスクリプトを実行すると、シドニーからメルボルンまでのドライビング経路が取得できる。
"""

import os

import googlemaps
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

gmaps = googlemaps.Client(key=api_key)

directions_result = gmaps.directions("東京", "新潟", mode="driving")
print(directions_result)
