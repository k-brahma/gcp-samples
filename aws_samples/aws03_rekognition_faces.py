"""
Amazon Rekognition を使用した顔検出サンプル

このモジュールは画像から顔を検出し、年齢・性別・感情などの分析を行います。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* AmazonRekognitionFullAccess

または、最小権限として以下のアクションを許可してください：

* rekognition:DetectFaces

推奨されるサンプルデータ
----------------------
data/faces.png : 複数人の顔が写った写真
- 会議やイベントの集合写真
- 異なる表情や年齢の人物を含む写真
- 正面から撮影された顔写真

- 検出される感情タイプとその意味:
    HAPPY: 幸せ
    SAD: 悲しい
    ANGRY: 怒り
    CONFUSED: 困惑
    DISGUSTED: 嫌悪
    SURPRISED: 驚き
    CALM: 穏やか
    UNKNOWN: 不明
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
SAMPLE_IMAGE = DATA_DIR / 'faces.png'  # 顔認識用：複数人の顔が写った写真

# Rekognitionクライアント作成
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)


def detect_faces(image_path):
    """
    顔検出（年齢・性別・感情も推定）する関数
    
    :param image_path: 分析する画像ファイルのパス
    :type image_path: str
    :return: 検出された顔の詳細情報のリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        with open(image_path, 'rb') as image:
            response = rekognition.detect_faces(
                Image={'Bytes': image.read()},
                Attributes=['ALL']
            )
        
        # 結果をファイルに保存
        json_file = RESULTS_DIR / f"{Path(image_path).stem}_faces.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=4)
        
        result_file = RESULTS_DIR / f"{Path(image_path).stem}_faces.txt"
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {image_path} の顔分析結果 ===\n")
            for i, face in enumerate(response['FaceDetails']):
                f.write(f"顔 {i+1}:\n")
                f.write(f"  年齢: {face['AgeRange']['Low']}-{face['AgeRange']['High']}歳\n")
                f.write(f"  性別: {face['Gender']['Value']} ({face['Gender']['Confidence']:.1f}%)\n")
                emotions = face['Emotions']
                top_emotion = max(emotions, key=lambda x: x['Confidence'])
                f.write(f"  感情: {top_emotion['Type']} ({top_emotion['Confidence']:.1f}%)\n")
        
        print(f"=== {image_path} の顔分析結果 ===")
        faces = []
        for i, face in enumerate(response['FaceDetails']):
            print(f"顔 {i+1}:")
            print(f"  年齢: {face['AgeRange']['Low']}-{face['AgeRange']['High']}歳")
            print(f"  性別: {face['Gender']['Value']} ({face['Gender']['Confidence']:.1f}%)")
            
            # 感情分析
            emotions = face['Emotions']
            top_emotion = max(emotions, key=lambda x: x['Confidence'])
            print(f"  感情: {top_emotion['Type']} ({top_emotion['Confidence']:.1f}%)")
            faces.append(face)
        
        print(f"\n分析結果は '{result_file}' に保存されました。")
        return faces
            
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
        print(f"予期せぬ顔検出エラー: {e}")
        return None

if __name__ == "__main__":
    if not SAMPLE_IMAGE.exists():
        print("\n=== サンプルデータが不足しています ===")
        print("以下のファイルを data ディレクトリに配置してください：")
        print("（.jpg または .png 形式）\n")
        print("- faces.png : 複数人の顔が写った写真（会議やイベントの集合写真など）")
    else:
        detect_faces(SAMPLE_IMAGE) 