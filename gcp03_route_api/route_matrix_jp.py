import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

"""
Google Maps Platformのルートマトリックス計算APIを使用して、
日本の複数の出発地から単一の目的地へのルート情報を計算し、結果をJSONファイルとして保存するスクリプト。

このスクリプトは、.envファイルからGoogle Maps PlatformのAPIキーを読み込み、
computeRouteMatrix APIを呼び出して日本語でのルート情報を取得します。
取得した情報は標準出力に表示され、JSONファイルとして保存されます。

参考: https://qiita.com/kngsym2018/items/15f19a88ea37c1cd3646

環境変数:
    GOOGLE_CLOUD_PROJECT_API_KEY: Google Maps PlatformのAPIキー

依存ライブラリ:
    - requests
    - python-dotenv
"""

load_dotenv()


def compute_route_matrix():
    """
    Google Maps PlatformのcomputeRouteMatrix APIを呼び出し、日本の複数の出発地から
    単一の目的地へのルートマトリックスを計算します。

    Returns:
        dict: API呼び出しの結果。エラーが発生した場合はNone。

    Note:
        この関数は、事前に定義された日本の出発地と目的地の座標を使用します。
        API呼び出しにはGOOGLE_CLOUD_PROJECT_API_KEYが必要です。
        言語設定は日本語（ja）になっています。
    """
    url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,status,condition",
    }

    payload = {
        "languageCode": "ja",
        "origins": [
            {"waypoint": {"location": {"latLng": {"latitude": 35.4654, "longitude": 139.6225}}}},
            {"waypoint": {"location": {"latLng": {"latitude": 35.2637, "longitude": 139.6198}}}},
            {"waypoint": {"location": {"latLng": {"latitude": 35.2196, "longitude": 139.0770}}}},
        ],
        "destinations": [
            {"waypoint": {"location": {"latLng": {"latitude": 34.6795, "longitude": 138.9453}}}}
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


# Create results directory in current working directory
results_dir = Path(__file__).parent / "results"
results_dir.mkdir(exist_ok=True)

route_matrix = compute_route_matrix()
if route_matrix:
    print(route_matrix)

    # Save the result to a file as json
    file_path = results_dir / "route_matrix_ja.json"
    with open(file_path, "w", encoding="utf8") as f:
        json.dump(route_matrix, f, indent=4)
        print(f"json file saved as {file_path}")
