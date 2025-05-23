"""
Amazon Rekognition を使用したテキスト検出サンプル

このモジュールは画像内のテキストを検出し、文字列として抽出します。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* AmazonRekognitionFullAccess

または、最小権限として以下のアクションを許可してください：

* rekognition:DetectText

推奨されるサンプルデータ
----------------------
data/text.jpg : 文字が写った写真
- 看板やメニュー
- 印刷された文書
- 手書きのメモ
- 商品ラベルやパッケージ

:author: AWS Samples
:version: 1.0
"""

import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

# .envファイルを明示的に指定して読み込み
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# 認証情報を取得
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-1')

if not all([aws_access_key_id, aws_secret_access_key]):
    raise ValueError("AWS認証情報が設定されていません。.envファイルを確認してください。")

# 出力ディレクトリと入力ディレクトリの設定
RESULTS_DIR = Path(__file__).parent / 'results'
DATA_DIR = Path(__file__).parent / 'data'
RESULTS_DIR.mkdir(exist_ok=True)

# サンプル画像のパス
SAMPLE_IMAGE = DATA_DIR / 'text.jpg'  # テキスト検出用：文字が写った写真

# Rekognitionクライアント作成
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)

def detect_text(image_path):
    """
    画像内のテキストを検出する関数
    
    :param image_path: 分析する画像ファイルのパス
    :type image_path: str
    :return: 検出されたテキストのリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        with open(image_path, 'rb') as image:
            response = rekognition.detect_text(
                Image={'Bytes': image.read()}
            )
        
        # 結果をファイルに保存
        result_file = RESULTS_DIR / f"{Path(image_path).stem}_text.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {image_path} のテキスト検出結果 ===\n")
            for text in response['TextDetections']:
                if text['Type'] == 'LINE':
                    f.write(f"- {text['DetectedText']} (信頼度: {text['Confidence']:.1f}%)\n")
        
        print(f"=== {image_path} のテキスト検出結果 ===")
        texts = []
        for text in response['TextDetections']:
            if text['Type'] == 'LINE':
                print(f"- {text['DetectedText']} (信頼度: {text['Confidence']:.1f}%)")
                texts.append(text)
        
        print(f"\n検出結果は '{result_file}' に保存されました。")
        return texts
            
    except Exception as e:
        print(f"テキスト検出エラー: {e}")
        return None

if __name__ == "__main__":
    if not SAMPLE_IMAGE.exists():
        print("\n=== サンプルデータが不足しています ===")
        print("以下のファイルを data ディレクトリに配置してください：")
        print("（.jpg または .png 形式）\n")
        print("- text.jpg : 文字が写った写真（看板、メニュー、案内板など）")
    else:
        detect_text(SAMPLE_IMAGE) 