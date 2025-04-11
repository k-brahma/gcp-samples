"""
基本的なレシート分析機能を提供するモジュール

このモジュールは、OCR結果のJSONから以下の情報を抽出します：
- 登録番号
- 購入店名
- 総支払額
- 消費税額

特徴：
- OCR結果のJSONを処理
- Google Gemini APIを使用して分析
- 結果をJSON形式で出力
- エラーハンドリング機能付き

使用方法：
1. プログラムを実行
2. OCR結果のJSONファイルのパスを入力
3. 分析結果を確認
4. 'exit'と入力して終了
"""

import json
import os
from pathlib import Path

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GOOGLE_CLOUD_PROJECT_API_KEY")
genai.configure(api_key=api_key)


def analyze_receipt_json(json_path):
    """OCR結果のJSONからレシートの情報を抽出する関数"""
    try:
        # JSONファイルを読み込む
        with open(json_path, "r", encoding="utf-8") as file:
            ocr_data = json.load(file)

        # OCR結果からテキストを取得
        if "text" in ocr_data:
            text_content = ocr_data["text"]
        else:
            text_content = json.dumps(ocr_data)

        prompt = """
        このレシートから以下の情報を抽出してください：
        1. 登録番号（登録番号もしくは事業者登録番号）
        2. 購入店名
        3. 総支払額
        4. 消費税額

        以下の形式でJSON形式で返してください：
        {
            "登録番号": "番号",
            "購入店": "店名",
            "総支払額": "金額",
            "消費税額": "金額"
        }
        """

        # Gemini APIを使用して分析
        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            generation_config={
                "temperature": 0.7,
                "response_mime_type": "application/json",
            },
        )
        response = model.generate_content(prompt + "\n\nOCRのテキスト結果:\n" + text_content)

        # JSON文字列を一度Pythonオブジェクトに変換し、再度日本語で整形されたJSON文字列に変換
        result_dict = json.loads(response.text)
        return json.dumps(result_dict, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return f"エラー: ファイル '{json_path}' が見つかりません"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


def main():
    print("レシート分析プログラム (OCR結果JSON版)")

    # まず、summaryディレクトリ内のファイルを削除
    summary_dir = Path(__file__).parent / "summary"
    if summary_dir.exists():
        for file in summary_dir.iterdir():
            file.unlink()
    else:
        # ディレクトリが存在しない場合は作成
        summary_dir.mkdir(exist_ok=True)

    # 現在のファイルのディレクトリを取得
    ocr_dir = Path(__file__).parent / "ocr_results"

    # ディレクトリが存在するか確認
    if not ocr_dir.exists() or not ocr_dir.is_dir():
        print(f"エラー: ディレクトリ '{ocr_dir}' が見つからないか、ディレクトリではありません")
        return

    # ディレクトリ内のすべてのJSONファイルを処理
    results = []
    for json_file in ocr_dir.glob("*.json"):
        result_str = analyze_receipt_json(json_file)
        try:
            # JSON文字列をPythonの辞書オブジェクトに変換
            result_dict = json.loads(result_str)
            results.append(result_dict)
        except json.JSONDecodeError as e:
            print(
                f"警告: ファイル '{json_file.name}' の解析結果をJSONとして解析できませんでした: {e}"
            )
            print(f"受け取った文字列: {result_str}")

    # 解析結果が空でないか確認
    if not results:
        print("警告: 有効な解析結果がありません。")
        return

    # 辞書のリストからDataFrameを作成
    df = pd.DataFrame(results)

    # summaryディレクトリが存在しない場合は作成
    summary_dir.mkdir(exist_ok=True)

    # csvファイルに保存
    csv_path = summary_dir / "summary.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # エクセルファイルに保存
    excel_path = summary_dir / "summary.xlsx"
    df.to_excel(excel_path, index=False)

    print(f"処理したレシート数: {len(results)}")
    print("レシート分析結果をファイルに保存しました。")


if __name__ == "__main__":
    main()
