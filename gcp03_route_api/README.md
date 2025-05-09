# GCP ルートAPI サンプル

このディレクトリには、Google Cloud Platform (GCP) の Routes API と Directions API を使用したサンプルアプリケーションが含まれています。このプロジェクトは `gcp02_directions_api` とは異なり、主にバックエンド処理と経路計算に焦点を当てています。

## 機能

- Google Maps Platform の Routes API を使用した経路行列の計算
- 複数の出発地と目的地間の距離と所要時間の計算
- Directions API を使用した詳細な経路情報の取得
- 異なる移動手段（車、徒歩など）でのルート計算
- 各APIの結果をJSON形式で保存

## ファイル構成

- `route_api.py` - Routes API を使用した基本的なサンプル
- `route_matrix.py` - Routes API を使用した詳細なサンプル
- `route_matrix_jp.py` - 日本語での出発地と目的地を使用したサンプル
- `step01_complete_sample.py` - Directions API を使用した基本的なサンプル（車での移動）
- `step02_complete_sample_dict.py` - Directions API を使用した徒歩での移動サンプル
- `results/` - API呼び出し結果の保存先

## 使用方法

1. `.env` ファイルを作成し、`GOOGLE_CLOUD_PROJECT_API_KEY` に有効な GCP API キーを設定してください
2. 必要なライブラリをインストールします: `pip install python-dotenv requests`
3. 実行したいサンプルを選択して実行します:
   - Route Matrix: `python route_matrix.py`
   - 日本語での経路計算: `python route_matrix_jp.py`
   - 詳細な経路情報（車）: `python step01_complete_sample.py`
   - 詳細な経路情報（徒歩）: `python step02_complete_sample_dict.py`
4. 結果は `results/` ディレクトリに JSON ファイルとして保存されます 