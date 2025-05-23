# AWS サービス入門ガイド (Python編)

## 🎯 このガイドの目的

GCP経験者がAWSの主要サービスをPythonで活用できるようになることを目指します。このリポジトリには以下のAWSサービスのサンプルコードが含まれています。

## 📚 含まれるサンプル

| ファイル名 | AWSサービス | 機能概要 |
|-----------|------------|----------|
| `aws01_translate_text.py` | Amazon Translate | テキスト翻訳・言語検出 |
| `aws02_polly_tts.py` | Amazon Polly | テキスト音声変換（TTS） |
| `aws03_rekognition_faces.py` | Amazon Rekognition | 顔検出・感情分析 |
| `aws04_rekognition_objects.py` | Amazon Rekognition | 物体検出・ラベリング |
| `aws05_rekognition_objects with_position.py` | Amazon Rekognition | 物体検出（位置情報付き） |
| `aws06_comprehend_sentiment.py` | Amazon Comprehend | 感情分析・キーフレーズ抽出 |
| `aws07_comprehend_sentiment multiline.py` | Amazon Comprehend | 複数テキストの一括分析 |
| `aws08_ses_send_email.py` | Amazon SES | メール送信 |

## 🌐 AWS vs GCP 対応表

| AWS | GCP | 用途 |
|-----|-----|------|
| Amazon Translate | Cloud Translation | テキスト翻訳 |
| Amazon Polly | Cloud Text-to-Speech | 音声合成 |
| Amazon Rekognition | Cloud Vision | 画像認識・分析 |
| Amazon Comprehend | Cloud Natural Language | 自然言語処理 |
| Amazon SES | なし（SendGridなど外部サービス利用） | メール送信 |
| IAM | Cloud IAM | アクセス管理 |

## 🚀 はじめかた

### 1. AWS アカウントの準備

1. **AWSアカウント作成**
   - ルートアカウントを作成（管理者権限）
   - クレジットカード登録が必要

2. **IAMユーザー作成**（重要！）
   - ルートアカウントは日常利用しない
   - プログラムからのアクセスには必ずIAMユーザーを使用

### 2. 認証情報の設定

#### アクセスキーの取得
1. AWS管理コンソールにログイン
2. IAM → ユーザー → セキュリティ認証情報
3. アクセスキーを作成

#### `.env` ファイルの作成
```bash
# aws_samples/.env
AWS_ACCESS_KEY_ID=あなたのアクセスキーID
AWS_SECRET_ACCESS_KEY=あなたのシークレットアクセスキー
AWS_DEFAULT_REGION=ap-northeast-1  # 東京リージョン

# SESを使う場合（オプション）
SENDER_EMAIL=送信元メールアドレス
RECIPIENT_EMAIL=受信先メールアドレス
```

⚠️ **重要**: `.env`ファイルは絶対にGitにコミットしない！

### 3. Python環境のセットアップ

```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 必要なライブラリのインストール
pip install boto3 python-dotenv
```

## 🔑 IAMポリシーの基本

### ポリシーとは？
- AWSリソースへのアクセス権限を定義
- GCPのロールに相当

### ポリシーの付与方法

#### 方法1: AWS管理のポリシーを使用（簡単）
各サービスごとに用意されている標準ポリシー：
- `TranslateFullAccess` - 翻訳サービスのフルアクセス
- `AmazonPollyFullAccess` - 音声合成のフルアクセス
- `AmazonRekognitionFullAccess` - 画像認識のフルアクセス
- `ComprehendFullAccess` - 自然言語処理のフルアクセス
- `AmazonSESFullAccess` - メール送信のフルアクセス

#### 方法2: カスタムポリシー（セキュア）
必要最小限の権限のみを付与：
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "translate:TranslateText",
                "polly:SynthesizeSpeech",
                "rekognition:DetectFaces",
                "comprehend:DetectSentiment"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📝 サンプルの実行方法

### 基本的な実行手順

1. **必要なデータファイルの準備**
   ```
   aws_samples/
   ├── data/
   │   ├── faces.png          # 顔認識用の画像
   │   ├── objects.png        # 物体検出用の画像
   │   ├── comprehend_sample1.txt  # 感情分析用テキスト
   │   ├── mail_body.txt      # メール本文（テキスト）
   │   └── mail_body.html     # メール本文（HTML）
   ```

2. **サンプルの実行**
   ```bash
   cd aws_samples
   python aws01_translate_text.py
   ```

### 各サービスの簡単な使い方

#### 翻訳（Translate）
```python
# 基本的な使い方
import boto3
translate = boto3.client('translate')
result = translate.translate_text(
    Text="こんにちは",
    SourceLanguageCode='ja',
    TargetLanguageCode='en'
)
print(result['TranslatedText'])  # Hello
```

#### 音声合成（Polly）
```python
# 日本語テキストを音声に変換
polly = boto3.client('polly')
response = polly.synthesize_speech(
    Text="こんにちは",
    OutputFormat='mp3',
    VoiceId='Mizuki',  # 日本語女性音声
    LanguageCode='ja-JP'
)
# response['AudioStream']を保存
```

## 💰 料金について

### 無料利用枠（月間）

たとえば以下のとおり。あまり信用しないでAWSのサイトで各自確認すること。

- **Translate**: 200万文字
- **Polly**: 500万文字（標準音声）
- **Rekognition**: 画像1,000枚、動画10分
- **Comprehend**: 5万ユニット
- **SES**: 送信メール1,000通（EC2から）

### コスト管理のヒント
1. AWS Budgetsで予算アラートを設定
2. 開発時は最小限のデータで検証
3. 不要なリソースは即削除

## 🛠️ トラブルシューティング

### よくあるエラーと対処法

#### 1. 認証エラー
```
An error occurred (UnauthorizedException) when calling the TranslateText operation
```
**対処**: IAMユーザーに適切なポリシーが付与されているか確認

#### 2. リージョンエラー
```
Could not connect to the endpoint URL
```
**対処**: `.env`でリージョンを正しく設定（例: `ap-northeast-1`）

#### 3. リソースが見つからない
```
FileNotFoundError: [Errno 2] No such file or directory
```
**対処**: 必要なデータファイルが`data/`ディレクトリに配置されているか確認

## 📚 さらに学ぶために

### 公式ドキュメント
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS Python コード例](https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python)

### 次のステップ
1. 各サンプルを実行して動作を確認
2. パラメータを変更して実験
3. 複数のサービスを組み合わせた応用例を作成
4. エラーハンドリングを追加してプロダクションレベルのコードに

## ⚠️ セキュリティ注意事項

1. **アクセスキーの管理**
   - 定期的にローテーション
   - 不要になったら即削除
   - Gitには絶対コミットしない

2. **最小権限の原則**
   - 必要最小限の権限のみ付与
   - 本番環境では`FullAccess`ポリシーは避ける

3. **リソースの管理**
   - 使用後は必ずクリーンアップ
   - コスト監視を設定

---

このサンプル集が、AWSサービスをPythonで活用する第一歩となることを願っています！
質問や改善提案があれば、お気軽にお寄せください。