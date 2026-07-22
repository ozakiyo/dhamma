#!/usr/bin/env bash
# =============================================================================
# ConoHa 上で実行: GitHub (ozakiyo/dhamma) から取り込み → pm2 再起動
#
# 前提: /opt/dhamma が https://github.com/ozakiyo/dhamma.git の clone
#
# 使い方:
#   bash /opt/dhamma/deploy/pull-dhamma.sh
# =============================================================================
set -euo pipefail

REPO_ROOT="${1:-/opt/dhamma}"
BRANCH="${DHAMMA_BRANCH:-main}"
REMOTE_URL="${DHAMMA_REMOTE:-https://github.com/ozakiyo/dhamma.git}"

echo ""
echo "========================================"
echo " ダンマ ← GitHub (ozakiyo/dhamma)"
echo "========================================"
echo " 配置: ${REPO_ROOT}"
echo " 枝:   ${BRANCH}"
echo "========================================"
echo ""

if [[ ! -d "${REPO_ROOT}/.git" ]]; then
  echo "[0/3] clone が無いので初回 clone…"
  parent="$(dirname "$REPO_ROOT")"
  mkdir -p "$parent"
  if [[ -e "$REPO_ROOT" ]]; then
    echo "エラー: ${REPO_ROOT} はあるが .git がありません。退避してから再実行してください。" >&2
    exit 1
  fi
  git clone -b "$BRANCH" "$REMOTE_URL" "$REPO_ROOT"
else
  echo "[1/3] git pull…"
  cd "$REPO_ROOT"
  git fetch origin "$BRANCH"
  git checkout "$BRANCH"
  git pull --ff-only origin "$BRANCH"
  echo "      OK ($(git rev-parse --short HEAD))"
fi
echo ""

cd "$REPO_ROOT"
mkdir -p logs

echo "[2/3] pm2…"
if pm2 describe dhamma >/dev/null 2>&1; then
  pm2 restart dhamma && pm2 save
else
  pm2 start "${REPO_ROOT}/deploy/ecosystem.dhamma.config.cjs"
  pm2 save
fi
echo ""

echo "[3/3] 完了"
echo "  URL: http://160.251.173.118:3053/"
echo ""
