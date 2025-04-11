"""
Google Maps Directions APIを使用して、指定された出発地から目的地までの経路情報を取得し、
所要時間と距離を表示するスクリプト。また、取得した詳細な経路情報をJSONファイルとして保存します。

このスクリプトは.envファイルからGoogle Maps PlatformのAPIキーを読み込み、
Directions APIを呼び出して経路情報を取得します。デフォルトでは東京から長野への翌日の経路を計算します。

参考: https://qiita.com/kngsym2018/items/15f19a88ea37c1cd3646

環境変数:
    GOOGLE_CLOUD_PROJECT_API_KEY: Google Maps PlatformのAPIキー

依存ライブラリ:
    - python-dotenv
"""

import datetime
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def get_directions(origin, destination, dep_time):
    """
    Google Maps Directions APIを使用して、指定された出発地から目的地までの経路情報を取得します。

    Args:
        origin (str): 出発地の名称
        destination (str): 目的地の名称
        dep_time (str): 出発時間（'yyyy/mm/dd hh:mm' 形式）

    Returns:
        dict: API呼び出しの結果

    Note:
        この関数はGOOGLE_CLOUD_PROJECT_API_KEYが必要です。
    """
    api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")
    endpoint = "https://maps.googleapis.com/maps/api/directions/json?"

    # UNIX時間の算出
    dtime = datetime.datetime.strptime(dep_time, "%Y/%m/%d %H:%M")
    unix_time = int(dtime.timestamp())

    nav_request = f"language=ja&origin={origin}&destination={destination}&departure_time={unix_time}&key={api_key}"
    nav_request = urllib.parse.quote_plus(nav_request, safe="=&")
    request = endpoint + nav_request

    print(f"Request URL: {request}")

    # Google Maps Platform Directions APIを実行
    response = urllib.request.urlopen(request).read()

    # 結果(JSON)を取得
    return json.loads(response)


def print_route_info(directions):
    """
    経路情報から距離と所要時間を抽出して表示します。

    Args:
        directions (dict): Directions APIのレスポンス
    """
    for route in directions["routes"]:
        for leg in route["legs"]:
            print("=====")
            print(f"距離: {leg['distance']['text']}")
            print(f"所要時間: {leg['duration_in_traffic']['text']}")
            print("=====")


def save_json(data, origin, destination, dep_time, mode="default"):
    """
    経路情報をJSONファイルとして保存します。

    Args:
        data (dict): 保存するデータ
        origin (str): 出発地
        destination (str): 目的地
        dep_time (str): 出発時間
        mode (str): 移動手段
    """
    file_name = f"{origin}_{destination}_{dep_time}_{mode}.json"
    file_name = file_name.replace(" ", "_").replace("/", "_").replace(":", "_")

    # スクリプトファイルの親ディレクトリにresultsフォルダを作成
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    file_path = results_dir / file_name

    with open(file_path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"JSON file saved as {file_path}")


def main():
    """
    メイン関数：経路情報を取得し、表示して保存します。
    """
    origin = "東京"
    destination = "長野"
    dep_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y/%m/%d %H:%M")

    directions = get_directions(origin, destination, dep_time)
    print_route_info(directions)
    save_json(directions, origin, destination, dep_time)


if __name__ == "__main__":
    main()
