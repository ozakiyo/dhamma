# ダンマ指針アプリ（PWA）

リポジトリ: https://github.com/ozakiyo/dhamma.git

| 役割 | 場所 |
|------|------|
| 編集・確認 | Mac `~/work/apps/dhamma` + Docker |
| 正本・履歴 | GitHub（このリポ） |
| 公開 | ConoHa + pm2 `dhamma`（ポート 3053） |

## ローカル開発（Docker・ライブ編集）

Docker Desktop を起動してから:

```bash
cd ~/work/apps/dhamma
docker compose up -d --build
```

ブラウザ: http://localhost:3053/

リポジトリ全体をコンテナの `/app` にマウントしているため、ローカルで保存した内容は即時反映されます。静的ファイルはリクエストごとに読み直すため、コード変更時のコンテナ再起動は不要です。表示が古い場合は PWA キャッシュの影響があるため、スーパーリロードしてください。

## GitHub → ConoHa

ローカルで動作確認後:

```bash
cd ~/work/apps/dhamma
git add -A
git commit -m "変更内容"
git push origin main
bash deploy/deploy-to-conoha.sh
```

`deploy-to-conoha.sh` は、未コミット変更がなくローカルと `origin/main` が一致することを確認してから、ConoHa の `/opt/dhamma` で pull と pm2 再起動を行います。

詳細・早見表: [`deploy/DHAMMA.md`](deploy/DHAMMA.md)
