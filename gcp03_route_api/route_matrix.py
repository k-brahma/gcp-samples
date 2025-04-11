"""
Google Maps Platformのルートマトリックス計算APIを使用して、
指定された出発地と目的地の間のルート情報を計算し、結果をJSONファイルとして保存するスクリプト。

このスクリプトは、.envファイルからGoogle Maps PlatformのAPIキーを読み込み、
computeRouteMatrix APIを呼び出してルート情報を取得します。
取得した情報は標準出力に表示され、JSONファイルとして保存されます。

参考: https://qiita.com/kngsym2018/items/15f19a88ea37c1cd3646

環境変数:
    GOOGLE_CLOUD_PROJECT_API_KEY: Google Maps PlatformのAPIキー

依存ライブラリ:
    - requests
    - python-dotenv
"""

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


def compute_route_matrix():
    """
    Google Maps PlatformのcomputeRouteMatrix APIを呼び出し、ルートマトリックスを計算します。

    Returns:
        dict: API呼び出しの結果。エラーが発生した場合はNone。

    Note:
        この関数は、事前に定義された出発地と目的地の座標を使用します。
        API呼び出しにはGOOGLE_CLOUD_PROJECT_API_KEYが必要です。
    """
    url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,status,condition",
    }

    payload = {
        "origins": [
            {
                "waypoint": {
                    "location": {"latLng": {"latitude": 37.420761, "longitude": -122.081356}}
                },
                "routeModifiers": {"avoid_ferries": True},
            },
            {
                "waypoint": {
                    "location": {"latLng": {"latitude": 37.403184, "longitude": -122.097371}}
                },
                "routeModifiers": {"avoid_ferries": True},
            },
        ],
        "destinations": [
            {
                "waypoint": {
                    "location": {"latLng": {"latitude": 37.420999, "longitude": -122.086894}}
                }
            },
            {
                "waypoint": {
                    "location": {"latLng": {"latitude": 37.383047, "longitude": -122.044651}}
                }
            },
        ],
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


# スクリプトファイルの親ディレクトリにresultsフォルダを作成
results_dir = Path(__file__).parent / "results"
results_dir.mkdir(exist_ok=True)

route_matrix = compute_route_matrix()
if route_matrix:
    print(route_matrix)

    # Save the result to a file as json
    file_path = results_dir / "route_matrix.json"
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(route_matrix, f, indent=4)
        print(f"json file saved as {file_path}")
