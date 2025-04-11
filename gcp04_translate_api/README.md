# GCP 翻訳API サンプル

このディレクトリには、Google Cloud Platform (GCP) の Translation API を使用した翻訳サンプルアプリケーションが含まれています。

## 機能

- 日本語のテキストや HTML を英語に翻訳します
- 複数の翻訳方法を提供:
  - HTML ファイルの翻訳 (`translate01_html.py`)
  - テキストファイルの通常翻訳 (`translate02_text_normal.py`)
  - 改行を保持するための行ごとの翻訳 (`translate03_text_for_each_line.py`)
- 環境変数から API キーを読み込み

## ファイル構成

- `translate01_html.py` - HTML ファイルを翻訳するスクリプト
- `translate02_text_normal.py` - テキストファイルを翻訳するスクリプト（改行が保持されない場合あり）
- `translate03_text_for_each_line.py` - 行ごとに翻訳して改行を保持するスクリプト
- `templates/ja.html` - 翻訳する日本語 HTML の入力ファイル
- `templates/ja.txt` - 翻訳する日本語テキストの入力ファイル
- `results/` - 翻訳結果の保存先

## 使用方法

1. `.env` ファイルを作成し、`GOOGLE_CLOUD_PROJECT_API_KEY` に有効な GCP API キーを設定してください
2. 必要なライブラリをインストールします: `pip install -r requirements.txt`
3. 翻訳したいファイルのタイプに応じて、適切なスクリプトを実行します:
   - HTML ファイルの翻訳: `python translate01_html.py`
   - テキストファイルの翻訳: `python translate02_text_normal.py`
   - 改行を保持する翻訳: `python translate03_text_for_each_line.py`
4. 翻訳結果は `results/` ディレクトリに保存されます 