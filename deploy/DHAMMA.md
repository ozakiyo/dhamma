# ダンマ指針アプリ — ConoHa（ozakiyo/dhamma）

## 役割

| 役割 | 場所 |
|------|------|
| 編集 | Cursor |
| 控え | GitHub `https://github.com/ozakiyo/dhamma.git` |
| 実行 | ConoHa `/opt/dhamma` + pm2 `dhamma` / ポート **3053** |

## 更新（日常）

GitHub に push したあと、サーバーで:

```bash
bash /opt/dhamma/deploy/pull-dhamma.sh
```

## 初回セットアップ

```bash
ssh root@160.251.173.118

# 旧構成を退避（必要なとき）
# mv /opt/dhamma /opt/dhamma.bak.$(date +%Y%m%d)

git clone https://github.com/ozakiyo/dhamma.git /opt/dhamma
pm2 start /opt/dhamma/deploy/ecosystem.dhamma.config.cjs
pm2 list    # dhamma のみ追加されたか確認（gsaxo / articleapp は触らない）
pm2 save
```

アクセス: http://160.251.173.118:3053/

## 隔離

- プロセス名は **`dhamma` のみ**
- `pm2 restart gsaxo` や articleapp は使わない
- 秘密情報はリポに載せない

## ローカル確認（任意）

```bash
DHAMMA_PORT=3053 node deploy/dhamma-serve.mjs
# http://localhost:3053/
```
