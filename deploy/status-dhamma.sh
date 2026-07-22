#!/usr/bin/env bash
# ダンマの状態を一言で確認
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== git ==="
git status -sb
git log -1 --oneline
echo ""
echo "=== pm2 dhamma ==="
pm2 describe dhamma 2>/dev/null | rg -i 'status|uptime|restarts|script path|pid ' || pm2 list | rg dhamma || true
echo ""
echo "=== http ==="
code="$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3053/sw.js || true)"
echo "sw.js → ${code}"
curl -s http://127.0.0.1:3053/sw.js 2>/dev/null | head -1 || true
