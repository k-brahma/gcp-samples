import json
import os
from pathlib import Path

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# .env ファイルのパスを明示的に指定
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'

def main():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] # スプレッドシートの操作なので drive.readonly は不要
    credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    gc = gspread.authorize(credentials)
    
    print("認証成功。スプレッドシートを開こうとしています...")
    
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    print(f"スプレッドシートのタイトル: {spreadsheet.title}")
    print("スプレッドシートへのアクセスに成功しました！")

    # 既存のシート名一覧を取得して表示
    print("\n既存のシート名:")
    worksheets = spreadsheet.worksheets()
    for worksheet in worksheets:
        print(f"- {worksheet.title}")

    # 削除するシート名を設定
    sheet_to_delete_name = "新しいシート" # ここで削除したいシート名を指定

    print(f"\nシート '{sheet_to_delete_name}' の削除を試みます...")
    try:
        worksheet_to_delete = spreadsheet.worksheet(sheet_to_delete_name)
        spreadsheet.del_worksheet(worksheet_to_delete)
        print(f"シート '{sheet_to_delete_name}' を削除しました。")
    except gspread.exceptions.WorksheetNotFound:
        print(f"シート '{sheet_to_delete_name}' は見つかりませんでした。")
    except Exception as e:
        print(f"シート '{sheet_to_delete_name}' の削除中にエラーが発生しました: {e}")

    # 最新のシート名一覧を取得して表示
    print("\n削除後のシート名:")
    worksheets = spreadsheet.worksheets()
    if worksheets:
        for worksheet in worksheets:
            print(f"- {worksheet.title}")
    else:
        print("シートはもうありません。")


if __name__ == '__main__':
    main() 