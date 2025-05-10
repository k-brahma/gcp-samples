# Google Spreadsheets の利用

## 事前準備

1. Google Cloud Console にログイン
2. プロジェクトを選択 or 新規プロジェクトを作成

## Google Sheets API を有効にする

1. APIとサービス
2. 有効なAPIとサービス
3. APIとサービスを有効にする
4. Google Sheets API を有効にする

## サービスアカウントを作り権限を付与する

### サービスアカウントを作る

1. APIとサービス
4. 認証情報
5. 認証情報を作成
6. サービスアカウント
7. サービスアカウントの詳細 -> 作成して続行
8. Grant this service account access to project (省略可) -> 何も入れない
9. Grant users access to this service account (省略可) -> 何も入れない
10. 完了

## 鍵を生成``

1. APIとサービス
2. 認証情報
3. 生成したサービスアカウントをクリック
4. 鍵タブへ
5. キーを追加 -> 新しい鍵を作成 -> JSON
6. credentials ディリクトリに保存する

## Google Spreadsheet 側での許可

gcp-demo-account@gcp-demos-456516.iam.gserviceaccount.com

なら

gcp-demo-account@gcp-demos-456516.iam.gserviceaccount.com

という具合に共有するアカウントを追加

## SCOPES の種類

| スコープ                                                     | 説明                                                                                                |
| :----------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| `https://www.googleapis.com/auth/spreadsheets`               | Google スプレッドシートのすべてのスプレッドシートの表示、編集、作成、削除を許可します。                               |
| `https://www.googleapis.com/auth/spreadsheets.readonly`      | Google スプレッドシートのすべてのスプレッドシートの表示を許可しますが、編集は許可しません。                               |
| `https://www.googleapis.com/auth/drive`                      | Google Drive 内のすべてのファイルの表示、編集、作成、削除を許可します。 (スプレッドシートも Drive ファイルの一種です) |
| `https://www.googleapis.com/auth/drive.file`                 | このアプリで使用する特定の Google Drive ファイルの表示、編集、作成、削除のみを許可します。                           |
| `https://www.googleapis.com/auth/drive.readonly`             | Google Drive 内のすべてのファイルの表示とダウンロードを許可しますが、編集は許可しません。                               |

## トラブルシューティング

| エラータイプ | 原因 | 対処法 |
|:-------------|:-----|:-------|
| **PermissionError** | サービスアカウントにスプレッドシートへのアクセス権がない | 正しいサービスアカウントのメールアドレス（credentials.jsonの`client_email`値）がスプレッドシートと共有されているか確認する |
| **API制限エラー** | Google API の利用制限（クォータ）に達した | Google Cloud Consoleで「APIとサービス」→「クォータ」から制限の確認と必要に応じて引き上げ申請を行う |
| **認証エラー** | 認証情報ファイルの問題 | credentials.jsonの内容が有効か、指定したファイルパスが正しいか確認する。必要に応じて新しい鍵を生成する |
| **スプレッドシートIDエラー** | スプレッドシートIDが不正 | スプレッドシートのURL（`https://docs.google.com/spreadsheets/d/[スプレッドシートID]/edit`）から正しいIDを抽出しているか確認する |
| **APIが有効化されていないエラー** | Google Sheets APIが有効になっていない | Google Cloud Consoleで「APIとサービス」→「ライブラリ」から「Google Sheets API」を有効化する |
| **スコープエラー** | 不十分なAPIスコープ | コードで指定しているスコープが適切か確認する。読み取りだけでなく書き込みも行う場合は `https://www.googleapis.com/auth/spreadsheets` を使用する |
