#!/usr/bin/env bash
# 編集反映用: pm2 restart + save + 簡易確認
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/2] pm2 restart dhamma…"
pm2 restart dhamma
pm2 save
echo "[2/2] check…"
sleep 1
code="$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3053/sw.js)"
echo "sw.js → ${code}"
curl -s http://127.0.0.1:3053/sw.js | head -1
pm2 describe dhamma | rg -i 'status|uptime' || true
echo "OK — ブラウザはスーパーリロード推奨"
