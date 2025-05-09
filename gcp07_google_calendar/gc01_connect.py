'''
Google Calendar API への接続を確立し、認証を行うためのモジュール。

このモジュールは、Google Calendar API サービスへの接続と認証を処理します。
サービスアカウントの認証情報を使用し、指定されたスコープでAPIクライアントを構築します。

主な機能:
  - Google Calendar API への認証済みサービスオブジェクトの提供

設定:
  - ``CREDENTIALS_FILE``: スクリプトと同じディレクトリにある ``credentials.json`` を
    サービスアカウントのJSONキーファイルとして使用します。
  - ``CALENDAR_ID``: 環境変数 ``GOOGLE_CALENDAR_ID`` または直接指定により、
    操作対象のGoogle Calendar IDを設定します。
  - ``SCOPES``: 必要なAPIスコープを指定します。

使用方法:
  1. 上記設定値を確認・設定します。
  2. :func:`connect_to_calendar` 関数を呼び出して、認証済みのサービスオブジェクトを取得します。

必要なライブラリ:
  - google.oauth2.service_account
  - googleapiclient.discovery
  - pathlib

注意:
  - サービスアカウントキーファイル (credentials.json) は、安全な場所に保管し、
    適切にアクセス権を管理してください。
  - スコープは、アプリケーションが必要とする最小限の権限に設定してください。
'''

import os
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')

# Google Calendar API のスコープ ref: https://developers.google.com/calendar/api/guides/auth
SCOPES = ['https://www.googleapis.com/auth/calendar']

def connect_to_calendar():
    '''Google Calendar API への接続と認証を行う。

    サービスアカウントの認証情報を使用し、指定されたスコープで
    Google Calendar APIサービスクライアントを構築して返します。

    :returns: 認証済みのCalendar APIサービスオブジェクト。
              認証に失敗した場合は None。
    :rtype: googleapiclient.discovery.Resource or None
    :raises FileNotFoundError: 認証情報ファイルが見つからない場合。
    :raises Exception: その他のAPIクライアント構築時のエラー。
    '''
    try:
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
        print("Google Calendar APIへの接続に成功しました。")
        return service
    except FileNotFoundError:
        print(f"エラー: 認証情報ファイルが見つかりません: {CREDENTIALS_FILE}")
        print("Google Cloudのサービスアカウントキーファイルへのパスを正しく設定してください。")
        return None
    except Exception as e:
        print(f"Google Calendar APIへの接続中にエラーが発生しました: {e}")
        return None


if __name__ == '__main__':
    # モジュールの動作テスト
    service = connect_to_calendar()
    if service:
        print("Calendarサービスオブジェクトが正常に取得されました。")
        print(f"使用するカレンダーID: {CALENDAR_ID}")
    else:
        print("Calendarサービスオブジェクトの取得に失敗しました。") 