# ダンマ指針アプリ — ConoHa（ozakiyo/dhamma）

## 役割

| 役割 | 場所 |
|------|------|
| 編集 | Cursor（SSH で ConoHa の `/opt/dhamma`） |
| 控え | GitHub `https://github.com/ozakiyo/dhamma.git` |
| 実行 | ConoHa `/opt/dhamma` + pm2 `dhamma` / ポート **3053** |

公開: http://160.251.173.118:3053/

---

## 毎回の開き方（ローカルPC → Cursor）

初回だけローカルの `~/.ssh/config` に別名を追加（例は `deploy/ssh-config.example`）:

```
Host conoha-dhamma
  HostName 160.251.173.118
  User root
```

そのあと毎回:

1. Cursor を開く  
2. `F1`（または Cmd/Ctrl+Shift+P）→ **Remote-SSH: Connect to Host…**  
3. **`conoha-dhamma`** を選ぶ  
4. フォルダ **`/opt/dhamma`** を開く  

2回目以降は Cursor 左下のリモート表示や **Recent** から同じ接続を選べます。

---

## コマンド早見表（サーバー上 `/opt/dhamma`）

編集はすでにサーバー上なので、**push 後に pull は不要**です。

| やりたいこと | コマンド |
|--------------|----------|
| 状態確認 | `bash deploy/status-dhamma.sh` |
| 反映（再起動） | `bash deploy/restart-dhamma.sh` |
| 変更を控える | `git add …` → `git commit -m "…"` → `git push origin main` |
| 本番URL確認 | ブラウザで `:3053` / 古い画面ならスーパーリロード |

### 編集〜公開の最短流れ

```bash
cd /opt/dhamma
# （Cursor で編集）
git status
git add -A
git commit -m "メッセージ"
git push origin main
bash deploy/restart-dhamma.sh
```

### 別マシンで push したあと、サーバーだけ取り込む場合

```bash
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

## ローカル確認（任意）

```bash
DHAMMA_PORT=3053 node deploy/dhamma-serve.mjs
# http://localhost:3053/
```
