#!/usr/bin/env bash
set -euo pipefail

branch="${1:-main}"
max_attempts="${2:-5}"

if ! [[ "$max_attempts" =~ ^[1-9][0-9]*$ ]]; then
  echo "::error::max_attempts must be a positive integer"
  exit 2
fi

for ((attempt=1; attempt<=max_attempts; attempt++)); do
  echo "Push attempt $attempt/$max_attempts for $branch"
  git fetch origin "$branch"

  if ! git rebase "origin/$branch"; then
    echo "::error::Rebase conflict while reconciling writer output with origin/$branch"
    git status --short || true
    git rebase --abort || true
    exit 3
  fi

  if git push origin "HEAD:$branch"; then
    echo "Push succeeded on attempt $attempt."
    exit 0
  fi

  if (( attempt < max_attempts )); then
    sleep_seconds=$((attempt * 2))
    echo "Remote moved between rebase and push; retrying after ${sleep_seconds}s."
    sleep "$sleep_seconds"
  fi
done

echo "::error::Unable to publish writer commit after $max_attempts attempts."
exit 4
