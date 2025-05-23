"""
Amazon Rekognition を使用したオブジェクト検出サンプル

このモジュールは画像内のオブジェクトを検出し、ラベル付けを行います。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* AmazonRekognitionFullAccess

または、最小権限として以下のアクションを許可してください：

* rekognition:DetectLabels

推奨されるサンプルデータ
----------------------
data/objects.png : 様々な物が写った写真
- オフィスの風景
- 公園や街並みの風景
- 室内のインテリア
- 複数の物が写った静物写真
"""
import json
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
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
SAMPLE_IMAGE = DATA_DIR / 'objects.png'  # オブジェクト検出用：様々な物が写った写真

# Rekognitionクライアント作成
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)


def analyze_image(image_path):
    """
    画像を分析してオブジェクトを検出する関数
    
    :param image_path: 分析する画像ファイルのパス
    :type image_path: str
    :return: 検出されたラベルのリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        with open(image_path, 'rb') as image:
            response = rekognition.detect_labels(
                Image={'Bytes': image.read()},
                MaxLabels=10,
                MinConfidence=70
            )
        
        # 結果をファイルに保存
        json_file = RESULTS_DIR / f"{Path(image_path).stem}_labels.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=4)

        result_file = RESULTS_DIR / f"{Path(image_path).stem}_labels.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {image_path} の分析結果 ===\n")
            for label in response['Labels']:
                f.write(f"- {label['Name']}: {label['Confidence']:.1f}%\n")
        
        print(f"=== {image_path} の分析結果 ===")
        labels = []
        for label in response['Labels']:
            print(f"- {label['Name']}: {label['Confidence']:.1f}%")
            labels.append(label)
        
        print(f"\n分析結果は '{result_file}' に保存されました。")
        return labels
            
    except FileNotFoundError:
        print(f"エラー: 指定された画像ファイル '{image_path}' が見つかりません。")
        return None
    except ClientError as e:
        print(f"AWS Rekognitionエラーが発生しました: {e}")
        # 例外の詳細情報を表示（デバッグ用）
        # print(e.response['Error']['Code'])
        # print(e.response['Error']['Message'])
        return None
    except Exception as e:
        print(f"画像分析エラー: {e}")
        return None


if __name__ == "__main__":
    if not SAMPLE_IMAGE.exists():
        print("\n=== サンプルデータが不足しています ===")
        print("以下のファイルを data ディレクトリに配置してください：")
        print("（.jpg または .png 形式）\n")
        print("- objects.png : 様々な物が写った写真（オフィス、公園、街並みなど）")
    else:
        analyze_image(SAMPLE_IMAGE) 