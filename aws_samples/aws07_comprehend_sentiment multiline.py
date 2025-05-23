"""
Amazon Comprehend を使用した感情分析、キーフレーズ抽出、エンティティ検出、言語検出サンプル

このモジュールはテキストの感情、キーフレーズ、エンティティ、言語を分析する機能を提供します。
複数行のテキストを分析することも可能です。

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

# Comprehendクライアント作成
comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)

# 入力ディレクトリと出力ディレクトリの設定
DATA_DIR = Path(__file__).parent / 'data'
RESULTS_DIR = Path(__file__).parent / 'results' / 'comprehend'
RESULTS_DIR.mkdir(parents=True, exist_ok=True) # results / comprehend ディレクトリがなければ作成


def analyze_sentiment(text):
    """
    テキストの感情分析を行う関数
    
    検出される感情タイプとその意味:
    POSITIVE: ポジティブな感情
    NEGATIVE: ネガティブな感情
    NEUTRAL: 中立的な感情
    MIXED: 複数の感情が混在している
    
    :param text: 分析するテキスト（str）
    :return: 感情分析結果の辞書。エラーの場合はNone
    :rtype: dict
    """
    try:
        response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='ja'  # 日本語を指定
        )
        
        sentiment = response['Sentiment']
        scores = response['SentimentScore']
        
        print(f"  総合感情: {sentiment}")
        print(f"  ポジティブ: {scores['Positive']:.3f}")
        print(f"  ネガティブ: {scores['Negative']:.3f}")
        print(f"  ニュートラル: {scores['Neutral']:.3f}")
        print(f"  混合: {scores['Mixed']:.3f}")
        
        return response
            
    except ClientError as e: # AWS APIからのエラーをキャッチ
        print(f"感情分析エラー (AWS ClientError): {e}")
        return None
    except Exception as e:
        print(f"感情分析エラー: {e}")
        return None


def extract_key_phrases(text):
    """
    キーフレーズ抽出を行う関数
    
    :param text: 分析するテキスト（str）
    :return: キーフレーズのリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        response = comprehend.detect_key_phrases(
            Text=text,
            LanguageCode='ja' # 日本語を指定
        )
        
        print(f"  \n=== キーフレーズ ===")
        key_phrases = []
        if not response['KeyPhrases']:
            print("  キーフレーズは検出されませんでした。")
        for phrase in response['KeyPhrases']:
            print(f"  - {phrase['Text']} (信頼度: {phrase['Score']:.3f})")
            key_phrases.append(phrase)
        
        return key_phrases
            
    except ClientError as e: # AWS APIからのエラーをキャッチ
        print(f"キーフレーズ抽出エラー (AWS ClientError): {e}")
        return None
    except Exception as e:
        print(f"キーフレーズ抽出エラー: {e}")
        return None


def detect_entities(text):
    """
    エンティティ（人名、地名など）を検出する関数
    
    検出されるエンティティタイプとその意味:
    PERSON: 人物
    LOCATION: 地名、場所
    ORGANIZATION: 組織名
    COMMERCIAL_ITEM: 商品名
    EVENT: イベント名
    DATE: 日付
    QUANTITY: 数量
    TITLE: 役職、肩書き
    OTHER: 上記以外のエンティティ
    
    :param text: 分析するテキスト（str）
    :return: エンティティのリスト。エラーの場合はNone
    :rtype: list
    """
    try:
        response = comprehend.detect_entities(
            Text=text,
            LanguageCode='ja' # 日本語を指定
        )
        
        print(f"  \n=== 検出されたエンティティ ===")
        entities = []
        if not response['Entities']:
            print("  エンティティは検出されませんでした。")
        for entity in response['Entities']:
            print(f"  - {entity['Text']} ({entity['Type']}) 信頼度: {entity['Score']:.3f}")
            entities.append(entity)
        
        return entities
            
    except ClientError as e: # AWS APIからのエラーをキャッチ
        print(f"エンティティ検出エラー (AWS ClientError): {e}")
        return None
    except Exception as e:
        print(f"エンティティ検出エラー: {e}")
        return None


def detect_language(text):
    """
    テキストの主要な言語を検出する関数
    
    :param text: 分析するテキスト（str）
    :return: 検出された言語コード。エラーの場合はNone
    :rtype: str
    """
    try:
        response = comprehend.detect_dominant_language(Text=text)
        
        dominant_language = None
        if response['Languages']:
            dominant_language = response['Languages'][0]
            print(f"  \n=== 言語検出結果 ===")
            print(f"  言語: {dominant_language['LanguageCode']} (信頼度: {dominant_language['Score']:.3f})")
        else:
            print("  言語は検出されませんでした。")
        
        return dominant_language['LanguageCode'] if dominant_language else None
            
    except ClientError as e: # AWS APIからのエラーをキャッチ
        print(f"言語検出エラー (AWS ClientError): {e}")
        return None
    except Exception as e:
        print(f"言語検出エラー: {e}")
        return None


def save_results(filename_base, text_content, sentiment_result, key_phrases, entities, language_code):
    """
    分析結果をファイルに保存する関数
    
    :param filename_base: 基本となるファイル名（拡張子なし）
    :param text_content: 分析対象のテキスト内容
    :param sentiment_result: 感情分析の結果
    :param key_phrases: キーフレーズのリスト
    :param entities: エンティティのリスト
    :param language_code: 検出された言語コード
    """
    # 全結果を含む辞書を作成
    all_results = {
        'filename': filename_base,
        'original_text': text_content, # 元のテキスト内容を追加
        'sentiment': sentiment_result,
        'key_phrases': key_phrases,
        'entities': entities,
        'language': language_code
    }
    
    # 全体のJSONファイルに保存
    json_path = RESULTS_DIR / f"{filename_base}_summary.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n全体のJSON結果を保存しました: {json_path}")
    
    # 感情分析結果を保存（テキストとJSON）
    sentiment_txt_path = RESULTS_DIR / f"{filename_base}_sentiment.txt"
    sentiment_json_path = RESULTS_DIR / f"{filename_base}_sentiment.json"
    
    with open(sentiment_txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Amazon Comprehend 感情分析結果 ({filename_base}) ===\n\n")
        f.write(f"--- 分析テキスト ---\n{text_content}\n\n")
        if sentiment_result:
            f.write(f"--- 分析結果 ---\n")
            f.write(f"総合感情: {sentiment_result['Sentiment']}\n")
            f.write(f"ポジティブ: {sentiment_result['SentimentScore']['Positive']:.3f}\n")
            f.write(f"ネガティブ: {sentiment_result['SentimentScore']['Negative']:.3f}\n")
            f.write(f"ニュートラル: {sentiment_result['SentimentScore']['Neutral']:.3f}\n")
            f.write(f"混合: {sentiment_result['SentimentScore']['Mixed']:.3f}\n")
        else:
            f.write("感情分析結果は取得できませんでした。\n")
    
    with open(sentiment_json_path, 'w', encoding='utf-8') as f:
        json.dump(sentiment_result, f, ensure_ascii=False, indent=2)
    
    print(f"感情分析結果を保存しました: {sentiment_txt_path}, {sentiment_json_path}")
    
    # キーフレーズを保存（テキストとJSON）
    key_phrases_txt_path = RESULTS_DIR / f"{filename_base}_key_phrases.txt"
    key_phrases_json_path = RESULTS_DIR / f"{filename_base}_key_phrases.json"
    
    with open(key_phrases_txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== キーフレーズ ({filename_base}) ===\n\n")
        f.write(f"--- 分析テキスト ---\n{text_content}\n\n")
        f.write(f"--- 検出されたキーフレーズ ---\n")
        if key_phrases:
            for phrase in key_phrases:
                f.write(f"- {phrase['Text']} (信頼度: {phrase['Score']:.3f})\n")
        else:
            f.write("キーフレーズは検出されませんでした。\n")
    
    with open(key_phrases_json_path, 'w', encoding='utf-8') as f:
        json.dump(key_phrases, f, ensure_ascii=False, indent=2)
    
    print(f"キーフレーズを保存しました: {key_phrases_txt_path}, {key_phrases_json_path}")
    
    # エンティティを保存（テキストとJSON）
    entities_txt_path = RESULTS_DIR / f"{filename_base}_entities.txt"
    entities_json_path = RESULTS_DIR / f"{filename_base}_entities.json"
    
    with open(entities_txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== 検出されたエンティティ ({filename_base}) ===\n\n")
        f.write(f"--- 分析テキスト ---\n{text_content}\n\n")
        f.write(f"--- 検出されたエンティティ ---\n")
        if entities:
            for entity in entities:
                f.write(f"- {entity['Text']} ({entity['Type']}) 信頼度: {entity['Score']:.3f}\n")
        else:
            f.write("エンティティは検出されませんでした。\n")
    
    with open(entities_json_path, 'w', encoding='utf-8') as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)
    
    print(f"エンティティを保存しました: {entities_txt_path}, {entities_json_path}")
    
    # 言語検出結果を保存（テキストとJSON）
    language_txt_path = RESULTS_DIR / f"{filename_base}_language.txt"
    language_json_path = RESULTS_DIR / f"{filename_base}_language.json"
    
    with open(language_txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== 言語検出結果 ({filename_base}) ===\n\n")
        f.write(f"--- 分析テキスト ---\n{text_content}\n\n")
        f.write(f"--- 検出された言語 ---\n")
        if language_code:
            f.write(f"検出された言語: {language_code}\n")
        else:
            f.write("言語は検出されませんでした。\n")
    
    with open(language_json_path, 'w', encoding='utf-8') as f:
        json.dump({'language_code': language_code}, f, ensure_ascii=False, indent=2)
    
    print(f"言語検出結果を保存しました: {language_txt_path}, {language_json_path}")


if __name__ == "__main__":
    # 分析対象のテキストファイルを指定 (data/comprehend_sample*.txt)
    # ここにエモい文章のファイル名をリストで指定します
    sample_file_names = [
        'comprehend_sample1',
        'comprehend_sample2',
        'comprehend_sample3',
        # 必要に応じて 'comprehend_sample_english' なども追加
    ]

    print("=== Amazon Comprehend 複数テキスト分析サンプル ===\n")

    for file_name_base in sample_file_names:
        text_file_path = DATA_DIR / f"{file_name_base}.txt"

        if not text_file_path.exists():
            print(f"エラー: テキストファイル '{text_file_path}' が見つかりません。")
            print("指定されたファイルを 'data/' ディレクトリに配置してください。\n")
            continue
        
        print(f"--- 処理中: {text_file_path.name} ---")
        print("="*60)
        
        # ファイルの内容を読み込む
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()

        print(f"分析テキスト:\n{text_content}\n")

        # 各種分析を実行
        sentiment_result = analyze_sentiment(text_content)
        key_phrases = extract_key_phrases(text_content)
        entities = detect_entities(text_content)
        language_code = detect_language(text_content)
        
        # 結果をファイルに保存
        save_results(file_name_base, text_content, sentiment_result, key_phrases, entities, language_code)
        
        print("\n" + "="*60 + "\n")