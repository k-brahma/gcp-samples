'''
Google Calendar API を使用してカレンダーから特定の既存イベントを削除するサンプルモジュール。

このモジュールは、カレンダーから既存のイベントを取得し、
その中から1つのイベントを削除する機能を提供します。

メインスクリプトとして実行する場合、
カレンダーから直近のイベントをいくつかリスト表示し、そのうちの最初のイベントを削除します。

主な機能:
  - :py:func:`list_upcoming_events`: 直近のイベントを取得し、イベントIDと共に表示します。
  - :py:func:`delete_event`: 指定されたカレンダーの特定のイベントを削除します。

設定:
  - ``CALENDAR_ID``: 環境変数 ``GOOGLE_CALENDAR_ID`` から取得。
  - ``.env`` ファイル: ``GOOGLE_CALENDAR_ID=your_calendar_id_here`` のように記述。

使用方法 (メインスクリプトとして実行する場合):
  1. 認証設定 (``credentials.json`` の配置) を行います。
  2. 必要に応じて ``.env`` ファイルで ``GOOGLE_CALENDAR_ID`` を設定します。
  3. このスクリプトを実行すると、設定されたカレンダーの直近のイベントがリスト表示され、
     リストの最初のイベントが削除されます。
'''

import datetime
import os

# import time # time.sleep は不要になったためコメントアウトまたは削除
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')
SCOPES = ['https://www.googleapis.com/auth/calendar'] # Listing and Deleting events requires write access

def connect_to_calendar():
    '''Google Calendar API への接続と認証を行う。'''
    try:
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES
        )
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
        print("Google Calendar APIへの接続に成功しました。")
        return service
    except FileNotFoundError:
        print(f"エラー: 認証情報ファイルが見つかりません: {CREDENTIALS_FILE}")
        return None
    except Exception as e:
        print(f"Google Calendar APIへの接続中にエラーが発生しました: {e}")
        return None

def list_upcoming_events(service, calendar_id, max_results=5):
    """直近のイベントを取得し、サマリーとイベントIDを含むリストを返します。"""
    try:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(f"直近{max_results}件のイベントを取得・表示します...")
        events_result = service.events().list(
            calendarId=calendar_id, timeMin=now,
            maxResults=max_results, singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('表示できる今後のイベントは見つかりませんでした。削除対象がありません。')
            return []
        
        print("削除対象となる可能性のあるイベント:")
        event_details = []
        for i, event in enumerate(events):
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_id = event['id']
            summary = event['summary']
            print(f"  {i+1}. Start: {start}, Summary: {summary}, ID: {event_id}")
            event_details.append({'id': event_id, 'summary': summary, 'start': start})
        return event_details

    except Exception as e:
        print(f"イベントの取得中にエラーが発生しました: {e}")
        return []

def delete_event(service, calendar_id, event_id, event_summary):
    """指定されたカレンダーの特定のイベントを削除します。"""
    try:
        print(f"イベント「{event_summary}」(ID: {event_id}) を削除しています...")
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        print(f"イベント「{event_summary}」(ID: {event_id}) を削除しました。")
        return True
    except Exception as e:
        print(f"イベント ID: {event_id} の削除中にエラーが発生しました: {e}")
        return False


if __name__ == "__main__":
    if not CALENDAR_ID:
        print("エラー: 環境変数 GOOGLE_CALENDAR_ID が設定されていません。")
    else:
        print(f"対象カレンダーID: {CALENDAR_ID}")
        service = connect_to_calendar()
        if service:
            print("既存イベントの削除処理を開始します。")
            
            # 1. 既存のイベントを取得
            upcoming_events = list_upcoming_events(service, CALENDAR_ID, max_results=5)

            if upcoming_events:
                # 2. 取得したイベントの最初のものを削除対象とする
                event_to_delete = upcoming_events[0]
                event_id_to_delete = event_to_delete['id']
                event_summary_to_delete = event_to_delete['summary']
                
                print(f"--- 削除対象イベント --- ")
                print(f"  Summary: {event_summary_to_delete}")
                print(f"  ID: {event_id_to_delete}")
                print(f"-----------------------")
                
                # ユーザーに確認を取る場合はここに追加できますが、今回は自動で削除します。
                # confirm = input(f"イベント「{event_summary_to_delete}」を本当に削除しますか？ (yes/no): ")
                # if confirm.lower() == 'yes':
                #     delete_event(service, CALENDAR_ID, event_id_to_delete, event_summary_to_delete)
                # else:
                #     print("削除をキャンセルしました。")
                delete_event(service, CALENDAR_ID, event_id_to_delete, event_summary_to_delete)
            else:
                print("削除対象となるイベントが見つかりませんでした。")
            
            print("既存イベントの削除処理を終了します。") 