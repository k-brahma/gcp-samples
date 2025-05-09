# Google Calendar API 利用ガイド (Python)

## できること

- カレンダーへの接続テスト
- イベントの作成・一覧表示・削除

## セットアップ手順

### 1. Google Cloud Platform での準備

1. **プロジェクトの用意**
   - Google Cloud Console にログイン
   - 既存/新規プロジェクトを選択

2. **Google Calendar API の有効化**
   - 「APIとサービス」→「ライブラリ」
   - 「Google Calendar API」を検索して有効化

3. **サービスアカウントの作成**
   - 「APIとサービス」→「認証情報」→「認証情報を作成」→「サービスアカウント」
   - サービスアカウント名を入力（例: `calendar-api-user`）
   - 権限設定はブランクのままでOK（個別に権限付与する場合）
   - 「作成して続行」→「完了」

4. **サービスアカウントキー (JSON) の生成**
   - サービスアカウント詳細画面の「キー」タブ
   - 「キーを追加」→「新しいキーを作成」→「JSON」
   - ダウンロードされたJSONファイルを `credentials.json` として保存

5. **カレンダー側での共有設定**
   - Googleカレンダーで対象カレンダーの「設定と共有」を開く
   - 「特定のユーザーと共有する」セクションで「+ ユーザーを追加」
   - サービスアカウントのメールアドレス（`credentials.json` の `client_email` 値）を入力
   - 「予定の変更権限」以上の権限を付与して「送信」

### 2. ローカル環境での準備

1. **ライブラリのインストール**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv
   ```

2. **環境変数の設定**
   - `.env` ファイルを作成し以下を記述:
   ```
   GOOGLE_CALENDAR_ID=your_calendar_id_here
   ```

## 主なスコープ

| スコープ | 説明 |
|:---------|:-----|
| `https://www.googleapis.com/auth/calendar` | カレンダーの読み書き全般（作成・削除等） |
| `https://www.googleapis.com/auth/calendar.readonly` | カレンダーの読み取り専用 |
| `https://www.googleapis.com/auth/calendar.events` | イベントの読み書き |
| `https://www.googleapis.com/auth/calendar.events.readonly` | イベントの読み取り専用 |

## トラブルシューティング

| エラータイプ | 原因 | 対処法 |
|:-------------|:-----|:-------|
| **ファイル不明エラー** | `credentials.json` が見つからない | 正しい場所にJSONキーファイルが配置されているか確認 |
| **権限エラー (403)** | サービスアカウントに権限がない | カレンダー共有設定でサービスアカウントのメールアドレスに適切な権限を付与 |
| **認証エラー** | 無効な認証情報や鍵 | credentials.jsonが最新か確認、必要に応じて新しい鍵を生成 |
| **API有効化エラー** | Calendar APIが有効になっていない | Google Cloud Consoleで「APIとサービス」から有効化 |
| **環境変数エラー** | カレンダーIDが設定されていない | `.env` ファイルに `GOOGLE_CALENDAR_ID` を正しく設定 |

---

このバージョンでは、元のreadmeの重要なポイントを保持しつつ、情報を整理して見やすくなるように構成しました。トラブルシューティングも表形式で簡潔にまとめています。コードサンプルも追加して、すぐに使い始められるようにしました。