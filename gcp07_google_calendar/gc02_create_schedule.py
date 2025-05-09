import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def add_event_to_calendar(calendar_id, summary, description, start_time, end_time, timezone='Asia/Tokyo'):
    """指定されたカレンダーに新しいイベントを追加します。

    接続処理を内部で行い、カレンダーIDや概要などの必要情報のみを引数として受け取ります。
    """
    # 接続処理を内部で行う
    CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
    except Exception as e:
        print(f"Google Calendar APIへの接続中にエラーが発生しました: {e}")
        return None

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

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"イベントを作成しました: {created_event.get('htmlLink')}")
    return created_event


if __name__ == "__main__":
    dotenv_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=dotenv_path)
    CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')

    if not CALENDAR_ID:
        print("エラー: 環境変数 GOOGLE_CALENDAR_ID が設定されていません。")
        print(".env ファイルに GOOGLE_CALENDAR_ID=your_calendar_id_here のように設定するか、")
        print("スクリプト内で直接 CALENDAR_ID を設定してください。")
        exit(1)

    print(f"対象カレンダーID: {CALENDAR_ID}")

    # デモイベントの作成
    summary = "自動追加テストイベント"
    description = "これは gc02_create_and_list.py によって自動的に追加されたテストイベントです。"

    # 現在時刻から1時間後を開始時刻とし、さらに1時間後を終了時刻とする
    start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    end_time = start_time + datetime.timedelta(hours=1)

    add_event_to_calendar(CALENDAR_ID, summary, description, start_time, end_time)
