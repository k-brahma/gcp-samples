# GCP Vision API レシート分析サンプル

このディレクトリには、Google Cloud Platform (GCP) の Vision API を使用したレシート画像分析サンプルアプリケーションが含まれています。OCR（光学式文字認識）を使用してレシート画像からテキストを抽出し、Gemini AI で内容を分析するプロセスを示しています。

## 機能

- Google Cloud Vision API を使用したレシート画像のテキスト抽出
- 抽出されたテキストデータの JSON 形式での保存
- Google Gemini AI を使用した抽出テキストの分析
- レシートから以下の情報を自動抽出:
  - 登録番号
  - 購入店名
  - 総支払額
  - 消費税額
- 単一画像または複数画像の一括処理

## ファイル構成

- `vision_01_read_one.py` - 単一のレシート画像を処理するサンプル
- `vision_02_read_all.py` - データディレクトリ内の全てのレシート画像を処理するサンプル
- `vision_03_summrize.py` - OCR結果を分析して要約するサンプル
- `vision_04_summrize to_files.py` - 要約結果をファイルに保存するサンプル
- `vision_05_summrize all_to_files.py` - 全てのOCR結果を分析し、要約をファイルに保存するサンプル
- `data/` - サンプルレシート画像を格納するディレクトリ
- `ocr_results/` - OCR処理結果の保存先
- `summary/` - 分析・要約結果の保存先

## 処理フロー

1. レシート画像の読み込み
2. Google Cloud Vision API を使用したテキスト抽出（OCR）
3. 抽出結果を JSON 形式で保存
4. Google Gemini AI を使用して抽出テキストから重要情報を分析
5. 分析結果の表示・保存

## 使用方法

1. `.env` ファイルを作成し、以下の API キーを設定してください:
   - `GOOGLE_CLOUD_PROJECT_API_KEY`: Google Cloud Platform の API キー
2. 必要なライブラリをインストールします: `pip install google-cloud-vision python-dotenv google-generativeai`
3. 目的に応じて適切なサンプルを選択して実行します:
   - 単一画像処理: `python vision_01_read_one.py`
   - 複数画像処理: `python vision_02_read_all.py`
   - OCR結果の分析: `python vision_03_summrize.py`
   - 全OCR結果の一括分析: `python vision_05_summrize all_to_files.py`

## データ準備

- 分析したいレシート画像を `data/` ディレクトリに配置してください
- サポートされる画像形式: JPG, PNG 