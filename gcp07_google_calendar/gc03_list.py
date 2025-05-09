'''
Google Calendar API を使用してカレンダーのイベントを一覧表示するサンプルモジュール。

このモジュールは、:py:mod:`gc01_connect` モジュールを使用してGoogle Calendar APIに接続し、
指定されたカレンダーID (このファイル内で環境変数 ``GOOGLE_CALENDAR_ID`` から取得) のカレンダーから
イベントの一覧を取得して表示する機能を提供します。

主な機能:
  - :py:func:`list_events`: 指定されたカレンダーのイベントを一覧表示します。

設定:
  - ``CALENDAR_ID``: このファイル内で、環境変数 ``GOOGLE_CALENDAR_ID`` またはデフォルト値により、
    操作対象のGoogle Calendar IDを設定します。
  - ``.env`` ファイル: スクリプトと同じディレクトリに ``.env`` ファイルを配置し、
    ``GOOGLE_CALENDAR_ID=your_calendar_id_here`` のように記述することで、対象カレンダーIDを指定できます。

使用方法 (メインスクリプトとして実行する場合):
  1. :py:mod:`gc01_connect` の認証設定 (``credentials.json`` の配置) を行います。
  2. 必要に応じて ``.env`` ファイルで ``GOOGLE_CALENDAR_ID`` を設定します。
  3. このスクリプトを実行すると、設定されたカレンダーのイベントが一覧表示されます。

必要なライブラリ:
  - datetime
  - python-dotenv
  - google-api-python-client
  - google-auth-httplib2
  - google-auth-oauthlib
  - os, pathlib
'''

import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']  # Readonly scope for listing events


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


def list_events(service, calendar_id, max_results=10):
    """指定されたカレンダーのイベントを一覧表示します。

    :param service: 認証済みのCalendar APIサービスオブジェクト。
    :type service: googleapiclient.discovery.Resource
    :param calendar_id: イベントを取得するカレンダーのID。
    :type calendar_id: str
    :param max_results: 取得するイベントの最大数。デフォルトは10。
    :type max_results: int
    :returns: なし
    """
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print(f'直近{max_results}件のイベントを取得します...')
        events_result = service.events().list(
            calendarId=calendar_id, timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('イベントは見つかりませんでした。')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_id = event['id']
            print(f'{start} - {event_id} - {event["summary"]}')  # Use double quotes for summary key

    except Exception as e:
        print(f"イベントの取得中にエラーが発生しました: {e}")


if __name__ == "__main__":
    if not CALENDAR_ID:
        print("エラー: 環境変数 GOOGLE_CALENDAR_ID が設定されていません。")
        print(".env ファイルに GOOGLE_CALENDAR_ID=your_calendar_id_here のように設定するか、")
        print("スクリプト内で直接 CALENDAR_ID を設定してください。")
    else:
        print(f"対象カレンダーID: {CALENDAR_ID}")
        service = connect_to_calendar()
        if service:
            list_events(service, CALENDAR_ID)
