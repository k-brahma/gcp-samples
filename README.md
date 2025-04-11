# Google Cloud Platform (GCP) API サンプル集

このリポジトリは、Google Cloud Platform の様々な API を活用したサンプルアプリケーション集です。  
各サンプルは独立したディレクトリに配置されており、特定の GCP API の基本的な使用方法を示しています。

## 概要

このプロジェクトには以下の API を使用したサンプルが含まれています:

- **Cloud Vision API**: 画像認識と光学式文字認識（OCR）
- **Cloud Translation API**: テキストや HTML の翻訳
- **Generative Language API**: テキスト生成と分析（Gemini AI）
- **Directions API**: 経路検索と道案内情報
- **Maps JavaScript API**: インタラクティブな地図表示
- **Routes API**: 経路行列計算と距離・時間測定
- **Cloud Text-to-Speech API**: テキストから音声への変換

## サンプルプロジェクトのセットアップ

1. このリポジトリをクローンします:

```bash
git clone https://github.com/k-brahma/gcp-samples.git
cd gcp-samples
```

2. 仮想環境を作成し、アクティブにします:

```bash 
python -m venv venv
```

```bash
# Windows
venv\Scripts\activate
```

```bash
# macOS/Linux
souce venv/bin/activate
```

3. pip を使用して必要なライブラリをインストールします:

```bash
pip install -r requirements.txt
```
4. プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を記載します:

```
GOOGLE_CLOUD_PROJECT_API_KEY=あなたのAPIキー
```

APIキーの取得方法については後述します。

## サンプルディレクトリ

### 1. [gcp01_google_vision_api](./gcp01_google_vision_api)

レシート画像からテキストを抽出し、Gemini AI を使用して重要情報（店名、金額など）を分析するサンプルです。

**主な機能:**
- レシート画像のテキスト抽出（OCR）
- Gemini AI を使用した抽出テキストの分析
- 単一または複数画像の一括処理

### 2. [gcp02_directions_api](./gcp02_directions_api)

Google Maps Directions API を使用した経路検索と地図表示のサンプルです。フロントエンド表示と JavaScript 統合に焦点を当てています。

**主な機能:**
- 経路検索と地図表示
- 複数の経由地点を含む最適化された経路計算
- HTML と JavaScript を使用した視覚的表示

### 3. [gcp03_route_api](./gcp03_route_api)

Google Maps Platform の Route API と Directions API を使用した経路計算のサンプルです。バックエンド処理と純粋な経路計算に焦点を当てています。

**主な機能:**
- Route Matrix API を使用した経路行列の計算
- 複数の出発地と目的地間の距離と所要時間の計算
- 異なる移動手段（車、徒歩など）でのルート計算

### 4. [gcp04_translate_api](./gcp04_translate_api)

Google Cloud Translation API を使用した翻訳サンプルです。テキストや HTML の翻訳方法を示しています。

**主な機能:**
- 日本語のテキストや HTML を英語に翻訳
- 複数の翻訳方法（HTML、通常テキスト、行ごとの翻訳）
- 改行の保持など、特殊ケースの処理

### 5. [gcp05_text_to_speech_api](./gcp05_text_to_speech_api)

Google Cloud Text-to-Speech API を使用して、テキストを自然な音声に変換するサンプルです。

**主な機能:**
- 日本語テキストを音声（MP3形式）に変換
- Google Cloud の Neural2 音声モデルを使用
- テキストファイルから音声ファイルへの変換

## Google Cloud Platform の設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセスし、プロジェクトを作成または選択します
2. 必要な API を有効化します:
   - [API ライブラリ](https://console.cloud.google.com/apis/library) にアクセス
   - 以下の API を検索して有効化:
     - Cloud Vision API
     - Cloud Translation API
     - Generative Language API (Gemini API)
     - Directions API
     - Maps JavaScript API
     - Routes API
     - Cloud Text-to-Speech API
3. [認証情報](https://console.cloud.google.com/apis/credentials) ページでAPI キーを作成します
4. 作成した API キーをセキュリティのために制限することをお勧めします（使用する API のみに制限）

## トラブルシューティング

### API キーの問題

- API キーが正しく設定されていることを確認してください
- API が有効化されていることを確認してください
- API キーの制限が適切に設定されていることを確認してください

### ライブラリのインストール問題

- Python のバージョンが 3.8 以上であることを確認してください
- 仮想環境を使用している場合は、環境がアクティブであることを確認してください
- 以下のコマンドで pip を最新版に更新してみてください:

```bash
pip install --upgrade pip
```

## 注意事項

- このサンプル集は学習目的で作成されています
- API の使用には Google Cloud Platform の利用料金が発生する場合があります
- 各 API の利用制限や料金体系については、Google Cloud Platform の公式ドキュメントを参照してください 