#!/usr/bin/env bash
set -euo pipefail
set -x

export GIT_TERMINAL_PROMPT=0

# Autentica o GH CLI sem prompt
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  echo "$GITHUB_TOKEN" | gh auth login --with-token --hostname github.com --git-protocol https
  git config --global credential.helper "!gh auth git-credential"
fi

# Cria ou corrige o origin
if [[ -z "${REMOTE_URL:-}" ]]; then
  echo "❌ REMOTE_URL não definido" >&2
  exit 1
fi
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE_URL"

# Push upstream do branch atual
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if ! git rev-parse --verify "origin/$CURRENT_BRANCH" >/dev/null 2>&1; then
  git push -u origin "$CURRENT_BRANCH"
fi
