#!/usr/bin/env bash
# GitHub main の内容を ConoHa /opt/dhamma へ反映する（Mac から実行）
set -euo pipefail

DEST="${1:-conoha}"
REMOTE_DIR="${2:-/opt/dhamma}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$REPO_ROOT"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: 未コミットの変更があります。先に commit と push をしてください。" >&2
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [[ "$BRANCH" != "main" ]]; then
  echo "ERROR: 現在のブランチは ${BRANCH} です。main から実行してください。" >&2
  exit 1
fi

git fetch origin main
if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
  echo "ERROR: ローカルと origin/main が一致しません。先に git push origin main を実行してください。" >&2
  exit 1
fi

echo "=== GitHub main → ${DEST}:${REMOTE_DIR} ==="
ssh "$DEST" "bash '${REMOTE_DIR}/deploy/pull-dhamma.sh' '${REMOTE_DIR}'"

echo ""
echo "本番確認:"
echo "  ssh ${DEST} \"curl -s -o /dev/null -w '%{http_code}\\n' http://127.0.0.1:3053/\""
