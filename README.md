# ダンマ指針アプリ（PWA）

リポジトリ: https://github.com/ozakiyo/dhamma.git

| 役割 | 場所 |
|------|------|
| 編集 | Cursor |
| 控え・履歴 | GitHub（このリポ） |
| 公開 | ConoHa `/opt/dhamma` + pm2 `dhamma`（ポート 3053） |

## 日常の流れ

1. Cursor で編集する  
2. `git commit` → `git push origin main`  
3. ConoHa で:

```bash
bash /opt/dhamma/deploy/pull-dhamma.sh
```

## ConoHa 初回

```bash
# 旧 /opt/dhamma がある場合は退避してから
# mv /opt/dhamma /opt/dhamma.bak.$(date +%Y%m%d)

git clone https://github.com/ozakiyo/dhamma.git /opt/dhamma
pm2 start /opt/dhamma/deploy/ecosystem.dhamma.config.cjs
pm2 save
```

詳細は `deploy/DHAMMA.md` を参照。
