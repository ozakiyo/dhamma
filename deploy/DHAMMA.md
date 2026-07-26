# ダンマ指針アプリ — ConoHa（ozakiyo/dhamma）

## 役割

| 役割 | 場所 |
|------|------|
| 編集・確認 | Mac `~/work/apps/dhamma` + Docker |
| 正本・履歴 | GitHub `https://github.com/ozakiyo/dhamma.git` |
| 実行 | ConoHa `/opt/dhamma` + pm2 `dhamma` / ポート **3053** |

公開: http://160.251.173.118:3053/

---

## ローカル開発

```bash
cd ~/work/apps/dhamma
docker compose up -d --build
# http://localhost:3053/
```

ローカル全体をコンテナへマウントしているため、保存したファイルは即時反映されます。

---

## コマンド早見表

| やりたいこと | コマンド |
|--------------|----------|
| ローカル起動 | `docker compose up -d` |
| ローカル停止 | `docker compose down` |
| 本番状態確認 | `ssh conoha 'bash /opt/dhamma/deploy/status-dhamma.sh'` |
| GitHubから本番へ反映 | `bash deploy/deploy-to-conoha.sh` |
| 本番URL確認 | ブラウザで `:3053` / 古い画面ならスーパーリロード |

### 編集〜公開の流れ

```bash
cd ~/work/apps/dhamma
# Cursor で編集 → http://localhost:3053/ で確認
git status
git add -A
git commit -m "メッセージ"
git push origin main
bash deploy/deploy-to-conoha.sh
```

### サーバー上で手動反映する場合

```bash
ssh conoha
bash /opt/dhamma/deploy/pull-dhamma.sh
```

---

## 隔離

- プロセス名は **`dhamma` のみ**
- `pm2 restart gsaxo` や articleapp は使わない
- 秘密情報はリポに載せない

## 初回セットアップ（サーバー）

```bash
ssh root@160.251.173.118
# 旧構成を退避（必要なとき）
# mv /opt/dhamma /opt/dhamma.bak.$(date +%Y%m%d)
git clone https://github.com/ozakiyo/dhamma.git /opt/dhamma
pm2 start /opt/dhamma/deploy/ecosystem.dhamma.config.cjs
pm2 list    # dhamma のみ追加されたか確認
pm2 save
```

## Dockerを使わないローカル確認

```bash
DHAMMA_PORT=3053 node deploy/dhamma-serve.mjs
# http://localhost:3053/
```
