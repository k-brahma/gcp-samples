# GCP Directions API 地図表示サンプル

このディレクトリには、Google Cloud Platform (GCP) の Directions API を使用した地図表示サンプルアプリケーションが含まれています。このプロジェクトは `gcp03_route_api` とは異なり、主にフロントエンド表示と JavaScript による地図統合に焦点を当てています。

## 機能

- Directions API を使用した経路検索と表示
- 複数の経由地点を含む最適化された経路計算
- Maps JavaScript API を使用した HTML と JavaScript を使用した経路の視覚的表示
- ブラウザでの地図表示とルート案内
- URL 生成やテンプレートベースのアプローチなど、様々な実装方法

## ファイル構成

- `map01_sample_json.py` - 基本的な Directions API の使用例（JSON 結果の取得）
- `map02_disp.py` - Google Maps URL を生成してブラウザで表示
- `map03_using_params.py` - パラメータを使用した経路検索
- `map04_via.py` - 経由地点を含む経路検索
- `map05_saitekika_print_instructions.py` - 最適化された経路と手順の表示
- `map06_web_print_instructions.py` - Web ページでの経路手順の表示
- `map07_web_using_template.py` - HTML テンプレートを使用した地図表示
- `map08_web_json_only.py` - JSON データのみを使用した実装
- `map09_web_url1.py` - URL ベースの地図表示（方法1）
- `map10_web_url2.py` - URL ベースの地図表示（方法2）
- `templates/` - HTML テンプレートファイル
- `results/` - 生成された HTML ファイルの保存先

## gcp03_route_api との違い

このプロジェクトは主にフロントエンド表示と地図の視覚化に焦点を当てており、以下の点で `gcp03_route_api` と異なります：

- このプロジェクトは地図の視覚的表示と JavaScript 統合が中心
- HTML と JavaScript を使用したインタラクティブな地図表示
- ブラウザでのルート表示機能
- `gcp03_route_api` はバックエンド処理とデータ取得に特化している

## 使用方法

1. `.env` ファイルを作成し、`GOOGLE_CLOUD_PROJECT_API_KEY` に有効な GCP API キーを設定してください
2. 必要なライブラリをインストールします: `pip install googlemaps python-dotenv`
3. 目的に応じて適切なサンプルを選択して実行します:
   - 基本的な JSON 結果の取得: `python map01_sample_json.py`
   - ブラウザでの地図表示: `python map02_disp.py`
   - 経由地点を含む経路: `python map04_via.py`
   - テンプレートを使用した地図表示: `python map07_web_using_template.py`
4. ブラウザベースのサンプルでは、実行後に自動的にブラウザが開き、地図とルートが表示されます 