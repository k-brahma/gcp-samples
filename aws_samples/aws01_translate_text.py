"""
Amazon Translate を使用した翻訳サンプル

このモジュールはテキストの翻訳と言語検出機能を提供します。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* TranslateFullAccess

または、最小権限として以下のアクションを許可してください：

* translate:TranslateText
* translate:DetectDominantLanguage

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


def translate_text(text, source_lang, target_lang):
    """
    テキストを翻訳する関数
    
    :param text: 翻訳するテキスト
    :type text: str
    :param source_lang: 元の言語コード（例：'ja', 'en'）
    :type source_lang: str
    :param target_lang: 翻訳先の言語コード（例：'en', 'ja'）
    :type target_lang: str
    :return: 翻訳されたテキスト。エラーの場合はNone
    :rtype: str
    """
    # Translateクライアントの作成（認証情報を明示的に指定）
    translate = boto3.client(
        'translate',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=AWS_DEFAULT_REGION
    )

    try:
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"翻訳エラー: {e}")
        return None


def detect_language(text):
    """
    テキストの言語の判定のみをする関数 comprehendを使用
    
    :param text: 言語を検出するテキスト
    :type text: str
    :return: 検出された言語コード。エラーの場合はNone
    :rtype: str
    """
    try:
        comprehend = boto3.client(
            'comprehend',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=AWS_DEFAULT_REGION
        )
        response = comprehend.detect_dominant_language(Text=text)
        return response['Languages'][0]['LanguageCode']
    except Exception as e:
        print(f"言語検出エラー: {e}")
        return None


if __name__ == "__main__":
    # 日本語を英語にします。
    japanese_text = "今日はいい天気ですね！"
    english_result = translate_text(japanese_text, 'ja', 'en')
    print(f"日本語: {japanese_text}")
    print(f"英語: {english_result}")
    print("--------------------------------\n")
    
    # 英語を日本語にします。
    english_text = "Recently, I've been working on a project that uses various API services."
    japanese_result = translate_text(english_text, 'en', 'ja')
    print(f"英語: {english_text}")
    print(f"日本語: {japanese_result}")
    print("--------------------------------\n")

    # 言語を自動判定して翻訳します。
    auth_text = "Bonjour, comment allez-vous? C'est un beau jour."
    detected_result = translate_text(auth_text, 'auto', 'ja')
    print(f"不明な言語: {auth_text}")
    print(f"日本語: {detected_result}")
    print("--------------------------------\n")

    # 言語の自動判定のみを行います。
    test_text = "回答はインターネットでも行うことができます。ぜひご活用ください。"
    detected_lang = detect_language(test_text)
    print(f"テストテキスト: {test_text}")
    print(f"検出された言語: {detected_lang}") 
    print("--------------------------------\n")

