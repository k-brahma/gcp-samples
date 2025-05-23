"""
Amazon Polly を使用したテキスト読み上げサンプル

このモジュールは日本語テキストを音声ファイルに変換する機能を提供します。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* AmazonPollyFullAccess

または、最小権限として以下のアクションを許可してください：

* polly:SynthesizeSpeech
* polly:DescribeVoices
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

# 出力ディレクトリの設定
RESULTS_DIR = Path(__file__).parent / 'results'
RESULTS_DIR.mkdir(exist_ok=True)

# Pollyクライアント作成（認証情報を明示的に指定）
polly = boto3.client(
    'polly',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)


def text_to_speech(text, output_file='speech.mp3', voice_id='Mizuki', engine='standard'):
    """
    テキストを音声ファイルに変換する関数
    
    :param text: 音声化するテキスト
    :type text: str
    :param output_file: 出力ファイル名（デフォルト: 'speech.mp3'）
    :type output_file: str
    :param voice_id: 使用する音声ID（デフォルト: 'Mizuki'）
    :type voice_id: str
    :param engine: 使用する音声エンジン（'standard' または 'neural'）（デフォルト: 'standard'）
    :type engine: str # ★ここを追加
    :return: 成功した場合True、失敗した場合False
    :rtype: bool
    """
    try:
        # 出力ファイルパスの設定
        output_path = RESULTS_DIR / output_file
        
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,  # 使用する音声ID
            LanguageCode='ja-JP',
            Engine=engine
        )
        
        # 音声データをファイルに保存
        with open(output_path, 'wb') as file:
            file.write(response['AudioStream'].read())
        
        print(f"音声ファイル '{output_path}' を作成しました！ engine: {engine}")
        return True
    except Exception as e:
        print(f"音声生成エラー: {e}")
        return False


def list_voices(language_code='ja-JP'):
    """
    利用可能な音声リストを取得する関数
    
    :param language_code: 言語コード（デフォルト: 'ja-JP'）
    :type language_code: str
    :return: 音声リスト。エラーの場合はNone
    :rtype: list
    """
    try:
        response = polly.describe_voices(LanguageCode=language_code)
        return response['Voices']
    except Exception as e:
        print(f"音声リスト取得エラー: {e}")
        return None


if __name__ == "__main__":
    # 使用例
    japanese_text = "こんにちは！私はAmazon Pollyです。日本語を自然な音声で読み上げることができます。"
    
    print("=== Amazon Polly テキスト読み上げサンプル ===")
    print(f"テキスト: {japanese_text}")
    
    # 音声ファイル生成
    if text_to_speech(japanese_text):
        print("音声ファイルの生成が完了しました。")
    
    print("\n=== 利用可能な日本語音声一覧 ===")
    voices = list_voices()
    if voices:
        for voice in voices:
            print(f"- {voice['Name']} ({voice['Gender']})") 

        # 音質には standard と neural がある
        for voice in voices:
            if 'standard' in voice['SupportedEngines']:
                text_to_speech(japanese_text, f"speech-{voice['Name']}-standard.mp3", voice['Name'])
            else:
                text_to_speech(japanese_text, f"speech-{voice['Name']}-neural.mp3", voice['Name'], engine='neural')
