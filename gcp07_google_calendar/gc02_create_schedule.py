'''
Google Calendar API を使用してカレンダーにイベントを追加するサンプルモジュール。

このモジュールは、:py:mod:`gc01_connect` モジュールを使用してGoogle Calendar APIに接続し、
主に指定されたカレンダーID (このファイル内で環境変数 ``GOOGLE_CALENDAR_ID`` から取得) のカレンダーに
新しいイベントを追加する機能を提供します。
また、新しいカレンダーを作成するユーティリティ関数も提供します。

主な機能:
  - :py:func:`create_calendar`: 新しいGoogleカレンダーを作成します。
  - :py:func:`add_event_to_calendar`: 指定されたカレンダーに新しいイベントを追加します。

設定:
  - ``CALENDAR_ID``: このファイル内で、環境変数 ``GOOGLE_CALENDAR_ID`` またはデフォルト値により、
    操作対象のGoogle Calendar IDを設定します。
  - ``.env`` ファイル: スクリプトと同じディレクトリに ``.env`` ファイルを配置し、
    ``GOOGLE_CALENDAR_ID=your_calendar_id_here`` のように記述することで、対象カレンダーIDを指定できます。

使用方法 (メインスクリプトとして実行する場合):
  1. :py:mod:`gc01_connect` の認証設定 (``credentials.json`` の配置) を行います。
  2. 必要に応じて ``.env`` ファイルで ``GOOGLE_CALENDAR_ID`` を設定します。
  3. このスクリプトを実行すると、設定されたカレンダーにテストイベントが追加されます。

必要なライブラリ:
  - datetime (イベントの日時指定のため)
  - python-dotenv (``.env`` ファイル読み込みのため)
  - gc01_connect (API接続のため)
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


def add_event_to_calendar(service, calendar_id, summary, description, start_time, end_time, timezone='Asia/Tokyo'):
    """指定されたカレンダーに新しいイベントを追加します。

    :param service: 認証済みのCalendar APIサービスオブジェクト。
    :type service: googleapiclient.discovery.Resource
    :param calendar_id: イベントを追加するカレンダーのID。
    :type calendar_id: str
    :param summary: イベントの概要（タイトル）。
    :type summary: str
    :param description: イベントの詳細な説明。
    :type description: str
    :param start_time: イベントの開始日時。
    :type start_time: datetime.datetime
    :param end_time: イベントの終了日時。
    :type end_time: datetime.datetime
    :param timezone: イベントのタイムゾーン。デフォルトは 'Asia/Tokyo'。
    :type timezone: str
    :returns: 作成されたイベントの情報。
              イベントの作成に失敗した場合は None。
    :rtype: dict or None
    """
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': timezone,
        },
    }
    try:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"イベントを作成しました: {created_event.get('htmlLink')}")
        return created_event
    except Exception as e:
        print(f"イベントの作成中にエラーが発生しました: {e}")
        return None
    

if __name__ == "__main__":
    if not CALENDAR_ID:
        print("エラー: 環境変数 GOOGLE_CALENDAR_ID が設定されていません。")
        print(".env ファイルに GOOGLE_CALENDAR_ID=your_calendar_id_here のように設定するか、")
        print("スクリプト内で直接 CALENDAR_ID を設定してください。")
    else:
        print(f"対象カレンダーID: {CALENDAR_ID}")
        service = connect_to_calendar()
        if service:
            # デモイベントの作成
            summary = "自動追加テストイベント"
            description = "これは gc02_create_and_list.py によって自動的に追加されたテストイベントです。"
            # 現在時刻から1時間後を開始時刻とし、さらに1時間後を終了時刻とする
            start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            end_time = start_time + datetime.timedelta(hours=1)

            add_event_to_calendar(service, CALENDAR_ID, summary, description, start_time, end_time)

