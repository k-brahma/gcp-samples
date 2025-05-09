"""Google Calendar API を操作するためのクライアントクラス

Google Calendar APIを使ってイベントの閲覧、作成、削除などの操作を行うためのクラスです。
環境変数`GOOGLE_CALENDAR_ID`から対象カレンダーIDを読み込み、各種操作を提供します。

使い方の例:

>>> from datetime import datetime
>>> from gcp07_google_calendar.gc05_calendar_class import GoogleCalendarClient
>>>
>>> # クライアントの初期化
>>> client = GoogleCalendarClient()
>>>
>>> # イベントの追加
>>> start_time = datetime(2025, 5, 10, 10, 0)
>>> end_time = datetime(2025, 5, 10, 11, 0)
>>> event = client.add_event("新しい予定", "詳細文章です", start_time, end_time)
イベントを作成しました: https://www.google.com/calendar/event?eid=...
>>>
>>> # イベント一覧の取得と表示
>>> events = client.list_events()
直近10件のイベントを取得します...
1. 2025-05-10T10:00:00+09:00 - 新しい予定 (ID: ka44cbcqdrr2lnp20l48o4r3o8)
>>>
>>> # イベントの削除
>>> client.delete_event("ka44cbcqdrr2lnp20l48o4r3o8")
イベント (ID: ka44cbcqdrr2lnp20l48o4r3o8) を削除しています...
イベントを削除しました。
True

前提条件:
1. credentials.json ファイルが配置されていること
2. .env ファイルに GOOGLE_CALENDAR_ID が設定されていること
"""
import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleCalendarClient:
    """Google Calendar API を操作するためのクライアントクラス"""

    def __init__(self):
        """初期化"""
        # 認証情報ファイルのパス
        self.credentials_file = Path(__file__).parent / 'credentials.json'

        # カレンダーIDの設定は環境変数から読み込み
        dotenv_path = Path(__file__).parent / '.env'
        load_dotenv(dotenv_path=dotenv_path)
        self.calendar_id = os.getenv('GOOGLE_CALENDAR_ID')

    def _get_service(self, readonly=False):
        """Google Calendar API サービスを取得

        :param readonly: 読み取り専用モードかどうか (True/False)
        :return: サービスオブジェクト。エラー発生時はNone
        """
        # スコープの設定（読み取り専用かどうかで切り替え）
        if readonly:
            scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        else:
            scopes = ['https://www.googleapis.com/auth/calendar']

        try:
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=scopes)
            service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
            return service
        except Exception as e:
            print(f"Google Calendar APIへの接続中にエラーが発生しました: {e}")
            return None

    def add_event(self, summary, description, start_datetime, end_datetime, timezone='Asia/Tokyo'):
        """イベントを追加

        :param summary: イベントの概要（タイトル）
        :param description: イベントの詳細な説明
        :param start_datetime: イベントの開始日時 (datetime.datetime)
        :param end_datetime: イベントの終了日時 (datetime.datetime)
        :param timezone: タイムゾーン (デフォルト: 'Asia/Tokyo')
        :return: 作成されたイベント情報。失敗した場合はNone
        """
        if not self.calendar_id:
            print("エラー: カレンダーIDが設定されていません。")
            return None

        service = self._get_service()
        if not service:
            return None

        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': timezone,
            },
        }

        try:
            created_event = service.events().insert(calendarId=self.calendar_id, body=event).execute()
            print(f"イベントを作成しました: {created_event.get('htmlLink')}")
            return created_event
        except Exception as e:
            print(f"イベントの作成中にエラーが発生しました: {e}")
            return None

    def list_events(self, max_results=10):
        """イベント一覧を取得・表示

        :param max_results: 取得するイベントの最大数（デフォルト: 10）
        :return: イベントのリスト。失敗した場合はNone
        """
        if not self.calendar_id:
            print("エラー: カレンダーIDが設定されていません。")
            return None

        service = self._get_service(readonly=True)
        if not service:
            return None

        # 現在時刻の取得 (ISO形式)
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        try:
            print(f'直近{max_results}件のイベントを取得します...')
            events_result = service.events().list(
                calendarId=self.calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            if not events:
                print('イベントは見つかりませんでした。')
            else:
                for i, event in enumerate(events, 1):
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    event_id = event['id']
                    print(f'{i}. {start} - {event["summary"]} (ID: {event_id})')

            return events
        except Exception as e:
            print(f"イベントの取得中にエラーが発生しました: {e}")
            return None

    def delete_event(self, event_id):
        """イベントを削除

        :param event_id: 削除するイベントのID
        :return: 削除成功時はTrue、失敗時はFalse
        """
        if not self.calendar_id:
            print("エラー: カレンダーIDが設定されていません。")
            return False

        service = self._get_service()
        if not service:
            return False

        try:
            print(f"イベント (ID: {event_id}) を削除しています...")
            service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            print(f"イベントを削除しました。")
            return True
        except Exception as e:
            print(f"イベントの削除中にエラーが発生しました: {e}")
            return False

    def delete_first_event(self):
        """最初のイベントを削除する便利メソッド

        直近のイベントを取得し、そのうち最初のものを削除します。
        :return: 削除成功時はTrue、失敗時はFalse
        """
        events = self.list_events(max_results=5)
        if not events:
            print("削除対象となるイベントがありません。")
            return False

        # 最初のイベントを削除
        first_event = events[0]
        event_id = first_event['id']
        event_summary = first_event['summary']
        print(f"\n削除対象: {event_summary} (ID: {event_id})")

        return self.delete_event(event_id)
