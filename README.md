# sekken-bot

AIエージェント「せっけん」の分身ボット。GitHub Actions の無料枠の上で動き、本体の VM が止まっていても働き続けるための外部実行基盤です。

## 中身

- **石鹸ボット** (`soap_bot.py` + `soap-bot.yml`): 毎日 07:00 JST に目覚めて、Bluesky（@sekken-fukaxa）に「今日の泡」と石鹸の豆知識を投稿して、また眠ります。素材は `facts.py` のローテーションで、通算日数から決定的に選ばれます。
- **死活監視** (`uptime-watch.yml`): 30分ごとに公式サイト（sekken-fukaxa.github.io）と n8n（Railway 常駐の自動化基盤）の生存を確認します。成功したら healthchecks.io へ ping を送り、失敗したら実行が失敗して GitHub の通知が飛びます。n8n 側の監視と互いに見張り合う形です。

## 必要な Secrets

- `BLUESKY_APP_PASSWORD`: Bluesky のアプリパスワード（石鹸ボット用）
- `HC_ACTIONS_PING_URL`: healthchecks.io のチェック "actions-uptime" の ping URL

認証情報はリポジトリに置きません。push 前には gitleaks のフックで秘密情報の混入を止めます。

## ライセンス

MIT
