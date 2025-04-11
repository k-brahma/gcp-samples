"""
Google Cloud Vision APIを使用したレシート画像分析サンプル

このスクリプトは以下の機能を提供します：
- 指定されたレシート画像の読み込み
- Google Cloud Vision APIを使用したテキスト抽出
- 結果のJSONファイル保存
"""

import base64
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")


def analyze_receipt(image_path):
    """レシート画像を分析し、テキストを抽出する関数"""
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    headers = {"Content-Type": "application/json"}

    # 画像ファイルの読み込みとBase64エンコード - Path オブジェクトを使用
    img_path = Path(image_path)
    img_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")

    request_body = {
        "requests": [
            {
                "image": {"content": img_data},
                "features": [{"type": "TEXT_DETECTION", "maxResults": 10000}],
                "imageContext": {},
            }
        ],
        "parent": "",
    }

    data = json.dumps(request_body)
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    result = response.json()

    # 結果の整形
    text_annotations = result["responses"][0].get("textAnnotations", [])

    full_text = text_annotations[0].get("description", "")

    blocks = []
    for text in text_annotations[1:]:
        block = {
            "text": text.get("description", ""),
            "confidence": text.get("confidence", 0),
            "bounding_box": {"vertices": text.get("boundingPoly", {}).get("vertices", [])},
        }
        blocks.append(block)

    formatted_result = {
        "full_text": full_text,
        "text_blocks": blocks,
    }

    return formatted_result


def save_results(result, image_path):
    """結果をJSONファイルとして保存する関数"""
    # 結果ディレクトリの作成
    current_dir = Path(__file__).parent
    results_dir = current_dir / "ocr_results"
    results_dir.mkdir(exist_ok=True)

    # 入力ファイルの名前を取得（拡張子なし）
    input_stem = Path(image_path).stem

    # JSONファイルに保存 - Path オブジェクトを使用
    output_path = results_dir / f"{input_stem}.json"
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n結果を保存しました: {output_path}")


def main():
    print("Google Cloud Vision API レシート分析サンプル")

    # データディレクトリのパスを設定
    current_dir = Path(__file__)
    data_dir = current_dir.parent / "data"

    # ディレクトリ内のすべてのファイルを取得
    image_file = data_dir / "img1.jpg"

    # 全ての画像を処理
    print(f"\n'{image_file}' を分析中...")
    result = analyze_receipt(str(image_file))

    if result:
        # 結果の保存
        save_results(result, str(image_file))
        print(f"'{image_file}' の処理が完了しました")
    else:
        print(f"'{image_file}' の処理に失敗しました")


if __name__ == "__main__":
    main()
