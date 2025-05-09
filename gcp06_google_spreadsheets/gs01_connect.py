import json
import os  # osモジュールをインポート
from pathlib import Path

import gspread
from dotenv import load_dotenv  # dotenvをインポート
from google.oauth2.service_account import Credentials

# .env ファイルのパスを明示的に指定
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path) # .envファイルから環境変数を読み込む

# スプレッドシートIDと認証情報ファイルへのパスを指定
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID') # 環境変数からSPREADSHEET_IDを取得
CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'

def main():
    if not SPREADSHEET_ID:
        print("エラー: .envファイルからSPREADSHEET_IDが読み込めませんでした。")
        print(".envファイルが正しく配置され、SPREADSHEET_IDが設定されているか確認してください。")
        return
    try:
        # 認証情報ファイルの内容を確認（メールアドレスを表示）
        with open(CREDENTIALS_FILE) as f:
            creds_data = json.load(f)
            print(f"サービスアカウントのメールアドレス: {creds_data.get('client_email')}")
        
        # 明示的にスコープを指定して認証情報をロード
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly'] # 読み取り専用スコープに変更
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(credentials)
        
        print("認証成功。スプレッドシートを開こうとしています...")
        
        try:
            # スプレッドシートを開く
            spreadsheet = gc.open_by_key(SPREADSHEET_ID)
            print(f"スプレッドシートのタイトル: {spreadsheet.title}")
            print("スプレッドシートへのアクセスに成功しました！")
        except gspread.exceptions.APIError as e:
            print(f"API エラー: {e}")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"スプレッドシートが見つかりません: {SPREADSHEET_ID}")
        
    except Exception as e:
        print(f"エラーが発生しました: {type(e).__name__}: {e}")
        print("スプレッドシートへのアクセスに失敗しました。")
        print("以下を確認してください:")
        print(f"- {CREDENTIALS_FILE} が正しいパスに存在するか")
        print("- サービスアカウントにスプレッドシートへのアクセス権が付与されているか")
        print("- スプレッドシートIDが正しいか")

if __name__ == '__main__':
    main() 