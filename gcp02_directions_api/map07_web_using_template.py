"""
Google Maps APIを使用して、指定された出発地、目的地、経由地を通る最適化されたルートをHTMLページに表示するスクリプト。

必要ライブラリ:
- os: ファイルパスの操作を行うためのPythonの標準ライブラリ
- webbrowser: 生成したHTMLファイルをデフォルトのブラウザで開くためのPythonの標準ライブラリ
- pathlib: ファイルパスの操作を行うためのPythonの標準ライブラリ
- dotenv: .envファイルから環境変数を読み込むためのライブラリ

使い方:
1. GoogleMapsのAPIキーを取得し、.envファイルにGOOGLE_CLOUD_PROJECT_API_KEYとして記載する。
2. python-dotenvをpipでインストールする。
   pip install python-dotenv
3. HTMLテンプレートファイル（optimized_waypoints.html）を用意する。
4. このスクリプトを実行すると、HTMLテンプレートにルート情報が埋め込まれ、map_directions.htmlファイルが生成される。
5. 生成されたHTMLファイルがデフォルトのブラウザで開かれ、最適化されたルートが表示される。

関数:
- create_html_from_template(api_key, origin, destination, waypoints)
  - 引数:
    - api_key: Google Maps APIキー
    - origin: 出発地
    - destination: 目的地
    - waypoints: 経由地のリスト
  - 機能:
    - HTMLテンプレートファイルを読み込み、ルート情報を埋め込んでHTMLファイルを生成する。
    - 生成されたHTMLファイルをデフォルトのブラウザで開く。
"""

import os
import webbrowser
from pathlib import Path

from dotenv import load_dotenv

# .envファイルからAPIキーをロード
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")


def create_html_from_template(api_key, origin, destination, waypoints):
    """
    HTMLテンプレートにルート情報を埋め込み、HTMLファイルを生成し、ブラウザで開く関数。

    引数:
    - api_key: Google Maps APIキー
    - origin: 出発地
    - destination: 目的地
    - waypoints: 経由地のリスト
    """
    template_path = "templates/optimized_waypoints.html"  # HTMLテンプレートのパス
    output_path = "results/map_directions.html"  # 生成するHTMLファイルのパス

    # テンプレートファイルを読み込む
    with open(template_path, "r") as file:
        template_content = file.read()

    # プレースホルダを値で置換
    filled_content = template_content.format(
        api_key=api_key,
        origin=origin,
        destination=destination,
        waypoint1=waypoints[0],
        waypoint2=waypoints[1],
        waypoint3=waypoints[2],
        waypoint4=waypoints[3],
    )

    # 結果をHTMLファイルに書き込み
    if not os.path.exists("results"):
        os.makedirs("results")
    with open(output_path, "w") as file:
        file.write(filled_content)

    # 生成したHTMLファイルをデフォルトのブラウザで開く
    webbrowser.open(f"file://{os.path.realpath(output_path)}")


# APIキーとルート情報を設定
origin = "東京, 日本"  # 出発地
destination = "熱海, 日本"  # 目的地
waypoints = [
    "修善寺温泉, 静岡",
    "小田原城, 神奈川",
    "伊豆高原, 静岡",
    "下田, 静岡",
]  # 経由地のリスト

create_html_from_template(
    api_key, origin, destination, waypoints
)  # 関数を呼び出してHTMLを生成し、ブラウザで開く
