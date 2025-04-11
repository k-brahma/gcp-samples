# GCP テキスト読み上げAPI サンプル

このディレクトリには、Google Cloud Platform (GCP) の Text-to-Speech API を使用した簡単なサンプルアプリケーションが含まれています。

## 機能

- 日本語のテキストファイルを音声（MP3形式）に変換します
- Google Cloud の Neural2 音声モデルを使用
- 環境変数から API キーを読み込み

## ファイル構成

- `text_to_speech01.py` - メインのPythonスクリプト
- `templates/ja.txt` - 変換する日本語テキストの入力ファイル
- `results/` - 生成された音声ファイルの保存先

## 使用方法

1. `.env` ファイルを作成し、`GOOGLE_CLOUD_PROJECT_API_KEY` に有効な GCP API キーを設定してください
2. `templates/ja.txt` ファイルに変換したい日本語テキストを記述してください
3. スクリプトを実行します: `python text_to_speech01.py`
4. 変換された音声ファイルは `results/ja.mp3` に保存されます 