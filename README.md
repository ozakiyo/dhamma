# ダンマ指針アプリ（PWA）

リポジトリ: https://github.com/ozakiyo/dhamma.git

| 役割 | 場所 |
|------|------|
| 編集 | Cursor（SSH → ConoHa `/opt/dhamma`） |
| 控え・履歴 | GitHub（このリポ） |
| 公開 | ConoHa + pm2 `dhamma`（ポート 3053） |

## 毎回の開き方

1. Cursor → **Remote-SSH: Connect to Host…** → `conoha-dhamma`  
2. フォルダ `/opt/dhamma` を開く  

SSH 別名の例: `deploy/ssh-config.example`

## 日常の流れ（サーバー上で編集する場合）

```bash
cd /opt/dhamma
# 編集 → commit → push
git push origin main
bash deploy/restart-dhamma.sh
```

状態確認: `bash deploy/status-dhamma.sh`

詳細・早見表: [`deploy/DHAMMA.md`](deploy/DHAMMA.md)
