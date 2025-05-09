import os
from pathlib import Path

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'


def check_sheet_names_and_write():
    # 明示的にスコープを指定して認証情報をロード
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.readonly']
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    gc = gspread.authorize(credentials)

    print("認証成功。スプレッドシートを開こうとしています...")

    # スプレッドシートを開く
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    print(f"スプレッドシートのタイトル: {spreadsheet.title}")
    print("スプレッドシートへのアクセスに成功しました！")

    # 既存のシート名一覧を取得して表示
    print("\n既存のシート名:")
    worksheets = spreadsheet.worksheets()
    for worksheet in worksheets:
        print(f"- {worksheet.title}")

    # データ書き込み先シートのシート名を決定
    target_sheet_name = "新しいシート"

    # データ書き込み先シートと同名のシートが存在しないか確認
    if any(ws.title == target_sheet_name for ws in worksheets):
        print(f"\nシート '{target_sheet_name}' は既に存在します。")
        # 既存のシートを取得
        target_worksheet = spreadsheet.worksheet(target_sheet_name)
    else:
        # 新しいシートを作成
        print(f"\nシート '{target_sheet_name}' を作成します...")
        target_worksheet = spreadsheet.add_worksheet(title=target_sheet_name, rows=100, cols=20)
        print(f"シート '{target_sheet_name}' を作成しました。")

    # 作成したシートにデータを書き込む
    print(f"\nシート '{target_sheet_name}' にデータを書き込みます...")
    data_to_write = [
        ["名前", "年齢", "都市"],
        ["山田太郎", "30", "東京"],
        ["佐藤花子", "25", "大阪"],
        ["鈴木一郎", "40", "名古屋"]
    ]
    target_worksheet.update('A1', data_to_write)
    print("データの書き込みが完了しました。")


if __name__ == '__main__':
    check_sheet_names_and_write()
