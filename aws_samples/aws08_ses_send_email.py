"""
Amazon SES を使用したメール送信サンプル

このモジュールは、テキストメールおよびHTMLメールを送信する機能を提供します。

必要なAWS IAMポリシー
----------------------
以下のポリシーをIAMユーザーまたはロールにアタッチしてください：

* AmazonSESFullAccess (推奨、テスト用)

または、最小権限として以下のアクションを許可してください：

* ses:SendEmail
* ses:SendRawEmail (HTMLメールや添付ファイル付きメールの場合)

注意:
- 送信元メールアドレスは、Amazon SES で検証済みである必要があります。
- AWSアカウントがSESサンドボックス環境にある場合、送信先メールアドレスも検証済みである必要があります。
  サンドボックス環境外に送信するには、AWSにリクエストして本番アクセスを取得する必要があります。
"""

import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# .envファイルを明示的に指定して読み込み
# aws01_translate ディレクトリ内に .env があることを想定
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # .envファイルが存在しない場合、環境変数から直接読み込もうと試みる
    # GitHub ActionsなどのCI環境では.envファイルがない場合があるため
    print(f"情報: .env ファイルが見つかりません ({env_path})。環境変数を直接使用します。")


# 認証情報を取得
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
# SESが利用可能なリージョンを指定。東京リージョンをデフォルトに設定。
# 利用可能なリージョン例: us-east-1, us-west-2, eu-west-1, ap-northeast-1
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-1')

if not all([aws_access_key_id, aws_secret_access_key, AWS_DEFAULT_REGION]):
    raise ValueError("AWS認証情報（アクセスキーID、シークレットアクセスキー）またはリージョンが設定されていません。環境変数または.envファイルを確認してください。")

# SESクライアント作成
ses = boto3.client(
    'ses',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=AWS_DEFAULT_REGION
)

# .envファイルまたは環境変数からメールアドレスを読み込む
# これらは事前にSESで検証済みである必要があります（サンドボックス環境の場合、受信者も）。
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'seminar@pc5bai.com')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'k.brahma.nirvana@gmail.com')

# 文字コード
CHARSET = "UTF-8"

# データファイルのパス
DATA_DIR = Path(__file__).parent / 'data'
TEXT_BODY_FILE = DATA_DIR / 'mail_body.txt'
HTML_BODY_FILE = DATA_DIR / 'mail_body.html'


def read_file_content(file_path):
    """指定されたファイルを読み込み、内容を文字列として返す"""
    try:
        with open(file_path, 'r', encoding=CHARSET) as f:
            return f.read()
    except FileNotFoundError:
        print(f"エラー: メール本文ファイルが見つかりません: {file_path}")
        return None
    except Exception as e:
        print(f"エラー: ファイル読み込み中にエラーが発生しました ({file_path}): {e}")
        return None


def send_plain_text_email(subject, body_text, recipient=RECIPIENT_EMAIL, sender=SENDER_EMAIL):
    """
    プレーンテキスト形式のメールを送信する関数

    :param subject: メールの件名
    :type subject: str
    :param body_text: メールの本文 (テキスト)
    :type body_text: str
    :param recipient: 受信者メールアドレス
    :type recipient: str
    :param sender: 送信者メールアドレス (SESで検証済みであること)
    :type sender: str
    :return: メッセージID。エラーの場合はNone
    :rtype: str
    """
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    except ClientError as e:
        print(f"メール送信エラー (テキスト): {e.response['Error']['Message']}")
        return None
    else:
        print(f"テキストメール送信成功！ Message ID: {response['MessageId']}")
        return response['MessageId']


def send_html_email(subject, body_html, body_text, recipient=RECIPIENT_EMAIL, sender=SENDER_EMAIL):
    """
    HTML形式のメールを送信する関数 (フォールバック用のテキスト本文も含む)

    :param subject: メールの件名
    :type subject: str
    :param body_html: メールの本文 (HTML)
    :type body_html: str
    :param body_text: メールの本文 (HTML非対応クライアント用のプレーンテキスト)
    :type body_text: str
    :param recipient: 受信者メールアドレス
    :type recipient: str
    :param sender: 送信者メールアドレス (SESで検証済みであること)
    :type sender: str
    :return: メッセージID。エラーの場合はNone
    :rtype: str
    """
    if sender == 'your-verified-sender-email@example.com' or \
       recipient == 'recipient-email@example.com':
        print("エラー: 送信元または受信先のメールアドレスがデフォルト値のままです。")
        print(".envファイルで SENDER_EMAIL と RECIPIENT_EMAIL を設定してください。")
        return None

    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': { # HTML非対応メーラー用のフォールバック
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    except ClientError as e:
        print(f"メール送信エラー (HTML): {e.response['Error']['Message']}")
        return None
    else:
        print(f"HTMLメール送信成功！ Message ID: {response['MessageId']}")
        return response['MessageId']


if __name__ == "__main__":
    print("=== Amazon SES メール送信サンプル ===")

    # --- プレーンテキストメールの送信例 ---
    print("\n--- プレーンテキストメール送信テスト ---")
    subject_text = "SES テストメール (テキスト)"
    body_text_content = read_file_content(TEXT_BODY_FILE)
    
    if body_text_content:
        send_plain_text_email(subject_text, body_text_content)
    else:
        print("テキストメールの本文が読み込めなかったため、送信をスキップしました。")
    print("--------------------------------\n")

    # --- HTMLメールの送信例 ---
    print("\n--- HTMLメール送信テスト ---")
    subject_html = "SES テストメール (HTML)"
    body_html_content = read_file_content(HTML_BODY_FILE)
    
    # HTMLメール用のフォールバックテキスト (テキストファイルの内容を再利用)
    body_text_for_html = body_text_content 
    
    if body_html_content and body_text_for_html:
        send_html_email(subject_html, body_html_content, body_text_for_html)
    elif not body_html_content:
        print("HTMLメールの本文が読み込めなかったため、送信をスキップしました。")
    elif not body_text_for_html:
        print("HTMLメールのフォールバックテキスト本文が読み込めなかったため、送信をスキップしました。")

    print("--------------------------------\n")

    print("サンプル実行完了。")
    print("実際のメール送信には、SENDER_EMAILとRECIPIENT_EMAILが正しく設定され、")
    print("送信元メールアドレスがSESで検証済みである必要があります。")
    print("また、AWSアカウントがサンドボックス環境の場合は、受信先も検証済みである必要があります。") 