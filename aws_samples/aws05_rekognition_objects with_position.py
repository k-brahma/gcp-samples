"""
Amazon Rekognition を使用したオブジェクト検出サンプル

このモジュールは画像内のオブジェクトを検出し、ラベル付けを行います。
また、検出された物体の位置情報（バウンディングボックス）も取得し、詳細な分析結果を出力します。
レスポンスはJSON形式で出力され、Pythonのデータ構造を理解しやすくなっています。

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
from botocore.exceptions import ClientError  # エラーハンドリングのために追加
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
        # 画像ファイルが存在するかチェック
        if not Path(image_path).exists():
            print(f"エラー: 指定された画像ファイル '{image_path}' が見つかりません。")
            return None

        with open(image_path, 'rb') as image:
            response = rekognition.detect_labels(
                Image={'Bytes': image.read()},
                MaxLabels=10,       # 検出するラベルの最大数
                MinConfidence=70    # 検出の最小信頼度
            )
        
        # 結果をJSONファイルに保存 (ラベルとその詳細情報のみを保存)
        json_file = RESULTS_DIR / f"{Path(image_path).stem}_labels_with_position.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            # インデント付きで整形されたJSONを出力し、日本語も正しく表示
            json.dump(response['Labels'], f, indent=2, ensure_ascii=False)
        
        # 結果をテキストファイルに保存
        txt_file = RESULTS_DIR / f"{Path(image_path).stem}_labels_with_position.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {image_path} の分析結果 ===\n")
            if not response['Labels']:
                f.write("  ラベルは検出されませんでした。\n")
            for label in response['Labels']:
                f.write(f"- ラベル名: {label['Name']}\n")
                f.write(f"  信頼度: {label['Confidence']:.1f}%\n")
                
                # 検出されたオブジェクトのインスタンス（位置情報）がある場合
                if label.get('Instances'):
                    for i, instance in enumerate(label['Instances']):
                        bbox = instance['BoundingBox']
                        # バウンディングボックスの座標を整形して出力
                        f.write(f"  - インスタンス {i+1}:\n")
                        f.write(f"    位置 (正規化): 左({bbox['Left']:.2f}), 上({bbox['Top']:.2f}), "
                                f"幅({bbox['Width']:.2f}), 高さ({bbox['Height']:.2f})\n")
                        f.write(f"    位置の信頼度: {instance['Confidence']:.1f}%\n")
                
                # 上位カテゴリがある場合
                if label.get('Parents'):
                    parent_names = [p['Name'] for p in label['Parents']]
                    f.write(f"  上位カテゴリ: {', '.join(parent_names)}\n")
                f.write("---\n") # 各ラベルの区切り
        
        # コンソールに結果を表示
        print(f"\n=== {image_path} の分析結果 ===")
        print("以下に検出されたラベルと詳細情報を表示します。")
        labels_found = False
        if not response['Labels']:
            print("  ラベルは検出されませんでした。")
        for label in response['Labels']:
            labels_found = True
            print(f"- ラベル名: {label['Name']}")
            print(f"  信頼度: {label['Confidence']:.1f}%")
            
            if label.get('Instances'):
                for i, instance in enumerate(label['Instances']):
                    bbox = instance['BoundingBox']
                    print(f"  - インスタンス {i+1}:")
                    print(f"    位置 (正規化): 左({bbox['Left']:.2f}), 上({bbox['Top']:.2f}), "
                          f"幅({bbox['Width']:.2f}), 高さ({bbox['Height']:.2f})")
                    print(f"    位置の信頼度: {instance['Confidence']:.1f}%")
            
            if label.get('Parents'):
                parent_names = [p['Name'] for p in label['Parents']]
                print(f"  上位カテゴリ: {', '.join(parent_names)}")
            print("---") # 各ラベルの区切り
        
        if labels_found:
            print(f"\n詳細な分析結果は '{json_file}' と '{txt_file}' に保存されました。")
        
        return response['Labels']
            
    except FileNotFoundError:
        print(f"エラー: 指定された画像ファイル '{image_path}' が見つかりません。")
        return None
    except ClientError as e:
        print(f"AWS Rekognitionエラーが発生しました: {e}")
        # 詳細なエラー情報を表示することも可能（必要に応じてコメントを解除）
        # print(f"  エラーコード: {e.response['Error']['Code']}")
        # print(f"  メッセージ: {e.response['Error']['Message']}")
        return None
    except Exception as e:
        print(f"予期せぬ画像分析エラーが発生しました: {e}")
        return None


if __name__ == "__main__":
    if not SAMPLE_IMAGE.exists():
        print("\n=== サンプルデータが不足しています ===")
        print("以下のファイルを data ディレクトリに配置してください：")
        print(f"  - {SAMPLE_IMAGE.name} (.jpg または .png 形式)")
        print("\n例: オフィス、公園、街並み、室内のインテリア、複数の物が写った静物写真など")
    else:
        analyze_image(SAMPLE_IMAGE)