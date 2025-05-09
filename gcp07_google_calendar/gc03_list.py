import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def list_events(calendar_id, max_results=10):
    """指定されたカレンダーのイベントを一覧表示します。

    接続処理を内部で行い、カレンダーIDと取得件数のみを引数として受け取ります。

    :param calendar_id: イベントを取得するカレンダーのID
    :param max_results: 取得するイベントの最大数（デフォルト: 10）
    :return: 取得したイベントのリスト。失敗した場合はNone
    """
    # 接続処理を内部で行う
    CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']  # 読み取り専用スコープ

    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        service = build('calendar', 'v3', credentials=creds, cache_discovery=False)
        print("Google Calendar APIへの接続に成功しました。")
    except FileNotFoundError:
        print(f"エラー: 認証情報ファイルが見つかりません: {CREDENTIALS_FILE}")
        return None
    except Exception as e:
        print(f"Google Calendar APIへの接続中にエラーが発生しました: {e}")
        return None

    # 現在時刻の取得 (ISO形式)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()

    print(f'直近{max_results}件のイベントを取得します...')
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print('イベントは見つかりませんでした。')
    else:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_id = event['id']
            print(f'{start} - {event["summary"]}')

    return events


if __name__ == "__main__":
    # 環境変数の読み込み
    dotenv_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=dotenv_path)
    CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')

    if not CALENDAR_ID:
        print("エラー: 環境変数 GOOGLE_CALENDAR_ID が設定されていません。")
        print(".env ファイルに GOOGLE_CALENDAR_ID=your_calendar_id_here のように設定してください。")
        exit(1)

    print(f"対象カレンダーID: {CALENDAR_ID}")

    # イベント一覧の取得と表示
    list_events(CALENDAR_ID)
