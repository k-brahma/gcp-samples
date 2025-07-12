"""
Amazon Comprehend を使用した感情分析サンプル

このモジュールはテキストの感情やキーワードを分析する機能を提供します。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* ComprehendFullAccess

または、最小権限として以下のアクションを許可してください：

* comprehend:DetectSentiment
* comprehend:DetectKeyPhrases
* comprehend:DetectDominantLanguage
* comprehend:DetectEntities
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

# Comprehendクライアント作成
comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)


def analyze_sentiment(text):
    """
    テキストの感情分析を行う関数
    
    :param text: 分析するテキスト
    :type text: str
    :return: 感情分析結果の辞書。エラーの場合はNone
    :rtype: dict
    """
    try:
        response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='ja'  # 日本語
        )
        
        sentiment = response['Sentiment']
        scores = response['SentimentScore']
        
        print(f"テキスト: {text}")
        print(f"総合感情: {sentiment}")
        print(f"ポジティブ: {scores['Positive']:.3f}")
        print(f"ネガティブ: {scores['Negative']:.3f}")
        print(f"ニュートラル: {scores['Neutral']:.3f}")
        print(f"混合: {scores['Mixed']:.3f}")
        
        return response
        
    except Exception as e:
        print(f"感情分析エラー: {e}")
        return None


def extract_key_phrases(text):
    """
    キーフレーズ抽出を行う関数
    
    :param text: 分析するテキスト
    :type text: str
    :return: キーフレーズのリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        response = comprehend.detect_key_phrases(
            Text=text,
            LanguageCode='ja'
        )
        
        print(f"\n=== キーフレーズ ===")
        key_phrases = []
        for phrase in response['KeyPhrases']:
            print(f"- {phrase['Text']} (信頼度: {phrase['Score']:.3f})")
            key_phrases.append(phrase)
        
        return key_phrases
            
    except Exception as e:
        print(f"キーフレーズ抽出エラー: {e}")
        return None


def detect_entities(text):
    """
    エンティティ（人名、地名など）を検出する関数
    
    :param text: 分析するテキスト
    :type text: str
    :return: エンティティのリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        response = comprehend.detect_entities(
            Text=text,
            LanguageCode='ja'
        )
        
        print(f"\n=== 検出されたエンティティ ===")
        entities = []
        for entity in response['Entities']:
            print(f"- {entity['Text']} ({entity['Type']}) 信頼度: {entity['Score']:.3f}")
            entities.append(entity)
        
        return entities
            
    except Exception as e:
        print(f"エンティティ検出エラー: {e}")
        return None


def detect_language(text):
    """
    テキストの言語を検出する関数
    
    :param text: 分析するテキスト
    :type text: str
    :return: 検出された言語コード。エラーの場合はNone
    :rtype: str
    """
    try:
        response = comprehend.detect_dominant_language(Text=text)
        
        dominant_language = response['Languages'][0]
        print(f"\n=== 言語検出結果 ===")
        print(f"言語: {dominant_language['LanguageCode']} (信頼度: {dominant_language['Score']:.3f})")
        
        return dominant_language['LanguageCode']
            
    except Exception as e:
        print(f"言語検出エラー: {e}")
        return None


if __name__ == "__main__":
    # 使用例
    texts = [
        "今日は最高に楽しい一日でした！友達と美味しいランチを食べて、映画も面白かったです。",
        "電車が遅れて会議に遅刻してしまい、とても困りました。本当にイライラします。",
        "今日は普通の日でした。特に何も起こりませんでした。",
        "カルモジインの田舎は大理石の産地でそこで私は夏を過ごしたことがあった。"
    ]
    
    print("=== Amazon Comprehend 感情分析サンプル ===\n")
    
    for i, text in enumerate(texts, 1):
        print(f"--- テストケース {i} ---")
        print("="*60)
        
        # 感情分析
        analyze_sentiment(text)
        
        # キーフレーズ抽出
        extract_key_phrases(text)
        
        # エンティティ検出
        detect_entities(text)
        
        # 言語検出
        detect_language(text)
        
        print("\n") 